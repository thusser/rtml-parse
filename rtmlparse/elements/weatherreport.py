from lxml import etree

from .baseelement import BaseElement


class WeatherReport(BaseElement):
    def __init__(self, parent, name=None, uid=None):
        BaseElement.__init__(self, 'WeatherReport', parent, name=name, uid=uid)
