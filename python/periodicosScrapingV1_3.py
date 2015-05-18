# -*- coding: utf-8 -*-
"""
Created on Mon May 11 09:26:46 2015

@author: bluecap
mas de periodicos scraping - con import.io
"""

import requests
import MySQLdb
import string
from bs4 import BeautifulSoup
import re
import re
import time
import sys
import os
import urllib2
import pygoogle
from mechanize import Browser
import nltk
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

os.chdir("C:\\Users\\bluecap\\Desktop\\bluecap\\project\\scrapper\\python")
url="http://www.20minutos.es/busqueda"

badTerms = ["SL", "SA", "S.L.", "SOCIEDAD", "ANONIMA", "LIMITADA", "SCCL"]

def nombresLimpiador(nombresVec, terms) :
    nombresNuevos = []
    punct = set(string.punctuation)
    if type(nombresVec) == list :
        for nom in nombresVec :
            nomList = nom.split()
            nomNew = [''.join(x for x in a if x not in punct) for a in nomList if a not in terms]
            nombresNuevos.append(" ".join(nomNew))  
            #print "shouldnt be this"
    else : 
        #print "should be this"
        nomList = nombresVec.split()
        nomNew = [''.join(x for x in a if x not in punct) for a in nomList if a not in terms]
        nombresNuevos = " ".join(nomNew)
        
    return(nombresNuevos)

def elCorrerUrlMaker(query, badTerms) :
    baseUrl = "http://www.elcorreo.com/hemeroteca/noticia/"
    query1 = nombresLimpiador(query, badTerms)
    print query1
    temp = query1.split()
    addition = "%20".join(a for a in temp)
    finalUrl = baseUrl+addition+".html?pag=1"
    return finalUrl
    
        
    
    
class DarmeNoticiasElCorreo():
    def __init__(self, sourceUrl, nombre, badTerms):
        self.startQ = nombre           
        self.myNom = nombre
        self.baseUrl = sourceUrl
        self.terms = badTerms
        
    def myLimpiador(self, terms) :
        punct = set(string.punctuation)
        nomList = self.myNom.split()
        nomNew = [''.join(x for x in a if x not in punct) for a in nomList if a not in terms]
        nombresNuevos = " ".join(nomNew)
        self.myNom = nombresNuevos
        
        
    def elCorrerUrlMaker(self, query, badTerms) :
        baseUrl = self.baseUrl
        query1 = self.myLimpiador(query, badTerms)
        temp = query1.split()
        addition = "%20".join(a for a in temp)
        finalUrl = baseUrl+addition+".html?pag=1"
        self.startQ = finalUrl
        
    def getResults(self, tag) :
    # se hace un dataframe con 1. url, 2. titulo, 3. un descripcion corto, 4. el texto del articulo
    # .article.not_Aut
        driver = webdriver.Chrome()

        driver.get(self.elCorrerUrlMaker(self.myLimpiador(self.terms), self.terms))
        baseText = driver.find_elements_by_css_selector(tag)
        
        while len(baseText) == 0 :
            print "....Comprobando si base text se funcciona...."
            baseText = driver.find_elements_by_css_selector('.gsc-tabdActive')
    
        resultados = 
        
        
testUrl = "http://www.elcorreo.com/hemeroteca/noticia/SOC%20Y%20PORTA.html?pag=1"
driver = webdriver.Chrome()
driver.get(testUrl)
baseText = driver.find_elements_by_css_selector(".not_Aut")
baseText1 = driver.find_element_by_css_selector(".noticiaH")
