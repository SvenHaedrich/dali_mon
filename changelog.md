# Changelog for `dali_mon`

## Unreleased

- Remove the runtime type checking with `typeguard`, the dependency is removed
- Static type checking with `pyright`, strict for the program and standard for the tests, like `dali-interface`
- `source/tests/run_lint.sh` checks formatting, lint and types
- Every pull request runs `markdownlint`, `run_lint.sh` and the tests without hardware on GitHub
- The exit code of `run_mon.sh` and `run_hid.sh` is the result of the tests, a failing setup stops them
- All decoders take a `DaliFrame`, the decoders for 16 and 24 bit frames use its getters `address_byte`, `instance_byte` and `opcode_byte`
- Device types, eDALI device classes and the address and event types of 24 bit frames are `IntEnum`s with `@unique`
- The decoders for 24 and 32 bit frames use byte and bit operations instead of `bitstring`, the dependency is removed
- Every decoder takes a `DaliFrame` and derives from `DecodedFrame`, whose getters `data()`, `address()`, `command()`, `standard()` and `reference()` give the texts of the frame; `Decode` chooses the decoder by the frame length and keeps it in `dali_frame`, the device type for the next frame in `next_device_type`.
  The command tables hold tuples of command, standard and clause, `DecodedFrame.lookup` finds a command in them
- `MonitorState` holds the output options of `dali_mon` (`--absolute`, `--echo` and the shown references) and what is kept from frame to frame; `dali_mon` creates it and passes it to the functions instead of using globals
- Each command shows the standard that defines it (e.g. `IEC 62386-102:2022`) and the clause, in columns with fixed width; `eDALI` for eDALI frames
- `--no-standard`, `--no-clause` and `--no-reference` hide these columns
- `SAVE PERSISTENT VARIABLES`, removed in the current editions, refers to IEC 62386-102:2014 and IEC 62386-103:2014
- Uniform number formats: hex values in upper case, binary values with a trailing `b` (also the DTR of 24 bit frames), `SEARCHADDRH/M/L (0x..)` in brackets also in 16 bit frames, no double spaces within a command (`PHYSICAL SELECTION (DEPRECATED)`)
- Fix the clauses of `QUERY LAMP FAILURE` (11.5.5) and `QUERY PHYSICAL MINIMUM` (11.5.14) of IEC 62386-102
- Fix the command names `QUERY CATCHING`, `SET REPORT TIMER (DTR0) - TYPE 303` and `CANCEL HOLD TIMER - TYPE 303` of IEC 62386-303

## Version 1.8.0

- Replace the git submodule `dali_interface` by the python package [dali-interface](https://github.com/sevenlab-de/dali-interface) v2.0.0
- Track version and dependencies in `pyproject.toml`, `requirements.txt` is removed
- Fix the crash of `--absolute`
- ENABLE DEVICE TYPE only changes the meaning of the application extended commands 0xE0 to 0xFF, and stays active until the next command for control gear
- `--help` shows the description of `dali_mon` again
- `--version` and the usage line show the program name `dali_mon` instead of `dali_mon.py`
- Fix typos in the output: `CONTINUOUS UP/DOWN`, `COLOUR TEMPERATURE TC STEP WARMER`, `QUERY PARAMETER`, and the eDALI addresses (`BC UN` instead of `BC una`, single spaces)
- The udev rule is `70-lunatone-dali.rules` and grants access with `TAG+="uaccess"` instead of `MODE="0666"`
- Serial port, USB converter, and a serial device piped into `dali_mon` keep listening until `Ctrl-C`.
  A lost connection is reported with `connection lost` and exit code 1, instead of hanging or using 100 % CPU.
  A piped file ends at the end of the file with exit code 0.
- Messages go to stderr, the decoded frames to stdout
- `dali_mon` can be started from any directory, and passes arguments with spaces unchanged
- `--echo` also works with `--serial-port`, and is rejected together with `--hid`
- `Ctrl-C` ends `dali_mon` with exit code 130
- Wrong command line parameters end `dali_mon` with exit code 2: `--hid` together with `--serial-port`, `--on` together with `--off`, `--on` or `--off` without `--hid`, and a serial port that does not exist
- `power control not supported` ends `dali_mon` with exit code 1
- A serial port or USB converter that cannot be opened is reported with `cannot open ...` and exit code 1, instead of a python traceback
- 24 bit frames: broadcast instance addresses are separated by a comma (e.g. `BC DEV,BC INST`), the address column is 22 characters wide to fit the longest address

## Version 1.7.0

- Generate no output when lines without DALI information are encountered
- Support --echo for piped file input.
  Fixes: <https://github.com/SvenHaedrich/dali_mon/issues/32>
- Fixes: <https://github.com/SvenHaedrich/dali_mon/issues/31>
