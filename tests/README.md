# DALI MON Tests

## Description

The tests cover the following aspects
1. Correct translation of binary codes into command memonics
2. Correct function of the interfaces to the DALI bus

## Run 

To run the code interpreter tests enter

    cd tests
    ./run_mon.sh

These tests are completely self-contained.

To run the test for the USB HID device enter

    cd tests
    ./run_hid.sh

Theses tests expect a HID device available at a USB port, also a serial connector. The two connetcors should have their respective DALI ports connected and a bus power supply should be connected as well.
