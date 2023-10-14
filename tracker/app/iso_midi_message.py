import isobar as iso
import mido
from abc import ABC, abstractmethod
import logging

log = logging.getLogger(__name__)

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


class MetaMessageInterface(ABC):

    @abstractmethod
    def to_meta_message(self):
        return None

class MessageInterface(ABC):

    @abstractmethod
    def to_meta_message(self):
        return None

class MidiMessageControl:
    def __init__(self, channel, cc, value, location, time=0, track_idx=0):
        self.channel = channel
        self.cc = cc
        self.value = value
        # location in time, beats
        self.location = location
        self.time = time
        self.track_idx = track_idx
class MidiMessageProgram:
    def __init__(self, channel, program,  location, time=0, track_idx=0):
        self.channel = channel
        self.program = program
        self.location = location
        # duration in time, beats
        self.time = time
        self.track_idx = track_idx

class MidiMessagePitch:
    def __init__(self, channel, pitch, location, time=0, track_idx=0):
        self.channel = channel
        self.pitch = pitch
        self.location = location
        self.time = time
        self.track_idx = track_idx

class MidiMessagePoly:
    def __init__(self, channel, pitch, value, location, time=0, track_idx=0):
        self.channel = channel
        self.pitch = pitch
        self.velocity = value
        self.location = location
        self.time = time
        self.track_idx = track_idx

    def xto_meta_message(self):
        return None
        # return mido.Message(tempo=self.tempo, time=self.time, type='set_tempo')

class CustMidiOutputDevice(iso.MidiOutputDevice):
    def aftertouch(self, control=0, value=0, channel=0, track_idx=0):
        log.debug("[midi] Pitch bend (channel %d, pitch %d)" % (channel, pitch))
        msg = mido.Message('aftertouch', control=int(control), value=value, channel=int(channel))
        self.midi.send(msg)

    def polytouch(self, control=0, note=0, channel=0, track_idx=0):
        log.debug("[midi] Pitch bend (channel %d, pitch %d)" % (channel, pitch))
        msg = mido.Message('polytouch', control=int(control), note=note, channel=int(channel))

iso.MidiOutputDevice.aftertouch=CustMidiOutputDevice.aftertouch
iso.MidiOutputDevice.polytouch=CustMidiOutputDevice.polytouch

class MidiMessageAfter:
    def __init__(self, channel, value, location, time=0):
        self.channel = channel
        self.value = value
        self.location = location
        self.time = time

    def xto_meta_message(self):
        return None
        # return mido.Message(tempo=self.tempo, time=self.time, type='set_tempo')



class MidiMetaMessageTempo(MetaMessageInterface):
    def __init__(self, tempo: int, location, type='set_tempo', time=0, track_idx=0):
        #   0..16777215
        self.tempo = tempo
        self.location = location
        self.is_meta = True
        self.time = time
        self.track_idx = track_idx

    def to_meta_message(self):
        return mido.MetaMessage(tempo=self.tempo, time=self.time, type='set_tempo')


class MidiMetaMessageKey(MetaMessageInterface):
    def __init__(self, key: str, location, time=0, track_idx=0):
        self.key = key
        self.location = location
        self.is_meta = True
        self.time = time

    def to_meta_message(self):
        return mido.MetaMessage(key=self.key, time=self.time, type='key_signature')


class MidiMetaMessageTimeSig(MetaMessageInterface):
    def __init__(self, numerator: int, denominator: int ,
                 clocks_per_click: int, notated_32nd_notes_per_beat: int,
                 location, time=0, track_idx=0):
        self.numerator = numerator
        self.denominator = denominator
        self.clocks_per_click = clocks_per_click
        self.notated_32nd_notes_per_beat = notated_32nd_notes_per_beat
        self.location = location
        self.is_meta = True
        self.time = time

    def to_meta_message(self):
        return mido.MetaMessage(numerator=self.numerator, denominator=self.denominator,
                                clocks_per_click=self.clocks_per_click,
                                notated_32nd_notes_per_beat= self.notated_32nd_notes_per_beat,
                                time=self.time, type='time_signature')


class MidiMetaMessageTrackName(MetaMessageInterface):
    def __init__(self,  name: str, location, time=0, track_idx=0):
        self.name = name
        self.location = location
        self.is_meta = True
        self.time = time

    def to_meta_message(self):
        return mido.MetaMessage(name=self.name, time=self.time, type='track_name')


class MidiMetaMessageMidiPort(MetaMessageInterface):
    def __init__(self, port: int, location, time=0, track_idx=0):
        self.port = port
        self.location = location
        self.is_meta = True
        self.time = time

    def to_meta_message(self):
        return mido.MetaMessage(port=self.port, time=self.time, type='midi_port')


class MidiMetaMessageEndTrack(MetaMessageInterface):
    def __init__(self, location, time=0, track_idx=0):
        self.location = location
        self.is_meta = True
        self.time = time

    def to_meta_message(self):
        return mido.MetaMessage(time=self.time, type='end_of_track')

