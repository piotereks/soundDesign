import mido
import isobar as iso
import time


def print_message(message):
    """
    The callback argument is a mido Message object:
    https://mido.readthedocs.io/en/latest/messages.html
    """
    print(" - Received MIDI: %s" % message)


def print_tempo():
    if midi_in.tempo:
        print("Estimated tempo: %.3f" % midi_in.tempo)


def crt_input():
    names = mido.get_input_names()
    print(names)
    input_midi_name = 'Bome Virtual MIDI Port 1'
    # input_midi_name='loopMIDI 5'

    try:
        midi_in = iso.MidiInputDevice(device_name=input_midi_name)
        print(f'open in {input_midi_name} opened')

    except:
        print(f'open in {input_midi_name} failed')

    timeline_in = iso.Timeline(clock_source=midi_in)
    # timeline_in.schedule({
    #     "action": print_tempo
    # })
    # timeline_in.background()

    timeline_in.background()
    timeline_in.schedule({
        "action": lambda: blah(),
        "duration": 4,
        "quantize": 1
    })

    print('Input Done')
    return midi_in


def blah():
    print('blah')


def crt_output():
    names = mido.get_output_names()
    print(names)
    output_midi_name = 'Bome Virtual MIDI Port 2'
    # output_midi_name='loopMIDI 6'

    try:
        output_device = iso.MidiOutputDevice(device_name=output_midi_name, send_clock=True)
        # output_device = iso.MidiOutputDevice(device_name=output_midi_name)
        print(f'open out {output_midi_name} opened')


    except:
        print(f'open out {output_midi_name} failed')
        exit

    timeline_out = iso.Timeline(120, output_device=output_device)
    timeline_out.background()
    print('output Done')


midi_in = crt_input()
# crt_output()

# midi_in = iso.MidiInputDevice()
# midi_in.callback = print_message
# midi_in.callback = print_tempo

print("Opened MIDI input: %s" % midi_in.device_name)

print('Processing Done')