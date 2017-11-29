from __future__ import print_function, division
import argparse
import os
import json
from json import JSONEncoder


from bioc import BioCReader
from bioc import BioCJsonReader
from bioc import BioCWriter
from bioc import BioCCollection
from bioc import bioc_utils as utils
from datetime import datetime
from tqdm import tqdm

class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-i1', '--in1', help='Directory for input files 1')
    parser.add_argument('-i2', '--in2', help='Directory for input files 2')
    parser.add_argument('-o', '--outFile', help='output file for BioCCollection')
    parser.add_argument('-s', '--sourceDescription', help='Source Description')
    args = parser.parse_args()

    print("\nLoading " + args.in1)
    c1 = utils.load_bioc_from_path(args.in1)
    c1.source = args.sourceDescription
    c1.date = datetime.now().isoformat()

    print("\nLoading " + args.in2)
    c2 = utils.load_bioc_from_path(args.in2)

    lookup = {}
    for d in c2.documents:
        lookup[d.id] = d

    for d1 in tqdm(c1.documents):
        if lookup.get(d1.id, None) is not None:
            d2 = lookup.get(d1.id)
            if(len(d1.passages) != 1 or len(d2.passages) != 1):
                continue
            p1 = d1.passages[0]
            p2 = d2.passages[0]
            if p1.text == p2.text:
                a_list = p2.annotations
                p2.annotations = None
                p1.annotations.extend(a_list)
            else:
                print('Text from the main passages for document ' + d1.id + ' does not match!')

        else:
            pause = 0

    c1.source = args.sourceDescription
    if args.outFile[-4:] == '.xml':
        writer = BioCWriter(collection=c1)
        writer.write(args.outFile)
    else:
        if os.path.exists(args.outFile) is False:
            os.mkdir(args.outFile)
        for d in c1.documents:
            f = open(args.outFile + '/' + d.id + '.json', 'w')
            f.write(json.dumps(d, cls=MyEncoder, indent=4))
            f.close()
        c1.documents = None
        f = open(args.outFile + '/collection.json', 'w')
        f.write(json.dumps(c1, cls=MyEncoder, indent=4))
        f.close()

