import mido
import time

def direct_midi_play():
    #defaults
    # tempo = 500000
    ticks_per_beat=480
    names=mido.get_output_names()
    print(names)

    # port = mido.open_output('Microsoft GS Wavetable Synth 0')
    # port = mido.open_output('Bome Virtual MIDI Port 2')
    port = mido.open_output('Arturia MiniLab mkII 1')

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
    # "F0 00 20 6B 7F 42 02 00 10 7n cc F7"
    # n is the
    # pad
    # number, 0
    # to
    # F, corresponding
    # to
    # Pad1
    # to
    # Pad16
    # cc is the
    # color:
    # 00 - black
    # 01 - red
    # 04 - green
    # 05 - yellow
    # 10 - blue
    # 11 - magenta
    # 14 - cyan
    # 7
    # F - white
    print("blah")
    # xx=tuple([int(x, 16) for x in "F0 00 20 6B 7F 42 02 00 10 74 04 F7".split()])
    # print(xx, "blah3")
    # msg = Message('sysex', data=bytearray(b'ABC'))
    # xxx=bytearray(b'F000206B7F420200107404F7')
    xxx=bytearray(b'F000206B7F420200107404F7')
    xxx=bytearray(b'F000206B7F420200107404F7')
    xxxy=bytearray(b'F000206B7F420200107402F7')
    xxxy=bytearray(b'00206B7F420200107000')
    xxxy=bytearray(b'00206B7F420200107105')
    xxxy=bytearray(b'00206B7F4202007171')

    '''
    
basically it query values becomes:

 F0 00 20 6B 7F 42 01 00 pp cc F7
 F0 00 20 6B 7F 42 02 00 10 7n cc F7
where
   pp is the parameter number or slot number - because each control has a bunch of settings stored in slots
   cc is the control number (for the pads that is 0x70 to 0x7F)
    '''
    # xx=tuple([int(x, 16) if int(x, 16)<128 else int(x, 16)-256 for x in "F0 00 20 6B 7F 42 02 00 10 74 04 F7".split()])
    print(xxxy, "blah2")
    yy=mido.Message('sysex', data = xxxy, time=0)
    print(yy)
    print("sdfsf:", yy.hex())
    port.send(yy)
    print(yy, "sent")
    # print([msg.type for msg in track if msg.is_meta ])
    # print(track)

    # print(mid)
    # mid=mido.MidiFile('..\\jupyter\\rythm_midi_files\\Dim6_2.mid',clip=True)
    # mid=mido.MidiFile('..\\jupyter\\rythm_midi_files\\Blah.mid',clip=True)
    # mid=mido.MidiFile('..\\jupyter\\rythm_midi_files\\Blah2.mid',clip=True)
    return
    for msg in mid:
        if msg.is_meta:
            print(msg)
        # print(msg.__dict__)
        # print(f'{msg.is_cc()=};{msg.is_meta=};{msg.is_realtime=}')
        print(msg, msg.is_meta)
        print(f'{msg.time=}')
        time.sleep(msg.time)
        print('x')
        if not msg.is_meta:
            print('y')
            port.send(msg)
        print('z')

    port.close()

direct_midi_play()