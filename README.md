# ckanext-partialview

CKAN extension to enable preview for long `txt` and `csv` files.

In txt/csv previews this extensions limits the number of
lines displayed for text files in a CKAN repository. 

This is especially useful for large files such as CSV tables.

By showing only the first few lines, it keeps the
interface clean while still providing a clear overview of
the file's content.

This CKAN Extension enables resource previews 
for large `txt` and `csv` files.

Tested on CKAN 2.10 and 2.11

## Installation

### Source Installation

Extract the ZIP file containing ckanext-partialview e.g.:

    unzip ckanext-partialview.zip -d /usr/lib/ckan/default/src

Activate your CKAN virtual environment:

    . /usr/lib/ckan/default/bin/activate

Install extension inside the virtual environment:

    cd ckanext-partialview
    pip install .

Make sure to add pages to ckan.plugins in your config file, located
in `/etc/ckan/default/ckan.ini` by default:

    ckan.plugins = ... textpreview csvpreview ...

Restart CKAN:

    supervisorctl restart ckan-uwsgi:  


### Installation using Docker

Download and extract the ZIP file containing ckanext-partialview 
in `./ckan-extensions` e.g.:

    unzip ckanext-partialview.zip

Copy and install via `Dockerfile`:

    COPY ckan-extensions/ $SRC_DIR
    RUN cd $SRC_DIR/ckanext-partialview && \
        python3 setup.py develop

Add the plugins to `CKAN__PLUGINS` in your .env file:

    CKAN__PLUGINS = textpreview csvpreview

Restart CKAN container:

    docker restart ckan

## Configuration

This extension includes two new resource views to your CKAN instance.  

**textpreview**: Supported for file formats such as `text/plain`, `txt`, `plain`, `xml`, `rdf`, `rdf+xml`, `owl+xml`, `atom`, `rss`, `json` and `csv`.  

**csvpreview**: Specifically for  `csv` files. 

Select the resource view in resource setting user interface.

The number of lines displayed is adjustable in the user 
interface. By default, the first 20 lines are shown.
This value may be configured using:

    ckanext.partialview_max_rows = 20

If the setting is omitted, it defaults to 20.

## License

Released under the GNU Affero General Public License v3.0 or later. 

See the file LICENSE for details.

## Author

(C) 2025, Ondics GmbH on behalf of FLI Friedrich-Loeffler-Institut, Bundesforschungsinstitut für Tiergesundheit 
