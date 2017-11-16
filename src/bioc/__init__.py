#
# Package for interoperability in BioCreative work
#

__version__ = '1.02'

__all__ = [
    'BioCAnnotation', 'BioCCollection', 'BioCDocument',
    'BioCLocation', 'BioCNode', 'BioCPassage', 'BioCRelation',
    'BioCSentence', 'BioCReader', 'BioCWriter'
    ]

__author__ = 'Hernani Marques (h2m@access.uzh.ch)'

from bioc.bioc_annotation import BioCAnnotation
from bioc.bioc_collection import BioCCollection
from bioc.bioc_document import BioCDocument
from bioc.bioc_location import BioCLocation
from bioc.bioc_node import BioCNode
from bioc.bioc_passage import BioCPassage
from bioc.bioc_relation import BioCRelation
from bioc.bioc_sentence import BioCSentence
from bioc.bioc_reader import BioCReader
from bioc.bioc_writer import BioCWriter
