from lxml import etree

from .baseelement import BaseElement


class Schedule(BaseElement):
    def __init__(self, parent, name=None, uid=None):
        # BaseElement
        import rtmlparse.elements as e
        BaseElement.__init__(self, 'Schedule', parent, name=name, uid=uid,
                             valid_element_types=[e.Spectrograph, e.Target, e.Setup, e.ExposureConstraint,
                                                  e.Exposure])

        # Schedule
        self.exposures = []

    def to_xml(self, parent, add_children=True):
        # add schedule
        element = BaseElement.to_xml(self, parent, add_children=add_children)
        if element is None:
            return None

        # exposures
        for exp in self.exposures:
            exposure = etree.SubElement(element, 'Exposure')
            exposure.set('count', '{0:d}'.format(exp[1]))
            value = etree.SubElement(exposure, 'Value')
            value.set('units', 'seconds')
            value.text = '{0:.2f}'.format(exp[0])

        # return base element
        return element

    def from_xml(self, xml, rtml):
        # base call
        BaseElement.from_xml(self, xml, rtml)
        ns = '{' + rtml.namespace + '}'

        # exposures
        exps = xml.findall(ns + 'Exposure')
        for exp in exps:
            exptime = float(exp.find(ns + 'Value').text)
            count = int(exp.attrib['count'])
            self.add_exposure(exptime, count)

    def add_exposure(self, exptime, count=1):
        self.exposures.append((exptime, count))
