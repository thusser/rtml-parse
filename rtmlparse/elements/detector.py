from lxml import etree

from .baseelement import BaseElement


class Detector(BaseElement):
    def __init__(self, parent, name=None, uid=None):
        BaseElement.__init__(self, 'Detector', parent, name=name, uid=uid)
        self.Binning = None
        self.ColumnPixelSize = None
        self.Description = None
        self.NumColumns = None
        self.NumRows = None
        self.PixelRadius = None
        self.PixelSize = None
        self.PositionAngle = None

    def to_xml(self, parent, add_children=True):
        # add element
        element = BaseElement.to_xml(self, parent, add_children=add_children)
        if element is None:
            return None

        # other stuff
        self.add_xy_value(element, 'Binning', self.Binning)
        self.add_text_value(element, 'ColumnPixelSize', self.ColumnPixelSize, '.8f', attrib={'units': 'micrometers'})
        self.add_text_value(element, 'Description', self.Description)
        self.add_text_value(element, 'NumColumns', self.NumColumns, 'd')
        self.add_text_value(element, 'NumRows', self.NumRows, 'd')
        self.add_text_value(element, 'PixelRadius', self.PixelRadius, attrib={'units': 'micrometers'})
        self.add_text_value(element, 'PixelSize', self.PixelSize, attrib={'units': 'micrometers'})
        self.add_text_value(element, 'PositionAngle', self.PositionAngle, attrib={'units': 'degrees'})

        # return base element
        return element

    def from_xml(self, element, rtml):
        # base call
        BaseElement.from_xml(self, element, rtml)
        ns = '{' + rtml.namespace + '}'

        # other stuff
        self.Binning = self.from_xy_value(element, 'Binning', ns + 'X', ns + 'Y')
        self.ColumnPixelSize = self.from_text_value(element, ns + 'ColumnPixelSize', float)
        self.Description = self.from_text_value(element, ns + 'Description', str)
        self.NumColumns = self.from_text_value(element, ns + 'NumColumns', int)
        self.NumRows = self.from_text_value(element, ns + 'NumRows', int)
        self.PixelRadius = self.from_text_value(element, ns + 'PixelRadius', float)
        self.PixelSize = self.from_text_value(element, ns + 'PixelSize', float)
        self.PositionAngle = self.from_text_value(element, ns + 'PositionAngle', float)
