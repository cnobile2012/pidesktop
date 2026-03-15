#!/usr/bin/env python3
#
# brute force
#

from .pidesktop import PiDesktop


if __name__ == "__main__":
    pd = PiDesktop()
    pd.update(pd.CONF_KEY, pd.VALUE_CONF)
    pd.update(pd.PIN_KEY, pd.VALUE_PIN_6)
    # pd.update(pd.PIN_KEY, pd.VALUE_PIN_13)
    pd.update_hwclock_set()
    pd.remove_fake_hwclock()
