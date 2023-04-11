import mido
import isobar as iso

global MULTI_TRACK
MULTI_TRACK = True

# MULTI_TRACK = False

if MULTI_TRACK:
    class MidiFileManyTracksOutputDevice(iso.MidiFileOutputDevice):

        def __init__(self, filename):
            self.filename = filename
            self.midifile = mido.MidiFile()
            self.miditrack = [mido.MidiTrack()]
            self.midifile.tracks.append(self.miditrack[0])
            self.channel_track = []
            self.channel_track.append(0)
            self.time = []
            self.time.append(0)
            self.last_event_time = []
            self.last_event_time.append(0)

        def extra_track(self, channel=None):
            if channel:
                if not [x for x in self.channel_track if x == channel]:
                    track = mido.MidiTrack()
                    self.miditrack.append(track)
                    self.midifile.tracks.append(track)
                    self.channel_track.append(channel)
                    self.time.append(0)
                    self.last_event_time.append(0)

        def get_channel_track(self, channel=0):
            try:
                track = self.channel_track.index(channel)
            except:
                track = 0
            return track

        def note_on(self, note=60, velocity=64, channel=0):
            # ------------------------------------------------------------------------
            # avoid rounding errors
            # ------------------------------------------------------------------------
            track = self.get_channel_track(channel)
            print(f"----------------track var: {channel=} {track=}")
            if track >= 0:
                print(f"------------note on: {track=}, {note=}, {channel=}")
                dt = self.time[track] - self.last_event_time[track]
                dt_ticks = int(round(dt * self.midifile.ticks_per_beat))
                self.miditrack[track].append(
                    mido.Message('note_on', note=note, velocity=velocity, channel=channel, time=dt_ticks))
                self.last_event_time[track] = self.time[track]

        def note_off(self, note=60, channel=0):
            track = self.get_channel_track(channel)
            if track >= 0:
                print(f"------------note on: {track=}, {note=}, {channel=}")
                dt = self.time[track] - self.last_event_time[track]
                dt_ticks = int(round(dt * self.midifile.ticks_per_beat))
                self.miditrack[track].append(mido.Message('note_off', note=note, channel=channel, time=dt_ticks))
                self.last_event_time[track] = self.time[track]

        def tick(self):
            self.time = list(map(lambda x: x + (1.0 / self.ticks_per_beat), self.time))

            pass

if not MULTI_TRACK:
    class MidiFileManyTracksOutputDevice(iso.MidiFileOutputDevice):
        pass


# class FileOut(iso.MidiFileOutputDevice, iso.MidiOutputDevice):
class FileOut(MidiFileManyTracksOutputDevice, iso.MidiOutputDevice):

    def __init__(self, filename, device_name, send_clock, virtual=False):
        # iso.MidiFileOutputDevice.__init__(self, filename=filename)
        MidiFileManyTracksOutputDevice.__init__(self, filename=filename)
        iso.MidiOutputDevice.__init__(self, device_name=device_name, send_clock=send_clock, virtual=virtual)

    def note_off(self, note, channel):
        MidiFileManyTracksOutputDevice.note_off(self, note=note, channel=channel)
        iso.MidiOutputDevice.note_off(self, note=note, channel=channel)

    def note_on(self, note, velocity, channel):
        MidiFileManyTracksOutputDevice.note_on(self, note=note, velocity=velocity, channel=channel)
        iso.MidiOutputDevice.note_on(self, note=note, velocity=velocity, channel=channel)

    # def program_change(self, program=0, channel=0):
    # iso.MidiFileOutputDevice.program_change(self, program=program, channel=channel)
    # MidiFileManyTracksOutputDevice.program_change(self, program=program, channel=channel)
    # iso.MidiOutputDevice.program_change(self, program=program, channel=channel)
    # super().program_change(program=program, channel=channel)

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
    #     # MidiFileManyTracksOutputDevice.tick(self)
    #     # iso.MidiOutputDevice.tick(self)
    #     super().tick()

    def write(self):
        iso.MidiFileOutputDevice.write(self)

    # def ticks_per_beat(self):
    #     iso.MidiFileOutputDevice.ticks_per_beat
    #         ticks_per_beat(self, *args, **kwargs)
    #     iso.MidiOutputDevice.ticks_per_beat(self, *args, **kwargs)


# </editor-fold>