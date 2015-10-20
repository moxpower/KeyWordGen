import unicodecsv
import csv
from os.path import join, dirname, abspath
import os
import fnmatch
import re
import pandas as pd

#read csv file directory

alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
abc=list(alphabet)
pattern='|'.join(abc)
#get column with links
#parse links in array links
#parse projectnumber in array project number
#index link, return projectnumber
#save project number and link
#links = ["P:\\Projekte\\17000\\1703 - APC","."]
redundand = ['1','2','3','4','5','6','7','8','9','0','/',"\\",':',',','[',']','(',')',"'",'.','_','-','csv','xlsx','txt']
keywordsfile = join(dirname(abspath('__file__')), 'KeyWordsList.csv')
directoryfile = join(dirname(abspath('__file__')), 'ProjectDirectoryList.csv')

#read links to be crawled
df=pd.read_csv(directoryfile, header=None, names=['Proj_No','Directory'], sep=',', nrows=20000, error_bad_lines=False)
df['Directory']=df['Directory'].str.replace("A:/Projekte/","")
df['Lstring']="A:/Projekte/"
df['Newdir']=df['Lstring'] + df['Directory']
df['Newdir']=df['Newdir'].str.replace('/',"\\")
linkstest = df['Newdir'][df['Directory'].str.contains(pattern)].values
links = linkstest[1:3]


#def keywords(link):
with open(keywordsfile,'w') as f:
    try:
        w=unicodecsv.writer(f, delimiter=",", encoding='utf-8')
        for link in links:
            matches = []
            arr1 = []
            result = []
            msg = []
            for root, dirs, files in os.walk(link, topdown=False):
                for name in files:
                    entry1=os.path.join(root, name)
                    matches.append(entry1)
                for name in dirs:
                    entry2=os.path.join(root, name)
                    matches.append(entry2)
                arr1=[''.join(matches)]
                big_regex = re.compile('|'.join(map(re.escape, redundand)))
                the_message = big_regex.sub(" ",str(arr1))
                msg=' '.join(unique_list(str(the_message).split()))
            w.writerow([msg])
    except:
        print "whatever"
