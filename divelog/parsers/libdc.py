from xml.etree import cElementTree
from divelog.models import Dive

# Implementation for files, does not work with in memory uploads
#def parse_short(fp):
#    dives = []
#    with open(fp, 'r') as file:
#        for event, elem in cElementTree.iterparse(file):
#            if elem.tag == "dive":
#                dive = {}
#                for child in elem:
#                    if child.tag == 'gasmix':
#                        pass
#                    if child.tag == 'sample':
#                        break # skip processing other samples
#                    else:
#                        dive[child.tag] = child.text
#                        pass
#                elem.clear()
#                dives.append(dive)
#    return dives

def parse_short(data):
    dives = []
    root = cElementTree.fromstring(data)
    for element in root:
        if element.tag == "dive":
            dive = {}
            for child in element:
                if child.tag == 'sample':
                    break
                if child.tag == 'gasmix':
                    pass
                else:
                    dive[child.tag] = child.text
                    pass
            element.clear()
        dives.append(dive)
    return dives

def parse_full(self, data):
    dives = []
    root = cElementTree.fromstring(data)
    for element in root:
        if element.tag == "dive":
            dive = Dive()
            for child in element:
                if child.tag == 'sample':
                    break
                if child.tag == 'gasmix':
                    pass
                else:
                    dive[child.tag] = child.text
                    pass
            element.clear()
        dives.append(dive)
    return dives
    
