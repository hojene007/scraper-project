# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 09:28:42 2015

@author: bluecap

en esto file hacemos la conexion con un server de mysql y se tira las tablas 
"""

import MySQLdb
import pandas as pd

host = "bluecap.cubz34n4knn2.eu-central-1.rds.amazonaws.com"
user = "bluecap"
password = "Bluecap2005"
dbname = "einformaDB"

db = MySQLdb.connect(host, user, password, dbname)
cursor = db.cursor()

#### get first few rows
# query1 = "select*from einformaDB.eInforma_Empresas limit 5;"
# top5= cursor.execute(query1)

queryConcurso = "SELECT * FROM einformaDB.Empresas where situacion like '%Concurso%';"

df = pd.read_sql(queryConcurso, db)
nombres = list(df['nombre_empresa'])




