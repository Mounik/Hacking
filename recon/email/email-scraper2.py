from bs4 import BeautifulSoup  # Importation de la bibliothèque BeautifulSoup pour analyser l'HTML
import requests  # Importation du module requests pour effectuer des requêtes HTTP
import requests.exceptions  # Importation du sous-module exceptions de requests
import urllib.parse  # Importation du module urllib.parse pour parser les URL
from collections import deque  # Importation de deque pour une gestion efficace des listes (pile/file)
import re  # Importation du module re pour les expressions régulières

# Demande à l'utilisateur d'entrer une URL cible
user_url = str(input('[+] Enter Target URL To Scan: '))
urls = deque([user_url])  # Initialisation de la file avec l'URL cible

scraped_urls = set()  # Ensemble pour stocker les URLs déjà visitées
emails = set()  # Ensemble pour stocker les emails trouvés

count = 0  # Compteur initialisé à zéro
try:
    while len(urls):  # Tant qu'il y a des URL dans la file
        count += 1  # Incrémenter le compteur
        if count == 100:  # Si le compteur atteint 100, arrêter la boucle
            break
        url = urls.popleft()  # Retirer et obtenir l'URL de la file
        scraped_urls.add(url)  # Ajouter l'URL à l'ensemble des URLs déjà visitées

        parts = urllib.parse.urlsplit(url)  # Décomposer l'URL en ses composants (schéma, netloc, path, etc.)
        base_url = '{0.scheme}://{0.netloc}'.format(parts)  # Construire la partie de base de l'URL

        path = url[:url.rfind('/')+1] if '/' in parts.path else url  # Déterminer le chemin de l'URL

        print('[%d] Processing %s' % (count, url))  # Afficher le message de traitement pour cette URL
        try:
            response = requests.get(url)  # Envoyer une requête GET à l'URL
        except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):  # Gérer les exceptions de schéma ou de connexion
            continue

        new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text, re.I))  # Utiliser une expression régulière pour trouver les emails dans le texte de la page
        emails.update(new_emails)  # Mettre à jour l'ensemble des emails avec les nouveaux emails trouvés

        soup = BeautifulSoup(response.text, features="lxml")  # Analyser le contenu HTML de la réponse avec BeautifulSoup

        for anchor in soup.find_all("a"):  # Parcourir tous les ancres (liens) dans la page
            link = anchor.attrs['href'] if 'href' in anchor.attrs else ''  # Obtenir l'attribut href de chaque lien s'il existe
            if link.startswith('/'):
                link = base_url + link  # Si le lien commence par '/', ajouter la partie de base de l'URL
            elif not link.startswith('http'):
                link = path + link  # Si le lien ne commence pas par 'http', ajouter le chemin de l'URL
            if not link in urls and not link in scraped_urls:
                urls.append(link)  # Ajouter le lien à la file si ce n'est pas déjà visité
except KeyboardInterrupt:  # Gérer l'interruption du clavier (Ctrl+C)
    print('[-] Closing!')

for mail in emails:  # Parcourir et afficher tous les emails trouvés
    print(mail)
