"""Base class for all RTML elements."""

import random
import string
import warnings

from lxml import etree

import rtmlparse.elements


class BaseElement(object):
    def __init__(self, tagname, parent, name=None, uid=None, valid_element_types=False, attributes={}):
        # uid must start with a letter
        self.uid = uid
        if self.uid is None:
            self.uid = random.choice(string.ascii_letters)
            self.uid += ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))

        # store stuff
        self.name = name
        self.tagname = tagname
        self.valid_element_types = valid_element_types
        self.elements = {}
        self.refs_to_resolve = []
        self.processed = False
        self.attributes = attributes

        # set root element
        self.rtml = None
        if parent is None and self.tagname == 'RTML':
            pass
        elif parent is not None and parent.tagname == 'RTML':
            self.rtml = parent
            parent.add_element(self)
            self.rtml.add_element(self)
        elif parent is not None and parent.rtml is not None:
            self.rtml = parent.rtml
            parent.add_element(self)
            self.rtml.add_element(self)
        else:
            raise ValueError("RTML root element not found.")

    def delete(self, uid):
        # loop all children
        for el in self.elements.values():
            el.delete(uid)
        # delete in my elements
        if uid in self.elements:
            del self.elements[uid]

    def to_xml(self, parent, add_children=True):
        # get refcount for this element
        rc = 0 if self.uid not in self.rtml.refcount else self.rtml.refcount[self.uid]

        # build attrib
        attrib = {}
        if self.name is not None:
            attrib['name'] = self.name
        if rc > 2 and self.uid is not False:
            if self.processed:
                attrib['ref'] = self.uid
            else:
                attrib['id'] = self.uid

        # create element
        ns = '{' + self.rtml.namespace + '}'
        base = etree.SubElement(parent, ns + self.tagname, attrib=attrib)

        # if this element has not been processed before, add children
        if not self.processed:
            # add children, if requested
            if add_children:
                self.to_xml_add_children(base)

            # indicate inserted
            self.processed = True

            # return base element
            return base

        else:
            # otherwise return None, indicating that this element should not
            # be filled
            return None

    def to_xml_add_children(self, base):
        # add all children to base element
        for element in self.elements.values():
            element.to_xml(base)

    @classmethod
    def create(cls, element, rtml, name=None, uid=None):
        return cls(rtml, name=name, uid=uid)

    def from_xml(self, xml, rtml):
        # loop all nodes
        for el in xml:
            # strip namespace
            tag = el.tag.split('}', 1)[1] if '}' in el.tag else el.tag

            # got name?
            name = el.attrib['name'] if 'name' in el.attrib else None

            # just a ref?
            if 'ref' in el.attrib:
                # get ref
                uid = el.attrib['ref']

                # store it
                self.refs_to_resolve.append(uid)
            else:
                # get id
                uid = el.attrib['id'] if 'id' in el.attrib else None

                # try to get class
                try:
                    klass = getattr(rtmlparse.elements, tag)
                except AttributeError as e:
                    continue

                # is it a BaseElement and not History?
                if issubclass(klass, BaseElement) and not issubclass(klass, rtmlparse.elements.History):
                    obj = klass.create(el, rtml, name=name, uid=uid)

                    # if rtml is not myself, add it
                    if rtml != self:
                        self.add_element(obj)

                    # go deeper
                    obj.from_xml(el, rtml)

    def resolve_refs(self, elements):
        # start with all children
        for el in self.elements.values():
            el.resolve_refs(elements)

        # if this is RTML, return here
        if self.name == 'RTML':
            return

        # loop all references
        for ref in self.refs_to_resolve:
            if ref in elements:
                # found it, add it
                self.add_element(elements[ref])
            else:
                # something went wrong
                raise RuntimeError("Could not find object with ref '{0:s}'.".format(ref))

    def reset_processed(self):
        self.processed = False
        for el in self.elements.values():
            el.reset_processed()

    def reference_count(self):
        # init
        refcount = {self.uid: 1}

        # processed already?
        if self.processed:
            return refcount

        # loop all elements
        for element in self.elements.values():
            for uid, count in element.reference_count().iteritems():
                if uid in refcount:
                    refcount[uid] += count
                else:
                    refcount[uid] = count

        # return it
        self.processed = True
        return refcount

    def add_element(self, element):
        # if valid_element_type is a boolean then we use that value directly
        if isinstance(self.valid_element_types, bool):
            valid = self.valid_element_types
        else:
            # check type
            valid = False
            for t in self.valid_element_types:
                if isinstance(element, t):
                    valid = True
                    break

        # not found?
        if not valid:
            raise ValueError("Element of type '{0:s}' cannot be added to element of type '{1:s}'."
                             .format(element.tagname, self.tagname))

        # exists already?
        if element.uid in self.elements:
            return

        # add it
        self.elements[element.uid] = element
        if self.rtml is not None:
            self.rtml.add_element(element)

    def filtered(self, types=[]):
        # loop all elements
        elements = {}
        for uid, element in self.elements.iteritems():
            # is type in list?
            valid = False
            for t in types:
                if isinstance(element, t):
                    valid = True
                    break
            # add it
            if valid:
                elements[uid] = element
        # return list
        return elements

    def find(self, type=None, name=None):
        # loop all elements
        filtered = {}
        for uid, element in self.elements.iteritems():
            # decide whether we want it or not
            match = True

            # decide on type
            if type is not None and not isinstance(element, type):
                match = False

            # decide on name
            if name is not None and name != element.name:
                match = False

            # got match?
            if match:
                filtered[uid] = element

        # finished
        return filtered

    def find_first(self, type=None, name=None):
        filtered = self.find(type=type, name=name)
        if len(filtered) == 0:
            return None
        return filtered.values()[0]

    @property
    def gratings(self):
        from .grating import Grating
        return {k: v for k, v in self.elements.iteritems() if isinstance(v, Grating)}

    @property
    def detectors(self):
        from .detector import Detector
        return {k: v for k, v in self.elements.iteritems() if isinstance(v, Detector)}

    @property
    def targets(self):
        from .target import Target
        return {k: v for k, v in self.elements.iteritems() if isinstance(v, Target)}

    @property
    def spectrographs(self):
        from .spectrograph import Spectrograph
        return {k: v for k, v in self.elements.iteritems() if isinstance(v, Spectrograph)}

    @property
    def telescopes(self):
        from .telescope import Telescope
        return {k: v for k, v in self.elements.iteritems() if isinstance(v, Telescope)}

    @staticmethod
    def add_text_value(element, tagname, value, fmt='s', attrib={}, namespace=''):
        if value is not None:
            # create element
            el = etree.SubElement(element, namespace + tagname)
            # set text
            # el.text = ('{0:' + fmt + '}').format(value)
            el.text = str(value)
            # set attributes
            for key, val in attrib.iteritems():
                el.attrib[key] = val

    @staticmethod
    def from_text_value(element, tagname, type=str, namespace=''):
        el = element.find(namespace + tagname)
        return type(el.text) if el is not None else None

    @staticmethod
    def add_enum_value(element, tagname, value, namespace=''):
        if value is not None:
            # create element and set text
            etree.SubElement(element, namespace + tagname).text = value.value

    @staticmethod
    def from_enum_value(element, tagname, type, namespace=''):
        return BaseElement.from_text_value(element, tagname, type, namespace=namespace)

    @staticmethod
    def add_unit_value(element, tagname, value, namespace=''):
        if value is not None:
            value.to_xml(element, tagname, namespace=namespace)

    @staticmethod
    def from_unit_value(element, tagname, type, namespace=''):
        return type.from_xml(element, tagname, namespace=namespace)

    @staticmethod
    def add_xy_value(element, tagname, value, namespace=''):
        if value is not None:
            # create element
            el = etree.SubElement(namespace + element, tagname)
            # create X/Y
            etree.SubElement(el, namespace + 'X').text = str(value[0])
            etree.SubElement(el, namespace + 'Y').text = str(value[1])

    @staticmethod
    def from_xy_value(element, tagname, namespace=''):
        el = element.find(namespace + tagname)
        if el is None:
            return None
        x = float(el.find(namespace + 'X').text)
        y = float(el.find(namespace + 'Y').text)
        return x, y

    def _get_one_element(self, element_type):
        # find all elements of this type
        elements = self.find(element_type)
        # check count
        if len(elements) == 0:
            return None
        else:
            if len(elements) > 1:
                warnings.warn("Multiple {0:s} elements are not supported. Use find().".format(element_type.__name__),
                              RuntimeWarning)
            return elements.values()[0]

    def _set_one_element(self, element_type, value):
        # check type first
        if not isinstance(value, element_type):
            raise ValueError("Value must be of type '{0:s}.".format(element_type.__name__))
        # get all elements
        elements = self.find(element_type)
        # more than 1?
        if len(elements) > 1:
            warnings.warn("Multiple {0:s} elements are not supported. Deleting all.".format(element_type.__name__),
                          RuntimeWarning)
        # delete all
        for uid in elements:
            self.delete(uid) if self.tagname == 'RTML' else self.rtml.delete(uid)
        # add new element
        self.add_element(value)
