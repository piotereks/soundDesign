DEFAULT_TEMPO = 500000
global MULTI_TRACK
MULTI_TRACK = True

import mido
import tracker.app.mido_fixes
import time
# import os
import threading

from tracker.app.tracker import *
from tracker.app.isobar_fixes import *
from mido.midifiles.tracks import MidiTrack, merge_tracks, fix_end_of_track
from mido.midifiles.units import tick2second
from tracker.app.midi_dev import FileOut

from tracker.app.log_call import *

def mid_meta_message(msg: mido.MetaMessage = None, *args, **kwargs):
    # return None
    # if self.midi_out_mode == self.MIDI_OUT_DEVICE:
    #     return None
    if not msg:
        msg = mido.MetaMessage(*args, **kwargs)

    if MULTI_TRACK:
        midi_out_device.miditrack[0].append(msg)
    else:
        midi_out_device.miditrack.append(msg)

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


def main():
    global tracker
    # global self.yy_tracker
    # global keyboard
    log_call()
    this_dir = os.path.dirname(os.path.abspath(__file__))
    config_file = os.path.join(this_dir, '../tracker/config/main_config.json')



    # wanted_file = os.path.join(this_dir, fname)

    with open(config_file, 'r') as file:
        loaded_config = json.load(file)
        app_config = loaded_config['app']
        tracker_config = loaded_config['tracker']
        midi_mapping = loaded_config.get('midi_mapping')

    # midi_out_flag = Tracker.MIDI_OUT_DEVICE
    midi_out_flag = Tracker.MIDI_OUT_MIX_FILE_DEVICE
    # midi_out_flag = Tracker.MIDI_OUT_FILE

    tracker = Tracker(tracker_config=tracker_config, midi_mapping=midi_mapping, midi_out_mode=midi_out_flag)
    # my_tracker.midi_out.program_change(program=22)

    # TrackerGuiApp(parm_rows=12, parm_cols=5, app_config=app_config, tracker_ref=tracker).run()



main()

ASYNC = False
ASYNC = True
midi_in_loop_name = 'KB loopMIDI Port 0'
midi_out_loop_name = 'KB loopMIDI Port 1'
midi_out_play_name = 'Microsoft GS Wavetable Synth 0'
counter = 0
midi_out = midi_out_play_name
# midi_out = midi_out_loop_name
# midi_out_device = iso.MidiOutputDevice(midi_out)
# midi_out_device = FileOut(device_name=midi_out, filename='x1x1.mid', send_clock=True,  virtual=False)
midi_out_device = tracker.midi_out
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


if __name__ == '__main__':
    # main()
    print('Processing Done.')

