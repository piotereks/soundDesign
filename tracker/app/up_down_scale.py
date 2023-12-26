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

    def get(self, *args, **kwargs):
        """ Retrieve the n'th degree of this scale. """
        parameters = {"n": None,
                      "scale_down": False}
        if hasattr(self, 'scale_down'):
            parameters['scale_down'] = self.scale_down
        for idx, arg in enumerate(args):
            parameters[list(parameters.keys())[idx]] = arg
        if kwargs is not None:
            parameters.update(kwargs)
        n = parameters['n']
        scale_down = parameters['scale_down']
        if n is None:
            return None
        semitones_down = None
        if hasattr(self, 'semitones_down'):
            semitones_down = self.semitones_down

        semitones = semitones_down if scale_down and semitones_down is not None else self.semitones
        octave = n // len(semitones)
        degree = n % len(semitones)
        semitone = semitones[degree]
        note = (self.octave_size * octave) + semitone
        return note

    def indexOf(self, *args, **kwargs):
        """ Return the index of the given note within this scale. """
        parameters = {"note": None,
                      "scale_down": False}
        if hasattr(self, 'scale_down'):
            parameters['scale_down'] = self.scale_down
        for idx, arg in enumerate(args):
            parameters[list(parameters.keys())[idx]] = arg
        if kwargs is not None:
            parameters.update(kwargs)
        scale_down = parameters.get('scale_down')
        if scale_down and hasattr(self, 'semitones_down') and self.semitones_down:
            semitones = self.semitones_down
        else:
            semitones = self.semitones

        note = parameters.get('note')
        octave = int(note / self.octave_size)
        index = octave * len(semitones)
        note -= octave * self.octave_size
        degree = 0

        while note > semitones[degree] and degree < len(semitones) - 1:
            degree += 1

        index += degree
        return index
