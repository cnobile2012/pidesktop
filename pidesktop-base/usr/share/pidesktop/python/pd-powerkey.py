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

# request LED output
led_request = chip.request_lines(consumer="pidesktop-led", config={
    LED_PIN: gpiod.LineSettings(direction=gpiod.LineDirection.OUTPUT)})

# request button interrupt
button_request = chip.request_lines(consumer="pidesktop-button",config={
    BUTTON_PIN: gpiod.LineSettings(direction=gpiod.LineDirection.INPUT,
                                   edge_detection=gpiod.LineEdge.RISING)})

# blink LED to show system alive
led_request.set_value(LED_PIN, 0)
led_request.set_value(LED_PIN, 1)
time.sleep(0.5)
led_request.set_value(LED_PIN, 0)

print("pidesktop: power button monitor enabled")

while True:
    if button_request.wait_edge_events(timeout=None):
        events = button_request.read_edge_events()

        for event in events:
            print("pidesktop: power button press detected")
            subprocess.run(["sync"])
            subprocess.run(["shutdown", "-h", "now"])
            exit(0)
