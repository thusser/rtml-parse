from lxml import etree

from .baseelement import BaseElement
from .misc import auto_attr_check, CoordinatesAccess, SpectralRegionAccess, SpectralEfficiencyAccess
from rtmlparse.misc import units, unitvalues


@auto_attr_check
class Telescope(BaseElement, CoordinatesAccess, SpectralEfficiencyAccess, SpectralRegionAccess):
    Aperture = unitvalues.ApertureValue
    Description = str
    FocalLength = float
    FocalRatio = str
    PlateScale = float
    # TODO: TrackRate

    def __init__(self, parent, name=None, uid=None):
        # BaseElement
        import rtmlparse.elements as e
        BaseElement.__init__(self, 'Telescope', parent, name=name, uid=uid,
                             valid_element_types=[e.Camera, e.Location, e.Setup, e.Spectrograph, e.Coordinates,
                                                  e.Device, e.SpectralEfficiency, e.SpectralRegion, e.Telescope,
                                                  e.WeatherReport, e.Mirrors])

        # Telescope
        self.Aperture = None
        self.Description = None
        self.FocalLength = None
        self.FocalRatio = None
        self.PlateScale = None

    def to_xml(self, parent, add_children=True):
        # add element
        element = BaseElement.to_xml(self, parent, add_children=add_children)
        if element is None:
            return

        # other stuff
        self.add_unit_value(element, 'Aperture', self.Aperture)
        self.add_text_value(element, 'Description', self.Description)
        self.add_text_value(element, 'FocalLength', self.FocalLength, attrib={'units': 'meters'})
        self.add_text_value(element, 'FocalRatio', self.FocalRatio)
        self.add_text_value(element, 'PlateScale', self.PlateScale, attrib={'units': 'arcseconds per millimeter'})

        # return base element
        return element

    def from_xml(self, element, rtml):
        # base call
        BaseElement.from_xml(self, element, rtml)
        ns = '{' + rtml.namespace + '}'

        # other stuff
        self.Aperture = self.from_unit_value(element, 'Aperture', unitvalues.ApertureValue, namespace=ns)
        self.Description = self.from_text_value(element, 'Description', str, namespace=ns)
        self.FocalLength = self.from_text_value(element, 'FocalLength', float, namespace=ns)
        self.FocalRatio = self.from_text_value(element, 'FocalRatio', str, namespace=ns)
        self.PlateScale = self.from_text_value(element, 'PlateScale', float, namespace=ns)
