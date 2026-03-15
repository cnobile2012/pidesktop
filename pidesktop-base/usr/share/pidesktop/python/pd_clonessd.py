#!/usr/bin/env python3
#
# pd_clonessd.py
#
import os
import sys

PWD = os.path.abspath(__file__)
BASE_DIR = os.path.dirname(PWD)
sys.path.append(BASE_DIR)

from .pidesktop import PiDesktop


if __name__ == "__main__":
    pd = PiDesktop()
    pd.check_sd()
