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
    def from_xml(parent, tagname, namespace=''):
        # find element
        el = parent.find(namespace + tagname)
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


class SpectralEfficiencyAccess(object):
    @property
    def SpectralEfficiency(self):
        from .spectralefficiency import SpectralEfficiency
        return self._get_one_element(SpectralEfficiency)

    @SpectralEfficiency.setter
    def SpectralEfficiency(self, value):
        from .spectralefficiency import SpectralEfficiency
        self._set_one_element(SpectralEfficiency, value)


class SpectralRegionAccess(object):
    @property
    def SpectralRegion(self):
        from .spectralregion import SpectralRegion
        region = self._get_one_element(SpectralRegion)
        return None if region is None else region.Type

    @SpectralRegion.setter
    def SpectralRegion(self, value):
        from .spectralregion import SpectralRegion
        self._set_one_element(SpectralRegion, None if value is None else SpectralRegion(self, type=value))


class SlitAccess(object):
    @property
    def Slit(self):
        from .slit import Slit
        return self._get_one_element(Slit)

    @Slit.setter
    def Slit(self, value):
        from .slit import Slit
        self._set_one_element(Slit, value)


class SlitMaskAccess(object):
    @property
    def SlitMask(self):
        from .slitmask import SlitMask
        return self._get_one_element(SlitMask)

    @SlitMask.setter
    def SlitMask(self, value):
        from .slitmask import SlitMask
        self._set_one_element(SlitMask, value)
