from lxml import etree
from datetime import datetime

from .baseelement import BaseElement
from .misc import auto_attr_check


@auto_attr_check
class Entry(BaseElement):
    Agent = str
    Date = datetime
    Description = str
    Error = str
    Rejection = str
    Version = int

    def __init__(self, parent, name=None, uid=None, agent='unknown', date=None, description=None, error=None, rejection=None, version=None):
        BaseElement.__init__(self, 'Entry', parent, name=None, uid=None)
        self.Agent = agent
        self.Date = datetime.utcnow() if date is None else date
        self.Description = description
        self.Error = error
        self.Rejection = rejection
        self.Version = version

    def to_xml(self, parent, add_children=True):
        # add element
        element = BaseElement.to_xml(self, parent, add_children=add_children)
        if element is None:
            return None
        ns = '{' + self.rtml.namespace + '}'

        # other stuff
        element.attrib['timeStamp'] = self.Date.strftime("%Y-%m-%dT%H:%M:%S")
        self.add_text_value(element, 'Agent', None, attrib={'name': self.Agent}, namespace=ns)

        # other fields
        self.add_text_value(element, 'Description', self.Description, namespace=ns)
        self.add_text_value(element, 'Error', self.Error, namespace=ns)
        #self.add_text_value(element, 'Rejection', self.Rejection, namespace=ns)
        self.add_text_value(element, 'Version', self.Version, 'd', namespace=ns)

        # return base element
        return element

    def from_xml(self, element, rtml):
        # base call
        BaseElement.from_xml(self, element, rtml)
        ns = '{' + rtml.namespace + '}'

        # agent
        agent = element.find(ns + 'Agent')
        if agent is not None:
            self.Agent = agent.attrib['name']

        # other stuff
        self.Date = datetime.strptime(element.attrib['timeStamp'], "%Y-%m-%dT%H:%M:%S")
        self.Description = self.from_text_value(element, 'Description', str, namespace=ns)
        self.Error = self.from_text_value(element, 'Error', float, namespace=ns)
        self.Version = self.from_text_value(element, 'Version', int, namespace=ns)

