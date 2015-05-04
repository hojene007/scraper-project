
### File scraps the website http://www.einforma.com/empresas/CNAE.html to create a database of 
## company information 
library("rvest")
library("stringr")


##### Helper funcntions 
substrRight <- function(x, n){
  # finds last n characters of string x
  substr(x, nchar(x)-n+1, nchar(x))
}


url <- "http://www.einforma.com/empresas/CNAE.html"
urlRoot <- html_session(url)
sectorList <- html_nodes(urlRoot, ".col-one02 a")
nSect <- as.numeric(length(sectorList)[[1]])
nameSect <- html_text(sectorList)
linkSect <- as.numeric(length(sectorList)[[1]])
print(paste("Found ",linkSect," sectors"))

for (i in 1:linkSect) {
  subSect1 <- html_text(sectorList)[i]
  
  print(paste("Subsector ",i," que se llamo", subSect1))
  
  Sys.sleep(sample(3:5, 1))
  urlSubSect1 <- urlRoot %>% follow_link(subSect1)
  subSect1List <- html_nodes(urlSubSect1, ".col-one02 a")
  subSect1Name <- html_text(subSect1List)
  linkSubSect1 <- as.numeric(length(subSect1List))[1]
  
  for (j in 1:linkSubSect1) {
    subSect2 <- html_text(subSect1List)[j]
    
    print(paste("Subsector, segundo orden",i," que se llamo", subSect2))
    Sys.sleep(sample(3:5, 1))
    
    urlSubSect2 <- urlSubSect1 %>% follow_link(subSect2)
    subSect1List <- html_nodes(urlSubSect2, ".col-one02 a")
    subSect1Name <- html_text(subSect1List)
    linkSubSect1 <- as.numeric(length(subSect1List))[1]
    
  }
  
  
}