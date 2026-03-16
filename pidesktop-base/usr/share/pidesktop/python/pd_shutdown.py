#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# pd_shutdown.py - oneshot service so do your thing and exit
#
# We are in shutdown processing either because shutdown or reboot is running
# or because the power button was pressed.  If we're here because the power
# button was pressed then Power MCU is already in Waiting OFF state and will
# turn off immediately if it sees pin 31 go high so avoid that! If power
# button has not been pressed we should inform power MCU  shutdown/reboot is
# taking place so the shutdown timer can start.
#
# Note: The timer will reset when the Pi powers off so the only purpose
# REALLY for doing this is to capture the current system time in the real
# time clock.
import os
import sys

PWD = os.path.abspath(__file__)
BASE_DIR = os.path.dirname(PWD)
sys.path.append(BASE_DIR)

from pidesktop import PiDesktop


if __name__ == "__main__":
    pd = PiDesktop()
    pd.shutdown()
