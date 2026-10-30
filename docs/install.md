# Install

    git clone https://github.com/SvenHaedrich/dali_mon.git
    cd dali_mon

The script `dali_mon` creates a virtual environment `.venv` on its first run and installs the dependencies listed in `pyproject.toml`.
The DALI interfaces are accessed through the python package [dali-interface](https://github.com/sevenlab-de/dali-interface), which is installed from its GitHub release tag, so the first run needs access to GitHub.

## HID-USB Support

For the Lunatone USB adapter you need to copy the file `70-lunatone-dali.rules` into the `udev` folder, reload the `udev` rules and apply them to a connected adapter.

    sudo cp 70-lunatone-dali.rules /etc/udev/rules.d/
    sudo udevadm control --reload-rules
    sudo udevadm trigger --attr-match=idVendor=17b5

The rule grants access to the user logged in locally at the computer (`TAG+="uaccess"`), no group membership and no new login are needed.
The file name must sort before `73-seat-late.rules`, which evaluates this tag, so keep the number `70` when you rename the file.

`uaccess` does not grant access to users logged in remotely, e.g. via `ssh`.
For them, replace `TAG+="uaccess"` by `GROUP="plugdev", MODE="0660"` in the rule and add the users to the `plugdev` group:

    sudo usermod -a -G plugdev username

They have to log out and back in for the group change to take effect.
