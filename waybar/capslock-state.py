#!/usr/bin/env python3

import os                                      # to run sound player and work with arguments
import sys                                     # to work with arguments
import pickle                                  # to work with serealizing/de-serealizing variable
from evdev import InputDevice, ecodes

# file name and path to temporary store Caps Lock state
TMP_PATH = '/tmp/'
CAPS_STATE_FILE = '_caps_led.state'

# file operations
READ_BINARY = 'rb'
WRITE_BINARY = 'wb'
CREATE_BINARY = 'xb'

# defining sound player and sets of sounds to choose from
SND_PLAYER = 'paplay'
SND_FILE_BELL = '/usr/share/sounds/freedesktop/stereo/bell.oga'
SND_FILE_MSG = '/usr/share/sounds/freedesktop/stereo/message.oga'
SND_FILE_DLG_INF = '/usr/share/sounds/freedesktop/stereo/dialog-information.oga'
SND_FILE_DLG_ERR = '/usr/share/sounds/freedesktop/stereo/dialog-error.oga'

# list of app standard messages
ERROR = 'Error!'
CAPS_ON = 'AA 🔒'
CAPS_OFF = 'aa 🔓'

# function to work with file were ops variable should have
# such values as 'rb' - read, 'wb' - write and 'xb' - create only
def file_ops(ops, caps_state = None):
    try:
        file = open(TMP_PATH + CAPS_STATE_FILE, ops)
        match ops:
            case 'rb':
               caps_state = pickle.load(file)
            case 'wb':
               pickle.dump(caps_state, file)

    except FileNotFoundError:
        file = open(TMP_PATH + CAPS_STATE_FILE, CREATE_BINARY)
        caps_state = 0

    file.close()
    return caps_state
   
# MAIN -------------------------------------------

def main(args):
    # reading args 
    # argv1 - device event path; argv2 - sound On/Off (default: Off)
    args_numb = len(args)

    # Sound switch (by default - Off)  
    sound_sw = 'sound-off'

    match args_numb:
        case 1:
            state_msg = ERROR
        case 2:
            device_event_number = args[1]
        case 3:
            device_event_number = args[1]
            sound_sw = args[2]

    # keyboard descriptor
    keyboard = InputDevice(device_event_number)

    # loading previous Caps Lock state if available
    previous_caps_state = file_ops(READ_BINARY)

    # reading current Caps Lock state from keyboard
    current_caps_state = keyboard.leds()

    # comprehension to determine and asigning Caps Lock state
    state_msg = CAPS_ON if current_caps_state == [1] else CAPS_OFF

    print(state_msg)
    # in case of changing states making a sound
    if sound_sw == 'sound-on' and previous_caps_state != current_caps_state:
        # playing sound file with player
        os.system(SND_PLAYER + ' ' + SND_FILE_BELL)
    # storing Caps Lock state in file and exit
    file_ops(WRITE_BINARY, current_caps_state)

if __name__ == '__main__':
    main(sys.argv)
