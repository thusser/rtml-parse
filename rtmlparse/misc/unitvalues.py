from enum import EnumMeta
from lxml import etree

from rtmlparse.misc.units import *


class UnitValue(object):
    def __init__(self, value_type, units_type, attrib_types={}, value=None, units=None, attrib={}):
        # store types
        self._value_type = value_type
        self._units_type = units_type
        self._attrib_types = attrib_types

        # init
        self._value = None
        self._units = None
        self._attrib = {}

        # set them
        self.Value = value
        self.Units = units
        for a in attrib:
            self[a] = attrib[a]

    @property
    def Value(self):
        return self._value

    @Value.setter
    def Value(self, value):
        if value is None or isinstance(value, self._value_type):
            self._value = value
        else:
            raise ValueError

    @property
    def Units(self):
        return self._units

    @Units.setter
    def Units(self, unit):
        if isinstance(unit, self._units_type):
            self._units = unit;
        elif isinstance(self._units_type, EnumMeta):
            self._units = self._units_type(unit)
        else:
            raise ValueError

    def __len__(self):
        return len(self._attrib)

    def __getitem__(self, key):
        return self._attrib[key]

    def __setitem__(self, key, value):
        if key not in self._attrib_types:
            return  # just ignore, need this for from_xml()
        elif isinstance(value, self._attrib_types[key]):
            self._attrib[key] = value
        elif isinstance(self._attrib_types[key], EnumMeta):
            self._attrib[key] = self._attrib_types[key](value)
        else:
            raise ValueError

    def __delitem__(self, key):
        del self._attrib[key]

    def __iter__(self):
        return iter(self._attrib)

    def __str__(self):
        units = self._units.value if isinstance(self._units, Enum) else str(self._units)
        return str(self.Value) + ' ' + units

    @classmethod
    def from_xml(cls, parent, tagname, namespace=''):
        # find element
        el = parent.find(namespace + tagname)
        if el is None:
            return None
        # set it
        value = float(el.text)
        units = el.attrib['units']
        # create new class
        return cls(value, units, attrib=dict(el.attrib))

    def to_xml(self, parent, tagname):
        # element itself
        el = etree.SubElement(parent, tagname)
        # value and units
        el.text = str(self.Value)
        el.attrib['units'] = self._units.value if isinstance(self._units, Enum) else str(self._units)
        # all attribs
        for a in self._attrib:
            if self._attrib[a] is not None:
                el.attrib[a] = self._attrib[a].value if isinstance(self._attrib[a], Enum) else str(self._attrib[a])


class SpectralValue(UnitValue):
    def __init__(self, value, units, attrib={}):
        UnitValue.__init__(self, float, SpectralUnits, value=value, units=units)


class VelocityValue(UnitValue):
    def __init__(self, value, units, attrib={}, system=None):
        if system is not None: attrib['system'] = system
        UnitValue.__init__(self, float, VelocityUnits, {'system': VelocitySystemTypes},
                           value=value, units=units, attrib=attrib)


class ApertureValue(UnitValue):
    def __init__(self, value, units='meters', attrib={}, ap_type=None):
        if ap_type is not None: attrib['type'] = ap_type
        UnitValue.__init__(self, float, LengthUnits, {'type': ApertureTypes},
                           value=value, units=units, attrib=attrib)
