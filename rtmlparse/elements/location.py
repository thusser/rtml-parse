from lxml import etree

from .baseelement import BaseElement


class Location(BaseElement):
    def __init__(self, parent, name=None, uid=None):
        BaseElement.__init__(self, 'Location', parent, name=name, uid=uid)
        self.EastLongitude = None
        self.Latitude = None
        self.Height = None
        self.TimeZone = None

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
        self.EastLongitude = self.from_text_value(element, ns + 'EastLongitude', float)
        self.Latitude = self.from_text_value(element, ns + 'Latitude', float)
        self.Height = self.from_text_value(element, ns + 'Height', float)
        self.TimeZone = self.from_text_value(element, ns + 'TimeZone', int)

