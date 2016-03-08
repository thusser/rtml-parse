from lxml import etree

from .baseelement import BaseElement
from .misc import SpectralEfficiencyAccess, SpectralRegionAccess, auto_attr_check


@auto_attr_check
class Window(BaseElement, SpectralEfficiencyAccess, SpectralRegionAccess):
    #LowerLeft = str
    #UpperRight = float

    def __init__(self, parent, name=None, uid=None):
        # BaseElement
        BaseElement.__init__(self, 'Window', parent, name=name, uid=uid)

        # Camera
        self.LowerLeft = None
        self.UpperRight = None

    def to_xml(self, parent, add_children=True):
        # add element
        element = BaseElement.to_xml(self, parent, add_children=add_children)
        if element is None:
            return None
        ns = '{' + self.rtml.namespace + '}'

        # other stuff
        self.add_xy_value(element, 'LowerLeft', self.LowerLeft, namespace=ns)
        self.add_xy_value(element, 'UpperRight', self.UpperRight, namespace=ns)

        # return base element
        return element

    def from_xml(self, element, rtml):
        # base call
        BaseElement.from_xml(self, element, rtml)
        ns = '{' + rtml.namespace + '}'

        # other stuff
        self.LowerLeft = self.from_xy_value(element, 'LowerLeft', namespace=ns)
        self.UpperRight = self.from_xy_value(element, 'UpperRight', namespace=ns)
