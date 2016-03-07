"""Routines for handling etrees representing RTML."""
import StringIO
import importlib
import inspect
import os
from enum import Enum
import datetime
import pkgutil
from lxml import etree
from astropy.time import Time

import rtmlparse.templates
from rtmlparse.irtml import ITemplate
from rtmlparse.elements.baseelement import BaseElement
from rtmlparse.elements import *

# define list of root elements
ROOT_ELEMENTS = [
    Target,
    Telescope,
    Camera, Spectrograph, Detector, Device,
    Calibration, Catalogue,
    Observatory,
    Pipeline,
    Project,
    Schedule,
    Setup,
    Scoring,
    WeatherReport
]


class RTML(BaseElement):
    """ Enumeration for RTML modes. """

    class Mode(Enum):
        abort = 'abort'
        acknowledged = 'acknowledged'
        complete = 'complete'
        confirm = 'confirm'
        fail = 'fail'
        incomplete = 'incomplete'
        inquiry = 'inquiry'
        offer = 'offer'
        reject = 'reject'
        report = 'report'
        request = 'request'
        resource = 'resource'
        update = 'update'

    def __init__(self, uid, mode):
        """Create a new RTML element tree, with specified uid and mode.

        Args:

            uid (string): the UID of the request, like:

                rtml://org.myTelescope/phase0

            mode (Mode): mode as defined in RTML schema
                (See also  RTML.Mode enumeration)
        """
        BaseElement.__init__(self, 'RTML', None, name='RTML', uid=uid, valid_element_types=True)

        self.xsd = None
        self.mode = None
        self.expires = None
        self.refcount = []
        self.history = []
        self.RespondTo = None
        self.mode = mode

    def _schema(self):
        if self.xsd is None:
            self.xsd = etree.XMLSchema(file=os.path.join(rtmlparse.__path__[0], "schema/RTML-3.3a.xsd"))
            # print self.xsd
        return self.xsd

    @property
    def namespace(self):
        return 'http://www.ivoa.net/xml/RTML/v3.3a'

    def xml(self):
        """Converts RTML to string.

        Args:
            pretty_print (bool): indent the output for improved human-legibility
                when possible. See also:
                http://lxml.de/FAQ.html#why-doesn-t-the-pretty-print-option-reformat-my-xml-output
            xml_declaration (bool): Prepends a doctype tag to the string output,
                i.e. something like ``<?xml version='1.0' encoding='UTF-8'?>``
        Returns:
            Bytes containing raw XML representation of VOEvent.

        """

        # name?
        name = self.mode.name if hasattr(self.mode, 'name') else str(self.mode)

        # create the root element
        xmlns = self.namespace
        xsi = "http://www.w3.org/2001/XMLSchema-instance"
        schemaLocation = "http://www.ivoa.net/xml/RTML/v3.3a http://www.astro.physik.uni-goettingen.de/~husser/RTML-3.2c.xsd"
        root = etree.Element('RTML', {'{' + xsi + '}schemaLocation': schemaLocation, 'mode': name,
                                      'uid': self.uid, 'version': "3.3a"}, nsmap={None: xmlns, 'xsi': xsi})

        # write xml
        self.to_xml(root)

        # to xml
        return root

    def dumps(self, pretty_print=False, xml_declaration=True, encoding='UTF-8'):
        return etree.tostring(self.xml(), pretty_print=pretty_print,
                              xml_declaration=xml_declaration,
                              encoding=encoding)

    def dump(self, file, pretty_print=True, xml_declaration=True):
        """Writes the RTML to the file object.

        e.g.::

            with open('/tmp/myrtml.xml','wb') as f:
                r.dump(f)

        Args:
            file (file): An open (binary mode) file object for writing.
            pretty_print
            pretty_print(bool): See :func:`dumps`
            xml_declaration(bool): See :func:`dumps`
        """
        file.write(self.dumps(pretty_print, xml_declaration))

    @staticmethod
    def load(file):
        # load XML
        tree = etree.parse(file)
        xml = tree.getroot()

        # get uid and mode
        uid = xml.attrib['uid']
        mode = RTML.Mode(xml.attrib['mode'])

        # create new RTML object
        rtml = RTML(uid, mode)

        # parse xml
        rtml.from_xml(xml, rtml)

        # now resolve all references
        rtml.resolve_refs(rtml.elements)

        # return it
        return rtml

    @staticmethod
    def loads(string):
        f = StringIO.StringIO(string)
        return RTML.load(f)

    def to_xml(self, parent):
        # type checks
        if self.expires is not None and not isinstance(self.expires, Time):
            raise ValueError('Value for "expires" is expected to be of type astropy.time.Time.')

        # # add some default history entry
        # if len(self.history) == 0:
        #     self.add_history(History(self, agent="rtmlparse"))
        #
        # # add history
        # if len(self.history) > 0:
        #     history = etree.SubElement(parent, 'History')
        #     for hist in self.history:
        #         hist.to_xml(history)

        # do reference count and reset inserted
        self.reset_processed()
        self.refcount = self.reference_count()
        self.reset_processed()

        # now we insert the top-level stuff, but only if their refcount!=2,
        # i.e. not referenced exactly exactly once
        root_elements = {}
        for klass in ROOT_ELEMENTS:
            for uid, element in self.filtered([klass]).iteritems():
                if uid in self.refcount and self.refcount[uid] != 2:
                    root_elements[element] = element.to_xml(parent, add_children=False)

        # now again, filling children
        for element, base in root_elements.iteritems():
            element.to_xml_add_children(base)

        # other stuff
        self.add_text_value(parent, 'RespondTo', self.RespondTo)
        if self.expires is not None:
            self.expires.format = 'iso'
            parent.attrib['expires'] = str(self.expires)

    def from_xml(self, element, rtml):
        # base call
        BaseElement.from_xml(self, element, rtml)
        ns = '{' + rtml.namespace + '}'

        # other stuff
        self.RespondTo = self.from_text_value(element, ns + 'RespondTo', str)
        t2 = Time('2010-01-01 00:00:00', scale='utc')
        #self.expires = datetime.datetime.strptime(element.attrib['expires'], '%Y-%m-%dT%H:%M:%Sz') \
        #    if 'expires' in element.attrib else None
        self.expires = Time(element.attrib['expires']) if 'expires' in element.attrib else None

        # history
#        history = element.find(ns + 'History')
#        if history is not None:
#            # find all entries
#            for entry in history.findall(ns + 'Entry'):
#                # create History object and parse
#                hist = History()
#                hist.from_xml(entry, self)
#                self.history.append(hist)

    def valid(self):
        """Tests if a RTML conforms to the schema.

        Returns: Bool (RTML is valid?)
        """
        xsd = self._schema()
        page = etree.ElementTree(self.xml())
        valid = xsd.assertValid(page)
        print xsd.error_log
        return valid

    def add_history(self, history):
        self.history.append(history)

    def get_plugins(self, interface, package):
        """
        Retrieve all plugins implementing the given interface beneath the given module.

        @param interface: An interface class.  Only plugins which implement this
        interface will be returned.

        @param package: A package beneath which plugins are installed.

        @return: An iterator of plugins.
        """

        # list for storing plugins
        plugins = []

        # list modules in gcdb.methods
        pkgpath = os.path.dirname(package.__file__)
        modules = [name for _, name, _ in pkgutil.iter_modules([pkgpath])]

        # loop modules
        for m in modules:
            # import module
            mod = importlib.import_module(package.__name__ + '.' + m)

            # get all classes
            for name, obj in inspect.getmembers(mod):
                if inspect.isclass(obj):
                    # does class implement interface?
                    if interface.implementedBy(obj):
                        # yep, add it to list
                        plugins.append(obj)

        # finished
        return plugins

    def templates(self):
        # list to store templates in
        templates = []

        # first get a list of all available templates
        plugins = self.get_plugins(ITemplate, rtmlparse.templates)

        # now loop all elements
        for element in self.elements.values():
            # try to find template that deals with this kind of element
            for plugin in plugins:
                if element.name == 'template:' + plugin.name and isinstance(element, plugin.type):
                    # instantiate template and add to list
                    tpl = plugin(element)
                    templates.append(tpl)

        # return list
        return templates
