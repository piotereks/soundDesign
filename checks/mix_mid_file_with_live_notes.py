import mido
import isobar as iso
import os

# Set the MIDI file path (change this to the appropriate value)
# midi_file_path = 'path/to/your/midi/file.mid'
file_path = os.path.abspath(__file__)
    # file = os.path.join('example_midi', 'Variable_tempo_one_note_mod.mid')
midi_file = os.path.join('example_midi', 'Variable_tempo_one_note.mid')

# Set the tempo in beats per minute for the manually provided notes (change this to the appropriate value)
manual_tempo_bpm = 120

# Load the MIDI file using mido.midifiles.MidiFile
midi_file = mido.MidiFile(filename=midi_file)
ticks_per_beat = midi_file.ticks_per_beat
midi_in_loop_name = 'KB loopMIDI Port 0'
midi_out_loop_name = 'KB loopMIDI Port 1'
midi_out_play_name = 'Microsoft GS Wavetable Synth 0'

# play_device = iso.MidiOutputDevice(midi_out_play_name)

# Extract tempo events from the MIDI file
tempo_events = []
for track in midi_file.tracks:
    for message in track:
        if message.type == 'set_tempo':
            tempo_events.append(message)

# Create an isobar scheduler
# timeline = isobar.Scheduler()
timeline = iso.Timeline(120)
# Set the initial tempo for the scheduler
initial_tempo_bpm = mido.tempo2bpm(tempo=tempo_events[0].tempo)
timeline.set_tempo(initial_tempo_bpm)
print("bef midi play")
# Schedule the MIDI events from the file
# timeline.schedule(
#
#     params={iso.EVENT_NOTE: iso.PSequence([60,63,64,65], repeats=1)
#             }, remove_when_done=True)
print("before background")
timeline.background()
print("after background")
for message in midi_file.play():
    print(message)
    print('xxxx')
    if message.type == 'set_tempo':
        tempo_bpm = mido.tempo2bpm(tempo=message.tempo)
        # timeline.set_tempo(tempo_bpm)
        timeline.schedule(
            # delay=message.time/ticks_per_beat,
            params={iso.EVENT_ACTION: lambda: timeline.set_tempo(tempo_bpm)
                    })
    elif message.type in ('note_on', 'note_off'):
        # print(dict(iso.PDict(message)))
        print({
                                iso.EVENT_NOTE: message.note,
                                iso.EVENT_AMPLITUDE: message.velocity if message.type=='note_on' else 0
                            })
        # timeline.schedule(delay=message.time/ticks_per_beat, params=
        timeline.schedule(
            # delay=message.time/ticks_per_beat,
                          params=
                            {
                                iso.EVENT_NOTE: message.note,
                                iso.EVENT_AMPLITUDE: message.velocity #if message.type=='note_on' else 0
                            }, count=1, remove_when_done=True)



# # Manually provide notes and schedule them
# manually_provided_notes = [60, 62, 64, 65]  # Example notes (change this to your desired notes)
# duration = 0.5  # Duration of each note in beats (change this to your desired duration)
#
# for note in manually_provided_notes:
#     timeline.schedule(delay=0, func=lambda note=note: iso.NoteOut(note=note, dur=duration))
#
# # Apply tempo changes from tempo_events
# for tempo_event in tempo_events:
#     tempo_bpm = mido.tempo2bpm(tempo=tempo_event.tempo)
#     timeline.schedule(delay=tempo_event.time, func=lambda tempo_bpm=tempo_bpm: setattr(timeline, 'tempo', tempo_bpm))

# Start the scheduler
# timeline.run()
