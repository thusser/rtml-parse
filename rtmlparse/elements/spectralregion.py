from lxml import etree
from enum import Enum

from .baseelement import BaseElement
from .misc import auto_attr_check


class SpectralRegionTypes(Enum):
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


@auto_attr_check
class SpectralRegion(BaseElement):
    Type = SpectralRegionTypes

    def __init__(self, parent, name=None, uid=None, description=None, uri=None, data=None,
                 type=SpectralRegionTypes.other):
        BaseElement.__init__(self, 'SpectralRegion', parent, name=None, uid=uid)
        self.Type = type

    def to_xml(self, parent):
        # add element
        element = BaseElement.to_xml(self, parent)
        if element is None:
            return None
        # set text and return element
        element.text = self.Type.value
        return element

    def from_xml(self, element, rtml):
        BaseElement.from_xml(self, element, rtml)
        self.Type = SpectralRegionTypes(element.text)
