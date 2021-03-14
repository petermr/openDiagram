import os

# https://stackoverflow.com/questions/19917492/how-can-i-use-a-python-script-in-the-command-line-without-cd-ing-to-its-director

from file_lib import AmiPath, PROJ
from text_lib import TextUtil
from xml.etree import ElementTree as ET
from collections import Counter

HOME = os.path.expanduser("~")
PYDIAG = "../../python/diagrams"
LIION = "../liion"
DICT_DIR = os.path.join(HOME, "dictionary")
OV21_DIR = os.path.join(DICT_DIR, "openVirus20210120")
CEV_DIR = os.path.join(DICT_DIR, "cevopen")
PMR_DIR = os.path.join(DICT_DIR, "pmr")
PROJECTS = os.path.join(HOME, "projects")
OIL186 = os.path.join(PROJECTS, "CEVOpen/searches/oil186") #https://github.com/petermr/CEVOpen
CCT = os.path.join(PROJECTS, "openDiagram/python/diagrams/satish/cct")
OPEN_VIRUS = os.path.join(PROJECTS, "openVirus")
MINIPROJ = os.path.join(OPEN_VIRUS, "miniproject")
FUNDER = os.path.join(MINIPROJ, "funder")

# print(FUNDER, os.path.exists(FUNDER))

class AmiSearch:

    def __init__(self):
        self.dictionaries = []
        self.word_counter = None
        self.debug = False

    def make_graph(self, dictionary):
        import matplotlib.pyplot as plt
#        ax = plt.gca()
        plt.bar(list(dictionary.keys()), dictionary.values(), color='blue')
#        ax.set_xticklabels(ax.get_xticks(), rotation=45)
        plt.xticks(rotation=45, ha='right') # this seems to work
        plt.show()

    def add_search_dictionary(self, dictionary):
        """adds a SearchDictionary
        """
        if dictionary is None or type(dictionary) != SearchDictionary:
            raise Exception("Search requires a SearchDictionary")
        self.dictionaries.append(dictionary)

    def use_dicts(self, dict_names):
        self.dict_dicts = {
            "country": os.path.join(OV21_DIR, "country", "country.xml"),
            "compound": os.path.join(CEV_DIR, "compound", "eo_compound.xml"),
        }
        self.dict_list = [self.dict_dicts[name] for name in dict_names]


    def search(self, file):
        matches_by_amidict = {}
        words = TextUtil.get_words_in_file(file)
#        print("words", len(words))

        found = False
        for dictionary in self.dictionaries:
#            print("d", dictionary)
            hits = dictionary.match(words)
            matches_by_amidict[dictionary.name] = hits
            if len(hits) > 0:
                found = True
                if self.debug:
                    print("HITS", len(hits))
        if found and self.debug:
            print("file: ", file)
            with open(file, "r") as f:
                print("read", f.read())

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
#            print("matchesx", matches_by_amidict)
            for amidict in matches_by_amidict:
#                print("dict>", amidict)
                matches = matches_by_amidict[amidict]
                if len(matches) > 0:
#                    print("matches", len(matches))
                    for match in matches:
                        counter[match] += 1
#        counter = self.sortxx(counter)
        print("counter", counter)
        self.make_graph(counter)

    def sortxx(self, counter):
        sorted_d = sorted((key, value) for (key, value) in counter.items())
        return sorted_d

    def set_dictionaries(self, dictionary_names):
        self.dict_names = dictionary_names

    def set_project(self, project):
        self.project = project

    def set_sections(self, sections):
        self.sections = sections


class SimpleDict:

    def __init__(self, file=None):
        if file:
            with open(file, "r") as f:
                self.lines = f.read().splitlines()
        print(self.lines)


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Search sections with dictionaries')
    """
    parser.add_argument('integers', metavar='N', type=int, nargs='+',
                        help='an integer for the accumulator')
    parser.add_argument('--sum', dest='accumulate', action='store_const',
                        const=sum, default=max,
                        help='sum the integers (default: find the max)')
    """
    parser.add_argument('--dict', nargs="+",
                        help='dictiomaries to search with (lookup table from JSON (NYI); empty gives list')
    parser.add_argument('--sect', nargs="+",
                        help='sections to search; empty gives list')


    args = parser.parse_args()
    print("dicts", args.dict)
    print("sects", args.sect)

#    print(f"Name of the script      : {sys.argv[0]=}")
#    print(f"Arguments of the script : {sys.argv[1:]=}")
#    return
    test_sect_dicts()
    print("finished search")


class SearchDictionary:
    """wrapper for an ami dictionary including search flags

    """

    TERM = "term"

    def __init__(self, file, **kwargs):
        if not os.path.exists(file):
            raise IOError("cannot find file " + str(file))
        self.read_file(file)
        self.options = {} if not "options" in kwargs else kwargs["options"]
        if "synonyms" in self.options:
            print("use synonyms")
        if "noignorecase" in self.options:
            print("use case")


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
                if SearchDictionary.TERM in entry.attrib:
                    term = entry.attrib[SearchDictionary.TERM]
                    # single word terms
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
    country_file = os.path.join(OV21_DIR, "country", "country.xml")
    compound_file = os.path.join(CEV_DIR, "compound", "eo_compound.xml")
#    ami_search.add_search_dictionary(SearchDictionary(country_file, options={"synonyms", "noignorecase", "ngrams"}))
    ami_search.add_search_dictionary(SearchDictionary(compound_file))
# dictionaries
    #    search_dictionary = SearchDictionary(os.path.join(OV21_DIR, "organization/organization.xml"))
    """
    ami_search.dict_dicts = {
        "country": country_file,
        "compound": compound_file,
    }
    """

#    ami_search.add_search_dictionary()
#    ami_search.use_dicts(["country", "compound"])
# section_types
#    project = {PROJ: OIL186}
#    project = {PROJ: CCT}
    project = OIL186
    ami_search.set_project(project)

#    project = {PROJ: FUNDER}
    sects = [
#        "acknowledge", "affiliation", "ethics",
        "method", "introduction"]
    ami_search.set_sections(sects)
#    ami_search.set_dictionaries()
    # this may not be correct
    for sect in sects:
        section_files = AmiPath.create(sect, {PROJ: OIL186}).get_globbed_files()
        print("***** section_files", sect, len(section_files))
        ami_search.search_and_count(section_files)




def test_sect():
    ami_search = AmiSearch()
# section_types
    section_type = "ethics"
    sects_method = AmiPath.create(section_type, {PROJ: OIL186})

    ami_search.dicts = [
        os.path.join(PMR_DIR, "ethics", "ethics.xml"),
        ]
#    globlets = [        AmiPath.create("fig_caption", {PROJ: proj_dir}),
#        AmiPath.create("", {PROJ: proj_dir}),


#    ami_search.search_with_dictionaries(dicts, globlets)
    section_files = AmiPath.create("fig_caption", {PROJ: OIL186}),
    ami_search.search_and_count(section_files)


def make_graph(self, counter):
    import matplotlib.pyplot as plt
    print("counter")
    fig, ax = plt.subplots()
    names = list(counter.keys())
    print("names>", names)
    ax.bar(names, counter.values(), color='g') # orig

#    plt.xticks(rotation=30)
    plt.setp(ax.get_xticklabels(), rotation=30, ha='right')
    plt.show()

# https://www.pythoncharts.com/matplotlib/rotating-axis-labels/

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
