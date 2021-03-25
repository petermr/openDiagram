import os

# https://stackoverflow.com/questions/19917492/how-can-i-use-a-python-script-in-the-command-line-without-cd-ing-to-its-director

from file_lib import AmiPath, PROJ
from text_lib import TextUtil, AmiSection
from util import Util
from xml.etree import ElementTree as ET
from collections import Counter
import re

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
DICT_CEV_OPEN = os.path.join(DICT_DIR, "cevopen")
DICT_AMI3 = os.path.join(DICT_DIR, "ami3")
OPEN_VIRUS = os.path.join(PROJECTS, "openVirus")
MINIPROJ = os.path.join(OPEN_VIRUS, "miniproject")
MINICORPORA = os.path.join(CEV_OPEN_DIR, "minicorpora")
WORCESTER_DIR = os.path.join(PROJECTS, "worcester")
FUNDER = os.path.join(MINIPROJ, "funder")

# print(FUNDER, os.path.exists(FUNDER))


class AmiSearch:

    def __init__(self):
        self.dictionaries = []
        self.patterns = []
        self.projects = []
        self.sections = []
        self.word_counter = None
        self.debug = False
        self.do_search = True
        self.do_plot = True
        self.ami_projects = AmiProjects()
        self.cur_sect = None
#        self.cur_dict = None
        self.cur_proj = None

        # print every debug_cnt filenamwe
        self.debug_cnt = 10000
        # maximum files to search
        self.max_files = 10000
        self.min_hits = 1

        # look up how sections work
#        self.ami_sections = AmiSections()
        self.ami_dictionaries = AmiDictionaries()

    def make_graph(self, counter, dict_name):
        import matplotlib.pyplot as plt
#        ax = plt.gca()
        plt.bar(list(counter.keys()), counter.values(), color='blue')
#        ax.set_xticklabels(ax.get_xticks(), rotation=45)
        plt.xticks(rotation=45, ha='right') # this seems to work
        plt.title(self.make_title(dict_name))
        plt.show()

    def make_title(self, dict_name):
        ptit = self.cur_proj.dir.split("/")[-1:][0]
        return ptit + ":   " + self.cur_sect + ":   " + dict_name

    def use_dictionaries(self, args):
        print("use_dictionaries", args, type(args))
        for arg in args:
            print("dikt", arg, type(arg))
            self.add_dictionary(arg)

    def add_dictionary(self, name):
        print("name", name)
        AmiSearch._append_facet("dictionary", name, self.ami_dictionaries.dictionary_dict, self.dictionaries)

    def use_projects(self, args):
        for arg in args:
            self.add_project(arg)

    def add_project(self, name):
        AmiSearch._append_facet("project", name, self.ami_projects.project_dict, self.projects)

    @staticmethod
    def _append_facet(label, name, dikt, dict_list):
        if not name in dikt:
            raise Exception("unknown name", name, "in", dikt)
        dict_list.append(dikt[name])

    def search(self, file):
        words = TextUtil.get_words_in_section(file)
#        print("words", len(words))
        matches_by_amidict = self.match_words_against_dictionaries(words)
        matches_by_pattern = self.match_words_against_pattern(words)

        return matches_by_amidict, matches_by_pattern

    def match_words_against_dictionaries(self, words):
        matches_by_amidict = {}
        found = False
        for dictionary in self.dictionaries:
            hits = dictionary.match(words)
            matches_by_amidict[dictionary.name] = hits
        return matches_by_amidict

    def match_words_against_pattern(self, words):
        matches_by_pattern = {}
        found = False
        for pattern in self.patterns:
            hits = pattern.match(words)
            matches_by_pattern[pattern.name] = hits
        return matches_by_pattern

    @staticmethod
    def print_file(file):
        print("file: ", file)
        with open(file, "r") as f:
            print("read", f.read())

    def search_and_count(self, section_files):
        dictionary_counter_dict = self.create_counter_dict(self.dictionaries)
        pattern_counter_dict = self.create_counter_dict(self.patterns)

        for index, target_file in enumerate(section_files[:self.max_files]):

            if index % self.debug_cnt == 0:
                print("file", target_file)
            matches_by_amidict, matches_by_pattern = self.search(target_file)
            self.add_matches_to_counter_dict(dictionary_counter_dict, matches_by_amidict)
            self.add_matches_to_counter_dict(pattern_counter_dict, matches_by_pattern)

        return dictionary_counter_dict, pattern_counter_dict

    def create_counter_dict(self, search_tools):
        counter_dict = {}
        for tool in search_tools:
            counter_dict[tool.name] = Counter()
        return counter_dict

    def add_matches_to_counter_dict(self, counter_dict, matches_by_amidict):
        for amidict in matches_by_amidict:
            matches = matches_by_amidict[amidict]
            if len(matches) > 0:
                for match in matches:
                    counter_dict[amidict][match] += 1

    def use_sections(self, sections):
        AmiSection.check_sections(sections)
        self.sections = sections

    def run_search(self):
        for proj in self.projects:
            print("***** project", proj.dir)
            self.cur_proj = proj
            for sect in self.sections:
                self.cur_sect = sect
                section_files = AmiPath.create(sect, {PROJ: proj.dir}).get_globbed_files()
                print("***** section_files", sect, len(section_files))
                counter_dict, pattern_dict = self.search_and_count(section_files)

                self.plot_tool_hits(counter_dict)
                self.plot_tool_hits(pattern_dict)

    def plot_tool_hits(self, tool_dict):
        for tool in tool_dict:
            c = tool_dict[tool]
            min_counter = Counter({k: c for k, c in c.items() if c >= self.min_hits})
            if self.do_plot:
                self.make_graph(min_counter, tool)

    @staticmethod
    def demo():
        ami_search = AmiSearch()
        ami_search.min_hits = 2

        ami_search.use_sections([
#            "method",
            AmiSection.INTRO,
            AmiSection.METHOD,
#            "fig_caption"
        ])
        ami_search.use_dictionaries([
            # intern dictionaries
#            AmiDictionaries.ACTIVITY,
#            AmiDictionaries.PLANT_COMPOUND,
#            AmiDictionaries.PLANT_PART,
            AmiDictionaries.PLANT_GENUS,

            AmiDictionaries.COUNTRY,
#            AmiDictionaries.GENUS,
#            AmiDictionaries.ELEMENT,
#            AmiDictionaries.ORGANIZATION,
#            AmiDictionaries.SOLVENT,
        ])
        ami_search.use_projects([
            AmiProjects.OIL26,
#            AmiProjects.OIL186,
#            AmiProjects.CCT,
#            AmiProjects.WORC_EXPLOSION,
#            AmiProjects.WORC_SYNTH,

            # minipprjects
#            AmiProjects.C_ACTIVITY,
            AmiProjects.C_INVASIVE,
#            AmiProjects.C_HYDRODISTIL,
#            AmiProjects.C_PLANT_PART,
        ])

#        ami_search.add_regex("abb_genus", "^[A-Z]\.$")
        ami_search.add_regex("all_caps", "^[A-Z]{3,}$")

        if ami_search.do_search:
            ami_search.run_search()

    def add_regex(self, name, regex):
        self.patterns.append(SearchPattern(name, SearchPattern.REGEX, regex))


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
    WORC_EXPLOSION = "worc_explosion"
    WORC_SYNTH = "worc_synth"

    # minicorpora
    C_ACTIVITY = "activity"
    C_INVASIVE = "invasive"
    C_PLANT_PART = "plantpart"
    C_HYDRODISTIL = "hydrodistil"


    def __init__(self):
        self.create_project_dict()

    def create_project_dict(self):
        self.project_dict = {}
        self.add_with_check(AmiProjects.LIION10, os.path.join(PHYSCHEM_RESOURCES, "liion10"))
        self.add_with_check(AmiProjects.OIL26, os.path.join(PHYSCHEM_RESOURCES, "oil26"))
        self.add_with_check(AmiProjects.OIL186, os.path.join(PROJECTS, "CEVOpen/searches/oil186"))
        self.add_with_check(AmiProjects.CCT, os.path.join(PROJECTS, "openDiagram/python/diagrams/satish/cct"))
        self.add_with_check(AmiProjects.WORC_SYNTH, os.path.join(PROJECTS, "worcester/synthesis"))
        self.add_with_check(AmiProjects.WORC_EXPLOSION, os.path.join(PROJECTS, "worcester/explosion"))

        # minicorpora
        self.add_with_check(AmiProjects.C_ACTIVITY, os.path.join(MINICORPORA, "activity"))
        self.add_with_check(AmiProjects.C_HYDRODISTIL, os.path.join(MINICORPORA, "hydrodistil"))
        self.add_with_check(AmiProjects.C_INVASIVE, os.path.join(MINICORPORA, "invasive"))
        self.add_with_check(AmiProjects.C_PLANT_PART, os.path.join(MINICORPORA, "plantpart"))


    def add_with_check(self, key, file):
        Util.check_exists(file)
        self.project_dict[key] = AmiProject(file)

class AmiProject:
    def __init__(self, dir):
        self.dir = dir

class SearchPattern:

    """ holds a regex or other pattern constraint (e.g. isnumeric) """
    REGEX = "regex"
    NUMBER = "_NUMBER"
    SPECIES = "_SPECIES"
    GENE = "_GENE"

    def __init__(self, name, type, value):
        self.name = name
        self.type = type
        self.value = value
        if SearchPattern.REGEX == type:
            self.regex = re.compile(value)

    def match(self, words):
        matched_words = []
        for word in words:
            matched = False
            if self.regex:
                matched = self.regex.match(word)
            elif SearchPattern.NUMBER == self.type:
                matched = str.isnumeric(word)
            else:
                pass
            if matched:
                matched_words.append(word)

        return matched_words


class SearchDictionary:
    """wrapper for an ami dictionary including search flags

    """

    TERM = "term"


    def __init__(self, file, **kwargs):
        if not os.path.exists(file):
            raise IOError("cannot find file " + str(file))
        self.read_dictionary(file)
        self.name = file.split("/")[-1:][0].split(".")[0]
        self.options = {} if not "options" in kwargs else kwargs["options"]
        if "synonyms" in self.options:
            print("use synonyms")
        if "noignorecase" in self.options:
            print("use case")
        self.split_terms = True

    def read_dictionary(self, file, ignorecase=True):
        self.file = file
        self.amidict = ET.parse(file)
        self.root = self.amidict.getroot()
        self.name = self.root.attrib["title"]
        self.ignorecase = ignorecase
        self.entries = list(self.root.findall("entry"))
        self.entry_by_term = self.create_entry_by_term();
        self.term_set = set()
        print("read dictionary", self.name, "with", len(self.entries), "entries")

    def get_or_create_term_set(self):
        if len(self.term_set) == 0:
            for entry in self.entries:
                if SearchDictionary.TERM in entry.attrib:
                    term = self.term_from_entry(entry)
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

    def term_from_entry(self, entry):
        if SearchDictionary.TERM not in entry.attrib:
            print("missing term", ET.tostring(entry))
        term = entry.attrib[SearchDictionary.TERM].strip()
        return term.lower() if self.ignorecase else term

    def add_processed_term(self, term):
        if self.ignorecase:
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

    def get_entry(self, term):
        return self.entry_by_term[term] if term in self.entry_by_term else None

    def create_entry_by_term(self):
        entry_by_term = {self.term_from_entry(entry) : entry  for entry in self.entries}


class AmiDictionaries:

    ACTIVITY = "activity"
    COMPOUND = "compound"
    COUNTRY = "country"
    ELEMENT = "elements"
    PLANT_GENUS = "plant_genus"
    ORGANIZATION = "organization"
    PLANT_COMPOUND = "plant_compound"
    PLANT = "plant"
    PLANT_PART = "plant_part"
    SOLVENT = "solvent"

    DICT_LIST = [
        ACTIVITY,
        COMPOUND,
        COUNTRY,
        ELEMENT,
        PLANT_GENUS,
        ORGANIZATION,
        PLANT,
        PLANT_COMPOUND,
        PLANT_PART,
        SOLVENT,
    ]


    def __init__(self):
        self.create_search_dictionary_dict()

    @staticmethod
    def check_dicts(dicts):
        for dikt in dicts:
            if dikt not in SearchDictionary.DICT_LIST:
                print("allowed dictionaries", SearchDictionary.DICT_LIST)
                raise Exception ("unknown dictionary: ", dikt)

    def create_search_dictionary_dict(self):
        self.dictionary_dict = {}

        # chemistry
        self.add_with_check(AmiDictionaries.ELEMENT,
                            os.path.join(DICT_AMI3, "elements.xml"))
        self.add_with_check(AmiDictionaries.SOLVENT,
                            os.path.join(DICT_AMI3, "solvents.xml"))

#        / Users / pm286 / projects / CEVOpen / dictionary / eoActivity / eo_activity / Activity.xml
        self.add_with_check(AmiDictionaries.ACTIVITY,
                            os.path.join(CEV_OPEN_DICT_DIR, "eoActivity", "eo_activity", "Activity.xml"))
        self.add_with_check(AmiDictionaries.COUNTRY,
                            os.path.join(OV21_DIR, "country", "country.xml"))
        self.add_with_check(AmiDictionaries.COMPOUND,
                            os.path.join(CEV_OPEN_DICT_DIR, "eoCompound", "eoCompound.xml"))
        # /Users/pm286/dictionary/cevopen/plant_genus/eo_plant_genus.xml
        self.add_with_check(AmiDictionaries.PLANT_GENUS,
                            os.path.join(CEV_OPEN_DICT_DIR, "plant_genus", "plant_genus.xml"))
        self.add_with_check(AmiDictionaries.ORGANIZATION,
                            os.path.join(OV21_DIR, "organization", "organization.xml"))
#        / Users / pm286 / projects / CEVOpen / dictionary / eoCompound / plant_compounds.xml
        self.add_with_check(AmiDictionaries.PLANT_COMPOUND,
                            os.path.join(CEV_OPEN_DICT_DIR, "eoCompound", "plant_compounds.xml"))
        self.add_with_check(AmiDictionaries.PLANT_PART,
                            os.path.join(CEV_OPEN_DICT_DIR, "eoPlantPart", "eoplant_part.xml"))
#        self.add_with_check(AmiDictionaries.PLANT,
#                            os.path.join(CEV_OPEN_DICT_DIR, "eoPlant", "eoPlant", "Plant.xml"))


        return self.dictionary_dict

    def add_with_check(self, key, file):
        Util.check_exists(file)
        dictionary = SearchDictionary(file)
        self.dictionary_dict[key] = dictionary
#        print(dictionary.get_or_create_term_set())
        return

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

    parser = argparse.ArgumentParser(description='Search sections with dictionaries and patterns')
    """
    """
    parser.add_argument('--dict', nargs="+",
                        help='dictionaries to search with (lookup table from JSON (NYI); empty gives list')
    parser.add_argument('--sect', nargs="+",
                        help='sections to search; empty gives all (Not yet tested')
    parser.add_argument('--proj', nargs="+",
                        help='projects to search; empty will exit')
    parser.add_argument('--patt', nargs="+",
                        help='patterns to search with; regex may need quoting')

    args = parser.parse_args()
    if      args.dict is None \
        and args.sect is None \
        and args.proj is None \
        and args.patt is None \
        :
        print("DEMO")
        AmiSearch.demo()
    else:
        print("dicts", args.dict, type(args.dict))
        print("sects", args.sect, type(args.sect))
        print("projs", args.proj, type(args.proj))
        print("patterns", args.patt, type(args.patt))
        ami_search = AmiSearch()
        ami_search.use_sections(args.sect)
        ami_search.use_dictionaries(args.dict)
        ami_search.use_projects(args.proj)

        if ami_search.do_search:
            ami_search.run_search()



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
"""https://stackoverflow.com/questions/22052532/matplotlib-python-clickable-points"""