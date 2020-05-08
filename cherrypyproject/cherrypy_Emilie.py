# -*- coding: utf-8 -*-

import cherrypy
import os


class site(object):
 def __init__(self):
  self.produits = Produits()
  self.recapitulatif = Recapitulatif()

class Produits(object):
 @cherrypy.expose
 def __init__(self):
    pass
  
 def index(self):
   return open("html/produits.html")
 index.exposed = True
 
   @cherrypy.expose
   def result(self, quantitePates, quantiteRiz, quantiteSucre, quantiteFarine):
        some_string = quantitePates + ' ' + quantiteRiz + ' ' + quantiteSucre + ' ' + quantiteFarine
        cherrypy.session['mystring'] = some_string
        file = open("test.txt","w")
        file.write(some_string)
        file.close()
        return some_string
       
   def display(self):
     return cherrypy.session['mystring']
    
    
class Recapitulatif(object):
    @cherrypy.expose
    def index(self):
        return open("html/recapitulatif.html")
    index.exposed = True
    
    # @cherrypy.expose
    # def Recapitulatif(self, quantitePates, quantiteRiz, quantiteSucre, quantiteFarine):
        # some_string = quantitePates + ' ' + quantiteRiz + ' ' + quantiteSucre + ' ' + quantiteFarine
        # cherrypy.session['mystring'] = some_string
        # file = open("test.txt","w")
        # file.write(some_string)
        # file.close()
        # return some_string
 
    # @cherrypy.expose
    # def demarrer(self, quantitePate):
        # return recap.format(quantitePate)
 
configcss = {
        '/css':
        { 'tools.staticdir.on':True,
          'tools.staticdir.dir':os.path.abspath("./css")
        },
        '/':
        {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        }   
        }
 
cherrypy.quickstart(site(), config = configcss)
