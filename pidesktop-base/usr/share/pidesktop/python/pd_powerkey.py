#!/usr/bin/env python3
#
# pd_powerkey.py - monitor GPIO to detect power key press from Power MCU (PCU)
#

from pidesktop import PiDesktop


if __name__ == "__main__":
    pd = PiDesktop()
    pd.power_key()
