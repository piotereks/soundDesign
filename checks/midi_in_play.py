
import logging

import isobar
from isobar import *
# from isobar.io.midi import MidiInput, MidiOutput
# from isobar import MIDIScheduler
import mido
import time
import os
import threading


class CustMidiFile(mido.MidiFile):
    counter = 0


    def play(self, meta_messages=False):
        """Play back all tracks.

        The generator will sleep between each message by
        default. Messages are yielded with correct timing. The time
        attribute is set to the number of seconds slept since the
        previous message.

        By default you will only get normal MIDI messages. Pass
        meta_messages=True if you also want meta messages.

        You will receive copies of the original messages, so you can
        safely modify them without ruining the tracks.
        """
        start_time = time.time()
        input_time = 0.0
        time_variable = time.time()
        # time_real = time_variable
        for msg in self:
            print(f"Inside counter {self.counter}")
            self.counter += 1
            time_delta = time.time()-time_variable
            time_variable += time_delta
            # time_real += time_delta
            if not run_event.is_set():
                print("PausedXX")
                run_event.wait()
                print("After IF...")
                time_delta = time.time() - time_variable
                time_variable += time_delta
                start_time += time_delta
            print(f"{input_time=}, {msg.time=}")
            input_time += msg.time

            # playback_time = time_real - start_time
            playback_time = time.time() - start_time
            duration_to_next_event = input_time - playback_time
            print('still running...')
            # print(f"{time_real=},{start_time=}, {time.time()=}, {time_variable=}, {time_delta=}")
            print(f"{start_time=}, {time.time()=}, {time_variable=}, {time_delta=}")
            print(f"{duration_to_next_event=},{input_time=}, {playback_time=}")
            if duration_to_next_event > 0.0:
                time.sleep(duration_to_next_event)

            if isinstance(msg, mido.MetaMessage) and not meta_messages:
                continue
            else:
                yield msg


mido.MidiFile = CustMidiFile


def play_mid_file():
    print("in play_mid_file")
    file_path = os.path.abspath(__file__)
    file = os.path.join('example_midi', 'Variable_tempo_one_note_mod_double.mid')

    port = midi_out_device.midi
    # port = mido.open_output(midi_out)
    mid = mido.MidiFile(file)
    # mid.__dict__
    # {'filename': 'example_midi\\Variable_tempo_one_note.mid', 'type': 1, 'ticks_per_beat': 480, 'charset': 'latin1',
    #  'debug': False, 'clip': False, 'tracks': [MidiTrack([
    #     MetaMessage('time_signature', numerator=4, denominator=4, clocks_per_click=24, notated_32nd_notes_per_beat=8,
    #                 time=0),



    # start_time = time.time()
    start_time = time.time()
    elapsed_time = start_time
    while not break_flag.is_set():
        for msg in mid.play(meta_messages=True):
        # for msg in mid:
            elapsed_time = time.time() - elapsed_time
            wait_time = msg.time - elapsed_time
            print(wait_time)
            if wait_time > 0:
                pass
                # time.sleep(wait_time)
            if break_flag.is_set():
                break
            # if not run_event.is_set():
            #     print("Paused")
            #     run_event.wait()
            print('running')

            if msg.type in ('note_on', 'note_off'):
                port.send(msg)
            else:
                print(f"{msg=}")
                if msg.type == 'set_tempo':
                    timeline.set_tempo(mido.tempo2bpm(msg.tempo))
        else:
            continue
        break



midi_in_loop_name = 'KB loopMIDI Port 0'
midi_out_loop_name = 'KB loopMIDI Port 1'
midi_out_play_name = 'Microsoft GS Wavetable Synth 0'
counter = 0
midi_out = midi_out_play_name
# midi_out = midi_out_loop_name
midi_out_device = MidiOutputDevice(midi_out)
# out_dev = MidiOutputDevice(midi_out)
# port = mido.open_output(midi_out)
# port = out_dev.midi

run_event = threading.Event()
run_event.set()

break_flag = threading.Event()
break_flag.clear()

x = 1
# file = os.path.join('example_midi', 'Variable_tempo_one_note_mod.mid')
# file_input_device = MidiFileInputDevice(file)
# pattern = file_input_device.read()
# print("Read pattern containing %d note events" % len(pattern["note"]))
# file_input_device.callback = handle_midi_input
#
# timeline = Timeline()
# timeline.schedule(pattern)
# timeline.background()


# play_mid_file()
# Asynchronous play of file using threading
player_thread = threading.Thread(target=play_mid_file)  #  Play to loopback mid dev

# time.sleep(15)
print('after schedule')

timeline = Timeline(123)
timeline.schedule(

    {EVENT_NOTE : PSequence([55,70,62,68], repeats=16),
     EVENT_DURATION : 2
     },
                  output_device=midi_out_device
                  )
player_thread.start()
timeline.background()
# define mid "wave" output
# play_device = MidiOutputDevice(midi_out_play_name, send_clock=True)
# play_device = MidiOutputDevice(midi_out_play_name)
# play_port = mido.open_output(midi_out_play_name)

# Create a MIDIInput instance to receive MIDI input
# input = MidiInputDevice(midi_in_loop_name)
# input.callback = handle_midi_input
x = 1
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

# print('before schedule')
# def print_tempo():
#     print("in print tempo")
#     if input.tempo:
#         print("Estimated tempo: %.3f" % input.tempo)






# player_thread = threading.Thread(target=play_mid_file)  #  Play to loopback mid dev


# timeline = Timeline(clock_source=input)
# timeline.schedule({
#     # "action" : print("asdfasdfasdfasdfasdfasdfasd")
#     # "action" : player_thread.start()
#     "action" : play_mid_file()
#     # "action" : sadfasdfadsdfa
#     # "action": print_tempo
#     # "action": lambda:print("inside schedule")
# },
# # output_device=play_device
# #
# output_device=DummyOutputDevice()
# # remove_when_done=False
# )
# print("Awaiting MIDI clock signal from %s..." % input.device_name)
print('after run')