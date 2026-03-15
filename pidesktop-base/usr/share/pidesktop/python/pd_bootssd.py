#!/usr/bin/env python3
#
# pd_bootssd.py
#

import logging
import os
import sys

PWD = os.path.abspath(__file__)
BASE_DIR = os.path.dirname(PWD)
sys.path.append(BASE_DIR)

from . import Logger


class BootSSDManager(Logger):
    """
    Boot the ssd.
    """
    _LOGGER_NAME = 'pidesktop'
    _LOG_PATH = '/var/log'

    def __init__(self):
        Logger().config(logger_name=self._LOGGER_NAME,
                        file_path=self._LOG_PATH)
        self._log = logging.getLogger(self._LOGGER_NAME)
        self._log.info("BootSSDManager initializing ...")

    def runask(self):
        ask = ("Do you want to change the file system from SD card to "
               "SSD?\nIf 'YES',please make sure the 'SD Card Copier' execute "
               "correctly.(y/N): ")
        answer = input(ask)

        if answer.upper() in ('Y', 'YES'):
            self._update_boot()

    def _update_boot(self):
        filename = '/boot/cmdline.txt'

        with open(filename, 'r') as fr:
            key = 'root='
            value = "root=/dev/sda2"
            lines = fr.readlines()
            new_value = ''
            update = False

            for line in lines:
                if line:
                    strps = line.split(" ")

                    for v in strps:
                        if v.startswith(key) and v != value:
                            new_value += f"{value} "
                            update = True
                        else:
                            new_value += f"{v} "

            if update:
                with open(filename, 'w') as fw:
                    fw.write(new_value.strip())

            self._reboot()

    def _reboot(self):
        ask = ("To put the new configuration into effect, you need to restart "
               "the system.\nDo you want to reboot now? (Y/n): ")
        answer = input(ask)

        if answer.upper() in ('N', 'NO'):
            print("Not restarting now.")
        else:
            os.popen("sudo reboot")


if __name__ == "__main__":
    m = BootSSDManager()
    m.runask()
