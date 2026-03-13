Installation with mSATA SSD
===========================
It is VERY easy to build a new pidesktop case with a new mSATA SSD attached on a Raspberry Pi 3 Model B+ (2018) and only slightly more difficult for the older Model B.  If you have a choice, pick the Model B+, it can boot from SSD out of the box, has a faster CPU and networking. 

Key features of pidesktop:
- Reliable reboot for mSATA SSD drives
- Flash on boot to signal pidesktop support is enabled
- Improved installation instructions (Raspian and Bootberry)
- New pd-check command that provides detailed environment support
- Improved logging information
- Improved systemd services
- Rationalized file naming scheme

The pidesktop add-on board functions as a USB mSATA SSD device when connected to *any* system not just an RP3 Model B or B+. If the special USB adapter that connects the RP3 to the add-on card (hat) is not inserted and there is no SD card in the RP3, the RP3 will not boot. When the micro-USB data port of the add-on card is connected to a computer and power is provided via the second micro-USB port on the add-on card, the add-on card alone becomes a functional USB mSATA SSD device when the power button on the add-on card is pressed.

Needed parts:
- Pi Desktop Case
- Raspberry Pi 3 Model B+ (recommended) or Model B
- Formatted Blank SD card (optional for Model B+)
- mSATA SSD
- two USB->miniUSB cables (just for imaging)

Model B pre-install
-------------------
If you have a Model B+ you can skip this step, but if you have a Model B it may not have the ["Boot from USB bit"](https://www.raspberrypi.org/documentation/hardware/raspberrypi/bootmodes/msd.md) set by [booting from an SD card](https://www.raspberrypi.org/documentation/installation/installing-images/README.md) and making sure the required configuration bit is set in hardware. You should be able to use an existing SD card, just *remember* to clear the /boot/config.txt changes used the set the boot bit if you are going to reuse it. Make certain: `vcgencmd otp_dump | grep 17:` shows `17:3020000a`, then shutdown and remove the SD card.  You can format your SD card and use it to optimize boot times, but it does add complexity to your configuration.  After trying both with and without an SD card, I generally do not use an SD card.

Assemble the case
-----------------
Attach the RP3 board (with optional blank SD card inserted) to the case using the provided posts. 
- Install the add-on board, and optionally a camera per the provided instruction booklet.
- Install the mSATA SSD onto the pidesktop add-on board and lock it in place with the provided small screws.
- DO NOT yet install the special USB adapter, first we need to image the SSD below.

Image your SSD
--------------
Use Etcher and the pidesktop add-on board (without the special USB adapter installed) as follows:
- a. Connect both USB ports of the pi-desktop add-on board to two USB ports on the imaging machine
- b. Press the power button on the add-on board, it will appear to your imaging system as a USB SSD device
- c. Use Etcher to write the latest Raspian image (or your OS of choice) to the mSATA SSD USB device.
- d. When complete unmount the USB SSD device and unplug the USB cables as they are no longer needed.

Test your Case
--------------
Now you can connect the special USB adapter to the case and boot with your monitor, keyboard, and mouse attached.  If you imaged Raspian the system should immediately reboot to resize partitions.  At this point, if you haven't already you can install the top on the case and know it takes a little pushing to get all the plastic clips in place.

Install the pidesktop package
-----------------------------
Good practice would be to [update Raspian via apt-get](https://www.raspberrypi.org/documentation/raspbian/updating.md) and while those instructions work, using a higher-level `apt` with the following commands is growing in popularity:
- `sudo apt update`
- `sudo apt full-upgrade`

Now you can go to the [pidesktop github](http://github.com/hoopsurfer/pidesktop) to download the .deb package from your browser. Install the pidesktop-base package using the command `sudo dpkg -i pidesktop-base.deb` and reboot, check all is well with `pd-check` and you should see your firmware & kernel versions, new commands added, new services, and RTC clock updated, and finally a summary of the installed pidesktop package.

**NOTE: CHECK THAT FIRMWARE IN `pd-check` IS DATED 2018-06-29 OR NEWER! A needed firmware update that we requested has been made that dramatically improves reboot reliability.  You can wait for the patch to make it into a formal release or if you do want to use the pre-release firmware you can run `rpi-update` to install the newest firmware build. Shutdown and restart and recheck that you have newer firmware with the `pd-check` command again.

Now you can then hit the case power button for 2 seconds and your Pi should immediately shutdown.  You can issue `shutdown now` or `reboot` (or the equivalent) and the case led will flash until reboot has started (~10 secs) or longer for shutdown (~30 secs) get to full power off.

Updated Tests with Different SSDs
---------------------------
This new pidesktop update along with firmware has improved reboot times by about 20 seconds (which in many cases means going from not working to working reliabily).  Imaging Raspian 2018-3-13 took about 8 minutes on all SSDs.  After booting updates were applied via apt update, full-upgrade and rpi-update).  Below tables are boot/reboot/shutdown times measured with no SD card and with a blank SD card.  No camera was installed.  Boot time was measured from pressing the power button to the first flash of the case LED.  The reboot time is from `reboot` command to case LED on steady.  The shutdown time is pressing power button for 2 seconds to Pi off (full power off is about 30 seconds).

__Raspberry Pi 3 Model B+__

   mSATA SSD w/o SD  | *Boot to LED Flash* | *Reboot to LED On* | *Power Button to Off*
---------------------|---------------------|--------------------|---------------------
Samsung 860 EVO 250GB | 32.8s | 15.5s | 3.3s
Kingston 120GB | 32.5s | 15.5s | 3.3s
Kingspec 64GB | 33.2s | 16.3s | 3.3s

   mSATA SSD w/ SD  | *Boot to LED Flash* | *Reboot to LED On* | *Power Button to Off*
--------------------|---------------------|--------------------|----------------------
**Samsung 860 EVO 250GB** | **27.2s** | **10.2s**  | 3.3s
**Kingston 120GB** | **27.2s** | **10.2s** | 3.3s
Kingspec 64GB | 28.2s | 11.7s | 3.3s

A Few Observations:
- Using a formatted blank SD card still cuts boot time by 5 seconds, but pidesktop does not require it 
- With the latest pidesktop here all devices reboot consistently with or without a blank SD card inserted.
- The Samsung and Kingston mSATA devices had identical, fastest boot and reboot times - your mileage may vary
- The Kingspec mSATA device had only slightly slower boot/reboot times

Hacking Your Pi Desktop Case
----------------------------
If you ever need to reimage your mSATA SSD, it is as easy as unplugging the special USB adapter and connecting the micro-USB and power ports to the imaging machine.  It takes about 8 minutes to reimage and it is not necessary to disassemble the case.   

If you use a wireless keyboard/mouse with your new pidesktop you can install the small dongle under the special USB adapter and that makes for a very clean installation with easy access to the remaining two USB ports.

If you're like me you want a clean look with no branding.  You can remove the branding in the center of the light ring by removing the plastic circle from the top of the case and then polishing off the branding using an abrasive like bar keepers friend liquid to remove the printing - lay a cloth on your bench and put a 2cm dot of abrasive liquid on a microfiber cloth to rub off the branding.

If you installed a camera you enable with "raspi-config" and then test it with `raspistill -vf -o test.jpg` and you can do some mild overclocking to speed up your new system - consider a micro cooling fan if you want to push your system.  

**FULL DISCLOSURE: I have not extensively tested clone and boot from SD configurations since I don't use them - would welcome feedback

References
----------
https://github.com/raspberrypi/documentation/blob/master/hardware/raspberrypi/bootmodes/bootflow.md
