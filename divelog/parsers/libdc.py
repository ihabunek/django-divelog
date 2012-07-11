"""
Parser function for the libdivecomputer XML format.
"""
from datetime import datetime
from divelog.models import Dive, Sample, Event
from django.utils.timezone import utc
from xml.etree import cElementTree
import logging

def parse_short(path):
    dives = []
    with open(path, 'r') as file:
        for event, node in cElementTree.iterparse(file):
            if node.tag == "dive":
                dive = {}
                for child in node:
                    if child.tag == 'gasmix':
                        pass
                    if child.tag == 'sample':
                        break # skip processing other samples
                    else:
                        dive[child.tag] = child.text
                        pass
                dives.append(dive)
    return dives

def parse_full(path):
    dives = []
    with open(path, 'r') as file:
        for event, elem in cElementTree.iterparse(file):
            if elem.tag == "dive":
                dives.append(parseDiveNode(elem))
                elem.clear()
    return dives

def parseDiveNode(diveNode):
    '''
    Parses a single dive from the dive log.
    @param xml: The dive data as an XML string (one <dive> node).
    @param parse_samples: If set to False, samples will not be parsed - quicker 
    '''

    samples = []
    events = []

    dive = Dive()
    for node in diveNode:
        if node.tag == 'number':
            dive.number = parseInt(node)
        elif node.tag == 'fingerprint':
            dive.fingerprint = node.text
        elif node.tag == 'size':
            dive.size = parseInt(node)
        elif node.tag == 'maxdepth':
            dive.max_depth = parseFloat(node)
        elif node.tag == 'datetime':
            dive.date_time = parseDateTime(node)
        elif node.tag == 'divetime':
            dive.duration = parseDuration(node)
        elif node.tag == 'sample':
            sample, new_events = parseSampleNode(node) 
            samples.append(sample)
            events += new_events
        elif node.tag == 'gasmix':
            pass
        else:
            logging.warning("unknown node: %s" % node.toxml())
    
    return (dive, samples, events)

def parseSampleNode(sampleNode):
    sample = Sample()
    events = []
    
    for node in sampleNode:
        if node.tag == 'depth':
            sample.depth = parseFloat(node)
        elif node.tag == 'time':
            sample.time = parseDuration(node)
        elif node.tag == 'temperature':
            sample.temperature = parseFloat(node)
        elif node.tag == 'bearing':
            pass
        elif node.tag == 'vendor':
            pass
        elif node.tag == 'event':
            event = Event()
            event.time = int(node.attributes['time'].value) # time within sample
            event.time += sample.time # add sample time to get actual time in dive
            event.text = node.childNodes[0].nodeValue
            
            if event.text != 'unknown':
                events.append(event)
        else:
            logging.warn("unknown: " + node.toxml()) 
            pass
    
    return sample, events

def parseInt(node):
    return int(node.text)

def parseFloat(node):
    return float(node.text)

def parseDuration(node):
    time = node.text.split(':')
    return int(time[0]) * 60 + int(time[1])

def parseDateTime(node):
    val = node.text
    return datetime.strptime(val, '%Y-%m-%d %H:%M:%S').replace(tzinfo=utc)
    