from lxml import etree

from .baseelement import BaseElement
from .misc import auto_attr_check


@auto_attr_check
class Bias(BaseElement):
    Base64Data = str
    Description = str
    Uri = str
    Value = float

    def __init__(self, parent, name=None, uid=None):
        # BaseElement
        BaseElement.__init__(self, 'Bias', parent, name=name, uid=uid)

        # Bias
        self.Base64Data = None
        self.Description = None
        self.Uri = None
        self.Value = None

    def to_xml(self, parent, add_children=True):
        # add element
        element = BaseElement.to_xml(self, parent, add_children=add_children)
        if element is None:
            return None
        ns = '{' + self.rtml.namespace + '}'

        # other stuff
        self.add_text_value(element, 'Base64Data', self.Base64Data, namespace=ns)
        self.add_text_value(element, 'Description', self.Description, namespace=ns)
        self.add_text_value(element, 'Uri', self.Uri, namespace=ns)
        self.add_text_value(element, 'Value', self.Value, 'f', attrib={'units': 'adu'}, namespace=ns)

        # return base element
        return element

    def from_xml(self, element, rtml):
        # base call
        BaseElement.from_xml(self, element, rtml)
        ns = '{' + rtml.namespace + '}'

        # other stuff
        self.Base64Data = self.from_text_value(element, 'Base64Data', str, namespace=ns)
        self.Description = self.from_text_value(element, 'Description', str, namespace=ns)
        self.Uri = self.from_text_value(element, 'Uri', str, namespace=ns)
        self.Value = self.from_text_value(element, 'Value', float, namespace=ns)

