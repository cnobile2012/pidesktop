#!/usr/bin/env python3
#
# pd-powerkey.py - monitor GPIO to detect power key press from Power MCU (PCU)
#

import gpiod
import time
import subprocess

print("pidesktop: power button service initializing")

LED_PIN = 6      # BOARD 31
BUTTON_PIN = 13  # BOARD 33

chip = gpiod.Chip("/dev/gpiochip0")
led = chip.get_line(LED_PIN)
button = chip.get_line(BUTTON_PIN)

led.request(consumer="pidesktop-led", type=gpiod.LINE_REQ_DIR_OUT)
button.request(consumer="pidesktop-button", type=gpiod.LINE_REQ_EV_RISING_EDGE)

# blink LED to show system alive
led.set_value(0)
led.set_value(1)
time.sleep(0.5)
led.set_value(0)

print("pidesktop: power button monitor enabled")

while True:
    if button.event_wait(sec=10):
        event = button.event_read()
        print("pidesktop: power button press detected")
        subprocess.run(["sync"])
        subprocess.run(["shutdown", "-h", "now"])
        break
