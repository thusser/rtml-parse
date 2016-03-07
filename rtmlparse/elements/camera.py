from lxml import etree
import warnings

from .baseelement import BaseElement


class Camera(BaseElement):
    def __init__(self, parent, name=None, uid=None):
        # BaseElement
        import rtmlparse.elements as e
        BaseElement.__init__(self, 'Camera', parent, name=name, uid=uid,
                             valid_element_types=[e.Detector, e.FilterWheel, e.Setup,
                                                  e.SpectralEfficiency, e.SpectralRegion])

        # Camera
        self.Description = None
        self.PlateScale = None

    def to_xml(self, parent, add_children=True):
        # add element
        element = BaseElement.to_xml(self, parent, add_children=add_children)
        if element is None:
            return None

        # other stuff
        self.add_text_value(element, 'Description', self.Description)
        self.add_text_value(element, 'PlateScale', self.PlateScale, attrib={'units': 'arcseconds per millimeter'})

        # return base element
        return element

    def from_xml(self, element, rtml):
        # base call
        BaseElement.from_xml(self, element, rtml)
        ns = '{' + rtml.namespace + '}'

        # other stuff
        self.Description = self.from_text_value(element, ns + 'Description', str)
        self.PlateScale = self.from_text_value(element, ns + 'PlateScale', float)

    @property
    def SpectralEfficiency(self):
        from .spectralefficiency import SpectralEfficiency
        return self._get_one_element(SpectralEfficiency)

    @SpectralEfficiency.setter
    def SpectralEfficiency(self, value):
        from .spectralefficiency import SpectralEfficiency
        self._set_one_element(SpectralEfficiency, value)

    @property
    def SpectralRegion(self):
        from .spectralregion import SpectralRegion
        region = self._get_one_element(SpectralRegion)
        return None if region is None else region.Type

    @SpectralRegion.setter
    def SpectralRegion(self, value):
        from .spectralregion import SpectralRegion
        self._set_one_element(SpectralRegion, None if value is None else SpectralRegion(self, type=value))
