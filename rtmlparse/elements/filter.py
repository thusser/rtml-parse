from lxml import etree
from enum import Enum

from .baseelement import BaseElement
from . import misc
from rtmlparse.misc import unitvalues
from .misc import auto_attr_check


class FilterTypes(Enum):
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


@auto_attr_check
class Filter(BaseElement):
    Type = FilterTypes
    Center = unitvalues.SpectralType
    FWHM = unitvalues.SpectralType
    PeakEfficiency = float
    Uri = str

    def __init__(self, parent, name=None, uid=None, filter_type=None):
        BaseElement.__init__(self, 'Filter', parent, name=name, uid=uid)
        self.Type = filter_type
        self.Center = None
        self.FWHM = None
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
        if self.Center is not None:
            self.Center.to_xml(element, 'Center')
        if self.FWHM is not None:
            self.FWHM.to_xml(element, 'FWHM')
        self.add_text_value(element, 'PeakEfficiency', self.PeakEfficiency, 'f')
        self.add_text_value(element, 'Uri', self.Uri, 's')

        # return base element
        return element

    def from_xml(self, element, rtml):
        # base call
        BaseElement.from_xml(self, element, rtml)
        ns = '{' + rtml.namespace + '}'

        # type
        self.Type = FilterTypes(element.attrib['type']) if 'type' in element.attrib else None

        # other stuff
        self.Center = unitvalues.SpectralType.from_xml(element, 'Center', namespace=ns)
        self.FWHM = unitvalues.SpectralType.from_xml(element, 'FWHM', namespace=ns)
        self.PeakEfficiency = self.from_text_value(element, 'PeakEfficiency', float, namespace=ns)
        self.Uri = self.from_text_value(element, 'Uri', str, namespace=ns)
