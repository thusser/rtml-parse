from lxml import etree
from datetime import datetime

from .baseelement import BaseElement


class History(BaseElement):
    def __init__(self, parent, name=None, uid=None):
        import rtmlparse.elements as e
        BaseElement.__init__(self, 'History', parent, name=None, uid=None, valid_element_types=[e.Entry])

