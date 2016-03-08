from rtmlparse import RTML
from rtmlparse.elements import *
from rtmlparse.misc import units, unitvalues


def main():
    # create rtml
    rtml = RTML('rtml://monet.uni-goettingen.de/resource', RTML.Mode.resource)

    # telescope
    telescope = Telescope(rtml, name='MONET/S')
    telescope.Aperture = unitvalues.ApertureValue(1.2)
    telescope.FocalLength = 8.4
    telescope.FocalRatio = 'f/7'
    telescope.PlateScale = 24.56

    # add mirrors
    Mirrors(telescope, number=3, coating=units.CoatingTypes.silver)

    # location
    location = Location(telescope)
    location.EastLongitude = 20.810694
    location.Latitude = -32.379444
    location.Height = 1798.
    location.TimeZone = 2

    # camera
    camera = Camera(telescope, name='SI-1100')
    #camera.Description = 'Scientific Instruments 1100'
    camera.SpectralRegion = SpectralRegionTypes.optical

    # detector
    detector = Detector(camera)
    detector.NumColumns = 2048
    detector.NumRows = 2048
    detector.PixelSize = 15.

    # dump it
    print rtml.dumps(pretty_print=True)
    with open("rtml.xml", "wb") as f:
        rtml.dump(f)

    # validate it
    print 'Validating...'
    rtml.valid()


if __name__ == '__main__':
    main()