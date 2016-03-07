from lxml import etree

from .baseelement import BaseElement


class SlitMask(BaseElement):
    def __init__(self, parent, name=None, uid=None):
        # BaseElement
        import rtmlparse.elements as e
        BaseElement.__init__(self, 'SlitMask', parent, name=None, uid=uid,
                             valid_element_types=[e.Slit])
