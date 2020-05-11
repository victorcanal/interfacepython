# -*- coding: utf-8 -*-

import cherrypy
import os

class Accueil(object):
    @cherrypy.expose 
    def __init__(self):
        self.inscription = Inscription()
        self.connexion = Connexion()
        
    def index(self):
        return open("html/accueil.html")
    index.exposed = True

class Inscription(object):
    @cherrypy.expose 
    def __init__(self):
        #self.accueil = Accueil() #censé être pour les navigations bars
        #self.connexion = Connexion()
        pass
        
    def index(self):
        return open("html/inscription.html")
    index.exposed = True
    
    @cherrypy.expose
    def generate(self, inputemail, inputpassword, inputnom, inputprenom, inputadresse, inputnumero):
        some_string = inputemail + "," + inputpassword + "," +inputnom + "," + inputprenom + "," + inputadresse + "," + inputnumero
        cherrypy.session['mystring'] = some_string
        # file = open("inscription.txt","w")
        # file.write(some_string)
        # file.close()
        return some_string

    # def display(self):
    #     return cherrypy.session['mystring']
    
class Connexion(object):
    @cherrypy.expose
    def __init__(self):
        # self.accueil = Accueil()
        # self.inscription = Inscription()
        pass
    
    def index(self):
        return open("html/connexion.html")
    index.exposed = True
    
    @cherrypy.expose
    def generate(self, inputemail, inputpassword):
        some_string = inputemail + "," + inputpassword
        cherrypy.session['mystring'] = some_string
        # file = open("connexion.txt","w")
        # file.write(some_string)
        # file.close()
        return some_string
    
    # def display(self):
    #     return cherrypy.session['mystring']

conf = {
        '/css':
        { 
            'tools.staticdir.on':True,
            'tools.staticdir.dir':os.path.abspath("./css")
        },
        '/':
        {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        }
        #Pas besoin du code en dessous pour l'instant
        #,
        # '/global.css':
        # { 'tools.staticfile.on':True,
        #   'tools.staticfile.filename':os.path.abspath("./css/global.css")
        # },
        # '/accueil.css':
        # { 'tools.staticfile.on':True,
        #   'tools.staticfile.filename':os.path.abspath("./css/accueil.css")
        # }
        }
cherrypy.quickstart(Accueil(), config = conf)
