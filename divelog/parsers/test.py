"""
Test script for divelog parsers.
"""
import os
from datetime import datetime

def DATA(filename):
    data_dir = os.path.join(os.path.dirname(__file__), '../data')
    return os.path.abspath(os.path.join(data_dir, filename))

os.environ['DJANGO_SETTINGS_MODULE'] = 'divelog.settings'

from divelog.parsers import subsurface

def run():
    path = DATA('subsurface-1.xml')
    
    start = datetime.now()
    p = subsurface.parse_short(path)
    print "Parse short taken: ", datetime.now() - start
    
    print p
    
    start = datetime.now()
    p = subsurface.parse_full(path)
    print "Parse full taken: ", datetime.now() - start
    
    print [(x[0], len(x[1])) for x in p]

if __name__ == '__main__':
    run()
#    cProfile.run('run()')
