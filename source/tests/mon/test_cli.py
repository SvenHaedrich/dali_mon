import re
import subprocess
import tomllib
from pathlib import Path

import dali_mon
import pytest
from click.testing import CliRunner
from dali_interface import DaliFrame, DaliSerial, DaliStatus

REPOSITORY = Path(__file__).resolve().parents[3]
SAMPLE = REPOSITORY / "source" / "tests" / "sample.txt"
# no colour codes, and no environment variable selects an interface
ENVIRONMENT = {"NO_COLOR": "1", "DALI_HID_USB": None, "DALI_SERIAL_PORT": None}


def run_cli(args: list[str], input: str = "", env: dict | None = None):
    environment = dict(ENVIRONMENT)
    environment.update(env or {})
    return CliRunner().invoke(dali_mon.dali_mon, args, input=input, env=environment)


def output_lines(result) -> list[str]:
    # split at "\n" only, messages after Ctrl-C start with "\r" to overwrite "^C"
    return result.output.split("\n")[:-1]


def project_version() -> str:
    with (REPOSITORY / "pyproject.toml").open("rb") as pyproject:
        return tomllib.load(pyproject)["project"]["version"]


class FakeConnection:
    """Stands in for DaliUsb and DaliSerial, returns the given frames and then
    raises KeyboardInterrupt like Ctrl-C does."""

    def __init__(self, frames=(), power_supported=True, error=None):
        self.frames = list(frames)
        self.power_supported = power_supported
        self.error = error
        self.power_calls = []
        self.closed = False

    def get(self, timeout=None):
        if self.frames:
            return self.frames.pop(0)
        if self.error:
            raise self.error
        raise KeyboardInterrupt

    def power(self, power=False):
        if not self.power_supported:
            raise RuntimeError("usb device must implement power")
        self.power_calls.append(power)

    def close(self):
        self.closed = True


@pytest.fixture
def usb(monkeypatch):
    connection = FakeConnection()
    connection.opened = False

    def open_usb():
        connection.opened = True
        return connection

    monkeypatch.setattr(dali_mon, "DaliUsb", open_usb)
    return connection


@pytest.fixture
def serial(monkeypatch):
    connection = FakeConnection()
    connection.port = None

    class FakeSerial:
        parse = staticmethod(DaliSerial.parse)

        def __new__(cls, port):
            connection.port = port
            return connection

    monkeypatch.setattr(dali_mon, "DaliSerial", FakeSerial)
    return connection


@pytest.fixture
def port(tmp_path) -> str:
    # dali_mon checks that the serial port exists
    path = tmp_path / "ttyDALI"
    path.touch()
    return str(path)


def frame(timestamp: float, length: int, data: int) -> DaliFrame:
    return DaliFrame(
        timestamp=timestamp, length=length, data=data, status=DaliStatus.FRAME
    )


# ---- help and version


def test_version():
    result = run_cli(["--version"])
    assert result.exit_code == 0
    assert project_version() in result.output


@pytest.mark.parametrize(
    "option",
    [
        "--version",
        "--hid",
        "-l",
        "--echo",
        "--absolute",
        "--on",
        "--off",
        "--serial-port",
        "-s",
    ],
)
def test_help_lists_option(option):
    result = run_cli(["--help"])
    assert result.exit_code == 0
    assert re.search(rf"(^|[ ,]){option}\b", result.output, re.MULTILINE)


def test_help_hides_debug():
    result = run_cli(["--help"])
    assert "--debug" not in result.output


@pytest.mark.parametrize("variable", ["DALI_HID_USB", "DALI_SERIAL_PORT"])
def test_help_shows_environment_variable(variable):
    result = run_cli(["--help"])
    assert variable in result.output


def test_help_shows_description():
    result = run_cli(["--help"])
    assert "Monitor for DALI commands." in result.output


# the wrapper script is what users run, so its options for python matter
def test_wrapper_help_shows_description():
    result = subprocess.run(
        ["./dali_mon", "--help"],
        cwd=REPOSITORY,
        capture_output=True,
        check=False,
        text=True,
        timeout=300,
    )
    assert result.returncode == 0
    assert "Monitor for DALI commands." in result.stdout


def test_wrapper_version():
    result = subprocess.run(
        ["./dali_mon", "--version"],
        cwd=REPOSITORY,
        capture_output=True,
        check=False,
        text=True,
        timeout=300,
    )
    assert result.returncode == 0
    assert project_version() in result.stdout


# ---- input from stdin


def test_sample_file():
    result = run_cli([], input=SAMPLE.read_text())
    assert result.exit_code == 0
    assert output_lines(result) == [
        "0.001 |    0.000 |     FF06 | BC GEAR              RECALL MIN LEVEL",
        "0.002 |    0.001 |     FF05 | BC GEAR              RECALL MAX LEVEL",
        "0.003 |    0.001 |     0102 | G00                  DOWN",
        "0.004 |    0.001 |     0102 | G00                  DOWN",
        "0.005 |    0.001 |     0100 | G00                  OFF",
        "0.006 |    0.001 | ERROR: SYSTEM FAILURE",
        "0.007 |    0.001 | SYSTEM RECOVER",
    ]


def test_delta_time():
    result = run_cli([], input="{000003E8:10 FF06}\n{00000BB8:10 FF05}\n")
    assert output_lines(result) == [
        "1.000 |    0.000 |     FF06 | BC GEAR              RECALL MIN LEVEL",
        "3.000 |    2.000 |     FF05 | BC GEAR              RECALL MAX LEVEL",
    ]


def test_lines_without_dali_information_are_ignored():
    text = "*** Booting Zephyr OS ***\n\n{00000001:10 FF06}\nno frame here\n"
    result = run_cli([], input=text)
    assert output_lines(result) == [
        "0.001 |    0.000 |     FF06 | BC GEAR              RECALL MIN LEVEL",
    ]


def test_echo():
    text = "*** Booting Zephyr OS ***\n{00000001:10 FF06}\n"
    result = run_cli(["--echo"], input=text)
    assert output_lines(result) == [
        "*** Booting Zephyr OS ***",
        "{00000001:10 FF06}",
        "0.001 |    0.000 |     FF06 | BC GEAR              RECALL MIN LEVEL",
    ]


def test_absolute_time():
    result = run_cli(["--absolute"], input=SAMPLE.read_text())
    assert result.exit_code == 0
    lines = output_lines(result)
    assert len(lines) == 7
    for line in lines:
        assert re.match(r"\d\d:\d\d:\d\d \| \d+\.\d{3} \| ", line)


# ---- input from the interfaces


def test_hid(usb):
    usb.frames = [frame(1.0, 16, 0xFF06), frame(1.25, 8, 0x12)]
    result = run_cli(["--hid"])
    assert output_lines(result) == [
        "1.000 |    0.000 |     FF06 | BC GEAR              RECALL MIN LEVEL",
        "1.250 |    0.250 |       12 |                      DATA 0x12 =  18 = 00010010b",
        "\rinterrupted",
    ]
    assert usb.closed


def test_hid_short_option(usb):
    usb.frames = [frame(1.0, 16, 0xFF06)]
    result = run_cli(["-l"])
    assert "RECALL MIN LEVEL" in result.output
    assert usb.closed


def test_hid_environment_variable(usb):
    usb.frames = [frame(1.0, 16, 0xFF06)]
    result = run_cli([], env={"DALI_HID_USB": "1"})
    assert "RECALL MIN LEVEL" in result.output
    assert usb.closed


def test_hid_error_frame(usb):
    usb.frames = [
        DaliFrame(
            timestamp=2.0,
            status=DaliStatus.TIMING,
            message="ERROR TIMING: CORRUPT FRAME",
        )
    ]
    result = run_cli(["--hid"])
    assert output_lines(result)[0] == "2.000 |    0.000 | ERROR TIMING: CORRUPT FRAME"


@pytest.mark.parametrize("option", ["--serial-port", "-s"])
def test_serial_port(serial, port, option):
    serial.frames = [frame(0.001, 16, 0xFF06)]
    result = run_cli([option, port])
    assert serial.port == port
    assert output_lines(result) == [
        "0.001 |    0.000 |     FF06 | BC GEAR              RECALL MIN LEVEL",
        "\rinterrupted",
    ]
    assert serial.closed


def test_serial_port_environment_variable(serial, port):
    serial.frames = [frame(0.001, 16, 0xFF06)]
    result = run_cli([], env={"DALI_SERIAL_PORT": port})
    assert serial.port == port
    assert "RECALL MIN LEVEL" in result.output


@pytest.mark.parametrize("option,power", [("--on", True), ("--off", False)])
def test_power(usb, option, power):
    run_cli(["--hid", option])
    assert usb.power_calls == [power]


def test_power_not_supported(usb):
    usb.power_supported = False
    usb.frames = [frame(1.0, 16, 0xFF06)]
    result = run_cli(["--hid", "--on"])
    assert result.exit_code == 1
    assert output_lines(result) == ["\rpower control not supported"]
    assert usb.closed


def test_connection_lost(usb):
    usb.frames = [frame(1.0, 16, 0xFF06)]
    error = RuntimeError("read thread is not running")
    error.__cause__ = OSError("Input/Output Error")
    usb.error = error
    result = run_cli(["--hid"])
    assert output_lines(result)[-1] == "\rconnection lost: Input/Output Error"
    assert usb.closed


# ---- command line parameter errors
# click reports usage errors with exit code 2


def test_unknown_option():
    result = run_cli(["--unknown"])
    assert result.exit_code == 2
    assert "No such option" in result.output


def test_unexpected_argument():
    result = run_cli(["unexpected"])
    assert result.exit_code == 2
    assert "unexpected extra argument" in result.output


@pytest.mark.parametrize("option", ["--serial-port", "-s"])
def test_serial_port_without_port(option):
    result = run_cli([option])
    assert result.exit_code == 2
    assert "requires an argument" in result.output


def test_serial_port_does_not_exist(serial):
    result = run_cli(["--serial-port", "/dev/does-not-exist"])
    assert result.exit_code == 2
    assert "/dev/does-not-exist" in result.output
    assert serial.port is None


def test_invalid_hid_environment_variable(usb):
    result = run_cli([], env={"DALI_HID_USB": "maybe"})
    assert result.exit_code == 2
    assert "not a valid boolean" in result.output
    assert not usb.opened


@pytest.mark.parametrize("hid_option", ["--hid", "-l"])
@pytest.mark.parametrize("serial_option", ["--serial-port", "-s"])
def test_hid_and_serial_port_exclude_each_other(
    usb, serial, port, hid_option, serial_option
):
    result = run_cli([hid_option, serial_option, port])
    assert result.exit_code == 2
    assert "Error" in result.output
    assert "--hid" in result.output
    assert "--serial-port" in result.output
    assert not usb.opened
    assert serial.port is None


def test_on_and_off_exclude_each_other(usb):
    result = run_cli(["--hid", "--on", "--off"])
    assert result.exit_code == 2
    assert "--on" in result.output
    assert "--off" in result.output
    assert not usb.opened


# only the USB converters have a power supply to switch
@pytest.mark.parametrize("option", ["--on", "--off"])
def test_power_without_interface(option):
    result = run_cli([option], input=SAMPLE.read_text())
    assert result.exit_code == 2
    assert option in result.output
    assert "--hid" in result.output


@pytest.mark.parametrize("serial_option", ["--serial-port", "-s"])
@pytest.mark.parametrize("option", ["--on", "--off"])
def test_power_with_serial_port(serial, port, serial_option, option):
    result = run_cli([serial_option, port, option])
    assert result.exit_code == 2
    assert option in result.output
    assert "--hid" in result.output
    assert serial.port is None


@pytest.mark.parametrize("option", ["--on", "--off"])
def test_power_with_serial_port_environment_variable(serial, port, option):
    result = run_cli([option], env={"DALI_SERIAL_PORT": port})
    assert result.exit_code == 2
    assert option in result.output
    assert "--hid" in result.output
    assert serial.port is None


@pytest.mark.parametrize("option,power", [("--on", True), ("--off", False)])
def test_power_with_hid_environment_variable(usb, option, power):
    run_cli([option], env={"DALI_HID_USB": "1"})
    assert usb.power_calls == [power]


# the wrapper script passes the exit code on
def test_wrapper_returns_exit_code():
    result = subprocess.run(
        ["./dali_mon", "--unknown"],
        cwd=REPOSITORY,
        capture_output=True,
        check=False,
        text=True,
        timeout=300,
    )
    assert result.returncode == 2
    assert "No such option" in result.stderr
