 ##  _____                   _   ____                      _     
 ## |  __ \                 | | |  _ \                    | |    
 ## | |__) |_      ___ __ __| | | |_) |_ __ ___  __ _  ___| |__  
 ## |  ___/\ \ /\ / / '__/ _` | |  _ <| '__/ _ \/ _` |/ __| '_ \ 
 ## | |     \ V  V /| | | (_| | | |_) | | |  __/ (_| | (__| | | |
 ## |_|      \_/\_/ |_|  \__,_| |____/|_|  \___|\__,_|\___|_| |_|                                                 

import hashlib                      #Interface commune à différents algorithmes de hachage sécurisés et de synthèse de messages
import requests                     #Requests vous permet d'envoyer des requêtes HTTP/1.1 très facilement
import argparse                     #Analyse/Syntaxe de ligne de commande
import colorama                     #Couleurs
from colorama import Fore

def check_leak(password): 

    SHA1 = hashlib.sha1(password.encode('utf-8'))                   #Encodage en UTF-8
    hash_string = SHA1.hexdigest().upper()                          #Géneration du hash en majuscule
    prefix = hash_string[0:5]                                       #Récupèration des 5 premiers caractères

    header = {
        'User-Agent': 'password checker'
    }

    url = "https://api.pwnedpasswords.com/range/{}".format(prefix)                              #Accède à l'API de HaveIbeenpawned

    req = requests.get(url, headers=header).content.decode('utf-8')
    hashes = dict(t.split(":") for t in req.split('\r\n'))                                      #Divise le résultat en une clé et les valeurs des préfixes des hash

    
    hashes = dict((prefix + key, value) for (key, value) in hashes.items())                     #Ajoute le préfixe aux valeurs clés du dictionnaire de hash

    for item_hash in hashes:
        if item_hash == hash_string:                    #Si le hash crée est égal à celui fourni par l'API, afficher le message suivant
            print(Fore.RED + "\nOh non! {} est déjà apparu lors d'une filtration de données, il a été utilisé {} fois, et ne devrait pas être utilisé. ".format(password,hashes[hash_string]))
            break

    if hash_string != item_hash:                #Sinon afficher ce message
        print(Fore.LIGHTGREEN_EX + "\nBonne nouvelle! {} n'a jamais été filtré".format(password))

    exit()

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--password", help="Renseignez votre mot de passe:")                              #Syntaxe attendue
args = parser.parse_args()

argv = vars(args)                           #Retourne _dict_de la liste
password = argv['password'] 

if args.password:
    check_leak(password)                            #Active la fonction lorsqu'un mot de passe est donné au script
else:
    print(Fore.LIGHTYELLOW_EX+ f"\nAucun mot de passe renseigné\n")                           #Message affiché lorsqu'aucun mot de passe n'est specifié
    parser.print_help()                         #Affiche message help

#Intéraction avec l'API: https://www.youtube.com/watch?v=_co5vQD_PKc&ab_channel=EdGoad