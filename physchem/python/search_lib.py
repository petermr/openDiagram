import os

# https://stackoverflow.com/questions/19917492/how-can-i-use-a-python-script-in-the-command-line-without-cd-ing-to-its-director

from file_lib import AmiPath, PROJ
from text_lib import TextUtil, AmiSection, WordFilter
from xml_lib import XmlLib
from util import Util
#from xml.etree import ElementTree as ET
from lxml import etree as ET
from collections import Counter
import re
import unicodedata
import json
from gutil import Gutil

HOME = os.path.expanduser("~")
PYDIAG = "../../python/diagrams"
#LIION = "../liion"
DICT_DIR = os.path.join(HOME, "dictionary")
PROJECTS = os.path.join(HOME, "projects")

OV21_DIR = os.path.join(DICT_DIR, "openVirus20210120")
CEV_DICT_DIR = os.path.join(DICT_DIR, "cevopen")
PMR_DIR = os.path.join(DICT_DIR, "pmr")

OPEN_DIAGRAM = os.path.join(PROJECTS, "openDiagram")
OPEN_DIAGRAM_SEARCH = os.path.join(OPEN_DIAGRAM, "searches")

PHYSCHEM = os.path.join(OPEN_DIAGRAM, "physchem")
PHYSCHEM_RESOURCES = os.path.join(PHYSCHEM, "resources")
PHYSCHEM_PYTHON = os.path.join(PHYSCHEM, "python")   # where code and config lives
DIAGRAMS_DIR = os.path.join(PROJECTS, "openDiagram", "python", "diagrams")

# require CEVOpen repo

CEV_OPEN_DIR = os.path.join(PROJECTS, "CEVOpen")
CEV_OPEN_DICT_DIR = os.path.join(CEV_OPEN_DIR, "dictionary")
MINICORPORA = os.path.join(CEV_OPEN_DIR, "minicorpora")

# require dictionary repo
DICT_CEV_OPEN = os.path.join(DICT_DIR, "cevopen")
DICT_AMI3 = os.path.join(DICT_DIR, "ami3")

# require openVirus repo
OPEN_VIRUS = os.path.join(PROJECTS, "openVirus")
MINIPROJ = os.path.join(OPEN_VIRUS, "miniproject")
FUNDER = os.path.join(MINIPROJ, "funder")

# requires Worcester repo
WORCESTER_DIR = os.path.join(PROJECTS, "worcester")


class AmiSearch:

    FIG_CAPTION_DEMO = "fig_caption"
    LUKE_DEMO = "luke"
    DIFFPROT_DEMO = "diffprot"
    DISEASE_DEMO = "disease"
    ETHICS_DEMO = "ethics"
    GENUS_DEMO = "genus" # TODO
    INVASIVE_DEMO = "invasive"
    MATTHEW_DEMO = "matthew"
    PLANT_DEMO = "plant"
    WORCESTER_DEMO = "worcester"
    WORD_DEMO = "word"

    DEMOS_JSON = os.path.join(PHYSCHEM_PYTHON, "demos.json")


    def __init__(self):
        # these are the main facets
        self.dictionaries = []
        self.patterns = []
        self.projects = []
        self.section_types = []

# working global variables
        self.cur_section_type = None
        self.cur_proj = None

#        self.word_counter = None
        self.debug = False
        self.do_search = True
        self.do_plot = True
        self.ami_projects = AmiProjects()

        self.max_bars = 10
        self.wikidata_label_lang = "en"

        # print every debug_cnt filenamwe
        self.debug_cnt = 10000
        # maximum files to search
        self.max_files = 10000
        self.min_hits = 2
        self.require_wikidata = False

        # look up how sections work
#        self.ami_sections = AmiSections()
        self.ami_dictionaries = AmiDictionaries()

    @staticmethod
    def run_demos(demos):
        demo_dict = {
            AmiSearch.DIFFPROT_DEMO : AmiSearch.diffprot_demo,
            AmiSearch.DISEASE_DEMO : AmiSearch.disease_demo,
            AmiSearch.ETHICS_DEMO : AmiSearch.ethics_demo,
            AmiSearch.FIG_CAPTION_DEMO : AmiSearch.fig_caption_demo,
            AmiSearch.INVASIVE_DEMO : AmiSearch.invasive_demo,
            AmiSearch.LUKE_DEMO : AmiSearch.luke_demo,
            AmiSearch.MATTHEW_DEMO : AmiSearch.matthew_demo,
            AmiSearch.PLANT_DEMO : AmiSearch.plant_parts_demo,
            AmiSearch.WORCESTER_DEMO : AmiSearch.worc_demo,
            AmiSearch.WORD_DEMO : AmiSearch.word_demo,
        }
        print("RUN DEMOS:", demos)
        if demos is None or len(demos) == 0:
            print("no demo given, choose from ", demo_dict.keys())
        else:
            for demo in demos:
                AmiSearch.run_demo(demo_dict, demo)
        print("END DEMO")

    @staticmethod
    def run_demo(demo_dict, demo):
        if demo in demo_dict.keys():
            demo_dict[demo]()
        else:
            demo_funct = Util.find_unique_dict_entry(demo_dict, demo)
            if demo_funct is not None:
                print("running:", demo_funct)
                demo_funct()

    def make_graph(self, counter, dict_name):
        import matplotlib as mpl
        import matplotlib.pyplot as plt
#        mpl.rcParams['font.family'] = 'sans-serif'
        mpl.rcParams['font.family'] = 'Helvetica'
        import matplotlib.pyplot as plt
#        rc('font', family='Arial')
#        ax = plt.gca()
        commonest = counter.most_common()
        keys = [c[0] for c in commonest]
        values = [c[1] for c in commonest]
#        plt.bar(list(counter.keys()), counter.values(), color='blue')
        plt.bar(keys[:self.max_bars], values[:self.max_bars], color='blue')
#        ax.set_xticklabels(ax.get_xticks(), rotation=45)
        plt.xticks(rotation=45, ha='right') # this seems to work
        plt.title(self.make_title(dict_name))
        plt.show()

    def make_title(self, dict_name):
        ptit = self.cur_proj.dir.split("/")[-1:][0]
        return ptit + ":   " + self.cur_section_type + ":   " + dict_name

    def use_dictionaries(self, args):
        if args is not None and len(args) > 0:
            for arg in args:
                self.add_dictionary(arg)
        else:
            # print dictionaries
            print("\n==========AMI DICTIONARIES========")
#            print("amidict keys: ", self.dict_)
            print("==================================\n")

    def add_dictionary(self, name):
        print("dict_name:", name)
        AmiSearch._append_facet("dictionary", name, self.ami_dictionaries.dictionary_dict, self.dictionaries)

    # crude till we work this out
    def use_patterns(self, args):
        if args is not None:
            for arg in args:
                self.use_pattern(arg)

    def use_pattern(self, pattern, name=None):
        """ use either name and pattern or name='pattern' """
        regex = pattern
        if name is None and "=" in pattern:
            name = pattern.split("=", 0)
            regex = pattern.split("=", 2)
        print (name, "=", regex)
        self.patterns.append(SearchPattern(regex, name))


    def use_projects(self, args):
        print("projects", args)
        if args is None or len(args) == 0:
            print("=================", "\n", "must give projects; here are some to test with, but they may need checking out")
            for key in AmiProjects().project_dict.keys():
                proj = AmiProjects().project_dict[key]
                print(key, "=>", proj.description)
            print("=================")
        else:
            for arg in args:
                self.add_project(arg)

    def add_project(self, name):
        AmiSearch._append_facet("project", name, self.ami_projects.project_dict, self.projects)

    def use_filters(self, name):
        print("filters NYI")

    @staticmethod
    def _append_facet(label, name, dikt, dict_list):
        if not name in dikt:
            raise Exception("unknown name: " +  name + " in " + str(dikt.keys()))
        dict_list.append(dikt[name])

    def search(self, file):
        words = TextUtil.get_words_in_section(file)
#        print("words", len(words))
        matches_by_amidict = self.match_single_words_against_dictionaries(words)
        matches_by_multiple = self.match_multiple_words_against_dictionaries(words)
        matches_by_pattern = self.match_words_against_pattern(words)

        return matches_by_amidict, matches_by_pattern

    def match_single_words_against_dictionaries(self, words):
        matches_by_amidict = {}
        found = False
        for dictionary in self.dictionaries:
            hits = dictionary.match(words)
            #            print("hits", len(hits))
            if dictionary.entry_by_term is not None:
                wid_hits = self.annotate_hits_with_wikidata(dictionary, hits)
            matches_by_amidict[dictionary.name] = wid_hits
        return matches_by_amidict

    def match_multiple_words_against_dictionaries(self, words):
        # really crude - we concatenate words into a giant string with
        matches_by_multiple = {}
        found = False

        for dictionary in self.dictionaries:
            hits = dictionary.match_multiple(words)
            #            print("hits", len(hits))
            if dictionary.entry_by_term is not None:
                wid_hits = self.annotate_hits_with_wikidata(dictionary, hits)
            matches_by_multiple[dictionary.name] = wid_hits
        return matches_by_multiple

    def annotate_hits_with_wikidata(self, dictionary, hits):
        wid_hits = []
        for hit in hits:
            if hit in dictionary.entry_by_term:
                entry = dictionary.entry_by_term[hit]
                if self.require_wikidata and "wikidataID" not in entry.attrib:
                    print("no wikidataID for ", hit, "in", dictionary.name)
                    continue
#                wikidata_id = entry.attrib["wikidataID"]
                label = hit
                if self.wikidata_label_lang in ['hi', 'ta', 'ur', 'fr', 'de']:
                    #                            self.xpath_search(entry)  # doesn't work
                    lang_label = self.search_by_xml_lang(entry)
                    if lang_label is not None:
                        label = lang_label
                wid_hits.append(label)
        return wid_hits

    def search_by_xml_lang(self, entry):
        label = None
        synonyms = entry.findall("synonym")
        for synonym in synonyms:
            if len(synonym.attrib) > 0:
#                print("attribs", synonym.attrib)
                pass
            if XmlLib.XML_LANG in synonym.attrib:
                lang = synonym.attrib[XmlLib.XML_LANG]
#                print("lang", lang)
                if lang == self.wikidata_label_lang:
                    label = synonym.text
#                    print("FOUND", label)
                    break
        return label

    def xpath_search(self, entry):
        """doesn't yet work"""
        lang_path = "synonym[" + XmlLib.XML_LANG + "='" + self.wikidata_label_lang + "']"
        #                            print("LP", lang_path)
        lang_equivs = entry.xpath('synonym[@xml:lang]', namespaces={'xml': XmlLib.XML_NS})
        lang_equivs = entry.findall(lang_path)
        if len(lang_equivs) > 0:
            lang_equiv = lang_equivs[0]
#            print("FOUND", self.wikidata_label_lang, lang_equiv)

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
        with open(file, "r", encoding="utf-8") as f:
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

#    def use_patterns(self, patterns):
#        SearchPattern.check_sections(patterns)
#        self.patterns = patterns

    def use_sections(self, sections):
        if sections is None or len(sections) == 0:
            self.section_help()
        else:
            try:
                AmiSection.check_sections(sections)
                self.section_types = sections
            except Exception as ex:
                print("\n=============cannot find section============\n", ex)
                self.section_help()
                print("\n===========================")
        return

    def section_help(self):
        print("sections to be used; ALL uses whole document (Not yet tested)")
        print("\n========SECTIONS===========")
        print(AmiSection.SECTION_LIST)
        print("===========================\n")

    def run_search(self):
        for proj in self.projects:
            print("***** project", proj.dir)
            self.cur_proj = proj
            for section_type in self.section_types:
                self.find_files_search_plot(proj, section_type)

    def find_files_search_plot(self, proj, section_type):
        self.cur_section_type = section_type
        templates = AmiPath.create_ami_path_from_templates(section_type, {PROJ: proj.dir})
        section_files = templates.get_globbed_files()
        print("***** section_files", section_type, len(section_files))
        counter_dict, pattern_dict = self.search_and_count(section_files)
        self.plot_tool_hits(counter_dict)
        self.plot_tool_hits(pattern_dict)

    def plot_tool_hits(self, tool_dict):
        for tool in tool_dict:
            c = tool_dict[tool]
            min_counter = Counter({k: c for k, c in c.items() if c >= self.min_hits})
            if self.do_plot:
                self.make_graph(min_counter, tool)
            print("tool:", tool, "\n", min_counter.most_common())
            self.make_dictionary(tool, min_counter)

    def make_dictionary(self, tool, counter):
        print("MOVE make_dictionary")
        print("<dictionary title='"+tool+"'>")
        for k, v in counter.items():
            if v > self.min_hits:
                print("  <entry term=`"+k.lower()+"'/>")
        print("</dictionary>")




    @staticmethod
    def plant_parts_demo():
        ami_search = AmiSearch()
        ami_search.min_hits = 2
        ami_search.wikidata_label_lang = "en"

        ami_search.use_sections([
#            "method",
            AmiSection.INTRO,
            AmiSection.METHOD,
#            AmiSection.TABLE,
            #            "fig_caption"
        ])
        ami_search.use_dictionaries([
            # intern dictionaries
            AmiDictionaries.ACTIVITY,
            AmiDictionaries.COMPOUND,
            AmiDictionaries.INVASIVE_PLANT,
            AmiDictionaries.PLANT,
            AmiDictionaries.PLANT_PART,
            AmiDictionaries.PLANT_GENUS,
        ])
        ami_search.use_projects([
            AmiProjects.OIL186,
        ])
        ami_search.use_filters([
            WordFilter.ORG_STOP
        ])

#        ami_search.add_regex("abb_genus", "^[A-Z]\.$")

        if ami_search.do_search:
            ami_search.run_search()

#    def add_regex(self, name, regex):
#        self.patterns.append(SearchPattern(name, SearchPattern.REGEX, regex))

    @staticmethod
    def diffprot_demo():
        ami_search = AmiSearch()
        ami_search.min_hits = 2

        ami_search.use_sections([AmiSection.METHOD,])
        ami_search.use_dictionaries([AmiDictionaries.PROT_STRUCT, AmiDictionaries.PROT_PRED, AmiDictionaries.CRISPR])
        ami_search.use_projects([AmiProjects.DIFFPROT,])

        ami_search.use_pattern("^[A-Z]{1,}[^\s]*\d{1,}$", "AB12")
        ami_search.use_pattern("_ALLCAPS", "all_capz")
        ami_search.use_pattern("_ALL", "_all")

        ami_search.run_search()


    @staticmethod
    def ethics_demo():
        ami_search = AmiSearch()
        ami_search.min_hits = 2

        ami_search.use_sections([AmiSection.ETHICS, ])
        ami_search.use_dictionaries([AmiDictionaries.ETHICS, AmiDictionaries.COUNTRY, AmiDictionaries.DISEASE, ])
        ami_search.use_projects([AmiProjects.DISEASE, ])
        ami_search.use_filters([WordFilter.ORG_STOP])

        ami_search.use_pattern("^[A-Z]{1,}[^\s]*\d{1,}$", "AB12")
        ami_search.use_pattern("_ALLCAPS", "all_capz")
        ami_search.use_pattern("_ALL", "_all")

        ami_search.run_search()

    @staticmethod
    def fig_caption_demo():
        ami_search = AmiSearch()
        ami_search.min_hits = 2

        ami_search.use_sections([AmiSection.FIG_CAPTION, ])
        ami_search.use_dictionaries([])
        ami_search.use_projects([AmiProjects.CCT, ])

        ami_search.use_pattern("Fig(ure)?", "FIG")
        ami_search.use_pattern("_ALL", "_all")

        ami_search.run_search()

    @staticmethod
    def matthew_demo():
        ami_search = AmiSearch()
        ami_search.min_hits = 2

        ami_search.use_sections([AmiSection.FIG_CAPTION, AmiSection.METHOD])
        ami_search.use_dictionaries([AmiDictionaries.ELEMENT, AmiDictionaries.CRYSTAL, AmiDictionaries.MAGNETISM])
        ami_search.use_projects([AmiProjects.LIION10, ])

        ami_search.use_pattern("^[A-Z]{1,}[^\s]*\d{1,}$", "AB12")
        ami_search.use_pattern("_ALLCAPS", "all_capz")
        ami_search.use_pattern("_ALL", "_all")

        ami_search.run_search()


    @staticmethod
    def species_demo():
        ami_search = AmiSearch()
        ami_search.min_hits = 2

        ami_search.use_sections([AmiSection.INTRO, AmiSection.METHOD])
        ami_search.use_dictionaries([])
        ami_search.use_projects([AmiProjects.OIL26, ])

        ami_search.use_pattern("^[A-Z][en]?\.", "SPECIES_ABB")
        ami_search.use_pattern("_ITALICS", "_italics")

        ami_search.run_search()


    @staticmethod
    def invasive_demo():
        ami_search = AmiSearch()
        ami_search.min_hits = 2

        ami_search.use_sections([AmiSection.SECTIONS])
        ami_search.use_dictionaries([AmiDictionaries.INVASIVE_PLANT])
        ami_search.use_dictionaries([AmiDictionaries.PLANT_GENUS]) # to check it works
        ami_search.use_projects([AmiProjects.C_INVASIVE])
        ami_search.use_projects([AmiProjects.OIL186])

        ami_search.run_search()

    @staticmethod
    def disease_demo():
        ami_search = AmiSearch()
        ami_search.min_hits = 1
        ami_search.max_bars = 200

        ami_search.use_sections([AmiSection.METHOD, AmiSection.RESULTS, AmiSection.ABSTRACT])
        ami_search.use_dictionaries([AmiDictionaries.DISEASE, AmiDictionaries.MONOTERPENE])
        ami_search.use_projects([AmiProjects.OIL186])

        ami_search.run_search()


    @staticmethod
    def luke_demo():
        ami_search = AmiSearch()
        ami_search.min_hits = 2

        ami_search.use_sections([AmiSection.METHOD, ])
        ami_search.use_dictionaries([AmiDictionaries.ELEMENT])
        ami_search.use_projects([AmiProjects.FFML20,])

        ami_search.use_pattern("^[A-Z]{1,}[^\s]*\d{1,}$", "AB12")
        ami_search.use_pattern("_ALLCAPS", "all_capz")
        ami_search.use_pattern("_ALL", "_all")

        ami_search.run_search()

    @staticmethod
    def worc_demo():
        ami_search = AmiSearch()
        ami_search.min_hits = 2

        ami_search.use_sections([AmiSection.METHOD])
        ami_search.use_dictionaries([AmiDictionaries.ELEMENT])
        ami_search.use_dictionaries([AmiDictionaries.SOLVENT])
        ami_search.use_dictionaries([AmiDictionaries.NMR])
        ami_search.use_projects([AmiProjects.WORC_EXPLOSION, AmiProjects.WORC_SYNTH])

        ami_search.use_pattern("^[A-Z]{1,}[^\s]*\d{1,}$", "AB12")
        ami_search.use_pattern("_ALLCAPS", "all_capz")
        ami_search.use_pattern("_ALL", "_all")

        ami_search.run_search()

    @staticmethod
    def word_demo():
        ami_search = AmiSearch()
        ami_search.min_hits = 2

        ami_search.use_sections([AmiSection.METHOD])
        ami_search.use_projects([AmiProjects.WORC_EXPLOSION, AmiProjects.WORC_SYNTH])

        ami_search.use_pattern("^[A-Z]{1,}[^\s]*\d{1,}$", "AB12")
        ami_search.use_pattern("_ALLCAPS", "all_capz")
        ami_search.use_pattern("_ALL", "_all")

        ami_search.run_search()

    def run_args(self):
        import argparse
        import sys
        local_test = False  # interactive debug
        parser = create_arg_parser()
        args = parser.parse_args()
        print("args", args)
        print("cmd", "sys.argv", sys.argv)
        print("interpreted from cmd", "arg.demo", args.demo)
        #    local_test = True
        if args.debug == "config":
            ami_runs = AmiRunner();
            ami_runs.read_config(AmiSearch.DEMOS_JSON)
        elif len(sys.argv) == 1:
            print(parser.print_help(sys.stderr))
        elif args.demo is not None:
            print("DEMOS")
            AmiSearch.run_demos(args.demo)
        else:
#            ami_search = AmiSearch()
#            copy_args_to_ami_search(args, ami_search)
#            if ami_search.do_search:
#                ami_search.run_search()
            copy_args_to_ami_search(args, self)
            if self.do_search:
                self.run_search()

        # this profiles it
        #    test_profile1()
        print("finished search")

    def run_search_from_gui(self, ami_gui):
        self.min_hits = 1
        self.max_bars = 200

        sections = Gutil.get_selections_from_listbox(ami_gui.sections_listbox)
        print("sections", sections)
        self.use_sections(sections)

        dictionaries = Gutil.get_selections_from_listbox(ami_gui.dictionary_names_listbox)
        print("dictionaries",dictionaries)
        self.use_dictionaries(dictionaries)

        projects = Gutil.get_selections_from_listbox(ami_gui.project_names_listbox)
        print("projects",projects)
        self.use_projects(projects)

        self.run_search()


class AmiRun:

    SECTIONS = "sections"
    DICTIONARIES = "dictionaries"
    PROJECTS = "projects"
    PATTERNS = "patterns"
    DEFAULTS = "defaults"

    def __init__(self, params, ami_runner):
        print("AMIRUNNER", dir(ami_runner))
        self.params = params
        self.sections = self._copy_params(__class__.SECTIONS)
        self.ami_sections = AmiSection()
        self.dictionaries = self._copy_params(__class__.DICTIONARIES)
        self.ami_dictionaries = AmiDictionaries()
        self.projects = self._copy_params(__class__.PROJECTS)
        self.ami_projects = AmiProjects()
        self.patterns = self._copy_params(__class__.PATTERNS)
# copying defaults to be partially overridden
        self.defalts = ami_runner.resources[__class__.DEFAULTS]
        self.ami_runner = ami_runner

        print("defaults", self.defalts)
        print("sections", self.sections)
        print("dictionaries", self.dictionaries)
        print("projects", self.projects)
        print("patterns", self.patterns)

        return

    def _copy_params(self, type):
        return self.params[type] if type in self.params else []

    def resolve_refs(self):

        for section in self.sections:
            if section not in self.ami_sections.SECTION_LIST:
                print("sectionsx ", section, "not in", self.ami_sections.SECTION_LIST)

        for dictionary in self.dictionaries:
            if not dictionary in self.ami_dictionaries.dictionary_dict:
                print("Cannot find dictionary:", dictionary, "\n", self.ami_dictionaries.dictionary_dict)

        for defalt in self.defalts.items():
            print("def", defalt)
            self.__setattr__(defalt[0], defalt[1])
        print("attrs", dir(self))

        # check section_names


class AmiRunner:

    RESOURCES = "resources"
    PROJECTS = "projects"
    CLASSES = "classes"
    PATTERNS = "patterns"
    DEFAULTS = "defaults"
    DEMOS = "demos"


    def __init__(self):
        self.runs = {}
        self.ami_dicts = AmiDictionaries()

    def read_config(self, file):
        print("reading JSON", file)
        with open(file, "r") as json_file:
            data = json.load(json_file)

        self.resources = data[__class__.RESOURCES]
        print("RES keys", self.resources.keys())
        self.classes   = self.resources[__class__.CLASSES]
        self.projects  = self.resources[__class__.PROJECTS]
        self.patterns  = self.resources[__class__.PATTERNS]
        self.defalts  = self.resources[__class__.DEFAULTS]
        self.demos     = data[__class__.DEMOS]

        print("resources", self.resources)
        print("classes", self.classes)
        print("projects", self.projects)
        print("patterns", self.patterns)
        print("defaults", self.defalts)
        print("demos", self.demos)

        for key, val in self.demos.items():
            print("======"+key+"======")
            ami_run = AmiRun(val, self)
            self.runs[key] = ami_run
            ami_run.resolve_refs()
            print("===================")

        print("json", data)


class SimpleDict:

    def __init__(self, file=None):
        if file:
            with open(file, "r", encoding="utf-8") as f:
                self.lines = f.read().splitlines()
        print(self.lines)


class AmiProjects:
    """project files"""
    CCT    = "cct"
    DIFFPROT = "diffprot"
    DISEASE = "disease"
    FFML = "ffml"
    FFML20 = "ffml20"
    LIION10 = "liion10"
    OIL186 = "oil186"
    OIL26 = "oil26"
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
        # in this repo
        self.add_with_check(AmiProjects.LIION10, os.path.join(PHYSCHEM_RESOURCES, "liion10"), "Li-ion batteries")
        self.add_with_check(AmiProjects.FFML20, os.path.join(DIAGRAMS_DIR, "luke", "ffml20"), "forcefields + ML")
        self.add_with_check(AmiProjects.OIL26, os.path.join(PHYSCHEM_RESOURCES, "oil26"), "26 oil plant papers")
        self.add_with_check(AmiProjects.CCT, os.path.join(DIAGRAMS_DIR, "satish", "cct"), "steel cooling curves"),
        self.add_with_check(AmiProjects.DIFFPROT, os.path.join(DIAGRAMS_DIR, "rahul", "diffprotexp"),
                            "differential protein expression")
        # foreign resources
        self.add_with_check(AmiProjects.DISEASE, os.path.join(MINIPROJ, "disease", "1-part"), "disease papers")
        self.add_with_check(AmiProjects.OIL186, os.path.join(PROJECTS, "CEVOpen/searches/oil186"), "186 oil plant papers")
        self.add_with_check(AmiProjects.WORC_SYNTH, os.path.join(PROJECTS, "worcester", "synthesis"), "chemical syntheses")
        self.add_with_check(AmiProjects.WORC_EXPLOSION, os.path.join(PROJECTS, "worcester", "explosion"), "explosion hazards")

        # minicorpora
        self.add_with_check(AmiProjects.C_ACTIVITY, os.path.join(MINICORPORA, "activity"), "biomedical activities")
        self.add_with_check(AmiProjects.C_HYDRODISTIL, os.path.join(MINICORPORA, "hydrodistil"), "hydrodistillation")
        self.add_with_check(AmiProjects.C_INVASIVE, os.path.join(MINICORPORA, "invasive"), "invasive plants")
        self.add_with_check(AmiProjects.C_PLANT_PART, os.path.join(MINICORPORA, "plantpart"), "plant parts")


    def add_with_check(self, key, file, desc=None):
        """checks for existence and adds filename to project_dict
        key: unique name for ami_dict , default ami_dict in AmiProjects"""
        if not os.path.isdir(file):
            print("project files not available for ", file)
            return
        Util.check_exists(file)
        if key in self.project_dict:
            raise Exception (str(key) + " already exists in project_dict,  must be unique")
        self.project_dict[key] = AmiProject(file, desc)

class AmiProject:
    def __init__(self, dir, desc=None):
        self.dir = dir
        self.description = desc

class SearchPattern:

    """ holds a regex or other pattern constraint (e.g. isnumeric) """
    REGEX = "_REGEX"

    _ALL = "_ALL"
    ALL_CAPS = "_ALLCAPS"
    NUMBER = "_NUMBER"
    SPECIES = "_SPECIES"
    GENE = "_GENE"
    PATTERNS = [
        _ALL,
        ALL_CAPS,
#        GENE,
        NUMBER,
#        SPECIES,
    ]

    def __init__(self, value, name=None):
        if value in SearchPattern.PATTERNS:
            self.type = value
            self.regex = None
            self.name = value if name is None else value
        else:
            self.type = SearchPattern.REGEX
            self.regex = re.compile(value)
            self.name = name if name is not None else "regex:"+value
            print("PATT: ", name, value)

    def match(self, words):
        matched_words = []
        for word in words:
            matched = False
            if self.regex:
                matched = self.regex.match(word)
            elif SearchPattern._ALL == self.type:
                matched = True      # pass everything
            elif SearchPattern.ALL_CAPS == self.type:
                matched = str.isupper(word)
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
        self.amidict = ET.parse(file, parser=ET.XMLParser(encoding="utf-8"))
        self.root = self.amidict.getroot()
        self.name = self.root.attrib["title"]
        self.ignorecase = ignorecase

        self.entries = list(self.root.findall("entry"))
        self.create_entry_by_term();
        self.term_set = set()
#        print("read dictionary", self.name, "with", len(self.entries), "entries")

    def get_or_create_term_set(self):
        if len(self.term_set) == 0:
            for entry in self.entries:
                if SearchDictionary.TERM in entry.attrib:
                    term = self.term_from_entry(entry)
#                    print("tterm", term)
                    # single word terms
                    if not " " in term:
                        self.add_processed_term(term)
                    elif self.split_terms:
                        # multiword terms
                        for termx in term.split(" "):
#                            print("term", termx)
                            self.add_processed_term(termx)

        #            print(len(self.term_set), list(sorted(self.term_set)))
        #        print ("terms", len(self.term_set))
        return self.term_set

    def get_or_create_multiword_terms(self):
        return
        """NYI"""
        if len(self.multiwords) == 0:
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
        self.term_set = self.get_or_create_term_set()
        for target_word in target_words:
            target_word = target_word.lower()
            if target_word in self.term_set:
                matched.append(target_word)
        return matched

    def match_multiple(self, target_words):
        """this will be slow with large dictionaries until we optimise the algorithm """
        matched = []
        self.get_or_create_multiword_terms()
        for target_word in target_words:
            target_word = target_word.lower()
            if target_word in self.term_set:
                matched.append(target_word)
        return matched

    def get_entry(self, term):
        return self.entry_by_term[term] if term in self.entry_by_term else None

    def create_entry_by_term(self):
        self.entry_by_term = {self.term_from_entry(entry) : entry  for entry in self.entries}


class AmiDictionaries:

    ACTIVITY = "activity"
    COMPOUND = "compound"
    COUNTRY = "country"
    DISEASE = "disease"
    ELEMENT = "elements"
    INVASIVE_PLANT = "invasive_plant"
    PLANT_GENUS = "plant_genus"
    ORGANIZATION = "organization"
    PLANT_COMPOUND = "plant_compound"
    PLANT = "plant"
    PLANT_PART = "plant_part"
    SOLVENT = "solvents"

    ANIMAL_TEST = "animaltest"
    COCHRANE = "cochrane"
    COMP_CHEM = "compchem"
    CRISPR = "crispr"
    CRYSTAL = "crystal"
    DISTRIBUTION = "distributions"
    DITERPENE = "diterpene"
    DRUG = "drugs"
    EDGE_MAMMAL = "edgemammals"
    CHEM_ELEMENT = "elements"
    EPIDEMIC = "epidemic"
    ETHICS = "ethics"
    EUROFUNDER = "eurofunders"
    ILLEGAL_DRUG = "illegaldrugs"
    INN = "inn"
    INSECTICIDE = "insecticide"
    MAGNETISM = "magnetism"
    MONOTERPENE = "monoterpene"
    NAL = "nal"
    NMR = "nmrspectroscopy"
    OBESITY = "obesity"
    OPTOGENETICS = "optogenetics"
    PECTIN = "pectin"
    PHOTOSYNTH = "photosynth"
    PLANT_DEV = "plantDevelopment"
    POVERTY = "poverty"
    PROT_STRUCT = "proteinstruct"
    PROT_PRED = "protpredict"
    REFUGEE = "refugeeUNHCR"
    SESQUITERPENE = "sesquiterpene"
    SOLVENT = "solvents"
    STATISTICS = "statistics"
    TROPICAL_VIRUS = "tropicalVirus"
    WETLANDS = "wetlands"
    WILDLIFE = "wildlife"

    def __init__(self):
        self.create_search_dictionary_dict()

    def create_search_dictionary_dict(self):
        self.dictionary_dict = {}

#        / Users / pm286 / projects / CEVOpen / dictionary / eoActivity / eo_activity / Activity.xml
        self.add_with_check(AmiDictionaries.ACTIVITY,
                            os.path.join(CEV_OPEN_DICT_DIR, "eoActivity", "eo_activity", "activity.xml"))
        self.add_with_check(AmiDictionaries.COUNTRY,
                            os.path.join(OV21_DIR, "country", "country.xml"))
        self.add_with_check(AmiDictionaries.DISEASE,
                            os.path.join(OV21_DIR, "disease", "disease.xml"))
        self.add_with_check(AmiDictionaries.COMPOUND,
                            os.path.join(CEV_OPEN_DICT_DIR, "eoCompound", "plant_compound.xml"))
        self.add_with_check(AmiDictionaries.PLANT,
                            os.path.join(CEV_OPEN_DICT_DIR, "eoPlant", "plant.xml"))
        self.add_with_check(AmiDictionaries.PLANT_GENUS,
                            os.path.join(CEV_OPEN_DICT_DIR, "plant_genus", "plant_genus.xml"))
        self.add_with_check(AmiDictionaries.ORGANIZATION,
                            os.path.join(OV21_DIR, "organization", "organization.xml"))
        self.add_with_check(AmiDictionaries.PLANT_COMPOUND,
                            os.path.join(CEV_OPEN_DICT_DIR, "eoCompound", "plant_compound.xml"))
        self.add_with_check(AmiDictionaries.PLANT_PART,
                            os.path.join(CEV_OPEN_DICT_DIR, "eoPlantPart", "eoplant_part.xml"))
        self.add_with_check(AmiDictionaries.INVASIVE_PLANT,
                            os.path.join(CEV_OPEN_DICT_DIR, "Invasive_species", "invasive_plant.xml"))

        self.make_ami3_dictionaries()

# tests - will remove as soon as I have learnt how to do tests
        fail_test = False
        if fail_test:
            self.add_with_check("junk", "none") # should throw missing file
            self.add_with_check(AmiDictionaries.PLANT_PART,
                    os.path.join(CEV_OPEN_DICT_DIR, "eoPlantPart", "eoplant_part.xml"))  # should throw duplicate key

#        self.print_dicts()
        return self.dictionary_dict

    def print_dicts(self):
        print("DICTIONARIES LOADED")
        dd = dir(self)
        for d in dd:
            if d[0].isupper():
                print(">>", d)

    def make_ami3_dictionaries(self):

        self.ami3_dict_index = {
            AmiDictionaries.ANIMAL_TEST : os.path.join(DICT_AMI3, "animaltest.xml"),
            AmiDictionaries.COCHRANE : os.path.join(DICT_AMI3, "cochrane.xml"),
            AmiDictionaries.COMP_CHEM : os.path.join(DICT_AMI3, "compchem.xml"),
            AmiDictionaries.CRISPR : os.path.join(DICT_AMI3, "crispr.xml"),
            AmiDictionaries.CRYSTAL : os.path.join(DICT_AMI3, "crystal.xml"),
            AmiDictionaries.DISTRIBUTION : os.path.join(DICT_AMI3, "distributions.xml"),
            AmiDictionaries.DITERPENE : os.path.join(DICT_AMI3, "diterpene.xml"),
            AmiDictionaries.DRUG : os.path.join(DICT_AMI3, "drugs.xml"),
            AmiDictionaries.EDGE_MAMMAL : os.path.join(DICT_AMI3, "edgemammals.xml"),
            AmiDictionaries.ETHICS : os.path.join(DICT_AMI3, "ethics.xml"),
            AmiDictionaries.CHEM_ELEMENT : os.path.join(DICT_AMI3, "elements.xml"),
            AmiDictionaries.EPIDEMIC : os.path.join(DICT_AMI3, "epidemic.xml"),
            AmiDictionaries.EUROFUNDER: os.path.join(DICT_AMI3, "eurofunders.xml"),
            AmiDictionaries.ILLEGAL_DRUG : os.path.join(DICT_AMI3, "illegaldrugs.xml"),
            AmiDictionaries.INN : os.path.join(DICT_AMI3, "inn.xml"),
            AmiDictionaries.INSECTICIDE : os.path.join(DICT_AMI3, "insecticide.xml"),
            AmiDictionaries.MAGNETISM : os.path.join(DICT_AMI3, "magnetism.xml"),
            AmiDictionaries.MONOTERPENE : os.path.join(DICT_AMI3, "monoterpene.xml"),
            AmiDictionaries.NAL : os.path.join(DICT_AMI3, "nal.xml"),
            AmiDictionaries.NMR : os.path.join(DICT_AMI3, "nmrspectroscopy.xml"),
            AmiDictionaries.OBESITY : os.path.join(DICT_AMI3, "obesity.xml"),
            AmiDictionaries.OPTOGENETICS : os.path.join(DICT_AMI3, "optogenetics.xml"),
            AmiDictionaries.PECTIN : os.path.join(DICT_AMI3, "pectin.xml"),
            AmiDictionaries.PHOTOSYNTH : os.path.join(DICT_AMI3, "photosynth.xml"),
            AmiDictionaries.PLANT_DEV : os.path.join(DICT_AMI3, "plantDevelopment.xml"),
            AmiDictionaries.POVERTY : os.path.join(DICT_AMI3, "poverty.xml"),
            AmiDictionaries.PROT_STRUCT : os.path.join(DICT_AMI3, "proteinstruct.xml"),
            AmiDictionaries.PROT_PRED : os.path.join(DICT_AMI3, "protpredict.xml"),
            AmiDictionaries.REFUGEE : os.path.join(DICT_AMI3, "refugeeUNHCR.xml"),
            AmiDictionaries.SESQUITERPENE : os.path.join(DICT_AMI3, "sesquiterpene.xml"),
            AmiDictionaries.SOLVENT : os.path.join(DICT_AMI3, "solvents.xml"),
            AmiDictionaries.STATISTICS : os.path.join(DICT_AMI3, "statistics.xml"),
            AmiDictionaries.TROPICAL_VIRUS : os.path.join(DICT_AMI3, "tropicalVirus.xml"),
            AmiDictionaries.WETLANDS : os.path.join(DICT_AMI3, "wetlands.xml"),
            AmiDictionaries.WILDLIFE : os.path.join(DICT_AMI3, "wildlife.xml"),
        }

        for item in self.ami3_dict_index.items():
            self.add_with_check(item[0], item[1])


    def add_with_check(self, key, file):
#        print("adding dictionary", file)
        if key in self.dictionary_dict:
            raise Exception("duplicate dictionary key " + key + " in "+ str(self.dictionary_dict))
        Util.check_exists(file)
        try:
            dictionary = SearchDictionary(file)
            self.dictionary_dict[key] = dictionary
        except Exception as ex:
            print("Failed to read dictionary", file, ex)
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
    ami_search = AmiSearch()
    ami_search.run_args()



def create_arg_parser():
    import argparse
    parser = argparse.ArgumentParser(description='Search sections with dictionaries and patterns')
    """
    """
    parser.add_argument('-d', '--dict', nargs="*",  # default=[AmiDictionaries.COUNTRY],
                        help='dictionaries to search with, empty gives list')
    parser.add_argument('-s', '--sect', nargs="*",  # default=[AmiSection.INTRO, AmiSection.RESULTS],
                        help='sections to search; empty gives all')
    parser.add_argument('-p', '--proj', nargs="*",
                        help='projects to search; empty will give list')
    parser.add_argument('--patt', nargs="+",
                        help='patterns to search with; regex may need quoting')
    parser.add_argument('--demo', nargs="*",
                        help='simple demos (NYI). empty gives list. May need downloading corpora')
    parser.add_argument('-l', '--loglevel', default="foo",
                        help='debug level (NYI)')
    parser.add_argument('--plot', action="store_false",
                        help='plot params (NYI)')
    parser.add_argument('--nosearch', action="store_true",
                        help='search (NYI)')
    parser.add_argument('--maxbars', nargs="?", type=int, default=25,
                        help='max bars on plot (NYI)')
    parser.add_argument('--languages', nargs="+", default=["en"],
                        help='languages (NYI)')
    parser.add_argument('--debug', nargs="+",
                        help='debugging commands , numbers, (not formalised)')
    return parser


def copy_args_to_ami_search(args, ami_search):
    print_args(args)
    # TODO dict on keywords
    ami_search.use_sections(args.sect)
    ami_search.use_dictionaries(args.dict)
    ami_search.use_projects(args.proj)
    ami_search.use_patterns(args.patt)
    if args.maxbars:
        ami_search.max_bars = args.maxbars
    if args.languages:
        ami_search.languages = args.languages
    for k, v in vars(args).items():
#        print("k, v", k, "=", v)
        pass
    return ami_search


def print_args(args):
    print("commandline args")
    print("dicts", args.dict, type(args.dict))
    print("sects", args.sect, type(args.sect))
    print("projs", args.proj, type(args.proj))
    print("patterns", args.patt, type(args.patt))
    print("args>", args)


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