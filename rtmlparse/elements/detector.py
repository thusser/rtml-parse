from lxml import etree

from .baseelement import BaseElement
from .misc import auto_attr_check


@auto_attr_check
class Detector(BaseElement):
    ColumnPixelSize = float
    Description = str
    NumColumns = int
    NumRows = int
    PixelRadius = float
    PixelSize = float
    PositionAngle = float

    def __init__(self, parent, name=None, uid=None):
        import rtmlparse.elements as e
        BaseElement.__init__(self, 'Detector', parent, name=name, uid=uid, valid_element_types=[e.Bias])
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
        ns = '{' + self.rtml.namespace + '}'

        # other stuff
        self.add_xy_value(element, 'Binning', self.Binning, namespace=ns)
        self.add_text_value(element, 'ColumnPixelSize', self.ColumnPixelSize, '.8f', attrib={'units': 'micrometers'},
                            namespace=ns)
        self.add_text_value(element, 'Description', self.Description, namespace=ns)
        self.add_text_value(element, 'NumColumns', self.NumColumns, 'd', namespace=ns)
        self.add_text_value(element, 'NumRows', self.NumRows, 'd', namespace=ns)
        self.add_text_value(element, 'PixelRadius', self.PixelRadius, attrib={'units': 'micrometers'}, namespace=ns)
        self.add_text_value(element, 'PixelSize', self.PixelSize, attrib={'units': 'micrometers'}, namespace=ns)
        self.add_text_value(element, 'PositionAngle', self.PositionAngle, attrib={'units': 'degrees'}, namespace=ns)

        # return base element
        return element

    def from_xml(self, element, rtml):
        # base call
        BaseElement.from_xml(self, element, rtml)
        ns = '{' + rtml.namespace + '}'

        # other stuff
        self.Binning = self.from_xy_value(element, 'Binning', namespace=ns)
        self.ColumnPixelSize = self.from_text_value(element, 'ColumnPixelSize', float, namespace=ns)
        self.Description = self.from_text_value(element, 'Description', str, namespace=ns)
        self.NumColumns = self.from_text_value(element, 'NumColumns', int, namespace=ns)
        self.NumRows = self.from_text_value(element, 'NumRows', int, namespace=ns)
        self.PixelRadius = self.from_text_value(element, 'PixelRadius', float, namespace=ns)
        self.PixelSize = self.from_text_value(element, 'PixelSize', float, namespace=ns)
        self.PositionAngle = self.from_text_value(element, 'PositionAngle', float, namespace=ns)
