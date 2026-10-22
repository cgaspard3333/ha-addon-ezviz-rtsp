# Add-on Home Assistant : EZVIZ RTSP keeper

Certaines caméras EZVIZ (constaté sur une **C3X**, firmware V5.2.5) désactivent leur
service RTSP après une coupure de courant : il faut alors aller dans l'appli EZVIZ,
« Vue directe via LAN », pour le réactiver.

Cet add-on vérifie régulièrement que le port RTSP de la caméra répond et, sinon,
réactive le RTSP par le port de commande local de la caméra (8000), comme le fait l'appli.
Il utilise la bibliothèque [pyEzvizApi](https://github.com/RenierM26/pyEzvizApi).

## Installation

[![Ajouter le dépôt à Home Assistant](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Fcgaspard3333%2Fha-addon-ezviz-rtsp)

Ou à la main : **Paramètres → Modules complémentaires → Boutique → ⋮ → Dépôts**, puis ajouter
`https://github.com/cgaspard3333/ha-addon-ezviz-rtsp`.

Installer ensuite **EZVIZ RTSP keeper**, renseigner la configuration et démarrer.

## Configuration

| Option | Description |
|---|---|
| `host` | Adresse IP locale de la caméra |
| `serial` | Numéro de série de la caméra (étiquette ou appli EZVIZ) |
| `verification_code` | Code de vérification à 6 lettres (étiquette de la caméra) |
| `check_interval` | Intervalle de vérification en secondes (30 à 3600, 120 par défaut) |

Le journal de l'add-on indique chaque perte et chaque réactivation du RTSP.
