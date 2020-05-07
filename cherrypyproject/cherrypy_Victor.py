# -*- coding: utf-8 -*-

import cherrypy
import os

class Acceuil(object):
    @cherrypy.expose 
    def __init__(self):
        self.inscription = Inscription()
        self.connexion = Connexion()
        
    def index(self):
        return open("html/acceuil.html")
    index.exposed = True

class Inscription(object):
    def __init__(self):
        #self.acceuil = Acceuil() #censé être pour les navigations bars
        # self.connexion = Connexion()
        pass
        
    def index(self):
        return open("html/inscription.html")
    index.exposed = True
    
class Connexion(object):
    def __init__(self):
        # self.acceuil = Acceuil()
        # self.inscription = Inscription()
        pass
    
    def index(self):
        return open("html/connexion.html")
    index.exposed = True

configcss = {
        '/css':
        { 'tools.staticdir.on':True,
          'tools.staticdir.dir':os.path.abspath("./css")
        }
        #Pas besoin du code en dessous pour l'instant
        #,
        # '/global.css':
        # { 'tools.staticfile.on':True,
        #   'tools.staticfile.filename':os.path.abspath("./css/global.css")
        # },
        # '/acceuil.css':
        # { 'tools.staticfile.on':True,
        #   'tools.staticfile.filename':os.path.abspath("./css/acceuil.css")
        # }
    }
cherrypy.quickstart(Acceuil(), config = configcss)
