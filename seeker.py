import argparse
import colorama                       
from colorama import Fore

banner = Fore.LIGHTRED_EX + """
                               ___                              
                              (   )                             
    .--.      .--.     .--.    | |   ___     .--.    ___ .-.    
  /  _  \    /    \   /    \   | |  (   )   /    \  (   )   \   
 . .' `. ;  |  .-. ; |  .-. ;  | |  ' /    |  .-. ;  | ' .-. ;  
 | '   | |  |  | | | |  | | |  | |,' /     |  | | |  |  / (___) 
 _\_`.(___) |  |/  | |  |/  |  | .  '.     |  |/  |  | |        
(   ). '.   |  ' _.' |  ' _.'  | | `. \    |  ' _.'  | |        
 | |  `\ |  |  .'.-. |  .'.-.  | |   \ \   |  .'.-.  | |        
 ; '._,' '  '  `-' / '  `-' /  | |    \ .  '  `-' /  | |        
  '.___.'    `.__.'   `.__.'  (___ ) (___)  `.__.'  (___)                                                              
"""

def menu_principal():
    print(Fore.LIGHTCYAN_EX + "\nVeuillez sélectionner un outils:")
    print(Fore.LIGHTBLUE_EX + "1. CVE Scrapper")
    print("2. Email hunter")
    print("3. Nmap Scanner")
    print("4. Mail Breach")
    print("5. Password Breach")
    print("6. Quitter")

def sous_menu_script_a():
    print(Fore.LIGHTGREEN_EX + "\n++++CVE SCRAPPER++++")
    print(Fore.LIGHTCYAN_EX + "\nCe script est un outil qui permet de collecter des informations sur les vulnérabilités connues \nsous le nom de CVE (Common Vulnerabilities and Exposures). Il fonctionne en spécifiant une date et un niveau de gravité,\npuis recherche les vulnérabilités correspondantes. Une fois les informations collectées,\nle script enregistre les résultats dans un fichier placé dans le répertoire Rapports.")
    print("\nPour commencer à utiliser la fonctionnalité CVE Scrapper, il suffit d'utiliser la commande: " + Fore.LIGHTRED_EX + "python3 cve_scrapper.py")
    # Explication du script A

def sous_menu_script_b():
    print(Fore.LIGHTGREEN_EX + "\n++++EMAIL HUNTER++++")
    print(Fore.LIGHTBLUE_EX + "\nCe script est un outil de recherche d'e-mails associés à un domaine cible qui utilise l'API de Hunter.io pour effectuer une \nrecherche de domaine et récupérer les adresses e-mail associées.\nLe script prend le domaine cible en argument de ligne de commande et envoie une requête à l'API.\nEnsuite, il traite la réponse obtenue et extrait les adresses e-mail pertinentes vers un fichier Excel (.xlsx) dans le répertoire Rapports.")
    print("\nPour commencer à utiliser la fonctionnalité Email Hunter, il suffit d'utiliser la commande: " + Fore.LIGHTRED_EX + "python3 email_hunter.py")
    # Explication du script B

def sous_menu_script_c():
    print(Fore.LIGHTGREEN_EX + "\n++++NMAP SCANNER++++")
    print(Fore.LIGHTMAGENTA_EX + "\nCe script effectue un scan de ports en utilisant la bibliothèque Nmap. Pour cela il effectue un balayage de l'hôte \net des ports spécifiés et renvoie en résultat Les résultats du scan l'état des ports ouverts,les protocoles utilisés \net les services associés. Finalement, il exporte les scans en format pdf dans le répertoire Rapports.")
    print("\nPour commencer à utiliser la fonctionnalité Nmap Scanner, il suffit d'utiliser la commande: " + Fore.LIGHTRED_EX + "python3 nmap_scanner.py")
    # Explication du script C

def sous_menu_script_d():
    print(Fore.LIGHTGREEN_EX + "\n++++MAIL BREACH++++")
    print(Fore.LIGHTRED_EX + "\nCe script permet de vérifier si une adresse e-mail a été compromise dans une fuite de données. Il utilise l'API \nHave I Been Pwned pour rechercher le hachage SHA-1 de l'adresse e-mail fournie. Le script génère le hachage SHA-1 de\nl'adresse e-mail et recherche les préfixes correspondants dans l'API. Si un préfixe correspondant est trouvé,\ncela indique que l'adresse e-mail a été compromise.")
    print("\nPour commencer à utiliser la fonctionnalité Mail Breach, il suffit d'utiliser la commande: " + Fore.LIGHTCYAN_EX + "python3 mail_breach.py")
    # Explication du script D

def sous_menu_script_e():
    print(Fore.LIGHTGREEN_EX + "\n++++PASSWORD BREACH++++")
    print(Fore.LIGHTBLUE_EX + "\nCe script permet de vérifier si un mot de passe a été compromis dans une fuite de données. Il utilise l'API \nHave I Been Pwned pour rechercher le hachage SHA-1 de l'adresse e-mail fournie. Le script génère le hachage SHA-1 de\nl'adresse e-mail et recherche les préfixes correspondants dans l'API. Si un préfixe correspondant est trouvé,\ncela indique que l'adresse e-mail a été compromise.")
    print("\nPour commencer à utiliser la fonctionnalité Password Breach, il suffit d'utiliser la commande: " + Fore.LIGHTRED_EX + "python3 password_breach.py")
    # Explication du script E

def main():
    parser = argparse.ArgumentParser(prog='seeker.py', description='Programme Boîte à outils Seeker', add_help=False)
    parser.add_argument('-h', '--aide_menu', action='store_true', help='afficher le menu d\'aide')
    args, _ = parser.parse_known_args()

    if args.aide_menu:
        menu_principal()
        option = input(Fore.LIGHTYELLOW_EX + "\nEntrez le numéro de l'outils : ")
        if option == '1':
            sous_menu_script_a()
        elif option == '2':
            sous_menu_script_b()
        elif option == '3':
            sous_menu_script_c()
        elif option == '4':
            sous_menu_script_d()
        elif option == '5':
            sous_menu_script_e()
        elif option == '6':
            print("Sortie...")
        else:
            print(Fore.RED + "Option invalide.")
    else:
        print(banner)
        print(Fore.LIGHTCYAN_EX + "Bienvenue sur Seeker : Votre toolbox de cybersécurité polyvalent!")
        print(Fore.LIGHTBLUE_EX + "\nSeeker est un toolbox polyvalent qui regroupe des fonctionnalités avancées pour protéger vos données\net assurer la sécurité de vos systèmes. Avec son interface conviviale et ses capacités étendues, Seeker vous permet\nde prendre des mesures proactives pour sécuriser vos infrastructures et minimiser les risques.")
        print(Fore.LIGHTYELLOW_EX + "Vous pouvez accéder au menu d'aide en utilisant 'python3 seeker.py -h'.")

if __name__ == '__main__':
    main()
