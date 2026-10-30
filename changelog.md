# Changelog for `dali_mon`

## Unreleased

- Replace the git submodule `dali_interface` by the python package [dali-interface](https://github.com/sevenlab-de/dali-interface) v2.0.0
- Track version and dependencies in `pyproject.toml`, `requirements.txt` is removed
- Fix the crash of `--absolute`
- ENABLE DEVICE TYPE only changes the meaning of the application extended commands 0xE0 to 0xFF,
  and stays active until the next command for control gear
- `--help` shows the description of `dali_mon` again
- Serial port, USB converter, and a serial device piped into `dali_mon` keep listening until `Ctrl-C`.
  A lost connection is reported with `connection lost` and exit code 1, instead of hanging or
  using 100 % CPU. A piped file ends at the end of the file with exit code 0.
- Messages go to stderr, the decoded frames to stdout
- `dali_mon` can be started from any directory, and passes arguments with spaces unchanged
- `--echo` also works with `--serial-port`, and is rejected together with `--hid`
- `Ctrl-C` ends `dali_mon` with exit code 130
- Wrong command line parameters end `dali_mon` with exit code 2: `--hid` together with `--serial-port`,
  `--on` together with `--off`, `--on` or `--off` without `--hid`, and a serial port that does not exist
- `power control not supported` ends `dali_mon` with exit code 1
- A serial port or USB converter that cannot be opened is reported with `cannot open ...` and exit code 1,
  instead of a python traceback
- 24 bit frames: broadcast instance addresses are separated by a comma (e.g. `BC DEV,BC INST`),
  the address column is 22 characters wide to fit the longest address

## Version 1.7.0

- Generate no output when lines without DALI information are encountered
- Support --echo for piped file input. Fixes: <https://github.com/SvenHaedrich/dali_mon/issues/32>
- Fixes: <https://github.com/SvenHaedrich/dali_mon/issues/31>
