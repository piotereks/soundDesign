import mido

names = mido.get_output_names()
print(names)
NO_MIDI_OUT = mido.get_output_names() == []
print(f"{NO_MIDI_OUT}")

names = mido.get_input_names()
print(names)
