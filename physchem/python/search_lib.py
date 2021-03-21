import os

# https://stackoverflow.com/questions/19917492/how-can-i-use-a-python-script-in-the-command-line-without-cd-ing-to-its-director

from file_lib import AmiPath, PROJ
from text_lib import TextUtil
from util import Util
from xml.etree import ElementTree as ET
from collections import Counter

HOME = os.path.expanduser("~")
PYDIAG = "../../python/diagrams"
#LIION = "../liion"
DICT_DIR = os.path.join(HOME, "dictionary")

OV21_DIR = os.path.join(DICT_DIR, "openVirus20210120")
CEV_DICT_DIR = os.path.join(DICT_DIR, "cevopen")
PMR_DIR = os.path.join(DICT_DIR, "pmr")

PROJECTS = os.path.join(HOME, "projects")
OPEN_DIAGRAM = os.path.join(PROJECTS, "openDiagram")
PHYSCHEM = os.path.join(OPEN_DIAGRAM, "physchem")
PHYSCHEM_RESOURCES = os.path.join(PHYSCHEM, "resources")
CEV_OPEN_DIR = os.path.join(PROJECTS, "CEVOpen")
CEV_OPEN_DICT_DIR = os.path.join(CEV_OPEN_DIR, "dictionary")
OPEN_VIRUS = os.path.join(PROJECTS, "openVirus")
MINIPROJ = os.path.join(OPEN_VIRUS, "miniproject")
FUNDER = os.path.join(MINIPROJ, "funder")

# print(FUNDER, os.path.exists(FUNDER))

class AmiSearch:

    def __init__(self):
        self.dictionaries = []
        self.projects = []
        self.sections = []
        self.word_counter = None
        self.debug = False
        self.do_search = True
        self.do_plot = True
        self.ami_projects = AmiProjects()
        self.cur_sect = None
        self.cur_dict = None
        self.cur_proj = None

        # print every debug_cnt filenamwe
        self.debug_cnt = 10000
        # maximum files to search
        self.max_files = 10000

        # look up how sections work
#        self.ami_sections = AmiSections()
        self.ami_dictionaries = AmiDictionaries()

    def make_graph(self, dictionary):
        import matplotlib.pyplot as plt
#        ax = plt.gca()
        plt.bar(list(dictionary.keys()), dictionary.values(), color='blue')
#        ax.set_xticklabels(ax.get_xticks(), rotation=45)
        plt.xticks(rotation=45, ha='right') # this seems to work
        plt.title(self.make_title())
        plt.show()

    def make_title(self):
        ptit = self.cur_proj.dir.split("/")[-1:][0]
        return ptit + ":   " + self.cur_sect + ":   " + self.cur_dict.name

    def use_dictionaries(self, *args):
        for arg in args:
            self.add_dictionary(arg)

    def add_dictionary(self, name):
        AmiSearch._append_facet("dictionary", name, self.ami_dictionaries.dictionary_dict, self.dictionaries)

    def use_projects(self, *args):
        for arg in args:
            self.add_project(arg)

    def add_project(self, name):
        AmiSearch._append_facet("project", name, self.ami_projects.project_dict, self.projects)

    """
    def use_sections(self, *args):
        for arg in args:
            self.add_section(arg)

    def add_section(self, name):
        print("******************don't use sections here")
        AmiSearch._append_facet("section", name, self.sections.section_dict, self.sections)
    """

    @staticmethod
    def _append_facet(label, name, dikt, dict_list):
        if not name in dikt:
            raise Exception("unknown", label, name)
        dict_list.append(dikt[name])

    def search(self, file):
        words = TextUtil.get_words_in_section(file)
#        print("words", len(words))
        matches_by_amidict = self.match_words_against_dictionaries(file, words)

        return matches_by_amidict

    def match_words_against_dictionaries(self, file, words):
        matches_by_amidict = {}
        found = False
        for dictionary in self.dictionaries:
            #            print("d", dictionary)
            self.cur_dict = dictionary
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

    def search_and_count(self, section_files):
        counter = Counter()
        for index, target_file in enumerate(section_files[:self.max_files]):

            if index % self.debug_cnt == 0:
                print("file", target_file)
            matches_by_amidict = self.search(target_file)
            if self.do_search:
                for amidict in matches_by_amidict:
                    matches = matches_by_amidict[amidict]
                    if len(matches) > 0:
                        for match in matches:
                            counter[match] += 1
        print("counter", counter)
        if self.do_plot:
            self.make_graph(counter)

    def use_sections(self, sections):
        self.sections = sections

    def run_search(self):
        for proj in self.projects:
            print("***** project", proj.dir)
            self.cur_proj = proj
            for sect in self.sections:
                self.cur_sect = sect
                section_files = AmiPath.create(sect, {PROJ: proj.dir}).get_globbed_files()
                print("***** section_files", sect, len(section_files))
                self.search_and_count(section_files)

    @staticmethod
    def test_sect_dicts():
        ami_search = AmiSearch()

        ami_search.use_sections(["method", "introduction", "fig_caption"])
        ami_search.use_dictionaries(AmiDictionaries.COUNTRY, AmiDictionaries.ORGANIZATION)
#        ami_search.use_projects(AmiProjects.OIL186, AmiProjects.CCT)
        ami_search.use_projects(AmiProjects.OIL26)

        ami_search.run_search()

    @staticmethod
    def test_sect():
        """ not currently used"""
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


class SimpleDict:

    def __init__(self, file=None):
        if file:
            with open(file, "r") as f:
                self.lines = f.read().splitlines()
        print(self.lines)


class AmiProjects:
    """project files"""
    LIION10 = "liion10"
    OIL186 = "oil186"
    OIL26 = "oil26"
    CCT    = "cct"

    def __init__(self):
        self.create_project_dict()

    def create_project_dict(self):
        self.project_dict = {}
        self.add_with_check(AmiProjects.LIION10, os.path.join(PHYSCHEM_RESOURCES, "liion10"))
        self.add_with_check(AmiProjects.OIL26, os.path.join(PHYSCHEM_RESOURCES, "oil26"))
        self.add_with_check(AmiProjects.OIL186, os.path.join(PROJECTS, "CEVOpen/searches/oil186"))
        self.add_with_check(AmiProjects.CCT, os.path.join(PROJECTS, "openDiagram/python/diagrams/satish/cct"))

    def add_with_check(self, key, file):
        Util.check_exists(file)
        self.project_dict[key] = AmiProject(file)

class AmiProject:
    def __init__(self, dir):
        self.dir = dir

class SearchDictionary:
    """wrapper for an ami dictionary including search flags

    """

    TERM = "term"

    def __init__(self, file, **kwargs):
        if not os.path.exists(file):
            raise IOError("cannot find file " + str(file))
        self.read_file(file)
        self.name = file.split("/")[-1:][0].split(".")[0]
        self.options = {} if not "options" in kwargs else kwargs["options"]
        if "synonyms" in self.options:
            print("use synonyms")
        if "noignorecase" in self.options:
            print("use case")
        self.split_terms = True

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
                        self.add_processed_term(term)
                    elif self.split_terms:
                        # multiword terms
                        for term in " ".split(term):
                            self.add_processed_term(term)

        #            print(len(self.term_set), list(sorted(self.term_set)))
#        print ("terms", len(self.term_set))
        return self.term_set

    def add_processed_term(self, term):
        term = term.lower()
        self.term_set.add(term)  # single word countries

    def match(self, target_words):
        matched = []
        self.get_or_create_term_set()
        for target_word in target_words:
            target_word = target_word.lower()
            if target_word in self.term_set:
                matched.append(target_word)
        return matched

class AmiDictionaries:

    COMPOUND = "compound"
    COUNTRY = "country"
    ORGANIZATION = "organization"
    PLANT_PART = "plant_part"

    def __init__(self):
        self.create_search_dictionary_dict()

    def create_search_dictionary_dict(self):
        self.dictionary_dict = {}
        self.add_with_check(AmiDictionaries.COUNTRY,
                            os.path.join(OV21_DIR, "country", "country.xml"))
        self.add_with_check(AmiDictionaries.COMPOUND,
                            os.path.join(CEV_OPEN_DICT_DIR, "eoCompound", "eoCompound.xml"))
        self.add_with_check(AmiDictionaries.ORGANIZATION,
                            os.path.join(OV21_DIR, "organization", "organization.xml"))
        self.add_with_check(AmiDictionaries.PLANT_PART,
                            os.path.join(CEV_OPEN_DICT_DIR, "eoPlantPart", "eoplant_part.xml"))
        return self.dictionary_dict

    def add_with_check(self, key, file):
        Util.check_exists(file)
        self.dictionary_dict[key] = SearchDictionary(file)


def test_profile():
    import cProfile
    print("profile")
    cProfile.run("[x for x in range(1500)]")

def test_profile1():
    import cProfile
    print("profile1")
    cProfile.run("AmiSearch.test_sect_dicts()")

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
# the main test

    AmiSearch.test_sect_dicts()
# this profiles it
#    test_profile1()
    print("finished search")


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
