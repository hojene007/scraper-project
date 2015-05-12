# -*- coding: utf-8 -*-
"""
Created on Fri May 08 10:57:35 2015

esto script se leendo el baso de los datos de sql y tirando los nombres de las empresas - ahora solo para empresas con concurso
funcciona con 20minutos
"""

import requests
import MySQLdb
from bs4 import BeautifulSoup
import re
import re
import time
import sys
import os
import urllib2
import pygoogle
from mechanize import Browser
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

os.chdir("C:\\Users\\bluecap\\Desktop\\bluecap\\project\\scrapper\\python")
url="http://www.20minutos.es/busqueda"

#### Conectando a baso de datos y tirando empresas con concurso
host = "bluecap.cubz34n4knn2.eu-central-1.rds.amazonaws.com"
user = "bluecap"
password = "Bluecap2005"
dbname = "einformaDB"

db = MySQLdb.connect(host, user, password, dbname)
cursor = db.cursor()

queryConcurso = "SELECT * FROM einformaDB.Empresas where situacion like '%Concurso%';"

df = pd.read_sql(queryConcurso, db)
nombres = list(df['nombre_empresa'])

urlTest = "http://www.20minutos.es/busqueda/?q=apple"
driver = webdriver.Chrome()


def get20Minutos(url) :
    driver.get(urlTest)
    baseText = driver.find_elements_by_css_selector('.gsc-webResult') #esto linea necesita hacer dos vezes - no se         porque todavia
    baseText[1].text
    while len(baseText) == 0 :
        print "Comprobando si base text se funcciona"
        baseText = driver.find_elements_by_css_selector('.gsc-tabdActive')





