# This file contains the WSGI configuration required to serve up your
# web application at http://vcanal.pythonanywhere.com/
# It works by setting the variable 'application' to a WSGI handler of some
# description.
#

# +++++++++++ GENERAL DEBUGGING TIPS +++++++++++
# getting imports and sys.path right can be fiddly!
# We've tried to collect some general tips here:
# https://help.pythonanywhere.com/pages/DebuggingImportError


# +++++++++++ HELLO WORLD +++++++++++
# A little pure-wsgi hello world we've cooked up, just
# to prove everything works.  You should delete this
# code to get your own working.

import sys
sys.stdout = sys.stderr

import atexit
import cherrypy
import os
import pymysql
import folium
from geopy.geocoders import Nominatim

cherrypy.config.update({'environment': 'embedded'})

if cherrypy.__version__.startswith('3.0') and cherrypy.engine.state == 0:
    cherrypy.engine.start(blocking=False)
    atexit.register(cherrypy.engine.stop)

#class Root(object):
#    def index(self):
#        return 'Hello World!'
#    index.exposed = True

def connexionBDD():
    connection = pymysql.connect(host='vcanal.mysql.pythonanywhere-services.com',
    user='vcanal',
    password='rootroot',
    db='vcanal$default',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor)
    return connection

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
    def generate(self, inputemail, inputpassword, inputnom, inputprenom, inputnumerorue, inputnomrue, inputcodepostal, inputnumero, inputnombre, inputnumcarte, inputexpirationdate, inputcryptogramme):
        some_string = inputemail + "," + inputpassword + "," +inputnom + "," + inputprenom + "," + inputnumerorue + " " + inputnomrue + " " + inputcodepostal + "," + inputnumero + "," + inputnombre + "," + inputnumcarte + "," + inputexpirationdate + "," + inputcryptogramme
        cherrypy.session['mystring'] = 'vous êtes inscrits ! '
        self.stockageBDD(some_string)
        raise cherrypy.HTTPRedirect('/connexion/')

    def stockageBDD(self,informationsInscription):
        donnees = informationsInscription.split(',')
        email = str(donnees[0])
        motDePasse = str(donnees[1])
        nom = donnees[2]
        adresse = donnees[4]
        nDeTel = donnees[5]
        nombrePers = donnees[6]
        numCarte = donnees[7]
        dateExpiration = donnees[8]
        cryptogramme = donnees[9]
        connection = connexionBDD()
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO foyer(nom,nbr_pers,mail,tel,adresse,num_carte,motDePasse,dateExpiration,cryptogramme) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sql,(nom,nombrePers,email,nDeTel,adresse,numCarte,motDePasse,dateExpiration,cryptogramme))
                connection.commit()
        finally:
            connection.close()
        self.display()

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

class Collectivite(object):
    @cherrypy.expose
    def __init__(self):
        self.top5produits = self.produitsPlusDemandes()
        self.circular = self.Circular()

    def produitsPlusDemandes(self):
        c= folium.Map(location=[48.8600019,2.3449987],zoom_start=15) #zoom sur le quartier cible, nous 1er arrondissement
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
        try:
            for row in tableauAdresse:
                #location = geolocator.geocode(row[0])
                locationLat = row['adresse_lat']
                locationLong = row['adresse_long']
                nom_magasin = row['nom_magasin']
                folium.Marker([locationLat, locationLong],popup=nom_magasin).add_to(c)
            c.save('html/mapmagasin.html')
        except:
            print("geopy error")
        a = folium.Map(location=[48.8600019,2.3449987],zoom_start=12) #zoom sur le quartier cible, nous 1er arrondissement de Paris
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
        try:
            for row in tableauAdresse:
                location = geolocator.geocode(row)
                folium.Marker([location.latitude, location.longitude]).add_to(a)
            a.save('html/mapfoyer.html')
        except:
            print("geopy error")

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

    def Circular(self):
        sql = "select nom_produit,  sum(quantiteCommandee) from commande group by nom_produit order by quantiteCommandee;"
        connection = connexionBDD()
        tableauCirc = []
        try :
            cursor = connection.cursor()
            cursor.execute(sql)
            connection.commit()
            for row in cursor:
                tableauCirc.append([row['nom_produit'],int(row['sum(quantiteCommandee)'])])
        finally:
            connection.close()
        return tableauCirc

    @cherrypy.expose
    def index(self):
        string = "['Produit','Quantité']"
        for i in self.circular:
            string += ',' + str(i)
        return '''
<html>
    <head>
        <meta charset="utf-8" name="Collectivite" content="Liste des 5 produits les plus commandés">
        <link rel="shortcut icon" href="/images/house-user-solid.svg"/>
        <link rel="stylesheet" type="text/css" href="../css/collectivite.css">
        <title>Collectivités</title>
    </head>
        <h1 id = "myHeader">Diagramme circulaire des produits commandés par quantité</h1>
        <div id="piechart"></div>
        <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
        <script type="text/javascript">
            // Load google charts
            google.charts.load('current', {'packages':['corechart']});
            google.charts.setOnLoadCallback(drawChart);

            // Draw the chart and set the chart values
            function drawChart() {
              var data = google.visualization.arrayToDataTable(['''+string+''']);

            var options = {'title':'Produits par quantités', 'width':750, 'height':600};

            var chart = new google.visualization.PieChart(document.getElementById('piechart'));
            chart.draw(data, options);
            }
        </script>
        <h1 id = "myHeader">Liste des 5 produits les plus commandés</h1>
        <p>Les cartes sont mises à jour 1 fois par jour à 14h. Elles utilisent le module geopy, qui peut ne pas fonctionner correctement, et ne pas se mettre à jour. (Timed out error)</p>
        <a href="/html/mapmagasin.html">Cliquez ici pour afficher la carte de localisation des magasins></a><br><br>
        <a href="/html/mapfoyer.html">Cliquez ici pour afficher la carte de localisation des foyers></a><br><br>
        <table style="width:100%">
        <tr>
            <th><h2 class = "produit">Le produit '''+self.top5produits[0]+''' est le premier produit le plus commandé.</h2></th>
            <th><h1><img src="/images/5_etoiles.png"></h1></th>
        </tr>
        <tr>
            <th><h2 class = "produit">Le produit '''+self.top5produits[1]+''' est le deuxième produit le plus commandé.</h2></th>
            <th><h1><img src="/images/4_etoiles.png"></h1></th>
        </tr>
        <tr>
            <th><h2 class = "produit">Le produit '''+self.top5produits[2]+''' est le troisième produit le plus commandé.</h2></th>
            <th><h1><img src="/images/3_etoiles.png"></h1></th>
        </tr>
        <tr>
            <th><h2 class = "produit">Le produit '''+self.top5produits[3]+''' est le quatrième produit le plus commandé.</h2></th>
            <th><h1><img src="/images/2_etoiles.png"></h1></th>
        </tr>
        </tr>
            <th><h2 class = "produit">Le produit '''+self.top5produits[4]+''' est le cinquième produit le plus commandé.</h2></th>
            <th><h1><img src="/images/etoile.png"></h1></th>
        </tr>
        <a href="/"><button type="submit">Retour vers l'accueil</button></a>
    </body>
</html>
'''
    index.exposed = True

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
            ['Haricots verts', '', 'boîte(s) de conserve, 250 grammes'],
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
        html += '<link rel="shortcut icon" href="/images/house-user-solid.svg"/>'
        html += '<link rel="stylesheet" type="text/css" href="../css/liste_commande.css">'
        html += '<title>Commande des produits</title>'
        html += '</head>'
        html += '<body>'
        html += '<h1 id = "myHeader">Commande</h1>'
        html += '<a href="#">Pour les besoins particuliers (allergies, traitements...), cliquez ici</a>'
        html += '<p>Choisissez votre produit ainsi que la quantité souhaitée. Mettez une quantité à côté du produit qui vous intéresse. Si vous ne mettez pas de quantité pour un produit il ne sera pas commandé. </p>'
        html += '<form method ="POST" action ="result">'

        for i in range(len(self.quantite)):
            html += '<h2 class = "produit">'+self.quantite[i][0]+' :</h2>'
            html += '<input type="number" size="25" placeholder="Quantité de '+self.quantite[i][0]+' :" name="quantite_temp" min="0" max="10"/>'
            #obligés de mettre la liste des quantités dans une liste, cherrypy ne prend pas en compte les matrices
            html += '<label for ="unite"> ' + self.quantite[i][2] + '.</label></br><br>'

        html += '<br><button type="submit">Valider la commande</button></form>'
        html += '<br><a href="/"><button type="button">Se déconnecter</button></a>'
        html += '</body></html>'
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
        html += '<body>'
        html += '<h2>Récapitulatif de votre commande</h2>'
        html += '<p>Date de la commande : <span id="datetime"></span></p>'
        html += '<script>'
        html += 'var dt = new Date();'
        html += 'document.getElementById("datetime").innerHTML = dt.toLocaleDateString();'
        html += '</script>'
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
        html += '</table>'
        html += '<table style = "width : 100%">'
        html += '<tr>'
        html += '<th><p>Votre commande sera directement débitée de votre carte bancaire.</p>'
        html += '<br><a href="/"><button type="submit">Se déconnecter</button></a>'
        html += '<br><a href="/produits/"><button type="submit">Passer une autre commande</button></a></th>'
        html += '</tr>'
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
        }

application = cherrypy.Application(Accueil(),script_name='', config=conf)

#HELLO_WORLD = """<html>
#<head>
#    <title>PythonAnywhere hosted web application</title>
#</head>
#<body>
#<h1>Hello, World!</h1>
#<p>
#    This is the default welcome page for a
#    <a href="https://www.pythonanywhere.com/">PythonAnywhere</a>
#    hosted web application.
#</p>
#<p>
#    Find out more about how to configure your own web application
#    by visiting the <a href="https://www.pythonanywhere.com/web_app_setup/">web app setup</a> page
#</p>
#</body>
#</html>"""


#def application(environ, start_response):
#    if environ.get('PATH_INFO') == '/':
#        status = '200 OK'
#        content = HELLO_WORLD
#    else:
#        status = '404 NOT FOUND'
#        content = 'Page not found.'
#    response_headers = [('Content-Type', 'text/html'), ('Content-Length', str(len(content)))]
#    start_response(status, response_headers)
#    yield content.encode('utf8')


# Below are templates for Django and Flask.  You should update the file
# appropriately for the web framework you're using, and then
# click the 'Reload /yourdomain.com/' button on the 'Web' tab to make your site
# live.

# +++++++++++ VIRTUALENV +++++++++++
# If you want to use a virtualenv, set its path on the web app setup tab.
# Then come back here and import your application object as per the
# instructions below


# +++++++++++ CUSTOM WSGI +++++++++++
# If you have a WSGI file that you want to serve using PythonAnywhere, perhaps
# in your home directory under version control, then use something like this:

# sys

#path = '/home/vcanal/path/to/my/app'
#if path not in sys.path:
#    sys.path.append(path)

#from my_wsgi_file import application  # noqa


# +++++++++++ DJANGO +++++++++++
# To use your own django app use code like this:
#import os
#import sys
#
## assuming your django settings file is at '/home/vcanal/mysite/mysite/settings.py'
## and your manage.py is is at '/home/vcanal/mysite/manage.py'
#path = '/home/vcanal/mysite'
#if path not in sys.path:
#    sys.path.append(path)
#
#os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
#
## then:
#from django.core.wsgi import get_wsgi_application
#application = get_wsgi_application()



# +++++++++++ FLASK +++++++++++
# Flask works like any other WSGI-compatible framework, we just need
# to import the application.  Often Flask apps are called "app" so we
# may need to rename it during the import:
#
#
#import sys
#
## The "/home/vcanal" below specifies your home
## directory -- the rest should be the directory you uploaded your Flask
## code to underneath the home directory.  So if you just ran
## "git clone git@github.com/myusername/myproject.git"
## ...or uploaded files to the directory "myproject", then you should
## specify "/home/vcanal/myproject"
#path = '/home/vcanal/path/to/flask_app_directory'
#if path not in sys.path:
#    sys.path.append(path)
#
#from main_flask_app_file import app as application  # noqa
#
# NB -- many Flask guides suggest you use a file called run.py; that's
# not necessary on PythonAnywhere.  And you should make sure your code
# does *not* invoke the flask development server with app.run(), as it
# will prevent your wsgi file from working.
