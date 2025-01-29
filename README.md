# ckanext-partialview

## Getting started

This extension adds two new resource views to your CKAN instance.  
1. **textpreview**  
A view for `text/plain`, `txt`, `plain`, `xml`, `rdf`, `rdf+xml`, `owl+xml`, `atom`, `rss`, `json` and `csv` files.  
2. **csvpreview**  
A view for `csv` files.   

They can be added to your CKAN resources like any other view plugin.  
In contrast to other view plugins though, these only show the first few lines of your resource file,  
therefore allowing for a new preview style, especially useful for handling big files.

During the creation or editing of one of the new views, you can set a value for the number of lines displayed in your resource view.  
If added via `ckan.views.default_views` or without declaring a value, it will default to 20 lines.

## Dependencies
The extension ckanext-partialview was installed and tested in CKAN 2.10 and Python 3.

## Installation

### Docker Installation

Extract the ZIP file containing ckanext-partialview e.g.:

    unzip ckanext-partialview.zip

Copy and Install via Dockerfile:

    COPY ckan-extensions/ $SRC_DIR
    RUN cd $SRC_DIR/ckanext-partialview && \
        python3 setup.py develop

Add the following plugins from ckanext-partialview to `CKAN__PLUGINS` in the .env file:

    CKAN__PLUGINS = "... textpreview csvpreview ..."

Restart CKAN container:

    docker restart ckan

### Source Installation

Extract the ZIP file containing ckanext-partialview e.g.:

    unzip ckanext-partialview.zip -d /usr/lib/ckan/default/src

Activate the CKAN virtual environment:

    . /usr/lib/ckan/default/bin/activate

Install extension inside the virtual environment:

    cd ckanext-partialview
    pip install .

Add the following plugins from ckanext-partialview to the CKAN config file,  
usually located in `/etc/ckan/default/ckan.ini`.  
Add to `ckan.plugins`:

    ckan.plugins = ... textpreview csvpreview ...

Restart CKAN:

    # e.g.:
    supervisorctl restart ckan-uwsgi:  

## Configuration

The max number of rows possible to be displayed can be customized in your config file.  
If this variable is not set, the default value will be 20:  

    ckanext.partialview_max_rows = 20

## License

Released under the GNU Affero General Public License (AGPL) v3.0.

## Author

(C) 2025, Ondics GmbH