from lxml import etree
import warnings

from .baseelement import BaseElement
from .misc import SpectralEfficiencyAccess, SpectralRegionAccess, auto_attr_check


@auto_attr_check
class Camera(BaseElement, SpectralEfficiencyAccess, SpectralRegionAccess):
    Description = str
    PlateScale = float

    def __init__(self, parent, name=None, uid=None):
        # BaseElement
        import rtmlparse.elements as e
        BaseElement.__init__(self, 'Camera', parent, name=name, uid=uid,
                             valid_element_types=[e.Detector, e.FilterWheel, e.Setup,
                                                  e.SpectralEfficiency, e.SpectralRegion])

        # Camera
        self.Description = None
        self.PlateScale = None

    def to_xml(self, parent, add_children=True):
        # add element
        element = BaseElement.to_xml(self, parent, add_children=add_children)
        if element is None:
            return None

        # other stuff
        self.add_text_value(element, 'Description', self.Description)
        self.add_text_value(element, 'PlateScale', self.PlateScale, attrib={'units': 'arcseconds per millimeter'})

        # return base element
        return element

    def from_xml(self, element, rtml):
        # base call
        BaseElement.from_xml(self, element, rtml)
        ns = '{' + rtml.namespace + '}'

        # other stuff
        self.Description = self.from_text_value(element, 'Description', str, namespace=ns)
        self.PlateScale = self.from_text_value(element, 'PlateScale', float, namespace=ns)
