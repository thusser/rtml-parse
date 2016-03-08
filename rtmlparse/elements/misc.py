from enum import Enum
from lxml import etree


def getter_setter_gen(name, type_):
    def getter(self):
        return getattr(self, "__" + name)

    def setter(self, value):
        if value is not None and not isinstance(value, type_):
            raise TypeError("%s attribute must be set to an instance of %s" % (name, type_))
        setattr(self, "__" + name, value)
    return property(getter, setter)


def auto_attr_check(cls):
    new_dct = {}
    for key, value in cls.__dict__.items():
        if isinstance(value, type):
            value = getter_setter_gen(key, value)
        new_dct[key] = value
    # Creates a new class, using the modified dictionary as the class dict:
    return type(cls)(cls.__name__, cls.__bases__, new_dct)


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


class CoordinatesAccess(object):
    @property
    def Coordinates(self):
        from .coordinates import Coordinates
        return self._get_one_element(Coordinates)

    @Coordinates.setter
    def Coordinates(self, value):
        from .coordinates import Coordinates
        self._set_one_element(Coordinates, value)


class HistoryAccess(object):
    @property
    def History(self):
        from .history import History
        return self._get_one_element(History)

    @History.setter
    def History(self, value):
        from .history import History
        self._set_one_element(History, value)


class WindowingAccess(object):
    @property
    def Windowing(self):
        from .windowing import Windowing
        return self._get_one_element(Windowing)

    @Windowing.setter
    def Windowing(self, value):
        from .windowing import Windowing
        self._set_one_element(Windowing, value)

