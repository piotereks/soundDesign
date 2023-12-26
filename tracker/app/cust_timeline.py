import copy
import logging
import math
from collections.abc import Iterable
from functools import partial

from isobar import Track, PSequence, Clock, Key, Scale
# from isobar.constants import (EVENT_ACTION, EVENT_ACTION_ARGS, INTERPOLATION_NONE,
#                               EVENT_DURATION, DEFAULT_TEMPO,DEFAULT_TICKS_PER_BEAT)
from isobar.constants import *
from isobar.exceptions import TrackLimitReachedException
from isobar.io import MidiOutputDevice

log = logging.getLogger(__name__)


class EventDefaults:
    def __init__(self):
        default_values = {
            EVENT_ACTIVE: True,
            EVENT_CHANNEL: DEFAULT_EVENT_CHANNEL,
            EVENT_DURATION: DEFAULT_EVENT_DURATION,
            EVENT_GATE: DEFAULT_EVENT_GATE,
            EVENT_AMPLITUDE: DEFAULT_EVENT_AMPLITUDE,
            EVENT_OCTAVE: DEFAULT_EVENT_OCTAVE,
            EVENT_TRANSPOSE: DEFAULT_EVENT_TRANSPOSE,
            EVENT_KEY: Key("C", Scale.default),
            EVENT_QUANTIZE: DEFAULT_EVENT_QUANTIZE
        }
        for key, value in default_values.items():
            setattr(self, key, value)


class CustTimeline():
    def __init__(self,
                 tempo=DEFAULT_TEMPO,
                 output_device=None,
                 clock_source=None,
                 ticks_per_beat=DEFAULT_TICKS_PER_BEAT):
        """ Expect to receive one tick per beat, generate events at 120bpm """
        self._clock_source = None
        if clock_source is None:
            clock_source = Clock(self, tempo, ticks_per_beat)
        self.set_clock_source(clock_source)

        self.output_devices = []
        self.clock_multipliers = {}
        if output_device:
            self.add_output_device(output_device)

        self.current_time = 0
        self.max_tracks = 0
        self.tracks = []

        self.thread = None
        self.stop_when_done = False
        self.events = []
        self.running = False
        self.ignore_exceptions = False

        self.defaults = EventDefaults()

        # --------------------------------------------------------------------------------
        # Optional callback to trigger each time an event is performed.
        # --------------------------------------------------------------------------------
        self.on_event_callback = None

    def schedule(self,
                 params=None,
                 quantize=None,
                 delay=0,
                 count=None,
                 interpolate=INTERPOLATION_NONE,
                 output_device=None,
                 remove_when_done=True,
                 name=None,
                 replace=False,
                 track_index=None,
                 sel_track_idx=None):
        """
        Schedule a new track within this Timeline.

        Args:
            params (dict):           Event dictionary. Keys are generally EVENT_* values, defined in constants.py.
                                     If param is None, a new empty Track will be scheduled and returned.
                                     This can be updated with Track.update().
                                     param can alternatively be a Pattern that generates a dict output.
            name (str):              Optional name for the track.
            quantize (float):        Quantize level, in beats. For example, 1.0 will begin executing the
                                     events on the next whole beats.
            delay (float):           Delay time, in beats, before events should be executed.
                                     If `quantize` and `delay` are both specified, quantization is applied,
                                     and the event is scheduled `delay` beats after the quantization time.
            count (int):             Number of events to process, or unlimited if not specified.
            interpolate (int):       Interpolation mode for control segments.
            output_device:           Output device to send events to. Uses the Timeline default if not specified.
            remove_when_done (bool): If True, removes the Track from the Timeline when it is finished.
                                     Otherwise, retains the Track, so update() can later be called to schedule
                                     additional events on it.
            name (str):              Optional name to identify the Track. If given, can be used to update the track's
                                     parameters in future calls to schedule() by specifying replace=True.
            replace (bool):          Must be used in conjunction with the `name` parameter. Instead of scheduling a
                                     new Track, this updates the parameters of an existing track with the same name.
            track_index (int):       When specified, inserts the Track at the given index.
                                     This can be used to set the priority of an event and ensure that it happens
                                     before another Track is evaluated, used in (e.g.) Track.update().
            sel_track_idx (int):     Track index to use for event arguments (default: None). This says about midinote track schedule us assigned to
        Returns:
            The new `Track` object.

        Raises:
            TrackLimitReachedException: If `max_tracks` has been reached.
        """

        # --------------------------------------------------------------------------------
        # Take a copy of param to avoid modifying the original
        # --------------------------------------------------------------------------------
        params_list = params if isinstance(params, list) else [params]
        tracks_list = []
        params_list2 = []
        event_args = {}
        for param in params_list:
            # with snoop:
            #     x = self.tracks
            print(param)
            if not isinstance(param, dict):
                param = dict(param)
            action_fun = param.get(EVENT_ACTION, None)
            event_args = param.get(EVENT_ACTION_ARGS, {})
            if action_fun and isinstance(action_fun, Iterable):
                attributes1 = vars(action_fun)
                # Get the attributes used by the class constructor
                constructor_attributes = list(PSequence.__init__.__code__.co_varnames[1:])

                # Filter the modified attributes to include only those used by the constructor
                attributes = {k: v for k, v in attributes1.copy().items() if
                              k in constructor_attributes}
                attributes2 = {k: v for k, v in attributes1.copy().items() if
                               k in constructor_attributes}
                action_fun2 = [
                                  partial(f, self) if isinstance(f, partial) else f
                                  for f in copy.copy(action_fun)
                              ][:1]
                attributes2['sequence'] = action_fun2
                action_fun2 = PSequence(**attributes2)
                params2 = copy.copy(param)
                params2[EVENT_ACTION] = action_fun2
                if event_args:
                    params2[EVENT_ACTION_ARGS] = event_args
                dur2 = list(params2.pop(EVENT_DURATION, None))

                # print(f"before dur2 {dur2=} {bool(dur2)=}")
                if dur2:
                    params2[EVENT_DURATION] = PSequence(dur2[:1], repeats=1)
                params_list2.append(params2)

                action_fun = [partial(f, self) if isinstance(f, partial) else f for f in copy.copy(action_fun)][1:]
                attributes['sequence'] = action_fun
                action_fun = PSequence(**attributes)
                param[EVENT_ACTION] = action_fun
                if event_args:
                    param[EVENT_ACTION_ARGS] = event_args

                dur = list(param.pop(EVENT_DURATION, None))

                if dur:
                    param["delay"] = dur[0]
                    param[EVENT_DURATION] = PSequence(dur[1:], repeats=1)

            elif action_fun:
                param[EVENT_ACTION] = action_fun
                param[EVENT_ACTION_ARGS] = event_args

            params_list2.append(param)

        print(params_list2)
        if not output_device:
            # --------------------------------------------------------------------------------
            # If no output device exists, send to the system default MIDI output.
            # --------------------------------------------------------------------------------
            if not self.output_devices:
                self.add_output_device(MidiOutputDevice())
            output_device = self.output_devices[0]

            # --------------------------------------------------------------------------------
            # If replace=True is specified, updated the param of any existing track
            # with the same name. If none exists, proceed to create it as usual.
            # --------------------------------------------------------------------------------
        for param in params_list2:
            extra_delay = param.pop("delay", None)
            if replace:
                if name is None:
                    raise ValueError("Must specify a track name if `replace` is specified")
                for existing_track in self.tracks:
                    if existing_track.name == name:
                        existing_track.update(param, quantize=quantize)
                        return

            if self.max_tracks and len(self.tracks) >= self.max_tracks:
                raise TrackLimitReachedException(
                    "Timeline: Refusing to schedule track (hit limit of %d)" % self.max_tracks)

            def start_track(track_int):
                # --------------------------------------------------------------------------------
                # Add a new track.
                # --------------------------------------------------------------------------------
                if track_index is not None:
                    self.tracks.insert(track_index, track_int)
                else:
                    self.tracks.append(track_int)
                log.info("Timeline: Scheduled new track (total tracks: %d)" % len(self.tracks))

            if not bool(event_args):
                event_args = {"track_idx": sel_track_idx}
            if not bool(param.get(EVENT_ACTION_ARGS, {})):
                param[EVENT_ACTION_ARGS] = event_args

            if isinstance(param, Track):
                track = param
                track.reset()
            else:
                # --------------------------------------------------------------------------------
                # Take a copy of param to avoid modifying the original
                # --------------------------------------------------------------------------------
                track = Track(self,
                              copy.copy(param),
                              max_event_count=count,
                              interpolate=interpolate,
                              output_device=output_device,
                              remove_when_done=remove_when_done,
                              name=name)
            tracks_list.append(track)

            if quantize is None:
                quantize = self.defaults.quantize
            if quantize or delay or extra_delay:
                # if quantize or delay:
                # --------------------------------------------------------------------------------
                # We don't want to begin events right away -- either wait till
                # the next beat boundary (quantize), or delay a number of beats.
                # --------------------------------------------------------------------------------
                scheduled_time = self.current_time
                if quantize:
                    scheduled_time = quantize * math.ceil(float(self.current_time) / quantize)
                scheduled_time += delay or extra_delay
                # scheduled_time += delay
                self.events.append({
                    EVENT_TIME: scheduled_time,
                    EVENT_ACTION: lambda t=track: start_track(t)
                })
            else:
                # --------------------------------------------------------------------------------
                # Begin events on this track right away.
                # --------------------------------------------------------------------------------
                start_track(track)

        if len(tracks_list) > 1:
            track = tracks_list
        elif len(tracks_list) == 1:
            track = tracks_list[0]
        else:
            track = None

        return track

    def tick(self):
        """
        Called once every tick to trigger new events.

        Raises:
            StopIteration: If `stop_when_done` is true and no more events are scheduled.
        """
        # --------------------------------------------------------------------------------
        # Each time we arrive at precisely a new beat, generate a debug msg.
        # Round to several decimal places to avoid 7.999999999 syndrome.
        # http://docs.python.org/tutorial/floatingpoint.html
        # --------------------------------------------------------------------------------

        if round(self.current_time, 8) % 1 == 0:
            log.debug("--------------------------------------------------------------------------------")
            log.debug("Tick (%d active tracks, %d pending events)" % (len(self.tracks), len(self.events)))

        # --------------------------------------------------------------------------------
        # Copy self.events because removing from it whilst using it = bad idea.
        # Perform events before tracks are executed because an event might
        # include scheduling a quantized track, which should then be
        # immediately evaluated.
        # --------------------------------------------------------------------------------
        for event in self.events[:]:
            # --------------------------------------------------------------------------------
            # The only event we currently get in a Timeline are add_track events
            #  -- which have a function object associated with them.
            #
            # Round to work around rounding errors.
            # http://docs.python.org/tutorial/floatingpoint.html
            # --------------------------------------------------------------------------------
            if round(event[EVENT_TIME], 8) <= round(self.current_time, 8):
                event[EVENT_ACTION]()
                self.events.remove(event)

        # --------------------------------------------------------------------------------
        # Copy self.tracks because removing from it whilst using it = bad idea
        # --------------------------------------------------------------------------------

        for track in self.tracks[:]:
            try:
                track.tick()
            except Exception as e:
                if self.ignore_exceptions:
                    print(f"*** Exception in track: {e}")
                else:
                    raise
            if track.is_finished and track.remove_when_done:
                self.tracks.remove(track)
                log.info("Timeline: Track finished, removing from scheduler (total tracks: %d)" % len(self.tracks))

        # --------------------------------------------------------------------------------
        # If we've run out of notes, raise a StopIteration.
        # --------------------------------------------------------------------------------
        if len(self.tracks) == 0 and len(self.events) == 0 and self.stop_when_done:
            # TODO: Don't do this if we've never played any events, e.g.
            #       right after calling timeline.background(). Should at least
            #       wait for some events to happen first.
            raise StopIteration

        # --------------------------------------------------------------------------------
        # Tell our output devices to move forward a step.
        # --------------------------------------------------------------------------------
        for device in self.output_devices:
            clock_multiplier = self.clock_multipliers[device]
            ticks = next(clock_multiplier)

            for _ in range(ticks):
                device.tick()

        # --------------------------------------------------------------------------------
        # Increment beat count according to our current tick_length.
        # --------------------------------------------------------------------------------
        self.current_time += self.tick_duration

    # @snoop(depth=2)
    def run(self, stop_when_done=None):
        """ Run this Timeline in the foreground.

        If stop_when_done is set, returns when no tracks are currently
        scheduled; otherwise, keeps running indefinitely. """

        self.start()

        if stop_when_done is not None:
            self.stop_when_done = stop_when_done

        try:
            # --------------------------------------------------------------------------------
            # Start the clock. This might internal (eg a Clock object, running on
            # an independent thread), or external (eg a MIDI clock).
            # --------------------------------------------------------------------------------
            for device in self.output_devices:
                device.start()
            self.running = True
            self.clock_source.run()

        except StopIteration:
            # --------------------------------------------------------------------------------
            # This will be hit if every Pattern in a timeline is exhausted.
            # --------------------------------------------------------------------------------
            log.info("Timeline: Finished")
            self.running = False

        except Exception as e:
            print(f" *** Exception in Timeline thread: {e}")
            if not self.ignore_exceptions:
                raise e
