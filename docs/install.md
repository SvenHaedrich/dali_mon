# Install

    git clone git@github.com:SvenHaedrich/dali_mon.git
    cd dali_mon
    git submodule update --init

## HID-USB Support

For the Lunatone USB adapter you need to copy the file `99-lunatone-dali.rules` into the `udev` folder
and reload the `udev` rules.

    sudo cp 99-lunatone-dali.rules /etc/udev/rules.d/
    sudo udevadm control --reload-rules

This file grants everyone read/write access.  If you want to restrict access,
you should modify `MODE` to `0660`.  You can then grant access to specific user
accounts by adding them to the plugdev group. Note that some Linux dirstibutions always require a per user permission. To grant permission to a specific user:

    sudo usermod -a -G plugdev username

You will have to log out and then back in for the group change to take effect.
