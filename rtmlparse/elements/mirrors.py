from lxml import etree

from .baseelement import BaseElement
from .misc import auto_attr_check
from rtmlparse.misc import units


@auto_attr_check
class Mirrors(BaseElement):
    Number = int
    Coating = units.CoatingTypes

    def __init__(self, parent, name=None, uid=None, number=1, coating=units.CoatingTypes.aluminum):
        BaseElement.__init__(self, 'Mirrors', parent, name=name, uid=uid)
        self.Number = number
        self.Coating = coating

    def to_xml(self, parent):
        # add element
        element = BaseElement.to_xml(self, parent)
        if element is None:
            return None
        ns = '{' + self.rtml.namespace + '}'

        # other stuff
        self.add_text_value(element, 'Number', self.Number, 'd', namespace=ns)
        self.add_enum_value(element, 'Coating', self.Coating, namespace=ns)

        # return base element
        return element

    def from_xml(self, element, rtml):
        # base call
        BaseElement.from_xml(self, element, rtml)
        ns = '{' + rtml.namespace + '}'

        # other stuff
        self.Number = self.from_text_value(element, 'Number', int, namespace=ns)
        self.Coating = self.from_enum_value(element, 'Coating', units.CoatingTypes, namespace=ns)
