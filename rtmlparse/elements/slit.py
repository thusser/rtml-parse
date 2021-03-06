from lxml import etree

from .baseelement import BaseElement
from .misc import auto_attr_check


@auto_attr_check
class Slit(BaseElement):
    PositionAngle = float
    #WidthLength =

    def __init__(self, parent, name=None, uid=None, angle=None, width_length=None):
        BaseElement.__init__(self, 'Slit', parent, name=name, uid=uid)
        self.PositionAngle = angle
        self.WidthLength = width_length

    def to_xml(self, parent, add_children=True):
        # add slit
        element = BaseElement.to_xml(self, parent, add_children=add_children)
        if element is None:
            return None
        ns = '{' + self.rtml.namespace + '}'

        # other stuff
        self.add_text_value(element, 'PositionAngle', self.PositionAngle, 'f', namespace=ns)
        self.add_xy_value(element, 'WidthLength', self.WidthLength, namespace=ns)

        # return base element
        return element

    def from_xml(self, element, rtml):
        # base call
        BaseElement.from_xml(self, element, rtml)
        ns = '{' + rtml.namespace + '}'

        # other stuff
        self.PositionAngle = self.from_text_value(element, 'PositionAngle', float, namespace=ns)
        self.WidthLength = self.from_xy_value(element, 'WidthLength', namespace=ns)
