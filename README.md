# ckanext-partialview

## Voraussetzungen
Extension installiert für CKAN 2.10.5 und Python 3

## Installation

### Docker Installation

ZIP Datei, die die Partialview Extension enthält, extrahieren, z.B.:

    unzip ckanext-partialview.zip

Über Dockerfile Verzeichnis mit den Extensions in Container kopieren und installieren:

    COPY ckan-extensions/ $SRC_DIR
    RUN cd $SRC_DIR/ckanext-partialview && \
        python3 setup.py develop

Theme der Plugin Liste in der .env Datei hinzufügen:

    CKAN__PLUGINS = "... textpreview csvpreview ..."

CKAN Container neustarten:

    docker restart ckan

### Source Installation

ZIP Datei, die die Partialview Extension enthält, extrahieren, z.B.:

    unzip ckanext-partialview.zip -d /usr/lib/ckan/default/src

Aktivieren der CKAN virtuellen Umgebung:

    . /usr/lib/ckan/default/bin/activate

Installieren der Extension in die virtuelle Umgebung:

    cd ckanext-partialview
    pip install .

Theme der Plugin Liste in der CKAN config Datei hinzufügen,  
meist zu finden in `/etc/ckan/default/ckan.ini`.  
Dort dann der Variable `ckan.plugins` hinzufügen:

    ckan.plugins = ... textpreview csvpreview ...

CKAN neustarten:

    # Bei Installation im Host z.B.:
    supervisorctl restart ckan-uwsgi:
    

## Autor und Lizenz

keine Open Source, alle Rechte vorbehalten

(C) 2025, Ondics GmbH