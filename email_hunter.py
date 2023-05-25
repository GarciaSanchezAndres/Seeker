#   ______                 _ _   _    _             _            
#  |  ____|               (_) | | |  | |           | |           
#  | |__   _ __ ___   __ _ _| | | |__| |_   _ _ __ | |_ ___ _ __ 
#  |  __| | '_ ` _ \ / _` | | | |  __  | | | | '_ \| __/ _ \ '__|
#  | |____| | | | | | (_| | | | | |  | | |_| | | | | ||  __/ |   
#  |______|_| |_| |_|\__,_|_|_| |_|  |_|\__,_|_| |_|\__\___|_|   
                                                               
import os
import xlsxwriter
import requests
import colorama
from colorama import Fore


def process_response(data):
    """
    Traite la réponse obtenue de l'API.
    """
    emails = []
    try:
        for email in data['data']['emails']:
            if 'value' in email:
                print(Fore.LIGHTYELLOW_EX + "\n-> Email : " + email['value'])
                emails.append(email['value'])
    except Exception:
        print(Fore.RED + "Impossible de trouver des informations.")
        emails = []
    return emails


def send_request(url):
    """
    Envoie une requête personnalisée à l'API.
    """
    try:
        response = requests.get(url, timeout=5, allow_redirects=True)
        return response.json()
    except Exception as excp:
        print(Fore.RED + "Erreur dans send_request :", str(excp))
        return None


def save_emails(emails, directory):
    """
    Enregistre les résultats des e-mails dans un fichier XLSX dans le répertoire spécifié.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)

    file_path = os.path.join(directory, 'hunted_emails.xlsx')

    try:
        workbook = xlsxwriter.Workbook(file_path)
        worksheet = workbook.add_worksheet()
        row = 0
        col = 0

        for email in emails:
            worksheet.write(row, col, email)
            row += 1

        workbook.close()
        print(Fore.LIGHTGREEN_EX + f"\nRésultats des e-mails enregistrés dans '{file_path}'")

    except Exception as excp:
        print(Fore.RED + "Erreur lors de l'enregistrement des e-mails dans un fichier :", str(excp))


def main():
    """
    Fonction principale de l'outil.
    """
    import sys  # Move the import statement here
    import colorama
    from colorama import Fore
    
    if len(sys.argv) < 2:
        print(Fore.LIGHTBLUE_EX + "Veuillez fournir un domaine cible <DOMAINE>   --> python3 email_hunter.py example.com")
        return

    target = sys.argv[1]
    api_key = "52e43b8c4d5e38aa0935956c2201382469b3e48d"
    response = None
    emails = []

    try:
        url = f"https://api.hunter.io/v2/domain-search?domain={target}&api_key={api_key}"
        response = send_request(url)
        if response:
            emails = process_response(response)
            save_emails(emails, "Rapports")

    except Exception as exception:
        print(Fore.RED + "Erreur dans la fonction principale :", str(exception))

    print(Fore.LIGHTGREEN_EX + "Génération du rapport terminée.")


if __name__ == "__main__":
    main()

