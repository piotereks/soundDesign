import copy
import inspect

from isobar import Track
from isobar.pattern import Pattern

from isobar.constants import *
from isobar.exceptions import InvalidEventException
from isobar.util import midi_note_to_frequency

import logging

log = logging.getLogger(__name__)

class CustTrack(Track):

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
            self.output_device.control(event.control, event.value, event.channel)

        #------------------------------------------------------------------------
        # Program change
        #------------------------------------------------------------------------
        elif event.type == EVENT_TYPE_PROGRAM_CHANGE:
            log.debug("Program change (channel %d, program %d)",
                      event.channel, event.program_change)
            self.output_device.program_change(event.program_change, event.channel)

        #------------------------------------------------------------------------
        # address: Send a value to an OSC endpoint
        #------------------------------------------------------------------------
        elif event.type == EVENT_TYPE_OSC:
            self.output_device.send(event.osc_address, event.osc_params)

        #------------------------------------------------------------------------
        # SuperCollider synth
        #------------------------------------------------------------------------
        elif event.type == EVENT_TYPE_SUPERCOLLIDER:
            self.output_device.create(event.synth_name, event.synth_params)

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
                        self.output_device.create(event.patch, params, output=event.output)
            else:
                self.output_device.create(event.patch, params, output=event.output)

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
                self.output_device.trigger(event.patch, event.trigger_name, event.trigger_value)

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
                        self.output_device.note_on(note, amp, channel)

                        note_dur = event.duration * gate
                        self.schedule_note_off(self.current_time + note_dur, note, channel)
        else:
            raise InvalidEventException("Invalid event type: %s" % event.type)

        if self.timeline.on_event_callback:
            self.timeline.on_event_callback(self, event)


Track.perform_event=CustTrack.perform_event