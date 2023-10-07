# import isobar as iso
import sys
from tracker.app.isobar_fixes import *
# from tracker.app.midi_dev import FileOut, MidiFileManyTracksOutputDevice
from tracker.utils.dump_midi import print_mid

import pytest
# import mido

from tracker.app.midi_dev import *

tmp_filename = 'x1x1a.mid'
tmp_filename2 = 'x1x1b.mid'

this_dir = os.path.dirname(os.path.abspath(__file__))
tmp_filenameX = os.path.join(this_dir, '..', '..', 'checks', 'example_midi', 'Var_tempo_1_trk_sax.mid')

@pytest.fixture()
def dummy_timeline():
    midi_out_play_name = 'Microsoft GS Wavetable Synth 0'
    midi_out = midi_out_play_name
    # midi_out_device = FileOut(device_name=midi_out, filename=tmp_filename, send_clock=True, virtual=False)
    filename = tmp_filename
    midi_out_device = MidiFileManyTracksOutputDevice(filename=filename)



    # timeline = iso.Timeline(output_device=iso.io.DummyOutputDevice(), clock_source=iso.DummyClock())
    timeline = iso.Timeline(output_device=midi_out_device, clock_source=iso.DummyClock())

    timeline.stop_when_done = True
    return timeline

@pytest.fixture()
def dummy_timeline2():
    midi_out_play_name = 'Microsoft GS Wavetable Synth 0'
    midi_out = midi_out_play_name
    filename=tmp_filename2
    midi_out_device = FileOut(device_name=midi_out, filename=filename, send_clock=True, virtual=False)

    # timeline = iso.Timeline(output_device=iso.io.DummyOutputDevice(), clock_source=iso.DummyClock())
    # timeline = iso.Timeline(tempo=123, output_device=midi_out_device, clock_source=iso.DummyClock())
    timeline = iso.Timeline(output_device=midi_out_device)
    timeline.stop_when_done = True
    return timeline



def test_timeline_schedulex(dummy_timeline):
    events = {
        iso.EVENT_NOTE: iso.PSequence([1], 1)
    }

    dummy_timeline.schedule(events)
    print("b")
    assert len(events.keys()) == 1
    print("c")
    dummy_timeline.run()
    print("d")
    assert len(dummy_timeline.output_device.events) == 2
    print("e")
    assert dummy_timeline.output_device.events[0] == [pytest.approx(0.0), "note_on", 1, 64, 0]
    print("f")
    assert dummy_timeline.output_device.events[1] == [pytest.approx(1.0), "note_off", 1, 0]
    print("g")
    # assert False


def test_timeline_wrk(dummy_timeline, dummy_timeline2):

    def mid_meta_message(msg: mido.MetaMessage = None, *args, **kwargs):
        # return None
        if not msg:
            msg = mido.MetaMessage(*args, **kwargs)
        dummy_timeline.output_device.miditrack[0].append(msg)

    def set_tempo(tempo):
        dummy_timeline.set_tempo(int(tempo))
        # tempo = mido.tempo2bpm(msg.tempo)
        mid_meta_message(type='set_tempo', tempo=int(mido.tempo2bpm(tempo)), time=0)

    def mid_meta_message2(msg: mido.MetaMessage = None, *args, **kwargs):
        # return None
        if not msg:
            msg = mido.MetaMessage(*args, **kwargs)
        dummy_timeline2.output_device.miditrack[0].append(msg)

    def set_tempo2(tempo):
        dummy_timeline2.set_tempo(int(tempo))
        # tempo = mido.tempo2bpm(msg.tempo)
        mid_meta_message2(type='set_tempo', tempo=int(mido.tempo2bpm(tempo)), time=0)

        print(f'{tempo=}')
    events = {
        # iso.EVENT_NOTE: iso.PSequence(sequence= [71, 62, 64, 65, 67, 69], repeats=1)
        # , iso.EVENT_DURATION : iso.PSequence(sequence=[1, 1, 1], repeats=2)
        iso.EVENT_NOTE: iso.PSequence(sequence=[71, 62, 60], repeats=1)
        , iso.EVENT_DURATION: iso.PSequence(sequence=[0.5, 1, 1], repeats=1)
        , iso.EVENT_CHANNEL: 0
        # , iso.EVENT_ACTION : iso.PSequence(sequence = [lambda: print('asdf1'), lambda: print('asdf2'), lambda: print('asdf3')], repeats=1)
        # ,iso.EVENT_ACTION : iso.PSequence(sequence=[None, lambda: print('x'), None], repeats=1)
    }

    events2 = {
        iso.EVENT_NOTE: iso.PSequence(sequence= [75,  69,  72], repeats=1)
        , iso.EVENT_DURATION : iso.PSequence(sequence=[2, 2, 2], repeats=1)
        , iso.EVENT_CHANNEL : 4
        # , iso.EVENT_ACTION : iso.PSequence(sequence = [lambda: print('asdf1'), lambda: print('asdf2'), lambda: print('asdf3')], repeats=1)
        # ,iso.EVENT_ACTION : iso.PSequence(sequence=[None, lambda: print('x'), None], repeats=1)
    }

    events_action= {
        # iso.EVENT_NOTE: iso.PSequence(sequence= [60, 72], repeats=1),
        # , iso.EVENT_GATE : iso.PSequence(sequence=[1, 1, 0.5], repeats=1)
        iso.EVENT_DURATION : iso.PSequence(sequence = [0.1, 1, 0.1, 1], repeats=1)
        # iso.EVENT_TIME : iso.PSequence(sequence=[1, 10], repeats=1)
        # , iso.EVENT_ACTION : iso.PSequence(sequence=[lambda: set_tempo(30), lambda: set_tempo(180)], repeats=1)
        , iso.EVENT_ACTION : iso.PSequence(sequence=[lambda: set_tempo(30), lambda: set_tempo(30),lambda: set_tempo(300), lambda: set_tempo(200)], repeats=1)
        # , iso.EVENT_ACTION : iso.PSequence(sequence = [lambda: print('asdf1'), lambda: print('asdf2')], repeats=1)
        # ,iso.EVENT_ACTION : iso.PSequence(sequence=[None, lambda: print('x'), None], repeats=1)
    }
    dummy_timeline.schedule(events)
    # dummy_timeline.schedule(events2)
    dummy_timeline.schedule(events_action)
    dummy_timeline.run()
    # dummy_timeline.background()
    skipp = True
    skipp = False
    if not skipp:
        for track in dummy_timeline.output_device.miditrack:
            for note in track:
                if note.type == 'note_off':
                    note_tmp_dict = note.__dict__
                    note_tmp_dict['velocity'] = 0
                    note_tmp_dict['type'] = 'note_on'
                    note.from_dict(note_tmp_dict)
    x = 1
    dummy_timeline.output_device.write()
    print('-'*20, 'second_timeline')

    file = os.path.join('..', '..', 'checks', 'example_midi', 'Var_tempo_1_trk_sax.mid')
    file_input_device = iso.MidiFileInputDevice(file)

    file_input_device = iso.MidiFileInputDevice(tmp_filename)
    # file_input_device = iso.MidiFileInputDevice(tmp_filenameX)
    patterns = file_input_device.read()
    def app_time():
        dummy_timeline2.event_times.append(time.time())
    dummy_timeline2.event_times = []
    for pattern in patterns:
        action_fun = pattern.pop(iso.EVENT_ACTION, None)
        # action_time = pattern.pop(iso.EVENT_TIME, None)

        flag = True
        if action_fun:
            action_fun = [partial(f, dummy_timeline2) for f in action_fun]
            # action_fun = [lambda: app_time() for f in action_fun]
            # action_fun = [lambda x=x: f(timeline, x) for f, x in action_fun]
            action_fun = iso.PSequence(action_fun, repeats=1)
            # action_time = iso.PSequence(action_time, repeats=1)

            dummy_timeline2.schedule({iso.EVENT_ACTION: action_fun,
                                      iso.EVENT_DURATION: pattern.get(iso.EVENT_DURATION, None)}, remove_when_done=flag)
            # dummy_timeline2.schedule({iso.EVENT_ACTION: iso.PSequence(sequence=[lambda: app_time(), lambda: app_time()], repeats=1),
            #                           iso.EVENT_DURATION: pattern.get(iso.EVENT_DURATION, None)}, remove_when_done=flag)

            # dummy_timeline2.schedule({iso.EVENT_ACTION: action_fun,
            #                           iso.EVENT_TIME: action_time}, remove_when_done=flag)
            # dummy_timeline2.schedule({iso.EVENT_TIME: action_time}, remove_when_done=flag)
            # pass
        else:
            dummy_timeline2.schedule(pattern, remove_when_done=flag)

    # time_ref = time.time()
    dummy_timeline2.run()
    print(dummy_timeline2.event_times)
    # time_gap = [(t-time_ref) for t in dummy_timeline2.event_times]
    # time_gap = [(120 / 48) * 1.0 /(t-time_ref) for t in dummy_timeline2.event_times]
    dummy_timeline2.output_device.write()
    # print(time_gap)
    # timeline.event_times = []
    # timeline.schedule({
    #     iso.EVENT_ACTION: lambda: timeline.event_times.append(time.time()),
    #     iso.EVENT_DURATION: iso.PSequence([ 0.001 ], 50)
    # })
    # timeline.run()
    x = 1

def test_action(dummy_timeline2):
    def app_time():
        dummy_timeline2.event_times.append(time.time())
    events_action = {
        iso.EVENT_NOTE: iso.PSequence(sequence= [1,2], repeats=1),
        # , iso.EVENT_GATE : iso.PSequence(sequence=[1, 1, 0.5], repeats=1)
        iso.EVENT_DURATION : iso.PSequence(sequence = [2, 1], repeats=1)
        # iso.EVENT_TIME: iso.PSequence(sequence=[1111, 10], repeats=1)
        # , iso.EVENT_ACTION: iso.PSequence(sequence=[lambda: app_time(), lambda: app_time()], repeats=1)
        }
    # timeline.schedule({
    #     iso.EVENT_ACTION: lambda: timeline.event_times.append(time.time()),
    #     iso.EVENT_DURATION: iso.PSequence([ 0.001 ], 50)
    # })
    dummy_timeline2.event_times = []
    dummy_timeline2.schedule(events_action)
    time_ref = time.time()
    dummy_timeline2.run()
    time_gap = [(t-time_ref) for t in dummy_timeline2.event_times]
    print(time_gap)
    x = 1

class Blah:
    def __init__(self, aaaa):
        self.aaaa=1

from abc import ABC, abstractmethod
class MetaMessageInterface(ABC):

    @abstractmethod
    def to_meta_message(self):
        return None
class MidiMetaMessageTempox(MetaMessageInterface):
    def __init__(self, tempo: int, location):
        #   0..16777215
        self.tempo = tempo
        self.location = location
        self.is_meta = True

    def to_meta_message(self):
        return mido.MetaMessage(tempo=self.tempo, time=self.location, type='set_tempo')


def test_track_play(dummy_timeline2):
    from isobar import MidiFileInputDevice
    events_trk1 = {
        iso.EVENT_NOTE: iso.PSequence(sequence= [1,2], repeats=1),
        iso.EVENT_DURATION : iso.PSequence(sequence = [2, 1], repeats=1),
        iso.EVENT_CHANNEL : 0
        }

    events_trk2 = {
        iso.EVENT_NOTE: iso.PSequence(sequence= [3,4], repeats=1),
        iso.EVENT_DURATION : iso.PSequence(sequence = [2, 1], repeats=1),
        iso.EVENT_CHANNEL : 5
        }
    # timeline.schedule({
    #     iso.EVENT_ACTION: lambda: timeline.event_times.append(time.time()),
    #     iso.EVENT_DURATION: iso.PSequence([ 0.001 ], 50)
    # })
    # MidiFileInputDevice.print_obj(dummy_timeline2, MidiMessageProgram(channel=2, program=3, location=0))


    events_action = {
        # iso.EVENT_ACTION: iso.PSequence(sequence= [MidiMessageProgram(channel=2, program=3, location=0)], repeats=1),
        iso.EVENT_ACTION:  lambda: dummy_timeline2.output_device.program_change(program=2, channel=5),
        # iso.EVENT_ACTION: iso.PSequence(sequence= [lambda: print('lambda')], repeats=1),
        # iso.EVENT_ACTION: lambda: print('lambda'),
        iso.EVENT_DURATION : iso.PSequence(sequence = [3], repeats=1)
        }


    # print_obj(self, timeline, objects)
    dummy_timeline2.schedule(events_trk1)
    dummy_timeline2.schedule(events_trk2)
    dummy_timeline2.schedule(events_action)
    dummy_timeline2.run()

    x = 1


def test_track_assignment(dummy_timeline, dummy_timeline2):
    dummy_tim = dummy_timeline

    def mid_meta_message(msg: mido.MetaMessage = None, *args, **kwargs):
        # return None
        track_idx = kwargs.pop('track_idx', 0)
        if not msg:
            msg = mido.MetaMessage(*args, **kwargs)
        dummy_tim.output_device.miditrack[track_idx].append(msg)

    def set_tempo(tempo):
        # dummy_timeline.set_tempo(int(tempo))
        # tempo = mido.tempo2bpm(msg.tempo)
        mid_meta_message(type='set_tempo', tempo=int(mido.tempo2bpm(tempo)), time=0)

    def track_name(name, track_idx=0):
        # dummy_timeline.set_tempo(int(tempo))
        # tempo = mido.tempo2bpm(msg.tempo)
        mid_meta_message(type='track_name', name=name, time=0, track_idx=track_idx)

    events = {

        iso.EVENT_NOTE: iso.PSequence(sequence=[71, 62, 60], repeats=1)
        , iso.EVENT_DURATION: iso.PSequence(sequence=[0.5, 1, 1], repeats=1)
        , iso.EVENT_CHANNEL: 0
        # , iso.EVENT_PROGRAM_CHANGE: 0
    }

    events2 = {
        iso.EVENT_NOTE: iso.PSequence(sequence= [75,  69,  72], repeats=1)
        , iso.EVENT_DURATION : iso.PSequence(sequence=[2, 2, 2], repeats=1)
        , iso.EVENT_CHANNEL : 4
        # , iso.EVENT_PROGRAM_CHANGE : 56
        # , iso.EVENT_ACTION : iso.PSequence(sequence = [lambda: print('asdf1'), lambda: print('asdf2'), lambda: print('asdf3')], repeats=1)
        # ,iso.EVENT_ACTION : iso.PSequence(sequence=[None, lambda: print('x'), None], repeats=1)
    }

    pgm = {

        iso.EVENT_CHANNEL : 0
        , iso.EVENT_PROGRAM_CHANGE : iso.PSequence([7], repeats=1)
    }

    pgm2 = {
        iso.EVENT_CHANNEL : 4
        , iso.EVENT_PROGRAM_CHANGE : iso.PSequence([56], repeats=1)
    }
    events_action= {

        iso.EVENT_DURATION : iso.PSequence(sequence = [1, 1, 1, 1], repeats=1)
        # , iso.EVENT_ACTION : iso.PSequence(sequence=[lambda: (set_tempo(31), set_tempo(35), track_name('blah'), track_name('blaxx',1)), lambda: set_tempo(30),lambda: set_tempo(300), lambda: set_tempo(200)], repeats=1)
        , iso.EVENT_ACTION : iso.PSequence(sequence=[lambda: (set_tempo(31),  track_name('blah'), track_name('blaxx',1)), lambda: set_tempo(30),lambda: set_tempo(300), lambda: set_tempo(200)], repeats=1)
        # , iso.EVENT_ACTION : iso.PSequence(sequence=[lambda: set_tempo(31), lambda: set_tempo(30),lambda: set_tempo(300), lambda: set_tempo(200)], repeats=1)

    }

    dummy_tim.schedule(pgm)
    dummy_tim.schedule(pgm2)
    dummy_tim.schedule(events)
    dummy_tim.schedule(events2)

    dummy_tim.schedule(events_action)
    dummy_tim.run()
    # dummy_timeline.background()

    dummy_tim.output_device.write()
    filename = os.path.join(this_dir, '..', 'tests', 'x1x1a.mid')
    print(dummy_tim.output_devices[0].filename)
    print_mid(dummy_tim.output_devices[0].filename)

    # return
    print('-'*20, 'second_timeline')
    dummy_tim2 = dummy_timeline2
    # file = os.path.join('..', '..', 'checks', 'example_midi', 'Var_tempo_1_trk_sax.mid')
    # file_input_device = iso.MidiFileInputDevice(file)

    file_input_device = iso.MidiFileInputDevice(dummy_tim.output_devices[0].filename)
    # file_input_device = iso.MidiFileInputDevice(tmp_filenameX)
    patterns = file_input_device.read()
    def app_time():
        dummy_tim2.event_times.append(time.time())
    dummy_tim2.event_times = []
    for pattern in patterns:
        action_fun = pattern.pop(iso.EVENT_ACTION, None)
        # action_time = pattern.pop(iso.EVENT_TIME, None)

        flag = True
        if action_fun:
            # action_fun = [partial(f, dummy_tim2) for f in action_fun]
            # action_fun = [lambda: app_time() for f in action_fun]
            # action_fun = [lambda x=x: f(timeline, x) for f, x in action_fun]
            # action_fun = iso.PSequence(action_fun, repeats=1)
            # action_time = iso.PSequence(action_time, repeats=1)

            dummy_tim2.schedule({iso.EVENT_ACTION: action_fun,
                                      iso.EVENT_DURATION: pattern.get(iso.EVENT_DURATION, None)}, remove_when_done=flag)
            # dummy_timeline2.schedule({iso.EVENT_ACTION: iso.PSequence(sequence=[lambda: app_time(), lambda: app_time()], repeats=1),
            #                           iso.EVENT_DURATION: pattern.get(iso.EVENT_DURATION, None)}, remove_when_done=flag)

            # dummy_timeline2.schedule({iso.EVENT_ACTION: action_fun,
            #                           iso.EVENT_TIME: action_time}, remove_when_done=flag)
            # dummy_timeline2.schedule({iso.EVENT_TIME: action_time}, remove_when_done=flag)
            # pass
        else:
            dummy_tim2.schedule(pattern, remove_when_done=flag)

    # time_ref = time.time()
    dummy_tim2.run()
    print(dummy_tim2.event_times)
    # time_gap = [(t-time_ref) for t in dummy_timeline2.event_times]
    # time_gap = [(120 / 48) * 1.0 /(t-time_ref) for t in dummy_timeline2.event_times]
    dummy_tim2.output_device.write()
    # print(dummy_tim2.output_devices[0].filename)
    print_mid(dummy_tim2.output_devices[0].filename)
    # print(time_gap)
    # timeline.event_times = []
    # timeline.schedule({
    #     iso.EVENT_ACTION: lambda: timeline.event_times.append(time.time()),
    #     iso.EVENT_DURATION: iso.PSequence([ 0.001 ], 50)
    # })
    # timeline.run()
    x = 1