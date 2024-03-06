# server.py
from xmlrpc.server import SimpleXMLRPCServer
import datetime
import xml.etree.ElementTree as ET
import requests
## help found here https://www.tutorialspoint.com/create-xml-documents-using-python
## and here https://docs.python.org/3/library/xml.etree.elementtree.html
class NoteBook:
    def __init__(self):
        self.database = "notebook.xml"
        self.tree = ET.parse(self.database)
        self.root = self.tree.getroot()
        self.URL = "https://en.wikipedia.org/w/api.php"
        self.S = requests.Session()
    def printOut(self, topic):
        return topic
    
    def save_to_xml(self):
        self.tree.write(self.database)
    
    def addNote(self, topic,name, text):
        child =self.findTopic(topic)
        if len(child)!=0:
            self.makeNote(child, name, text, 0)
            return True
        topic_elem = ET.Element('topic') ## make note xml structure
        topic_elem.set('name', topic)
        self.makeNote(topic_elem, name, text, 1)
        return True
    
    def getNotesByTopic(self, topic):
        foundNotes = []
        child =self.findTopic(topic)
        if len(child)!=0:
            for note in child.findall('note'):
                foundNote = {
                    'note': note.get('name'),
                    'text': note.find('text').text,
                    'timestamp': note.find('timestamp').text
                }
                foundNotes.append(foundNote)
        return foundNotes
    
    def findFromWikiApi(self, searchTerm, topic):
        PARAMS = { ## Cannot get the descriptions because this is said on the site "On Wikimedia wikis descriptions are disabled due to performance reasons, so the second array only contains empty strings"
            ##https://www.mediawiki.org/wiki/API:Opensearch
            "action": "opensearch",
            "namespace": "0",
            "search": searchTerm,
            "limit": "3",
            "format": "json"
        }
        R = self.S.get(url=self.URL, params=PARAMS)
        if(R):
            DATA = R.json()
            self.addNote(topic, searchTerm, DATA[3][0])
            
        
    
    def makeNote(self,topic_elem, name, text, new):
        note_elem = ET.SubElement(topic_elem, 'note')
        note_elem.set('name',name) ## add topic
        text_elem = ET.SubElement(note_elem, 'text')
        text_elem.text = text ## add text to note
        timestamp_elem = ET.SubElement(note_elem, 'timestamp')
        timestamp_elem.text = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') ##add timestamp
        if new:
            self.root.append(topic_elem)
        self.save_to_xml()

    def findTopic(self,name):
        for child in self.root.findall('topic'):
            topic_name = child.get('name')
            if topic_name == name:
                return child
        return ""

if __name__ == '__main__':
    server = SimpleXMLRPCServer(('localhost', 8000), allow_none=True)
    server.register_instance(NoteBook())
    print("Server started on localhost:8000...")
    server.serve_forever()