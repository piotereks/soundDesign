import mido
import isobar as iso
import time

names=mido.get_input_names()
print(names)
input_midi_name='Bome Virtual MIDI Port 1'


# input_midi_name='Bome''s Midi Translator 3 1'

names=mido.get_output_names()
print(names)
output_midi_name='Bome Virtual MIDI Port 2'
input_midi_name='BMO2'

# output_midi_name='Bome Virtual MIDI Port 2'
for inp in mido.get_input_names():
    try:
        midi_in = iso.MidiInputDevice(device_name=inp)
        print(f'open inp {inp} opened')

    except:
        print(f'open inp {inp} failed')

# midi_in = iso.MidiInputDevice(device_name=input_midi_name)
# timeline = iso.Timeline(clock_source=midi_in)
# timeline.run()
print('Input Done')

for out in mido.get_output_names():
    try:
        midi_out = iso.MidiOutputDevice(device_name=out)
        print(f'open out {out} opened')

    except:
        print(f'open out {out} failed')

# output_device = iso.MidiOutputDevice(device_name=output_midi_name,send_clock=True)
# timeline_out = iso.Timeline(120, output_device=output_device)o
# timeline_out.background()
print('output Done')



print('Processing Done')