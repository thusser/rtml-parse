from lxml import etree

from .baseelement import BaseElement


class Windowing(BaseElement):
    def __init__(self, parent, name=None, uid=None):
        # BaseElement
        import rtmlparse.elements as e
        BaseElement.__init__(self, 'Windowing', parent, name=None, uid=uid, valid_element_types=[e.Window])
