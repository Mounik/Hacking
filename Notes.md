# Hacking

## Reconnaissance :

### IP Checker
https://ipinfo.info/html/ip_checker.php

### Whois
whois

### WhatWeb
whatweb pour les sites internet (reco complète des techno du site)
whatweb -v nom_du_site > fichier de sortie

#### Pour scanner un réseau sans voir les erreurs
whatweb -v 192.168.0.0-192.168.0.255 --aggression 3 --no-errors

#### Pour scanner un réseau sans voir les erreurs et dans un fichiers de log
whatweb -v 192.168.0.131 --aggression 3 --log-verbose=scan.txt

### Email
peut servir a se connecter aux outils de la société

#### theHarvester
theHarvester -d mounik.hd.free.fr -b all
theHarvester -d mounik.hd.free.fr -b google

Si aucun résultats avec theHarvester
#### hunter.io

Sinon script Python pour trouver des emails

Pour trouver des outils il suffit de taper Information Gathering Tools Github dans la barre de recherche
#### Sherlock
sudo apt install sherlock

