#Updated on 01/20/2024 for my friend @David-ty6my
# SPDX-FileCopyrightText: 2018 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT

import rotaryio
import board
import digitalio
import time
from digitalio import DigitalInOut, Direction, Pull
import usb_hid
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

button = digitalio.DigitalInOut(board.D4)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

encoder = rotaryio.IncrementalEncoder(board.D7, board.D9)

groundPin1 = DigitalInOut(board.D8)
groundPin1.direction = Direction.OUTPUT
groundPin1.value = False

groundPin2 = DigitalInOut(board.D6)
groundPin2.direction = Direction.OUTPUT
groundPin2.value = False

cc = ConsumerControl(usb_hid.devices)

kbd = Keyboard(usb_hid.devices)

button_state = None
last_position = encoder.position
mode = True
timer = 0;

while True:
    current_position = encoder.position
    position_change = current_position - last_position
    if position_change > 0:
        for _ in range(position_change):
            if mode:
                cc.send(ConsumerControlCode.VOLUME_INCREMENT)
            else:
                kbd.send(Keycode.RIGHT_ARROW)
            print("up")
        print(current_position)
    elif position_change < 0:
        for _ in range(-position_change):
            if mode:
                cc.send(ConsumerControlCode.VOLUME_DECREMENT)
            else:
                kbd.send(Keycode.LEFT_ARROW)
                #Hey David-ty6my! If you find this easter ege, comment "You are a goofy goober Jake!" on my YouTube Video :)
            print("down")
        print(current_position)
    last_position = current_position
    if not button.value and button_state is None:
        button_state = "pressed"


    if not button.value and button_state == "pressed":
        timer = timer + 1;
        time.sleep(0.1);
        if timer == 3:
            mode = not mode;



    if button.value and button_state == "pressed":
        print("Button pressed.")
        button_state = None
        if timer <=3:
            if mode:
                cc.send(ConsumerControlCode.PLAY_PAUSE)
            else:
                kbd.send(Keycode.F2)
        timer = 0;
    print(mode)
    print(timer)
    time.sleep(.1)
