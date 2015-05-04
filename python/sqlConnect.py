# -*- coding: utf-8 -*-
#! python2
"""
Created on Tue Apr 21 12:01:40 2015

Esto file se tiene las functiones para contectar y escribir al SQL DB
@author: bluecap
"""
import sys
import MySQLdb
import random
host = "bluecap.cubz34n4knn2.eu-central-1.rds.amazonaws.com"
user = "bluecap"
password = "bluecap777"
dbname = "einformaDB"

db = MySQLdb.connect(host, user, password, dbname)
cursor = db.cursor()
cursor.execute("DROP TABLE IF EXISTS generalInfo")
crecerTabla = """create table generalInfo(
ActividadInforma text(200) ,
CIFNIF text(99),
CNAE2009 text(50),
Denominacin varchar(99),
DomicilioAnterior text(200),
DomicilioSocial text(200),
Fax text(200),
MarcasRegistradas text(999),
NmeroDUNS text(99),
ObjetoSocial text(400),
SIC text(999),
SituacindelaEmpresa text(200),
Telfono text(99),
URL text(999),
otraInfo text(9999),

primary key (Denominacin)) character set utf8;"""
cursor.execute(crecerTabla)

colNames = ["ActividadInforma", "CIFNIF", "CNAE2009", "Denominacin", "DomicilioAnterior", "DomicilioSocial", "Fax", "MarcasRegistradas", "NmeroDUNS", "ObjetoSocial", "SIC", "SituacindelaEmpresa", "Telfono", "URL", "otraInfo"]
tablaNombre = "generalInfo"    

def grabSubDict(myDict, keyParent, keyChildVec) :
    # esta function se tira los nodes apropriados segun keyChildVec de node keyParent en diccionario myDict
    myList = list()
    temp = myDict[keyParent]
    for val in keyChildVec :
        if val in temp :
            info = temp[val].encode("utf-8")
            info2 = info.replace('/', '')
            myList.append(str(info2))
            print info2

    return myList   

keysVec = empresaDict3['ACERIA DE ALAVA SA'].keys()

print keysVec
empresaNombres = empresaDict3.keys()

for empr in empresaNombres :
    print empresaNombres.index(empr)
    print empr
    estaEmpresaInfo = grabSubDict(empresaDict3, empr, keysVec)
    newInfoEmpr = [spainFix(a) for a in estaEmpresaInfo]
    stringToSql = insertarEnTabla(estaEmpresaInfo, colNames, tablaNombre)
    cursor.execute(stringToSql)
        