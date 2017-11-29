__all__ = ['BioCReader']

import os
import json
from tqdm import tqdm

from lxml import etree
from bioc.bioc_annotation import BioCAnnotation
from bioc.bioc_collection import BioCCollection
from bioc.bioc_document import BioCDocument
from bioc.bioc_location import BioCLocation
from bioc.bioc_passage import BioCPassage
from bioc.bioc_sentence import BioCSentence
from bioc.bioc_node import BioCNode
from bioc.bioc_relation import BioCRelation

class BioCJsonReader:

    """
    This class can be used to load BioC JSON files in PyBioC objects,
    for further manipulation.
    """

    def __init__(self, source):

        """
        source:             File path to a BioC Json input directory.
                            optional argument ensures DTD validation.
        """

        if os.path.isdir(source) is False:
            raise ValueError('This class can only read a directory containing JSON-formatted document files.')

        self.source = source
        self.collection = BioCCollection()
        self._read_collection()

    def _read_collection(self):
        documents = []
        for fn in tqdm(os.listdir(self.source)):
            infile = self.source + "/" + fn
            if (os.path.isfile(infile) and fn.endswith('.json')):
                with open(infile) as json_data:
                    d = json.load(json_data)
                if d is not None:
                    document = BioCDocument()
                    document.id = d['id']
                    document.infons = d['infons']
                    document.passages = self._read_passages(d['passages'])
                    document.relations = self._read_relations(d['relations'])
                    documents.append(document)
                self.collection.documents = documents

    def _read_passages(self, p_list):
        if p_list is None:
            return []
        passages = []
        for p in p_list:
            passage = BioCPassage()
            passage.infons = p['infons']

            if p.get('offset', None) is not None:
                passage.offset = p['offset']
            else:
                passage.offset = '0'

            passage.sentences = self._read_sentences(p.get('sentences'))
            if p.get('text', None) is not None:
                passage.text = p.get('text')

            if p.get('annotations', None) is not None:
                passage.annotations = self._read_annotations(p.get('annotations'))

            if p.get('relations', None) is not None:
                self._read_relations(p.get('relations'))
            passages.append(passage)

        return passages

    def _read_sentences(self, s_list):
        if s_list is None:
            return []
        sentences = []
        for s in s_list:
            sentence = BioCSentence()
            sentence.infon = s['infon']
            sentence.offset = s['offset']
            sentence.text = s['text']
            sentence.annotations = self._read_annotations(s.get('annotations', None))
            sentence.relations = self._read_relations(s.get('relations'))
            sentences.append(sentence)
        return sentences

    def _read_annotations(self, a_list):
        if a_list is None:
            return []
        annotations = []
        for a in a_list:
            annotation = BioCAnnotation()
            annotation.id = a.get('id', None)
            annotation.infons = a.get('infons', None)
            annotation.locations = self._read_locations(a.get('locations', None))
            annotation.text = a.get('text', None)
            annotations.append(annotation)
        return annotations

    def _read_locations(self, l_list):
        if l_list is None:
            return []
        locations = []
        for l in l_list:
            location = BioCLocation()
            location.offset = l.get('offset')
            location.length = l.get('length')
            locations.append(location)
        return locations

    def _read_relations(self, r_list):
        if r_list is None:
            return []
        relations = []
        for r in r_list:
            relation = BioCRelation()
            relation.id = r.get('id', None)
            relation.infons = r.get('infons', None)
            relation.nodes = self._read_nodes(r.get('nodes', None))
            relations.append(relation)
        return relations

    def _read_nodes(self, n_list):
        if n_list is None:
            return []
        nodes = []
        for n in n_list:
            node = BioCNode()
            node.refid = n.get('refid', None)
            node.infons = n.get('infons', None)
            node.role = n.get('role', None)
            nodes.append(node)
        return nodes