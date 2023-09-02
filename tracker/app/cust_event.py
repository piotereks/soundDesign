from isobar.timeline.event import Event, EventDefaults
from isobar.exceptions import InvalidEventException
# from isobar.constants import EVENT_NOTE, EVENT_ACTION, EVENT_DEGREE
from isobar import Scale, Key, Pattern
from isobar.constants import *
from typing import Iterable

# class XCustEvent(Event):
#     def __init__(self, event_values):
#
#         parm = list(set([EVENT_NOTE, EVENT_ACTION, EVENT_DEGREE]) & set(event_values))
#         if len(parm) >= 2:
#             raise InvalidEventException(f"Cannot specify both '{parm[0]}' 'and '{parm[1]}'")

class CustEvent():
    def __init__(self, event_values, defaults=EventDefaults()):
        for key in event_values.keys():
            if key not in ALL_EVENT_PARAMETERS:
                raise ValueError("Invalid key for event: %s" % (key))

        parm = list(set([EVENT_NOTE, EVENT_ACTION, EVENT_DEGREE]) & set(event_values))
        if len(parm) >= 2:
            raise InvalidEventException(f"Cannot specify both '{parm[0]}' 'and '{parm[1]}'")

        if EVENT_DURATION_LEGACY in event_values:
            event_values[EVENT_DURATION] = event_values[EVENT_DURATION_LEGACY]
        if EVENT_AMPLITUDE_LEGACY in event_values:
            event_values[EVENT_AMPLITUDE] = event_values[EVENT_AMPLITUDE_LEGACY]

        for key, value in defaults.__dict__.items():
            # Defaults can be patterns too
            event_values.setdefault(key, Pattern.value(value))

        if EVENT_NOTE in event_values and EVENT_DEGREE in event_values:
            raise InvalidEventException("Cannot specify both note and degree")

        #------------------------------------------------------------------------
        # Note/degree/etc: Send a MIDI note
        #------------------------------------------------------------------------
        if EVENT_DEGREE in event_values:
            degree = event_values[EVENT_DEGREE]
            if degree is None:
                event_values[EVENT_NOTE] = None
            else:
                key = event_values[EVENT_KEY]
                if isinstance(key, str):
                    key = Key(key)

                #----------------------------------------------------------------------
                # handle lists of notes (eg chords).
                # TODO: create a class which allows for scalars and arrays to handle
                # addition transparently
                #----------------------------------------------------------------------
                try:
                    event_values[EVENT_NOTE] = [key[n] for n in degree]
                except TypeError:
                    event_values[EVENT_NOTE] = key[degree]

        #----------------------------------------------------------------------
        # For cases in which we want to introduce a rest, set amplitude
        # to zero. This means that we can still send rest events to
        # devices which receive all generic events (useful to display rests
        # when rendering a score).
        #----------------------------------------------------------------------
        if EVENT_NOTE in event_values:
            if event_values[EVENT_NOTE] is None:
                #----------------------------------------------------------------------
                # Rest.
                #----------------------------------------------------------------------
                event_values[EVENT_NOTE] = 0
                event_values[EVENT_AMPLITUDE] = 0
                event_values[EVENT_GATE] = 0
            else:
                #----------------------------------------------------------------------
                # Handle lists of notes (eg chords).
                # TODO: create a class which allows for scalars and arrays to handle
                #       addition transparently.
                #
                # The below does not allow for event_values[EVENT_TRANSPOSE] to be an array,
                # for example.
                #----------------------------------------------------------------------
                try:
                    event_values[EVENT_NOTE] = [note +
                                                event_values[EVENT_OCTAVE] * 12 +
                                                event_values[EVENT_TRANSPOSE] for note in event_values[EVENT_NOTE]]
                except TypeError:
                    event_values[EVENT_NOTE] += event_values[EVENT_OCTAVE] * 12 + event_values[EVENT_TRANSPOSE]

        #----------------------------------------------------------------------
        # Classify the event type.
        #----------------------------------------------------------------------
        if EVENT_ACTION in event_values:
            self.type = EVENT_TYPE_ACTION
            self.action = event_values[EVENT_ACTION]
            self.args = {}
            if EVENT_ACTION_ARGS in event_values:
                self.args = dict((key, Pattern.value(value)) for key, value in event_values[EVENT_ACTION_ARGS].items())

        elif EVENT_PATCH in event_values:
            #----------------------------------------------------------------------
            # Patches support different event types:
            #  - create from PatchSpec (EVENT_TYPE_PATCH_CREATE)
            #  - trigger Patch (EVENT_TYPE_PATCH_TRIGGER)
            #  - set Patch params (EVENT_TYPE_PATCH_SET)
            #----------------------------------------------------------------------
            self.patch = event_values[EVENT_PATCH]
            self.output = None

            if EVENT_TYPE in event_values:
                self.type = event_values[EVENT_TYPE]
            else:
                if type(self.patch).__name__ == "PatchSpec" or isinstance(self.patch, type):
                    self.type = EVENT_TYPE_PATCH_CREATE
                else:
                    self.type = EVENT_TYPE_PATCH_SET

            if EVENT_PATCH_OUTPUT in event_values:
                self.output = event_values[EVENT_PATCH_OUTPUT]

            self.params = {}
            if EVENT_PATCH_PARAMS in event_values:
                self.params = event_values[EVENT_PATCH_PARAMS]

            if EVENT_NOTE in event_values:
                self.note = event_values[EVENT_NOTE]

            # TODO: Different kinds of event should really be different classes
            self.trigger_name = None
            self.trigger_value = None
            if EVENT_TRIGGER_NAME in event_values:
                self.trigger_name = event_values[EVENT_TRIGGER_NAME]
            if EVENT_TRIGGER_VALUE in event_values:
                self.trigger_value = event_values[EVENT_TRIGGER_VALUE]

        elif EVENT_CONTROL in event_values:
            self.type = EVENT_TYPE_CONTROL
            self.control = event_values[EVENT_CONTROL]
            self.value = event_values[EVENT_VALUE]
            self.channel = event_values[EVENT_CHANNEL]

        elif EVENT_PROGRAM_CHANGE in event_values:
            self.type = EVENT_TYPE_PROGRAM_CHANGE
            self.program_change = event_values[EVENT_PROGRAM_CHANGE]
            self.channel = event_values[EVENT_CHANNEL]

        elif EVENT_OSC_ADDRESS in event_values:
            self.type = EVENT_TYPE_OSC
            self.osc_address = event_values[EVENT_OSC_ADDRESS]
            self.osc_params = {}
            if EVENT_OSC_PARAMS in event_values:
                if not isinstance(event_values[EVENT_OSC_PARAMS], Iterable):
                    raise ValueError("OSC params must be an iterable")
                self.osc_params = list(event_values[EVENT_OSC_PARAMS])

        elif EVENT_SUPERCOLLIDER_SYNTH in event_values:
            self.type = EVENT_TYPE_SUPERCOLLIDER
            self.synth_name = event_values[EVENT_SUPERCOLLIDER_SYNTH]
            self.synth_params = {}
            if EVENT_SUPERCOLLIDER_SYNTH_PARAMS in event_values:
                if not isinstance(event_values[EVENT_SUPERCOLLIDER_SYNTH_PARAMS], dict):
                    raise ValueError("SuperCollider params must be a dict")
                self.synth_params = event_values[EVENT_SUPERCOLLIDER_SYNTH_PARAMS]

        elif EVENT_NOTE in event_values:
            self.type = EVENT_TYPE_NOTE
            self.note = event_values[EVENT_NOTE]
            self.amplitude = event_values[EVENT_AMPLITUDE]
            self.gate = event_values[EVENT_GATE]
            self.channel = event_values[EVENT_CHANNEL]

        else:
            possible_event_types = [EVENT_NOTE, EVENT_DEGREE, EVENT_ACTION, EVENT_PATCH, EVENT_CONTROL,
                                    EVENT_PROGRAM_CHANGE, EVENT_OSC_ADDRESS]
            raise InvalidEventException("No event type specified (must provide one of %s)" % possible_event_types)

        self.duration = event_values[EVENT_DURATION]
        self.active = event_values[EVENT_ACTIVE]
        self.fields = event_values

class CustEventx():

    def __init__(self, event_values):
        for key in event_values.keys():
            if key not in ALL_EVENT_PARAMETERS:
                raise ValueError("Invalid key for event: %s" % (key))

        parm = list(set([EVENT_NOTE, EVENT_ACTION, EVENT_DEGREE]) & set(event_values))
        if len(parm) >= 2:
            raise InvalidEventException(f"Cannot specify both '{parm[0]}' 'and '{parm[1]}'")

        event_values.setdefault(EVENT_ACTIVE, True)
        event_values.setdefault(EVENT_CHANNEL, DEFAULT_EVENT_CHANNEL)
        event_values.setdefault(EVENT_DURATION, DEFAULT_EVENT_DURATION)
        event_values.setdefault(EVENT_GATE, DEFAULT_EVENT_GATE)
        event_values.setdefault(EVENT_AMPLITUDE, DEFAULT_EVENT_AMPLITUDE)
        event_values.setdefault(EVENT_OCTAVE, DEFAULT_EVENT_OCTAVE)
        event_values.setdefault(EVENT_TRANSPOSE, DEFAULT_EVENT_TRANSPOSE)
        event_values.setdefault(EVENT_SCALE, Scale.default)

        if EVENT_NOTE in event_values and EVENT_DEGREE in event_values:
            raise InvalidEventException("Cannot specify both note and degree")

        #------------------------------------------------------------------------
        # Note/degree/etc: Send a MIDI note
        #------------------------------------------------------------------------
        if EVENT_DEGREE in event_values:
            degree = event_values[EVENT_DEGREE]
            if degree is None:
                event_values[EVENT_NOTE] = None
            else:
                if EVENT_KEY in event_values:
                    key = event_values[EVENT_KEY]
                else:
                    key = Key(0, event_values[EVENT_SCALE])

                #----------------------------------------------------------------------
                # handle lists of notes (eg chords).
                # TODO: create a class which allows for scalars and arrays to handle
                # addition transparently
                #----------------------------------------------------------------------
                try:
                    event_values[EVENT_NOTE] = [key[n] for n in degree]
                except TypeError:
                    event_values[EVENT_NOTE] = key[degree]

        #----------------------------------------------------------------------
        # For cases in which we want to introduce a rest, set amplitude
        # to zero. This means that we can still send rest events to
        # devices which receive all generic events (useful to display rests
        # when rendering a score).
        #----------------------------------------------------------------------
        if EVENT_NOTE in event_values:
            if event_values[EVENT_NOTE] is None:
                #----------------------------------------------------------------------
                # Rest.
                #----------------------------------------------------------------------
                event_values[EVENT_NOTE] = 0
                event_values[EVENT_AMPLITUDE] = 0
                event_values[EVENT_GATE] = 0
            else:
                #----------------------------------------------------------------------
                # Handle lists of notes (eg chords).
                # TODO: create a class which allows for scalars and arrays to handle
                #       addition transparently.
                #
                # The below does not allow for event_values[EVENT_TRANSPOSE] to be an array,
                # for example.
                #----------------------------------------------------------------------
                try:
                    event_values[EVENT_NOTE] = [note +
                                                event_values[EVENT_OCTAVE] * 12 +
                                                event_values[EVENT_TRANSPOSE] for note in event_values[EVENT_NOTE]]
                except TypeError:
                    event_values[EVENT_NOTE] += event_values[EVENT_OCTAVE] * 12 + event_values[EVENT_TRANSPOSE]

        #----------------------------------------------------------------------
        # Classify the event type.
        #----------------------------------------------------------------------
        if EVENT_ACTION in event_values:
            self.type = EVENT_TYPE_ACTION
            self.action = event_values[EVENT_ACTION]
            self.args = {}
            if EVENT_ACTION_ARGS in event_values:
                self.args = dict((key, Pattern.value(value)) for key, value in event_values[EVENT_ACTION_ARGS].items())
        # elif EVENT_TIME in event_values:
        #     pass
        # elif EVENT_PATCH in event_values:
        #     self.type = EVENT_TYPE_PATCH
        #     self.patch = event_values[EVENT_PATCH]
        #     self.params = {}
        #     if EVENT_PATCH_PARAMS in event_values:
        #         self.params = event_values[EVENT_PATCH_PARAMS]

        elif EVENT_CONTROL in event_values:
            self.type = EVENT_TYPE_CONTROL
            self.control = event_values[EVENT_CONTROL]
            self.value = event_values[EVENT_VALUE]
            self.channel = event_values[EVENT_CHANNEL]

        elif EVENT_PROGRAM_CHANGE in event_values:
            # TODO: Implement program changes
            self.type = EVENT_TYPE_PROGRAM_CHANGE

        elif EVENT_OSC_ADDRESS in event_values:
            self.type = EVENT_TYPE_OSC
            self.osc_address = event_values[EVENT_OSC_ADDRESS]
            self.osc_params = {}
            if EVENT_OSC_PARAMS in event_values:
                if not isinstance(event_values[EVENT_OSC_PARAMS], Iterable):
                    raise ValueError("OSC params must be an iterable")
                self.osc_params = list(event_values[EVENT_OSC_PARAMS])

        elif EVENT_SUPERCOLLIDER_SYNTH in event_values:
            self.type = EVENT_TYPE_SUPERCOLLIDER
            self.synth_name = event_values[EVENT_SUPERCOLLIDER_SYNTH]
            self.synth_params = {}
            if EVENT_SUPERCOLLIDER_SYNTH_PARAMS in event_values:
                if not isinstance(event_values[EVENT_SUPERCOLLIDER_SYNTH_PARAMS], dict):
                    raise ValueError("SuperCollider params must be a dict")
                self.synth_params = event_values[EVENT_SUPERCOLLIDER_SYNTH_PARAMS]

        elif EVENT_NOTE in event_values or EVENT_DEGREE in event_values:
            self.type = EVENT_TYPE_NOTE
            self.note = event_values[EVENT_NOTE]
            self.amplitude = event_values[EVENT_AMPLITUDE]
            self.gate = event_values[EVENT_GATE]
            self.channel = event_values[EVENT_CHANNEL]

        else:
            possible_event_types = [EVENT_NOTE, EVENT_DEGREE, EVENT_ACTION, EVENT_PATCH, EVENT_CONTROL,
                                    EVENT_PROGRAM_CHANGE, EVENT_OSC_ADDRESS]
            raise InvalidEventException("No event type specified (must provide one of %s)" % possible_event_types)

        self.duration = event_values[EVENT_DURATION]
        self.active = event_values[EVENT_ACTIVE]
        self.fields = event_values
