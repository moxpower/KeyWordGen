import unicodecsv
import csv
from os.path import join, dirname, abspath
import os
import fnmatch
import re
import pandas as pd
import time
from nltk.corpus import stopwords
import string

#read csv file directory
redundandwords = join(dirname(abspath('__file__')), 'gabikeywordsfinal.txt')
redundandwordsexcluded = join(dirname(abspath('__file__')), 'redundandwords.txt')
#redundandwords = join(dirname(abspath('__file__')), 'redundandwords1.txt')

alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
abc=list(alphabet)
pattern='|'.join(abc)

with open(redundandwords) as f:
    redexpressions = f.readlines()
    redex=''.join(redexpressions).split(' ')
    redex1=[s.decode('utf8') for s in redex]

with open(redundandwordsexcluded) as f:
    redexpressionsexc = f.readlines()
    redexexc=''.join(redexpressionsexc).split(' ')
    redex1exc=[s.decode('utf8') for s in redexexc]

emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""

regex_str = [r'(?:[\w_]+)']

"""
regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
 
    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]"""
    
tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.UNICODE | re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)

def tokenize(s):
    return tokens_re.findall(s)
 
def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens


def unique_list(l):
    ulist = []
    [ulist.append(x) for x in l if x not in ulist]
    return ulist



punctuation = list(string.punctuation)
stop = stopwords.words('english') + punctuation + abc + stopwords.words('german') + ['rt','via',':','RT',u'\u2026', u'\ud83d', u'\xfcck']
redundand = ['1','2','3','4','5','6','7','8','9','0','/',"\\",'!','?','+',':',',','[',']','(',')',"'",'.','_','-','csv','xlsx','txt',"´"]

keywordsfile = join(dirname(abspath('__file__')), 'KeyWordsList.csv')
directoryfile = join(dirname(abspath('__file__')), 'ProjectDirectoryList.csv')

#read links to be crawled
df=pd.read_csv(directoryfile, header=None, names=['Proj_No','Directory'], sep=';', nrows=20000, error_bad_lines=False)
#df['Directory']=df['Directory'].str.replace("P:/Projekte/","")
df['Directory']=df['Directory'].str.lstrip("\\bonanza\PE\Projekte/")
df['Lstring']="P:/Projekte/"
df['Newdir']=df['Lstring'] + df['Directory']
df['Newdir']=df['Newdir'].str.replace('/',"\\")
df=df[df['Proj_No'].apply(str).str.pad(6, side='left').str[3:]<>"000"]
linktest = df['Newdir'][df['Directory'].str.contains(pattern)].values
proj_no = df['Proj_No'][df['Directory'].str.contains(pattern)].values
#proj_no = proj_notest [1:10]
newindex=13001
newindexstop=newindex+1000
print(newindexstop+1)
links = linktest[newindex:newindexstop]


#def keywords(link): , encoding='utf-8'
with open(keywordsfile,'a') as f:
    try:
        w=unicodecsv.writer(f, delimiter=",", encoding='utf-8')
        for index,link in enumerate(links):
            #start=time.time()
            #while time.time() < start + 5:
            matches = []
            arr1 = []
            result = []
            msg = []
            globalindex=index+newindex
            pdindex=proj_no[globalindex]
            for root, dirs, files in os.walk(link.decode('latin-1').encode('utf8'), topdown=False):
                """if time.time() > start + 2:
                    break
                else:"""
                    #while time.time() < start + 5:
                for name in files:
                        #substitute link from root at this level
                    entry1=os.path.join(root.replace("P:\\Projekte\\",''), name)
                    matches.append(entry1)
                for name in dirs:
                    entry2=os.path.join(root.replace("P:\\Projekte\\",''), name)
                    matches.append(entry2)
                        #das hier unten nach links
            arr1=''.join(matches)
            big_regex = re.compile('|'.join(map(re.escape, redundand)))
            the_message = big_regex.sub(" ",str(arr1))
            msg=' '.join(unique_list(str(the_message).split()))
            msg=[term.lower() for term in preprocess(msg) if unicode(term, 'utf-8', errors='ignore').lower() in redex1 if unicode(term, 'utf-8', errors='ignore').lower() not in redex1exc if unicode(term, 'utf-8', errors='ignore').lower() not in stop]
            msg=' '.join(msg)
            w.writerow([pdindex,len(msg), msg])
#            w.writerow([proj_no[index],str(arr1)])
    except:
        print(proj_no[globalindex])
