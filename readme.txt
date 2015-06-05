README PARA PROYECTO DE WEBSCRAPING (periodicos grandes y Bing News
AUTHOR: YEVGENIY LEVIN

ARCHIVOS:

- periodicos_class2.py - tiene todos las funciónes para hacer scraping de El Pais, 
  El Mundo, Expansion. Hay funciónes para tirar los vinculos de cada periodico y los para tirar el text de cada noticia.
  (Ahora el límite de numero de paginas de resultados maxima para cada empresa en cada periodico es 7. Es porque a veces hay demasiado
  paginas con resultados que no parecen estar relevantes. Puede cambiar esta opción facilemente en el codigo). Necesito a instalar 
  selenium (un package para scraping) en Python y colocar chromedriver.exe en el correcto lugar (con referencia de selenium). 


- periodicosRecolecta.py - tiene codigo para tirar datos de baso de datos de AMAZON WEB SERVICES (MySQLDB) y tambien la 
  implementación de las funcionés en periodicos_class2.py para recolectar noticias de periodicios - necesita a correr 
  periodicos_class2.py antes esto archivo. También hay codigo para actualizar el baso de datos con el datos de cada periodico 
  (con texto de cada noticia, vinculos, fechas, fuentas). El baso de datos se llama einformaDB.PeriodicosGrandes5.


- bing_tirrando_v1.py - tiene codigo para tirar datos de baso de datos de AMAZON WEB SERVICES (MySQLDB) y tambien se tira
  vinculos de las noticias de Bing.com y colocalos en el baso de datos que se llama einformaDB.bingNoticias


- raw_docs.py - tiene las funciónes para text processing de datos de las noticias. Específicamente, hay dos classes - un para hacer
  el processing sobre un colección de documentos (un colección de textos), se llama RawDocs3, y un otro class para hace el processing
  de texto sobre un document. Remova stopwords, hace tokenizing, conta de palabras y IF-IDF metodica para pesar los documentos


- sqlPull.py - tiene codigo para tirar y limpiar datos de AMAZON WEB SERVICES (MySQLDB). Lo prepara datos para text_mining1.py


- text_mining1.py - utilisa los funccionés en raw_docs.py para preparar los datos para analisís de relevance. Hace analisís de relevance 
  en dos formas, 1. conta cuanto vezes los terminos en diccionario apparecen en texto 2. conta cuanto vezes los terminos en diccionario 
  apparecen en texto - conta mas que un tiempo cada palabra si esta en el texto mas que un vez. Necesita a correr raw_docs.py y sqlPull.py antes de
  este archivo


- all_concurso.spydata - todos las resultados de busqueda en periodocos El Pais, El Mundo y Expansion en un formato lo que se lee con Python