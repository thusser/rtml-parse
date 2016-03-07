from lxml import etree

from .baseelement import BaseElement


class Calibration(BaseElement):
    def __init__(self, parent, name=None, uid=None):
        BaseElement.__init__(self, 'Calibration', parent, name=name, uid=uid)
