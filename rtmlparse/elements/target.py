from lxml import etree

from .baseelement import BaseElement
from .misc import auto_attr_check, CoordinatesAccess


@auto_attr_check
class Target(BaseElement, CoordinatesAccess):
    TargetBrightness = float

    def __init__(self, parent, name=None, uid=None):
        import rtmlparse.elements as e
        BaseElement.__init__(self, 'Target', parent, name=name, uid=uid, valid_element_types=[e.Coordinates])
        self.TargetBrightness = None

    def to_xml(self, parent, add_children=True):
        # add element
        element = BaseElement.to_xml(self, parent, add_children=add_children)
        if element is None:
            return None
        ns = '{' + self.rtml.namespace + '}'

        # magnitude
        if self.TargetBrightness is not None:
            brightness = etree.SubElement(element, ns + 'TargetBrightness')
            etree.SubElement(brightness, ns + 'Magnitude').text = '{0:.2f}'.format(self.TargetBrightness)
            etree.SubElement(brightness, ns + 'Type').text = 'V'

        # return base element
        return element

    def from_xml(self, xml, rtml):
        # base call
        BaseElement.from_xml(self, xml, rtml)
        ns = '{' + rtml.namespace + '}'

        # magnitude
        mag = xml.find(ns + 'TargetBrightness')
        if mag is not None:
            self.TargetBrightness = float(mag.find(ns + 'Magnitude').text)
