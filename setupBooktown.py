## SETUP SCRIPT FOR Booktown ELASTICSEARCH 
import elasticsearch
import logging
import os
import json
import sys
import ConfigParser

config = ConfigParser.RawConfigParser()
config.read('config.cfg')
es_server = config.get('Elasticsearch','server')
if es_server == '':
    print "Please tell me the hostname of your elasticsearch server"
    sys.exit(2)
es = elasticsearch.Elasticsearch(es_server)
es_alias = config.get('Elasticsearch','alias')
es_index = "{}_{}".format(es_alias,"1")

from elasticsearch.transport import Transport
def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s', filename='reindx.log')
    from os import listdir
    from os.path import isfile, join
    if es.indices.exists(ex_index) == True:
        es.indices.delete(es_index)
    es.indices.create(es_index)
    mapping = json.loads(open("index-template.json", "r").read())
    es.indices.put_template(body=mapping,name=es_alias + 'template')
    es.indices.put_alias(index=es_index,name=es_alias)
    from elasticsearch.transport import Transport
    river = json.loads(open("river.json", "r").read())
    es.transport.perform_request('PUT', '/_river/' + es_alias + '/_meta', body=river  )
    
if __name__ == '__main__':
    main()
