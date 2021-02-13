
import numpy as np
import matplotlib.pyplot as plt
import nltk, unicodedata
import os
from file_lib import FileLib, Globber
from collections import namedtuple

import xml.etree.ElementTree as ET
import re


NFKD = "NFKD"


TAGS = {
    "\n": "",
    "</sup>": "",
    "</sub>": "",
    "</xref>": "",
}

TAG_REGEXES = {
    " +<": "<",
    "<xref[^>]*>": "@",
    " *<sup>": "^",
    " *<sub>": "_",
}

PUNCT = "!@#$%^&*+{}[]:;'|<>,.?/~`\"\\"


class Sentence():

    def __init__(self, string):
        self.string = string
        self.words = nltk.word_tokenize(string)
        self.words = Sentence.remove_punct(self.words)

    @staticmethod
    def remove_punct(tokens):
        """removes tokens consisting of punctuation in present `PUNCT`

        tokens: list of words
        returns: words diminished by deleted punctuation

        """
        tokens = [token for token in tokens if not token in PUNCT]
        return tokens

    def __str__(self):
        return " ".join(map(str, self.words))

class ProjectCorpus():

    def __init__(self):
        self.text = None
        self.sentences = None

    def read_para(self):
        self.remove_para_tags(self.text)
        self.text = unicodedata.normalize(NFKD, self.text)
        self.text = self.flatten_non_ascii(self.text)
        self.text = self.join_xml_texts(self.text)
        self.sentences = [Sentence(s) for s in (nltk.sent_tokenize(self.text))]

    def read_analyze(self):
        self.files = self.glob_corpus_files()
        print("xml title glob", str(len(self.files)), self.files)
        for file in self.files:
            document = Document(file)
            self.analyze_file_contents(file)

    def glob_corpus_files(self, glob_path, recurse=True):
        flib = FileLib();
        flib.recurse = recurse
        files = flib.get_globbed_files()
        return files

    def __str__(self):
        return " ".join(map(str, self.sentences))

def FileSection():
    """content of files selected as 'sections' by ami-section or other tools

    May not always be labeled "section". Contains paragraphs.
    """

    def __init__(self):
        self.paras = None
        pass

    def analyze_file_contents(self, file):
        """read a file as an ami-section of larger document """
        self.file = file
        with open(file, "r") as f:
            self.text = f.read()
        # assumes this has been chunked to sections
        self.read_para()

    def __str__(self):
        """
        joins string representation of paras by spaces
        """
        return " ".join(map(str, self.paras))


def Document():
    """ a standalone hierarchical document
    may contain a subset of the conventional document"""

    def __init__(self):
        self.sections = None


def TextUtil():

    @staticmethod
    def join_xml_texts(xml_string):
        """remove all tags in XML

        replace all tags by spaces. We may later wish to exclude some names tags (e.g. <sup>)
        xml_string: XML in serialized form
        return flattened string with spaces replacing tags
        """
        #remove tags
        untagged_text = str.join(" ", list(ET.fromstring(xml_string).itertext()))
        return untagged_text

    @staticmethod
    def remove_para_tags(text):
        """remove certain tags lexically.

        Messy. At present tags are in TAGS and TAG_REGEXES
        """
        for key in TAGS:
            text = text.replace(key, TAGS[key])
        for regex in TAG_REGEXES:
            text = re.sub(regex, TAG_REGEXES[regex], text)
        return text

    @staticmethod
    def flatten_non_ascii(text):
        """remove diacritics and other 'non-ascii' characters

        Messy.

        """
        text = text.encode("ascii", "ignore").decode("utf-8", "ignore")
        return text

    @staticmethod
    def remove_non_alphanumeric(text, remove_digits=False):
        """
        Remove nonalphanumeric characters

        remove_digits: remove digits 0-9
        """
        pattern = r'[^A-Za-z0-9\s]' if not remove_digits else r'[A-Za-z\s]'
        text = re.sub(pattern, '', text)
        return text


def main():
    print("started text_lib")
    c = ProjectCorpus()
    c.read_analyze()
    print("c", c)
    print("finished text_lib")

if __name__ == "__main__":
    main()
else:
    main()