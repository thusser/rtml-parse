from lxml import etree

from .baseelement import BaseElement
from .misc import auto_attr_check, SpectralEfficiencyAccess, SpectralRegionAccess, SlitAccess, SlitMaskAccess


@auto_attr_check
class Spectrograph(BaseElement, SpectralEfficiencyAccess, SpectralRegionAccess, SlitAccess, SlitMaskAccess):
    Description = str
    PositionAngle = float

    def __init__(self, parent, name=None, uid=None):
        # BaseElement
        import rtmlparse.elements as e
        BaseElement.__init__(self, 'Spectrograph', parent, name=name, uid=uid,
                             valid_element_types=[e.Grating, e.Detector, e.Device, e.FilterWheel, e.Slit, e.Setup,
                                                  e.SpectralEfficiency, e.SpectralRegion, e.SlitMask])

        # Spectrograph
        self.Description = None
        self.PositionAngle = None

    def to_xml(self, parent, add_children=True):
        # add element
        element = BaseElement.to_xml(self, parent, add_children=add_children)
        if element is None:
            return None
        ns = '{' + self.rtml.namespace + '}'

        # other stuff
        self.add_text_value(element, 'Description', self.Description, namespace=ns)
        self.add_text_value(element, 'PositionAngle', self.PositionAngle, attrib={'units': 'degrees'}, namespace=ns)

        # return base element
        return element

    def from_xml(self, element, rtml):
        # base call
        BaseElement.from_xml(self, element, rtml)
        ns = '{' + rtml.namespace + '}'

        # other stuff
        self.Description = self.from_text_value(element, 'Description', str, namespace=ns)
        self.PositionAngle = self.from_text_value(element, 'PositionAngle', float, namespace=ns)
