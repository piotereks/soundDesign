import time
import isobar as iso
from isobar_fixes import *

# one time init    (this is the best to used globals)
# One time is sufficient, so basically this may be repeated

import os
import inspect
from beats import *
from patterns import *
from log_call import *
import pprint
from copy import deepcopy
from queue import Queue
import mido
import math
import shutil
from datetime import datetime
# import mido


# <editor-fold desc="Init section">


global IN_COLAB
IN_COLAB = 'google.colab' in sys.modules
NO_MIDI_OUT = mido.get_output_names() == [];

global MULTI_TRACK
MULTI_TRACK = True
# MULTI_TRACK = False

if MULTI_TRACK:
    class MidiFileManyTracksOutputDevice(iso.MidiFileOutputDevice):


        def __init__(self, filename):
            self.filename = filename
            self.midifile = mido.MidiFile()
            self.miditrack = [mido.MidiTrack()]
            self.midifile.tracks.append(self.miditrack[0])
            # for track in self.miditrack:
            #     self.midifile.tracks.append(track)
            # [self.midifile.tracks.append(track) for track in self.miditrack]
            self.channel_track = []
            self.channel_track.append(0)
            # self.time = 0
            # self.last_event_time = 0
            self.time = []
            self.time.append(0)
            self.last_event_time = []
            self.last_event_time.append(0)



        def extra_track(self, channel=None):
            if channel:
                if not [x for x in self.channel_track if x == channel]:
                    track=mido.MidiTrack()
                    self.miditrack.append(track)
                    self.midifile.tracks.append(track)
                    self.channel_track.append(channel)
                    self.time.append(0)
                    self.last_event_time.append(0)

        def get_channel_track(self, channel=0):
            try:
                track = self.channel_track.index(channel)
            except:
                track = 0
            return track

        def note_on(self, note=60, velocity=64, channel=0):
            #------------------------------------------------------------------------
            # avoid rounding errors
            #------------------------------------------------------------------------
            track = self.get_channel_track(channel)
            print(f"----------------track var: {channel=} {track=}")
            if track >= 0:
                print(f"------------note on: {track=}, {note=}, {channel=}")
                dt = self.time[track] - self.last_event_time[track]
                dt_ticks = int(round(dt * self.midifile.ticks_per_beat))
                self.miditrack[track].append(mido.Message('note_on', note=note, velocity=velocity, channel=channel, time=dt_ticks))
                self.last_event_time[track] = self.time[track]

        def note_off(self, note=60, channel=0):
            track = self.get_channel_track(channel)
            if track >= 0:
                print(f"------------note on: {track=}, {note=}, {channel=}")
                dt = self.time[track] - self.last_event_time[track]
                dt_ticks = int(round(dt * self.midifile.ticks_per_beat))
                self.miditrack[track].append(mido.Message('note_off', note=note, channel=channel, time=dt_ticks))
                self.last_event_time[track] = self.time[track]


        def tick(self):
            # for time in self.time:
            #     time += 1.0 / self.ticks_per_beat
            self.time = list(map(lambda x : x + (1.0 / self.ticks_per_beat), self.time))

            pass



if not MULTI_TRACK:
    class MidiFileManyTracksOutputDevice(iso.MidiFileOutputDevice):
        pass

        def tick(self):
            super().tick()


        def note_on(self, note=60, velocity=64, channel=0):
            super().note_on(note, velocity, channel)

        def note_off(self, note=60, channel=0):
            super().note_off(note, channel)


    # def __init__(self, filename):
    #     super.__init__(self, filename=filename)

# class FileOut(iso.MidiFileOutputDevice, iso.MidiOutputDevice):
class FileOut(MidiFileManyTracksOutputDevice, iso.MidiOutputDevice):

    def __init__(self, filename, device_name, send_clock, virtual=False):
        # iso.MidiFileOutputDevice.__init__(self, filename=filename)
        MidiFileManyTracksOutputDevice.__init__(self, filename=filename)
        iso.MidiOutputDevice.__init__(self, device_name=device_name, send_clock=send_clock, virtual=virtual)

    # def all_notes_off(self):
    #     # iso.MidiFileOutputDevice.all_notes_off(self)
    #     # MidiFileManyTracksOutputDevice.all_notes_off(self)
    #     # iso.MidiOutputDevice.all_notes_off(self)
    #     super().all_notes_off()
    #
    # def control(self, control, value, channel):
    #     # iso.MidiFileOutputDevice.control(self, control=control, value=value, channel=channel)
    #     # MidiFileManyTracksOutputDevice.control(self, control=control, value=value, channel=channel)
    #     # iso.MidiOutputDevice.control(self, control=control, value=value, channel=channel)
    #     super().control(control=control, value=value, channel=channel)
    #
    # def note_off(self,  note, channel):
    #     # iso.MidiFileOutputDevice.note_off(self, note=note, channel=channel)
    #     # MidiFileManyTracksOutputDevice.note_off(self, note=note, channel=channel)
    #     # iso.MidiOutputDevice.note_off(self, note=note, channel=channel)
    #     super().note_off(note=note, channel=channel)
    #
    # def note_on(self, note, velocity, channel):
    #     print(f"----------------{channel=}")
    #     # iso.MidiFileOutputDevice.note_on(self, note=note, velocity=velocity, channel=channel)
    #     # MidiFileManyTracksOutputDevice.note_on(self, note=note, velocity=velocity, channel=channel)
    #     # iso.MidiOutputDevice.note_on(self, note=note, velocity=velocity, channel=channel)
    #     super().note_on(note=note, velocity=velocity, channel=channel)
    #
    # def program_change(self, program=0, channel=0):
        # iso.MidiFileOutputDevice.program_change(self, program=program, channel=channel)
        # MidiFileManyTracksOutputDevice.program_change(self, program=program, channel=channel)
        # iso.MidiOutputDevice.program_change(self, program=program, channel=channel)
        # super().program_change(program=program, channel=channel)

    #
    #
    # def start(self):
    #     # iso.MidiFileOutputDevice.start(self)
    #     # MidiFileManyTracksOutputDevice.start(self)
    #     # iso.MidiOutputDevice.start(self)
    #     super().start()
    #
    # def stop(self):
    #     # iso.MidiFileOutputDevice.stop(self)
    #     # MidiFileManyTracksOutputDevice.stop(self)
    #     # iso.MidiOutputDevice.stop(self)
    #     super().stop()
    #
    # def tick(self):
    #     # iso.MidiFileOutputDevice.tick(self)
    #     # MidiFileManyTracksOutputDevice.tick(self)
    #     # iso.MidiOutputDevice.tick(self)
    #     super().tick()

    # def write(self):
    #     iso.MidiFileOutputDevice.write(self)


    # def ticks_per_beat(self):
    #     iso.MidiFileOutputDevice.ticks_per_beat
    #         ticks_per_beat(self, *args, **kwargs)
    #     iso.MidiOutputDevice.ticks_per_beat(self, *args, **kwargs)

# self.midi_out = iso.MidiFileOutputDevice(filename)
# print("file mode")
# elif midi_out_mode == self.MIDI_OUT_DEVICE and not NO_MIDI_OUT:
# self.midi_out = iso.MidiOutputDevice(device_name=self.name, send_clock=True)

global my_tracker


# def log_call():
#     print(inspect.stack()[1][3])
# </editor-fold>



class Tracker:
    # <editor-fold desc="Class init functions">
    MIDI_OUT_DUMMY = 0
    MIDI_OUT_FILE = 1
    MIDI_OUT_DEVICE = 2
    MIDI_OUT_MIX_FILE_DEVICE = 3


    name = "Microsoft GS Wavetable Synth 0"



    # degree = 0

    # name = "Bome Virtual MIDI Port 2"
    # name = "Bome Virtual MIDI Port 4"
    # name = "Virtual Midi"

    # name= "loopMIDI 6"
    def __init__(self,
                 # interval_array=None, note_array=None, midi_note_array=None,
                 midi_out_mode='dummy',
                 filename=os.path.join("saved_midi_files","xoutput.mid")):

        read_config_file_scales()
        # my_beats = Beats()
        # self.scale = iso.Scale.major  - replaced by key, and scale always can be referred as self.key.scale
        self.key = iso.Key("C", "major")
        self.prev_key = None
        self.loopq = None
        # self.root_midi = [('C')]  #TODO check what is root_midi used for
        self.midi_out = None
        self.track = None
        self.filename = filename
        log_call()
        self.beat_count = -1 % 4
        self.diff_time = 0
        self.prev_time = 0
        self.timeline = None
        self.note_patterns = NotePatterns()
        self.prev_get_pattern_name = None
        self.root_note = 0
        self.last_note = None
        self.last_from_note = None
        self.notes_pair =[None,None]
        self.queue_content_wrk = None
        self.note_queue = Queue(maxsize = 16)
        self.amp_for_beat_factor = dict(zip([0, 2], [1.5, 1.25]))


        self.pattern_idx = 0


        # self.init_timeline(True)
        self.init_timeline(midi_out_mode)
        self.beat = lambda: self.play_from_to(None,None,in_pattern=True)
        self.metro_beat = lambda: print('metro_beat init')
        # self.play_from_to(None, None, in_pattern=True)
        # self.beat = self.beat_none
        # my_tracker.metronome_start()


        # self.set_program_change(program=30)
        self.tmln = self.tracker_timeline()
        self.metro = self.metro_timeline()


    def save_midi(self):
        date = datetime.now().strftime('%Y%m%d%H%M%S')
        self.midi_out.write()
        shutil.copy(self.filename, f"{self.filename.split('.')[0]}_{date}.mid")

    def init_timeline(self, midi_out_mode='dummy'):
        log_call()
        print(f" Device:{midi_out_mode}")
        print(f"{NO_MIDI_OUT=}")
        filename = self.filename

        if midi_out_mode == self.MIDI_OUT_FILE:
            self.midi_out = iso.MidiFileOutputDevice(filename)
            print("file mode")
        elif midi_out_mode == self.MIDI_OUT_DEVICE and not NO_MIDI_OUT:
            self.midi_out = iso.MidiOutputDevice(device_name=self.name, send_clock=True)
            print("device mode")
        elif midi_out_mode ==  self.MIDI_OUT_MIX_FILE_DEVICE:
            self.midi_out = FileOut(filename=filename, device_name=self.name, send_clock=True, virtual = NO_MIDI_OUT)
            # self.midi_out = FileOut(filename=filename, device_name=self.name, send_clock=True, virtual=True)
            print("device mode")
        else:
            self.MIDI_OUT_DUMMY
            self.midi_out = iso.DummyOutputDevice()
            print("dummy mode")

        print(f"----------- {MULTI_TRACK=}")
        # midi_out = iso.DummyOutputDevice()
        self.timeline = iso.Timeline(120, output_device=self.midi_out)
        # self.timeline.background()  # use background ts()instead of run to enable live performing (async notes passing)
        # self.tstart()
    # </editor-fold>


    def get_amp_factor(self):
        accent = self.amp_for_beat_factor.get(self.beat_count)
        return accent if accent else 1


    def log_and_schedule(func):
        def inner(self, *args, **kwargs):
            log_call()
            print(func.__name__)
            self.beat_count += 1
            self.diff_time = self.timeline.current_time - self.prev_time
            self.prev_time = self.timeline.current_time
            print(f"{func.__name__} diff:{self.diff_time}, timeXX: {self.timeline.current_time},"
                  f" {round(self.timeline.current_time)} beat: {self.beat_count}\n")
            self.beat_count %= 4
            # print('bef func')
            # print('args: ',*args)
            # print('kwargs: ', ** kwargs)
            notes = func(self, *args, **kwargs)
            # print("result type: ",type(result), result)
            # if type(result) == 'tuple':
            #     notes, skip = result
            # else:
            #     notes, skip = result, False
            # print('skip checked: ', skip)
            # if not skip:
            # notes[iso.EVENT_NOTE] = iso.PMap(notes[iso.EVENT_NOTE], lambda midi_note: None if not midi_note else None if midi_note < 0 else None if midi_note > 127 else midi_note)
            notes[iso.EVENT_NOTE] = iso.PMap(notes[iso.EVENT_NOTE], lambda midi_note:
            (None if not midi_note else None if midi_note < 0 else None if midi_note > 127 else midi_note)
            if isinstance(midi_note, np.int64) or isinstance(midi_note, int)
            else tuple(map(lambda u: None if not u else None if u < 0 else None if u > 127 else u, midi_note)))

            # create accent depending on beat
            # notes[iso.EVENT_AMPLITUDE] = iso.PMap(notes[iso.EVENT_AMPLITUDE], lambda midi_amp: None if not midi_amp else None if midi_amp < 0 else 127 if midi_amp > 127 else int(midi_amp * 1.5)   )
            notes[iso.EVENT_AMPLITUDE] = iso.PMapEnumerated(notes[iso.EVENT_AMPLITUDE], lambda n, value: int(value*self.get_amp_factor()) if n==0 else value)

            notes[iso.EVENT_AMPLITUDE] = iso.PMap(notes[iso.EVENT_AMPLITUDE], lambda midi_amp: None if not midi_amp else None if midi_amp < 0 else None if midi_amp > 127 else midi_amp)

            self.check_notes=list(notes[iso.EVENT_NOTE].copy())
            print('check notes: ', self.check_notes)
            self.check_notes_action()
            # print('aft func')
            xxx = self.timeline.schedule(
                notes
                # ,replace=True,  # this is not working with version 0.1.1, only with github
                # name="blah"  # this is not working with version 0.1.1, only with github

            )
            print('post sched')

        return inner

    # <editor-fold desc="Base beat functions">
    @log_and_schedule
    def beat1(self):
        return iso.PDict({
            iso.EVENT_NOTE:iso.PSequence([1, 3, 2, 4], repeats=1) +72 })

    @log_and_schedule
    def beat2(self):
        return  iso.PDict({
            iso.EVENT_NOTE:iso.PSequence([1, 3, 2, 4, 3, 5], repeats=1) + 66})

    @log_and_schedule
    def beat_none(self):
        return iso.PDict({
            iso.EVENT_NOTE: iso.PSequence([None], repeats=4)})
    # </editor-fold>


    # <editor-fold desc="Metro functions">

    def metro_timeline(self):
        log_call()
        if MULTI_TRACK:
            self.midi_out.extra_track(9)  # for percussion channel 10 (or 9 when counting from 0).
        return self.timeline.schedule({
            "action": lambda: self.metro_beat()
            ,"duration": 4
            # ,"quantize": 1
        }
            # , quantize=1
            , remove_when_done=False
        )

    def metro_none(self):
        log_call()
        xxx = self.timeline.schedule({
            # "action" : lambda: print('XXXXXXXXXXXXXXX'),
            # "note": iso.PSequence([1, 5, 5, 5]) +gap,
            # "note": iso.PSequence([82, 69, 69, 69]) ,
            iso.EVENT_NOTE: iso.PSequence([None], repeats=1),
            # "note" : iso.PSeries(1,1),
            "duration": 1,
            "channel": 9,
            # "quantize": 1
        }
            # , quantize=1
            , remove_when_done=True)

        # @log_and_schedule

    def metro_play(self):
        log_call()
        xxx = self.timeline.schedule({
            # "action" : lambda: print('XXXXXXXXXXXXXXX'),
            # "note": iso.PSequence([1, 5, 5, 5]) +gap,
            # "note": iso.PSequence([82, 69, 69, 69]) ,
            "note": iso.PSequence([32, 37, 37, 37], repeats=1),
            # "note" : iso.PSeries(1,1),
            "duration": 1-0.000000000000002,
            "channel": 9,
            "amplitude": iso.PSequence([55, 45, 45, 45],  repeats=1),
            # "quantize": 1
        }
            # , quantize=1
            , remove_when_done=True)

    def metro_start_stop(self, start):
        if start.get() == 1:
            print('-----------metro on-----------------')
            # self.metro_beat = lambda: print ('metro_play')
            self.metro_beat = self.metro_play
            # self.metro_beat = lambda: self.beat1()
        else:
            print('-----------metro off-----------------')
            # self.metro_beat = lambda: print ('metro_none')
            self.metro_beat = self.metro_none
            # self.metro_beat = lambda: self.beat2()
        pass
    # </editor-fold>

    # <editor-fold desc="Gui actions">
    def loop_play_queue_action(self, flag):
        if flag == 0:
            self.loopq = False
        else:
            self.loopq = True

    def check_notes_action(self):
        log_call()

    def scale_name_action(self):
        log_call()

    def queue_content_action(self):
        log_call()

    def curr_notes_pair_action(self):
        log_call()

    def fullq_content_action(self):
        log_call()

    # </editor-fold>

    # <editor-fold desc="Queue functions">
    def get_queue_content(self):
        return 'empty' if self.note_queue.empty() else list(self.note_queue.queue)
        # return 'empty' if self.note_queue.empty() else xxx

    def get_queue_content_full(self):
        # queue_v = list(['bbbb'])
        queue_v = []


        print(f"{self.notes_pair[0]=} {queue_v}")
        if self.notes_pair[0]:
            queue_v += list([self.notes_pair[0]])
        if not self.note_queue.empty():
            queue_v += list(self.note_queue.queue)
        return 'Empty' if not queue_v else queue_v


    def get_queue_pair(self):
        v_queue = list(self.note_queue.queue)
        if len(v_queue) >= 2:
            return v_queue[0], v_queue[1]
        elif len(v_queue) == 1:
            return v_queue[0], None
        else:
            return None, None



    def put_to_queue(self, note, q_action = True):

        if not self.note_queue.full():
            self.note_queue.put(note)
            if q_action:
                self.queue_content_action()
                self.fullq_content_action()

    def get_from_queue(self):

        note = None if self.note_queue.empty() else self.note_queue.get_nowait()
        print(f"{self.loopq=}")
        # if self.loopq and self.last_from_note is not None:
        #     # print(f'note {note} back to queue')
        #     # self.put_to_queue(note)
        #     print(f'note {self.last_from_note=} back to queue')
        #     self.put_to_queue(self.last_from_note)

        self.queue_content_action()
        self.fullq_content_action()
        return note
    # </editor-fold>

    # <editor-fold desc="play functions">

    # <editor-fold desc="play definitions">
    # def set_program_change(self, program_nr = 0, channel = 0):
        # self.timeline.schedule({
        #     iso.EVENT_PROGRAM_CHANGE: program_nr,
        #
        #     iso.EVENT_CHANNEL: iso.DEFAULT_EVENT_CHANNEL
        # })
        # control_series = iso.PSeries(start=1, step=2, length=3)
        # self.timeline.schedule({
        #     iso.EVENT_CONTROL: 0,
        #     iso.EVENT_VALUE: control_series,
        #     iso.EVENT_DURATION: 1,
        #     iso.EVENT_CHANNEL: 0
        # })
        # control_series = iso.PSeries(start=1, step=2, length=3)
        # self.timeline.schedule({
        #     iso.EVENT_PROGRAM_CHANGE: 22,
        #     iso.EVENT_VALUE: control_series,
        #     iso.EVENT_DURATION: 1,
        #     iso.EVENT_CHANNEL: 0
        # })
        # pass

    def tracker_timeline(self):
        log_call()
        return self.timeline.schedule({
            "action": lambda: self.beat()
            ,"duration": 4
            # "quantize": 1
        }
            # , quantize=1
            , remove_when_done=False
        )

    def set_tempo(self, new_tempo):
        log_call()
        print(f"b_read tempo: {self.timeline.get_tempo()=}, {new_tempo=}")
        # self.timeline.set_tempo(int(new_tempo))
        self.timeline.set_tempo(int(new_tempo))
        if MULTI_TRACK:
            self.midi_out.miditrack[0].append(mido.MetaMessage('set_tempo',tempo=mido.bpm2tempo(int(new_tempo)), time=0))
        else:
            self.midi_out.miditrack.append(mido.MetaMessage('set_tempo',tempo=mido.bpm2tempo(int(new_tempo)), time=0))
        print(f"a_read tempo: {self.timeline.get_tempo()=}, {new_tempo=}")

    def set_program_change(self, program = 0, channel = 0):
        log_call()
        self.midi_out.program_change(program=int(program), channel=int(channel))
        if MULTI_TRACK:
            self.midi_out.miditrack[0].append(mido.Message('program_change', program=int(program), channel=int(channel)))
        else:
            self.midi_out.miditrack.append(mido.Message('program_change', program=int(program), channel=int(channel)))

    def write_mid_text_meta(self, message):
        if MULTI_TRACK:
            self.midi_out.miditrack[0].append(mido.MetaMessage('text',text=message, time=0))
        else:
            self.midi_out.miditrack.append(mido.MetaMessage('text',text=message, time=0))


    def meta_key_scale(self, key, scale):
        self.write_mid_text_meta(f"scale:{key}-{scale}")


    def meta_func(self,func):
        self.write_mid_text_meta(f"func:{func}")


    def meta_tempo(self,tempo):
        self.write_mid_text_meta(f"tempo:{tempo}")


    def ts(self):
        log_call()
        self.timeline.stop()

    def tstart(self):
        log_call()
        self.timeline.background()

        # @log_and_schedule
    # </editor-fold>


    @log_and_schedule
    def play_from_to(self, from_note, to_note, in_pattern=False ):
        print('---------------------')
        print(f"in_pattern: {in_pattern} from_note:{from_note}, to_note: {to_note}")
        print(f"{self.key.scale.name=}, key={iso.Note.names[self.key.tonic%12]}, {self.key.scale.name=}")
        # print(f"{self.scale.name=}, {self.key.tonic=}")

        # self.prev_get_pattern
        # self.patterns.get_pattern
        # self.prev_key
        # self.key.scale.name
        # self.key.tonic

        if self.prev_get_pattern_name != self.note_patterns.get_pattern.__name__:
            # self.meta_func(func=f"prev:{self.prev_get_pattern_name}")
            self.meta_func(func=f"curr:{self.note_patterns.get_pattern.__name__}")
            # pass
        if (not self.prev_key and self.key) \
            or self.prev_key != self.key:
            # if self.prev_key:
            #     self.meta_key_scale(key=f"prev: {self.prev_key.tonic}", scale=self.prev_key.scale.name)

            self.meta_key_scale(key=f"curr: {self.key.tonic}", scale=self.key.scale.name)

        self.prev_key = self.key
        print(f"============={self.prev_get_pattern_name=} {self.note_patterns.get_pattern.__name__=}")
        self.prev_get_pattern_name = self.note_patterns.get_pattern.__name__
        # my_tracker.meta_func(func=app.play_func_combo.get())
        # my_tracker.meta_key_scale(key=app.keys_group.get(), scale=app.scale_combo.get())


        self.scale_name_action()   #TODO extend scale
        # if  from_note == None:
        #     return None
        if in_pattern:
            if self.loopq and self.last_from_note is not None:
                # print(f'note {note} back to queue')
                # self.put_to_queue(note)
                print(f'note {self.last_from_note=} back to queue')
                self.put_to_queue(self.last_from_note, q_action=False)

            from_note, to_note = self.get_queue_pair()
            if self.loopq and not to_note:
                to_note=from_note  # TODO add put to queue
                self.put_to_queue(from_note)
            # self.scale = iso.Scale.chromatic
            # self.scale = iso.Scale.chromatic
            print("if in_pattern")
            from_notex = self.last_note
            # to_note = None if self.note_queue.empty() else self.note_queue.get_nowait()
            # to_notex = self.get_from_queue()
            # if self.loopq and note is not None:
            #     print(f'note {note} back to queue')
            #     self.put_to_queue(note)

            # if not from_note and to_note:
                # from_notex = to_note
                # to_notex = self.get_from_queue()
            # to_note = self.note_queue.get_nowait()  # handle empty queue
            self.last_notex = to_note
            new_note=to_note
            # print(f"in_pattern (next pattern for later):  from_note:{from_note} new_note:{new_note}")
            # self.beat = lambda: self.play_from_to(from_note, new_note, in_pattern=True)
            print(f"in_pattern (next pattern for later):  from_note:{from_note} new_note:{to_note}")
            self.beat = lambda: self.play_from_to(from_note, to_note, in_pattern=True)
            dummy_var = self.get_from_queue()
        else:
            print("else in_pattern")
            if to_note is not None:
                print('is not None', to_note)
                self.beat = lambda: self.play_from_to(to_note, None)
            else:
                print('else ', to_note)
                self.beat = self.beat_none
        self.notes_pair=[from_note,to_note]
        self.queue_content_wrk = [from_note,to_note] + [' ']+ list(self.get_queue_content())
        self.curr_notes_pair_action()  #TODO action
        self.fullq_content_action()
        self.last_from_note=from_note
        if (to_note is None) or (from_note is None):
          from_note = None if not from_note else self.key.scale.indexOf(from_note)
          return iso.PDict({
            # iso.EVENT_NOTE: iso.PDegree(iso.PSequence([from_note], repeats=1), self.scale),
            iso.EVENT_NOTE: iso.PDegree(iso.PSequence([from_note], repeats=1), self.key),
            iso.EVENT_DURATION: iso.PSequence([4], repeats=1),
            # iso.EVENT_OCTAVE: 5
            # iso.EVENT_DEGREE: xxxx
        })   #TODO extend scale
        print('after_check')
        # root_note = self.scale.indexOf(from_note-60)
        # note = self.scale.indexOf(to_note-60)
        root_note = self.key.scale.indexOf(from_note-self.key.tonic%12)
        note = self.key.scale.indexOf(to_note-self.key.tonic%12)
        interval = note - root_note
        #print(f"{from_note=} {to_note=} {from_note-60=} {to_note-60=}  {root_note=} {note=} {interval=}")

        # pattern = self.patterns.get_random_pattern(interval) + root_note
        # print(f"{self.patterns.get_pattern(interval)=}")

        # pattern = self.patterns.get_pattern(interval) + root_note
        pattern = self.note_patterns.get_pattern(interval)


        print(f"type of pattern: {type(pattern)=}, {isinstance(pattern, np.ndarray)}")

        pattern_amplitude = np.array(None)
        pattern_gate = np.array(None)
        pattern_duration = np.array(None)
        if isinstance(pattern, np.ndarray):
            pattern_notes = pattern
        elif isinstance(pattern, dict):
            pattern_notes = pattern[iso.EVENT_NOTE]
            pattern_amplitude = pattern.get(iso.EVENT_AMPLITUDE)
            # if not isinstance(pattern_amplitude,np.ndarray):
            #     pattern_amplitude = np.array(None)
            pattern_gate = pattern.get(iso.EVENT_GATE)
            # if not isinstance(pattern_gate,np.ndarray):
            #     pattern_gate = np.array(None)
            pattern_duration = pattern.get(iso.EVENT_DURATION)
            # if not isinstance(pattern_duration,np.ndarray):
            #     pattern_duration = np.array(None)


        elif not pattern:
            pattern_notes = None
        else:
            raise Exception("No notes returned!!!")

        if isinstance(pattern_notes, int) or isinstance(pattern_notes, np.int64):
            pattern_notes+=root_note
        else:
            pattern_notes = [x + root_note if isinstance(x, np.int64) or isinstance(x, int)
                             else tuple(map(lambda u: u + root_note, x)) for x in pattern_notes]
        # xxxxx =[x + 1 if isinstance(x,np.int) else  tuple(map(lambda xx : xx +1, x)) for x   in pattern_notes]
        # [x + 11 if isinstance(x, np.int) else tuple(map(lambda u: u + 5, x)) for x in aa]
        pattern_notes = pattern_notes[:-1]
        len_pattern = len(pattern_notes)
        print(f"----debug----{pattern_notes} {len_pattern=}")
        # len_pattern = len(pattern_notes)-1
        # len_pattern = len(pattern_notes)

        if not isinstance(pattern_duration, np.ndarray):
            pattern_duration = np.array(None)
            pattern_duration = np.repeat((4 / len_pattern) - 0.000000000000002, len_pattern)
            # pattern_duration = np.repeat(1.5, len_pattern)

        if not isinstance(pattern_amplitude, np.ndarray):
            pattern_amplitude = np.array([64])

        if not isinstance(pattern_gate, np.ndarray):
            pattern_gate = np.array([1])

        # when duration size (elements) is less then multiply
        # and remove if lenth is longer after multiplication
        if pattern_duration.size<len_pattern:
            # pattern_duration = np.repeat(pattern_duration, int(len_pattern/pattern_duration.size)+1)
            pattern_mult = np.tile(pattern_duration,(int(len_pattern/pattern_duration.size)+1, 1))
            pattern_duration = pattern_mult.reshape(pattern_mult.shape[0]*pattern_mult.shape[1])
        pattern_duration = pattern_duration[:len_pattern]
        
        # rescale duration of notes
        pattern_duration = 4*pattern_duration/pattern_duration.sum()-0.000000000000002

        #recalculate/normalize duration - base is now 4 (could be different in future)
        # pattern_duration_sum=pattern_duration.sum()
        # 6 * 4/6


        print(f"{pattern_duration=}")

        print('Pseq:', list(iso.PSequence(pattern_notes, repeats=1)))
        print('Pseq + Degree - scale:', list(iso.PDegree(iso.PSequence(pattern_notes, repeats=1), self.key.scale)))
        print('Pseq + Degree - key:', list(iso.PDegree(iso.PSequence(pattern_notes, repeats=1), self.key)))
        print('bef Pdict2')
        print('=====================')

        return iso.PDict({
            # iso.EVENT_NOTE: iso.PDegree(iso.PSequence(pattern, repeats=1), self.scale),
            iso.EVENT_NOTE: iso.PDegree(iso.PSequence(pattern_notes, repeats=1), self.key),
            # iso.EVENT_DURATION: iso.PSequence([(4 / len_pattern) - 0.000000000000002], repeats=len_pattern),
            iso.EVENT_DURATION: iso.PSequence(pattern_duration, repeats=1),
            iso.EVENT_AMPLITUDE: iso.PSequence(pattern_amplitude)
            ,iso.EVENT_GATE: iso.PSequence(pattern_gate)
            # iso.EVENT_OCTAVE: 5
            # iso.EVENT_DEGREE: xxxx
        })  #TODO extend scale


    # </editor-fold>

