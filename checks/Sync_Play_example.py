import time
import isobar as iso

# one time init  (this is the best to used globals)
# One time is sufficient, so basically this may be repeated


import isobar as iso

global midi_out
global timeline
global tline1
global tline2

name = "Microsoft GS Wavetable Synth 0"
name = "Bome Virtual MIDI Port 2"
# name = "Virtual Midi"

# name= "loopMIDI 6"

print('mo in gl:', 'midi_out' in globals())
if 'midi_out' not in locals():
    print('no midiout')
    midi_out = iso.MidiOutputDevice(device_name=name, send_clock=True)

else:
    print('yes: midi out')

if 'timeline' not in locals():
    print('creating timeline')
    timeline = iso.Timeline(120, output_device=midi_out)
    timeline.background()  # use background instead of run to enable live performing (async notes passing)
else:
    print('reusing timeline')


# filename = "output.mid"
# output = iso.MidiFileOutputDevice(filename)
# # iso.MAX_CLOCK_RATE
# timeline = iso.Timeline(120, output_device=output)
# # timeline = iso.Timeline(iso.MAX_CLOCK_RATE, output_device=output)
# timeline.stop_when_done = True
print(f"xtime: {round(timeline.current_time)}")
global beat_count
beat_count = 0
prev_time = 0


def beat1():
    global beat_count
    global prev_time
    beat_count += 1

    diff_time = timeline.current_time - prev_time
    prev_time = timeline.current_time
    print(f"diff:{diff_time}, timeYY: {timeline.current_time}, {round(timeline.current_time)} beat: {beat_count}\n")
    beat_count %= 4

    notes = iso.PSequence([1, 3, 2, 4], repeats=1)

    xxx = timeline.schedule(
        {"note": notes.copy() + 72
         }
        ,
        replace=True  # this is not working with version 0.1.1, only with github
        , name="blah"  # this is not working with version 0.1.1, only with github

    )


def beat2():
    global beat_count
    global prev_time
    beat_count += 1

    diff_time = timeline.current_time - prev_time
    prev_time = timeline.current_time
    print(f"diff:{diff_time}, timeXX: {timeline.current_time}, {round(timeline.current_time)} beat: {beat_count}\n")
    beat_count %= 4

    notes = iso.PSequence([1, 3, 2, 4], repeats=1)

    xxx = timeline.schedule(
        {"note": notes.copy() + 66
         }
        , replace=True  # this is not working with version 0.1.1, only with github
        , name="blah"  # this is not working with version 0.1.1, only with github
    )


def beatNone():
    global beat_count
    global prev_time
    beat_count += 1

    diff_time = timeline.current_time - prev_time
    prev_time = timeline.current_time
    print(f"diff:{diff_time}, timeXX: {timeline.current_time}, {round(timeline.current_time)} beat: {beat_count}\n")
    beat_count %= 4

    notes = iso.PSequence([1, 3, 2, 4], repeats=1)

    xxx = timeline.schedule()


# intialize with beat1
# beat=beat1
beat = beatNone

# Run main function beat with duration 4. This one is looping forever.
timeline.background()
timeline.schedule({
    "action": lambda: beat(),
    "duration": 4
})


