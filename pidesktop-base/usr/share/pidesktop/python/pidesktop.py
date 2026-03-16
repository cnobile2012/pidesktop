# -*- coding: utf-8 -*-
#
# pidesktop.py
#
__docformat__ = "restructuredtext en"

import logging
import os
import shlex
import sys
import time
import lgpio

from subprocess import run as sp_run, Popen, PIPE

from logger import Logger


class PiDesktop:
    """
    Support for the Desktop Case supporting software sold by
    http://www.element14.com.
    """
    _LOGGER_NAME = 'pidesktop'
    _LOG_PATH = os.path.join('/var/log', _LOGGER_NAME + '.log')
    _BOOT_CONF_FILE = '/boot/firmware/config.txt'

    PIN_KEY = 'gpio'
    CONF_KEY = 'dtoverlay'
    VALUE_PIN_6 = '6=op,pn,dl'
    VALUE_PIN_13 = '13=ip'
    VALUE_CONF = 'i2c-rtc,pcf8563'

    def __init__(self):
        Logger().config(logger_name=self._LOGGER_NAME,
                        file_path=self._LOG_PATH)
        self._log = logging.getLogger(self._LOGGER_NAME)
        self._log.info("PiDesktop initializing ...")

    def run_command(self, cmd):
        """
        Run a shell command.
        """
        self._log.info("Running run_command: %s", cmd)
        cmd_list = shlex.split(cmd) if isinstance(cmd, str) else cmd

        with Popen(cmd_list, stdout=PIPE, stderr=PIPE,
                   text=True, bufsize=1) as proc:
            self._log.info("Number of stdout lines: %s", len(proc.stdout))

            for line in proc.stdout:
                self._log.info(line.rstrip())

                # Wait for process to complete and check return code
                proc.wait()

                if proc.returncode != 0:  # Read any remaining stderr
                    stderr = proc.stderr.read()

                    if stderr:
                        self._log.info("Error code %s: %s", proc.returncode,
                                       stderr)

    def update(self, key, value):
        self._log.info("Running update with: %s, %s", key, value)

        with open(self._BOOT_CONF_FILE, 'r') as fr:
            lines = fr.readlines()
            update = 0
            new_value = ''

            for line in lines:
                if line and line.count(key) > 0:
                    if not line.strip().startswith('#'):
                        sps = line.split('=', 2)

                        if len(sps) == 2 and sps[1] == value:
                            update = 1
                        elif update == 0:
                            new_value += f"{key}={value}\r\n"
                            update = 2
                else:
                    new_value += line

            if not update == 1:
                if update == 0:
                    new_value += f"\r\n{key}={value}"

                with open(self._BOOT_CONF_FILE, 'w') as fw:
                    fw.write(new_value)

    def update_hwclock_set(self):
        filename = '/lib/udev/hwclock-set'

        if os.path.exists(filename):
            with open(filename, 'r') as fr:
                key = '-e /run/systemd/system'
                update = False
                do_update = False
                lines = fr.readlines()
                new_value = ''

                for line in lines:
                    if (line and line.strip().startswith('if')
                        and line.count(key)):
                        update = True
                        do_update = True

                    if update:
                        new_value += '#'

                    if line and line.strip() == 'fi':
                        update = False

                    new_value += line

                if do_update:
                    with open(filename, 'wb') as fw:
                        fw.write(new_value)

    def remove_fake_hwclock(self):
        cmd = 'sudo systemctl status fake-hwclock.service'
        # Split command string into list (safer than shell=True)
        cmd_list = shlex.split(cmd) if isinstance(cmd, str) else cmd

        with Popen(cmd_list, stdout=PIPE, stderr=PIPE,
                   text=True, bufsize=1) as proc:
            for line in proc.stdout:
                if line and line.strip().startswith('Loaded:'):
                    strps = line.split('fake-hwclock.service; ', 2)
                    s_len = len(strps)

                    if s_len == 2 and strps[1].strip().startswith('enabled'):
                        cmd = 'sudo systemctl disable fake-hwclock.service'
                        self.run_command(cmd)

    def new_partition(self, sd):
        cmd = b"o\nn\np\n1\n\n\nw\n"
        result = sp_run(['sudo', 'fdisk', sd], input=cmd, stdout=PIPE,
                        stderr=PIPE)
        self._log.info("Code: %s, stdout: %s, stderr: %s", result.returncode,
                       result.stdout, result.stderr)

    def check_sd(self):
        msg = "Please insert mSATA disk."
        cmd = 'ls -la /dev/sd*'
        cmd_list = shlex.split(cmd) if isinstance(cmd, str) else cmd

        with Popen(cmd_list, stdout=PIPE, stderr=PIPE,
                   text=True, bufsize=1) as proc:
            info = proc.stdout

            if len(info) > 0:
                # sd = ''
                num = 0

                for line in info:
                    if line.startswith("ls:"):
                        self._log.info(msg)
                        print(msg)
                        return

                    if line.strip()[-1].isdigit():
                        num += 1
                #     else:
                #         sd = line.strip('\r\n')

                # if num == 0:
                #     self.new_partition(sd);

                self._disk_clone()
            else:
                self._log.info(msg)
                print(msg)

    def _disk_clone(self):
        message = ("Calling the 'SD Card copier' to clone the filesystem from "
                   "SD Card to SSD...")
        command = 'piclone'
        self._log.info(message)
        self.run_command(command)

    def power_key(self):
        # callback function
        def powerkey_pressed(channels):
            self._log.info("pidesktop: power button press detected, "
                           "initiating shutdown")
            os.system("sync")
            os.system("shutdown -h now")
            sys.exit()

        self._log.info("pidesktop: power button service initializing")
        h = lgpio.gpiochip_open(0)

        # Pi to PCU - start/stop shutdown timer (BOARD 31 = BCM 6)
        lgpio.gpio_claim_output(h, 6, lgpio.LOW)

        # PCU to Pi - detect power key pressed (BOARD 33 = BCM 13)
        lgpio.gpio_claim_input(h, 13, lgpio.SET_PULL_DOWN)

        # Tell PCU we are alive
        lgpio.gpio_write(h, 6, 0)   # LOW
        lgpio.gpio_write(h, 6, 1)   # HIGH - blink/start shutdown timer
        time.sleep(0.5)
        lgpio.gpio_write(h, 6, 0)   # LOW - clear timer, we're alive

        # Wait for power key press
        self._log.info("pidesktop: power button monitor enabled")
        lgpio.gpio_claim_alert(h, 13, lgpio.RISING_EDGE)
        cb = lgpio.callback(h, 13, lgpio.RISING_EDGE, powerkey_pressed)

        # Idle
        while True:
            time.sleep(10)

    def reboot(self):
        h = lgpio.gpiochip_open(0)
        lgpio.gpio_claim_output(h, 6)
        lgpio.gpio_claim_input(h, 13)

        # In practice, detecting the power button press is unfortunately not
        # reliable, message if detected
        if lgpio.gpio_read(h, 13):
            # Power Key was already pressed - shut the system down immediately
            self._log.info("pidesktop: reboot service unexpected power "
                           "button detected")
        else:
            # reboot initiated, do whatever is needed on reboot
            self._log.info("pidesktop: reboot service active")

        # we're done
        lgpio.gpiochip_close(h)
        self._log.info("pidesktop: reboot service completed")

    def shutdown(self):
        h = lgpio.gpiochip_open(0)

        # Pi to Power MCU communication (BOARD 31 = BCM 6)
        lgpio.gpio_claim_output(h, 6)
        # Power MCU to Pi on power button (BOARD 33 = BCM 13)
        lgpio.gpio_claim_input(h, 13)

        # In practice detecting power button press is unfortunately not
        # reliable, message if detected
        if lgpio.gpio_read(h, 13):
            # Power Key was already pressed - shut the system down immediately
            self._log.info("pidesktop: shutdown service initated from "
                           "power button")
        else:
            # shutdown or reboot not related to the power key
            # lgpio.gpio_write(h, 6, 1)  # tell power MCU and exit immediately
            self._log.info("pidesktop: shutdown service active")

        # unmount SD card to clean up logs
        if os.path.exists('/dev/mmcblk0p1'):
            self._log.info("pidesktop: shutdown service unmounting SD card")
            os.system("umount /dev/mmcblk0p1")

        # stash the current system clock setting into the RTC hardware
        if os.path.exists('/sbin/hwclock'):
            self._log.info("pidesktop: shutdown service saving system clock "
                           "to hardware clock")
            os.system("/sbin/hwclock --systohc")

        # we're done
        lgpio.gpiochip_close(h)
        self._log.info("pidesktop: shutdown service completed")
