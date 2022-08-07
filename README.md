# DALI PY

## Description

This script takes input from a serial port and converts the information into
human readable DALI command descriptions.

## Usage

```bash
python source/main.py [options]
```
### Commandline Parameters
```
--absolute        : add stamp with absolute time
--file, -f <name> : send file e.g. --file cmds/bc_on.cmd
--help, -h        : help
--nocolor         : don't use colors
--port, -p <port> : set serial port e.g. --port /dev/ttyUSB0
--transparent     : print all input lines
--version, -v     : show version information
```
### Output Columns
  
* if enabled: absolute timestamp (from host machine)
* timestamp in seconds (from interface)
* delta time to previous command
* hex data received
* DALI command translation

### Expected DALI frame format
  
Each DALI frame has to use the following format:
```
"{" <timestamp> <error> <bits> " " <data> "}"
```
Only information framed by curly braces is interpreted. <br/>
```
<timestamp> : integer number, 
              each tick represents 1 millisecond, 
              number is given in hex presentation, 
              fixed length of 8 digits
<error>     : either a 
              "-" (minus) indicating normal state, or 
              "*" (asteriks) inidcating an error
<bits>      : data bits received, 
              number is given in hex presentation, 
              fixed length of 2 digits
<data>      : received data payload, 
              number is given in hex presentation, 
              fixed length of 8 digits
```
In case of an error state:<br/>
```
<bits> : codes the error code
<data> : contains additional error information
```   
## Install
```bash
git clone git@github.com:SvenHaedrich/dali_py.git
```
## Run

```bash
cd dali_py
python source/main.py --port /dev/ttyUSB2
```
