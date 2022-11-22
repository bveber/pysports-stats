import os
from pyquery import PyQuery as pq


def read_file(filename, sport, stat_type):
    filepath = os.path.join(os.path.dirname(__file__), stat_type, sport, filename)
    return pq(open('%s' % filepath, 'r', encoding='utf8').read())