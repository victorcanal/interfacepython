# interfacepython
github du groupe interface python

CONTRIBUTEURS

Groupe composé de : Victor Canal, Aymeric Peronnau-Nyssens, Anna Bouillon, Bianca Bieder, Salomé Billy et Emilie Spriet

INFORMATIONS GENERALES

Nous avons hebergé notre programme sur le site https://vcanal.pythonanywhere.com/.

Notre projet est de répondre aux demandes des citoyens et des collectivités dans le cas d'un confinement total. Nous nous occupons de la gestion des demandes (saisie et analyse). 


GUIDE D'INSTALLATION

NOTE : Le code python pour serveur local est daté, et ne présente pas d'intérêt particulier par rapport au site en ligne, hormis à titre informatif.

Le programme fonctionne normalement pour les versions de python 3.7 et 3.8, il n'est pas assuré qu'il fonctionne pour d'autres versions.
Les modules nécessaires au bon fonctionnement du programme python sont cherrypy, os, pymysql, folium et geopy.
Le script python2-script.txt pour MySQL doit être utilisé afin de peupler une base de données qui sera utilisée par le code python, mais la base de données actuellement utilisée par le site a été modifiée à plusieurs reprises à la main pour répondre a certains besoins.
Le projet python à compiler est le projet final.py (le fichier vcanal_pythonanywhere_com_wsgi.py n'est utilisable que par le site pythonanywhere.com pour créer le site à l'adresse vcanal.pythonanywhere.com). Il faut qu'il soit dans le document principal et avoir avec lui les dossiers : images (5 .png, 1 .svg), css (7 .css) et enfin un dossier html (3 .html). Une fois le programme lancé, il suffit de naviguer entre les différentes pages à l'adresse localhost:8080 (127.0.0.1:8080) pour avoir accès à toutes les disponibilités. 
