#!/usr/bin/python3
# zmonkey
# written by unix-ninja
# 2021

import argparse
import pyglet
from simplecoremidi import send_midi

############################################################
## Configs

## find our joysticks
joysticks = pyglet.input.get_joysticks()
joystick_names = []

############################################################
## Functions

def midi_normalize(value, *, reverse=False):
  if reverse:
    value *= -1
  normalized = round((value + 1) * 63.5)
  return normalized

def main():
  ## sort our available devices alphabetically
  for joystick in joysticks:
    joystick_names.append(joystick.device.name)

  ## display available devices
  print("Available input devices:")
  for joystick in sorted(joystick_names):
    print("  " + joystick)
  print()

  ## select our joystick
  for joy in joysticks:
    if joy.device.name == sorted(joystick_names)[args.device]:
      joystick = joy
  print("Using device: %s" % (joystick.device.name))
  print()
  
  ## init
  x = 0
  y = 0
  
  btns = {}
  for btn in joystick.button_controls:
    btns[btn.raw_name] = False
  
  ## logic loop
  while(True):
    show = False
    ## there's an issue with pyglet on macOS
    ## we need to open and close the inout device each loop to poll for new values
    joystick.open()
  
    ## grab our data
    _x = midi_normalize(joystick.x)
    _y = midi_normalize(joystick.y, reverse=True)
  
    ## process our x/y axis
    if (x != _x):
      x = _x
      show = True
      send_midi((0xb0, 0x21, x))
    if (y != _y):
      y = _y
      show = True
      send_midi((0xb0, 0x22, y))
  
    ## process our button presses
    for btn in joystick.button_controls:
      if btn.value != btns[btn.raw_name]:
        btns[btn.raw_name] = btn.value
        note = 0x3c + list(btns.keys()).index(btn.raw_name)
        if btn.value:
          velocity = 0x7f
          if args.debug:
            print(btn.raw_name + " on")
        else:
          ## velocity 0 will send a note off event
          velocity = 0x0
          if args.debug:
            print(btn.raw_name + " off")
        send_midi((0x90, note, velocity))
  
    if show and args.debug:
      print("x:%d, y:%d" % (x, y))
    joystick.close()

############################################################
# Parse options
parser = argparse.ArgumentParser(description='Map joysticks and gamepads to MIDI')
parser.add_argument('--debug', dest='debug', action='store_true', help='enable debug info')
parser.add_argument('-d', '--device', dest='device', type=int, default=0, help='enable debug info')
args = parser.parse_args()

############################################################
## Main

## make sure our devices are positive
if args.device < 0:
  args.device = 0

if args.device > len(joysticks):
  print("Invalid input device.")
elif not joysticks:
  print("No input devices found.")
else:
  main()

