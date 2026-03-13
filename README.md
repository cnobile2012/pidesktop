pidesktop  V1.1.7
=================
This repository is a fork of the "offical" DIY Pi Desktop Case supporting software sold by http://www.element14.com sourced from Embest Technology Ltd. The case comes with a novel mSATA USB Disk, a power management solution, and real time clock integrated with the Raspberry Pi GPIO Connector.  Together they provide the missing mass storage, power management, and real time clock available in a typical desktop computer.

Key features of pidesktop:
- Reliable reboot for mSATA SSD drives
- Flash on boot to signal pidesktop support is enabled
- Improved installation instructions (Raspian and Berryboot)
- New pd-check command that provides detailed environment support
- Improved logging information
- Improved systemd services
- Rationalized file naming scheme

This fork DRAMATICALLY improves reboot performance so that many USB mSATA drives will reboot correctly.  It also adds a "flash" of the case top LED at startup so it is clear that the power button service has been enabled.  It has been tested on Raspian and Berryboot and the package should work with modern Debian-based distributions.   The fork was orignally created to apply patches requested by the community of users, to bring together all the related files and polish the product and support files. The approach here is focused on using a RP3 Model B+ (2018) and a USB mSATA SSD, if you don't take advantage of that capability there is not much point in purchasing the case.  It should work fine on an older RP3 Model B.

Install
-------
[Fast Installation booting from an mSATA drive](install.md) - Boot from mSATA USB with or without a blank SD card - cleanest

[Fast & Easiest Installation using Berryboot](berry.md) - Boot from SD to mSATA SSD no-clone multi OS images on single system

[Standard Installation booting from an SD card](documents/Installation-Manual.md) - Not recommended and not updated from the original

Utilities
----------
The original script utilities have been refactored and renamed

[pd-check](pidesktop-base/usr/share/pidesktop/script/pd-check) - summarize the files, scripts, links, and services to support pidesktop (new)

[pd-fixrtc.py](pidesktop-base/usr/share/pidesktop/python/pd-fixrtc.py) - install fixup to support RTC and GPIO

[pd-clonessd](pidesktop-base/usr/share/pidesktop/script/pd-clonessd) - image SD to SSD and make bootable (was ppp-hdclone) 
which uses [pd-clonessd.py](pidesktop-base/usr/share/pidesktop/python/pd-clonessd.py) and [pd-bootssd.py](pidesktop-base/usr/share/pidesktop/python/pd-bootssd.py) 

systemd service files
---------------------
lib/systemd/system/pidesktop-shutdown.service which uses [pd-shutdown.py](pidesktop-base/usr/share/pidesktop/python/pd-shutdown.py)

lib/systemd/system/pidesktop-reboot.service which uses [pd-reboot.py](pidesktop-base/usr/share/pidesktop/python/pd-reboot.py)

lib/systemd/system/pidesktop-powerkey.service which uses [pd-powerkey.py](pidesktop-base/usr/share/pidesktop/python/pd-powerkey.py)

package files
-------------
control - package control info

postinst - post installation script

postrm = post uninstall script

building pidesktop-base
-----------------------
There is a simple Makefile to build pidesktop-base.deb file from sources if you clone or fork the repos.

`make uninstall`   will uninstall the current pidesktop package
`make clean`       will clean the build environment
`make`             will make the .deb file
`make install`     will install the rebuilt pidesktop package

Or you can simply download the provided .deb file and install with the following command:

`dpkg -i pidesktop-base.deb`

If you want to change things you can clone this repository `make uninstall`, `make clean`, and make your changes to the underlying code, then `make` to build a new .deb package and install it with `make install`.
