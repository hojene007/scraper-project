# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 00:08:38 2015

@author: Stephen Carmody


# NOTE!!! Used a custom dict as it was too slow with full scale dictionaries !!!!!!!!!
"""
import os
import pandas as pd
import csv
from class_functions import RawDocs2

os.chdir("C:\\Users\\Epoch\\Desktop\\BGSE\\mining\\tutorials\\Homework_2_Levein_Carmody_Kryrzanowska")


dataZH = pd.read_table("textDataZeroHedge.txt",encoding="utf-8",error_bad_lines=False)
dataRT = pd.read_table("textDataReuters.txt",encoding="utf-8",error_bad_lines=False)
stopW = open("stopwords.txt")


print dataZH.columns, dataZH.shape
print dataRT.columns, dataRT.shape

allData = dataZH.append(dataRT)

data = allData[pd.notnull(allData['text'])]
data['temp'] = data.text.str.len()
data = data[data.temp>11]
del data['temp']


reutersData = data.loc[data['source'] == "reuters"]
zeroHedgeData = data.loc[data['source'] == "zerohedge"]

with open('LoughranMcDonald_MasterDictionary_2014.csv', 'rb') as f:
    reader = csv.reader(f)
    MasterDict = list(reader)
    
i = len(MasterDict)
dict_list = zip(xrange(0,i), MasterDict)
MasterDict = dict(dict_list)


from itertools import islice

def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))
    
n_items = take(100, MasterDict.iteritems())
i = len(n_items)
dict_list = zip(xrange(0,i), n_items)
MasterDict = dict(dict_list)


dict4 = ["iraq", "government", "bonds", "budget", "deficit", "finance", "russia"]
dict5 = MasterDict

def cleanData(myClass):
    docsobj = myClass

    ###### step 1 ######
    
    all_terms = [t for d in docsobj.tokens for t in d]
    print "# tokens = ", len(all_terms)
    print "# unique tokens = ", len(set(all_terms))
    print "\n"
    
    ###### step 2 ######
    
    docsobj.token_clean(0)
    all_terms = [t for d in docsobj.tokens for t in d]
    print "# alpha tokens = ", len(all_terms)
    print "# unique alpha tokens = ", len(set(all_terms))
    print "\n"
    
    ###### step 3 ######
    
    docsobj.token_clean(1)
    docsobj.stopword_remove()
    all_terms = [t for d in docsobj.tokens for t in d]
    print "# alpha tokens without stopwords = ", len(all_terms)
    print "# unique alpha tokens without stopwords = ", len(set(all_terms))
    print "\n"
    
    ###### step 4 ######
    
    docsobj.stem()
    all_terms = [t for d in docsobj.stems for t in d]
    print "# stems = ", len(all_terms)
    print "# unique stems = ", len(set(all_terms))
    print '\n'
    
    tok = docsobj.tokens
    doc = docsobj.docs
    
    testCount = docsobj.count3(dict4)
    testIf = docsobj.if_idf(dict4)
    
    #Converts to Dataframe
    testCount_df = pd.DataFrame.from_dict(testCount, orient = 'index')
    dfIfIdf = pd.DataFrame.from_dict(testIf, orient = 'index')
    #Gets score per document
    results = dfIfIdf.sum()/len(dfIfIdf.index)
    testCount_df = testCount_df.sum()/len(testCount_df.index)
    print(results)
    
    return results, testCount_df



docsobj = RawDocs2(data.text, "stopwords.txt")
docsobjZH = RawDocs2(zeroHedgeData.text, "stopwords.txt")
docsobjRT = RawDocs2(reutersData.text, "stopwords.txt")

ZH_tf_idf,ZH_count = cleanData( docsobjZH)
RT_tf_idf,RT_count = cleanData( docsobjRT)


