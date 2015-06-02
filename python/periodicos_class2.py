# -*- coding: utf-8 -*-
"""
Created on Tue May 19 09:38:52 2015

@author: bluecap
"""

__autor__ = "Yevgeniy Levin, Enrich Gilabert"

from selenium import webdriver
import time
import pymysql
import pymysql.cursors
import sys

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException, WebDriverException

"""
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
binary = FirefoxBinary('C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe')
driver = webdriver.Firefox(firefox_binary=binary)
"""
#driver = webdriver.Chrome()



#############################################################################
"""EL PAIS"""
#############################################################################

def ElPaisTP2(key, wait=0):
    
    # go to the google home page
    driver.get("http://elpais.com/buscador/")
    resultados = []
    # find the element that's name attribute is q (the google search box)
    try :
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'formulario_busquedas')))
        form = element
    except :
        print "hay alguno terible en tu codigo...... al final no tenemos nada sobre esta empresa..EL Pais"
        return(resultados)

    #form = driver.find_element_by_id('formulario_busquedas')
    inputElement = form.find_element_by_name('qt')
    # type in the search
    
    try :
        inputElement.send_keys(key)
    except UnicodeDecodeError : 
        inputElement.send_keys(key.decode("utf-8"))
    # submit the form (although google automatically searches now without submitting)
    inputElement.submit()
    
    proximaPaginaBool = 0   
    pageDoing = 1
    
    def cogerDatos() :
        element = WebDriverWait(driver, wait*2).until(
        EC.presence_of_element_located((By.CLASS_NAME, "article")))        #Nos movemos a lo largo de todos los resultados de la búsqueda extrayendo la info 
        for res in driver.find_elements_by_class_name('article'):
            try :
                noticia = {}
                titulo = res.find_element_by_css_selector('div.noticia h2 a').text
                link = res.find_element_by_css_selector('div.noticia h2 a').get_attribute('href')
                fecha = res.find_element_by_class_name('fecha').text
                fuente = res.find_element_by_css_selector('.firma_comentarios').text
                parrafo = res.find_element_by_tag_name('p').text
                noticia['Empresa']=key
                noticia['titulo']=titulo
                noticia['link'] = link
                noticia['autor'] =fuente
                noticia['fecha'] =fecha
                noticia['parrafo']=parrafo
                resultados.append(noticia)
            except :
                print ("el pais no love from you ......", sys.exc_info()[0])
    
    try:
        cogerDatos()
        while proximaPaginaBool == 0 :
            try:
                temp = driver.find_element_by_class_name("paginacion")
                temp2 = temp.find_elements_by_tag_name("a")
                temp3 = temp2[0].get_attribute("href")
                
                if temp3.encode("utf-8") != 'javascript:void(0);' and pageDoing<7 :
                    temp2[0].click()
                    cogerDatos()
                    pageDoing +=1 
                    print """       
                    
                    .....scraping pagina no. %s......      """ % pageDoing
                else :
                    print """
                    
                    no hay mas paginas con resultados ... or ... demasiado paginas ... movando a la proxima empresa...
                    
                    """
                    proximaPaginaBool = 1
            except :
                print ("""
                
                no hay mas paginas con resultados
                
                """, sys.exc_info()[0])
                proximaPaginaBool = 1
        
        return(resultados)
    
    except:
        print('''
        Ha ocurrido un error con la busqueda de  
        
        '''+key)
        print("Unexpected error:", sys.exc_info()[1])
        return(resultados)
        

#############################################################################
"""El MUNDO"""
#############################################################################        
        
        
def ElMundoTP2(key, wait=0):
    resultados = []
    # go to the google home page
    driver.get("http://ariadna.elmundo.es/buscador/archivo.html")
    # find the element that's name attribute is q (the google search box)
    #form = driver.find_element_by_id('formulario_busquedas')
    try :
        element = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.NAME, 'q')))
        inputElement = element
    except :
        print """
        
        hay alguno terible en tu codigo...... al final no tenemos nada sobre esta empresa... el mundo
        
        
        """
        return(resultados)
        
    # type in the search
    try :
        inputElement.send_keys(key)
    except UnicodeDecodeError :
        inputElement.send_keys(key.decode("utf-8"))
    # submit the form (although google automatically searches now without submitting)
    inputElement.submit()
    proximaPaginaBool = 0   
    pageDoing = 1
    
    def cogerDatos() :
        element = WebDriverWait(driver, wait*2).until(
        EC.presence_of_element_located((By.CLASS_NAME, "lista_resultados")))
        #Nos movemos a lo largo de todos los resultados de la búsqueda extrayendo la info 
        busc = driver.find_element_by_class_name('lista_resultados')        
        for res in busc.find_elements_by_css_selector('li'):
            try :
                noticia = {}
                
                titulo = res.find_element_by_tag_name('h3').find_element_by_tag_name('a').text
                #print(titulo)
                link = res.find_element_by_tag_name('h3').find_element_by_tag_name('a').get_attribute('href')
                #print(link)            
                fecha = res.find_element_by_class_name('fecha').text
                #print(fecha)            
                fuente = res.find_element_by_class_name('autor').text
                #print(fuente)            
                parrafo = res.find_elements_by_tag_name('p')[3].text
                #print(parrafo)            
                noticia['Empresa'] =key
                noticia['titulo'] =titulo
                noticia['link'] =link
                noticia['autor'] =fuente
                noticia['fecha'] =fecha
                noticia['parrafo'] =parrafo
                resultados.append(noticia)
                print """
                
                .... anexo resultad con titulo:.... %s      .....""" % titulo
            except :
                print("""
                
                Potentially no results...
                
                """, sys.exc_info()[0])

    try : 
        cogerDatos()
        while proximaPaginaBool == 0 :
            try:
                element = WebDriverWait(driver, wait*2).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'nav_resultados')))
                temp = element # verificando si hay mas que una pagina
                temp2 = temp.find_elements_by_tag_name("a")
                temp3 = temp2[-1].text
                if temp3.encode("utf-8") == 'Siguiente \xc2\xbb' and pageDoing<7:
                    temp2[-1].click()
                else :
                    print """
                    
                    no hay mas paginas con resultados... o no quieremos mas que 7 paginas de resultados
                    
                    """
                    proximaPaginaBool = 1
                    
                cogerDatos()
                pageDoing +=1 
                print """     
                
                .....scraping pagina no. %s......     
                
                """ % pageDoing
            except :
                print """
                
                no hay mas paginas con resultados
                
                """
                proximaPaginaBool = 1
        print proximaPaginaBool    
        return(resultados)
    except :
        print('''
        
        Ha ocurrido un error con la busqueda de 
        
        '''+key)
        print("""
        
        Unexpected error:
        
        """, sys.exc_info()[0])
        return(resultados)

        
#############################################################################
"""EXPANSION"""
#############################################################################

def ExpansionTP2(key, wait=2) :
        # go to the google home page
    driver.get("http://www.expansion.com")
    resultados = []

    # find the element that's name attribute is q (the google search box)

    try :
        element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'buscar')))
        inputElement =  driver.find_element_by_id("buscar")
    except :
        print """
        
        hay alguno terible en tu codigo...al final no tenemos nada sobre esta empresa... expansion
        
        """
        return(resultados)

        
    # type in the search
    try :
        inputElement.send_keys(key)
    except UnicodeDecodeError :
        inputElement.send_keys(key.decode("utf-8"))
        
    # submit the form (although google automatically searches now without submitting)
    inputElement.submit()
    time.sleep(wait) # <----  no se funciona sin esto
    proximaPaginaBool = 0   
    pageDoing = 1
    
    def cogerDatos() :
        try :
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
        except :
            print ("""
            
            why you no give me no love baby.... Expansion
            
            """, sys.exc_info()[0])
        
    try:
        #Nos movemos a lo largo de todos los resultados de la búsqueda extrayendo la info 
        cogerDatos()
        while proximaPaginaBool == 0 :
            try :
                if pageDoing<7 :
                    time.sleep(wait)
                    temp = driver.find_element_by_class_name("siguiente")
                    temp.click()
                    cogerDatos()
                    pageDoing +=1 
                    print """  
                    
                    .....scraping pagina no. %s......   
                    
                    """ % pageDoing
                else :
                    print """
                    
                    ... too many pages ... moving to next empresa...
                    
                    """
                    proximaPaginaBool = 1
            except :
                print """
                
                ... no hay mas paginas ....
                
                """
                proximaPaginaBool = 1   

        
        return(resultados)
        
    except:
        print('''
        
        Ha ocurrido un error con la busqueda de '''+key)
        print("""
        
        Unexpected error:
        
        """, sys.exc_info()[0])
        return(resultados)
        
        
#############################################################################
        """PROBANDO COSAS"""
#############################################################################
        """
appleTry = ElPaisTP("apple", wait=4) # se nesecito a poner mas tiempo si internet esta despacio
appleTry = ElMundoTP("immobiliaria", wait=4) # se nesecito a poner mas tiempo si internet esta despacio


driver.get("http://ariadna.elmundo.es/buscador/archivo.html?q=immobiliaria%20&t=1&i=1&n=10&fd=0&td=0&w=70&s=1&no_acd=1")
temp = driver.find_element_by_class_name("nav_resultados")
temp2 = temp.find_elements_by_tag_name("a")
temp3 = temp2[-1].text
if temp3.encode("utf-8") == 'Siguiente \xc2\xbb' :
    temp2[-1].click()
    print "clicking"
else :
    print "done"
temp2[-1].click()

"""
#############################################################################
"""Tirando texto de noticias CLASS """ 
#############################################################################

    
def tiraElPais(vinculo) :
    try :
        driver.get(vinculo)
        time.sleep(2)
        text = driver.find_elements_by_tag_name("p")
        textL = [a.text for a in text]
        return " ".join(filter(None, list(set(textL))))
    except WebDriverException :
        driver = webdriver.Chrome()
        driver.get(vinculo)
        time.sleep(2)
        text = driver.find_elements_by_tag_name("p")
        textL = [a.text for a in text]
        return " ".join(filter(None, list(set(textL))))
    except :
        return("no hay texto disponible")
    
    
#############################################################################
"""Tirando texto de noticias CLASS """ 
#############################################################################

def tiraElMundo(vinculo) :
    try :
        driver.get(vinculo)
        time.sleep(2)
        text = driver.find_elements_by_tag_name("p")
        textL = [a.text for a in text]
        return " ".join(filter(None, list(set(textL))))
    except WebDriverException :
        driver = webdriver.Chrome()
        driver.get(vinculo)
        time.sleep(2)
        text = driver.find_elements_by_tag_name("p")
        textL = [a.text for a in text]
        return " ".join(filter(None, list(set(textL))))
    except :
        return("no hay texto disponible")
#############################################################################
"""Tirando texto de noticias CLASS """ 
#############################################################################
    
def tiraExpansion(vinculo) :
    try :
        driver.get(vinculo)
        time.sleep(2)
        text = driver.find_elements_by_tag_name("p")
        textL = [a.text for a in text]
        return " ".join(filter(None, list(set(textL))))
    except WebDriverException :
        driver = webdriver.Chrome()
        driver.get(vinculo)
        time.sleep(2)
        text = driver.find_elements_by_tag_name("p")
        textL = [a.text for a in text]
        return " ".join(filter(None, list(set(textL))))
    except :
        return("no hay texto disponible")
        
        
#############################################################################
        """probando cosas variadas""" 
#############################################################################        
"""
driver.get("http://economia.elpais.com/economia/2012/09/01/actualidad/1346529488_347848.html")
#tamano
temp = driver.find_elements_by_tag_name("p")
textL = [a.text for a in temp]
str_list = filter(None, textL)

"""


