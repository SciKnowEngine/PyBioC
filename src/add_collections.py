from __future__ import print_function, division
import argparse
import os

from bioc import BioCReader
from bioc import BioCWriter
from bioc import BioCCollection
from datetime import datetime
from tqdm import tqdm


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--inDir', help='Directory for input files')
    parser.add_argument('-o', '--outFile', help='output file for BioCCollection')
    parser.add_argument('-s', '--sourceDescription', help='Source Description')
    args = parser.parse_args()

    biocc = BioCCollection()
    biocc.source = args.sourceDescription
    biocc.date = datetime.now().isoformat()

    for fn in tqdm(os.listdir(args.inDir)):
        infile = args.inDir + "/" + fn
        if (os.path.isfile(infile) and fn.endswith('.xml')):
            id = fn.replace(".xml", "")

            reader = BioCReader(infile)
            reader.read()

            for biocd in reader.collection.documents:
                biocc.add_document(biocd)

    writer = BioCWriter(collection=biocc)
    writer.write(args.outFile)
