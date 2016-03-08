from enum import Enum


class SpectralUnits(Enum):
    centimeters = 'centimeters'
    eV = 'eV'
    GeV = 'GeV'
    gigahertz = 'gigahertz'
    hertz = 'hertz'
    keV = 'keV'
    kilohertz = 'kilohertz'
    megahertz = 'megahertz'
    meters = 'meters'
    MeV = 'MeV'
    micrometers = 'micrometers'
    millimeters = 'millimeters'
    nanometers = 'nanometers'
    TeV = 'TeV'


class VelocityUnits(Enum):
    kms = 'kilometers/second'
    redshift = 'redshift'


class VelocitySystemTypes(Enum):
    barycentric ='barycentric'
    geocentric = 'geocentric'
    heliocentric = 'heliocentric'
    lsr = 'lsr'


class LengthUnits(Enum):
    meters = 'meters'


class ApertureTypes(Enum):
    geometric = 'geometric'
    effective = 'effective'
    

class CoordinateSystemTypes(Enum):
    ICRS = 'ICRS'
    FK4 = 'FK4'
    FK4_no_e = 'FK4-no-e'
    FK5 = 'FK5'
    GAPPT = 'GAPPT'
    other = 'other'
    
    
class CoatingTypes(Enum):
    aluminum = 'aluminum'
    enhanced_aluminum = 'enhanced aluminum'
    enhanced_silver = 'enhanced silver'
    gold = 'gold'
    mercury = 'mercury'
    silver = 'silver'
