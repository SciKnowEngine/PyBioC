import os
from bioc import BioCJsonReader
from bioc import BioCReader

def load_bioc_from_path(inPath):
    c = None
    if os.path.isdir(inPath):
        jsonReader = BioCJsonReader(inPath)
        c = jsonReader.collection
    else:
        reader = BioCReader(inPath)
        reader.read()
        c = reader.collection
    return c