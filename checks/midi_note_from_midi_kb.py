#!/usr/bin/env python3

#------------------------------------------------------------------------
# Prints all received MIDI messages to the console.
# Demonstrates the use of callbacks to generate events when MIDI
# messages are received.
#------------------------------------------------------------------------

import isobar as iso
from datetime import datetime
import time
import mido
global knob_01
knob_01 = 0
def print_message(message):
    global knob_01
    """
    The callback argument is a mido Message object:
    https://mido.readthedocs.io/en/latest/messages.html
    """
    print(" - Received MIDI: %s %s" % (message ,datetime.now()))
    print(message.__dict__)
    # time.sleep(0.1)

    pass
    # if message.type == 'note_on':
    #    pass
    # elif message.type == 'control_change':
    #     if message.control == 22:
    #         if message.control != 0:  # or message.contol==64:
    #             knob_01 += (message.contol + 64) % 128 - 64
    #             print(f"{knob_01}")


print(mido.get_input_names())
# midi_in = iso.MidiInputDevice('KB loopMIDI Port 0')
midi_in = iso.MidiInputDevice(mido.get_input_names()[0])
midi_in.callback = print_message
print("Opened MIDI input: %s" % midi_in.device_name)

pass
# try:
#     while True:
#         time.sleep(0.1)
# except KeyboardInterrupt:
#     pass