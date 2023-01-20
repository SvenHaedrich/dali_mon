# DALI PY

## Description

This script converts DALI codes into human readable messages. DALI is the digital addressable lighting interface as described [here](https://www.dali-alliance.org).

The source for the DALI code can be one of
* serial port
* Lunatone DALI / USB converter (see: [Lunatone](https://www.lunatone.com/produkt/dali-usb/))

This script is based on the following standards
* IEC 62386-102 control gear
* IEC 62386-103 control device
* IEC 62386-207 LED module DT6
* IEC 62386-208 switching function DT7
* IEC 62386-209 colour control DT8

## Run

```bash
dali_mon [options]
```

## Sample Output

<pre> ./dali_mon < /dev/ttyUSB0
<font color="#26A269">11618.586 |    0.000 |     FF00 | </font><font color="#D0CFCC">BC        OFF</font>
<font color="#26A269">11619.459 |    0.873 |     FF06 | </font><font color="#D0CFCC">BC        RECALL MIN LEVEL</font>
<font color="#26A269">11620.596 |    1.137 |     FF05 | </font><font color="#D0CFCC">BC        RECALL MAX LEVEL</font>
<font color="#26A269">11626.347 |    5.751 |     FF02 | </font><font color="#D0CFCC">BC        DOWN</font>
<font color="#26A269">11626.880 |    0.533 |     FF02 | </font><font color="#D0CFCC">BC        DOWN</font>
<font color="#26A269">11627.332 |    0.452 |     FF02 | </font><font color="#D0CFCC">BC        DOWN</font>
<font color="#26A269">11633.766 |    6.434 |     FF11 | </font><font color="#D0CFCC">BC        GO TO SCENE 1</font>
<font color="#26A269">11635.703 |    1.937 |     FF00 | </font><font color="#D0CFCC">BC        OFF</font>
</pre>

### Commandline Parameters

| Option    | Short | Usage                                                       |
|-----------|-------|-------------------------------------------------------------|
|--help     |       | Show help message and exit.                                 |
|--version  |       | Show the version information and exit.                      |
|--nocolor  |       | Do not use color coding for output.                         |
|--absolute |       | Add absolute local time to output.                          |
|--echo     |       | Echo unprocessed input line to output.                      |
|--lunatone | -l    | Try to use a Lunatone USB connector for DALI communication. |
|--debug    |       | Enable debug level logging.                                 |

### Output Columns
  
* if enabled: absolute timestamp (from host machine)
* timestamp in seconds (from serial message, or host machine for lunatone interface)
* delta time to previous command
* hex data received
* DALI command translation

## Install
```
git clone git@github.com:SvenHaedrich/dali_py.git
```
For the Lunatone USB adapter you need to copy the file `99-lunatone-dali.rules` into the `udev` folder
and reload the `udev` rules.

```
sudo cp 99-lunatone-dali.rules /etc/udev/rules.d/
sudo udevadm control --reload-rules
```
This file grants everyone read/write access.  If you want to restrict access,
you should modify MODE to "0660".  You can then grant access to specific user
accounts by adding them to the plugdev group. Note that some Linux dirstibutions always require a per user permission. To grant permission to a specific user:
```
sudo usermod -a -G plugdev username
```
You will have to log out and then back in for the group change to take effect.

## Tests

To run the tests enter
```
cd tests
./run_tests.sh
```

## DALI frame format for serial input
  
Each DALI frame is expected to use the following format:
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
