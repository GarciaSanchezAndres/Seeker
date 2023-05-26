# Seeker 🔭
[![Typing SVG](https://readme-typing-svg.herokuapp.com?font=Fira+Code&pause=1000&width=435&lines=Explorez%2C+Prot%C3%A9gez%2C+Dominez+!)](https://git.io/typing-svg)

Êtes-vous préoccupé par la sécurité de vos réseaux et de vos mots de passe ? Vous craignez les vulnérabilités potentielles et les violations de données ? Ne cherchez plus, CyberSec Toolbox est l'outil ultime tout-en-un pour la cybersécurité.

Seeker est un puissant toolbox conçu pour renforcer votre posture en matière de cybersécurité et protéger vos précieux actifs. Avec son interface intuitive et ses fonctionnalités avancées, il permet aux individus et aux organisations de protéger proactivement leurs réseaux, de garantir la sécurité de leurs mots de passe, de filtrer les CVE (Common Vulnerabilities and Exposures) et bien plus encore.

Overview
---
![Capture d’écran du 2023-05-25 20-08-36](https://github.com/GarciaSanchezAndres/Seeker/assets/82510284/191fc80b-6b0c-4629-be6d-0c94ea72a92c)

How to use
---
La vidéo suivante montre comment lancer un script seeker:

[![Running Seeker](https://img.youtube.com/vi/k1qict_sfxo/0.jpg)](https://www.youtube.com/watch?v=k1qict_sfxo)
 
Requirements
---
Pour installer les librairies nécessaires utilisez la commande suivante:
```
$pip3 install -r requirements.txt
```

Installation
---
```
$git clone https://github.com/GarciaSanchezAndres/Seeker.git
$cd Seeker
$python3 seeker.py
```
Fonctionnalité d'envoi de mail
---
Seeker propose à l'utilisateur d'envoyer les rapports générés par mail à un destinataire de son choix depuis une adresse Gmail (de nouveaux smtp seront rajoutés dans les prochaines mises à jour). La commande est la suivante:
```
$python3 seeker.py -r
```
Cependant si votre compte gmail utilise une authentication 2FA, il faudra génèrer un mot de passe d'application qui sera demandé avec l'adresse expéditeur et destinataire du mail.
Voici les étapes pour générer ce mot de passe:
 1) Se connecter à https://myaccount.google.com/
 2) Cliquez sur l'onglet "Sécurité".
 3) Cliquez sur Validation en deux étapes
 4) Tout en bas de la page, cliquez sur "Mot de passe d'application"
 5) Selectionnez Messagerie puis votre OS. Votre mot passe sera généré (vous devez le noter)
 
![image](https://github.com/GarciaSanchezAndres/Seeker/assets/82510284/c680c35a-06c4-497c-99dc-11796e7fb607)

 6) Le mot de passe généré devra être utilisé lors de l'envoi des mails

Cette vidéo vous montre comment utiliser la fonctionnalité:

[![Sending an email with Seeker](https://img.youtube.com/vi/3UuD2FBMFuk/0.jpg)](https://www.youtube.com/watch?v=3UuD2FBMFuk)

A savoir
---
- Seeker utilise Nmap pour certaines de ces fonctions, il est donc fortement recommandé de l'installer sur une machine **Linux**.
- Si les commandes ne fonctionnant pas avec **$python3** essayez avec **$python**. Example: **$python seeker.py**. Cela dépent de votre version de Python!
