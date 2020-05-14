# interfacepython
github du groupe interface python

CONTRIBUTEURS
Groupe composé de : Victor Canal, Aymeric Peronnau-Nyssens, Anna Bouillon, Bianca Bieder, Salomé Billy et Emilie Spriet

INFORMATIONS GENERALES
Nous avons hebergé notre programme sur un site qui est le suivant:

Notre projet est de répondre aux demandes des citoyens et des collectivités dans le cas d'un confinement total. Nous nous occupons de la gestion des demandes (saisie et analyse). 

Nous avons utilisé le module cherrypy sur python pour l'interface graphique (en nous appuyant sur des patrons html et css). Nous avons importé la librairie os afin de lier tous ces documents. Le projet utilise une base de donnée (MySQL) composée de 4 tables: Produits, Supermarchés, Foyers et Commandes. Nous avons enfin importé la librairie folium pour convertir les adresses des foyers et des supermarchés en coordonnées afin de les afficher dans une "map.html" dont le lien est accessible directement depuis notre site. 

Nous avons 2 interfaces disponibles. L'interface citoyen permet à celui-ci de s'inscrire sur la plateforme. Une fois inscrit, il choisit la quantité des produits qu'il veut choisir parmis une liste de 22 éléments que nous considérons essentiels. Il est possible d'accéder à l'interface Collectivite en se connectant à partir de la page d'accueil avec l'adresse mail : collectivite@devinci.fr avec le mot de passe "0000". Après connection, s'affichera le top 5 des produits commandés par les citoyens. En haut de cette page est disponible une map des foyers ainsi qu'une map des supermachés enregistrés dans notre base de donnée. 

GUIDE D'INSTALLATION
Le projet python à compiler est le projet python.py. Il faut qu'il soit dans le document principal et avoir avec lui les dossiers: images (5 png), css (avec tous les css) et enfin un dossier html (comprenant les html). Une fois le programme lancé, il suffit de naviguer entre les différentes pages pour avoir accès à toutes les disponibilités. 
