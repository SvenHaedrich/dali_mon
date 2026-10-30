# Install

    git clone https://github.com/SvenHaedrich/dali_mon.git
    cd dali_mon

The script `dali_mon` creates a virtual environment `.venv` on its first run and installs
the dependencies listed in `pyproject.toml`. The DALI interfaces are accessed through the
python package [dali-interface](https://github.com/sevenlab-de/dali-interface), which is
installed from its GitHub release tag, so the first run needs access to GitHub.

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
