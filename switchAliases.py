
# This script reads a "current index number" from file 
#setting the alias "es_alias" to point to the newly created index, removing the old pointer, and deleting the old index.
import elasticsearch
import logging
import os
import json
import sys
import ConfigParser

#es_server = 'http://192.168.125.116:9200/'
#es_server = 'http://localhost:9200/'
#es_server = 'http://80.91.34.90:9200/'
config = ConfigParser.RawConfigParser()
config.read('config.cfg')
es_server = config.get('Elasticsearch','server')
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s', filename='reindx.log')
logger = logging.getLogger('newAlias')
if es_server == '':
	print "Please supply servername"
	logger.error('No Elasticsearch server in config')
	exit()
file = open('nextIndexNumber.txt','r')
nextNumber = file.read()
es_indexNumber = int(nextNumber)
if es_indexNumber == '':
	print "cannot procedd without indexnumber"
	logger.info("no new indexnumber given. aborting")
	exit()
def main():
    from os import listdir
    from os.path import isfile, join
    es = elasticsearch.Elasticsearch(es_server)
    es_alias = config.get('Elasticsearch','alias')
    es_index = "{}_{}".format(es_alias, es_indexNumber)
    oldIndex = int(es_indexNumber) - 1
    es_old_index = "{}_{}".format(es_alias, oldIndex)
    logger.info("will remove old index {} and set new index {} for alias {}".format(es_old_index, es_index, es_alias))
    actions = {'actions': [{'remove': {'index': es_old_index, 'alias':es_alias} }, {'add': {'index': es_index, 'alias':es_alias}}]}
    
    es.indices.update_aliases(body=json.dumps(actions))
    es.indices.delete(es_old_index)
if __name__ == '__main__':
    main()
