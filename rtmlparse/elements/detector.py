from lxml import etree

from .baseelement import BaseElement
from .misc import auto_attr_check, SpectralEfficiencyAccess, SpectralRegionAccess, WindowingAccess


@auto_attr_check
class Detector(BaseElement, SpectralEfficiencyAccess, SpectralRegionAccess, WindowingAccess):
    # TODO: type for Binning
    Capacity = float
    ColumnPixelSize = float
    Description = str
    NumColumns = int
    NumRows = int
    PixelRadius = float
    PixelSize = float
    PositionAngle = float
    RowPixelSize = float

    def __init__(self, parent, name=None, uid=None):
        # BaseElement
        import rtmlparse.elements as e
        BaseElement.__init__(self, 'Detector', parent, name=name, uid=uid,
                             valid_element_types=[e.Bias, e.DarkCurrent, e.FlatField, e.Gain, e.SpectralEfficiency,
                                                  e.SpectralRegion, e.ReadoutNoise, e.Windowing])

        # Detector
        self.Binning = None
        self.Capacity = None
        self.ColumnPixelSize = None
        self.Description = None
        self.NumColumns = None
        self.NumRows = None
        self.PixelRadius = None
        self.PixelSize = None
        self.PositionAngle = None
        self.RowPixelSize = None

    def to_xml(self, parent, add_children=True):
        # add element
        element = BaseElement.to_xml(self, parent, add_children=add_children)
        if element is None:
            return None
        ns = '{' + self.rtml.namespace + '}'

        # other stuff
        self.add_xy_value(element, 'Binning', self.Binning, namespace=ns)
        self.add_text_value(element, 'Capacity', self.Capacity, 'f', attrib={'units': 'adu'}, namespace=ns)
        self.add_text_value(element, 'ColumnPixelSize', self.ColumnPixelSize, 'f', attrib={'units': 'micrometers'},
                            namespace=ns)
        self.add_text_value(element, 'Description', self.Description, namespace=ns)
        self.add_text_value(element, 'NumColumns', self.NumColumns, 'd', namespace=ns)
        self.add_text_value(element, 'NumRows', self.NumRows, 'd', namespace=ns)
        self.add_text_value(element, 'PixelRadius', self.PixelRadius, attrib={'units': 'micrometers'}, namespace=ns)
        self.add_text_value(element, 'PixelSize', self.PixelSize, attrib={'units': 'micrometers'}, namespace=ns)
        self.add_text_value(element, 'PositionAngle', self.PositionAngle, attrib={'units': 'degrees'}, namespace=ns)
        self.add_text_value(element, 'RowPixelSize', self.ColumnPixelSize, 'f', attrib={'units': 'micrometers'},
                            namespace=ns)

        # return base element
        return element

    def from_xml(self, element, rtml):
        # base call
        BaseElement.from_xml(self, element, rtml)
        ns = '{' + rtml.namespace + '}'

        # other stuff
        self.Binning = self.from_xy_value(element, 'Binning', namespace=ns)
        self.Capacity = self.from_text_value(element, 'Capacity', float, namespace=ns)
        self.ColumnPixelSize = self.from_text_value(element, 'ColumnPixelSize', float, namespace=ns)
        self.Description = self.from_text_value(element, 'Description', str, namespace=ns)
        self.NumColumns = self.from_text_value(element, 'NumColumns', int, namespace=ns)
        self.NumRows = self.from_text_value(element, 'NumRows', int, namespace=ns)
        self.PixelRadius = self.from_text_value(element, 'PixelRadius', float, namespace=ns)
        self.PixelSize = self.from_text_value(element, 'PixelSize', float, namespace=ns)
        self.PositionAngle = self.from_text_value(element, 'PositionAngle', float, namespace=ns)
        self.RowPixelSize = self.from_text_value(element, 'RowPixelSize', float, namespace=ns)

    def add_element(self, element):
        # allow adding of windows directly by explicitely creating a Windowing element first
        from .window import Window
        from .windowing import Windowing
        if isinstance(element, Window):
            # if there is no Windowing element, create one
            wnd = self.Windowing
            if wnd is None:
                wnd = Windowing(self)
            # add element
            wnd.add_element(element)
            return

        # default behaviour
        BaseElement.add_element(self, element)
