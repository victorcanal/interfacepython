import cherrypy
import os
import pymysql
import folium
from geopy.geocoders import Nominatim

def connexionBDD():
    connection = pymysql.connect(host='127.0.0.1',
    user='root',
    password='Pichagouille47',                             
    db='python1',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor)
    return connection

def produitPlusDemandes():
        sql = "select nom_produit ,sum(quantiteCommandee) from produit group by nom_produit order by sum(quantiteCommandee) desc limit 5;"
        connection = connexionBDD()
        tableauProduits = []
        try :
            cursor = connection.cursor()
            cursor.execute(sql)
            connection.commit()
            for row in cursor:
                tableauProduits.append(row['nom_produit'])
        finally:
            connection.close()
        return tableauProduits
    
class Accueil(object):
    @cherrypy.expose 
    def __init__(self):
        self.inscription = Inscription()
        self.connexion = Connexion()
        self.produits = Produits()
        self.collectivite = Collectivite()
        
    def index(self):
        return open("html/accueil.html")
    index.exposed = True

class Inscription(object):
    @cherrypy.expose 
    def __init__(self):
        pass
        
    def index(self):
        return open("html/inscription.html")
    index.exposed = True
    
    @cherrypy.expose
    def generate(self, inputemail, inputpassword, inputnom, inputprenom, inputadresse, inputnumero, inputnombre, inputnumcarte, inputexpirationdate, inputcryptogramme):
        some_string = inputemail + "," + inputpassword + "," +inputnom + "," + inputprenom + "," + inputadresse + "," + inputnumero + "," + inputnombre + "," + inputnumcarte + "," + inputexpirationdate + "," + inputcryptogramme
        cherrypy.session['mystring'] = 'vous êtes inscrits ! '
        self.stockageBDD(some_string)
    
    def stockageBDD(self,informationsInscription):
        donnees = informationsInscription.split(',')
        email = str(donnees[0])
        motDePasse = str(donnees[1])
        nom = donnees[2]
        adresse = str(donnees[4]+' '+donnees[5]+' '+donnees[6])
        nDeTel = donnees[7]
        nombrePers = donnees[8]
        numCarte = donnees[9]
        dateExpiration = donnees[10]
        cryptogramme = donnees[11]
        connection = connexionBDD()
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO foyer(nom,nbr_pers,mail,tel,adresse,num_carte,motDePasse,dateExpiration,cryptogramme) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sql,(nom,nombrePers,email,nDeTel,adresse,numCarte,motDePasse,dateExpiration,cryptogramme))
                connection.commit()
        finally:
            connection.close()
        self.display()

    def display(self):
        return cherrypy.session['mystring']
    
class Connexion(object):
    @cherrypy.expose
    def __init__(self):
        self.inscription = Inscription()
        self.collectivite = Collectivite()
        
    def index(self):
        return open("html/connexion.html")
    index.exposed = True
    
    @cherrypy.expose
    def generate(self, inputemail, inputpassword):
        if inputemail == 'collectivite@devinci.fr' and inputpassword == '0000':
            raise cherrypy.HTTPRedirect('/collectivite/')
        if self.checkIfClientInscrit(inputpassword,inputemail) == False:
            raise cherrypy.HTTPRedirect('/inscription/')
        else:
            raise cherrypy.HTTPRedirect('/produits/')
    
    def checkIfClientInscrit(self,inputpassword,inputemail):
        sql = "Select idCompte from foyer where motDePasse = %s and mail = %s;"
        connection = connexionBDD()
        try :
            cursor = connection.cursor()
            cursor.execute(sql,(inputpassword,inputemail))
            resultat = cursor.fetchone()
            connection.commit()
        finally:
            connection.close()
        if resultat == None:
            return False
        else :
            return resultat['idCompte']
            
    
    def display(self,message):
        cherrypy.session['mystring'] = message
        return cherrypy.session['mystring']
    
class Collectivite(object):
    @cherrypy.expose
    def __init__(self):
        #self.accueil = Accueil()
        self.top5produits = self.produitsPlusDemandes()
        c= folium.Map(location=[48.8600019,2.3449987],zoom_start=15) #zoom sur le quartier cible, nous 1e arrondissement
        geolocator = Nominatim()
        #location = geolocator.geocode("29 rue des Bourdonnais, 75001")
        #folium.Marker([location.latitude, location.longitude],popup="carrefour").add_to(c)
        sql = "select adresse_lat,adresse_long,nom_magasin from magasin"
        connection = connexionBDD()
        tableauAdresse = []
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql)
                connection.commit()
                for row in cursor:
                    tableauAdresse.append({'adresse_lat':row['adresse_lat'],'adresse_long':row['adresse_long'],'nom_magasin':row['nom_magasin']})
        finally:
            connection.close()
        for row in tableauAdresse:
            #location = geolocator.geocode(row[0])
            locationLat = row['adresse_lat']
            locationLong = row['adresse_long']
            nom_magasin = row['nom_magasin']
            folium.Marker([locationLat, locationLong],popup=nom_magasin).add_to(c)
        c.save('html/mapmagasin.html')
        a = folium.Map(location=[48.8600019,2.3449987],zoom_start=15) #zoom sur le quartier cible, nous 1e arrondissement de Paris
        geolocator = Nominatim()
        sql = "select adresse from foyer"
        connection = connexionBDD()
        tableauAdresse = []
        try:
            cursor = connection.cursor()
            cursor.execute(sql)
            connection.commit()
            for row in cursor:
                tableauAdresse.append(row['adresse'])
        finally:
            connection.close()
        for row in tableauAdresse:
            location = geolocator.geocode(row)
            folium.Marker([location.latitude, location.longitude]).add_to(a)
        a.save('html/mapfoyer.html')
        
    def produitsPlusDemandes(self):
        sql = "select nom_produit ,sum(quantiteCommandee) from commande group by nom_produit order by sum(quantiteCommandee) desc limit 5;"
        connection = connexionBDD()
        tableauProduits = []
        try :
            cursor = connection.cursor()
            cursor.execute(sql)
            connection.commit()
            for row in cursor:
                tableauProduits.append(row['nom_produit'])
        finally:
            connection.close()
        return tableauProduits
    
    @cherrypy.expose
    def index(self):
        return '''
<html>
    <head>
        <meta charset="utf-8" name="Collectivite" content="Liste des 5 produits les plus commandés">
        <link rel="stylesheet" type="text/css" href="../css/collectivite.css">
        <title>Collectivités</title>
    </head>
        
    <body>
        <a href="/html/mapmagasin.html">Cliquez ici pour afficher la carte de localisation des magasins></a>
        <a href="/html/mapfoyer.html">Cliquez ici pour afficher la carte de localisation des foyers></a>
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
        <a href="/accueil/"><button type="submit">Retour vers l'accueil</button></a>
    </body>
</html>
'''
    index.exposed = True
'''    
    def mapmagasin():
        return open("html/mapmagasin.html")
    def mapfoyer():
        return open("html/mapfoyer.html")
'''   
class Produits(object):
    @cherrypy.expose
    def __init__(self):
        #self.accueil = Accueil()
        self.quantite = [['Pâtes', '', 'paquet(s) de 500 grammes'],
            ['Riz', '', 'paquet(s) de 500 grammes'],
            ['Eau', '', 'pack(s) de 8 bouteilles'],
            ['Pain', '', 'paquet(s) de 12 tranches'],
            ['Jambon', '', 'paquet(s) de 4 tranches'],
            ['Fromage', '', 'unité'],
            ['Poulet', '', 'entier'],
            ['Haricots verts', '', 'boîte(s) de conserve, 250'],
            ['Carottes', '', 'paquet(s) de 10 carottes'],
            ['Yaourt', '', 'pack(s) de 8'],
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
        html += '</form>'
        html += '</table>'
        html += '<table style = "width : 100%">'
        html += '<tr>'
        html += '<th><p>Votre commande sera directement débitée de votre carte bancaire.</p>'
        html += '<p></p><a href="/accueil/"><button type="submit">Se déconnecter</button></a>'
        html += '<p></p><a href="/produits/"><button type="submit">Passer une autre commande</button></a></th>'
        html += '</tr>'
        html += '</table></body></html>'
        return html
    index.exposed = True
    #toutes les quantités sont dans un tableau
    
    def ajoutCommande(self,produit,quantite):
        connection = connexionBDD()
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO commande(nom_produit,quantiteCommandee) VALUES(%s,%s);"
                cursor.execute(sql,(produit,quantite))
                connection.commit()
        finally:
            connection.close()
        
    @cherrypy.expose
    def result(self, quantite_temp):
        #met la liste des quantités (quantite_temp) dans la matrice quantite de base
        for i in range(len(self.quantite)):
            if quantite_temp[i]=='':
                quantite_temp[i]=0
            self.quantite[i][1] = int(quantite_temp[i])
            if self.quantite[i][1]>0:
                self.ajoutCommande(self.quantite[i][0],int(quantite_temp[i]))
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
            if(self.quantite[i][1] != 0):
                html += '<tr><td>'+ str(self.quantite[i][0]) + '</td>'
                html += '<td>'+ str(self.quantite[i][1]) +'</td>'
                html += '<td>'+ str(self.quantite[i][2]) +'</td></tr>'

        html += '</table></body></html>'                        
        return html
    index.exposed = True

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
        '/html':
        { 
            'tools.staticdir.on':True,
            'tools.staticdir.dir':os.path.abspath("./html")
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