DEFAULT_TEMPO = 500000
# import logging

# import isobar
# from isobar import *
# from isobar.io.midi import MidiInput, MidiOutput
# from isobar import MIDIScheduler
import mido
import time
# import os
import threading

from tracker.app.isobar_fixes import *
from mido.midifiles.tracks import MidiTrack, merge_tracks, fix_end_of_track
from mido.midifiles.units import tick2second
from tracker.app.midi_dev import FileOut
# from types import SimpleNamespace


def _to_abstime(messages):
    """Convert messages to absolute time."""
    now = 0
    for msg in messages:
        now += msg.time
        yield msg.copy(time=now)
# mido.MetaMessage

def _to_reltime(messages):
    """Convert messages to relative time."""
    now = 0
    for msg in messages:
        delta = msg.time - now
        yield msg.copy(time=delta)
        now = msg.time


def merge_tracks(tracks):
    """Returns a MidiTrack object with all messages from all tracks.

    The messages are returned in playback order with delta times
    as if they were all in one track.
    """
    messages = []
    track_idx = []
    for track in tracks:
        abs_trk = list(_to_abstime(track))
        track_idx.extend([tracks.index(track)] * len(list(abs_trk)))
        messages.extend(abs_trk)

    msg_zip_list = list(zip(messages, track_idx))
    msg_zip_list.sort(key = lambda m : m[0].time)
    messages, track_idx = zip(*msg_zip_list)
    # messages.sort(key=lambda msg: msg.time)

    return MidiTrack(fix_end_of_track(_to_reltime(messages))), track_idx

mido.midifiles.tracks.merge_tracks = merge_tracks
mido.midifiles.tracks._to_abstime = _to_abstime
mido.midifiles.tracks._to_reltime = _to_reltime

class CustMidiFile(mido.MidiFile):
    counter = 0

    def __iter__(self):
        # The tracks of type 2 files are not in sync, so they can
        # not be played back like this.
        if self.type == 2:
            raise TypeError("can't merge tracks in type 2 (asynchronous) file")

        tempo = DEFAULT_TEMPO
        merged_tracks, merged_tracks_idx = merge_tracks(self.tracks)
        for msg in merged_tracks:
            # Convert message time from absolute time
            # in ticks to relative time in seconds.
            if msg.time > 0:
                delta = tick2second(msg.time, self.ticks_per_beat, tempo)
            else:
                delta = 0

            yield msg.copy(time=delta), merged_tracks_idx[merged_tracks.index(msg)]

            if msg.type == 'set_tempo':
                tempo = msg.tempo

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
        for msg, msg_track in self:
            # midi_out_device.tick()
            # print(f"Inside counter {self.counter}")
            # self.counter += 1
            time_delta = time.time()-time_variable
            time_variable += time_delta
            # time_real += time_delta
            if not run_event.is_set():
                # print("PausedXX")
                run_event.wait()
                # print("After IF...")
                time_delta = time.time() - time_variable
                time_variable += time_delta
                start_time += time_delta
            print(f"{input_time=}, {msg.time=}")
            input_time += msg.time

            # playback_time = time_real - start_time
            playback_time = time.time() - start_time
            duration_to_next_event = input_time - playback_time
            # print('still running...')
            # print(f"{time_real=},{start_time=}, {time.time()=}, {time_variable=}, {time_delta=}")
            # print(f"{start_time=}, {time.time()=}, {time_variable=}, {time_delta=}")
            # print(f"{duration_to_next_event=},{input_time=}, {playback_time=}")
            if duration_to_next_event > 0.0:
                time.sleep(duration_to_next_event)

            if isinstance(msg, mido.MetaMessage) and not meta_messages:
                continue
            else:
                msg_cpy = msg.copy()
                msg_cpy.time = round(msg_cpy.time)
                yield msg_cpy, msg_track


mido.MidiFile.__iter__ = CustMidiFile.__iter__
mido.MidiFile.play = CustMidiFile.play


def mid_meta_message(msg: mido.MetaMessage = None, *args, **kwargs):
    # return None
    # if self.midi_out_mode == self.MIDI_OUT_DEVICE:
    #     return None
    if not msg:
        msg = mido.MetaMessage(*args, **kwargs)

    midi_out_device.miditrack[0].append(msg)


def play_mid_file():
    print("in play_mid_file")

    # file = os.path.join('example_midi', 'Variable_tempo_one_note_mod.mid')
    # file = os.path.join('example_midi', 'Variable_tempo_one_note')

    port = midi_out_device.midi
    # port = mido.open_output(midi_out)


    time_division = mid.ticks_per_beat

    # start_time = time.time()
    start_time = time.time()
    elapsed_time = start_time
    while not break_flag.is_set():
        for msg, msg_track in mid.play(meta_messages=True):
        # for msg in mid:
            elapsed_time = time.time() - elapsed_time
            wait_time = msg.time - elapsed_time
            print(f"{wait_time=}")
            # ticks = int(mido.second2tick(msg.time, time_division, tempo=timeline.tempo))

            if wait_time > 0:
                pass
                # ticks = int(mido.second2tick(wait_time, time_division, tempo=timeline.tempo))
                # print(f"{ticks=}")
                # for _ in range(ticks):
                #     # timeline.tick()
                #     midi_out_device.tick()
                # time.sleep(wait_time)
            if break_flag.is_set():
                break
            # if not run_event.is_set():
            #     print("Paused")
            #     run_event.wait()
            print('running')
            if msg.type in ('note_on', 'note_off'):
                # port.send(msg)
                if msg.type == 'note_on':
                    midi_out_device.note_on(channel=msg.channel, note=msg.note, velocity=msg.velocity)
                else:
                    midi_out_device.note_off(channel=msg.channel, note=msg.note)
            elif msg.type == 'program_change':
                midi_out_device.program_change(program=msg.program, channel=msg.channel)
                mid_meta_message(msg=msg)
                print(f"program change {msg=}")


            else:
                print(f"{msg=}")
                if msg.type == 'set_tempo':
                    timeline.set_tempo(tempo=mido.tempo2bpm(msg.tempo))
                    # mid_meta_message(type='set_tempo', tempo=mido.bpm2tempo(msg.tempo), time=0)
                    pass

                # midi_out_device.miditrack[0].append(msg)
                mid_meta_message(msg=msg)

            # for _ in range(50):
            #     midi_out_device.tick()
        else:
            ww()
            break
            continue
        break

def ww():
    midi_out_device.write()
ASYNC = False
ASYNC = True
midi_in_loop_name = 'KB loopMIDI Port 0'
midi_out_loop_name = 'KB loopMIDI Port 1'
midi_out_play_name = 'Microsoft GS Wavetable Synth 0'
counter = 0
midi_out = midi_out_play_name
# midi_out = midi_out_loop_name
# midi_out_device = iso.MidiOutputDevice(midi_out)
midi_out_device = FileOut(device_name=midi_out, filename='x1x1.mid', send_clock=True,  virtual=False)
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

file_path = os.path.abspath(__file__)
file = os.path.join('example_midi', 'Variable_tempo_one_note_mod_double_instr.mid')
mid = mido.MidiFile(file)

available_channels = set(range(16))-set(m.channel for t in mid.tracks
                                        for m in t if hasattr(m, 'channel'))-{9}
min_channel = min(available_channels)
available_channels.remove(min_channel)

timeline = iso.Timeline(123,output_device=midi_out_device)
timeline.schedule(

    {iso.EVENT_NOTE : iso.PSequence([55,70,62,68], repeats=16),
     iso.EVENT_DURATION : 0.5,
     iso.EVENT_CHANNEL : min_channel
     }

                  )
if ASYNC:
    player_thread.start()
else:
    play_mid_file()

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