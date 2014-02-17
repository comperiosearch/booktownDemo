## Index Alias SCRIPT  
# This is part of a set of three scripts that enable reindexing content into river-jdbc
# This script creates a new index for the river-jdbc to index into 
# Indexes are referenced by an alias, and the alias is pointing to 
 # The new index number is stored in file "nextIndexNumber.txt"
# Another script runs after elasticsearch is restarted, setting the alias "es_alias" to point to the newly created index, 
# removing the old pointer, and deleting the old index.
import elasticsearch
import logging
import os
import json
import sys
import re
import ConfigParser
config = ConfigParser.RawConfigParser()
config.read('config.cfg')
es_server = config.get('Elasticsearch','server')
if es_server == '':
  print "Please supply servername"
  sys.exit(2)
print es_server
es = elasticsearch.Elasticsearch(es_server)

es_alias = config.get('Elasticsearch','alias')
es_index = "{}_{}".format(es_alias,"2")
es_old_index = "{}_{}".format(es_alias,"1")

from elasticsearch.transport import Transport
def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s', filename='reindx.log')
    from os import listdir
    from os.path import isfile, join
    logger = logging.getLogger('newAlias')
    existingAlias = es.cat.aliases(es_alias)   
    if existingAlias == '':
        logger.error("no Existing alias found")
        sys.exit(2)
    aliasMatch = re.search(r"(\d+)", existingAlias)
    if aliasMatch == None:
        logger.error("no matching index definition found for alias {}".format(existingAlias) )
        sys.exit(2)
    es_old_index =  existingAlias.split()[1]
    logger.info("found old index {}".format(es_old_index))
    groupResult = aliasMatch.groups()
    aliasNumber = int(groupResult[0])
    aliasNumber += 1
    es_index =  "{}_{}".format(es_alias, aliasNumber)
    logger.info("will create new index {}".format(es_index))
    es.indices.create(es_index)
    river = json.loads(open("river.json", "r").read())
    logger.info("got the old river from river-jdbc {}".format(river['jdbc']['index'])
    river['jdbc']['index'] = es_index
    print river
    es.transport.perform_request('PUT', '/_river/' + es_alias + '/_meta', body=river)
    # Write out the number of the index index. 
    with open('nextIndexNumber.txt', 'wb') as fh:
        fh.write(str(aliasNumber)+'\n')
if __name__ == '__main__':
    main()
