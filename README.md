# DALI MON

## Description

This script converts DALI codes into human readable messages. DALI is the digital addressable lighting interface as described [here](https://www.dali-alliance.org).

The source for the DALI code aka frames can be one of
* stdin
* HID class DALI / USB converter (e.g. [Lunatone](https://www.lunatone.com/produkt/dali-usb/))

This script is based on the following standards
* IEC 62386-101:2022 system components
* IEC 62386-102:2022 control gear
* IEC 62386-103:2022 control device
* IEC 62386-207 LED module DT6
* IEC 62386-208 switching function DT7
* IEC 62386-209 colour control DT8

## Run

    dali_mon [options]

## Stop

Use `Ctrl-C` to stop a running instance of `dali_mon`.

## Sample Output

    ./dali_mon < /dev/ttyUSB0
    11618.586 |    0.000 |     FF00 | BC        OFF
    11619.459 |    0.873 |     FF06 | BC        RECALL MIN LEVEL
    11620.596 |    1.137 |     FF05 | BC        RECALL MAX LEVEL
    11626.347 |    5.751 |     FF02 | BC        DOWN
    11626.880 |    0.533 |     FF02 | BC        DOWN
    11627.332 |    0.452 |     FF02 | BC        DOWN
    11633.766 |    6.434 |     FF11 | BC        GO TO SCENE 1
    11635.703 |    1.937 |     FF00 | BC        OFF

## Read from Serial Port

Remember to set the serial port communication parammeters before starting the monitor routine. This example reads from a serial port connected to `ttyUSB0` using a baudrate of 115200 Baud.
```bash
stty -F /dev/ttyUSB0 115200 litout -crtscts
./dali_mon < /dev/ttyUSB0
```

## Commandline Parameters

| Option    | Short | Usage                                               |
|-----------|-------|-----------------------------------------------------|
|--help     |       | Show help message and exit.                         |
|--version  |       | Show the version information and exit.              |
|--nocolor  |       | Do not use color coding for output.                 |
|--absolute |       | Add absolute time from host machine to output.      |
|--echo     |       | Echo unprocessed input line to output.              |
|--hid      | -l    | Use HID class USB connector for DALI communication. |
|--debug    |       | Enable debug level logging.                         |

### Output Columns
  
* if enabled: absolute timestamp (from host machine)
* timestamp in seconds (from serial message, or host machine for USB HID interface)
* delta time to previous command
* hex data received
* DALI command translation

## Install

    git clone git@github.com:SvenHaedrich/dali_mon.git
    cd dali_mon
    python -m venv env

For the Lunatone USB adapter you need to copy the file `99-lunatone-dali.rules` into the `udev` folder
and reload the `udev` rules.

    sudo cp 99-lunatone-dali.rules /etc/udev/rules.d/
    sudo udevadm control --reload-rules

This file grants everyone read/write access.  If you want to restrict access,
you should modify `MODE` to `0660`.  You can then grant access to specific user
accounts by adding them to the plugdev group. Note that some Linux dirstibutions always require a per user permission. To grant permission to a specific user:

    sudo usermod -a -G plugdev username

You will have to log out and then back in for the group change to take effect.

## Address- and Event-Schemes for Control Devices

see [Addressing](Addressing_103.md)

## Tests

see [README.md](tests/README.md)

## DALI frame format for serial input
  
Each DALI frame is expected to use the following format:

    "{" <timestamp> <error> <bits> " " <data> "}"

Only information framed by curly braces is interpreted. <br/>

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

In case of an error state:<br/>

    <bits> : codes the error code
    <data> : contains additional error information

