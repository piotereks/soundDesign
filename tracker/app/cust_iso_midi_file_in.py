# import mido
import logging
import snoop

from collections.abc import Iterable
from functools import partial
from typing import Union

from isobar import *

from .iso_midi_message import *
from .midi_dev import MULTI_TRACK

log = logging.getLogger(__name__)


class CustMidiFileInputDevice(MidiFileInputDevice):
    """ Read events from a MIDI file.
        Requires mido. """

    def __init__(self, filename):
        self.filename = filename

    # def set_tempo_callback(self, tempo):
    def set_tempo_callback(self, *args, **kwargs):
        pass

    @snoop
    def print_obj(self, timeline, objects=None, track_idx=0):

        print(f"{type(objects)}=")
        if not isinstance(objects, Iterable):
            objects = [objects]
        text = [(type(o), o.__dict__) for o in objects]
        if MULTI_TRACK:
            # if len(timeline.output_device.miditrack)-1 < track_idx:
                # timeline.output_device.extra_track(track_idx)
            # midi_track0 = timeline.output_device.miditrack[track_idx]
            midi_track0 = timeline.output_device.miditrack[0]

        else:
            midi_track0 = timeline.output_device.miditrack

        # msg = mido.MetaMessage('text', text=str(text))
        # TODO Fix here the way it is written to miditrack
        # for obj in objects:
        #     # msg2 = mido.MetaMessage(obj)
        #     if MULTI_TRACK:
        #         if timeline.output_device.miditrack[0]:
        #             timeline.output_device.miditrack[0].append(obj)
        #     else:
        #         if timeline.output_device.miditrack:
        #             timeline.output_device.miditrack.append(obj)

        for obj in objects:
            if isinstance(obj, MidiMetaMessageTempo):
                print('inside of MidiMetaMessageTempo')
                timeline.set_tempo(int(mido.tempo2bpm(obj.tempo)))
                self.set_tempo_callback(int(mido.tempo2bpm(obj.tempo)))
                msg = mido.MetaMessage('text', text=f"tempo:{int(mido.tempo2bpm(obj.tempo))}")
                midi_track0.append(msg)
            elif isinstance(obj, MidiMessageControl):
                timeline.output_device.control(control=obj.cc, value=obj.value, channel=obj.channel,
                                               track_idx=track_idx)
            elif isinstance(obj, MidiMessageProgram):
                timeline.output_device.program_change(program=obj.program, channel=obj.channel,
                                                      track_idx=track_idx)
            elif isinstance(obj, MidiMessagePitch):
                timeline.output_device.pitch_bend(self, pitch=obj.pitch, channel=obj.channel,
                                                  track_idx=track_idx)
            elif isinstance(obj, MidiMessageAfter):
                timeline.output_device.aftertouch(self, control=obj.control, value=obj.value,
                                                  channel=obj.channel, track_idx=track_idx)
            elif isinstance(obj, MidiMessagePoly):
                timeline.output_device.polytouch(self, control=obj.control, note=obj.note,
                                                 channel=obj.channel, track_idx=track_idx)

            if midi_track0 is not None and hasattr(obj, 'to_meta_message'):

                if hasattr(obj, 'channel'):
                    channel_param = obj.channel
                else:
                    channel_param = None
                new_track_idx = timeline.output_device.get_channel_track(channel=channel_param, src_track_idx=track_idx)
                # for t in list(range(len(timeline.output_device.miditrack) - 1, track_idx)):
                # # if len(timeline.output_device.miditrack) - 1 < track_idx:
                #     timeline.output_device.extra_track(new_track_idx=t+1)
                timeline.output_device.miditrack[new_track_idx].append(obj.to_meta_message())


        print(timeline, text)

    def read(self, quantize=None):
        def create_lam_function(tgt_dict, messages, track_idx = 0):
            lam_function = partial(self.print_obj, objects=messages, track_idx=track_idx)
            # lam_function = partial(self.print_obj, objects=None)
            tgt_dict[EVENT_ACTION].append(lam_function)
            if isinstance(messages, Iterable):
                msg_loc = messages[0].location
            else:
                msg_loc = messages.location
            tgt_dict[EVENT_TIME].append(msg_loc)

        midi_reader = mido.MidiFile(self.filename)
        # log.info("Loading MIDI data from %s, ticks per beat = %d" % (self.filename, midi_reader.ticks_per_beat))
        note_tracks = list(filter(lambda track: any(message.type == 'note_on' for message in track),
                                  midi_reader.tracks))
        if not note_tracks:
            raise ValueError("Could not find any tracks with note data")

        # ------------------------------------------------------------------------
        # TODO: Support for multiple tracks
        # ------------------------------------------------------------------------
        # track = note_tracks[0]
        tracks_note_dict = []
        channel_calc = 0
        for track in note_tracks:
            track_idx = note_tracks.index(track)
            notes = []
            offset = 0
            offset_int = 0
            for event in track:
                if event.type == 'note_on' and event.velocity > 0:
                    # ------------------------------------------------------------------------
                    # Found a note_on event.
                    # ------------------------------------------------------------------------

                    # ------------------------------------------------------------------------
                    # Sanitisation (some midifiles seem to give invalid input).
                    # ------------------------------------------------------------------------
                    if event.velocity > 127:
                        event.velocity = 127


                    offset_int += event.time
                    offset = offset_int / midi_reader.ticks_per_beat
                    note = MidiNote(event.channel, event.note, event.velocity, offset)
                    notes.append(note)
                elif event.type == 'note_off' or (event.type == 'note_on' and event.velocity == 0):
                    # ------------------------------------------------------------------------
                    # Found a note_off event.
                    # ------------------------------------------------------------------------
                    offset_int += event.time
                    offset = offset_int / midi_reader.ticks_per_beat
                    for note in reversed(notes):
                        if not isinstance(note,  MidiNote):
                            continue
                        if note.pitch == event.note and note.duration is None:
                            note.duration = offset - note.location
                            break
                elif event.type == 'program_change':
                    offset_int += event.time
                    offset = offset_int / midi_reader.ticks_per_beat
                    pgm_chg = MidiMessageProgram(channel=event.channel, program=event.program, location=offset,
                                                 track_idx=track_idx)
                    notes.append(pgm_chg)
                elif event.type == 'control_change':
                    offset_int += event.time
                    offset = offset_int / midi_reader.ticks_per_beat
                    ctrl_chg = MidiMessageControl(channel=event.channel, cc=event.control, value=event.value,
                                                  location=offset, time=event.time, track_idx=track_idx)
                    notes.append(ctrl_chg)
                elif event.type == 'polytouch':
                    offset_int += event.time
                    offset = offset_int / midi_reader.ticks_per_beat
                    poly_touch = MidiMessagePoly(channel=event.channel, pitch=event.pitch, value=event.value,
                                                 location=offset, time=event.time, track_idx=track_idx)
                    notes.append(poly_touch)
                elif event.type == 'aftertouch':
                    offset_int += event.time
                    offset = offset_int / midi_reader.ticks_per_beat
                    after_touch = MidiMessageAfter(channel=event.channel, value=event.value, location=offset,
                                                   time=event.time, track_idx=track_idx)
                    notes.append(after_touch)
                elif event.type == 'pitchwheel':
                    offset_int += event.time
                    offset = offset_int / midi_reader.ticks_per_beat
                    pitch_wheel = MidiMessagePitch(channel=event.channel, pitch=event.pitch, location=offset,
                                                   time=event.time, track_idx=track_idx)
                    notes.append(pitch_wheel)
                #  meta messages
                elif event.type == 'end_of_track':
                    offset_int += event.time
                    offset = offset_int / midi_reader.ticks_per_beat
                    end_of_track = MidiMetaMessageEndTrack(location=offset,
                                                           time=event.time, track_idx=track_idx)
                    notes.append(end_of_track)
                elif event.type == 'midi_port':
                    offset_int += event.time
                    offset = offset_int / midi_reader.ticks_per_beat
                    midi_port = MidiMetaMessageMidiPort(port=event.port, location=offset,
                                                        time=event.time, track_idx=track_idx)
                    notes.append(midi_port)
                elif event.type == 'key_signature':
                    offset_int += event.time
                    offset = offset_int / midi_reader.ticks_per_beat
                    key_sig = MidiMetaMessageKey(key=event.key, location=offset,
                                                 time=event.time, track_idx=track_idx)
                    notes.append(key_sig)
                elif event.type == 'time_signature':
                    offset_int += event.time
                    offset = offset_int / midi_reader.ticks_per_beat
                    time_sig = MidiMetaMessageTimeSig(numerator=event.numerator, denominator=event.denominator,
                                                      clocks_per_click=event.clocks_per_click,
                                                      notated_32nd_notes_per_beat=event.notated_32nd_notes_per_beat,
                                                      location=offset, time=event.time, track_idx=track_idx)
                    notes.append(time_sig)
                elif event.type == 'track_name':
                    offset_int += event.time
                    offset = offset_int / midi_reader.ticks_per_beat
                    track_name = MidiMetaMessageTrackName(name=event.name, location=offset, time=event.time,
                                                          track_idx=track_idx)
                    notes.append(track_name)
                elif event.type == 'set_tempo':
                    offset_int += event.time
                    offset = offset_int / midi_reader.ticks_per_beat
                    tempo = MidiMetaMessageTempo(tempo=event.tempo, location=offset, time=event.time,
                                                 track_idx=track_idx)
                    notes.append(tempo)

            # ------------------------------------------------------------------------
            # Quantize
            # ------------------------------------------------------------------------
            for note in notes:
                if quantize:
                    note.location = round(note.location / quantize) * quantize
                    if hasattr(note, 'duration'):
                        note.duration = round(note.duration / quantize) * quantize

            # ------------------------------------------------------------------------
            # Construct a sequence which honours chords and relative lengths.
            # First, group all notes by their starting time.
            # ------------------------------------------------------------------------
            notes_by_time = {}
            action_by_time = {}
            non_meta_by_time = {}
            for note in notes:
                if isinstance(note,  MidiNote):
                    if not note.duration:
                        note.duration = 1  #  default lenght for hanging notes
                    log.debug(" - MIDI event (t = %.2f): Note %d, velocity %d, duration %.3f" %
                              (note.location, note.pitch, note.velocity, note.duration))
                location = note.location
                if isinstance(note, MidiNote):
                    if location in notes_by_time:
                        notes_by_time[location].append(note)
                    else:
                        notes_by_time[location] = [note]
                elif getattr(note, 'is_meta', False):
                    if location in action_by_time:
                        action_by_time[location].append(note)
                    else:
                        action_by_time[location] = [note]
                else:
                    if location in non_meta_by_time:
                        non_meta_by_time[location].append(note)
                    else:
                        non_meta_by_time[location] = [note]

            note_dict = {
                # EVENT_ACTION: [],
                # EVENT_TIME: [],
                EVENT_NOTE: [],
                EVENT_AMPLITUDE: [],
                EVENT_GATE: [],
                EVENT_DURATION: [],
                EVENT_CHANNEL: []
            }
            action_dict = {
                EVENT_ACTION: [],
                EVENT_TIME: [],
                EVENT_DURATION: []
            }

            non_meta_dict = {
                EVENT_ACTION: [],
                EVENT_TIME: [],
                EVENT_DURATION: []
            }
            # ------------------------------------------------------------------------
            # Next, iterate through groups of notes chronologically, figuring out
            # appropriate parameters for duration (eg, inter-note distance) and
            # gate (eg, proportion of distance note extends across).
            # ------------------------------------------------------------------------
            non_meta_times = sorted(non_meta_by_time.keys())
            for i, t in enumerate(non_meta_times):
                t = non_meta_times[i]
                notes = non_meta_by_time[t]
                if i < len(non_meta_times) - 1:
                    next_time = non_meta_times[i + 1]
                else:
                    next_time = t + max([note.duration for note in notes if hasattr(note, 'duration')] or [1.0])

                time_until_next_note = next_time - t
                # action_dict[EVENT_DURATION].append(time_until_next_note)
                if len(notes) > 1:
                    # note_dict[EVENT_ACTION].append(tuple(lambda: print(type(note)) for note in notes if not hasattr(note, 'duration')))
                    messages = tuple(note for note in notes)
                    create_lam_function(non_meta_dict, messages, track_idx)
                else:
                    # if time_until_next_note:
                    note = notes[0]
                    create_lam_function(non_meta_dict, note, track_idx)

            action_times = sorted(action_by_time.keys())
            for i, t in enumerate(action_times):
                t = action_times[i]
                notes = action_by_time[t]
                if i < len(action_times) - 1:
                    next_time = action_times[i + 1]
                else:
                    next_time = t + max([note.duration for note in notes if hasattr(note, 'duration')] or [1.0])

                time_until_next_note = next_time - t
                # action_dict[EVENT_DURATION].append(time_until_next_note)
                if len(notes) > 1:
                    # note_dict[EVENT_ACTION].append(tuple(lambda: print(type(note)) for note in notes if not hasattr(note, 'duration')))
                    messages = tuple(note for note in notes)
                    create_lam_function(action_dict, messages, track_idx)
                else:
                    # if time_until_next_note:
                    note = notes[0]
                    create_lam_function(action_dict, note, track_idx)

            times = sorted(notes_by_time.keys())
            for i, t in enumerate(times):
                t = times[i]
                notes = notes_by_time[t]

                # ------------------------------------------------------------------------
                # Our duration is always determined by the time of the next note event.
                # If a next note does not exist, this is the last note of the sequence;
                # use the maximal length of note currently playing (assuming a chord)
                # ------------------------------------------------------------------------
                # if i < len(times) - 1:
                #     next_time = times[i + 1]
                # else:
                #     next_time = t + max([note.duration for note in notes if hasattr(note, 'duration')] or [1.0])
                #
                # time_until_next_note = next_time - t
                # note_dict[EVENT_DURATION].append(time_until_next_note)
                # TODO need to differentiate depending on type of message (note, other or meta)

                if len(notes) > 1:
                    # note_dict[EVENT_ACTION].append(tuple(lambda: print(type(note)) for note in notes if not hasattr(note, 'duration')))
                    messages = tuple(note for note in notes if not isinstance(note, MidiNote))
                    # create_lam_function(messages)
                    note_tuple = tuple(
                        note.pitch for note in notes if isinstance(note, MidiNote))
                    if len(note_tuple):
                        if i < len(times) - 1:
                            next_time = times[i + 1]
                        else:
                            next_time = t + max([note.duration for note in notes if hasattr(note, 'duration')] or [1.0])

                        time_until_next_note = next_time - t
                        note_dict[EVENT_DURATION].append(time_until_next_note)
                        note_dict[EVENT_NOTE].append(note_tuple)
                        note_dict[EVENT_AMPLITUDE].append(
                            tuple(note.velocity for note in notes if isinstance(note, MidiNote)))
                        note_dict[EVENT_GATE].append(
                            tuple(note.duration / time_until_next_note for note in notes if isinstance(note, MidiNote)))
                        note_dict[EVENT_CHANNEL].append(tuple(
                            int(note.channel / time_until_next_note) for note in notes if isinstance(note, MidiNote)))
                else:
                    if time_until_next_note:
                        note = notes[0]
                        if isinstance(note, MidiNote):
                            if i < len(times) - 1:
                                next_time = times[i + 1]
                            else:
                                next_time = t + max(
                                    [note.duration for note in notes if
                                     hasattr(note, 'duration') and isinstance(note, MidiNote)] or [1.0])

                            time_until_next_note = next_time - t
                            note_dict[EVENT_DURATION].append(time_until_next_note)
                            note_dict[EVENT_NOTE].append(note.pitch)
                            note_dict[EVENT_AMPLITUDE].append(note.velocity)
                            note_dict[EVENT_GATE].append(note.duration / time_until_next_note)
                            note_dict[EVENT_CHANNEL].append(int(note.channel / time_until_next_note))
                        else:
                            # note_dict[EVENT_ACTION].append( lambda note=note: print(note.__dict__))
                            # note_dict[EVENT_ACTION].append(lambda timeline, note=note: self.print_obj(timeline, note))
                            # note_dict[EVENT_ACTION].append((self.print_obj, note))
                            # note_dict[EVENT_ACTION].append(partial(lambda timeline: self.print_obj(timeline), note))
                            # create_lam_function(note)
                            pass

            for key, value in note_dict.items():
                note_dict[key] = PSequence(value, repeats=1)

            #  recalculate EVENT_TIME -> EVENT_DURATION
            time_list = action_dict.pop(EVENT_TIME, None)
            if time_list:
                action_dict[EVENT_DURATION] = [dur - time_list[i] for (i, dur) in enumerate(time_list[1:])] + [1.0]

            for key, value in action_dict.copy().items():
                if len(value) != 0:
                    action_dict[key] = PSequence(value, repeats=1)
                else:
                    action_dict.pop(key, None)

            #  recalculate EVENT_TIME -> EVENT_DURATION
            time_list = non_meta_dict.pop(EVENT_TIME, None)
            if time_list:
                non_meta_dict[EVENT_DURATION] = [dur - time_list[i] for (i, dur) in enumerate(time_list[1:])] + [1.0]

            for key, value in non_meta_dict.copy().items():
                if len(value) != 0:
                    non_meta_dict[key] = PSequence(value, repeats=1)
                else:
                    non_meta_dict.pop(key, None)


                # channel_calc += 1

            if bool(non_meta_dict):
                non_meta_dict[iso.EVENT_ACTION_ARGS] = {"track_idx": track_idx}
                tracks_note_dict.append(non_meta_dict)

            if bool(action_dict):
                # action_dict[iso.EVENT_CHANNEL] = channel_calc
                action_dict[iso.EVENT_ACTION_ARGS] = {"track_idx": track_idx}
                tracks_note_dict.append(action_dict)

            if bool(note_dict):
                note_dict[iso.EVENT_ACTION_ARGS] = {"track_idx": track_idx}
                tracks_note_dict.append(note_dict)

        return sorted(tracks_note_dict, key=lambda t: 0 if t.get('action', None) else 1)
        # return tracks_note_dict
