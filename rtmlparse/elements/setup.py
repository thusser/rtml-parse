from lxml import etree

from .baseelement import BaseElement


class Setup(BaseElement):
    def __init__(self, parent, name=None, uid=None):
        # BaseElement
        import rtmlparse.elements as e
        BaseElement.__init__(self, 'Setup', parent, name=name, uid=uid,
                             valid_element_types=[e.Spectrograph, e.Target, e.Grating, e.Filter, e.Camera,
                                                  e.Exposure, e.ExposureConstraint, e.Location])


