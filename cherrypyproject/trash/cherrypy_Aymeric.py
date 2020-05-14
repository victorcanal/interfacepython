import pymysql
import cherrypy
import os

def connexionBDD():
    connection = pymysql.connect(host='127.0.0.1',
    user='root',
    password='Pichagouille47',                             
    db='python',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor)
    return connection

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
        motDePasse =donnees[1]
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

    def display(self):
        return cherrypy.session['mystring']
    
class Connexion(object):
    @cherrypy.expose
    def __init__(self):
        self.inscription = Inscription()
        
    def index(self):
        return open("html/connexion.html")
    index.exposed = True
    
    @cherrypy.expose
    def generate(self, inputemail, inputpassword):
        if self.checkIfClientInscrit(inputpassword,inputemail) == False:
            raise cherrypy.HTTPRedirect('/inscription/')
        else:
            self.display("vous êtes connectés ! ")
    
    def checkIfClientInscrit(self,inputpassword,inputemail):
        inscrit = True
        sql = "Select mail,motDePasse from foyer where motDePasse = %s and mail = %s;"
        connection = connexionBDD()
        try :
            cursor = connection.cursor()
            cursor.execute(sql,(inputpassword,inputemail))
            resultatSelect = []
            for row in cursor:
                resultatSelect.append(row)
            if len(resultatSelect)==0:
                inscrit = False
        finally:
            connection.close()
        return inscrit
    
    def display(self,message):
        cherrypy.session['mystring'] = message
        return cherrypy.session['mystring']

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