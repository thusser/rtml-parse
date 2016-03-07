from lxml import etree

from .baseelement import BaseElement


class Exposure(BaseElement):
    def __init__(self, parent, name=None, uid=None):
        BaseElement.__init__(self, 'Exposure', parent, name=name, uid=uid)
        self.Description = None
        self.Count = None
        self.Exposures = []

    def to_xml(self, parent, add_children=True):
        # add element
        element = BaseElement.to_xml(self, parent, add_children=add_children)
        if element is None:
            return None

        # count
        if self.Count is not None:
            element.attrib['count'] = '{0:d}'.format(self.Count)

        # description
        if self.Description is not None:
            etree.SubElement(element, 'Description').text = self.Description

        # exposures
        for exposure in self.Exposures:
            value = etree.SubElement(element, 'Value')
            value.attrib['units'] = 'seconds'
            value.text = '{0:.3f}'.format(exposure)

        # return base element
        return element

    def from_xml(self, element, rtml):
        # base call
        BaseElement.from_xml(self, element, rtml)
        ns = '{' + rtml.namespace + '}'

        # count
        self.Count = int(element.attrib['count']) if 'count' in element.attrib else None

        # description
        desc = element.find(ns + 'Description')
        self.Description = desc.text if desc is not None else None

        # exposures
        self.Exposures = []
        for exp in element.findall(ns + 'Value'):
            self.Exposures.append(float(exp.text))

