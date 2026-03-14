#!/usr/bin/env python3
#
# pd-powerkey.py - monitor GPIO to detect power key press from Power MCU (PCU)
#

import gpiod
import time
import subprocess

print("pidesktop: power button service initializing")

chip = gpiod.Chip("/dev/gpiochip0")

POWER_LED = 6      # GPIO6  (BOARD 31)
POWER_BUTTON = 13  # GPIO13 (BOARD 33)

led = chip.get_line(POWER_LED)
button = chip.get_line(POWER_BUTTON)

led.request(consumer="pidesktop", type=gpiod.LINE_REQ_DIR_OUT)
button.request(consumer="pidesktop", type=gpiod.LINE_REQ_EV_RISING_EDGE)

# Blink to show Pi is alive
led.set_value(0)
led.set_value(1)
time.sleep(0.5)
led.set_value(0)

print("pidesktop: power button monitor enabled")

while True:
    if button.event_wait():
        event = button.event_read()
        print("pidesktop: power button press detected")
        subprocess.run(["sync"])
        subprocess.run(["shutdown", "-h", "now"])
        break
