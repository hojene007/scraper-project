# -*- coding: utf-8 -*-
"""
Created on Tue May  5 15:43:05 2015

@author: Bluecap
"""

__author__ = 'Enric Gilabert'

from selenium import webdriver
import time
import pymysql
import pymysql.cursors
import sys

host = "bluecap.cubz34n4knn2.eu-central-1.rds.amazonaws.com"
user = "bluecap"
password = "Bluecap2005"
dbname = "einformaDB"


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""        Drop table                                                    """        
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def dropTable(name):
    # Connect to the database
    connection = pymysql.connect(host=host,
                                 user=user,
                                 passwd=password,
                                 db=dbname,
                                 port=3306)
                                 #cursorclass=pymysql.cursors.DictCursor)
                                 #charset='utf8mb4',
    
    try:

        with connection.cursor() as cursor:
            # Create a new record
            sql = "DROP TABLE IF EXISTS "+name+";"
            cursor.execute(sql)
    
        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()
        
    finally:
        connection.close()
        
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""        Create table                                                    """        
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def createTable(name):
    
    # Connect to the database
    connection = pymysql.connect(host=host,
                                 user=user,
                                 passwd=password,
                                 db=dbname,
                                 port=3306)
                                 #cursorclass=pymysql.cursors.DictCursor)
                                 #charset='utf8mb4',
    
    try:

        with connection.cursor() as cursor:
            # Create a new record
            sql = "CREATE TABLE IF NOT EXISTS "+name+" (empresa varchar(255), autor varchar(255), fecha varchar(255), link varchar(255), parrafo varchar(255), titulo varchar(255));"
            cursor.execute(sql)
    
        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()
        
    finally:
        connection.close()


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""        Get companies from DB                                           """        
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def getCompanies(key):

    # Connect to the database
    connection = pymysql.connect(host=host,
                                 user=user,
                                 passwd=password,
                                 db=dbname,
                                 port=3306)
                                 #cursorclass=pymysql.cursors.DictCursor)
                                 #charset='utf8mb4',

    
    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "SELECT * FROM Empresas WHERE situacion LIKE %s"
            cursor.execute(sql,key)
            empresas = cursor.fetchall()
            return(empresas)
    finally:
        connection.close()


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""        Insert Into the DB                                              """        
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def putResults(table, dicc):
    
    # Connect to the database
    connection = pymysql.connect(host=host,
                                 user=user,
                                 passwd=password,
                                 db=dbname,
                                 port=3306,
                                 charset='utf8mb4')
                                 #cursorclass=pymysql.cursors.DictCursor)
                                 #charset='utf8mb4',

    try:
        with connection.cursor() as cursor:
            for empresa in dicc:
                if empresa:
                    for res in empresa:
                        sql = "INSERT INTO "+ table +" (empresa,autor,fecha,link,parrafo,titulo) VALUES (%s, %s, %s, %s, %s, %s);"
                        print(sql)
                        cursor.execute(sql, (res['Empresa'], res['autor'], res['fecha'], res['link'], res['parrafo'], res['titulo']))
                        
                        # connection is not autocommit by default. So you must commit to save
                        # your changes.
                        connection.commit()
    
    finally:
        connection.close()

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""        Visitando a Yahoo Noticias                                     """        
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def YahooNews(key, wait=0):
    
    # go to the google home page
    driver.get("https://es.noticias.yahoo.com/")
    # find the element that's name attribute is q (the google search box)
    inputElement = driver.find_element_by_id("mediasearchform-p")
    # type in the search
    inputElement.send_keys(key)
    # submit the form (although google automatically searches now without submitting)
    inputElement.submit()
    resultados = []
    
    try:
        #Nos movemos a lo largo de todos los resultados de la búsqueda extrayendo la info 
        for res in driver.find_elements_by_css_selector('.NewsArticle'):
            noticia = {}
            titulo = res.find_element_by_css_selector('.fz-m').text
            link = res.find_element_by_css_selector('.fz-m').get_attribute('href')
            fecha = res.find_element_by_css_selector('.ml-10').text
            fuente = res.find_element_by_css_selector('.cite').text
            parrafo = res.find_element_by_tag_name('p').text
            noticia['Empresa']=key
            noticia['titulo']=titulo
            noticia['link']=link
            noticia['fecha']=fecha
            noticia['autor']=fuente
            noticia['parrafo']=parrafo
            resultados.append(noticia)
        time.sleep(wait)
        return(resultados)
    
    except:
        print('Ha ocurrido un error con la busqueda de '+key)
        print("Unexpected error:", sys.exc_info()[0])
        time.sleep(2)
        
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""        Visitando a Bing Noticias                                     """        
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def BingNews(key, wait=0):
    
    # go to the google home page
    driver.get("https://www.bing.com/?scope=news")
    # find the element that's name attribute is q (the google search box)
    inputElement = driver.find_element_by_id("sb_form_q")
    # type in the search
    inputElement.send_keys(key)
    # submit the form (although google automatically searches now without submitting)
    inputElement.submit()
    resultados = []
    
    try:
        #Nos movemos a lo largo de todos los resultados de la búsqueda extrayendo la info 
        for res in driver.find_elements_by_class_name('sn_r'):
            noticia = {}
            titulo = res.find_element_by_tag_name('a').text
            link = res.find_element_by_tag_name('a').get_attribute('href')
            fecha = res.find_element_by_css_selector('.sn_tm').text
            fuente = res.find_element_by_css_selector('.sn_src').text
            parrafo = res.find_element_by_css_selector('.sn_snip').text
            noticia['Empresa']=key
            noticia['titulo']=titulo
            noticia['link']=link
            noticia['fecha']=fecha
            noticia['autor']=fuente
            noticia['parrafo']=parrafo
            resultados.append(noticia)
        time.sleep(wait)
        return(resultados)
    
    except:
        print('Ha ocurrido un error con la busqueda de '+key)
        print("Unexpected error:", sys.exc_info())
        time.sleep(2)


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""        Visitando a ElPais.com                                          """        
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
     
def ElPais(key, wait=0):
    
    # go to the google home page
    driver.get("http://elpais.com/buscador/")
    # find the element that's name attribute is q (the google search box)
    form = driver.find_element_by_id('formulario_busquedas')
    inputElement = form.find_element_by_name('qt')
    # type in the search
    inputElement.send_keys(key)
    # submit the form (although google automatically searches now without submitting)
    inputElement.submit()
    resultados = []
    
    try:
        
        #Nos movemos a lo largo de todos los resultados de la búsqueda extrayendo la info 
        for res in driver.find_elements_by_class_name('article'):
            noticia = {}
            titulo = res.find_element_by_css_selector('div.noticia h2 a').text
            link = res.find_element_by_css_selector('div.noticia h2 a').get_attribute('href')
            fecha = res.find_element_by_class_name('fecha').text
            fuente = res.find_element_by_css_selector('.firma_comentarios').text
            parrafo = res.find_element_by_tag_name('p').text
            noticia['Empresa']=key
            noticia['titulo']=titulo
            noticia['link']=link
            noticia['autor']=fuente
            noticia['fecha']=fecha
            noticia['parrafo']=parrafo
            resultados.append(noticia)
        time.sleep(wait)
        return(resultados)
    
    except:
        print('Ha ocurrido un error con la busqueda de '+key)
        print("Unexpected error:", sys.exc_info()[0])
        time.sleep(2)


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""        Visitando a ElMundo.com                                          """        
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
     
def ElMundo(key, wait=0):
    
    # go to the google home page
    driver.get("http://ariadna.elmundo.es/buscador/archivo.html")
    # find the element that's name attribute is q (the google search box)
    #form = driver.find_element_by_id('formulario_busquedas')
    inputElement = driver.find_element_by_name('q')
    # type in the search
    inputElement.send_keys(key)
    # submit the form (although google automatically searches now without submitting)
    inputElement.submit()
    resultados = []
    
    #Nos movemos a lo largo de todos los resultados de la búsqueda extrayendo la info 
    busc = driver.find_element_by_class_name('lista_resultados')
    for res in busc.find_elements_by_css_selector('li'):
        noticia = {}
        try:
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
            noticia['Empresa']=key
            noticia['titulo']=titulo
            noticia['link']=link
            noticia['autor']=fuente
            noticia['fecha']=fecha
            noticia['parrafo']=parrafo
            resultados.append(noticia)
        except:
            print('Ha ocurrido un error con la busqueda de '+key)
            print("Unexpected error:", sys.exc_info()[0])
            pass
        finally:
            time.sleep(wait)
            
    return(resultados)


if __name__ == '__main__':
    
    dropTable('noticias')
    createTable('noticias')
    
    yahoo = []
    elpais = []
    elmundo = []
    bing = []
    companies = []
    # Abrimos el archivo con las empresas que han presentado concurso
    companies = getCompanies('%Concurso%')
    # Create a new instance of the Firefox driver
    driver = webdriver.Firefox()
        
    try:
        
        for line in companies:
            print(line[1]+" "+line[3])
            yahoo.append(YahooNews(line[1]+" "+line[2]))
            bing.append(BingNews(line[1]+" "+line[2]))
            elpais.append(ElPais(line[1]))
            elmundo.append(ElMundo(line[1]))
            
    finally:
        #Cerramos el navegador
        driver.quit()
        putResults("noticias",elmundo)
        putResults("noticias",elpais)
        putResults("noticias",yahoo)
        putResults("noticias",bing)
        print("Hemos acabado...")
    