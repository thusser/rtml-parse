from lxml import etree
from datetime import datetime

from .baseelement import BaseElement


class History(BaseElement):
    def __init__(self, parent, name=None, uid=None, agent='unknown', date=None, description=None, error=None, rejection=None, version=None):
        BaseElement.__init__(self, 'Entry', parent, name=None, uid=False)
        self.Agent = agent
        self.Date = datetime.utcnow() if date is None else date
        self.Description = description
        self.Error = error
        self.Rejection = rejection
        self.Version = version

    def to_xml(self, parent):
        # add Entry and Agent
        entry = etree.SubElement(parent, 'Entry', attrib={'timeStamp': self.Date.strftime("%Y-%m-%dT%H:%M:%S")})
        etree.SubElement(entry, 'Agent', attrib={'name': self.Agent})

        # other fields
        self.add_text_value(entry, 'Description', self.Description)
        self.add_text_value(entry, 'Error', self.Error)
        #self.add_text_value(entry, 'Rejection', self.Rejection)
        self.add_text_value(entry, 'Version', self.Version, 'd')

    def from_xml(self, xml, rtml):
        # namespace
        ns = '{' + rtml.namespace + '}'

        # get timestamp and agent
        self.Date = datetime.strptime(xml.attrib['timeStamp'], "%Y-%m-%dT%H:%M:%S")
        agent = xml.find(ns + 'Agent')
        if agent is not None:
            self.Agent = agent.attrib['name']

        # others
        self.Description = self.from_text_value(xml, ns + 'Description')
        self.Error = self.from_text_value(xml, ns + 'Error')
        #self.Rejection = self.from_text_value(xml, ns + 'Rejection')
        self.Version = self.from_text_value(xml, ns + 'Version', int)


