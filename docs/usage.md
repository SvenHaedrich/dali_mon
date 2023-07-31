# Usage

## Run

    dali_mon [options]

## Stop

Use `Ctrl-C` to stop a running instance of `dali_mon`.

## Sample Output

    ./dali_mon < tests/sample.txt
    0.001 |    0.000 |     FF06 | BC GEAR     RECALL MIN LEVEL
    0.002 |    0.001 |     FF05 | BC GEAR     RECALL MAX LEVEL
    0.003 |    0.001 |     0102 | G00         DOWN
    0.004 |    0.001 |     0102 | G00         DOWN
    0.005 |    0.001 |     0100 | G00         OFF
    0.006 |    0.001 | ERROR: SYSTEM FAILURE
    0.007 |    0.001 | ERROR: SYSTEM RECOVER

You can remove the colour control codes from the output stream using `ansifilter`.

    ./dali_mon < tests/sample.txt | ansifilter

## Read from Serial Port

Remember to set the serial port communication parammeters before starting the monitor routine. This example reads from a serial port connected to `ttyUSB0` using a baudrate of 115200 Baud.

    stty -F /dev/ttyUSB0 115200
    ./dali_mon < /dev/ttyUSB0

## Commandline Parameters

| Option    | Short | Usage                                               |
|-----------|-------|-----------------------------------------------------|
|--help     |       | Show help message and exit.                         |
|--version  |       | Show the version information and exit.              |
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


