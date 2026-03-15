#!/usr/bin/env python3
#
# pd_clonessd.py
#

from .pidesktop import PiDesktop


if __name__ == "__main__":
    pd = PiDesktop()
    pd.check_sd()
