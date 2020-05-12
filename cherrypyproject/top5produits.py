# -*- coding: utf-8 -*-

import cherrypy
import os

class Collectivite(object):
    @cherrypy.expose
    def __init__(self):
        self.top5produits = ['pâtes', 'riz', 'farine', 'sucre', 'oeufs']
        
    
    @cherrypy.expose
    def index(self):
        return '''
<html>
    <head>
        <meta charset="utf-8" name="Collectivite" content="Liste des 5 produits les plus commandés">
        <link rel="stylesheet" type="text/css" href="../css/collectivite.css">
        <title>Liste des 5 produits les plus commandés</title>
    </head>
        
    <body>
        <h1 id = "myHeader">Liste des 5 produits les plus commandés</h1>
        <table style="width:100%">
        <tr>
            <th><h2 class = "produit">Les '''+self.top5produits[0]+''' sont le premier produit le plus commandé.</h2></th>
            <th><h1><img src="/images/5_etoiles.png"></h1></th>
        </tr>

        <tr>
            <th><h2 class = "produit">Le '''+self.top5produits[1]+''' est le deuxième produit le plus commandé.</h2></th>
            <th><h1><img src="/images/4_etoiles.png"></h1></th>
        </tr>

        <tr>
            <th><h2 class = "produit">La '''+self.top5produits[2]+''' est le troisième produit le plus commandé.</h2></th>
            <th><h1><img src="/images/3_etoiles.png"></h1></th>
        </tr>

        <tr>
            <th><h2 class = "produit">Le '''+self.top5produits[3]+''' est le quatrième produit le plus commandé.</h2></th>
            <th><h1><img src="/images/2_etoiles.png"></h1></th>
        </tr>

        </tr>
            <th><h2 class = "produit">Les '''+self.top5produits[4]+''' sont le cinquième produit le plus commandé.</h2></th>
            <th><h1><img src="/images/etoile.png"></h1></th>
        </tr>

        <button type="submit">Retour vers l'accueil</button>
    </body>
</html>

'''
    index.exposed = True
    #toutes les quantités sont dans un tableau
    

conf = {
        '/images':
        { 
            'tools.staticdir.on':True,
            'tools.staticdir.dir':os.path.abspath("./images")
        },
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
        }
cherrypy.quickstart(Collectivite(), config = conf)