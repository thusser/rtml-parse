from lxml import etree

from .baseelement import BaseElement


class SpectralEfficiency(BaseElement):
    def __init__(self, parent, name=None, uid=None, description=None, uri=None, data=None):
        BaseElement.__init__(self, 'SpectralEfficiency', parent, name=None, uid=uid)
        self.Description = description
        self.Uri = uri
        self.Data = data

    def to_xml(self, parent):
        # add element
        element = BaseElement.to_xml(self, parent)
        if element is None:
            return None

        # other stuff
        self.add_text_value(element, 'Description', self.Description)
        self.add_text_value(element, 'Uri', self.Uri)

        # return base element
        return element

    def from_xml(self, element, rtml):
        # base call
        BaseElement.from_xml(self, element, rtml)
        ns = '{' + rtml.namespace + '}'

        # other stuff
        self.Description = self.from_text_value(element, 'Description', str, namespace=ns)
        self.Uri = self.from_text_value(element, 'Uri', str, namespace=ns)
