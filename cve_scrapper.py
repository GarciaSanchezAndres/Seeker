#    _______      ________                                            
#   / ____\ \    / /  ____|                                           
#  | |     \ \  / /| |__     ___  ___ _ __ __ _ _ __  _ __   ___ _ __ 
#  | |      \ \/ / |  __|   / __|/ __| '__/ _` | '_ \| '_ \ / _ \ '__|
#  | |____   \  /  | |____  \__ \ (__| | | (_| | |_) | |_) |  __/ |   
#   \_____|   \/   |______| |___/\___|_|  \__,_| .__/| .__/ \___|_|   
#                                              | |   | |              
#                                              |_|   |_|              


import os                              # Importation du module os pour les opérations liées au système d'exploitation
import json                            # Importation du module json pour la manipulation des données JSON
import requests                        # Importation du module requests pour effectuer des requêtes HTTP
import argparse                        # Importation du module argparse pour gérer les arguments de ligne de commande
from queue import Queue                # Importation de la classe Queue du module queue
from threading import Thread           # Importation de la classe Thread du module threading
from bs4 import BeautifulSoup          # Importation de la classe BeautifulSoup du module bs4 (BeautifulSoup)
from datetime import datetime          # Importation de la classe datetime du module datetime
import colorama                         #Couleurs
from colorama import Fore


RESULTS_FILE = 'parsed_exploits.json'       # Fichier de résultats
CONCURRENT_THREADS = 50                      # Nombre de threads concurrents
CVSS_THRESHOLD = {                            # Seuil CVSS pour chaque niveau de gravité
    'low': (0.1, 3.9),
    'medium': (4.0, 6.9),
    'high': (7.0, 8.9),
    'critical': (9.0, 10.0)
}

MAX_CVE_COUNT = 50                              # Nombre maximum de CVE à récupérer


class CVEScrapper:
    def __init__(self, date, severity):
        self.results = []                                   # Liste pour stocker les résultats
        self.queue = Queue(CONCURRENT_THREADS * 2)          # File d'attente pour les URL à scraper
        self.cve_count = 0                                  # Compteur de CVE récupérés
        self.date = date                                    # Date spécifiée
        self.severity = severity                            # Niveau de gravité spécifié

    def save_results(self):
        output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Rapports')       # Répertoire de sortie
        os.makedirs(output_dir, exist_ok=True)                                                      # Création du répertoire si inexistant

        results_file = f'scrapped_cves_{self.date.strftime("%Y-%m")}.json'                          # Nom du fichier de résultats
        file_path = os.path.join(output_dir, results_file)                                          # Chemin complet du fichier de résultats

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=4)                         # Enregistrement des résultats au format JSON

        return results_file

    def scrape_cve_details(self, url):
        try:
            response = requests.get(url)
            if response.ok:
                soup = BeautifulSoup(response.text, 'html.parser')
                cve_id = url.split('cve_id=')[1]                                        # Extraction de l'ID CVE depuis l'URL
                cve_score = soup.find('div', {'class': 'cvssbox'}).text.strip()         # Score CVE
                cve_score = float(cve_score) if cve_score else 0.0                      # Conversion en float, 0.0 si vide
                if cve_score >= CVSS_THRESHOLD[self.severity][0] and cve_score <= CVSS_THRESHOLD[self.severity][1]:
                    cve_vulnerability_type = soup.findAll('td')[23].text.strip()                                    # Type de vulnérabilité CVE
                    cve_description = soup.find('div', {'class': 'cvedetailssummary'}).text.strip().replace('\n', ' ')              # Description CVE
                    authentication = soup.findAll('td')[21].text.strip()                                                            # Méthode d'authentification
                    access_complexity = soup.findAll('td')[20].text.strip()                                             # Complexité d'accès
                    references = [link['href'] for link in soup.findAll('td', {'class': 'r_average'})[0].findAll('a')]  # Références

                    data = {
                        'cve_id': cve_id,
                        'cve_score': cve_score,
                        'cve_vulnerability_type': cve_vulnerability_type,
                        'cve_description': cve_description,
                        'authentication': authentication,
                        'access_complexity': access_complexity,
                        'references': references
                    }

                    self.results.append(data)                     # Ajout des données à la liste des résultats
                    self.cve_count += 1                           # Incrémentation du compteur de CVE récupérés
                    print(Fore.LIGHTYELLOW_EX + f'-> {cve_id} Scraping réussi')         # Message de succès

        except Exception as e:
            pass

    def worker(self):
        while True:
            url = self.queue.get()
            self.scrape_cve_details(url)
            self.queue.task_done()

    def run(self):
        for _ in range(CONCURRENT_THREADS):
            t = Thread(target=self.worker)
            t.daemon = True
            t.start()

        try:
            if not self.date or not self.severity:
                print(Fore.LIGHTBLUE_EX + "Veuillez spécifier les deux paramètres : -d/--date et -s/--severity")
                exit(1)

            prefix = f'https://www.cvedetails.com/cve-details.php?cve_id=CVE-{self.date.year}-{{:04n}}'
            cves = [prefix.format(i) for i in range(1, 10000)]                      # Génération des URL des CVE
            for cve in cves:
                if self.cve_count >= MAX_CVE_COUNT:
                    break
                self.queue.put(cve.strip())                           # Ajout des URL à la file d'attente

            self.queue.join()

            results_file = self.save_results()

            if self.cve_count >= MAX_CVE_COUNT:
                print(Fore.LIGHTGREEN_EX + f"Le maximum de {MAX_CVE_COUNT} CVE a été atteint et enregistré dans le fichier : Rapports/{results_file}")
            else:
                print(Fore.LIGHTGREEN_EX+ f"Terminé. Total des CVE récupérés : {self.cve_count}. Enregistrés dans le fichier : Rapports/{results_file}")

        except Exception as e:
            print(Fore.RED+ f"Une erreur s'est produite : {e}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='CVEScrapper')
    parser.add_argument('-d', '--date', help='Spécifiez la date des CVE récupérés (AAAA-MM)')
    parser.add_argument('-s', '--severity', choices=['low', 'medium', 'high', 'critical'], help='Spécifiez le niveau de gravité des CVE récupérés')
    args = parser.parse_args()

    if not args.date and not args.severity:
        parser.print_help()
        exit(1)

    if args.date:
        try:
            date = datetime.strptime(args.date, '%Y-%m')
        except ValueError:
            print(Fore.RED + "Format de date invalide. Veuillez utiliser le format AAAA-MM.")
            exit(1)
    else:
        print(Fore.RED + "Veuillez spécifier les deux paramètres : -d/--date et -s/--severity")
        exit(1)

    cve_scrapper = CVEScrapper(date, args.severity)
    cve_scrapper.run()
