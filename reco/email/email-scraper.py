from bs4 import BeautifulSoup
import requests
import requests.exceptions
import urllib.parse
from collections import deque
import re

# Demande à l'utilisateur d'entrer l'URL cible à scanner
user_url = str(input('[+] Entrer l\'URL cible à scanner: '))
urls = deque([user_url])  # Crée une file d'attente avec l'URL de l'utilisateur

scraped_urls = set()  # Ensemble pour stocker les URL déjà scrapées
emails = set()  # Ensemble pour stocker les emails trouvées

count = 0  # Compteur pour limiter le nombre d'URLs scrapées
try:
    while len(urls):  # Tant qu'il y a des URLs dans la file d'attente
        count += 1  # Incrémente le compteur
        if count == 100:  # Si le compteur atteint 100, sort de la boucle
            break
        url = urls.popleft()  # Retire l'URL de tête de la file d'attente
        scraped_urls.add(url)  # Ajoute l'URL à l'ensemble des URL déjà scrapées

        # Analyse l'URL pour extraire le nom de domaine et le chemin
        parts = urllib.parse.urlsplit(url)
        base_url = '{0.scheme}://{0.netloc}'.format(parts)  # URL de base
        path = url[:url.rfind('/')+1] if '/' in parts.path else url  # Chemin de l'URL

        print('[%d] Traitement de %s' % (count, url))  # Affiche l'URL en cours de traitement
        try:
            response = requests.get(url)  # Tente de récupérer le contenu de l'URL
        except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
            continue  # Si une erreur de connexion ou de schéma manquant, passe à la prochaine itération

        # Trouve les nouveaux emails dans le contenu de la page
        new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text, re.I))
        emails.update(new_emails)  # Ajoute les nouveaux emails à l'ensemble des emails trouvées

        # Analyse le contenu HTML de la page pour trouver de nouveaux liens
        soup = BeautifulSoup(response.text, features="lxml")
        for anchor in soup.find_all("a"):  # Pour chaque lien trouvé
            link = anchor.attrs['href'] if 'href' in anchor.attrs else ''
            if link.startswith('/'):
                link = base_url + link  # Convertit le lien relatif en lien absolu
            elif not link.startswith('http'):
                link = path + link  # Convertit le lien relatif en lien absolu
            if not link in urls and not link in scraped_urls:  # Si le lien n'est pas déjà dans la file d'attente ou l'ensemble des URL scrapées
                urls.append(link)  # Ajoute le lien à la file d'attente
except KeyboardInterrupt:
    print('[-] Fermeture!')  # Si l'utilisateur interrompt le programme, affiche un message

for mail in emails:  # Pour chaque email trouvée
    print(mail)  # Affiche l'email
