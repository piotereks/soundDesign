import mido
import isobar as iso
import logging
import time
import re
import inspect
import snoop


import os
import queue

global MULTI_TRACK
MULTI_TRACK = True
log = logging.getLogger(__name__)
# MULTI_TRACK = False

if MULTI_TRACK:
    class MidiFileManyTracksOutputDevice(iso.MidiFileOutputDevice):

        def __init__(self, filename):
            self.filename = filename
            self.midifile = None
            self.midifile = mido.MidiFile()
            # self.miditrack = []
            self.miditrack = [mido.MidiTrack()]
            self.midifile.tracks.append(self.miditrack[0])
            self.channel_track = [None]
            # self.channel_track.append(0)
            self.tgt_track_idxs = [None]
            # self.tgt_track_idxs.append(0)
            self.time = []
            self.time.append(0)
            self.last_event_time = []
            self.last_event_time.append(0)

        @snoop(watch=('self.tgt_track_idxs', 'self.channel_track'))
        def extra_track(self, channel=None, src_track_idx=None):
            snoop.pp(inspect.currentframe().f_back.f_back)
            # if src_track_idx is not None and channel is not None:
                # if src_track_idx not in self.tgt_track_idxs or channel not in self.channel_track:
                #     track = mido.MidiTrack()
                #     self.miditrack.append(track)
                #     self.midifile.tracks.append(track)
                #     self.channel_track.append(channel)
                #     self.tgt_track_idxs.append(src_track_idx)
                #     self.time.append(0)
                #     self.last_event_time.append(0)
                #     return next((index for index, ch in enumerate(self.channel_track) if ch is channel), None)

            if src_track_idx is not None:
                if src_track_idx not in self.tgt_track_idxs:
                    # if self.miditrack == [None]:
                    #     self.miditrack = []
                    # if self.midifile.tracks == [None]:
                    #     self.midifile.tracks = []
                    # early_return = self.channel_track == [None] or self.tgt_track_idxs == [None]
                    if self.tgt_track_idxs == [None] and self.channel_track == [None]:
                        if self.tgt_track_idxs == [None]:
                            self.tgt_track_idxs = [src_track_idx]
                        if self.channel_track == [None]:
                            self.channel_track = [channel]
                        return 0


                    track = mido.MidiTrack()
                    self.miditrack.append(track)
                    self.midifile.tracks.append(track)
                    self.channel_track.append(channel)
                    self.tgt_track_idxs.append(src_track_idx)

                    self.time.append(0)
                    self.last_event_time.append(0)
                    return next((index for index, tr in enumerate(self.midifile.tracks) if tr is track), None)
                    # return self.midifile.tracks.index(track)
                else:
                    src_track_idx_pos = self.tgt_track_idxs.index(src_track_idx)
                    if self.channel_track[src_track_idx_pos] is None:
                        self.channel_track[src_track_idx_pos] = channel
                        return src_track_idx_pos
                    else:
                        if self.channel_track[src_track_idx_pos] == channel:
                            return src_track_idx_pos

            if channel is not None:
                # if not [x for x in self.channel_track if x == channel]:
                if channel not in self.channel_track:
                    if self.tgt_track_idxs == [None] and self.channel_track == [None]:
                        if self.tgt_track_idxs == [None]:
                            self.tgt_track_idxs = [src_track_idx]
                        if self.channel_track == [None]:
                            self.channel_track = [channel]
                        return 0


                    track = mido.MidiTrack()
                    self.miditrack.append(track)
                    self.midifile.tracks.append(track)
                    self.channel_track.append(channel)
                    self.tgt_track_idxs.append(src_track_idx)
                    self.time.append(0)
                    self.last_event_time.append(0)
                    return next((index for index, ch in enumerate(self.channel_track) if ch is channel), None)
                    # return self.channel_track.index(channel)
                else:
                    channel_pos = self.channel_track.index(channel)
                    if self.tgt_track_idxs[channel_pos] is None:
                        self.tgt_track_idxs[channel_pos] = src_track_idx
                        return channel_pos
                    else:
                        if self.channel_track[channel_pos] == channel:
                            return channel_pos
                    assert False

        @snoop(watch=('self.tgt_track_idxs','self.channel_track'))
        def get_channel_track(self, channel=0, src_track_idx=None):
            snoop.pp(inspect.currentframe().f_back.f_back)
            if src_track_idx is not None:
                try:
                    track_idx = self.tgt_track_idxs.index(src_track_idx)
                    if self.channel_track[track_idx] is None:
                        self.channel_track[track_idx] = channel

                except ValueError:
                    track_idx = self.extra_track(channel=channel, src_track_idx=src_track_idx)
                return track_idx
            try:
                track = self.channel_track.index(channel)
            except ValueError:
                # track = 0
                track = self.extra_track(channel=channel)
            return track

        @snoop
        def note_on(self, note=60, velocity=64, channel=0, track_idx=0):
            # ------------------------------------------------------------------------
            # avoid rounding errors
            # ------------------------------------------------------------------------
            snoop.pp(inspect.currentframe().f_back.f_code.co_name)
            track = self.get_channel_track(channel=channel, src_track_idx=track_idx)
            # track = track_idx  #  tmp change
            print(f"----------------track va: r{channel=} {track=} {track_idx=}")
            if track >= 0:
                # print(f"------------note on: {track=}, {note=}, {channel=}")
                dt = self.time[track] - self.last_event_time[track]
                dt_ticks = int(round(dt * self.midifile.ticks_per_beat))
                self.miditrack[track].append(
                    mido.Message('note_on', note=note, velocity=velocity, channel=channel, time=dt_ticks))
                self.last_event_time[track] = self.time[track]

        def note_off(self, note=60, channel=0, track_idx=0):
            snoop.pp(inspect.currentframe().f_back.f_code.co_name)
            track = self.get_channel_track(channel=channel, src_track_idx=track_idx)
            # track = track_idx  #  tmp change
            if track >= 0:
                print(f"------------note on: {track=}, {note=}, {channel=}")
                dt = self.time[track] - self.last_event_time[track]
                dt_ticks = int(round(dt * self.midifile.ticks_per_beat))
                self.miditrack[track].append(mido.Message('note_off', note=note, channel=channel, time=dt_ticks))
                self.last_event_time[track] = self.time[track]

        def tick(self):
            self.time = list(map(lambda x: x + (1.0 / self.ticks_per_beat), self.time))


        def _msg_deduplication(self):


            # Create a new MIDI file and track
            new_mid = mido.MidiFile()
            # new_mid.tracks.append(new_track)

            # for idx, track in enumerate(self.midifile.tracks):
            #     dt = self.time[idx] - self.last_event_time[idx]
            #     dt_ticks = int(round(dt * self.midifile.ticks_per_beat))
            #     track.append(mido.Message('note_off', note=0, channel=0, time=dt_ticks))

            for i, track in enumerate(self.midifile.tracks):
                latest_meta_messages = {}
                new_track = mido.MidiTrack()
                track.reverse()
                for msg in track:
                    if msg.time != 0:
                        latest_meta_messages = {}
                    # if msg.is_meta and msg.type == 'set_tempo':
                    if msg.is_meta or (msg.type not in ('note_on', 'note_off')):
                        # Check if there is already a meta message of this type at the same time
                        key = None
                        if msg.type == 'text':
                            key = re.search(r'^.*?:', msg.text).group(0)
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
                        # Add non-meta messages directly to the new track

                        new_track.append(msg)
                new_track.reverse()
                new_mid.tracks.append(new_track)

            self.midifile.tracks = new_mid.tracks



        def write(self, dedup = True):
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
                pass
            self.midifile.save(self.filename)

        def control(self, control=0, value=0, channel=0, track_idx=0):
            snoop.pp(inspect.currentframe().f_back.f_code.co_name)
            track = self.get_channel_track(channel=channel, src_track_idx=track_idx)
            # track = track_idx  #  tmp change
            print(f"----------------track var: {channel=} {track=}")
            if track >= 0:
                dt = self.time[track] - self.last_event_time[track]
                dt_ticks = int(round(dt * self.midifile.ticks_per_beat))
                self.miditrack[track].append(
                    mido.Message('control_change', control=int(control), value=int(value), channel=int(channel)))
                self.last_event_time[track] = self.time[track]

        def pitch_bend(self, pitch=0, channel=0, track_idx=0):
            snoop.pp(inspect.currentframe().f_back.f_code.co_name)
            track = self.get_channel_track(channel=channel, src_track_idx=track_idx)
            # track = track_idx  #  tmp change
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
            # track = track_idx  #  tmp change
            if track >= 0:
                dt = self.time[track] - self.last_event_time[track]
                dt_ticks = int(round(dt * self.midifile.ticks_per_beat))
                self.miditrack[track].append(
                    mido.Message('program_change', program=int(program), channel=int(channel)))
                self.last_event_time[track] = self.time[track]


        def aftertouch(self, control=0, value=0, channel=0, track_idx=0):
            snoop.pp(inspect.currentframe().f_back.f_code.co_name)
            track = self.get_channel_track(channel=channel, src_track_idx=track_idx)
            # track = track_idx  #  tmp change
            if track >= 0:
                dt = self.time[track] - self.last_event_time[track]
                dt_ticks = int(round(dt * self.midifile.ticks_per_beat))
                self.miditrack[track].append(
                    msg = mido.Message('aftertouch', control=int(control), value=value, channel=int(channel)))
                self.last_event_time[track] = self.time[track]

        def polytouch(self, control=0, note=0, channel=0, track_idx=0):
            snoop.pp(inspect.currentframe().f_back.f_code.co_name)
            track = self.get_channel_track(channel=channel, src_track_idx=track_idx)
            # track = track_idx  #  tmp change
            if track >= 0:
                dt = self.time[track] - self.last_event_time[track]
                dt_ticks = int(round(dt * self.midifile.ticks_per_beat))
                self.miditrack[track].append(
                    msg = mido.Message('polytouch', control=int(control), note=note, channel=int(channel)))
                self.last_event_time[track] = self.time[track]



if not MULTI_TRACK:
    class MidiFileManyTracksOutputDevice(iso.MidiFileOutputDevice):
        pass


# class FileOut(iso.MidiFileOutputDevice, iso.MidiOutputDevice):
class FileOut(MidiFileManyTracksOutputDevice, iso.MidiOutputDevice):

    def __init__(self, filename, device_name, send_clock, virtual=False):
        # iso.MidiFileOutputDevice.__init__(self, filename=filename)
        MidiFileManyTracksOutputDevice.__init__(self, filename=filename)
        iso.MidiOutputDevice.__init__(self, device_name=device_name, send_clock=send_clock, virtual=virtual)

    def note_off(self, note, channel, track_idx=0):
        MidiFileManyTracksOutputDevice.note_off(self, note=note, channel=channel, track_idx=track_idx)
        iso.MidiOutputDevice.note_off(self, note=note, channel=channel)

    def note_on(self, note, velocity, channel, track_idx=0):
        MidiFileManyTracksOutputDevice.note_on(self, note=note, velocity=velocity, channel=channel, track_idx=track_idx)
        iso.MidiOutputDevice.note_on(self, note=note, velocity=velocity, channel=channel)

    def program_change(self, program=0, channel=0, track_idx=0):
        # iso.MidiFileOutputDevice.program_change(self, program=program, channel=channel)
        MidiFileManyTracksOutputDevice.program_change(self, program=program, channel=channel, track_idx=track_idx)
        iso.MidiOutputDevice.program_change(self, program=program, channel=channel)
        # super().program_change(program=program, channel=channel)

    def control(self, control=0, value=0, channel=0, track_idx=0):
        # iso.MidiFileOutputDevice.control(self, control=control, value=value, channel=channel)
        MidiFileManyTracksOutputDevice.control(self, control=control, value=value, channel=channel, track_idx=track_idx)
        iso.MidiOutputDevice.control(self, control=control, value=value, channel=channel)
        # super().control(control=control, value=value, channel=channel)

    def pitch_bend(self, pitch=0, channel=0, track_idx=0):
        MidiFileManyTracksOutputDevice.pitch_bend(self, pitch=pitch, channel=channel, track_idx=track_idx)
        iso.MidiOutputDevice.pitch_bend(self, pitch=pitch, channel=channel)

    def aftertouch(self, control=0, value=0, channel=0, track_idx=0):
        MidiFileManyTracksOutputDevice.aftertouch(self, control=control, value=value, channel=channel, track_idx=track_idx)

    def polytouch(self, control=0, note=0, channel=0, track_idx=0):
        MidiFileManyTracksOutputDevice.polytouch(self, control=control, note=note, channel=channel, track_idx=track_idx)


    #
    #
    # def start(self):
    #     # iso.MidiFileOutputDevice.start(self)
    #     # MidiFileManyTracksOutputDevice.start(self)
    #     # iso.MidiOutputDevice.start(self)
    #     super().start()
    #
    # def stop(self):
    #     # iso.MidiFileOutputDevice.stop(self)
    #     # MidiFileManyTracksOutputDevice.stop(self)
    #     # iso.MidiOutputDevice.stop(self)
    #     super().stop()
    #
    # def tick(self):
    #     # iso.MidiFileOutputDevice.tick(self)
    #     MidiFileManyTracksOutputDevice.tick(self)
    #     iso.MidiOutputDevice.tick(self)
        # super().tick()

    def write(self, dedup = True):
        # iso.MidiFileOutputDevice.write(self)
        MidiFileManyTracksOutputDevice.write(self, dedup)

    # def ticks_per_beat(self):
    #     iso.MidiFileOutputDevice.ticks_per_beat
    #         ticks_per_beat(self, *args, **kwargs)
    #     iso.MidiOutputDevice.ticks_per_beat(self, *args, **kwargs)

class ExtendedMidiInputDevice(iso.MidiInputDevice):
    def _callback(self, message):

        log.debug(" - MIDI message received: %s" % message)

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
            else:
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

        elif message.type in ['note_on', 'note_off', 'control_change', 'pitchwheel','program_change']:
            if self.callback:
                self.callback(message)
            else:
                self.queue.put(message)

# </editor-fold>