# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 22:41:17 2015

@author: Epoch
classes functions tutorial
"""

import codecs,re
from nltk.tokenize import wordpunct_tokenize
from nltk import PorterStemmer
import pandas as pd
import numpy as np


          
  
  
class RawDocs2():

	def __init__(self, doc_data, stopword_file):

		self.docs = [s.lower() for s in doc_data]

		with codecs.open(stopword_file,'r','utf-8') as f: raw = f.read()
		self.stopwords = set(raw.splitlines())

		self.docs = map(lambda x: re.sub(u'[\u2019\']', '', x), self.docs)

		self.N = len(self.docs)
		self.tokens = map(wordpunct_tokenize,self.docs)


	def token_clean(self,length):

		""" 
		strip out non-alpha tokens and length one tokens
		"""

		def clean(tokens): return [t for t in tokens if t.isalpha() == 1 and len(t) > length]

		self.tokens = map(clean,self.tokens)


	def stopword_remove(self):

		"""
		Remove stopwords from tokens.
		"""

		def remove(tokens): return [t for t in tokens if t not in self.stopwords]
		self.tokens = map(remove,self.tokens)


	def stem(self):

		"""
		Stem tokens with Porter Stemmer.
		"""

		def s(tokens): return [PorterStemmer().stem(t) for t in tokens]
		self.stems = map(s,self.tokens)
  
	
          
	def count3(self, dictionary):
          indList = []
          fullDict = {}
          for doc in self.tokens :
              df2 = {}
              ind = self.tokens.index(doc)
              indList.append(ind)
              docName1 = "docNo%s" % ind
              for v in dictionary :
                  df2[v]= 0
                  for tt in self.tokens[ind]:
                      if tt==v :
                          df2[v]=+1
                      
              fullDict[docName1] = df2
          return (fullDict)

              
          
	def if_idf(self, dictionary):
     # if_idf weighting 
         dfvVec = {}
         for v in dictionary :
             count2 = 0
             for tok in self.tokens:
               if v in tok :
                   count2=+1
             dfvVec[v]=count2
         idfVec = {}
         D =len(self.docs)
         llD = len(dictionary)
         for v in dictionary:
             df = dfvVec[v]
             if df == 0:
                 idfVec[v] = 1
             else:
                 idfVec[v]= np.log(D/df)
                 #print(np.log(D/df))
                 print "term %s out of %s for df" % dictionary.index(v), llD
             
         myDic = self.count3(dictionary)
         ifIdf = {}
         for doc in self.docs:
             ind = self.docs.index(doc)
             docName1 = "docNo%s" % ind
             tempD = {}
             try :
                 for v in myDic[docName1]:
                     tempD[v] = np.log(myDic[docName1][v]+1)*idfVec[v]
                     ifIdf[docName1] = tempD 
                 
             except KeyError:
                 ifIdf[docName1] = tempD
             print "document number %s" % ind
                         
                 
         return ifIdf
             
  
