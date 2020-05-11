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

# # -*- coding: utf-8 -*-

# import cherrypy
# import os

# # some_string = ""

# # class Site(object):
# #     def __init__(self):
# #         self.produits = Produits()
# #         self.recapitulatif = Recapitulatif()


#         # <tr>
#         #   <td>Riz</td>
#         #   <td>'''+ quantite[i] + '''</td>
#         #   <td>paquet(s) (de 1 kilo)</td>
#         # </tr>
#         # <tr>
#         #   <td>Sucre</td>
#         #   <td>'''+ quantite[i] + '''</td>
#         #   <td>paquet(s) (de 500 grammes)</td>
#         # </tr>
#         # <tr>
#         #   <td>Farine</td>
#         #   <td>'''+ quantite[i] + '''</td>
#         #   <td>paquet(s) (de 500 grammes)</td>
#         # </tr>

# # <h2 class = "produit">Riz :</h2>

# #         			<br><input placeholder="Quantité de Riz :" name="quantite"/>
# #         			<label for ="unitéRiz">paquet(s) de 500 grammes.</label></br>

# # 			<h2 class = "produit">Sucre :</h2>

# #         			<br><input placeholder="Quantité de sucre :" name="quantite"/>
# #         			<label for ="unitéSucre">paquet(s) de 500 grammes.</label></br>

# # 			<h2 class = "produit">Farine :</h2>

# #         			<br><input placeholder="Quantité de Farine :" name="quantite"/>
# #         			<label for ="unitéFarine">paquet(s) de 500 grammes.</label></br>
# # quantite = [['Pâtes', '', 'paquet(s) de 500 grammes'],
# #             ['Riz', '', 'paquet(s) de 500 grammes'],
# #             ['Eau', '', 'pack(s) de 8 bouteilles'],
# #             ['Pain', '', 'paquet(s) de 12 tranches'],
# #             ['Jambon', '', 'paquet(s) de 4 tranches'],
# #             ['Fromage', '', 'unité'],
# #             ['Poulet', '', 'entier'],
# #             ['Haricots verts', '', 'boîte(s) de conserve, 250'],
# #             ['Carottes', '', 'paquet(s) de 10 carottes'],
# #             ['Yogourt', '', 'pack(s) de 8'],
# #             ['Salade', '', 'unité'],
# #             ['Lentilles', '', 'boîte(s) de conserve, 250 grammes'],
# #             ['Poisson', '', 'filet'],
# #             ['Pommes de terre', '', 'filet(s) de 1 kilo'],
# #             ['Céréales', '', 'unité'],
# #             ['Lait', '', 'brique(s) de 6'],
# #             ['Beurre', '', 'brique(s)'],
# #             ['Huile végétale', '', 'bouteille'],
# #             ['Farine', '', 'paquet(s) de 1 kilo'],
# #             ['Chocolat', '', 'tablette(s)'],
# #             ['Sucre', '', 'paquet(s) de 1 kilo']]
    
# class Produits(object):
#     @cherrypy.expose
#     def __init__(self):
#         self.quantite = [['Pâtes', '', 'paquet(s) de 500 grammes'],
#             ['Riz', '', 'paquet(s) de 500 grammes'],
#             ['Eau', '', 'pack(s) de 8 bouteilles'],
#             ['Pain', '', 'paquet(s) de 12 tranches'],
#             ['Jambon', '', 'paquet(s) de 4 tranches'],
#             ['Fromage', '', 'unité'],
#             ['Poulet', '', 'entier'],
#             ['Haricots verts', '', 'boîte(s) de conserve, 250'],
#             ['Carottes', '', 'paquet(s) de 10 carottes'],
#             ['Yogourt', '', 'pack(s) de 8'],
#             ['Salade', '', 'unité'],
#             ['Lentilles', '', 'boîte(s) de conserve, 250 grammes'],
#             ['Poisson', '', 'filet'],
#             ['Pommes de terre', '', 'filet(s) de 1 kilo'],
#             ['Céréales', '', 'unité'],
#             ['Lait', '', 'brique(s) de 6'],
#             ['Beurre', '', 'brique(s)'],
#             ['Huile végétale', '', 'bouteille'],
#             ['Farine', '', 'paquet(s) de 1 kilo'],
#             ['Chocolat', '', 'tablette(s)'],
#             ['Sucre', '', 'paquet(s) de 1 kilo']]
        
    
#     @cherrypy.expose
#     def index(self):
#         # return open("html/produits.html")
#         html = '<html><head>'
#         html += '<meta charset="utf-8" name="Produits" content="Commande des produits">'
#         html += '<link rel="stylesheet" type="text/css" href="../css/liste_commande.css">'
#         html += '<title>Commande des Produits</title>'
#         html += '</head>'
#         html += '<body>'
#         html += '<a href = "produits">Produits</a>'
#         html += '<a href = "recapitulatif">Récapitulatif</a>'
        
#         html += '<h1 id = "myHeader">Commande</h1>'
#         html += '<p>Choisissez votre produit ainsi que la quantité souhaitée. Mettez une quantité à côté du produit qui vous intéresse. Si vous ne mettez pas de quantité pour un produit il ne sera pas commandé. </p>'
#         html += '<form method ="POST" action ="result">'
        
#         for i in range(len(self.quantite)):
#             html += '<h2 class = "produit">'+self.quantite[i][0]+' :</h2>'
            
#             html += '<br><input placeholder="Quantité de '+self.quantite[i][0]+' :" name="quantite[i][1]"/>'
#             html += '<label for ="unite">'+ self.quantite[i][2] + '.</label></br>'
        
#         html += '<button type="submit">Valider la commande</button>'
#         html += '</form></body></html>'
#         return html
#     index.exposed = True
#     #toutes les quantités sont dans un tableau
    

#     @cherrypy.expose
#     def result(self):
#         # cherrypy.session['mystring'] = quantitePates
#         # some_string = quantitePates + '\n' + quantiteRiz + '\n' + quantiteSucre + '\n' + quantiteFarine
#         # cherrypy.session['mystring'] = some_string
#         # file = open("test.txt","w")
#         # file.write(some_string)
#         # file.close()
        
#         html = '<html><head>'
        
#         html += '<meta charset="utf-8" name="Recapitulatif" content="Récapitulatif de la commande">'
#         html += '<link rel="stylesheet" type="text/css" href="../css/recap.css">'
#         html += '<title>Récapitulatif de la commande</title></head>'
#         html += '<body><nav>'
#         html += '<a href="Produits">Produits</a>'
#         html += '<a href="recapitulatif">Récapitulatif</a>'
#         html += '</nav>'
#         html += '<h2>Récapitulatif de votre commande</h2>'
#         html += '<table id = "tabcommande" style = "width : 100%">'
        
#         html += '<tr>'
#         html += '<th>Produit</th>'
#         html += '<th>Quantité</th>'
#         html += '<th>Unité</th>'
#         html += '</tr>'
        
#         #affiche toutes les quantités ainsi que les produits qui ont été choisis
#         for i in range(len(self.quantite)):
#             if(self.quantite[i][1] != 0):
#                 html += '<tr><td>'+ self.quantite[i][0] + '</td>'
#                 html += '<td>'+ self.quantite[i][1] +'</td>'
#                 html += '<td>'+ self.quantite[i][2] +'</td></tr>'
#                 # html += '<tr>'
#                 # html += '<td>Pâtes</td>'
#                 # html += '<td>'+ self.quantite[i] +'</td>'
#                 # html += '<td>paquet(s) (de 500 grammes)</td>'
#                 # html += '</tr>'

#         html += '</table></body></html>'                        
#         return html
#     index.exposed = True
 
#     # @cherrypy.expose
#     # def result(self, quantitePates, quantiteRiz, quantiteSucre, quantiteFarine):
#     #     some_string = quantitePates + '\n' + quantiteRiz + '\n' + quantiteSucre + '\n' + quantiteFarine
#     #     # cherrypy.session['mystring'] = some_string
#     #     # file = open("test.txt","w")
#     #     # file.write(some_string)
#     #     # file.close()
#     #     return some_string
       
#     # def display(self):
#     #     # cherrypy.session['mystring']
#     #     return open("html/recapitulatif.html")
    
#     # @cherrypy.expose
#     # def result(self, quantite):
#     #     # cherrypy.session['mystring'] = quantitePates
#     #     # some_string = quantitePates + '\n' + quantiteRiz + '\n' + quantiteSucre + '\n' + quantiteFarine
#     #     # cherrypy.session['mystring'] = some_string
#     #     # file = open("test.txt","w")
#     #     # file.write(some_string)
#     #     # file.close()
        
#     #         return '''
        
#     # <html>
#     #   <head>
#     #     <meta charset="utf-8" name="Recapitulatif" content="Récapitulatif de la commande">
#     # 	<link rel="stylesheet" type="text/css" href="../css/recap.css">
#     # 	<title>Récapitulatif de la commande</title>
#     #   </head>
      
#     # <body>
#     #   <nav>
#     # 	<a href="Produits">Produits</a>
#     # 	<a href="recapitulatif">Récapitulatif</a>
#     #   </nav>
    
#     #   <h2>Récapitulatif de votre commande</h2>
    
#     #   <table id = "tabcommande" style = "width : 100%">
#     #     <tr>
#     #       <th>Produit</th>
#     #       <th>Quantité</th> 
#     #       <th>Unité</th> 
#     #     </tr>
#     #     '''for i in range(len(quantite)):'''
#     #         <tr>
#     #           <td>Pâtes</td>
#     #           <td>'''+ quantite[i] + '''</td>
#     #           <td>paquet(s) (de 500 grammes)</td>
#     #         </tr>

#     #   </table>
#     #  </body>
#     # </html>
#     #     '''
#     # index.exposed = True
    

    
    
# # class Recapitulatif(object):
# #     def __init__(self):
# #         pass
    
# #     def quantite(self):
        
        
        
# #     @cherrypy.expose
# #     def index(self):
# #         return open("html/recapitulatif.html")
# #     index.exposed = True
    
#     # @cherrypy.expose
#     # def Recapitulatif(self, quantitePates, quantiteRiz, quantiteSucre, quantiteFarine):
#         # some_string = quantitePates + ' ' + quantiteRiz + ' ' + quantiteSucre + ' ' + quantiteFarine
#         # cherrypy.session['mystring'] = some_string
#         # file = open("test.txt","w")
#         # file.write(some_string)
#         # file.close()
#         # return some_string
 
#     # @cherrypy.expose
#     # def demarrer(self, quantitePate):
#         # return recap.format(quantitePate)
 
# configcss = {
#         '/css':
#         { 'tools.staticdir.on':True,
#           'tools.staticdir.dir':os.path.abspath("./css")
#         },
#         '/':
#         {
#             'tools.sessions.on': True,
#             'tools.staticdir.root': os.path.abspath(os.getcwd())
#         }   
#         }
 
# cherrypy.quickstart(Produits(), config = configcss)