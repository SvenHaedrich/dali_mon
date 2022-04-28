# DALI PY

## Description

This script takes input from a serial port and converts the information into
human readable DALI command descriptions.

## Usage

```bash
python source/main.py [options]
```
### Commandline Parameters
--absolute        : add stamp with absolute time <br/>
--file, -f <name> : send file e.g. --file cmds/bc_on.cmd <br/>
--help, -h        : help <br/>
--nocolor         : don't use colors <br/>
--port, -p <port> : set serial port e.g. --port /dev/ttyUSB0 <br/>
--transparent     : print all input lines <br/>
--version, -v     : show version information <br/>

### Output Columns
  
* if enabled: absolute timestamp (from host machine)
* timestamp in seconds (from interface)
* delta time to previous command
* hex data received
* DALI command translation

### Expected DALI frame format
  
Each DALI frame should use the following format:
  
"{" <timestamp> <error> <bits> " " <data> "}"

Only information framed by curly barces is interpreted. <br/>
<timestamp> : integer number, each tick represents 1 millisecond, number is given in hex presentation, fixed length of 8 digits<br/>
<error> : either a "-" (minus) indicating normal state, or "*" (asteriks) inidcating an error<br/>
<bits> : number of data bits received, number is given in hex presentation, fixed length of 2 digits<br/>
<data> : received data payload, number is given in hex presentation, fixed length of 8 digits<br/> 
  
## Run

```bash
source ~/Repos/dali_py/venv/bin/activate
python source/main.py --port /dev/ttyUSB2
```
