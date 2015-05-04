### File scraps the website http://www.einforma.com/empresas/CNAE.html to create a database of 
## company information 

# install.packages("rvest")
# install.packages("stringr")
library("rvest")
library("stringr")


 ##### Helper funcntions 
substrRight <- function(x, n){
  # finds last n characters of string x
  substr(x, nchar(x)-n+1, nchar(x))
}


url <- "http://www.einforma.com/empresas/CNAE.html"
urlRoot <- html_session(url)
sectorList <- html_nodes(urlRoot, ".col-one02 td")
nSect <- as.numeric(length(sectorList)[[1]])
name <- html_text(sectorList)
lastC <- substrRight(name, 1)
indices <- is.na(as.numeric(lastC))==FALSE
trueVec <- which(indices %in% FALSE)
namesSect <- name[trueVec]
subSect <- urlRoot %>% follow_link(sectorList[1])
