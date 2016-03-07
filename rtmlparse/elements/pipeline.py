from lxml import etree

from .baseelement import BaseElement


class Pipeline(BaseElement):
    def __init__(self, parent, name=None, uid=None):
        BaseElement.__init__(self, 'Pipeline', parent, name=name, uid=uid)
