# -*- coding: utf-8 -*-
"""
Created on Fri May  8 13:24:06 2020

@author: emili
"""

import cherrypy
import os
import random
import string

#         <input type="submit" value="Exécuter le script" />



 
produits = \
"""
<html>

<head>
    <meta charset="utf-8" />
    <title>Page interactive</title>

<style>
#myHeader {
  background-color: lightblue;
  color: black;
  padding: 40px;
  text-align: center;
}

.produit {
  background-color: black;
  color: white;
  padding: 10px;
}

</style>
</head>


<body>
<a href = "https:/localhost:8080/commande"></a>
<h1 id = "myHeader">Commande</h1>

<p>Choisissez votre produit ainsi que la quantité souhaitée. Mettez une quantité à côté du produit qui vous intéresse. Si vous ne mettez pas de quantité pour un produit il ne sera pas commandé. </p>


<h2 class = "produit">Pâtes :</h2>

    <form method ="POST" action ="Recapitulatif">
        <br><input placeholder="Quantité de pâtes :" name="quantitePates"/>
        <label for ="unitePates">paquet(s) de 500 grammes.</label></br>
    </form>


<h2 class = "produit">Riz :</h2>

    <form method ="POST" action ="Recapitulatif">
        <br><input placeholder="Quantité de Riz :" name="quantiteRiz"/>
        <label for ="unitéRiz">paquet(s) de 500 grammes.</label></br>
    </form>


<h2 class = "produit">Sucre :</h2>


    <form method ="POST" action ="Recapitulatif">
        <br><input placeholder="Quantité de sucre :" name="quantiteSucre"/>
        <label for ="unitéSucre">paquet(s) de 500 grammes.</label></br>
    </form>

<h2 class = "produit">Farine :</h2>

    <form method ="POST" action ="Recapitulatif">
        <br><input placeholder="Quantité de Farine :" name="quantiteFarine"/>
        <label for ="unitéFarine">paquet(s) de 500 grammes.</label></br>
    </form>
    
<a href="/recap"><input type="submit">Validez votre commande</input></a>

</body>
</html>

"""
 
recap = \
"""
<html>

<head>
    <meta charset="utf-8" />
    <title>Page interactive - Recapitulatif</title>
    
<style>
table {
  width:100%;
}
table, th, td {
  border: 1px solid black;
  border-collapse: collapse;
}
th, td {
  padding: 15px;
  text-align: left;
}
table#tabcommande tr:nth-child(even) {
  background-color: #eee;
}
table#tabcommande tr:nth-child(odd) {
 background-color: #fff;
}
table#tabcommande th {
  background-color: black;
  color: white;
}
</style>
</head>


<body>
<h2>Récapitulatif de votre commande</h2>

<table id = "tabcommande" style = "width : 100%">
  <tr>
    <th>Produit</th>
    <th>Quantité</th> 
    <th>Unité</th> 

  </tr>
  <tr>
    <td>Pates</td>
    
    <td>quantitePate</td>
    <td>paquet(s) de 500 grammes</td>

  </tr>
  <tr>
    <td>Riz</td>
    <td>quantiteRiz</td>
    <td>paquet(s) de 1 kilo</td>
  </tr>
</table>
<br>

</body>
</html>
"""
 
class Root(object):
    @cherrypy.expose
    def index(self):
        return produits
    
    @cherrypy.expose
    def Recapitulatif(self, quantitePates, quantiteRiz, quantiteSucre, quantiteFarine):
        some_string = quantitePates + ' ' + quantiteRiz + ' ' + quantiteSucre + ' ' + quantiteFarine
        cherrypy.session['mystring'] = some_string
        # file = open("test.txt","w")
        # file.write(some_string)
        # file.close()
        return some_string
 
    @cherrypy.expose
    def demarrer(self, quantitePate):
        return recap.format(quantitePate)
 
configcss = {
        # '/css':
        # { 'tools.staticdir.on':True,
        #   'tools.staticdir.dir':os.path.abspath("./css")
        # },
        '/':
        {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        }   
        }
 
cherrypy.quickstart(Root(), config = configcss)