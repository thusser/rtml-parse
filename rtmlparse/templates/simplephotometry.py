from zope.interface import implementer
from rtmlparse.irtml import ITemplate
from rtmlparse.elements import *


@implementer(ITemplate)
class SimplePhotometry(object):
    name = "SimplePhotometry"
    type = Setup

    def __init__(self, element=None, rtml=None):
        # define our elements
        self.setup = None
        self.Camera = None
        self.Filter = None
        self.Target = None
        self.Exposure = None
        self.ExposureConstraint = None

        # existing or new?
        if element is None:
            # do we have rtml?
            if rtml is None:
                raise ValueError('Need RTML instance for creating new template.')
            # create all necessary elements
            self.create(rtml)
        else:
            # store it, just use the first matching elements found
            self.setup = element
            self.Camera = self.setup.find_first(Camera)
            self.Target = self.setup.find_first(Target)
            self.Filter = self.setup.find_first(Filter)
            self.Exposure = self.setup.find_first(Exposure)
            self.ExposureConstraint = self.setup.find_first(ExposureConstraint)

    def create(self, rtml):
        self.setup = Setup(rtml, name='template:SimplePhotometry')
        self.Camera = Camera(self.setup)
        self.Filter = Filter(self.setup)
        self.Target = Target(self.setup)
        self.Exposure = Exposure(self.setup)
        self.ExposureConstraint = ExposureConstraint(self.setup)
