from isobar import Key
from isobar import Scale, InvalidKeyException,  note_name_to_midi_note

# from .scale import Scale
# from .note import Note
# from .util import midi_note_to_note_name, note_name_to_midi_note
# from .exceptions import InvalidKeyException

class UpDownKey(Key):
    """ Represents a harmonic structure, containing a tonic and scale.
    """

    def __init__(self, tonic=0, scale=Scale.major):

        if type(tonic) == str:
            tonic = note_name_to_midi_note(tonic)
        if type(scale) == str:
            scale = Scale.byname(scale)
        if tonic < 0:
            raise InvalidKeyException("Tonic must be >= 0")
        if tonic >= scale.octave_size:
            raise InvalidKeyException("Tonic cannot be beyond octave size")

        self.tonic = tonic
        self.scale = scale


    # def get(self, degree):
    def get(self,  *args, **kwargs):
        """ Returns the <degree>th semitone within this key. """
        # print("UpDownKey get")
        parms = {"degree": None,
                 "scale_down": False}
        for idx, arg in enumerate(args):
            parms[list(parms.keys())[idx]] = arg
        if kwargs is not None:
            parms.update(kwargs)
        degree = parms['degree']
        scale_down = parms['scale_down']
        if degree is None:
            return None

        # dg_list = list(degree.copy())
        # scale_down = dg_list[0] > dg_list[-1]
        # if scale_down:
        #     print("scale down----------------------------")
        # self.scale_down = scale_down

        # semitones = self.semitones_down if scale_down else self.semitones
        # semitone = self.scale[degree]
        semitone = self.scale.get(degree, scale_down=scale_down)
        return semitone + self.tonic

