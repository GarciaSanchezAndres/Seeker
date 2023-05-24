#   _   _                          _____                                 
#  | \ | |                        / ____|                                
#  |  \| |_ __ ___   __ _ _ __   | (___   ___ __ _ _ __  _ __   ___ _ __ 
#  | . ` | '_ ` _ \ / _` | '_ \   \___ \ / __/ _` | '_ \| '_ \ / _ \ '__|
#  | |\  | | | | | | (_| | |_) |  ____) | (_| (_| | | | | | | |  __/ |   
#  |_| \_|_| |_| |_|\__,_| .__/  |_____/ \___\__,_|_| |_|_| |_|\___|_|   
#                        | |                                             
#                        |_|                                             


import nmap
import sys
import socket
import os
from reportlab.pdfgen import canvas
from datetime import datetime
import colorama                         #Couleurs
from colorama import Fore

if len(sys.argv) != 3:
    print(Fore.LIGHTYELLOW_EX + "Utilisation: ./port.py <Adresse_Hôte> <Plage_de_Ports>")
    sys.exit(0)

hostaddress = sys.argv[1]
portrange = sys.argv[2]

ipaddress = socket.gethostbyname(hostaddress)                          # traduire le nom d'hôte en adresse IPv4

# Créer le répertoire 'Rapports' s'il n'existe pas
directory = "Rapports"
if not os.path.exists(directory):
    os.makedirs(directory)

# Créer un nouveau fichier PDF avec un nom unique basé sur l'horodatage
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
pdf_filename = os.path.join(directory, "rapport_scan_ports_{}.pdf".format(timestamp))
pdf = canvas.Canvas(pdf_filename)

# Définir les styles du PDF
title_style = "Helvetica-Bold"
subtitle_style = "Helvetica"
content_style = "Courier"

# Afficher la bannière
def display_banner():
    print(Fore.LIGHTBLUE_EX + "*****************************************")
    print(Fore.LIGHTBLUE_EX + "     Scan de l'hôte : " + ipaddress)
    print(Fore.LIGHTBLUE_EX + "*****************************************")

try:
    # Initialiser le scanner de ports
    nmScan = nmap.PortScanner()                         # Instancier un objet nmap.PortScanner
    display_banner()                                    # Afficher la bannière initiale
    nmScan.scan(ipaddress, portrange)                   # Balayer l'hôte spécifié et les ports dans la plage
except nmap.PortScannerError:
    print(Fore.RED + 'Nmap non trouvé', sys.exc_info()[0])
    sys.exit(0)
except:
    print(Fore.RED + "Erreur inattendue:", sys.exc_info()[0])
    sys.exit(0)

# Afficher les résultats dans le terminal et les écrire simultanément dans le PDF
def print_output(text):
    global y_position                       # Déclarer y_position comme variable globale
    print(text)
    pdf.drawString(50, y_position, text)
    y_position -= 20                        # Mettre à jour la position y pour la ligne suivante

# Écrire le titre et les sous-titres dans le PDF
pdf.setFont(title_style, 18)
pdf.drawString(50, 750, "Rapport du scan des ports")
pdf.setFont(subtitle_style, 14)
pdf.drawString(50, 700, "Hôte : %s (%s)" % (hostaddress, ipaddress))

# Parcourir les protocoles et les ports ouverts pour les afficher dans le terminal et le PDF
y_position = 650                                # Position de départ y pour le contenu du PDF
pdf.setFont(content_style, 12)

print_output(Fore.LIGHTYELLOW_EX + "\nHôte : %s (%s)" % (ipaddress, hostaddress))
print_output(Fore.LIGHTYELLOW_EX + "État : %s" % nmScan[ipaddress].state())

for proto in nmScan[ipaddress].all_protocols():
    print_output("\nProtocole : %s" % proto)

    for port in nmScan[ipaddress][proto]:
        if nmScan[ipaddress][proto][port]['state'] == 'open':
            print_output("Port : %s\tÉtat : %s\tService : %s" % (
                port, nmScan[ipaddress][proto][port]['state'], nmScan[ipaddress][proto][port]['name']))

# Enregistrer le fichier PDF
pdf.save()

print(Fore.LIGHTGREEN_EX + "\nRapport de scan : %s" % pdf_filename)
