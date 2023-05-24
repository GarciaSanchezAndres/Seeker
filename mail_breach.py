##  __  __       _ _   ____                      _     
## |  \/  |     (_) | |  _ \                    | |    
## | \  / | __ _ _| | | |_) |_ __ ___  __ _  ___| |__  
## | |\/| |/ _` | | | |  _ <| '__/ _ \/ _` |/ __| '_ \ 
## | |  | | (_| | | | | |_) | | |  __/ (_| | (__| | | |
## |_|  |_|\__,_|_|_| |____/|_|  \___|\__,_|\___|_| |_|
                                                     
import hashlib                                          #Interface commune à différents algorithmes de hachage sécurisés et de synthèse de messages
import requests                                         #Requests vous permet d'envoyer des requêtes HTTP/1.1 très facilement
import argparse                                         #Analyse/Syntaxe de ligne de commande
import re                                               #regular expressions
import colorama                                         #Couleurs
from colorama import Fore

def check_leak(email):
    SHA1 = hashlib.sha1(email.encode('utf-8'))                              #Encodage en UTF-8
    hash_string = SHA1.hexdigest().upper()                                  #Géneration du hash en majuscule
    prefix = hash_string[:5]                                                #Récupèration des 5 premiers caractères

    header = {
        'User-Agent': 'email checker'
    }

    url = f"https://api.pwnedpasswords.com/range/{prefix}"                      #Accède à l'API de HaveIbeenpawned

    req = requests.get(url, headers=header).content.decode('utf-8')
    hashes = dict(t.split(':') for t in req.split('\r\n'))                          #Divise le résultat en une clé et les valeurs des préfixes des hash

    hashes = {prefix + key: value for key, value in hashes.items()}                     #Ajoute le préfixe aux valeurs clés du dictionnaire de hash

    for item_hash in hashes:
        if item_hash == hash_string:                        #Si le hash crée est égal à celui fourni par l'API, afficher le message suivant
            print(Fore.RED + f"\nOh non! L'adresse mail '{email}' a été impliqué dans une filtration de données, et il est recommandé de prendre les mesures nécessaires pour sécuriser votre compte.")
            break

    if hash_string != item_hash:                                    #Sinon afficher ce message
        print(Fore.LIGHTGREEN_EX + f"\nBonne Nouvelle! L'adresse mail '{email}' n'a pas été impliqué dans une filtration de données.")

    exit()


def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'                       #Syntaxe attendue
    if not re.match(pattern, email):
        print(Fore.LIGHTYELLOW_EX + "\nFormat d'adresse mail invalide. Veuillez utiliser le format suivant: 'example@example.example'.")            #Message d'erreur
        return False
    return True


parser = argparse.ArgumentParser()
parser.add_argument("-e", "--email", help="Renseignez votre email:")
args = parser.parse_args()

if args.email: 
    if validate_email(args.email): 
        check_leak(args.email)                              #Active la fonction lorsqu'un mot de passe est donné au script
else:
    print(Fore.LIGHTBLUE_EX +f"\nAucun mail n'a été renseigné.\n")                      #Message affiché lorsqu'aucun mot de passe n'est specifié
    parser.print_help()                     #Affiche message help

# Intéraction avec l'API: https://www.youtube.com/watch?v=_co5vQD_PKc&ab_channel=EdGoad