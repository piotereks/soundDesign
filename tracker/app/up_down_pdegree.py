from isobar import PDegree, Scale, Pattern
# import isobar as iso
from .up_down_scale import *
import typing
import inspect
from pprint import pprint

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
        if scale_down:
            print("scale down: True --------------------")
        else:
            print("scale down: False -------------------")

        self.scale_down = scale_down

        self.degree = degree
        self.scale = scale


    def __next__(self):

        degree = Pattern.value(self.degree)
        scale = Pattern.value(self.scale)
        if degree is None:
            return None
        # print(f'Degree new {degree=}, {self.scale_down=}, {scale.get(degree, scale_down=self.scale_down)=}')

        # dg_list = list(degree.copy())
        # scale_down = dg_list[0] > dg_list[-1]
        # if scale_down:
        #     print("scale down----------------------------")
        # self.scale_down = scale_down

        if isinstance(degree, typing.Iterable):
            # return tuple(scale[degree] for degree in degree)
            return tuple(scale.get(degree, scale_down=self.scale_down) for degree in degree)
        else:
            # return scale[degree]
            # return scale.get(degree, self.scale_down)
            # iso.Scale.get = UpDownScale.get
            # print(type(scale))
            # pprint(inspect.getmembers(scale.get))
            return scale.get(degree, scale_down=self.scale_down)