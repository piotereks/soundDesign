import threading
import time

import mido
from mido.midifiles.tracks import MidiTrack, merge_tracks, fix_end_of_track
from mido.midifiles.units import tick2second


def _to_abstime(messages):
    """Convert messages to absolute time."""
    now = 0
    for msg in messages:
        now += msg.time
        yield msg.copy(time=now)


def _to_reltime(messages):
    """Convert messages to relative time."""
    now = 0
    for msg in messages:
        delta = msg.time - now
        yield msg.copy(time=delta)
        now = msg.time


def merge_tracks(tracks):
    """Returns a MidiTrack object with all messages from all tracks.

    The messages are returned in playback order with delta times
    as if they were all in one track.
    """
    messages = []
    track_idx = []
    for track in tracks:
        abs_trk = list(_to_abstime(track))
        track_idx.extend([tracks.index(track)] * len(list(abs_trk)))
        messages.extend(abs_trk)

    msg_zip_list = list(zip(messages, track_idx))
    msg_zip_list.sort(key=lambda m: m[0].time)
    messages, track_idx = zip(*msg_zip_list)
    # messages.sort(key=lambda msg: msg.time)

    return MidiTrack(fix_end_of_track(_to_reltime(messages))), track_idx


mido.midifiles.tracks.merge_tracks = merge_tracks
mido.midifiles.tracks._to_abstime = _to_abstime
mido.midifiles.tracks._to_reltime = _to_reltime


# class CustMidiFile(mido.MidiFile):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
        # self.run_event = threading.Event()
        # self.run_event.set()
        #
        # self.break_flag = threading.Event()
        # self.break_flag.clear()

    # def __iter__(self):
    #     # The tracks of type 2 files are not in sync, so they can
    #     # not be played back like this.
    #     if self.type == 2:
    #         raise TypeError("can't merge tracks in type 2 (asynchronous) file")
    #
    #     tempo = mido.midifiles.midifiles.DEFAULT_TEMPO
    #     merged_tracks, merged_tracks_idx = merge_tracks(self.tracks)
    #     for msg in merged_tracks:
    #         # Convert message time from absolute time
    #         # in ticks to relative time in seconds.
    #         if msg.time > 0:
    #             delta = tick2second(msg.time, self.ticks_per_beat, tempo)
    #         else:
    #             delta = 0
    #
    #         yield msg.copy(time=delta), merged_tracks_idx[merged_tracks.index(msg)]
    #
    #         if msg.type == 'set_tempo':
    #             tempo = msg.tempo

    # def play(self, meta_messages=False):
    #     """Play back all tracks.
    #
    #     The generator will sleep between each message by
    #     default. Messages are yielded with correct timing. The time
    #     attribute is set to the number of seconds slept since the
    #     previous message.
    #
    #     By default you will only get normal MIDI messages. Pass
    #     meta_messages=True if you also want meta messages.
    #
    #     You will receive copies of the original messages, so you can
    #     safely modify them without ruining the tracks.
    #     """
    #     start_time = time.time()
    #     input_time = 0.0
    #     time_variable = time.time()
    #     for msg, msg_track in self:
    #         time_delta = time.time() - time_variable
    #         time_variable += time_delta
    #         if not self.run_event.is_set():
    #             self.run_event.wait()
    #             time_delta = time.time() - time_variable
    #             time_variable += time_delta
    #             start_time += time_delta
    #         input_time += msg.time
    #
    #         playback_time = time.time() - start_time
    #         duration_to_next_event = input_time - playback_time
    #         if duration_to_next_event > 0.0:
    #             time.sleep(duration_to_next_event)
    #
    #         if isinstance(msg, mido.MetaMessage) and not meta_messages:
    #             continue
    #         msg_cpy = msg.copy()
    #         msg_cpy.time = round(msg_cpy.time)
    #         yield msg_cpy, msg_track


# mido.MidiFile = CustMidiFile
