#
# pidesktop
#
PREFIX		= $(shell pwd)
SCRIPT_PATH	= ${PREFIX}/pidesktop-base/usr/share/pidesktop/scripts
PYTHON_PATH	= ${PREFIX}/pidesktop-base/usr/share/pidesktop/python
PIDESKTOP_PATH	= /usr/share/pidesktop
SCRIPT_DEST	= ${PIDESKTOP_PATH}/scripts
PYTHON_DEST	= ${PIDESKTOP_PATH}/python

MAJORVERSION	= 2
MINORVERSION	= 0
PATCHLEVEL	= 0
VERSION		= ${MAJORVERSION}.${MINORVERSION}.${PATCHLEVEL}
APP_NAME	= pidesktop-base
PACKAGE_NAME	= ${APP_NAME}-${VERSION}
RM_REGEX	= '(^.*.pyc$$)|(^.*~$$)|(.*\#$$)|(^.*__pycache__$$)'
RM_CMD		= find $(PREFIX) -regextype posix-egrep -regex $(RM_REGEX) \
                       -exec rm -rf {} +

.PHONY	: pidesktop
pidesktop: pidesktop-base.deb

.PHONY	: pidesktop-base.deb
pidesktop-base.deb: clobber
	@dpkg-deb --build --root-owner-group ${APP_NAME}/ \
                  ${PREFIX}/../${PACKAGE_NAME}.deb

uninstall:
	sudo dpkg -r ${PACKAGE_NAME}

.PHONY	: install
install	: pidesktop-base.deb
	@sudo dpkg -i ${PREFIX}/../${PACKAGE_NAME}.deb

.PHONY	: test
test	:
	@install -d ${SCRIPT_DEST}
	@install -d ${PYTHON_DEST}
#       Service scripts
	@install -m 775 ${SCRIPT_PATH}/pd-check       ${SCRIPT_DEST}
	@install -m 775 ${SCRIPT_PATH}/pd-clonessd    ${SCRIPT_DEST}
	@install -m 775 ${SCRIPT_PATH}/pd-rtcsync     ${SCRIPT_DEST}
#       Python code
	@install -m 775 ${PYTHON_PATH}/__init__.py    ${PYTHON_DEST}
	@install -m 775 ${PYTHON_PATH}/pidesktop.py   ${PYTHON_DEST}
	@install -m 775 ${PYTHON_PATH}/pd_bootssd.py  ${PYTHON_DEST}
	@install -m 775 ${PYTHON_PATH}/pd_fixrtc.py   ${PYTHON_DEST}
	@install -m 775 ${PYTHON_PATH}/pd_powerkey.py ${PYTHON_DEST}
	@install -m 775 ${PYTHON_PATH}/pd_shutdown.py ${PYTHON_DEST}

.PHONY	: remove_test
remove_test:
	sudo rm -rf ${PIDESKTOP_PATH}

.PHONY	: flake8
flake8	:
#       Error on syntax errors or undefined names.
	@flake8 . --select=E9,F7,F63,F82 --show-source
#       Warn on everything else.
	@flake8 . --exit-zero

.PHONY	: clean
clean	:
	@$(shell $(RM_CMD))

.PHONY	: clobber
clobber	:
	@rm -f ${PREFIX}/../${PACKAGE_NAME}.deb
