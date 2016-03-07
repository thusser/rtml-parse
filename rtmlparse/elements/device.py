from lxml import etree

from .baseelement import BaseElement


class Device(BaseElement):
    def __init__(self, parent, name=None, uid=None):
        BaseElement.__init__(self, 'Device', parent, name=name, uid=uid)
