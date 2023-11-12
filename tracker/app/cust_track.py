import copy
import inspect

from isobar import Track
from isobar.pattern import Pattern
from isobar.pattern import PInterpolate, PSequence, PDict

from isobar.constants import *
from isobar.exceptions import InvalidEventException
from isobar.util import midi_note_to_frequency

from tracker.app.cust_event import *

import logging

log = logging.getLogger(__name__)

class CustTrack(Track):

    def tick(self):
        """
        Step forward one tick.

        Args:
            tick_duration (float): Duration, in beats.
        """

        #----------------------------------------------------------------------
        # Process note_offs before we play the next note, else a repeated note
        # with gate = 1.0 will immediately be cancelled.
        #----------------------------------------------------------------------
        if self.event_stream['args']['track_idx'].constant is not None:
            track_idx = self.event_stream['args']['track_idx'].constant
        else:
            track_idx = 0

        # action_dur = []
        # if self.event_stream.dict.get('action', None):
        #     action_dur = self.event_stream.dict.get('duration', [])
        #
        #     # action_dur = []
        #     if bool(action_dur):
        #         pass
                # action_dur = [[x, 0, 0, 0] for x in action_dur.copy()]
                # print(action_dur)
        # else:
        #     # pass
        #     action_dur = []

        # if action_dur:
        #     # action_dur = [ [x, 0, 0, 0] for x in action_dur.copy() ]
        #     # mixed_list = [item for sublist in zip(numbers, [0] * len(numbers)) for item in sublist]
        #     # [a for x in [1, 2, 3] for a in (x, 0)]
        #     pass
            # action_dur = []

        # for n, note in enumerate(self.note_offs[:] or action_dur):
        for n, note in enumerate(self.note_offs[:] ):
            # TODO: Use a MidiNote object to represent these note_off events
            # try:
            if round(note[0], 8) <= round(self.current_time, 8):
                index = note[1]
                channel = note[2]
                self.output_device.note_off(index, channel, track_idx=track_idx)
                # if self.note_offs:
                self.note_offs.remove(note)
            # except Exception as e:
            #     x = 1


        try:
            if self.interpolate is INTERPOLATION_NONE:
                if round(self.current_time, 8) >= round(self.next_event_time, 8):
                    while round(self.current_time, 8) >= round(self.next_event_time, 8):
                        #--------------------------------------------------------------------------------
                        # Retrieve the next event.
                        # If no more events are available, this raises StopIteration.
                        #--------------------------------------------------------------------------------
                        self.current_event = self.get_next_event()
                        self.next_event_time += float(self.current_event.duration)

                    #--------------------------------------------------------------------------------
                    # Perform the event.
                    #--------------------------------------------------------------------------------
                    self.perform_event(self.current_event)
            else:
                #--------------------------------------------------------------------------------
                # Track has interpolation enabled.
                # Interpolation is done by wrapping the evolving event in an
                # interpolating_event, which generates a new value each tick until it is
                # exhausted.
                #--------------------------------------------------------------------------------
                try:
                    interpolated_values = next(self.interpolating_event)
                    interpolated_event = Event(interpolated_values, self.timeline.defaults)
                    self.perform_event(interpolated_event)
                except StopIteration:
                    is_first_event = False
                    if self.next_event is None:
                        #--------------------------------------------------------------------------------
                        # The current and next events are needed to perform interpolation.
                        # No events have yet been obtained, so query the current and next events off
                        # the stack.
                        #--------------------------------------------------------------------------------
                        self.next_event = self.get_next_event()
                        is_first_event = True

                    self.current_event = self.next_event
                    self.next_event = self.get_next_event()

                    #--------------------------------------------------------------------------------
                    # Special case to handle zero-duration events: continue to pop new
                    # events from the pattern.
                    #--------------------------------------------------------------------------------
                    while int(self.current_event.duration * self.timeline.ticks_per_beat) <= 0:
                        self.current_event = self.next_event
                        self.next_event = self.get_next_event()

                    if self.current_event.type != EVENT_TYPE_CONTROL or self.next_event.type != EVENT_TYPE_CONTROL:
                        raise InvalidEventException("Interpolation is only valid for control event")

                    interpolating_event_fields = copy.copy(self.current_event.fields)
                    duration = self.current_event.duration
                    duration_ticks = duration * self.timeline.ticks_per_beat
                    for key, value in self.current_event.fields.items():
                        #--------------------------------------------------------------------------------
                        # Create a new interpolating_event with patterns for each parameter to
                        # interpolate.
                        #--------------------------------------------------------------------------------
                        if key == EVENT_TYPE or key == EVENT_DURATION:
                            continue
                        if type(value) is not float and type(value) is not int:
                            continue
                        interpolating_event_fields[key] = PInterpolate(PSequence([self.current_event.fields[key],
                                                                                  self.next_event.fields[key]], 1),
                                                                       duration_ticks,
                                                                       self.interpolate)

                    self.interpolating_event = PDict(interpolating_event_fields)
                    if not is_first_event:
                        next(self.interpolating_event)
                    event = Event(next(self.interpolating_event), self.timeline.defaults)
                    self.perform_event(event)

        except StopIteration:
            if len(self.note_offs) == 0:
                self.is_finished = True

        self.current_time += self.tick_duration

    def perform_event(self, event):

        if event.fields['args']['track_idx'] is not None:
            track_idx = event.fields['args']['track_idx']
        elif self.event_stream['args']['track_idx'].constant is not None:
            track_idx = self.event_stream['args']['track_idx'].constant
        else:
            track_idx = 0
        if not event.active:
            return

        #------------------------------------------------------------------------
        # Action: Carry out an action each time this event is triggered
        #------------------------------------------------------------------------
        if event.type == EVENT_TYPE_ACTION:
            try:
                fn = event.action
                try:
                    fn_params = inspect.signature(fn).parameters
                    for key in event.args.keys():
                        if key not in fn_params:
                            raise Exception("Named argument not found in callback args: %s" % key)
                except ValueError:
                    #------------------------------------------------------------------------
                    # inspect.signature does not work on cython/pybind11 bindings, and
                    # raises a ValueError. In these cases, simply pass the arguments
                    # without validation.
                    #------------------------------------------------------------------------
                    pass

                event.action(**event.args)
            except StopIteration:
                raise StopIteration()
            except Exception as e:
                print(("Exception when handling scheduled action: %s" % e))
                import traceback
                traceback.print_exc()
                pass

        #------------------------------------------------------------------------
        # Control: Send a control value
        #------------------------------------------------------------------------
        elif event.type == EVENT_TYPE_CONTROL:
            log.debug("Control (channel %d, control %d, value %d)",
                      event.channel, event.control, event.value)
            self.output_device.control(event.control, event.value, event.channel, track_idx=track_idx)

        #------------------------------------------------------------------------
        # Program change
        #------------------------------------------------------------------------
        elif event.type == EVENT_TYPE_PROGRAM_CHANGE:
            log.debug("Program change (channel %d, program %d)",
                      event.channel, event.program_change)
            self.output_device.program_change(event.program_change, event.channel, track_idx=track_idx)

        #------------------------------------------------------------------------
        # address: Send a value to an OSC endpoint
        #------------------------------------------------------------------------
        elif event.type == EVENT_TYPE_OSC:
            self.output_device.send(event.osc_address, event.osc_params, track_idx=track_idx)

        #------------------------------------------------------------------------
        # SuperCollider synth
        #------------------------------------------------------------------------
        elif event.type == EVENT_TYPE_SUPERCOLLIDER:
            self.output_device.create(event.synth_name, event.synth_params, track_idx=track_idx)

        #------------------------------------------------------------------------
        # SignalFlow patch
        #------------------------------------------------------------------------
        elif event.type == EVENT_TYPE_PATCH_CREATE:
            #------------------------------------------------------------------------
            # Action: Create patch
            #------------------------------------------------------------------------
            if not hasattr(self.output_device, "create"):
                raise InvalidEventException("Device %s does not support this kind of event" % self.output_device)
            params = dict((key, Pattern.value(value)) for key, value in event.params.items())
            if hasattr(event, "note"):
                notes = event.note if hasattr(event.note, '__iter__') else [event.note]

                for note in notes:
                    if note > 0:
                        # TODO: Should use None to denote rests
                        params["frequency"] = midi_note_to_frequency(note)
                        self.output_device.create(event.patch, params, output=event.output, track_idx=track_idx)
            else:
                self.output_device.create(event.patch, params, output=event.output, track_idx=track_idx)

        elif event.type == EVENT_TYPE_PATCH_SET or event.type == EVENT_TYPE_PATCH_TRIGGER:
            #------------------------------------------------------------------------
            # Action: Set patch's input(s) and/or trigger an event
            #------------------------------------------------------------------------
            for key, value in event.params.items():
                value = Pattern.value(value)
                event.patch.set_input(key, value)

            if hasattr(event, "note"):
                event.patch.set_input("frequency", midi_note_to_frequency(event.note))

            if event.type == EVENT_TYPE_PATCH_TRIGGER:
                #------------------------------------------------------------------------
                # Action: Trigger a patch
                #------------------------------------------------------------------------
                if not hasattr(self.output_device, "trigger"):
                    raise InvalidEventException("Device %s does not support this kind of event" % self.output_device)
                params = dict((key, Pattern.value(value)) for key, value in event.params.items())
                self.output_device.trigger(event.patch, event.trigger_name, event.trigger_value, track_idx=track_idx)

        #------------------------------------------------------------------------
        # Note: Classic MIDI note
        #------------------------------------------------------------------------
        elif event.type == EVENT_TYPE_NOTE:
            #----------------------------------------------------------------------
            # event: Certain devices (eg Socket IO) handle generic events,
            #        rather than note_on/note_off. (Should probably have to
            #        register for this behaviour rather than happening magically...)
            #----------------------------------------------------------------------
            if hasattr(self.output_device, "event") and callable(getattr(self.output_device, "event")):
                d = copy.copy(event)
                for key, value in list(d.items()):
                    #------------------------------------------------------------------------
                    # turn non-builtin objects into their string representations.
                    # we don't want to call repr() on numbers as it turns them into strings,
                    # which we don't want to happen in our resultant JSON.
                    # TODO: there absolutely must be a way to do this for all objects which are
                    #       non-builtins... ie, who are "class" instances rather than "type".
                    #
                    #       we could check dir(__builtins__), but for some reason, __builtins__ is
                    #       different here than it is outside of a module!?
                    #
                    #       instead, go with the lame option of listing "primitive" types.
                    #------------------------------------------------------------------------
                    if type(value) not in (int, float, bool, str, list, dict, tuple):
                        value = repr(value)
                        d[key] = value

                self.output_device.event(d)
                return

            #----------------------------------------------------------------------
            # note_on: Standard (MIDI) type of device
            #----------------------------------------------------------------------
            if type(event.amplitude) is tuple or event.amplitude > 0:
                # TODO: pythonic duck-typing approach might be better
                # TODO: doesn't handle arrays of amp, channel event, etc
                notes = event.note if hasattr(event.note, '__iter__') else [event.note]

                #----------------------------------------------------------------------
                # Allow for arrays of amp, gate etc, to handle chords properly.
                # Caveat: Things will go horribly wrong for an array of amp/gate event
                # shorter than the number of notes.
                #----------------------------------------------------------------------
                for index, note in enumerate(notes):
                    amp = event.amplitude[index] if isinstance(event.amplitude, tuple) else event.amplitude
                    channel = event.channel[index] if isinstance(event.channel, tuple) else event.channel
                    gate = event.gate[index] if isinstance(event.gate, tuple) else event.gate
                    # TODO: Add an EVENT_SUSTAIN that allows absolute note lengths to be specified

                    if (amp is not None and amp > 0) and (gate is not None and gate > 0):
                        self.output_device.note_on(note, amp, channel, track_idx=track_idx)

                        note_dur = event.duration * gate
                        self.schedule_note_off(self.current_time + note_dur, note, channel, track_idx=track_idx )
        else:
            raise InvalidEventException("Invalid event type: %s" % event.type)

        if self.timeline.on_event_callback:
            self.timeline.on_event_callback(self, event)

    def schedule_note_off(self, time, note, channel, track_idx=0):
        self.note_offs.append([time, note, channel, track_idx])


Track.tick=CustTrack.tick
Track.perform_event=CustTrack.perform_event
Track.schedule_note_off=CustTrack.schedule_note_off