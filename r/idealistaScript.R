print(paste("###########################################################"))
print(paste("Entrado en la pagina web...",url))
print(paste("###########################################################"))

url2 <- "http://www.idealista.com/venta-oficinas/barcelona-barcelona/mapa"
url_ciudad <- html_session(url2)
barrios <- html_nodes(url_ciudad, "#subdivisions a")
links_barrios <- as.numeric(length(barrios)[[1]])
print(paste("Encontrados ",links_barrios," barrios"))

########## Entrar en cada link para cada barrio ###########################
for (b in 1:links_barrios) {
  
  barrio = html_text(barrios)[b]
  print(paste("###########################################################"))
  print(paste("Entrando en el barrio número ",b," con nombre", barrio))
  print(paste("###########################################################"))
  
  Sys.sleep(sample(3:5, 1))
  url_barrio <- url_ciudad %>% follow_link(barrio)
  subdivisions_barri <- html_nodes(url_barrio, "#subdivisions a")
  unlist(subdivisions_barri)
  links_subdivisions_barrio <- as.numeric(length(subdivisions_barri)[[1]])
  print(paste("Encontradas ",links_subdivisions_barrio," subdivisiones en ", barrio))
  
  ######################### Entrar en cada link para cada subdivision de cada barrio #########
  for (sub in 1:links_subdivisions_barrio) {
    
    subbarrio = html_text(subdivisions_barri)[sub]
    Sys.sleep(sample(3:5, 1))
    print(paste("###########################################################"))
    print(paste("Entrando en subdivision número ",sub," con nombre", subbarrio))
    print(paste("###########################################################"))
    
    new_url_sub <- url_barrio %>% follow_link(subbarrio)  
    siguiente <- html_nodes(new_url_sub, ".icon-arrow-right-after")
    unlist(siguiente)
    sig = html_text(siguiente)
    first = 1
    new_url <- html_session(new_url_sub$url)
    ########### RECORRER TODAS LAS HOJAS DE UNA SUBDIVISION BUSCANDO LOS PISOS ####
    
    repeat{
      siguiente <- html_nodes(new_url, ".icon-arrow-right-after")
      sig = html_text(siguiente)
      Sys.sleep(sample(3:5, 1))
      if (!identical(sig, character(0))) {
        if (first!=1) {
          new_url <- new_url %>% follow_link(sig)
        }
        new_url <- html_session(new_url$url)
        first = 0
        print(new_url$url)
        error = 0
        
        ########### COGER LOS ITEMS QUE QUIERO DE LA PAGINA ####
        
        idealista <- html(new_url)
        Sys.sleep(3)
        lugar <- html_nodes(idealista, ".item-link")
        precio <- html_nodes(idealista, ".item-price")
        detalles <- html_nodes(idealista, ".item-detail")
        telefono <- html_nodes(idealista, ".item-not-clickable-phone")
        descripcion <- html_nodes(idealista, ".item-description")
        
        for (i in 1:length(precio)) {
          hab_check = FALSE
          metro_check = FALSE
          det_check = FALSE
          
          preu = as.numeric(gsub("[.]", "",substr(html_text(precio)[i], 1, nchar(html_text(precio)[i])-1)))
          
          if (grepl("piso en",html_text(lugar)[i]) || grepl("barcelona",html_text(lugar)[i])) {
            lloc <- as.character(gsub("piso en ","",html_text(lugar)[i]))
          } else {
            
            lloc <- NA
            print(lloc)
          }
          
          if ((grepl("hab.",html_text(detalles)[(3*(i-1))+1-error]))) {
            habitaciones <- as.numeric(gsub(" hab.","",html_text(detalles)[(3*(i-1))+1-error]))
            hab_check=TRUE
          } else {
            error = error+1
            habitaciones<-NA
          }
          
          if ( grepl(" m²",html_text(detalles)[(3*(i-1))+2-error])) {
            metro <- as.numeric(gsub(" m²","",html_text(detalles)[(3*(i-1))+2-error]) )
            metro_check=TRUE
          } else {
            error=error+1
            metro <-NA
          }
          
          if ( grepl("planta",html_text(detalles)[(3*(i-1))+3-error]) || grepl("ascensor",html_text(detalles)[(3*(i-1))+3-error])) {
            detalle<- as.character(html_text(detalles)[(3*(i-1))+3-error])
            det_check = TRUE
          } else {
            error=error+1
            detalle <- NA
          }
          
          if (is.na(metro)==TRUE) {
            metro_2 = NA
          } else {
            metro_2 = as.numeric(preu/metro)
          }
          
          ########### AÑADIR A LA BASE DE DATOS ####
          
          pisos<-rbind(pisos, data.frame(Ciudad = ciudad, 
                                         Barrio = barrio,
                                         Direccion = lloc,
                                         Precio = preu,
                                         Habitaciones = habitaciones,
                                         Metros = metro,
                                         Detalle = detalle,
                                         metro_cuadrado = metro_2))
        }
      } else {
        break
      }
    }
  }
  print(paste("###########################################################"))
  print(paste("Esperando 60s entre barrios para que no me detecte como robot..."))
  print(paste("###########################################################"))
  Sys.sleep(sample(50:70, 1))
}