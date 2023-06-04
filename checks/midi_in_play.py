
import mido
import logging
from isobar import *
import mido
import time
import os

import logging

log = logging.getLogger(__name__)

global tme
tme = time.time()


class PatchMidiFileInputDevice(MidiFileInputDevice):
    def read(self, quantize=None):
        midi_reader = mido.MidiFile(self.filename)
        log.debug("Loading MIDI data from %s, ticks per beat = %d" % (self.filename, midi_reader.ticks_per_beat))
        note_tracks = list(filter(lambda track: any(message.type == 'note_on' for message in track),
                                  midi_reader.tracks))
        if not note_tracks:
            raise ValueError("Could not find any tracks with note data")

        #------------------------------------------------------------------------
        # TODO: Support for multiple tracks
        #------------------------------------------------------------------------
        track = note_tracks[0]

        notes = []
        offset = 0
        for event in track:
            if event.type == 'note_on' and event.velocity > 0:
                #------------------------------------------------------------------------
                # Found a note_on event.
                #------------------------------------------------------------------------

                #------------------------------------------------------------------------
                # Sanitisation (some midifiles seem to give invalid input).
                #------------------------------------------------------------------------
                if event.velocity > 127:
                    event.velocity = 127

                offset += event.time / midi_reader.ticks_per_beat
                note = MidiNote(event.note, event.velocity, offset)
                notes.append(note)
            elif event.type == 'note_off' or (event.type == 'note_on' and event.velocity == 0):
                #------------------------------------------------------------------------
                # Found a note_off event.
                #------------------------------------------------------------------------
                offset += event.time / midi_reader.ticks_per_beat
                for note in reversed(notes):
                    if note.pitch == event.note and note.duration is None:
                        note.duration = offset - note.location
                        break

        #------------------------------------------------------------------------
        # Quantize
        #------------------------------------------------------------------------
        for note in notes:
            if quantize:
                note.location = round(note.location / quantize) * quantize
                note.duration = round(note.duration / quantize) * quantize

        #------------------------------------------------------------------------
        # Construct a sequence which honours chords and relative lengths.
        # First, group all notes by their starting time.
        #------------------------------------------------------------------------
        notes_by_time = {}
        for note in notes:
            if not note.duration:
                continue
            log.debug(" - MIDI event (t = %.2f): Note %d, velocity %d, duration %.3f" %
                      (note.location, note.pitch, note.velocity, note.duration))
            location = note.location
            if location in notes_by_time:
                notes_by_time[location].append(note)
            else:
                notes_by_time[location] = [note]

        note_dict = {
            EVENT_NOTE: [],
            EVENT_AMPLITUDE: [],
            EVENT_GATE: [],
            EVENT_DURATION: []
        }

        #------------------------------------------------------------------------
        # Next, iterate through groups of notes chronologically, figuring out
        # appropriate parameters for duration (eg, inter-note distance) and
        # gate (eg, proportion of distance note extends across).
        #------------------------------------------------------------------------
        times = sorted(notes_by_time.keys())
        for i, t in enumerate(times):
            t = times[i]
            notes = notes_by_time[t]

            #------------------------------------------------------------------------
            # Our duration is always determined by the time of the next note event.
            # If a next note does not exist, this is the last note of the sequence;
            # use the maximal length of note currently playing (assuming a chord)
            #------------------------------------------------------------------------
            if i < len(times) - 1:
                next_time = times[i + 1]
            else:
                next_time = t + max([note.duration for note in notes])

            time_until_next_note = next_time - t
            note_dict[EVENT_DURATION].append(time_until_next_note)

            if len(notes) > 1:
                note_dict[EVENT_NOTE].append(tuple(note.pitch for note in notes))
                note_dict[EVENT_AMPLITUDE].append(tuple(note.velocity for note in notes))
                note_dict[EVENT_GATE].append(tuple(note.duration / time_until_next_note for note in notes))
            else:
                if time_until_next_note:
                    note = notes[0]
                    note_dict[EVENT_NOTE].append(note.pitch)
                    note_dict[EVENT_AMPLITUDE].append(note.velocity)
                    note_dict[EVENT_GATE].append(note.duration / time_until_next_note)

        for key, value in note_dict.items():
            note_dict[key] = PSequence(value, 1)

        return note_dict

def print_tempo():
    global tme
    # print(time.time()-tme)
    # print(midi_in.__dict__)
    tme = time.time()
    # if midi_in.tempo:
    #     print("Estimated tempo: %.3f" % midi_in.tempo)


MidiFileInputDevice.read = PatchMidiFileInputDevice.read
midi_in_name = 'KB loopMIDI Port 0'
# midi_in = iso.MidiInputDevice(midi_in_name)
# midi_in = iso.MidiFileInputDevice(filename='example_midi\\Variable_tempo_one_note.mid')
# pattern = iso.MidiFileInputDevice(filename='example_midi\\Variable_tempo_one_note.mid').read()
print(os.getcwd())
file = os.path.join('example_midi', 'Variable_tempo_one_note.mid')
# file = os.path.join('example_midi', 'prates.mid')
midi_in = MidiFileInputDevice(filename=file)
pattern = midi_in.read()
print("Read pattern containing %d note events" % len(pattern["note"]))
# iso.Clock
# timeline = iso.Timeline(120, clock_source=midi_in)
# timeline = iso.Timeline(clock_source=midi_in)
# timeline = iso.Timeline()
# timeline.schedule({
#     "action": lambda : print_tempo(),
#     # "action": lambda: beat(),
#     "duration": 4
#
# })


timeline = Timeline(clock_source=midi_in)
timeline.schedule(pattern)
# timeline.run()

# print("Awaiting MIDI clock signal from %s..." % midi_in)

timeline.run()

