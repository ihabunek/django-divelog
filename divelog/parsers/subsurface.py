"""
Parser functions for the subsurface XML format.

http://subsurface.hohndel.org/
"""

from datetime import datetime
from xml.etree import cElementTree
import cProfile
import os

#if __name__ == '__main__':
#    os.environ['DJANGO_SETTINGS_MODULE'] = 'divelog.settings'

from divelog.models import Dive, Sample, Event

def parse_short(path):
    dives = []
    with open(path, 'r') as file:
        for event, node in cElementTree.iterparse(file):
            if node.tag == "dive":
                dive = {
                    'number': node.get('number'),
                    'date_time': _datetime(node.get('date'), node.get('time')),
                    'duration': _duration(node.get('duration')),
                }
                for child in node:
                    if child.tag == 'depth':
                        dive['max_depth'] = _depth(child.get('max'))
                        dive['avg_depth'] = _depth(child.get('mean'))
                    elif child.tag == 'temperature':
                        dive['temperature'] = _temp(child.get('water'))
                    elif child.tag == 'location':
                        dive['location'] = child.text
                    elif child.tag == 'sample':
                        break # skip processing other samples
                dives.append(dive)
    return dives

def parse_full(path):
    dives = []
    samples = []
    with open(path, 'r') as file:
        for event, node in cElementTree.iterparse(file):
            if node.tag == "dive":
                dive = Dive()
                dive.number = int(node.get('number'))
                dive.date_time = _datetime(node.get('date'), node.get('time'))
                dive.duration = _duration(node.get('duration'))
                
                samples = []
                
                for child in node:
                    if child.tag == 'depth':
                        dive.max_depth = _depth(child.get('max'))
                        dive.avg_depth = _depth(child.get('mean'))
                    elif child.tag == 'temperature':
                        dive.temperature = _temp(child.get('water'))
                    elif child.tag == 'location':
                        dive.location = child.text
                    elif child.tag == 'sample':
                        sample = Sample()
                        #sample.dive = dive
                        sample.time = _duration(child.get('time'))
                        sample.depth = _depth(child.get('depth'))
                        
                        # Parse the temperature or copy from last sample if not present
                        temp = child.get('temp')
                        if temp:
                            sample.temperature = _temp(temp)
                        elif samples:
                            sample.temperature = samples[-1].temperature

                        samples.append(sample)

                dives.append((dive, samples))
    return dives

def _duration(value):
    """
    Converts a given time duration to the equivalent number of seconds.
    @param value: A string in 'mm:ss min' format, e.g. '10:31 min'. 
    """
    minutes = int(value[-6:-4])
    seconds = int(value[:-7])
    return 60 * minutes + seconds 

def _datetime(date, time):
    """
    Converts given date and time into a datetime object.
    @param date: Date string in yyyy-mm-dd format.
    @param time: Time string in mm:hh:ss format. 
    """
    dt = date + time
    return datetime.strptime(dt, '%Y-%m-%d%H:%M:%S')

def _depth(value):
    "Converts a depth string '##.## m' to float"
    return float(value[:-2])

def _temp(value):
    "Converts a temperature string '##.## C' to float"
    return float(value[:-2])

#def run():
#    start = datetime.now()
#    p = parse_full('d:/Dropbox/divecomputer/divelog-1.xml')
#    end = datetime.now()
#    print end - start
#    print [(x[0], len(x[1])) for x in p]
#
#if __name__ == '__main__':
##    run()
#    cProfile.run('run()')
