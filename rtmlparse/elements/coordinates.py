from lxml import etree

from .baseelement import BaseElement
from .misc import auto_attr_check
from rtmlparse.misc import units, unitvalues


class Coordinates(BaseElement):
    Description = str

    def __init__(self, parent, name=None, uid=None):
        BaseElement.__init__(self, 'Coordinates', parent, name=name, uid=uid)

    @classmethod
    def create(cls, element, rtml, name=None, uid=None):
        ns = '{' + rtml.namespace + '}'
        if element.find(ns + 'RightAscension') is not None:
            return EquatorialCoordinates(rtml, name=name, uid=uid)
        elif element.find(ns + 'Altitude') is not None:
            return HorizontalCoordinates(rtml, name=name, uid=uid)
        elif element.find(ns + 'DomeScreen') is not None:
            return DomeScreenCoordinates(rtml, name=name, uid=uid)
        elif element.find(ns + 'ParkPosition') is not None:
            return ParkPositionCoordinates(rtml, name=name, uid=uid)
        elif element.find(ns + 'ServicePosition') is not None:
            return ServicePositionCoordinates(rtml, name=name, uid=uid)
        elif element.find(ns + 'Zenith') is not None:
            return ZenithCoordinates(rtml, name=name, uid=uid)
        else:
            raise ValueError


@auto_attr_check
class EquatorialCoordinates(Coordinates):
    # TODO: RA and Dec with proper types
    RightAscension = float
    Declination = float
    Epoch = float
    Equinox = float
    System = units.CoordinateSystemTypes
    Description = str

    def __init__(self, parent, name=None, uid=None):
        Coordinates.__init__(self, parent, name=name, uid=uid)
        self.RightAscension = None
        self.Declination = None
        self.Epoch = None
        self.Equinox = None
        self.Description = None
        self.System = None

    def to_xml(self, parent, add_children=True):
        # add element
        element = BaseElement.to_xml(self, parent, add_children=add_children)
        if element is None:
            return None
        ns = '{' + self.rtml.namespace + '}'

        # other stuff
        self.add_text_value(element, 'RightAscension', self.RightAscension, 'f', namespace=ns)
        self.add_text_value(element, 'Declination', self.Declination, 'f', namespace=ns)
        self.add_text_value(element, 'Epoch', self.Epoch, 'f', namespace=ns)
        self.add_text_value(element, 'Equinox', self.Equinox, 'f', namespace=ns)
        self.add_enum_value(element, 'System', self.System, namespace=ns)
        self.add_text_value(element, 'Description', self.Description, 's', namespace=ns)

        # return base element
        return element

    def from_xml(self, xml, rtml):
        # base call
        BaseElement.from_xml(self, xml, rtml)
        ns = '{' + rtml.namespace + '}'

        # other stuff
        self.RightAscension = self.from_text_value(xml, 'RightAscension', float, namespace=ns)
        self.Declination = self.from_text_value(xml, 'Declination', float, namespace=ns)
        self.Epoch = self.from_text_value(xml, 'Epoch', float, namespace=ns)
        self.Equinox = self.from_text_value(xml, 'Equinox', float, namespace=ns)
        self.System = self.from_enum_value(xml, 'System', units.CoordinateSystemTypes, namespace=ns)
        self.Description = self.from_text_value(xml, 'Description', str, namespace=ns)


@auto_attr_check
class HorizontalCoordinates(Coordinates):
    Altitude = float
    Azimuth = float
    Description = float

    def __init__(self, parent, name=None, uid=None):
        Coordinates.__init__(self, parent, name=name, uid=uid)
        self.Altitude = None
        self.Azimuth = None
        self.Description = None

    def to_xml(self, parent, add_children=True):
        # add element
        element = BaseElement.to_xml(self, parent, add_children=add_children)
        if element is None:
            return None
        ns = '{' + self.rtml.namespace + '}'

        # other stuff
        self.add_text_value(element, 'Altitude', self.Altitude, 'f', namespace=ns)
        self.add_text_value(element, 'Azimuth', self.Azimuth, 'f', namespace=ns)
        self.add_text_value(element, 'Description', self.Description, 's', namespace=ns)

        # return base element
        return element

    def from_xml(self, xml, rtml):
        # base call
        BaseElement.from_xml(self, xml, rtml)
        ns = '{' + rtml.namespace + '}'

        # other stuff
        self.Altitude = self.from_text_value(xml, 'Altitude', float, namespace=ns)
        self.Azimuth = self.from_text_value(xml, 'Azimuth', float, namespace=ns)
        self.Description = self.from_text_value(xml, 'Description', str, namespace=ns)


@auto_attr_check
class PredefinedCoordinates(Coordinates):
    Description = float

    def __init__(self, parent, name=None, uid=None, position='ParkPosition'):
        Coordinates.__init__(self, parent, name=name, uid=uid)
        self.Description = None
        self._position = position

    def to_xml(self, parent, add_children=True):
        # add element
        element = BaseElement.to_xml(self, parent, add_children=add_children)
        if element is None:
            return None
        ns = '{' + self.rtml.namespace + '}'

        # other stuff
        etree.SubElement(element, self._position)
        self.add_text_value(element, 'Description', self.Description, 's', namespace=ns)

        # return base element
        return element

    def from_xml(self, xml, rtml):
        # base call
        BaseElement.from_xml(self, xml, rtml)
        ns = '{' + rtml.namespace + '}'

        # other stuff
        self.Description = self.from_text_value(xml, 'Description', str, namespace=ns)


class DomeScreenCoordinates(PredefinedCoordinates):
    def __init__(self, parent, name=None, uid=None):
        PredefinedCoordinates.__init__(self, parent, name=name, uid=uid, position='DomeScreen')


class ParkPositionCoordinates(PredefinedCoordinates):
    def __init__(self, parent, name=None, uid=None):
        PredefinedCoordinates.__init__(self, parent, name=name, uid=uid, position='ParkPosition')


class ServicePositionCoordinates(PredefinedCoordinates):
    def __init__(self, parent, name=None, uid=None):
        PredefinedCoordinates.__init__(self, parent, name=name, uid=uid, position='ServicePosition')


class ZenithCoordinates(PredefinedCoordinates):
    def __init__(self, parent, name=None, uid=None):
        PredefinedCoordinates.__init__(self, parent, name=name, uid=uid, position='Zenith')
