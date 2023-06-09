
import logging
from isobar import *
# from isobar.io.midi import MidiInput, MidiOutput
# from isobar import MIDIScheduler
import mido
import time
import os
import threading


def print_tempo():
    global tme
    # print(time.time()-tme)
    # print(midi_in.__dict__)
    tme = time.time()
    # if midi_in.tempo:
    #     print("Estimated tempo: %.3f" % midi_in.tempo)

def play_mid_file():

    file_path = os.path.abspath(__file__)
    # file = os.path.join('example_midi', 'Variable_tempo_one_note_mod.mid')
    file = os.path.join('example_midi', 'Variable_tempo_one_note.mid')
    midi_out = midi_out_play_name
    midi_out = midi_out_loop_name
    port = mido.open_output(midi_out)
    # clock_message = mido.Message('clock')
    mid = mido.MidiFile(file)
    # microseconds_per_beat = mido.bpm2tempo(120)
    # ticks_per_beat = mid.ticks_per_beat  # Number of ticks per beat (adjust as needed)
    # microseconds_per_tick = microseconds_per_beat / ticks_per_beat

    # mid.__dict__
    # {'filename': 'example_midi\\Variable_tempo_one_note.mid', 'type': 1, 'ticks_per_beat': 480, 'charset': 'latin1',
    #  'debug': False, 'clip': False, 'tracks': [MidiTrack([
    #     MetaMessage('time_signature', numerator=4, denominator=4, clocks_per_click=24, notated_32nd_notes_per_beat=8,
    #                 time=0),


    # start_time = time.time()
    while True:
        for msg in mid.play():

            port.send(msg)

            # elapsed_time = time.time() - start_time
            # start_time = time.time()
            # ticks = int(elapsed_time / (microseconds_per_tick / 1e6))
            # print(f"{elapsed_time=}")
            # print("ticks----------"+str(ticks))
            # for _ in range(ticks):
            #     port.send(clock_message)

            # Sleep briefly to control the clock rate
            # time.sleep(0.001)


def handle_midi_input(message):
    """Get data from in midi dev and play it on midi 'wave' dev"""
    play_device.midi.send(message)  #  midi port taken from isobar device
    # Print the MIDI message
    print(message)

midi_in_loop_name = 'KB loopMIDI Port 0'
midi_out_loop_name = 'KB loopMIDI Port 1'
midi_out_play_name = 'Microsoft GS Wavetable Synth 0'


# play_mid_file()
# Asynchronous play of file using threading
player_thread = threading.Thread(target=play_mid_file)  #  Play to loopback mid dev
player_thread.start()
# time.sleep(15)
print('after schedule')

# define mid "wave" output
play_device = MidiOutputDevice(midi_out_play_name, send_clock=True)
# play_port = mido.open_output(midi_out_play_name)

# Create a MIDIInput instance to receive MIDI input
input = MidiInputDevice(midi_in_loop_name)
input.callback = handle_midi_input

# Create a MIDIOutput instance to send MIDI messages
# output = MidiOutputDevice(midi_out_play_name)
# Set the MIDI output device index (change this to the appropriate value)
# output.open_output(0)

# Start the MIDI input processing
# input.start()
# print('input started')
# Continue with other tasks while receiving MIDI input
# ...

# Stop the MIDI input processing
# print('input stopped')
# input.stop()

# midi_out = MidiOutputDevice(mido.get_input_names()[0])
# midi_out.callback = lambda : print('blahblah')
#
# play_port = mido.open_output(midi_out_play_name)

print('before schedule')
def print_tempo():
    print("in print tempo")
    if input.tempo:
        print("Estimated tempo: %.3f" % input.tempo)



timeline = Timeline(120, clock_source=input)
# timeline = Timeline(clock_source=input)
timeline.schedule({
    "action" : print("asdfasdfasdfasdfasdfasdfasd")
    # "action" : sadfasdfadsdfa
    # "action": print_tempo
    # "action": lambda:print("inside schedule")
},
# output_device=play_device

output_device=DummyOutputDevice(),
remove_when_done=False
)
print("Awaiting MIDI clock signal from %s..." % input.device_name)
timeline.background()
print('after run')