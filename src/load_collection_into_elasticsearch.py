from elasticsearch import Elasticsearch, helpers
import argparse

import gzip
import numpy
import os
import codecs
import argparse
import json
import string
import re
import time
import sys

from bioc import BioCJsonReader
from bioc import BioCReader
from tqdm import tqdm

class ElasticLoader(object):

    def __init__(self, biocc, indexName):

        self.es = Elasticsearch()

        index_exists = self.es.indices.exists(index=[indexName], ignore=404)
        if( index_exists is False) :
            self.es.indices.create(index=indexName, ignore=400)

        # NOTE the (...) round brackets. This is for a generator.
        gen = ({
            "_index": indexName,
            "_type": "documents",
            "_id": i,
            "_source": es_d,
        } for i, es_d in self.unpack_bioccollection_for_es(biocc))
        helpers.bulk(self.es, gen)

    def unpack_bioccollection_for_es(self, biocc):
        for i, d in tqdm(enumerate(biocc.documents)):
            d = json.dumps(d)
            # Return the row on each iteration
            yield i, d  # <- Note the usage of 'yield'

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--inPath', help='Path to input data structure (XML file, JSON dir, zip archive')
    parser.add_argument('-e', '--esIndex', help='Name of ES archive to build')
    args = parser.parse_args()

    c = None
    if os.path.isdir(args.inPath):
        jsonReader = BioCJsonReader(args.inPath)
        c = jsonReader.collection
    else:
        reader = BioCReader(args.inPath)
        reader.read()
        c = reader.collection

    esLoader = ElasticLoader(c, args.esIndex)

    print("load complete into index " + args.esIndex)
