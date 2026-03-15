#!/user/bin/env python3
#
# pd_reboot.py - oneshot service so do your thing and exit
#
# We are in reboot processing because reboot is running.
#
import os
import sys

PWD = os.path.abspath(__file__)
BASE_DIR = os.path.dirname(PWD)
sys.path.append(BASE_DIR)

from .pidesktop import PiDesktop


if __name__ == "__main__":
    pd = PiDesktop()
    pd.reboot()
