from isobar import Key
from isobar import Scale, InvalidKeyException,  note_name_to_midi_note


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

        semitone = self.scale.get(degree, scale_down=scale_down)
        return semitone + self.tonic

    def nearest_note(self, *args, ** kwargs):
        """ Return the index of the given note within this scale. """
        parms = {"note": None,
        "scale_down": False}
        if hasattr(self, 'scale_down'):
            parms['scale_down'] = self.scale_down
        for idx, arg in enumerate(args):
            parms[list(parms.keys())[idx]] = arg
        if kwargs is not None:
            parms.update(kwargs)

        note = parms.get('note')

        scale_down = parms.get('scale_down')
        if scale_down and hasattr(self.scale, 'semitones_down') and self.scale.semitones_down:
            semitones = self.scale.semitones_down
        else:
            semitones = self.scale.semitones
        # if note in self:
        if self.__contains__(semitone=note, scale_down=scale_down):
            return note
        else:
            octave, pitch = divmod(note, self.scale.octave_size)
            nearest_semi = None
            nearest_dist = None
            calc_octave = octave
            for semi in semitones:
                dist = min(abs(semi - pitch),abs(abs(semi-pitch)-self.scale.octave_size))
                if nearest_dist is None or dist < nearest_dist:
                    nearest_semi = semi
                    nearest_dist = dist
                    if dist == abs(abs(semi-pitch)-self.scale.octave_size):
                        calc_octave = octave +1
                    else:
                        calc_octave = octave
            octave = calc_octave
            return (octave * self.scale.octave_size) + nearest_semi

    def __contains__(self, *args, ** kwargs):
        """ Return the index of the given note within this scale. """
        parms = {"note": None,
        "scale_down": False}
        if hasattr(self, 'scale_down'):
            parms['scale_down'] = self.scale_down
        for idx, arg in enumerate(args):
            parms[list(parms.keys())[idx]] = arg
        if kwargs is not None:
            parms.update(kwargs)

        semitone = parms.get('semitone')
        scale_down = parms.get('scale_down')
        if scale_down and hasattr(self.scale, 'semitones_down') and self.scale.semitones_down:
            semitones = self.semitones_down
        else:
            semitones = self.semitones

        if semitone is None:
            return True
        return (semitone % self.scale.octave_size) in semitones

    @property
    def semitones_down(self):
        semitones_down = [(n + self.tonic) % self.scale.octave_size for n in self.scale.semitones_down]
        semitones_down.sort()
        return semitones_down
