from lxml import etree

from .baseelement import BaseElement


class Scoring(BaseElement):
    def __init__(self, parent, name=None, uid=None):
        BaseElement.__init__(self, 'Scoring', parent, name=name, uid=uid)
