# -*- coding: utf-8 -*-
"""
Created on Tue May 19 09:38:52 2015

@author: bluecap
"""

__autor__ = "Yevgeniy Levin, Enrich Gilabert"

from bs4 import BeautifulSoup
import re
import requests
from datetime import datetime

max_pag = 3
pagination = 10
headers = {'Accept-Encoding': 'identity, deflate, compress, gzip',
           'Accept': '*/*','User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'}

cookie= {'uid':'W9g/8VVfHfplwTL2AzAyAg==#69209aef53130fdb6de5ffb6bc3822c0', '__gads':'ID=1802bd5d11c3cfde:T=1432296967:S=ALNI_MYTjRdO3G4NczeWmr8J-iAoKvs4XA', 'avisopc':'1', 's_vnum':'1435701600011%26vn%3D2', 's_fid':'26FFD3718CCAA0EA-0CE730C7D881C034', 's_nr':'1433757370231-Repeat', 's_invisit':'true', 's_lv':'1433757370233', 's_lv_s':'Less%20than%201%20day', 's_sq':'%5B%5BB%5D%5D', 's_cc':'true', 'crtTags':'ctol300%3B'}


def makeSoup(url):
    try:
        source_code = requests.get(url, headers=headers)#, verify=False)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text)
        return(soup)
    except:
        print('No he podido hacer el soup de '+url)
        return("")

def getNoticia(url) :
    try:
        noticia = makeSoup(url)
        text1 = noticia.findAll('p')
        text2 = [a.text for a in text1]
        textFinal = " ".join(text2)
        return textFinal
    except :
        return("no hay texto disponible")
        
#############################################################################
"""EL PAIS"""
#############################################################################

        
def ElPaisLinks(key, pag=1, wait=0):
    url = "http://elpais.com/buscador/"
    
    try:
        payload = {'qr': '', 'tt': '', 'qt': '"'+key+'"', 'np': pag, 'db': 240782344060, 'bu':'ep', 'sf':0, 'ss': '' }       
        #payload2 = {'qt': key, 'np': pag}
        print('request---')
        r = requests.post(url, data=payload, headers=headers, cookies=cookie)
        print('fin requests request---')
        pagina = r.text
        soup = BeautifulSoup(pagina)
        return(soup)
    except UnicodeDecodeError :
        payload = {'qr': '', 'tt': '', 'qt': key.decode("utf-8"), 'np': pag, 'db': '240782344060', 'bu':'ep', 'sf':'0', 'ss': '' }
        r = requests.post(url, data=payload)
        pagina = r.text
        soup = BeautifulSoup(pagina)
        return(soup)
    except:
        print('No he podido sacar la lista de ofertas de Elpais.es'+url)
        return("")
        
def ElPaisPull(key, wait=0):
    resultados = []
    for pag in range(1,max_pag):
        print('-------Noticias en El País para '+key+' -- Pagina '+str(pag)+'-------')
        pagina = ElPaisLinks(key, pag=pag)
        articulos = pagina.findAll('div',{'class': 'article'})
        if articulos:
            for articulo in articulos:
                noticia = {}
                try:
                    titulo = articulo.find('h2').find('a', href=True).text
                except:
                    print('no se ha podido recoger el titulo')
                try:
                    relevancia = articulo.find('div',{'class': 'porcentaje'})
                    befor_keyowrd, keyword, after_keyword = relevancia.text.strip().partition('de')
                    relevancia = befor_keyowrd.strip()[:-1]
                except:
                    print('no se ha podido recoger el relevancia')
                try:
                    link = articulo.find('h2').find('a', href=True)['href']
                except:
                    print('no se ha podido recoger el link')
                try:
                    fecha = articulo.find('span',{'class': 'fecha'}).text
                except:
                    print('no se ha podido recoger el fecha')
                try:
                    hora = articulo.find('span',{'class': 'hora'}).text
                except:
                    print('no se ha podido recoger el hora')
                try:
                    fuente = articulo.find('span',{'class': 'firma'}).text
                except:
                    print('no se ha podido recoger el fuente')
                try:
                    parrafo = articulo.find('p').text
                except:
                    print('no se ha podido recoger el parrafo')
                noticia['Empresa']=key
                noticia['titulo']=titulo
                noticia['link'] = 'http://elpais.com'+link
                noticia['autor'] =fuente
                noticia['fecha'] =fecha
                noticia['hora'] =hora
                noticia['parrafo']=parrafo
                noticia['relevancia']=relevancia
                noticia['texto'] = getNoticia(noticia['link'])
                noticia['created_at'] = datetime.now()
                resultados.append(noticia)
        else:
            print('No hay resultados para esta empresa en el Pais...')
            break
        
    return(resultados)

#pais = ElPaisPull('coca cola')

#############################################################################
"""El MUNDO"""
#############################################################################        
        
def ElMundoLinks(key, pag=1, wait=0):
    try:
        key_ok = re.sub(' ','+', key.strip())
        url = 'http://ariadna.elmundo.es/buscador/archivo.html?q="'+key_ok+'"&t=1&i='+str((1+(pag-1)*pagination))+'&n='+str(pagination)+'&fd=0&td=0&w=70&s=1&no_acd=1'
        #print(url)        
        return(makeSoup(url))
    except UnicodeDecodeError :
        key_ok = re.sub(' ','+', key.decode("utf-8").strip())
        url = "http://ariadna.elmundo.es/buscador/archivo.html?q="+key_ok+"&t=1&i="+(1+(pag-1)*pagination)+"&n="+pagination+"&fd=0&td=0&w=70&s=1&no_acd=1"
        print('unicode '+url)         
        return(makeSoup(url))
    except:
        print('No he podido sacar la lista de ofertas de Elpais.es'+url)
        return("")

def ElMundoPull(key, wait=0):
    resultados = []
    for pag in range(1,max_pag):
        print('-------Noticias en El Mundo para '+key+' -- Pagina '+str(pag)+'-------')
        pagina = ElMundoLinks(key, pag=pag)
        art = pagina.find('ul',{'class': 'lista_resultados'})
        if art:
            articulos = art.findAll('li', recursive=False)
            if not 'no ha' in articulos[0].text:
                for i,articulo in enumerate(articulos):
                    noticia = {}
                    if i>0:
                        try:
                            titulo = articulo.find('h3').find('a', href=True).text.strip()
                        except:
                            print('no se ha podido recoger el titulo')
                        try:
                            relevancia = articulo.find('p',{'class': 'coincidencia'}).findAll('strong')[1].text[:-1].strip()
                        except:
                            print('no se ha podido recoger el relevancia')
                        try:
                            link = articulo.find('h3').find('a', href=True)['href']
                        except:
                            print('no se ha podido recoger el link')
                        try:
                            fecha = articulo.find('span',{'class': 'fecha'}).text.strip()
                        except:
                            print('no se ha podido recoger el fecha')
                        try:
                            fuente = articulo.find('strong',{'class': 'autor'}).text.strip()
                        except:
                            print('no se ha podido recoger el fuente')
                        noticia['len']=len(articulo.findAll('p'))
                        try:
                            if len(articulo.findAll('p'))>4:
                                parrafo = articulo.findAll('p')[3].text.strip()
                            else:
                                parrafo = articulo.findAll('p')[2].text.strip()
                        except:
                            print('no se ha podido recoger el parrafo')
                        noticia['Empresa']=key
                        noticia['titulo']=titulo
                        noticia['link'] = link
                        noticia['autor'] =fuente
                        noticia['fecha'] =fecha
                        noticia['parrafo']=parrafo
                        noticia['relevancia']=relevancia
                        noticia['texto'] = getNoticia(noticia['link'])
                        noticia['created_at'] = datetime.now()
                        resultados.append(noticia)
            else:
                print('No hay resultados para esta empresa en el Mundo...')
                break
        else:
            print('No hay resultados para esta empresa en el Mundo...')
            break

    return(resultados)
   
#mundo = ElMundoPull('coca cola')
        
#############################################################################
"""EXPANSION"""
#############################################################################

def ExpansionLinks(key, pag=1, wait=0):
    try:
        key_ok = re.sub(' ','+', key.strip())
        url = 'http://cgi.expansion.com/buscador/archivo_expansion.html?q="'+key_ok+'"&t=1&i='+str((1+(pag-1)*pagination))+'&n='+str(pagination)+'&fd=0&td=0&w=65&s=1'
        #print(url)        
        return(makeSoup(url))
    except UnicodeDecodeError :
        key_ok = re.sub(' ','+', key.decode("utf-8").strip())
        url = "http://ariadna.elmundo.es/buscador/archivo.html?q="+key_ok+"&t=1&i="+(1+(pag-1)*pagination)+"&n="+pagination+"&fd=0&td=0&w=70&s=1&no_acd=1"
        print('unicode '+url)         
        return(makeSoup(url))
    except:
        print('No he podido sacar la lista de ofertas de Elpais.es'+url)
        return("")

#expansion = ExpansionLinks('coca cola')

def ExpansionPull(key, wait=0):
    resultados = []
    for pag in range(1,max_pag):
        print('-------Noticias en Expansion para '+key+' -- Pagina '+str(pag)+'-------')
        pagina = ExpansionLinks(key, pag=pag)
        art = pagina.find('ul',{'id': 'buscador_expansion'})
        if art:
            articulos = art.findAll('li', recursive=False)
        
            for i,articulo in enumerate(articulos):
                noticia = {}
                try:
                    titulo = articulo.find('h2').find('a', href=True).text.strip()
                except:
                    print('no se ha podido recoger el titulo')
                try:
                    relevancia = articulo.find('span',{'class': 'coincidencia'}).text[:-1].strip()
                except:
                    print('no se ha podido recoger el relevancia')
                try:
                    link = articulo.find('h2').find('a', href=True)['href']
                except:
                    print('no se ha podido recoger el link')
                try:
                    fecha = articulo.find('span',{'class': 'firma'}).text.strip()
                except:
                    print('no se ha podido recoger el fecha')
                try:
                    fuente = "Expansion"
                except:
                    print('no se ha podido recoger el fuente')
                try:                        
                    parrafo = articulo.find('p').text.strip()
                except:
                    print('no se ha podido recoger el parrafo')
                noticia['Empresa']=key
                noticia['titulo']=titulo
                noticia['link'] = link
                noticia['autor'] =fuente
                noticia['fecha'] =fecha
                noticia['parrafo']=parrafo
                noticia['relevancia']=relevancia
                noticia['texto'] = getNoticia(noticia['link'])
                noticia['created_at'] = datetime.now()
                resultados.append(noticia)
            
        else:
            print('No hay resultados para esta empresa en Expansion...')
            break

    return(resultados)
   
#expansion = ExpansionPull('coca cola')
   
#############################################################################
"""LA VANGUARDIA"""
#############################################################################

def LaVanguardiaLinks(key, pag=1, wait=0):
    try:
        key_ok = re.sub(' ','+', key.strip())
        url = 'http://cgi.expansion.com/buscador/archivo_expansion.html?q="'+key_ok+'"&t=1&i='+str((1+(pag-1)*pagination))+'&n='+str(pagination)+'&fd=0&td=0&w=65&s=1'
        #print(url)        
        return(makeSoup(url))
    except UnicodeDecodeError :
        key_ok = re.sub(' ','+', key.decode("utf-8").strip())
        url = "http://ariadna.elmundo.es/buscador/archivo.html?q="+key_ok+"&t=1&i="+(1+(pag-1)*pagination)+"&n="+pagination+"&fd=0&td=0&w=70&s=1&no_acd=1"
        print('unicode '+url)         
        return(makeSoup(url))
    except:
        print('No he podido sacar la lista de ofertas de Elpais.es'+url)
        return("")

#expansion = ExpansionLinks('coca cola')

def LaVanguardiaPull(key, wait=0):
    resultados = []
    for pag in range(1,max_pag):
        print('-------Noticias en Expansion para '+key+' -- Pagina '+str(pag)+'-------')
        pagina = ExpansionLinks(key, pag=pag)
        art = pagina.find('ul',{'id': 'buscador_expansion'})
        if art:
            articulos = art.findAll('li', recursive=False)
        
            for i,articulo in enumerate(articulos):
                noticia = {}
                try:
                    titulo = articulo.find('h2').find('a', href=True).text.strip()
                except:
                    print('no se ha podido recoger el titulo')
                try:
                    relevancia = articulo.find('span',{'class': 'coincidencia'}).text[:-1].strip()
                except:
                    print('no se ha podido recoger el relevancia')
                try:
                    link = articulo.find('h2').find('a', href=True)['href']
                except:
                    print('no se ha podido recoger el link')
                try:
                    fecha = articulo.find('span',{'class': 'firma'}).text.strip()
                except:
                    print('no se ha podido recoger el fecha')
                try:
                    fuente = "Expansion"
                except:
                    print('no se ha podido recoger el fuente')
                try:                        
                    parrafo = articulo.find('p').text.strip()
                except:
                    print('no se ha podido recoger el parrafo')
                noticia['Empresa']=key
                noticia['titulo']=titulo
                noticia['link'] = link
                noticia['autor'] =fuente
                noticia['fecha'] =fecha
                noticia['parrafo']=parrafo
                noticia['relevancia']=relevancia
                noticia['texto'] = getNoticia(noticia['link'])
                noticia['created_at'] = datetime.now()
                resultados.append(noticia)
            
        else:
            print('No hay resultados para esta empresa en Expansion...')
            break

    return(resultados)
   
#expansion = ExpansionPull('coca cola')
   
#http://www.lavanguardia.com/buscador/index.html?filter.q=%22coca+cola%22&filter.page=2