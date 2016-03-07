from lxml import etree
from enum import Enum

from .baseelement import BaseElement


class SpectralRegion(BaseElement):
    class Types(Enum):
        radio = "radio"
        millimeter = "millimeter"
        infrared = "infrared"
        optical = "optical"
        ultraviolet = "ultraviolet"
        extreme_ultraviolet = "extreme-ultraviolet"
        x_ray = "x-ray"
        gamma_ray = "gamma-ray"
        gravitational_wave = "gravitational wave"
        cosmos_ray = "cosmic ray"
        neutrino = "neutrino"
        other = "other"

    def __init__(self, parent, name=None, uid=None, description=None, uri=None, data=None,
                 type=Types.other):
        BaseElement.__init__(self, 'SpectralRegion', parent, name=None, uid=uid)
        self._type = type

    def to_xml(self, parent):
        # add element
        element = BaseElement.to_xml(self, parent)
        if element is None:
            return None
        # set text and return element
        element.text = self._type.value
        return element

    def from_xml(self, element, rtml):
        BaseElement.from_xml(self, element, rtml)
        self._type = SpectralRegion.Types(element.text)

    @property
    def Type(self):
        return self._type

    @Type.setter
    def Type(self, value):
        if isinstance(value, basestring):
            self._type = SpectralRegion.Types(basestring)
        elif isinstance(value, SpectralRegion.Types):
            self._type = value
        else:
            raise ValueError


