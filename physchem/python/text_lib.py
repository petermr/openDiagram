
import numpy as np
import matplotlib.pyplot as plt
import nltk, unicodedata
import os
import glob
from file_lib import AmiPath, Globber
from collections import namedtuple

import xml.etree.ElementTree as ET
import re


NFKD = "NFKD"

"""tags
b i em strong 
table 
fig 

"""
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

LIION_PROJ = os.path.abspath(os.path.normpath(os.path.join("../liion")))

class ProjectCorpus():

    def __init__(self, cwd, tree_glob="./*/"):
        self.cwd = cwd
        self.tree_glob = tree_glob

    def read_analyze_child_documents(self):
#        self.files = self.glob_corpus_files()
        self.files = glob.glob(os.path.join(self.cwd, self.tree_glob))
        print("glob", self.cwd, self.tree_glob, str(len(self.files)), self.files)
        for file in self.files:
            document = Document(file) #level of tree
            document.create_analyze_sections()

    def glob_corpus_files(self, glob_path, recurse=True):
        ami_path = AmiPath();
        ami_path.recurse = recurse
        files = ami_path.get_globbed_files()
        return files

    @staticmethod
    def test():
        print("start test", LIION_PROJ)
        assert (os.path.exists(LIION_PROJ))
        project = ProjectCorpus(LIION_PROJ)
        project.read_analyze_child_documents()
        print("end test")

    def __str__(self):
        return " ".join(map(str, self.sentences))

class Document():
    """ a standalone hierarchical document
    level of Tree or below
    may contain a subset of the conventional document"""

    def __init__(self, file="f"):
        self.sections = None
        self.file = file

    def create_analyze_sections(self):
        sections_file = os.path.abspath(os.path.join(self.file, "sections"))
        if not os.path.exists(sections_file):
            print("PLEASE CREATE sections with ami sections, will add pyami later")
            return
        terminal_files = glob.glob(os.path.join(sections_file, "**/*.xml"))
        for terminal_file in terminal_files:
            terminal_page = TerminalPage(terminal_file)
            terminal_page.analyze_file_contents()



class TerminalPage():
    """the xml sub-document with text
    Currently either <title> or <p>

    Will often get annotated with sentence markers
    """
    def __init__(self, file):
        self.file = file


    def analyze_file_contents(self):
        """read a file as an ami-section of larger document """
        with open(self.file, "r") as f:
            self.text = f.read()
        # assumes this has been chunked to sections
        print("t", len(self.text), self.text[:50])
        self.read_para()

    def read_para(self):
        self.text = TextUtil.remove_para_tags(self.text)
        self.text = unicodedata.normalize(NFKD, self.text)
        self.text = TextUtil.flatten_non_ascii(self.text)
        self.text = TextUtil.join_xml_texts(self.text)
        self.sentences = [Sentence(s) for s in (nltk.sent_tokenize(self.text))]
#        self.sentences = Sentence.merge_false_sentence_breaks(self.sentences)
        for sentence in self.sentences:
            print(sentence)
        print(len(self.sentences), list(self.sentences))
        ft = self.file[:-4] + ".txt"
        print(ft)
        with open(ft, "w") as f:
            i = 0
            for i, sentence in enumerate(self.sentences):
                print(type(sentence))
                f.write(str(i) + ": " + sentence.string+"\n")
                i += 1


class Sentence():

    def __init__(self, string):
        self.string = string
        self.words = nltk.word_tokenize(string)
        self.words = Sentence.remove_punct(self.words)

    @staticmethod
    def merge_false_sentence_breaks(sentences):
        sent0 = []
        for i, sent in enumerate(sentences):
            pass
#        its = [iter(arr), iter(arr[1:]), iter(arr[2:])]  # Construct the pattern for longer windowss
#        its = [iter(arr), iter(arr[1:])]  # Construct the pattern for longer windowss
#        its = zip(*its)
#        print ("its", its)
#        return its



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

class TextUtil():

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
        """remove certain tags within paras lexically.
        Works on flat text

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
    ProjectCorpus.test()
    print("finished text_lib")

if __name__ == "__main__":
    main()
else:
#    main()
    pass