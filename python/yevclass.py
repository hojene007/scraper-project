# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 11:04:38 2015

File contains classes to do with various things (change as we get more material)

@author: bluecap
"""

class StringOps() :
    # un class que se tiene los operaciones con text, como regular expression y otras

    ##########==============================###########

    def _init_(self, fakeAttr):
        self.fakeAttr = "fake"
        
    ##########==============================###########
    
    def keyChange1(myDict, newKeys) :
        # esta function se pone nueve nombre en uun key de dicconario 
        index = 0
        newDict = {}
        for cell in myDict :
            myDict[cell]
            index =+ 1
            newDict = myDict
        return newDict
            
    ##########==============================###########
            
    def keyChange2 (myDict, ref) :
        # esta function se cambia el keys del diccionario al los de ref (un diccianario por dentro              myDict)
        # myRef = ref['Denominación']
        newDict = {}
        for cell in myDict :
            print cell
            name = myDict[cell][ref]
            newDict[name] = myDict[cell]        
        return newDict
        
    ##########==============================###########
    
    def keyChange3(myDict) :
        # esta funccion  se quita los espacios en el nombre de cada elemento del diccionario
        keys = myDict.keys()
        newDict = {}
        for key in keys :
            newDict[noSpace(key)] = myDict[key]
        return newDict
        
    ##########==============================###########  
        
    def keyChange4(myDict) :
    # una funccion de inception que se quita los espacios en un diccinario dentro uno otro diccionario 
        keyss = myDict.keys()
        newDict = {}
        for key in keyss :
           newDict[key] = keyChange3(myDict[key])
        return newDict
            
    ##########==============================###########
            
    def keyChange5(myDict) :
    # una funccion para poner nuevo nombre (de nuevo) a un diccenario - se quita los caracteres españoles y otras estranños - non-inception version
        keyss = myDict.keys()
        newDict = {}
        for key in keyss :
            newKey = key.decode('ascii','ignore')
            newKey.encode('utf-8')
            newKey = re.sub('[^A-Za-z0-9]+', '', newKey)
            newKey = newKey.encode('ascii')
            newDict[newKey] = myDict[key]
        
        return newDict
        
    def keyChange6(myDict) :
        # una funccion de inception que se cambia los nombres de los elementos y se ponelos en un format agradable para mysql
        keyss = myDict.keys()
        newDict = {}
        for key in keyss :
           newDict[key] = keyChange5(myDict[key])
        return newDict
        
    ##########==============================###########
        
    def find_between( s, first, last ):
        # una funccion que se encuentra un substring entre dos otros
        try:
            start = s.index( first ) + len( first )
            end = s.index( last, start )
            return s[start:end]
        except ValueError:
            return ""
    
    def getInsideDict(myDict) :
        # una funccion que se pone los elementos de un diccionario en un listo
        dictList = list()
        for elem in myDict:
            dictList.append(elem)
        return dictList
    
    ##########==============================###########
                        
    def noPunct(myString) :
        # esta function se suprime el punctuacion de las frases 
        exclude = set(string.punctuation)
        s = ''.join(ch for ch in myString if ch not in exclude)
        return s
        
    def noSpace(myString) :
        newString = myString.replace(" ", "")
        return newString
        
    ##########==============================###########
        
    def spainFix(myString) :
        # esto function se hace los caracteres español en el mas cerca carácters ingles
        bigN = 0
        smallN = 0
        newString = list(unidecode(myString))
        if "Ñ" in myString :
            bigN = 1
            indN = myString.index("Ñ")
            newString[indN] = "N"
        if "ñ" in myString :
            smallN = 1
            indNn = myString.index("ñ")
            newString[indNn] = "n"
        if "Ç" in myString :
            indC = myString.index("Ç")
            newString[indC] = "C"
        if "ç" in myString :
            indc = myString.index("ç")
            newString[indc] = "c"
                        
        return "".join(newString)
    
    ##########==============================###########    
    
    def insertarEnTabla(infoVec, colNames, tablaNombre) :
    # esta function se prepara el string para insertar in cursor.execute por anadir en tabla

        infoVecDecoded = list()
        colNombre = ",".join(colNames)
        for info in infoVec :
            infoVecDecoded.append(spainFix(str(info))) #decoding into english characters
        infoVecNuevo = ",".join(infoVecDecoded)
        myString = "insert into {} ({}) values ({})".format(tablaNombre, str(colNombre), str(infoVecNuevo.encode("utf-8")))
        return myString
        
class OnlineOps() :
    # esto class se tiene las operaciones para hacer web scaping
    
    ##########==============================###########

    def getEmpresaInfo(url) :
    # Esto function se necesita para seguir a pagina de la empresa y entonces tirar infos necesitos
        response = requests.get(url)
        soup = BeautifulSoup(response.text)
        table = soup.find(id="tablaInformesSuperetiqueta")
        errorVal = 'NoError'
        try :
            rawRowList = table.findAll('tr') 
        except :
            errorVal = "Houston we have a problem"
            rawRowList = list()
            
        rowDict = {}
    
        if errorVal == 'NoError' :
            for row in rawRowList :
                thisRow = row.findAll("td")
                k = len(thisRow)
                if k>1 :
                    t1 = re.findall('.+', thisRow[0].text)
                    t2 = re.findall('.+', thisRow[1].text)
                    rowDict[str(t1[0].encode("utf-8"))] = t2[0]
                elif k==1 :
                    t1 = re.findall('.+', thisRow[0].text)
                    rowDict["otraInfo"] = t1[0]
        else :
            rowDict["otraInfo"] = ["no info sobre empresa"]
            print("no info sobre empresa")
        
        return rowDict
        
    ##########==============================###########
        
    def matchUrl(path, empresa) :
    # esta function es necesita para encontrar el pagina de la empresa correcta 
    # path es el sendero que se tenga el nombre de la empresa
    # el umrbral se signfica de majoritad de palabras que es necesita para classificar el link
        umbral = 0.8
        splitE = empresa.split()
        boolVec = list()
        
        for palabra in splitE :
            if spainFix(palabra) in path :
                boolVec.append(1)
            else :
                boolVec.append(0)
                
        if (sum(boolVec)/len(splitE))>=umbral :
            correct = 1
        else :
            correct = 0 
         
        return correct