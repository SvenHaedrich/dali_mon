# DALI PY

## Description

This skript takes input from a serial port and converts the information into
human readable DALI command descriptions.

## Usage

```bash
python source/main.py [options]
```
### Commandline Parameters
--absolute        : add stamp with absolute time
--file, -f <name> : send file e.g. --file cmds/bc_on.cmd
--help, -h        : help
--nocolor         : don't use colors
--port, -p <port> : set serial port e.g. --port /dev/ttyUSB0
--transparent     : print all input lines
--version, -v     : show version information

### Output Columns
  
* if enabled: absolute timestamp (from host machine)
* timestamp in seconds (from interface)
* delta time to previous command
* hex data received
* DALI command translation

## Run

```bash
source ~/Repos/dali_py/venv/bin/activate
python source/main.py --port /dev/ttyUSB2
```
