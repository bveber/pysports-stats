import os
from pyquery import PyQuery as pq


def read_file(filename, sport, stat_type):
    filepath = os.path.join(os.path.dirname(__file__), stat_type, sport, filename)
    file_contents = open('%s' % filepath, 'r', encoding='utf8').read()
    return pq(file_contents)