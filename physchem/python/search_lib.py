import os
import glob
import copy

from file_lib import AmiPath, PROJ
from text_lib import ProjectCorpus, Document, TerminalPage, Sentence, TextUtil
from xml.etree import ElementTree as ET
from collections import Counter

HOME = os.path.expanduser("~")
PYDIAG = "../../python/diagrams"
LIION = "../liion"
DICT_DIR = os.path.join(HOME, "dictionary")
OV21_DIR = os.path.join(DICT_DIR, "openVirus20210120")
CEV_DIR = os.path.join(DICT_DIR, "cevopen")
OIL186 = os.path.join(HOME, "projects/CEVOpen/searches/oil186")


class AmiSearch():

    def __init__(self):
        self.dictionaries = []
        self.word_counter = None

    def add_search_dictionary(self, dictionary):
        """adds a SearchDictionary
        """
        if dictionary is None or type(dictionary) != SearchDictionary:
            raise Exception("Search requires a SearchDictionary")
        self.dictionaries.append(dictionary)


    def search(self, file):
        matches_by_amidict = {}
        words = TextUtil.get_words_in_file(file)

        for dictionary in self.dictionaries:
            matches_by_amidict[dictionary.name] = dictionary.match(words)

        return matches_by_amidict



class SimpleDict():

    def __init__(self, file=None):
        if file:
            with open(file, "r") as f:
                self.lines = f.read().splitlines()
        print (self.lines)


def main():
    print("started search")
    test()
    print("finished search")

class SearchDictionary():
    """wrapper for an ami dictionary including search flags

    """
    def __init__(self, file):
        if not os.path.exists(file):
            raise IOError("cannot find file " + str(file))
        self.read_file(file)

    def read_file(self, file):
        self.file = file
        self.amidict = ET.parse(file)
        self.root = self.amidict.getroot()
        self.name = self.root.attrib["title"]
        self.entries = list(self.root.findall("entry"))
        print("read dictionary", self.name, "with", len(self.entries), "entries")

    def match(self, target_words):
        matched = []
        for target_word in target_words:
            for entry in self.entries:
                if "term" in entry.attrib:
                    term = entry.attrib["term"]
                    if term.lower() == target_word.lower():
#                        print(self.name, term, "matched")
                        matched.append(term)
        return matched


def test():
    ami_search = AmiSearch()
    search_dictionary = SearchDictionary(os.path.join(OV21_DIR, "country/country.xml"))
    ami_search.add_search_dictionary(search_dictionary)
    section_type = "method"
#    sections = AmiPath.create(section_type, {PROJ: LIION})
    sections = AmiPath.create(section_type, {PROJ: OIL186})
    target_files = sections.get_globbed_files()
    print("found", len(target_files), section_type, "sections")
    counter = Counter()
    for target_file in target_files:
        matches_by_amidict = ami_search.search(target_file)
        for amidict in matches_by_amidict:
            matches = matches_by_amidict[amidict]
            if len(matches) > 0:
                for match in matches:
                    counter[match] += 1
    print("counter", counter)

if __name__ == "__main__":
    print("running search main")
    main()
else:
#    print("running search main anyway")
#    main()
    pass

"""
https://gist.github.com/benhoyt/dfafeab26d7c02a52ed17b6229f0cb52
"""