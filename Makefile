#
# pidesktop
#
SCRIPT_PATH	= pidesktop-base/usr/share/pidesktop/script
PYTHON_PATH	= pidesktop-base/usr/share/pidesktop/python
SCRIPT_DEST	= /usr/share/pidesktop/script
PYTHON_DEST	= /usr/share/pidesktop/python
MAJORVERSION	= 2
MINORVERSION	= 0
PATCHLEVEL	= 0
VERSION		= ${MAJORVERSION}.${MINORVERSION}.${PATCHLEVEL}

.PHONY	: pidesktop
pidesktop: pidesktop-base.deb

.PHONY	: pidesktop-base.deb
pidesktop-base.deb: clean
	dpkg -b pidesktop-base/ pidesktop-base-${VERSION}.deb

.PHONY	: clean
clean: pidesktop-base.deb
	@rm -f pidesktop-base-${VERSION}.deb

.PHONY	: install
install: pidesktop-base.deb
	@sudo dpkg -i pidesktop-base-${VERSION}.deb

.PHONY	: test
test:
	@cp ${SCRIPT_PATH}/pd-check       ${SCRIPT_DEST}
	@cp ${SCRIPT_PATH}/pd-clonessd    ${SCRIPT_DEST}
	@cp ${PYTHON_PATH}/pd-bootssd.py  ${PYTHON_DEST}
	@cp ${PYTHON_PATH}/pd-fixrtc.py   ${PYTHON_DEST}
	@cp ${PYTHON_PATH}/pd-powerkey.py ${PYTHON_DEST}
	@cp ${PYTHON_PATH}/pd-shutdown.py ${PYTHON_DEST}

uninstall:
	sudo dpkg -r pidesktop-base
