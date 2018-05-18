# Site de test pour la classification de visages

Ce projet web permet de tester le réseau élaboré pour le projet de classification 
des visages. Il a été réalisé en Flask et utilise une base de données SQLite embarquée
(avec SQLAlchemy). 

## Inclure le frozen model
Le fichier '.pb' doit être placé dans le dossier "network" du projet. S'il porte 
un nom différent de inception_v3_frozen_graph, il faut modifier l'attribut dans 
le fichier "image/analyseur_image.py". Si la liste de labels est différente, il
faut remplacer le fichier "network/liste_labels.txt", et également l'attribut
correspondant (il se trouve dans le même fichier).

####Remarque :
Les prédictions des images prennent un peu de temps à être générées, car le code n'est
pas prévu pour optimiser la rapidité d'exécution de l'analyse. 