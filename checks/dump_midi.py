import mido
from tracker.app.mido_fixes import *

import time
import os

def direct_midi_play():
    #defaults
    # tempo = 500000
    ticks_per_beat=480



    # mid=mido.MidiFile('Def 5 4.mid',clip=True)
    # mid=mido.MidiFile('..\\jupyter\\rythm_midi_files\\Def (5.mid',clip=True)
    this_dir = os.path.dirname(os.path.abspath(__file__))
    # config_file = os.path.join(this_dir, 'note_patterns.json')
    filename = os.path.join(this_dir, "..","saved_midi_files", "xoutput.mid")
    filename = os.path.join(this_dir, '..','tracker', 'tests', 'x1x1b.mid')
    # filename = os.path.join(this_dir, 'example_midi', 'Var_tempo_1_trk_sax_c.mid')
    # filename = os.path.join('example_midi', 'x1x1')
    # filename = os.path.join('example_midi', 'Var_tempo_1_trk_sax.mid')
    mid=mido.MidiFile(filename)
    ticks_per_beat= mid.ticks_per_beat or 480
    # tempo=[msg.tempo for msg in track if msg.is_meta and msg.type=='set_tempo'][0] or 500000
    tempo = 120 # temporary prevent exception
    tick_time=tempo/(1000000*ticks_per_beat)   # this is not needed in mido midi file since time is already calculated with this principle
    print(f"{ticks_per_beat=},{tempo=},{tick_time=}")
    # print([msg.type for msg in track if msg.is_meta ])
    # print(track)

    # print(mid)
    # mid=mido.MidiFile('..\\jupyter\\rythm_midi_files\\Dim6_2.mid',clip=True)
    # mid=mido.MidiFile('..\\jupyter\\rythm_midi_files\\Blah.mid',clip=True)
    # mid=mido.MidiFile('..\\jupyter\\rythm_midi_files\\Blah2.mid',clip=True)
    for track in mid.tracks or []:
        print(f'Track #{mid.tracks.index(track)}')
        for msg in track:
            if msg.is_meta:
                print(msg)
            else:
                pass
                print(msg)
            # print(msg.__dict__)
            # print(f'{msg.is_cc()=};{msg.is_meta=};{msg.is_realtime=}')
            # print(msg)
            # print(f'{msg.time=}')
            # time.sleep(msg.time)
            if not msg.is_meta:
                pass
                # port.send(msg)



direct_midi_play()