# -*- coding: utf-8 -*-
"""
Created on Tue May 12 11:58:38 2015

@author: bluecap
"""

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import requests
import MySQLdb
import string
from bs4 import BeautifulSoup
import re
import re
import time
import sys
import os
import nltk
import pandas as pd
import numpy as np

def Expansion(key, wait=2) :
    driver = webdriver.Chrome()

        # go to the google home page
    driver.get("http://www.expansion.com")
    # find the element that's name attribute is q (the google search box)
    inputElement = driver.find_element_by_id("buscar")
    # type in the search
    inputElement.send_keys(key)
    # submit the form (although google automatically searches now without submitting)
    inputElement.submit()
    time.sleep(wait) # <----  no se funciona sin esto
    resultados = []
    
    try:
        #Nos movemos a lo largo de todos los resultados de la búsqueda extrayendo la info 
        for res in driver.find_elements_by_css_selector('.detalle_noticia_busqueda'):
            noticia = {}
            titulo = res.find_element_by_css_selector('h2').text
            link = res.find_element_by_css_selector('a').get_attribute('href')
            fecha = res.find_element_by_css_selector('span.firma').text
            fuente = "Expansion"
            parrafo = res.find_element_by_css_selector(*'p').text
            noticia['Empresa']=key
            noticia['titulo']=titulo
            noticia['link']=link
            noticia['fecha']=fecha
            noticia['autor']=fuente
            noticia['parrafo']=parrafo
            resultados.append(noticia)
        time.sleep(wait)
        driver.close()
        return(resultados)
        
    except:
        print('Ha ocurrido un error con la busqueda de '+key)
        print("Unexpected error:", sys.exc_info()[0])
        time.sleep(2)
        
    
tryApple = Expansion("apple", wait=2)