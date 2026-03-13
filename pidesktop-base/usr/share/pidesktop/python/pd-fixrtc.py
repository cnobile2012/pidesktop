#!/usr/bin/env python
#
# brute force
#

import os
import shlex

from subprocess import Popen, PIPE


def runCommand(command):
    print(command)
    # Split command string into list (safer than shell=True)
    cmd_list = shlex.split(command) if isinstance(command, str) else command

    with Popen(cmd_list, stdout=PIPE, stderr=PIPE,
               text=True, bufsize=1) as proc:
        for line in proc.stdout:
            print(line.rstrip())

        # Wait for process to complete and check return code
        proc.wait()

        if proc.returncode != 0:
            # Read any remaining stderr
            stderr = proc.stderr.read()

            if stderr:
                print(f"Error (code {proc.returncode}): {stderr}")


def updategpio6():
    filename = '/boot/config.txt'
    key = 'gpio'
    value = '6=op,pn,dl'

    with open(filename, 'rb') as fr:
        lines = fr.readlines()
        update = 0
        newValue = ''

        for line in lines:
            if line and line.count(key) > 0:
                if not line.strip().startswith('#'):
                    sps = line.split('=', 2)

                    if len(sps) == 2 and sps[1] == value:
                        update = 1
                    elif update == 0:
                        newValue += key + '=' + value + '\r\n'
                        update = 2
            else:
                newValue += line

        if not update == 1:
            if update == 0:
                newValue += '\r\n' + key + '=' + value

            with open(filename, 'wb') as fw:
                fw.write(newValue)


def updategpio13():
    filename = '/boot/config.txt'
    key = 'gpio'
    value = '13=ip'

    with open(filename,'rb') as fr:
        lines = fr.readlines()
        update = 0
        newValue = ''

        for line in lines:
            if line and line.count(key) > 0:
                if not line.strip().startswith('#'):
                    sps = line.split('=', 2)

                    if len(sps) == 2 and sps[1] == value:
                        update = 1
                    elif update == 0:
                        newValue += key + '=' +value + '\r\n'
                        update = 2
            else:
                newValue += line

        if not update == 1:
            if update == 0:
                newValue += '\r\n' + key + '=' + value

            with open(filename,'wb') as fw:
                fw.write(newValue)


def updateConfig():
    filename = '/boot/config.txt'
    key = 'dtoverlay'
    value = 'i2c-rtc,pcf8563'

    with open(filename, 'r') as fr:
        lines = fr.readlines()
        update = 0
        newValue = ''

        for line in lines:
            if line and line.count(key) > 0:
                if not line.strip().startswith('#'):
                    sps = line.split('=', 2)

                    if len(sps) == 2 and sps[1] == value:
                        update = 1
                    elif update == 0:
                        newValue += f"{key}={value}\r\n"
                        update = 2
            else:
                newValue += line
        if not update == 1:
            if update == 0:
                newValue += f"\r\n{key}={value}"

            with open(filename, 'w') as fw:
                fw.write(newValue)


def removeFakeHwclock():
    command = 'sudo systemctl status fake-hwclock.service'
    # Split command string into list (safer than shell=True)
    cmd_list = shlex.split(command) if isinstance(command, str) else command
    
    with Popen(cmd_list, stdout=PIPE, stderr=PIPE,
               text=True, bufsize=1) as proc:
        for line in proc.stdout:
            if line and line.strip().startswith('Loaded:'):
                strps = line.split('fake-hwclock.service; ', 2);

                if len(strps) == 2 and strps[1].strip().startswith('enabled'):
                    command = 'sudo systemctl disable fake-hwclock.service'
                    runCommand(command)


def updateHwclockSet() :
    filename = '/lib/udev/hwclock-set'

    with = open(filename,'rb') as fr:
        key = '-e /run/systemd/system'
        update = False
        doUpdate = False
        lines = fr.readlines()
        newValue = ''

        for line in lines:
            if line and line.strip().startswith('if') and line.count(key):
                update = True
                doUpdate = True

            if update:
                newValue += '#'

            if line and line.strip() == 'fi':
                update = False

            newValue += line;

        if doUpdate :
            with open(filename,'wb') as fw:
                fw.write(newValue)


if __name__ == "__main__":
    updateConfig()
    updategpio6()
    # updategpio13()
    updateHwclockSet()
    removeFakeHwclock()
