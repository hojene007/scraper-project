# -*- coding: utf-8 -*-
"""
Created on Fri May 22 13:01:04 2015

@author: Epoch
"""
a = "ISLEÑA DE PESCADO"
norm = "some english words"
b = unicode(a, "utf-8")
print "Se actualizo empresa '%s' y articulo se llama '%s' " % (b.decode("utf-8"), "mas espaÑol")