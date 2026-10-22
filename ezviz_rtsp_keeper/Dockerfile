ARG BUILD_FROM
FROM $BUILD_FROM

# Seul le client LAN de pyezvizapi est utilisé : il n'a besoin que de pycryptodome.
# pyezvizapi n'a pas encore publié l'écriture de servicesSwitch sur PyPI (1.0.5.0) :
# version figée sur le commit testé avec la C3X le 23/10/2026.
RUN pip install --no-cache-dir pycryptodome \
 && pip install --no-cache-dir --no-deps \
    "pyezvizapi @ https://github.com/RenierM26/pyEzvizApi/archive/605e5bad78b073984cf466b9f2ca6d9e5beb7ba8.tar.gz" \
 && find /usr/local/lib -name '__pycache__' -prune -exec rm -rf {} +

COPY run.py /run.py
CMD ["python3", "-u", "/run.py"]
