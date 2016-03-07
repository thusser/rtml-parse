import os
import unittest
import tempfile

from rtmlparse import RTML
from rtmlparse.elements import *
from rtmlparse.elements import misc


class TestMinimalRTML(unittest.TestCase):
    def test_make_minimal_rtml(self):
        # create rtml
        rtml = RTML("rtml://test.org/rtml", RTML.Mode.request)

        # check uid and mode
        self.assertEqual(rtml.uid, "rtml://test.org/rtml", "Checking RTML uid.")
        self.assertEqual(rtml.mode, RTML.Mode.request, "Checking RTML mode.")


class TestDelete(unittest.TestCase):
    def test_delete(self):
        # create rtml
        rtml = RTML("rtml://test.org/rtml", RTML.Mode.request)
        c = Camera(rtml, name='TestCamera', uid='some_uid')
        s1 = Setup(rtml)
        s1.add_element(c)
        s2 = Setup(rtml)
        s2.add_element(c)

        # delete camera
        rtml.delete(c.uid)

        # check
        self.assertEqual(len(rtml.find(Camera)), 0)
        self.assertEqual(len(s1.find(Camera)), 0)
        self.assertEqual(len(s2.find(Camera)), 0)


class TestElements(unittest.TestCase):
    def setUp(self):
        # create RTML
        self.rtml = RTML("rtml://test.org/rtml", RTML.Mode.request)

    def saveLoad(self):
        # save file
        with tempfile.NamedTemporaryFile(delete=False) as f:
            self.rtml.dump(f)
        # load file
        with open(f.name, 'r') as f:
            rtml = RTML.load(f)
        return rtml

    def test_uid_ref(self):
        # create camera
        c = Camera(self.rtml, name='TestCamera', uid='some_uid')
        # we need to reference it twice
        s1 = Setup(self.rtml)
        s1.add_element(c)
        s2 = Setup(self.rtml)
        s2.add_element(c)

        # save it and load it again
        rtml = self.saveLoad()

        # check uid of camera
        camera = rtml.find_first(Camera)
        self.assertEqual(camera.uid, 'some_uid')

        # check references in setups
        for s in rtml.find(Setup).values():
            # check number of cameras
            cameras = s.find(Camera)
            self.assertEqual(len(cameras), 1)
            # check cameras
            for c in cameras.values():
                self.assertEqual(c, camera)

    def test_camera(self):
        # create camera
        camera = Camera(self.rtml, name='TestCamera')
        camera.Description = "Some test camera"
        camera.SpectralEfficiency = SpectralEfficiency(self.rtml, description='Some description',
                                                       uri='http://example.org')
        camera.SpectralRegion = SpectralRegionTypes.optical

        # save it and load it again
        rtml = self.saveLoad()

        # check
        camera = rtml.find_first(Camera)
        self.assertEqual(camera.name, 'TestCamera')
        self.assertEqual(camera.SpectralEfficiency.Description, 'Some description')
        self.assertEqual(camera.SpectralEfficiency.Uri, 'http://example.org')
        self.assertEqual(camera.SpectralRegion, SpectralRegionTypes.optical)

    def test_filter(self):
        # create filter
        camera = Camera(self.rtml, name='TestCamera')
        wheel = FilterWheel(camera)
        f = Filter(wheel, filter_type=FilterTypes.clear)
        f.Center = misc.SpectralUnitValue(3.14159, misc.SpectralUnits.nanometers)
        f.FWHM = misc.SpectralUnitValue(42., misc.SpectralUnits.centimeters)
        f.PeakEfficiency = 0.95
        f.Uri = 'uri://test.org/'

        # save it and load it again
        rtml = self.saveLoad()

        # check
        wheel = camera.find_first(FilterWheel)
        f = wheel.find_first(Filter)
        self.assertEqual(str(f.Center), "3.14159 nanometers")
        self.assertEqual(str(f.FWHM), "42.0 centimeters")
        self.assertEqual(f.PeakEfficiency, 0.95)
        self.assertEqual(f.Uri, 'uri://test.org/')

    def test_spectrograph(self):
        # create spectrograph
        spectrograph = Spectrograph(self.rtml, name='TestSpectrograph')
        spectrograph.Description = "Some test spectrograph"
        spectrograph.PositionAngle = 3.14
        # single slit
        slit = Slit(spectrograph)
        slit.PositionAngle = 42.
        slit.WidthLength = (7, 13)
        # slit mask with 3 slits
        slitmask = SlitMask(spectrograph)
        Slit(slitmask)
        Slit(slitmask)
        Slit(slitmask)

        # save it and load it again
        rtml = self.saveLoad()

        # check
        spectrograph = rtml.find_first(Spectrograph)
        self.assertEqual(spectrograph.name, 'TestSpectrograph')
        self.assertEqual(spectrograph.Description, 'Some test spectrograph')
        self.assertEqual(spectrograph.PositionAngle, 3.14)
        self.assertEqual(spectrograph.Slit.PositionAngle, 42.)
        self.assertEqual(spectrograph.Slit.WidthLength, (7, 13))
        self.assertEqual(len(spectrograph.SlitMask.find(Slit)), 3)

    def test_location(self):
        # create a setup with a location
        setup = Setup(self.rtml)
        location = Location(setup)
        location.EastLongitude = 20.810694
        location.Latitude = -32.379444
        location.Height = 1798.
        location.TimeZone = 2

        # save it and load it again
        rtml = self.saveLoad()

        # check
        location = rtml.find_first(Setup).find_first(Location)
        self.assertEqual(location.EastLongitude, 20.810694)
        self.assertEqual(location.Latitude, -32.379444)
        self.assertEqual(location.Height, 1798.)
        self.assertEqual(location.TimeZone, 2)

if __name__ == '__main__':
    unittest.main(verbosity=2)
