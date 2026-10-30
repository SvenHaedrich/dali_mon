# Changelog for `dali_mon`

## Unreleased

- Replace the git submodule `dali_interface` by the python package [dali-interface](https://github.com/sevenlab-de/dali-interface) v2.0.0
- Report a lost connection to a serial port or USB converter instead of crashing

## Version 1.7.0

- Generate no output when lines without DALI information are encountered
- Support --echo for piped file input. Fixes: <https://github.com/SvenHaedrich/dali_mon/issues/32>
- Fixes: <https://github.com/SvenHaedrich/dali_mon/issues/31>
