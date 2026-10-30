# Usage

## Run

    dali_mon [options]

## Stop

Use `Ctrl-C` to stop a running instance of `dali_mon`.

When reading from a serial port, a USB converter, or a serial device piped into `dali_mon`,
the monitor keeps listening until you press `Ctrl-C`. A connection that ends, e.g. because the
converter is unplugged, is never expected: `dali_mon` reports `connection lost` and ends with an error.
Only a file piped into `dali_mon` ends at the end of the file without an error.

The decoded frames are written to stdout, messages like `interrupted` or `connection lost` to stderr.
So you can log the frames without the messages:

    ./dali_mon -s /dev/ttyUSB0 > dali.log

## Exit Codes

| Code | Meaning                                                                      |
|------|------------------------------------------------------------------------------|
| 0    | end of the file piped into `dali_mon`                                        |
| 1    | interface cannot be opened, connection lost, or power control not supported |
| 2    | wrong command line parameters                                                |
| 130  | stopped with `Ctrl-C`                                                        |

## Sample Output

    ./dali_mon < source/tests/sample.txt
    0.001 |    0.000 |     FF06 | BC GEAR                RECALL MIN LEVEL
    0.002 |    0.001 |     FF05 | BC GEAR                RECALL MAX LEVEL
    0.003 |    0.001 |     0102 | G00                    DOWN
    0.004 |    0.001 |     0102 | G00                    DOWN
    0.005 |    0.001 |     0100 | G00                    OFF
    0.006 |    0.001 | ERROR: SYSTEM FAILURE
    0.007 |    0.001 | SYSTEM RECOVER

You can remove the colour control codes from the output stream using `ansifilter`.

    ./dali_mon < source/tests/sample.txt | ansifilter

## Read from Serial Port

There are two options to read DALI frames from a serial device.
The first option is to open a pipe from the serial port. Remember that you have to initialize the serial port to use the correct baudrate, 
This example reads from a serial port connected to `ttyUSB0` using a baudrate of 115200 Baud.
`-echo` keeps the serial device from sending the received lines back to the adapter.

    stty -F /dev/ttyUSB0 115200 -echo
    ./dali_mon < /dev/ttyUSB0

A serial device piped into `dali_mon` behaves like the `serial-port` parameter: `dali_mon` keeps
listening until `Ctrl-C`, and ends with `connection lost` when the device disappears.
Serial data that is passed through another program (e.g. `ssh host cat /dev/ttyUSB0 | ./dali_mon`)
arrives as a pipe and is treated like a file: `dali_mon` ends without an error when the pipe ends.

The other option is to use the `serial-port` command line parameter.
Note that the default baudrate of 500,000 baud will be used, and that the port must exist:

    ./dali_mon --serial-port /dev/ttyUSB0

Alternatively, you can use the short form of the same parameter.

    ./dali_mon -s /dev/ttyUSB0

Or, you can store the serial port into an environment variable and use the ususal approach to make this a permanent setting.

    export DALI_SERIAL_PORT=/dev/ttyUSB0
    ./dali_mon
    
## Using Lunatone and compatible devices

Supported are:
* Lunatone 241 389 23DO
* Lunatone 241 389 23-30
* BEGA 71024

You can use `dali_mon` with HID class USB connectors, like the devices from Lunatone.

    ./dali_mon --hid

Alternatively, set the environment variable `DALI_HID_USB`:

    export DALI_HID_USB=1
    ./dali_mon

These devices provide no independent clock, so timestamps are generated using the clock
information of the host computer.
Some of these devices can act as DALI power supply. To enable this integrated power supply use:

    ./dali_mon --hid --on

To disable the power supply use:

    ./dali_mon --hid --off

`--on` and `--off` need `--hid`, the serial port has no power supply to switch.
If the USB converter has no integrated power supply, `dali_mon` reports
`power control not supported` and ends with an error.


## Commandline Parameters

| Option              | Short | Usage                                               |
|---------------------|-------|-----------------------------------------------------|
|--help               |       | Show help message and exit.                         |
|--version            |       | Show the version information and exit.              |
|--absolute           |       | Add absolute time from host machine to output.      |
|--serial-port <port> | -s    | Use the serial port for DALI communication          |
|--echo               |       | Echo unprocessed input line to output.              |
|--hid                | -l    | Use HID class USB connector for DALI communication. |
|--debug              |       | Enable debug level logging.                         |
|--on                 |       | Enable power supply (if available), needs `--hid`.  |
|--off                |       | Disable power supply (if available), needs `--hid`. |

These combinations are rejected with exit code 2:

* `--hid` together with `--serial-port`. An option given on the command line overrides the
  environment variable of the other one, e.g. `--hid` overrides `DALI_SERIAL_PORT`.
* `--on` together with `--off`.
* `--on` or `--off` without `--hid`.
* `--serial-port` with a port that does not exist.

### Output Columns
  
* if enabled: absolute timestamp (from host machine)
* timestamp in seconds (from serial message, or monotonic clock of the host machine for USB HID interface)
* delta time to previous command
* hex data received
* DALI command translation


