from lxml import etree
from enum import Enum

from .baseelement import BaseElement
from . import misc


class Filter(BaseElement):
    class Types(Enum):
        none = "none"
        clear = "clear"
        neutral_density = "neutral density"
        blue = "blue"
        green = "green"
        red = "red"
        U = "U"
        B = "B"
        V = "V"
        R = "R"
        I = "I"
        H = "H"
        J = "J"
        K = "K"
        L = "L"
        M = "M"
        N = "N"
        JohnsonU = "Johnson U"
        JohnsonB = "Johnson B"
        JohnsonV = "Johnson V"
        JohnsonR = "Johnson R"
        JohnsonI = "Johnson I"
        JohnsonJ = "Johnson J"
        JohnsonH = "Johnson H"
        JohnsonK = "Johnson K"
        JohnsonL = "Johnson L"
        JohnsonM = "Johnson M"
        JohnsonN = "Johnson N"
        BesselU = "Bessel U"
        BesselB = "Bessel B"
        BesselV = "Bessel V"
        BesselR = "Bessel R"
        BesselI = "Bessel I"
        CousinsR = "Cousins R"
        CousinsI = "Cousins I"
        Sloanu = "Sloan u"
        Sloang = "Sloan g"
        Sloanr = "Sloan r"
        Sloani = "Sloan i"
        Sloanz = "Sloan z"
        Stroemgrenu = "Stroemgren u"
        Stroemgrenb = "Stroemgren b"
        Stroemgrenbeta = "Stroemgren beta"
        Stroemgrenv = "Stroemgren v"
        Stroemgreny = "Stroemgren y"
        Gunng = "Gunn g"
        Gunnr = "Gunn r"
        Gunni = "Gunn i"
        Gunnz = "Gunn z"
        narrowband = "narrowband"
        Halpha = "Halpha"
        Hbeta = "Hbeta"
        forbiddenOI = "forbidden OI"
        forbiddenOII = "forbidden OII"
        forbiddenOIII = "forbidden OIII"
        forbiddenNII = "forbidden NII"
        forbiddenSII = "forbidden SII"
        other = "other"
    
    def __init__(self, parent, name=None, uid=None, filter_type=None):
        BaseElement.__init__(self, 'Filter', parent, name=name, uid=uid)
        self._type = None
        self.Type = filter_type
        self._center = None
        self._fwhm = None
        self.PeakEfficiency = None
        self.Uri = None

    def to_xml(self, parent):
        # add element
        element = BaseElement.to_xml(self, parent)
        if element is None:
            return None

        # type
        if self.Type is not None:
            element.attrib['type'] = self.Type.value

        # other stuff
        if self._center is not None:
            self._center.to_xml(element, 'Center')
        if self._fwhm is not None:
            self._fwhm.to_xml(element, 'FWHM')
        self.add_text_value(element, 'PeakEfficiency', self.PeakEfficiency, 'f')
        self.add_text_value(element, 'Uri', self.Uri, 's')

        # return base element
        return element

    def from_xml(self, element, rtml):
        # base call
        BaseElement.from_xml(self, element, rtml)
        ns = '{' + rtml.namespace + '}'

        # type
        self.Type = Filter.Types(element.attrib['type']) if 'type' in element.attrib else None

        # other stuff
        self._center = misc.SpectralUnitValue.from_xml(element, ns + 'Center')
        self._fwhm = misc.SpectralUnitValue.from_xml(element, ns + 'FWHM')
        self.PeakEfficiency = self.from_text_value(element, ns + 'PeakEfficiency', float)
        self.Uri = self.from_text_value(element, ns + 'Uri', str)

    @property
    def Type(self):
        return self._type

    @Type.setter
    def Type(self, value):
        if value is None:
            self._type = None
        elif isinstance(value, basestring):
            self._type = Filter.Types(value)
        elif isinstance(value, Filter.Types):
            self._type = value
        else:
            raise ValueError

    @property
    def Center(self):
        return self._center

    @Center.setter
    def Center(self, value):
        if value is None:
            self._center = None
        elif isinstance(value, misc.SpectralUnitValue):
            self._center = value
        else:
            raise ValueError

    @property
    def FWHM(self):
        return self._fwhm

    @FWHM.setter
    def FWHM(self, value):
        if value is None:
            self._fwhm = None
        elif isinstance(value, misc.SpectralUnitValue):
            self._fwhm = value
        else:
            raise ValueError

