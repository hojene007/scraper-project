# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 16:05:41 2015

@author: Bluecap
"""

from bs4 import BeautifulSoup
import requests

headers = {'Accept-Encoding': 'identity, deflate, compress, gzip',
           'Accept': '*/*','User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'}

cookie= {'uid':'W9g/8VVfHfplwTL2AzAyAg==#69209aef53130fdb6de5ffb6bc3822c0', '__gads':'ID=1802bd5d11c3cfde:T=1432296967:S=ALNI_MYTjRdO3G4NczeWmr8J-iAoKvs4XA', 'avisopc':'1', 's_vnum':'1435701600011%26vn%3D2', 's_fid':'26FFD3718CCAA0EA-0CE730C7D881C034', 's_nr':'1433757370231-Repeat', 's_invisit':'true', 's_lv':'1433757370233', 's_lv_s':'Less%20than%201%20day', 's_sq':'%5B%5BB%5D%5D', 's_cc':'true', 'crtTags':'ctol300%3B'}


f = open('C:/Users/Bluecap/Documents/Python Scripts/eInforma/diccionario_empresas.txt', 'r')
dic_empresas = []
[dic_empresas.append(line.strip().lower()) for line in f]
f.close()

def makeSoup(url):
    try:
        source_code = requests.get(url, headers=headers)
        print(source_code.encoding)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text)
        return(soup)
    except:
        print('No he podido hacer el soup de '+url)
        return("")
        
def spainFix(myString) :
    # esto function se hace los caracteres español en el mas cerca carácters ingles - necesito lower case
    newString = list(myString)
    
    if "ñ" in myString :
        indNn = myString.index("ñ")
        newString[indNn] = "n"
    if "ç" in myString :
        indc = myString.index("ç")
        newString[indc] = "c"
    if "é" in myString :
        indc = myString.index("é")
        newString[indc] = "e"
    if "í" in myString :
        indc = myString.index("í")
        newString[indc] = "i"
    if "ó" in myString :
        indc = myString.index("ó")
        newString[indc] = "o"
    if "ó" in myString :
        indc = myString.index("ó")
        newString[indc] = "o"
    if "á" in myString :
        indc = myString.index("á")
        newString[indc] = "a"
    if "ü" in myString :
        indc = myString.index("ú")
        newString[indc] = "u"
    return "".join(newString)
    
    
def generateDict(lista, rec):
    dictionary = []
    nest=1
    while (nest<=rec):
        rec_dictionary = []
        for word in lista:
            try:
                url = "http://lenguaje.com/cgi-bin/Thesauro.exe?edition_field="+spainFix(word.lower())+"&B1=Buscar"
                print(url)
                try:
                    resultados = makeSoup(url)
                    get = resultados.find('ul', {'class':'Synonyms'})
                    for sinonim in get.findAll('li'):
                        my_list = [x.strip() for x in sinonim.text.split(",")]
                        rec_dictionary.extend(my_list)
                except Exception as e:
                    print(e)
                    continue
            except:
                continue
        lista = rec_dictionary
        rec_dictionary = [x for x in rec_dictionary if x not in dictionary]
        dictionary.extend(rec_dictionary)
        nest+=1
            
    return(dictionary)


dic_empresas_gen = generateDict(['bueno'],4)

f = open('pos_dic.txt', 'w')
dic_empresas_generated = []
for item in dic_empresas_gen:
  f.write("%s\n" % item)
  dic_empresas_generated.append(item)
  
f.close()