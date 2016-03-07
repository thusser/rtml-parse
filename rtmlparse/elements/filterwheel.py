from lxml import etree

from .baseelement import BaseElement


class FilterWheel(BaseElement):
    def __init__(self, parent, name=None, uid=None):
        # BaseElement
        import rtmlparse.elements as e
        BaseElement.__init__(self, 'FilterWheel', parent, name=None, uid=uid,
                             valid_element_types=[e.Filter, e.Detector])
