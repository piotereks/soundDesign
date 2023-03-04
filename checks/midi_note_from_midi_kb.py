#!/usr/bin/env python3

#------------------------------------------------------------------------
# Prints all received MIDI messages to the console.
# Demonstrates the use of callbacks to generate events when MIDI
# messages are received.
#------------------------------------------------------------------------

import isobar as iso
import time

def print_message(message):
    """
    The callback argument is a mido Message object:
    https://mido.readthedocs.io/en/latest/messages.html
    """
    print(" - Received MIDI: %s" % message)
    print(message.__dict__)

midi_in = iso.MidiInputDevice('loopMIDI Port 0')
midi_in.callback = print_message
print("Opened MIDI input: %s" % midi_in.device_name)

pass
# try:
#     while True:
#         time.sleep(0.1)
# except KeyboardInterrupt:
#     pass