# -*- coding: utf-8 -*-

import cherrypy
import os

    
class Produits(object):
    @cherrypy.expose
    def __init__(self):
        self.quantite = [['Pâtes', '', 'paquet(s) de 500 grammes'],
            ['Riz', '', 'paquet(s) de 500 grammes'],
            ['Eau', '', 'pack(s) de 8 bouteilles'],
            ['Pain', '', 'paquet(s) de 12 tranches'],
            ['Jambon', '', 'paquet(s) de 4 tranches'],
            ['Fromage', '', 'unité'],
            ['Poulet', '', 'entier'],
            ['Haricots verts', '', 'boîte(s) de conserve, 250'],
            ['Carottes', '', 'paquet(s) de 10 carottes'],
            ['Yogourt', '', 'pack(s) de 8'],
            ['Salade', '', 'unité'],
            ['Lentilles', '', 'boîte(s) de conserve, 250 grammes'],
            ['Poisson', '', 'filet'],
            ['Pommes de terre', '', 'filet(s) de 1 kilo'],
            ['Céréales', '', 'unité'],
            ['Lait', '', 'brique(s) de 6'],
            ['Beurre', '', 'brique(s)'],
            ['Huile végétale', '', 'bouteille'],
            ['Farine', '', 'paquet(s) de 1 kilo'],
            ['Chocolat', '', 'tablette(s)'],
            ['Sucre', '', 'paquet(s) de 1 kilo']]
        
    
    @cherrypy.expose
    def index(self):
        # return open("html/produits.html")
        html = '<html><head>'
        html += '<meta charset="utf-8" name="Produits" content="Commande des produits">'
        html += '<link rel="stylesheet" type="text/css" href="../css/liste_commande.css">'
        html += '<title>Commande des Produits</title>'
        html += '</head>'
        html += '<body>'
        html += '<a href = "produits">Produits</a>'
        html += '<a href = "recapitulatif">Récapitulatif</a>'
        
        html += '<h1 id = "myHeader">Commande</h1>'
        html += '<p>Choisissez votre produit ainsi que la quantité souhaitée. Mettez une quantité à côté du produit qui vous intéresse. Si vous ne mettez pas de quantité pour un produit il ne sera pas commandé. </p>'
        html += '<form method ="POST" action ="result">'
        
        for i in range(len(self.quantite)):
            html += '<h2 class = "produit">'+self.quantite[i][0]+' :</h2>'
            html += '<br><input placeholder="Quantité de '+self.quantite[i][0]+' :" name="quantite_temp"/>'
            #obligés de mettre la liste des quantités dans une liste, cherrypy ne prend pas en compte les matrices
            html += '<label for ="unite">' + self.quantite[i][2] + '.</label></br>'
        
        html += '<p></p><button type="submit">Valider la commande</button>'
        html += '</form></body></html>'
        return html
    index.exposed = True
    #toutes les quantités sont dans un tableau
    

    @cherrypy.expose
    def result(self, quantite_temp):
        #met la liste des quantités (quantite_temp) dans la matrice quantite de base
        for i in range(len(self.quantite)):
            self.quantite[i][1] = quantite_temp[i]
        
        html = '<html><head>'
        
        html += '<meta charset="utf-8" name="Recapitulatif" content="Récapitulatif de la commande">'
        html += '<link rel="stylesheet" type="text/css" href="../css/recap.css">'
        html += '<title>Récapitulatif de la commande</title></head>'
        html += '<body><nav>'
        html += '<a href="Produits">Produits</a>'
        html += '<a href="recapitulatif">Récapitulatif</a>'
        html += '</nav>'
        html += '<h2>Récapitulatif de votre commande</h2>'
        html += '<table id = "tabcommande" style = "width : 100%">'
        
        html += '<tr>'
        html += '<th>Produit</th>'
        html += '<th>Quantité</th>'
        html += '<th>Unité</th>'
        html += '</tr>'
        
        #affiche toutes les quantités ainsi que les produits qui ont été choisis
        for i in range(len(self.quantite)):
            if(self.quantite[i][1] != ''):
                html += '<tr><td>'+ self.quantite[i][0] + '</td>'
                html += '<td>'+ self.quantite[i][1] +'</td>'
                html += '<td>'+ self.quantite[i][2] +'</td></tr>'

        html += '</table></body></html>'                        
        return html
    index.exposed = True

 
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
 
cherrypy.quickstart(Produits(), config = configcss)