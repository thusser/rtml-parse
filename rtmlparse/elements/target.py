from lxml import etree

from .baseelement import BaseElement
from .misc import auto_attr_check


@auto_attr_check
class Target(BaseElement):
    RightAscension = float
    Declination = float
    TargetBrightness = float

    def __init__(self, parent, name=None, uid=None):
        BaseElement.__init__(self, 'Target', parent, name=name, uid=uid)
        self.RightAscension = None
        self.Declination = None
        self.TargetBrightness = None

    def to_xml(self, parent, add_children=True):
        # add element
        element = BaseElement.to_xml(self, parent, add_children=add_children)
        if element is None:
            return None

        # set coordinates
        if self.RightAscension is not None and self.Declination is not None:
            coords = etree.SubElement(element, 'Coordinates')
            ra = etree.SubElement(coords, 'RightAscension')
            etree.SubElement(ra, 'Value').text = '{0:.8f}'.format(self.RightAscension)
            dec = etree.SubElement(coords, 'Declination')
            etree.SubElement(dec, 'Value').text = '{0:.8f}'.format(self.Declination)

        # magnitude
        if self.TargetBrightness is not None:
            brightness = etree.SubElement(element, 'TargetBrightness')
            etree.SubElement(brightness, 'Magnitude').text = '{0:.2f}'.format(self.TargetBrightness)
            etree.SubElement(brightness, 'Type').text = 'V'

        # return base element
        return element

    def from_xml(self, xml, rtml):
        # base call
        BaseElement.from_xml(self, xml, rtml)
        ns = '{' + rtml.namespace + '}'

        # coordinates
        coords = xml.find(ns + 'Coordinates')
        if coords is not None:
            self.RightAscension = float(coords.find(ns + 'RightAscension').find(ns + 'Value').text)
            self.Declination = float(coords.find(ns + 'Declination').find(ns + 'Value').text)

        # magnitude
        mag = xml.find(ns + 'TargetBrightness')
        if mag is not None:
            self.TargetBrightness = float(mag.find(ns + 'Magnitude').text)
