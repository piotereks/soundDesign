from isobar import Scale


class UpDownScale(Scale):
    dict = {}

    def __init__(self, semitones=[0, 2, 4, 5, 7, 9, 11], name="unnamed scale", octave_size=12, semitones_down=None):
        self.scale_down = False

        self.semitones = semitones
        self.semitones_down = semitones_down
        """ For polymorphism with WeightedScale -- assume all notes equally weighted. """
        self.weights = [1.0 / len(self.semitones) for _ in range(len(self.semitones))]
        self.name = name
        self.octave_size = octave_size
        if name not in Scale.dict:
            Scale.dict[name] = self

    def __getitem__(self, key):
        return self.get(key)

    # def get(self, n, scale_down = False):
    def get(self, *args, **kwargs):
        """ Retrieve the n'th degree of this scale. """
        # print("UpDownScale get")
        parms = {"n": None,
                 "scale_down": self.scale_down}
        for idx, arg in enumerate(args):
            parms[list(parms.keys())[idx]] = arg
        if kwargs is not None:
            parms.update(kwargs)
        n = parms['n']
        scale_down = parms['scale_down']
        if n is None:
            return None
        semitones = self.semitones_down if scale_down and self.semitones_down is not None else self.semitones
        octave = n // len(semitones)
        degree = n % len(semitones)
        semitone = semitones[degree]
        note = (self.octave_size * octave) + semitone
        return note