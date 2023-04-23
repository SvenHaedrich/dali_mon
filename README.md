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
* IEC 62386-105:2020 firmware transfer (not supported by USB converter)
* IEC 62386-207 LED module DT6
* IEC 62386-208 switching function DT7
* IEC 62386-209 colour control DT8

## Further Documents

[General usage](docs/usage.md)
[Address representation](docs/addressing.md)
[Installation and HID-USB support](docs/install.md)
[Serial port and input format](docs/serial.md)
[Tests](tests/README.md)
