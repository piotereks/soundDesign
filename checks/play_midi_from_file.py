import mido
import time

def direct_midi_play():
    #defaults
    # tempo = 500000
    ticks_per_beat=480
    names=mido.get_output_names()
    print(names)

    # port = mido.open_output('Microsoft GS Wavetable Synth 0')
    port = mido.open_output('Bome Virtual MIDI Port 2')

    # port.close()

    print(port)
    # mid=mido.MidiFile('Def 5 4.mid',clip=True)
    # mid=mido.MidiFile('..\\jupyter\\rythm_midi_files\\Def (5.mid',clip=True)
    mid=mido.MidiFile('..\\jupyter\\rythm_midi_files\\Def (5.mid')
    track=mid.tracks[0]
    ticks_per_beat= mid.ticks_per_beat or 480
    tempo=[msg.tempo for msg in track if msg.is_meta and msg.type=='set_tempo'][0] or 500000
    tick_time=tempo/(1000000*ticks_per_beat)   # this is not needed in mido midi file since time is already calculated with this principle
    print(f"{ticks_per_beat=},{tempo=},{tick_time=}")
    # print([msg.type for msg in track if msg.is_meta ])
    # print(track)

    # print(mid)
    # mid=mido.MidiFile('..\\jupyter\\rythm_midi_files\\Dim6_2.mid',clip=True)
    # mid=mido.MidiFile('..\\jupyter\\rythm_midi_files\\Blah.mid',clip=True)
    # mid=mido.MidiFile('..\\jupyter\\rythm_midi_files\\Blah2.mid',clip=True)
    for msg in mid:
        if msg.is_meta:
            print(msg)
        # print(msg.__dict__)
        # print(f'{msg.is_cc()=};{msg.is_meta=};{msg.is_realtime=}')
        print(msg)
        print(f'{msg.time=}')
        time.sleep(msg.time)
        if not msg.is_meta:
            port.send(msg)

    port.close()

direct_midi_play()