"""Réactive le RTSP d'une caméra EZVIZ quand le port RTSP ne répond plus.

Toutes les `check_interval` secondes :
  - si le port RTSP (554) répond « RTSP/1.0 200 », rien à faire ;
  - sinon, si le port de commande local (8000) est ouvert, lit servicesSwitch
    et réécrit rtsp=1 en conservant les autres services.
"""

import json
import os
import socket
import sys
import time

from pyezvizapi.hcnetsdk import HcNetSdkLanEndpoint, HcNetSdkPurePythonClient

OPTIONS_FILE = os.environ.get("OPTIONS_FILE", "/data/options.json")
RTSP_PORT = 554
COMMAND_PORT = 8000


def log(msg: str) -> None:
    print(time.strftime("%Y-%m-%d %H:%M:%S"), msg, flush=True)


def rtsp_answers(host: str) -> bool:
    try:
        with socket.create_connection((host, RTSP_PORT), timeout=5) as s:
            s.sendall(f"OPTIONS rtsp://{host}:{RTSP_PORT}/ RTSP/1.0\r\nCSeq: 1\r\n\r\n".encode())
            return s.recv(64).startswith(b"RTSP/1.0 200")
    except OSError:
        return False


def port_open(host: str, port: int) -> bool:
    try:
        with socket.create_connection((host, port), timeout=5):
            return True
    except OSError:
        return False


def enable_rtsp(client: HcNetSdkPurePythonClient) -> None:
    state = client.services_switch_state()
    log(f"servicesSwitch actuel : {state.raw.get('servicesSwitch')}")
    if state.rtsp == 1:
        log("RTSP déjà activé dans la caméra, le port ne répond pas encore : on attend.")
        return
    result = client.services_switch_set(current_payload=state.raw, rtsp=1)
    log("Écriture rtsp=1 : " + ("ok" if result.succeeded else "réponse non-ok"))


def main() -> None:
    with open(OPTIONS_FILE, encoding="utf-8") as f:
        opts = json.load(f)
    host, code = opts["host"], opts["verification_code"]
    interval = int(opts.get("check_interval", 120))
    if not (host and opts.get("serial") and code):
        log("Renseigner host, serial et verification_code dans la configuration de l'add-on.")
        sys.exit(1)

    client = HcNetSdkPurePythonClient(
        HcNetSdkLanEndpoint(serial=opts["serial"], host=host, command_port=COMMAND_PORT, rtsp_port=RTSP_PORT),
        code,
        timeout=10,
    )
    log(f"Surveillance du RTSP de {host} toutes les {interval} s.")
    last_ok = None
    while True:
        ok = rtsp_answers(host)
        if ok != last_ok:
            log("RTSP OK." if ok else "RTSP ne répond pas.")
            last_ok = ok
        if not ok:
            if port_open(host, COMMAND_PORT):
                try:
                    enable_rtsp(client)
                except Exception as err:  # caméra en redémarrage, mauvais code, etc.
                    log(f"Échec de la réactivation : {err!r}")
                time.sleep(10)
                if rtsp_answers(host):
                    log("RTSP réactivé.")
                    last_ok = True
            else:
                log("Port de commande fermé (caméra éteinte ou service local coupé) : nouvel essai plus tard.")
        if os.environ.get("RUN_ONCE"):
            return
        time.sleep(interval)


if __name__ == "__main__":
    main()
