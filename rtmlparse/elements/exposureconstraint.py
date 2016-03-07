from lxml import etree

from .baseelement import BaseElement
from .misc import auto_attr_check


@auto_attr_check
class ExposureConstraint(BaseElement):
    Description = str
    Count = int
    MinimumSignalToNoise = float
    MaximumSignalToNoise = float

    def __init__(self, parent, name=None, uid=None):
        BaseElement.__init__(self, 'ExposureConstraint', parent, name=name, uid=uid)
        self.Description = None
        self.Count = None
        self.MinimumSignalToNoise = None
        self.MaximumSignalToNoise = None

    def to_xml(self, parent, add_children=True):
        # add element
        element = BaseElement.to_xml(self, parent, add_children=add_children)
        if element is None:
            return None

        # other fields
        self.add_text_value(element, 'Description', self.Description)
        self.add_text_value(element, 'Count', self.Count, 'd')
        self.add_text_value(element, 'MinimumSignalToNoise', self.MinimumSignalToNoise, '.2f')
        self.add_text_value(element, 'MaximumSignalToNoise', self.MaximumSignalToNoise, '.2f')

        # return base element
        return element

    def from_xml(self, xml, rtml):
        # base call
        BaseElement.from_xml(self, xml, rtml)
        ns = '{' + rtml.namespace + '}'

        # other fields
        self.Description = self.from_text_value(xml, 'Description', namespace=ns)
        self.Count = self.from_text_value(xml, 'Count', int, namespace=ns)
        self.MinimumSignalToNoise = self.from_text_value(xml, 'MinimumSignalToNoise', float, namespace=ns)
        self.MaximumSignalToNoise = self.from_text_value(xml, 'MaximumSignalToNoise', float, namespace=ns)
