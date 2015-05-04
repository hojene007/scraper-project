library("rvest")
library("stringr")


##### Helper funcntions 
substrRight <- function(x, n){
  # finds last n characters of string x
  substr(x, nchar(x)-n+1, nchar(x))
}

######################################


url <- "http://www.einforma.com/empresas/CNAE.html"
urlRoot <- html_session(url)
empresaListo <- html_nodes(urlRoot, ".right td.first")
links <- as.numeric(length(empresaListo)[[1]])     

# Data frame para registrar info de cada empresa
dfEmpresas <- data.frame(Denominacion=character(),
                 DenominacionAntigua=character(), 
                 Situacion=character(), 
                 NumeroDUNS=character(), 
                 DomicilioSocial = character(), 
                 Telefono=character(), 
                 Fax = character(),
                 url=character(), 
                 MarcasRegistrd=character(), 
                 ActividadInf = character(), 
                 CNAE=character(), 
                 SIC=character(), 
                 ObjectoSocial =character(), 
                 otroInfo = character(), stringsAsFactors=FALSE) 
## Primero vez se va a cada link de cada empresa       
#tablaInformesSuperetiqueta tr:nth-child(2) td:nth-child(2)
#tablaInformesSuperetiqueta tr:nth-child(2) td:nth-child(2)
tagList <- c("#tablaInformesSuperetiqueta tr:nth-child(2) td:nth-child(2)", 
             ".ulclear", 
             ".pelotaverde", 
             "#tablaInformesSuperetiqueta tr:nth-child(6) td:nth-child(2)", 
             "#tablaInformesSuperetiqueta tr:nth-child(8) td:nth-child(2)", 
             "#tablaInformesSuperetiqueta tr:nth-child(11) td:nth-child(2)", 
             "#tablaInformesSuperetiqueta tr:nth-child(12) td:nth-child(2)", 
             "#tablaInformesSuperetiqueta u", 
             "tr:nth-child(14) td:nth-child(2)", 
             "tr:nth-child(15) td:nth-child(2)", 
             "tr:nth-child(16) td:nth-child(2)", 
             "tr:nth-child(17) td:nth-child(2)",
             ".category", 
             "tr:nth-child(21) td")


for (i in 1:links) {
  urlNew <- urlRoot %>% follow_link(html_text(empresaListo[i]))
  for (j in 1:length(tagList)) {
    temp <- as.character(html_text(html_nodes(urlNew, tagList[j])))
    print(temp)
    if (length(temp)!=0) {
      dfEmpresas[i, j] <- temp
    } else {
      dfEmpresas[i, j] <- NA
    }
  }
}

urlNew <-  urlRoot %>% follow_link(html_text(empresaListo[1]))
temp <- as.character(html_text(html_nodes(urlNew, ".mod-contents02")))

population <- urlNew %>%
  html() %>%
  html_nodes(urlNew, ".mod-contents02") %>%
  html_table()

