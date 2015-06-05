# -*- coding: utf-8 -*-
"""
Created on Tue May 12 09:56:57 2015

@author: bluecap
se usa Noticias.py para recolectar articulos mientras consiguiendo codigo en Noticias.py - tienes que correr los funciones por dentrolo anterior que corriendo estas aquí 
"""

import MySQLdb
import string
from bs4 import BeautifulSoup
import re
import re
import time
import sys
import os
from selenium import webdriver
import pandas as pd
#os.system("taskkill /im chrome.exe")

import sys  


#reload(sys)  
#sys.setdefaultencoding('utf-8')

global driver 
driver = webdriver.Chrome()




dictElPais = {}
dictElMundo = {}
dictExpansion = {}

ind = 0


noms = ["Banco Santander", "BBVA", "Telefónica", "Inditex", "Iberdrola", "Repsol", "Caixabank", "Gas Natural", "Amadeus IT Holding", "Ferrovial"]

try :
    for nom in noms :
        # para bigNoticias3 acabadó a 280
        if noms.index(nom) > -1 :     
                ind= noms.index(nom)
                
                
                print "...........Yendo a Expansion............"
                
                
                try :
                    expansionTemp = ExpansionTP2("'"+nom+"'", wait=2)
                    if len(expansionTemp) > 0 :
                        for link in expansionTemp :
                            index = expansionTemp.index(link)
                            print ".... cogiendo noticia %s de %s .....Expansion" % (index, len(expansionTemp))
                            if index != 0 and index%30 == 0:
                                driver.quit()
                                #os.system("taskkill /im chrome.exe")
                                driver = webdriver.Chrome()
                            link["texto"] = tiraText(str(link["link"]))
                            " going to link num. %s ... " % expansionTemp.index(link)
                except :
                    driver = webdriver.Chrome()
                    expansionTemp = ExpansionTP2("'"+nom+"'", wait=2)
                    if len(expansionTemp) > 0 :
                        for link in expansionTemp :
                            index = expansionTemp.index(link)
                            print ".... cogiendo noticia %s de %s .....Expansion" % (index, len(expansionTemp))
                            if index != 0 and index%30 == 0:
                                driver.quit()
                                #os.system("taskkill /im chrome.exe")
                                driver = webdriver.Chrome()
                            link["texto"] = tiraText(str(link["link"]))
                            " going to link num. %s ... " % expansionTemp.index(link)
                            
                            
                    
                print "...........Yendo a El Mundo............"
                
                
                
                try :
                    elmundoTemp = ElMundoTP2("'"+nom+"'", wait=2)
                    if len(elmundoTemp)> 0 :
                        for link in elmundoTemp :
                            index = elmundoTemp.index(link)
                            print ".... cogiendo noticia %s de %s .....El Mundo" % (index, len(elmundoTemp))
                            if index != 0 and index%30 == 0:
                                driver.quit()
                               # os.system("taskkill /im chrome.exe")
                                driver = webdriver.Chrome()
                            link["texto"] = tiraText(str(link["link"])) # seguiendo a cada vinculo
                except :
                    driver = webdriver.Chrome()
                    elmundoTemp = ElMundoTP2("'"+nom+"'", wait=2)
                    if len(elmundoTemp)> 0 :
                        for link in elmundoTemp :
                            index = elmundoTemp.index(link)
                            print ".... cogiendo noticia %s de %s .....El Mundo" % (index, len(elmundoTemp))
                            if index != 0 and index%30 == 0:
                                driver.quit()
                                #os.system("taskkill /im chrome.exe")
                                driver = webdriver.Chrome()
                            link["texto"] = tiraText(str(link["link"])) # seguiendo a cada vinculo
                            
                            
                    
                print "...........Yendo a El Pais............"   
                
                
                try :
                    elpaisTemp = ElPaisTP2("'"+nom+"'", wait =2) # variables temopranias que contenen la busqueda en cada periodoco empresa se llama "nom"
                    if len(elpaisTemp) > 0 :
                        for link in elpaisTemp :
                            index = elpaisTemp.index(link)
                            print ".... cogiendo noticia %s de %s .....El Pais" % (index, len(elpaisTemp))
                            if index != 0 and index%30 == 0:
                                driver.quit()
                                os.system("taskkill /im chrome.exe") # limpiando los procesos para no se paran chrome 
                                driver = webdriver.Chrome()
                            link["texto"] = tiraText(link["link"]) 
                except :
                    driver = webdriver.Chrome()
                    elpaisTemp = ElPaisTP2("'"+nom+"'", wait =2) # variables temopranias que contenen la busqueda en cada periodoco empresa se llama "nom"
                    if len(elpaisTemp) > 0 :
                        for link in elpaisTemp :
                            index = elpaisTemp.index(link)
                            print ".... cogiendo noticia %s de %s .....El Pais" % (index, len(elpaisTemp))
                            if index != 0 and index%30 == 0:
                                driver.quit()
                                os.system("taskkill /im chrome.exe") # limpiando los procesos para no se paran chrome 
                                driver = webdriver.Chrome()
                            link["texto"] = tiraText(str(link["link"])) 
                            
                            
                
                dictExpansion[nom.decode("utf-8")] = expansionTemp
                dictElMundo[nom.decode("utf-8")] = elmundoTemp
                dictElPais[nom.decode("utf-8")] = elpaisTemp
                

                ind +=1
except WebDriverException :
      for nom in noms :
        # para bigNoticias3 acabadó a 280
        if noms.index(nom) > ind :     
                ind= noms.index(nom)
                
                
                print "...........Yendo a Expansion............"
                
                
                try :
                    expansionTemp = ExpansionTP2("'"+nom+"'", wait=2)
                    if len(expansionTemp) > 0 :
                        for link in expansionTemp :
                            index = expansionTemp.index(link)
                            print ".... cogiendo noticia %s de %s .....Expansion" % (index, len(expansionTemp))
                            if index != 0 and index%30 == 0:
                                driver.quit()
                                #os.system("taskkill /im chrome.exe")
                                driver = webdriver.Chrome()
                            link["texto"] = tiraText(str(link["link"]))
                            " going to link num. %s ... " % expansionTemp.index(link)
                except :
                    driver = webdriver.Chrome()
                    expansionTemp = ExpansionTP2("'"+nom+"'", wait=2)
                    if len(expansionTemp) > 0 :
                        for link in expansionTemp :
                            index = expansionTemp.index(link)
                            print ".... cogiendo noticia %s de %s .....Expansion" % (index, len(expansionTemp))
                            if index != 0 and index%30 == 0:
                                driver.quit()
                                #os.system("taskkill /im chrome.exe")
                                driver = webdriver.Chrome()
                            link["texto"] = tiraText(str(link["link"]))
                            " going to link num. %s ... " % expansionTemp.index(link)
                            
                            
                    
                print "...........Yendo a El Mundo............"
                
                
                
                try :
                    elmundoTemp = ElMundoTP2("'"+nom+"'", wait=2)
                    if len(elmundoTemp)> 0 :
                        for link in elmundoTemp :
                            index = elmundoTemp.index(link)
                            print ".... cogiendo noticia %s de %s .....El Mundo" % (index, len(elmundoTemp))
                            if index != 0 and index%30 == 0:
                                driver.quit()
                               # os.system("taskkill /im chrome.exe")
                                driver = webdriver.Chrome()
                            link["texto"] = tiraText(str(link["link"])) # seguiendo a cada vinculo
                except :
                    driver = webdriver.Chrome()
                    elmundoTemp = ElMundoTP2("'"+nom+"'", wait=2)
                    if len(elmundoTemp)> 0 :
                        for link in elmundoTemp :
                            index = elmundoTemp.index(link)
                            print ".... cogiendo noticia %s de %s .....El Mundo" % (index, len(elmundoTemp))
                            if index != 0 and index%30 == 0:
                                driver.quit()
                                #os.system("taskkill /im chrome.exe")
                                driver = webdriver.Chrome()
                            link["texto"] = tiraText(str(link["link"])) # seguiendo a cada vinculo
                            
                            
                    
                print "...........Yendo a El Pais............"   
                
                
                try :
                    elpaisTemp = ElPaisTP2("'"+nom+"'", wait =2) # variables temopranias que contenen la busqueda en cada periodoco empresa se llama "nom"
                    if len(elpaisTemp) > 0 :
                        for link in elpaisTemp :
                            index = elpaisTemp.index(link)
                            print ".... cogiendo noticia %s de %s .....El Pais" % (index, len(elpaisTemp))
                            if index != 0 and index%30 == 0:
                                driver.quit()
                                os.system("taskkill /im chrome.exe") # limpiando los procesos para no se paran chrome 
                                driver = webdriver.Chrome()
                            link["texto"] = tiraText(str(link["link"])) 
                except :
                    driver = webdriver.Chrome()
                    elpaisTemp = ElPaisTP2("'"+nom+"'", wait =2) # variables temopranias que contenen la busqueda en cada periodoco empresa se llama "nom"
                    if len(elpaisTemp) > 0 :
                        for link in elpaisTemp :
                            index = elpaisTemp.index(link)
                            print ".... cogiendo noticia %s de %s .....El Pais" % (index, len(elpaisTemp))
                            if index != 0 and index%30 == 0:
                                driver.quit()
                                os.system("taskkill /im chrome.exe") # limpiando los procesos para no se paran chrome 
                                driver = webdriver.Chrome()
                            link["texto"] = tiraText(str(link["link"])) 
                            
                            
                
                dictExpansion[nom.decode("utf-8")] = expansionTemp
                dictElMundo[nom.decode("utf-8")] = elmundoTemp
                dictElPais[nom.decode("utf-8")] = elpaisTemp
                

                ind +=1
except KeyboardInterrupt : 
    print "Master says stop!"


"""

def tiraText(vinculo) :
    try :  
       driver.get(vinculo)
       print "aaa"
       time.sleep(2)
        
       text = driver.find_elements_by_tag_name("p")
       textL = [a.text for a in text]
       return " ".join(filter(None, list(set(textL))))
        
    except KeyboardInterrupt  :
       "Yes Master, I will stop now"
    except :
       print sys.exc_info()[0]
       return("no hay texto disponible")
        

expansionTemp = ExpansionTP2("banco santander", wait=2)
elpaisTemp = ElPaisTP2("banco santander", wait=2)
elmundoTemp = ElMundoTP2("banco santander", wait=2)


for link in expansionTemp :
    index = expansionTemp.index(link)
    print ".... cogiendo noticia %s de %s .....Expansion" % (index, len(expansionTemp))
    if index != 0 and index%30 == 0:
        driver.quit()
        #os.system("taskkill /im chrome.exe")
        driver = webdriver.Chrome()
    link["texto"] = tiraText(str(link["link"]))
    #print type(link["link"])
    " going to link num. %s ... " % expansionTemp.index(link)
"""