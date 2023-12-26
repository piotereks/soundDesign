import typing

from isobar import PDegree, Pattern, PSeries

# import isobar as iso
from .up_down_scale import *


class UpDownPDegree(PDegree):
    """ PDegree: Map scale index <degree> to MIDI notes in <scale>.

        >>> p = PDegree(PSeries(0, 1), Scale.major)
        >>> p.nextn(16)
        [0, 2, 4, 5, 7, 9, 11, 12, 14, 16, 17, 19, 21, 23, 24, 26]
        """

    def __init__(self, degree, scale=Scale.major):
        dg_list = list(degree.copy())

        if dg_list != [None]:
            dg_list = [dg for dg in dg_list if dg is not None]
            scale_down = dg_list[0] > dg_list[-1]
        else:
            scale_down = False

        self.scale_down = scale_down
        self.degree = degree
        self.scale = scale

    def __next__(self):

        degree = Pattern.value(self.degree)
        scale = Pattern.value(self.scale)
        if degree is None:
            return None

        if isinstance(degree, typing.Iterable):
            return tuple(scale.get(degree, scale_down=self.scale_down) for degree in degree)
        else:
            return scale.get(degree, scale_down=self.scale_down)
