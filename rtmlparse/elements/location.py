from lxml import etree

from .baseelement import BaseElement
from .misc import auto_attr_check


@auto_attr_check
class Location(BaseElement):
    EastLongitude = float
    Latitude = float
    Height = float
    TimeZone = int

    def __init__(self, parent, name=None, uid=None, lon=None, lat=None, height=None, timezone=None):
        BaseElement.__init__(self, 'Location', parent, name=name, uid=uid)
        self.EastLongitude = lon
        self.Latitude = lat
        self.Height = height
        self.TimeZone = timezone

    def to_xml(self, parent, add_children=True):
        # add element
        element = BaseElement.to_xml(self, parent, add_children=add_children)
        if element is None:
            return None

        # other stuff
        self.add_text_value(element, 'EastLongitude', self.EastLongitude, attrib={'units': 'degrees'})
        self.add_text_value(element, 'Latitude', self.Latitude, attrib={'units': 'degrees'})
        self.add_text_value(element, 'Height', self.Height, attrib={'units': 'meters'})
        self.add_text_value(element, 'TimeZone', self.TimeZone)

        # return base element
        return element

    def from_xml(self, element, rtml):
        # base call
        BaseElement.from_xml(self, element, rtml)
        ns = '{' + rtml.namespace + '}'

        # other stuff
        self.EastLongitude = self.from_text_value(element, 'EastLongitude', float, namespace=ns)
        self.Latitude = self.from_text_value(element, 'Latitude', float, namespace=ns)
        self.Height = self.from_text_value(element, 'Height', float, namespace=ns)
        self.TimeZone = self.from_text_value(element, 'TimeZone', int, namespace=ns)

