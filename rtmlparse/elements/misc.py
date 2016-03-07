from enum import Enum
from lxml import etree


class SpectralUnits(Enum):
    centimeters = "centimeters"
    eV = "eV"
    GeV = "GeV"
    gigahertz = "gigahertz"
    hertz = "hertz"
    keV = "keV"
    kilohertz = "kilohertz"
    megahertz = "megahertz"
    meters = "meters"
    MeV = "MeV"
    micrometers = "micrometers"
    millimeters = "millimeters"
    nanometers = "nanometers"
    TeV = "TeV"


class SpectralUnitValue(object):
    def __init__(self, value, unit):
        self.Value = value
        self._units = None
        self.Units = unit

    @property
    def Units(self):
        return self._units

    @Units.setter
    def Units(self, value):
        if isinstance(value, SpectralUnits):
            self._units = value
        elif isinstance(value, basestring):
            self._units = SpectralUnits(value)
        else:
            raise ValueError

    def __str__(self):
        return str(self.Value) + ' ' + self._units.value

    @staticmethod
    def from_xml(parent, tagname):
        # find element
        el = parent.find(tagname)
        if el is None:
            return None
        # set it
        value = float(el.text)
        units = SpectralUnits(el.attrib['units'])
        # return new instance
        return SpectralUnitValue(value, units)

    def to_xml(self, parent, tagname):
        el = etree.SubElement(parent, tagname)
        el.text = str(self.Value)
        el.attrib['units'] = self._units.value

