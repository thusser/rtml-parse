from lxml import etree

from .baseelement import BaseElement


class Grating(BaseElement):
    def __init__(self, parent, name=None, uid=None):
        BaseElement.__init__(self, 'Grating', parent, name=name, uid=uid)
        self.Angle = None

    def to_xml(self, parent, add_children=True):
        # add element
        element = BaseElement.to_xml(self, parent, add_children=add_children)
        if element is None:
            return None

        # grating angle
        if self.Angle is not None:
            angle = etree.SubElement(element, 'BlazeAngle')
            angle.text = "{0:.3f}".format(self.Angle)

        # return base element
        return element

    def from_xml(self, xml, rtml):
        # base call
        BaseElement.from_xml(self, xml, rtml)
        ns = '{' + rtml.namespace + '}'

        # grating angle
        angle = xml.find(ns + 'BlazeAngle')
        if angle is not None:
            self.Angle = float(angle.text)
