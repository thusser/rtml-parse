from lxml import etree

from .baseelement import BaseElement


class Project(BaseElement):
    def __init__(self, parent, name=None, uid=None):
        BaseElement.__init__(self, 'Project', parent, name=name, uid=uid)
