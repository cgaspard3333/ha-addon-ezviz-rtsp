# EZVIZ RTSP keeper

Certaines caméras EZVIZ (constaté sur une C3X, firmware V5.2.5) désactivent leur
service RTSP après une coupure de courant. Il faut alors le réactiver dans l'appli
EZVIZ (« Vue directe via LAN »).

Cet add-on vérifie régulièrement que le port RTSP répond et, sinon, réactive le
RTSP par le port de commande local de la caméra (8000), comme le fait l'appli.

## Options

- `host` : adresse IP locale de la caméra.
- `serial` : numéro de série de la caméra.
- `verification_code` : code de vérification à 6 lettres (étiquette de la caméra).
- `check_interval` : intervalle de vérification en secondes (30 à 3600).

Le journal de l'add-on indique chaque perte et chaque réactivation du RTSP.
