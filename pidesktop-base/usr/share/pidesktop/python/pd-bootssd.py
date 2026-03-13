#!/usr/bin/env python
import os;

class Manager:
    def updateBoot(self):
        filename = '/boot/cmdline.txt'

        with open(filename, 'r') as fr:
            key = 'root='
            value = "root=/dev/sda2"
            lines = fr.readlines()
            newValue = ''
            update = False

            for line in lines:
                if line:
                    strps = line.split(" ")

                    for v in strps:
                        if v.startswith(key) and v != value:
                            newValue += f"{value} "
                            update = True
                        else:
                            newValue += f"{v} "

            if update :
                with open(filename,'w') as fw:
                    fw.write(newValue.strip())

            self.reboot()


    def runask(self):
        ask = ("Do you want to change the file system from SD card to "
               "SSD?\nIf 'YES',please make sure the 'SD Card Copier' execute "
               "correctly.(y/N): ")
        answer = raw_input(ask)

        if answer.upper() in ('Y', 'YES'):
            self.updateBoot()

    def reboot(self):
        ask = ("To put the new configuration into effect, you need to restart "
               "the system.\nDo you want to reboot now? (Y/n): ")
        answer = raw_input(ask)

        if answer.upper() in ('N', 'NO'):
            print("You don't want to restart now.")
        else:
            os.popen("sudo reboot")


if __name__ == "__main__":
    m = Manager()
    m.runask()
