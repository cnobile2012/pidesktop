#!/usr/bin/env python
import os
import shlex

from subprocess import Popen, PIPE
#from pppBoot import Manager


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


def newPartition(sd):
    command = 'echo -e "o\nn\np\n1\n\n\nw\n" | sudo fdisk ' + sd
    os.popen(command)


def chekSD():
    command = 'ls -la /dev/sd*'

    with Popen(cmd_list, stdout=PIPE, stderr=PIPE,
               text=True, bufsize=1) as proc:
        info = proc.stdout

        if len(info) > 0:
            sd = ''
            num = 0

            for line in info:
                if line.startswith("ls:") :
                    print('Please insert mSATA disk.')
                    return

                if line.strip()[-1].isdigit():
                    num += 1
                else:
                    sd = line.strip('\r\n')

            # if num == 0:
            #     newPartition(sd);

            diskClone();
        else:
            print('Please insert mSATA disk.')


def diskClone():
    message = ("Calling the 'SD Card copier' to clone the filesystem from "
               "SD Card to SSD...")
    print(message)
    command = 'piclone'
    runCommand(command)
    # m = Manager();
    # m.runask();


if __name__ == "__main__":
    chekSD()
