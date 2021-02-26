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
PMR_DIR = os.path.join(DICT_DIR, "pmr")
OIL186 = os.path.join(HOME, "projects/CEVOpen/searches/oil186") #https://github.com/petermr/CEVOpen


class AmiSearch:

    def __init__(self):
        self.dictionaries = []
        self.word_counter = None

    def make_graph(self, dictionary):
        import matplotlib.pyplot as plt
        plt.bar(list(dictionary.keys()), dictionary.values(), color='g')
        plt.show()

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

    def search_with_dictionaries(self, dicts, globlets):
        for dikt in dicts:
            search_dictionary = SearchDictionary(dikt)
            self.add_search_dictionary(search_dictionary)
        for globlet in globlets:
            glob_files = globlet.get_globbed_files()
#            print("found", len(glob_files))
            self.search_and_count(glob_files)

    def search_and_count(self, section_files):
        counter = Counter()
        debug_cnt = 10000
        max_files = 10000
        for index, target_file in enumerate(section_files[:max_files]):

            if index % debug_cnt == 0:
                print("file", target_file)
            matches_by_amidict = self.search(target_file)
#            print("matches", matches_by_amidict)
            for amidict in matches_by_amidict:
#                print("dict>", amidict)
                matches = matches_by_amidict[amidict]
                if len(matches) > 0:
                    for match in matches:
                        counter[match] += 1
#        counter = self.sortxx(counter)
        print("counter", counter)
        self.make_graph(counter)

    def sortxx(self, counter):
        sorted_d = sorted((key, value) for (key, value) in counter.items())
        return sorted_d


class SimpleDict:

    def __init__(self, file=None):
        if file:
            with open(file, "r") as f:
                self.lines = f.read().splitlines()
        print(self.lines)


def main():
    print("started search")
    test()
    print("finished search")


class SearchDictionary:
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
        self.term_set = set()
        print("read dictionary", self.name, "with", len(self.entries), "entries")

    def get_or_create_term_set(self):
        if len(self.term_set) == 0:
            for entry in self.entries:
                if "term" in entry.attrib:
                    term = entry.attrib["term"]
                    if not " " in term:
                        term = term.lower()
                        self.term_set.add(term) # single word countries
#            print(len(self.term_set), list(sorted(self.term_set)))

        return self.term_set

    def match(self, target_words):
        matched = []
        self.get_or_create_term_set()
        for target_word in target_words:
            target_word = target_word.lower()
            if target_word in self.term_set:
                matched.append(target_word)
        return matched


def test_sect_dicts():
    ami_search = AmiSearch()
# dictionaries
    #    search_dictionary = SearchDictionary(os.path.join(OV21_DIR, "organization/organization.xml"))
    dicts = [
        os.path.join(OV21_DIR, "country", "country.xml"),
        os.path.join(CEV_DIR, "compound", "eo_compound.xml"),
#        os.path.join(OV21_DIR, "country", "country.xml"),
    ]
# section_types
    section_type = "acknowledge"
    sects_ack = AmiPath.create(section_type, {PROJ: OIL186})
    section_type = "affiliation"
    sects_aff = AmiPath.create(section_type, {PROJ: OIL186})
    section_type = "method"
    sects_method = AmiPath.create(section_type, {PROJ: OIL186})

    ami_search.search_with_dictionaries(dicts, [sects_ack, sects_aff, sects_method])

def test_sect():
    ami_search = AmiSearch()
# section_types
    section_type = "ethics"
    sects_method = AmiPath.create(section_type, {PROJ: OIL186})

    dicts = [
        os.path.join(PMR_DIR, "ethics", "ethics.xml"),
        ]
    ami_search.search_with_dictionaries(dicts, [])


def make_graph(self, counter):
    import matplotlib.pyplot as plt
    print("counter")
    plt.bar(list(counter.keys()), counter.values(), color='g')
    plt.show()


if __name__ == "__main__":
    print("running search main")
    import nltk
    nltk.download('stopwords')
    main()
else:
    #    print("running search main anyway")
    #    main()
    pass

"""
https://gist.github.com/benhoyt/dfafeab26d7c02a52ed17b6229f0cb52
"""
