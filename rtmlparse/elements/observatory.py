from lxml import etree

from .baseelement import BaseElement


class Observatory(BaseElement):
    def __init__(self, parent, name=None, uid=None):
        BaseElement.__init__(self, 'Observatory', parent, name=name, uid=uid)

