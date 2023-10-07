import math
import copy

# import isobar
from isobar import Timeline, Track, PSequence, PDict
from isobar.constants import EVENT_TIME, EVENT_ACTION, INTERPOLATION_NONE
from isobar.io import MidiOutputDevice
from isobar.exceptions import TrackLimitReachedException
from functools import partial
from collections.abc import Iterable
import logging

log = logging.getLogger(__name__)


class CustTimeline(Timeline):

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
                 track_index=None):
        """
        Schedule a new track within this Timeline.

        Args:
            params (dict):           Event dictionary. Keys are generally EVENT_* values, defined in constants.py.
                                     If params is None, a new empty Track will be scheduled and returned.
                                     This can be updated with Track.update().
                                     params can alternatively be a Pattern that generates a dict output.
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
                                     before another Track is evaluted, used in (e.g.) Track.update().

        Returns:
            The new `Track` object.

        Raises:
            TrackLimitReachedException: If `max_tracks` has been reached.
        """

        # --------------------------------------------------------------------------------
        # Take a copy of params to avoid modifying the original
        # --------------------------------------------------------------------------------
        if not isinstance(params, list):
            params_list = [params]
        else:
            params_list = params
        tracks_list = []
        for params in params_list:
            if isinstance(params, PDict):
                params = dict(params)
            # params = copy.copy(params)
            action_fun = params.pop(EVENT_ACTION, None)

            if action_fun and isinstance(action_fun, Iterable):
                attributes = vars(action_fun)
                # Get the attributes used by the class constructor
                constructor_attributes = list(PSequence.__init__.__code__.co_varnames[1:])

                # Filter the modified attributes to include only those used by the constructor
                attributes = {k: v for k, v in attributes.copy().items() if
                              k in constructor_attributes}
                action_fun = [partial(f, self) if isinstance(f, partial) else f for f in action_fun]
                attributes['sequence'] = action_fun
                # action_fun = PSequence(action_fun, repeats=1)
                action_fun = PSequence(**attributes)
                params[EVENT_ACTION] = action_fun
            elif action_fun:
                params[EVENT_ACTION] = action_fun
            # params = PDict(params)



            if not output_device:
                # --------------------------------------------------------------------------------
                # If no output device exists, send to the system default MIDI output.
                # --------------------------------------------------------------------------------
                if not self.output_devices:
                    self.add_output_device(MidiOutputDevice())
                output_device = self.output_devices[0]

            # --------------------------------------------------------------------------------
            # If replace=True is specified, updated the params of any existing track
            # with the same name. If none exists, proceed to create it as usual.
            # --------------------------------------------------------------------------------
            if replace:
                if name is None:
                    raise ValueError("Must specify a track name if `replace` is specified")
                for existing_track in self.tracks:
                    if existing_track.name == name:
                        existing_track.update(params, quantize=quantize)
                        return

            if self.max_tracks and len(self.tracks) >= self.max_tracks:
                raise TrackLimitReachedException("Timeline: Refusing to schedule track (hit limit of %d)" % self.max_tracks)

            def add_track(track):
                # --------------------------------------------------------------------------------
                # Add a new track.
                # --------------------------------------------------------------------------------
                if track_index is not None:
                    self.tracks.insert(track_index, track)
                else:
                    self.tracks.append(track)
                log.info("Timeline: Scheduled new track (total tracks: %d)" % len(self.tracks))

            if isinstance(params, Track):
                track = params
                track.reset()
            else:
                # --------------------------------------------------------------------------------
                # Take a copy of params to avoid modifying the original
                # --------------------------------------------------------------------------------
                track = Track(self,
                              events=copy.copy(params),
                              max_event_count=count,
                              interpolate=interpolate,
                              output_device=output_device,
                              remove_when_done=remove_when_done,
                              name=name)
                tracks_list.append(track)

            if quantize is None:
                quantize = self.defaults.quantize
            if quantize or delay:
                # --------------------------------------------------------------------------------
                # We don't want to begin events right away -- either wait till
                # the next beat boundary (quantize), or delay a number of beats.
                # --------------------------------------------------------------------------------
                self._schedule_action(function=lambda: add_track(track),
                                      quantize=quantize,
                                      delay=delay)
            else:
                # --------------------------------------------------------------------------------
                # Begin events on this track right away.
                # --------------------------------------------------------------------------------
                add_track(track)

        if len(tracks_list) > 1:
            track = tracks_list
        elif len(tracks_list) == 1:
            track = tracks_list[0]
        else:
            track = None

        return track


Timeline.schedule = CustTimeline.schedule