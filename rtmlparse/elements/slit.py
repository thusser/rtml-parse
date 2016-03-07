from lxml import etree

from .baseelement import BaseElement


class Slit(BaseElement):
    def __init__(self, parent, name=None, uid=None):
        BaseElement.__init__(self, 'Slit', parent, name=name, uid=uid)
        self.positionAngle = 0.
        self.width = 10.
        self.length = 10.

    def to_xml(self, parent, add_children=True):
        # add slit
        element = BaseElement.to_xml(self, parent, add_children=add_children)
        if element is None:
            return None

        # position angle
        etree.SubElement(element, 'PositionAngle').text = '{0:.2f}'.format(self.positionAngle)

        # width/length
        size = etree.SubElement(element, 'WidthLength')
        etree.SubElement(size, 'X').text = '{0:.2f}'.format(self.width)
        etree.SubElement(size, 'Y').text = '{0:.2f}'.format(self.length)

        # return base element
        return element

    def from_xml(self, xml, rtml):
        # base call
        BaseElement.from_xml(self, xml, rtml)
        ns = '{' + rtml.namespace + '}'

        # grating angle
        angle = xml.find(ns + 'PositionAngle')
        if angle is not None:
            self.positionAngle = float(angle.text)
