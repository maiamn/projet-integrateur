# projet-integrateur

Ce repo git comporte notre projet intégrateur dans le cadre de la 5SDBD.

Ce projet implémente une adaptation du jeu "Qui est-ce ?" en utilisant une architecture de micro-services ainsi qu'un modèle CNN pour déterminer les labels de photos uploadées pour jouer au jeu.

## Vous pouvez trouver trois dossiers :
  - Notebook: qui contient les notebooks qui nous ont servis à développer des fonctions, tester nos modèles localement
  - models: qui contient les scripts pythons à éxécuter pour lancer l'entrainement du CNN, ainsi que le meilleur modèle que nous avons obtenu
  - web-app: qui contient la partie architecture orientée service (SOA) et le site web

## Notebook

Vous pouvez trouver ici le notebook Final_tests, qui vous permet d'utiliser le modèle enregistré pour le tester sur vos propres photos en fournissant un chemin vers le dossier contenant vos photos.

## models

Deux modèles sont visibles, V2 et V3, cependant la V3 ne fonctionne pas. Le modèle V2 est celui que nous utilisons pour nos résultats.

Le modèle enregistré à été obtenu suite à un entrainement de 202 599 photos sur 100 epochs.

*Il peut être nécessaire de vérifier/modifier les variables des configurations au début du script pour adapter le path suite à des déplacements de fichiers, ou si vous souhaitez utiliser un dossier personnel.*

Vous devriez pouvoir accéder à nos courbes via le lien suivant : https://tensorboard.dev/experiment/viVHbZiMQKe9Ndi0py2juw/#scalars&run=train

## web-app

### Pour lancer l'application web:
1) Vous devez avoir python installé sur votre machine.
2) Vous devez avoir npm installé sur votre machine.
3) Placez-vous dans le dossier web-app/back et lancez la commande "pip install requirements.txt" afin d'installer les dépendances python
4) Placez-vous dans le dossier web-app/front et lancez la commande "npm install" afin d'installer les dépendances du front
5) Vous pouvez maintenant lancer chaque microservice. Pour cela placez vous dans le dossier web-app/back et lancer la commande "python ./[nom_du_microservice]". Les noms des microservices sont les suivants : BDDdefault.py, BDDgame.py, BDDuser.py, gestCNN.py, ms-questionsdecision.py. Il faut également lancer le dispatcher, pour cela exécuter la commande "python ./main.py".
6) Pour lancer l'interface web, placez-vous dans le dossier web-app/front et lancer la commande "npm start".
7) Le projet s'éxécute à l'adresse http://localhost:3000/
