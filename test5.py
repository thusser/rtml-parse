from rtmlparse.misc.unitvalues import *
from rtmlparse.misc.units import *

a = SpectralValue(1., SpectralUnits.centimeters)
print str(a)

b = VelocityValue(10., VelocityUnits.kms, system=VelocitySystemTypes.heliocentric)
print str(b)
print b['system'].value


namespace = 'http://www.ivoa.net/xml/RTML/v3.3a'
xmlns = namespace
xsi = "http://www.w3.org/2001/XMLSchema-instance"
schemaLocation = "http://www.ivoa.net/xml/RTML/v3.3a http://www.astro.physik.uni-goettingen.de/~husser/RTML-3.2c.xsd"
root = etree.Element('RTML', {'{' + xsi + '}schemaLocation': schemaLocation}, nsmap={None: xmlns, 'xsi': xsi})

b.to_xml(root, 'Velocity')

print etree.tostring(root, pretty_print=True)

c = VelocityValue.from_xml(root, 'Velocity')


print str(c)
print c['system'].value