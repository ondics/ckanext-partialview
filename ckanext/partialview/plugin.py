# encoding: utf-8
from __future__ import annotations

from ckan.types import Context, ValidatorFactory
import logging
from typing import Any, cast

from ckan.common import CKANConfig, json
import ckan.plugins as p
import ckanext.resourceproxy.plugin as proxy
import ckan.lib.datapreview as datapreview

import requests
from itertools import islice
import ckan.plugins.toolkit as toolkit

import ckan.lib.navl.dictization_functions as df

import pandas

import ckan.logic as logic
import ckan.lib.uploader as uploader

default = cast(ValidatorFactory, toolkit.get_validator(u'default'))

natural_number_validator = toolkit.get_validator(u'natural_number_validator')

Invalid = df.Invalid

log = logging.getLogger(__name__)

def is_natural_number(n):
    try:
        return isinstance(n, int) and n > 0
    except ValueError:
        raise Invalid(_('Please enter a Natural Number, n>=0'))

def read_text(resource_id, max_rows):
    log.debug("################################################")
    log.debug(resource_id)
    log.debug(max_rows)
    try:
        rsc = logic.get_action(u'resource_show')(data_dict={u'id': resource_id})
    except logic.NotFound as e:
        # Fehler ins Log schreiben und leere Liste zurückgeben
        log.debug(f"Not authorized to download resource: {e}")
        return []

    if rsc.get(u'url_type') == u'upload':
        upload = uploader.get_resource_uploader(rsc)
        filepath = upload.get_path(rsc[u'id'])
        with open(filepath, 'r', encoding='utf-8') as file:
            return [line.strip() for line in islice(file, max_rows)]
    
    elif not rsc.get(u'url_type'):
        log.debug("################################################")
        log.debug( "URL Link")
        # return ""
        try:
            response = requests.get(rsc.get(u'url'), stream=True, timeout=10)  # Timeout setzen
            response.raise_for_status()  # HTTP-Fehler abfangen (z. B. 404, 500)
        except requests.exceptions.RequestException as e:
            # Fehler ins Log schreiben und leere Liste zurückgeben
            log.debug(f"########################################################")
            log.debug(f"Cannot access resource at {rsc.get(u'url')}: {e}")
            return f"Cannot access resource at {rsc.get(u'url')}: {e}"

        zeilen = []
        try:
            for line in islice(response.iter_lines(decode_unicode=True), max_rows):  # Nur 20 Zeilen
                zeilen.append(line.strip())
        except Exception as e:
            log.debug(f"########################################################")
            log.debug(f"Fehler beim Verarbeiten der Datei: {e}")
            return []
        return zeilen

    elif u'url' not in rsc:
        log.debug( "No download is available")
        return []

    return []


def read_csv(resource_id, max_rows):

    log.debug("################################################")
    log.debug(resource_id)
    log.debug(max_rows)
    try:
        rsc = logic.get_action(u'resource_show')(data_dict={u'id': resource_id})
    except logic.NotFound as e:
        # Fehler ins Log schreiben und leere Liste zurückgeben
        log.debug(f"Not authorized to download resource: {e}")
        return ""

    if rsc.get(u'url_type') == u'upload':
        upload = uploader.get_resource_uploader(rsc)
        filepath = upload.get_path(rsc[u'id'])
        data = pandas.read_csv(filepath, nrows=max_rows)
        return data.to_html()

    elif not rsc.get(u'url_type'):
        log.debug("################################################")
        log.debug( "URL Link")
        # return ""
        data = pandas.read_csv(rsc.get(u'url'), nrows=max_rows)
        return data.to_html()

    elif u'url' not in rsc:
        log.debug("No download URL available")
        return "No download URL available"

    return ""


class PartialViewPlugin(p.SingletonPlugin):
    '''This extension previews JSON(P).'''

    p.implements(p.IConfigurer, inherit=True)
    p.implements(p.IResourceView, inherit=True)
    p.implements(p.ITemplateHelpers, inherit=True)
    p.implements(p.IValidators, inherit=True)

    def update_config(self, config: CKANConfig):
        p.toolkit.add_public_directory(config, 'public')
        p.toolkit.add_template_directory(config, 'templates')
        p.toolkit.add_resource('assets', 'ckanext-partialview')
    
    def get_validators(self):
        return {
            'partialview_is_natural_number': is_natural_number
        }
    
    def get_helpers(self):
        return {
            'partialview_read_text': read_text,
            'partialview_read_csv': read_csv
        }

class TextPreviewPlugin(PartialViewPlugin):
    '''This extension previews JSON(P).'''

    allowed_file_formats = ['text/plain', 'txt', 'plain', 'xml', 'rdf', 'rdf+xml', 'owl+xml', 'atom', 'rss', 'json', 'csv']
    max_rows = 20

    def info(self):
        return {
            'name': 'text_preview',
            'title': p.toolkit._('Text Preview'),
            'icon': 'file-lines',
            'default_title': p.toolkit._('Text Preview'),
            'iframed': True,
            'schema': {
                'max_rows': [default(self.max_rows), natural_number_validator]
            }
        }

    def can_view(self, data_dict: dict[str, Any]):
        resource = data_dict['resource']
        format_lower = resource.get('format', '').lower()
        if format_lower in self.allowed_file_formats:
            return True
        return False

    def setup_template_variables(self, context: Context,
                                 data_dict: dict[str, Any]):

        log.debug("################################################ data_dict: ")
        log.debug(data_dict)
        log.debug("################################################ context: ")
        log.debug(context)

        resource_id = data_dict['resource']['id']
        max_rows = 20
        if data_dict['resource_view'].get('max_rows'):
            max_rows = data_dict['resource_view']['max_rows']

        return {
            'resource_id': resource_id,
            'max_rows': max_rows
        }

    def view_template(self, context: Context, data_dict: dict[str, Any]):
        return 'textpreview_view.html'

    def form_template(self, context: Context, data_dict: dict[str, Any]):
        return 'textpreview_form.html'


class CsvPreviewPlugin(PartialViewPlugin):
    '''This extension previews JSON(P).'''

    allowed_file_formats = ['csv']
    max_rows = 20

    def info(self):
        return {
            'name': 'csv_preview',
            'title': p.toolkit._('CSV Preview'),
            'icon': 'file-lines',
            'default_title': p.toolkit._('CSV Preview'),
            'iframed': True,
            'schema': {
                'max_rows': [default(self.max_rows), natural_number_validator]
            }
        }

    def can_view(self, data_dict: dict[str, Any]):
        resource = data_dict['resource']
        format_lower = resource.get('format', '').lower()
        if format_lower in self.allowed_file_formats:
            return True
        return False

    def setup_template_variables(self, context: Context,
                                 data_dict: dict[str, Any]):

        resource_id = data_dict['resource']['id']
        max_rows = 20
        if data_dict['resource_view'].get('max_rows'):
            max_rows = data_dict['resource_view']['max_rows']

        return {
            'resource_id': resource_id,
            'max_rows': max_rows
        }

    def view_template(self, context: Context, data_dict: dict[str, Any]):
        return 'csvpreview_view.html'

    def form_template(self, context: Context, data_dict: dict[str, Any]):
        return 'csvpreview_form.html'