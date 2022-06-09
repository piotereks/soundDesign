import mido
import isobar as iso
import time
import datetime

filter1=('note_on','note_off','clock','control_change')
filter2=('note_on','note_off','control_change')
filter=filter1
def print_message(message):
    """
    The callback argument is a mido Message object:
    https://mido.readthedocs.io/en/latest/messages.html
    """
    print(" - Received MIDI: %s" % message)
    print(" - Received MIDI: %s" % message.__dict__, message.type)
    print(dir(message))


def print_message_meta(message):
    """
    The callback argument is a mido Message object:
    https://mido.readthedocs.io/en/latest/messages.html
    """
    if message.type not in filter:
        print(datetime.datetime.now()," - Received MIDI: %s" % message)

def print_tempo():
    if midi_in.tempo:
        print(time, "Estimated tempo: %.3f" % midi_in.tempo)
def crt_input():
    names = mido.get_input_names()
    print(names)
    input_midi_name = 'Bome Virtual MIDI Port 1'

    try:
        midi_in = mido.open_input(input_midi_name)
        print(f'open in {input_midi_name} opened')

    except:
        print(f'open in {input_midi_name} failed')
    return midi_in

def crt_inputX():
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
print('asdfsdf')
# crt_output()

# midi_in = iso.MidiInputDevice()
midi_in.callback = print_message_meta
# midi_in.callback = print_tempo

print("Opened MIDI input: %s" % midi_in.__dict__)
# print("Opened MIDI input: %s" % midi_in.device_name)

print('Processing Done')