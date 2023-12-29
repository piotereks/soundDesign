import inspect
import logging
import re
import time

import isobar as iso
import mido
import snoop

log = logging.getLogger(__name__)


class MidiFileManyTracksOutputDevice(iso.MidiFileOutputDevice):

    def __init__(self, filename):
        self.filename = filename
        # self.midifile = None
        self.midifile = mido.MidiFile()
        # self.miditrack = []
        self.miditrack = [mido.MidiTrack()]
        self.midifile.tracks.append(self.miditrack[0])
        self.channel_track = [None]
        # self.channel_track.append(0)
        self.tgt_track_idxs = [None]
        self.time = [0]
        self.last_event_time = [0]

    @snoop(watch=('self.tgt_track_idxs', 'self.channel_track'))
    def get_channel_track(self, channel=None, src_track_idx=None):
        def add_track(chn, tix):
            track = mido.MidiTrack()
            self.miditrack.append(track)
            self.midifile.tracks.append(track)
            self.channel_track.append(chn)
            self.tgt_track_idxs.append(tix)

            self.time.append(0)
            self.last_event_time.append(0)
            snoop.pp(self.channel_track, self.tgt_track_idxs)
            return len(self.tgt_track_idxs) - 1

        snoop.pp(inspect.currentframe().f_back.f_back)
        if src_track_idx is not None and channel is not None:
            if self.tgt_track_idxs == [None] and self.channel_track == [None]:
                self.tgt_track_idxs = [src_track_idx]
                self.channel_track = [channel]
                snoop.pp(self.channel_track, self.tgt_track_idxs)
                return 0
            if (channel, src_track_idx) in zip(self.channel_track, self.tgt_track_idxs):
                snoop.pp(self.channel_track, self.tgt_track_idxs)
                return list(zip(self.channel_track, self.tgt_track_idxs)).index((channel, src_track_idx))
            if (channel, None) in zip(self.channel_track, self.tgt_track_idxs):
                idx = list(zip(self.channel_track, self.tgt_track_idxs)).index((channel, None))
                self.tgt_track_idxs[idx] = src_track_idx
                snoop.pp(self.channel_track, self.tgt_track_idxs)
                return idx
            if (None, src_track_idx) in zip(self.channel_track, self.tgt_track_idxs):
                idx = list(zip(self.channel_track, self.tgt_track_idxs)).index((None, src_track_idx))
                self.channel_track[idx] = channel
                snoop.pp(self.channel_track, self.tgt_track_idxs)
                return idx

            return add_track(chn=channel, tix=src_track_idx)

        if src_track_idx is not None:
            if self.tgt_track_idxs == [None] and self.channel_track == [None]:
                self.tgt_track_idxs = [src_track_idx]
                snoop.pp(self.channel_track, self.tgt_track_idxs)
                return 0

            if src_track_idx in self.tgt_track_idxs:
                idx = self.tgt_track_idxs.index(src_track_idx)
                snoop.pp(self.channel_track, self.tgt_track_idxs)
                return idx

            return add_track(chn=None, tix=src_track_idx)

        if channel is not None:
            if self.tgt_track_idxs == [None] and self.channel_track == [None]:
                self.channel_track = [channel]
                snoop.pp(self.channel_track, self.tgt_track_idxs)
                return 0

            if channel in self.channel_track:
                idx = self.channel_track.index(channel)
                snoop.pp(self.channel_track, self.tgt_track_idxs)
                return idx

            return add_track(chn=channel, tix=None)
        snoop.pp(self.channel_track, self.tgt_track_idxs)
        return 1

    @snoop
    def note_on(self, note=60, velocity=64, channel=0, track_idx=0):
        # ------------------------------------------------------------------------
        # avoid rounding errors
        # ------------------------------------------------------------------------
        snoop.pp(inspect.currentframe().f_back.f_code.co_name)
        track = self.get_channel_track(channel=channel, src_track_idx=track_idx)
        if track >= 0:
            dt = self.time[track] - self.last_event_time[track]
            dt_ticks = int(round(dt * self.midifile.ticks_per_beat))
            self.miditrack[track].append(
                mido.Message('note_on', note=note, velocity=velocity, channel=channel, time=dt_ticks))
            self.last_event_time[track] = self.time[track]

    def note_off(self, note=60, channel=0, track_idx=0):
        snoop.pp(inspect.currentframe().f_back.f_code.co_name)
        track = self.get_channel_track(channel=channel, src_track_idx=track_idx)
        if track >= 0:
            dt = self.time[track] - self.last_event_time[track]
            dt_ticks = int(round(dt * self.midifile.ticks_per_beat))
            self.miditrack[track].append(mido.Message('note_off', note=note, channel=channel, time=dt_ticks))
            self.last_event_time[track] = self.time[track]

    def tick(self):
        self.time = list(map(lambda x: x + (1.0 / self.ticks_per_beat), self.time))

    def _msg_deduplication(self):
        new_mid = mido.MidiFile()

        for i, track in enumerate(self.midifile.tracks):
            latest_meta_messages = {}
            new_track = mido.MidiTrack()
            track.reverse()
            for msg in track:
                if msg.time != 0:
                    latest_meta_messages = {}
                if msg.is_meta or (msg.type not in ('note_on', 'note_off')):
                    key = None
                    if msg.type == 'text':
                        key = re.search(r'^.*?:', msg.text)[0]
                    elif hasattr(msg, 'channel'):
                        if msg.type == 'polytouch':
                            key = (msg.type, msg.channel, msg.note)
                        elif msg.type == 'control_change':
                            key = (msg.type, msg.channel, msg.control)
                        else:
                            key = (msg.type, msg.channel)
                    else:
                        key = msg.type

                    if key not in latest_meta_messages:
                        if msg.time == 0:
                            latest_meta_messages[key] = msg
                        new_track.append(msg)

                else:
                    new_track.append(msg)
            new_track.reverse()
            new_mid.tracks.append(new_track)

        self.midifile.tracks = new_mid.tracks

    def write(self, dedup=True):
        # ------------------------------------------------------------------------
        # When closing the MIDI file, append a dummy `note_off` event to ensure
        # any rests at the end of the file remain intact
        # (cf. https://forum.noteworthycomposer.com/?topic=4708.0)
        # ------------------------------------------------------------------------
        for idx, track in enumerate(self.midifile.tracks):
            dt = self.time[idx] - self.last_event_time[idx]
            dt_ticks = int(round(dt * self.midifile.ticks_per_beat))
            track.append(mido.Message('note_off', note=0, channel=0, time=dt_ticks))
        if dedup:
            self._msg_deduplication()
        self.midifile.save(self.filename)

    def control(self, control=0, value=0, channel=0, track_idx=0):
        snoop.pp(inspect.currentframe().f_back.f_code.co_name)
        track = self.get_channel_track(channel=channel, src_track_idx=track_idx)
        if track >= 0:
            dt = self.time[track] - self.last_event_time[track]
            dt_ticks = int(round(dt * self.midifile.ticks_per_beat))
            self.miditrack[track].append(
                mido.Message('control_change', control=int(control), value=int(value), channel=int(channel)))
            self.last_event_time[track] = self.time[track]

    def pitch_bend(self, pitch=0, channel=0, track_idx=0):
        snoop.pp(inspect.currentframe().f_back.f_code.co_name)
        track = self.get_channel_track(channel=channel, src_track_idx=track_idx)
        if track >= 0:
            dt = self.time[track] - self.last_event_time[track]
            dt_ticks = int(round(dt * self.midifile.ticks_per_beat))
            self.miditrack[track].append(
                mido.Message('pitchwheel', pitch=int(pitch), channel=int(channel)))
            self.last_event_time[track] = self.time[track]

    @snoop
    def program_change(self, program=0, channel=0, track_idx=0):
        snoop.pp(inspect.currentframe().f_back.f_back)
        log.debug("[midi] Program change (channel %d, program_change %d)" % (channel, program))
        track = self.get_channel_track(channel=channel, src_track_idx=track_idx)
        if track >= 0:
            dt = self.time[track] - self.last_event_time[track]
            dt_ticks = int(round(dt * self.midifile.ticks_per_beat))
            self.miditrack[track].append(
                mido.Message('program_change', program=int(program), channel=int(channel)))
            self.last_event_time[track] = self.time[track]

    def aftertouch(self, value=0, channel=0, track_idx=0):
        snoop.pp(inspect.currentframe().f_back.f_code.co_name)
        track = self.get_channel_track(channel=channel, src_track_idx=track_idx)
        if track >= 0:
            dt = self.time[track] - self.last_event_time[track]
            dt_ticks = int(round(dt * self.midifile.ticks_per_beat))
            self.miditrack[track].append(
                msg=mido.Message('aftertouch', value=value, channel=int(channel)))
            self.last_event_time[track] = self.time[track]

    def polytouch(self, value=0, note=0, channel=0, track_idx=0):
        snoop.pp(inspect.currentframe().f_back.f_code.co_name)
        track = self.get_channel_track(channel=channel, src_track_idx=track_idx)
        # track = track_idx  #  tmp change
        if track >= 0:
            dt = self.time[track] - self.last_event_time[track]
            dt_ticks = int(round(dt * self.midifile.ticks_per_beat))
            self.miditrack[track].append(
                msg=mido.Message('polytouch', value=int(value), note=note, channel=int(channel)))
            self.last_event_time[track] = self.time[track]


class FileOut(MidiFileManyTracksOutputDevice, iso.MidiOutputDevice):

    def __init__(self, filename, device_name, send_clock, virtual=False):
        MidiFileManyTracksOutputDevice.__init__(self, filename=filename)
        iso.MidiOutputDevice.__init__(self, device_name=device_name, send_clock=send_clock, virtual=virtual)

    def note_off(self, note, channel, track_idx=0):
        MidiFileManyTracksOutputDevice.note_off(self, note=note, channel=channel, track_idx=track_idx)
        iso.MidiOutputDevice.note_off(self, note=note, channel=channel)

    def note_on(self, note, velocity, channel, track_idx=0):
        MidiFileManyTracksOutputDevice.note_on(self, note=note, velocity=velocity, channel=channel, track_idx=track_idx)
        iso.MidiOutputDevice.note_on(self, note=note, velocity=velocity, channel=channel)

    def program_change(self, program=0, channel=0, track_idx=0):
        MidiFileManyTracksOutputDevice.program_change(self, program=program, channel=channel, track_idx=track_idx)
        iso.MidiOutputDevice.program_change(self, program=program, channel=channel)

    def control(self, control=0, value=0, channel=0, track_idx=0):
        MidiFileManyTracksOutputDevice.control(self, control=control, value=value, channel=channel, track_idx=track_idx)
        iso.MidiOutputDevice.control(self, control=control, value=value, channel=channel)

    def pitch_bend(self, pitch=0, channel=0, track_idx=0):
        MidiFileManyTracksOutputDevice.pitch_bend(self, pitch=pitch, channel=channel, track_idx=track_idx)
        iso.MidiOutputDevice.pitch_bend(self, pitch=pitch, channel=channel)

    def aftertouch(self, control=0, value=0, channel=0, track_idx=0):
        MidiFileManyTracksOutputDevice.aftertouch(self, value=value, channel=channel,
                                                  track_idx=track_idx)

    def polytouch(self, value=0, note=0, channel=0, track_idx=0):
        MidiFileManyTracksOutputDevice.polytouch(self, value=value, note=note, channel=channel, track_idx=track_idx)

    def write(self, dedup=True):
        MidiFileManyTracksOutputDevice.write(self, dedup)


class ExtendedMidiInputDevice(iso.MidiInputDevice):
    def _callback(self, message):
        log.debug(f" - MIDI message received: {message}")

        if message.type == 'clock':
            if self.last_clock_time is not None:
                dt = time.time() - self.last_clock_time
                tick_estimate = (120 / 48) * 1.0 / dt
                if self.estimated_tempo is None:
                    self.estimated_tempo = tick_estimate
                else:
                    smoothing = 0.95
                    self.estimated_tempo = (smoothing * self.estimated_tempo) + ((1.0 - smoothing) * tick_estimate)
            self.last_clock_time = time.time()
            if self.clock_target is not None:
                self.clock_target.tick()

        elif message.type == 'start':
            log.info(" - MIDI: Received start message")
            if self.clock_target is not None:
                self.clock_target.start()

        elif message.type == 'stop':
            log.info(" - MIDI: Received stop message")
            if self.clock_target is not None:
                self.clock_target.stop()

        elif message.type == 'songpos':
            log.info(" - MIDI: Received songpos message")
            if message.pos == 0:
                if self.clock_target is not None:
                    self.clock_target.reset()
            else:
                log.warning("MIDI song position message received, but MIDI input cannot seek to arbitrary position")

        elif message.type in ['note_on', 'note_off', 'control_change', 'pitchwheel', 'program_change']:
            if self.callback:
                self.callback(message)
            else:
                self.queue.put(message)
