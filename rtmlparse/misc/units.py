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
