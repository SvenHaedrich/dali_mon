# DALI MON Tests

## Description

The tests cover the following aspects

1. Correct translation of binary codes into command mnemonics
2. Correct function of the interfaces to the DALI bus

## Run

To run the code interpreter tests enter

    cd source/tests
    ./run_mon.sh --log-level=debug

These tests are completely self-contained.

To run the test for the USB HID device enter

    cd source/tests
    ./run_hid.sh

These tests expect a HID device available at a USB port, also a serial connector.
The two connectors should have their respective DALI ports connected and a bus power supply should be connected as well.

To check formatting, lint and types of the python code with `ruff` and `pyright` enter

    cd source/tests
    ./run_lint.sh

The scripts can be started from any directory, their exit code is the result of the tests or checks.

## Continuous Integration

Every pull request runs `markdownlint`, `run_lint.sh`, and `run_mon.sh` with the oldest supported and a current python version (`.github/workflows/pull-request.yml`).
The tests with hardware (`run_hid.sh`) are not part of it.
