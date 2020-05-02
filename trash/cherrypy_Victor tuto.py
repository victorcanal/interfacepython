# -*- coding: utf-8 -*-

import cherrypy

class HomePage(object):
    @cherrypy.expose
    # def index(self):
    #     return "Hello World!"
        
    # def shutdown(self):  
    #     cherrypy.engine.exit()
    #     return 
    # '<a id="shutdown"; href="./shutdown">Shutdown Server</a>'
    
    def __init__(self):
        self.maxime = MaximeDuJour()
        self.liens = PageDeLiens()
        
    def index(self):
        return open("html/acceuil.html")
    '''
        <h3>Site des adorateurs du Python royal - Page d'acceuil.</h3>
        <p>Veuillez visiter nos rubriques géniales :</p>
        <ul>
            <li><a href="/entreNous">Restons entre nous</a></li>
            <li><a href="/maxime/">Une maxime subtile</a></li>
            <li><a href="/liens/utiles">Des liens utiles</a></li>
        </ul>
    '''
    index.exposed = True
    
    def entreNous(self):
        return '''
            Cette page est produite à la racine du site.<br />
            [<a href="/">Retour</a>]
        '''
    entreNous.exposed = True

class MaximeDuJour(object):
    def index(self):
        return '''
        <h3>Il existe 10 sortes de gens : ceux qui comprennent le binaire, et les autres !</h3>
        <p>[<a href="../">Retour</a>]</p>
    '''
    index.exposed = True
    
class PageDeLiens(object):
    def __init__(self):
        self.extra = LiensSupplementaires()
    
    def index(self):
        return '''
        <p>Page racine des liens (sans utilité réelle).</p>
        <p>En fait, les liens <a href="utiles">sont plutôt ici</a></p>
    '''
    index.exposed = True
    
    def utiles(self):
        return '''
        <p>Quelques liens utiles :</p>
        <ul>
            <li><a href="http://www.cherrypy.org">Site de CherryPy</a></li>
            <li><a href="http://www.python.org">Site de Python</a></li>
        </ul>
        <p>D'autres liens utiles vous sont proposés
        <a href="./extra/"> ici </a>.</p>
        <p>[<a href="../">Retour</a>]</p>
    '''
    utiles.exposed = True

class LiensSupplementaires(object):
    def index(self):
        return '''
        <p>Encore quelques autres liens utiles :</p>
        <ul>
            <li><a href="http://pythomium.net">Le site de l'auteur</a></li>
            <li><a href="http://ubuntu-fr.org">Ubuntu :le must</a></li>
        </ul>
        <p>[<a href="../">Retour à la page racine des liens</a>]</p>
    '''
    index.exposed = True

racine = HomePage()
cherrypy.quickstart(racine)#, config = "tutoriel.conf")

#cherrypy.quickstart(HelloWorld())