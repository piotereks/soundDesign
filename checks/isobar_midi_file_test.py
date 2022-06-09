import isobar as iso
pattern = iso.MidiFileInputDevice('..\\jupyter\\rythm_midi_files\\Dim6_1.mid').read()
# pattern = iso.MidiFileInputDevice('..\\jupyter\\rythm_midi_files\\Dim3.mid').read()
print(pattern)
print(f'{list(pattern["note"])=}')
print(f'in ticks {list(pattern["duration"])=}')
# print(list(pattern['note']))