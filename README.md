# projet-integrateur

Pour lancer l'application web:
1) Vous devez avoir python installé sur votre machine.
2) Vous devez avoir npm installé sur votre machine.
3) Placez-vous dans le dossier web-app/back et lancez la commande "pip install requirements.txt" afin d'installer les dépendances python
4) Placez-vous dans le dossier web-app/front et lancez la commande "npm install" afin d'installer les dépendances du front
5) Vous pouvez maintenant lancer chaque microservice. Pour cela placez vous dans le dossier web-app/back et lancer la commande "python ./[nom_du_microservice]". Les noms des microservices sont les suivants : BDDdefault.py, BDDgame.py, BDDuser.py, gestCNN.py, ms-questionsdecision.py. Il faut également lancer le dispatcher, pour cela exécuter la commande "python ./main.py".
6) Pour lancer l'interface web, placez-vous dans le dossier web-app/front et lancer la commande "npm start".
7) Le projet s'éxécute à l'adresse http://localhost:3000/
