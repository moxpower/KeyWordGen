

import unicodecsv
import csv
from os.path import join, dirname, abspath
import os

dirfile = join(dirname(abspath('__file__')), 'ProjectDirectoryList.csv')


def walklevel(some_dir, level):
    some_dir = some_dir.rstrip(os.path.sep)
    num_sep = some_dir.count(os.path.sep)
    for root, dirs, files in os.walk(some_dir):
        yield root, dirs, files
        num_sep_this = root.count(os.path.sep)
        if num_sep + level <= num_sep_this:
            del dirs[:] 
 
levels=[1,2]
rootdir = "A:\Projekte"
with open(dirfile,'w') as f:
    w=unicodecsv.writer(f, delimiter=",", encoding='utf-8')
    for level in levels:
        for root,dirs,files in walklevel(rootdir,level):
            for dir in dirs:
                if dir[1].isdigit():
                    if os.path.join(root,dir).count(dir[:5])>0:
                    #if root.count('\\')>2: # http://stackoverflow.com/questions/1155617/count-occurrence-of-a-character-in-a-string
                        w.writerow([dir[:5],os.path.join(root,dir).replace('\\','/')])

