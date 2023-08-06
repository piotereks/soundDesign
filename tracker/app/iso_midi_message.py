import isobar as iso


class CustMidiNote(iso.MidiNote):
    def __init__(self, channel, pitch, velocity, location, duration=None):
        self.channel = channel
        # pitch = MIDI 0..127
        self.pitch = pitch
        # velocity = MIDI 0..127
        self.velocity = velocity
        # location in time, beats
        self.location = location
        # duration in time, beats
        self.duration = duration

# iso.io.MidiNote = CustMidiNote
iso.io.MidiNote.__init__ = CustMidiNote.__init__

class MidiMessageControl:
    def __init__(self, channel, cc, value, location):
        self.channel = channel
        self.cc = cc
        self.value = value
        # location in time, beats
        self.location = location

class MidiMessageProgram:
    def __init__(self, channel, program,  location):
        self.channel = channel
        self.program = program
        self.location = location
        # duration in time, beats

class MidiMessagePoly:
    def __init__(self, channel, pitch, value, location):
        self.channel = channel
        self.pitch = pitch
        self.velocity = value
        self.location = location


class MidiMessagePitch:
    def __init__(self, channel, pitch, location):
        self.channel = channel
        self.pitch = pitch
        self.location = location


class MidiMessageAfter:
    def __init__(self, channel, value, location):
        self.channel = channel
        self.value = value
        self.location = location


class MidiMetaMessageTempo:
    def __init__(self, tempo: int, location):
        #   0..16777215
        self.tempo = tempo
        self.location = location
        self.is_meta = True


class MidiMetaMessageKey:
    def __init__(self, key: str, location):
        self.key = key
        self.location = location
        self.is_meta = True


class MidiMetaMessageTimeSig:
    def __init__(self, numerator: int, denominator: int ,
                 clocks_per_click: int, notated_32nd_notes_per_beat: int,
                 location):
        self.numerator = numerator
        self.denominator = denominator
        self.clocks_per_click = clocks_per_click
        self.notated_32nd_notes_per_beat = notated_32nd_notes_per_beat
        self.location = location
        self.is_meta = True


class MidiMetaMessageTrackName:
    def __init__(self, name: str, location):
        self.name = name
        self.location = location
        self.is_meta = True


class MidiMetaMessageMidiPort:
    def __init__(self, port: int, location):
        self.port = port
        self.location = location
        self.is_meta = True


class MidiMetaMessageEndTrack:
    def __init__(self, location):
        self.location = location
        self.is_meta = True

