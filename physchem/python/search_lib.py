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

HOME = os.path.expanduser("~")
PYDIAG = "../../python/diagrams"
#LIION = "../liion"
DICT_DIR = os.path.join(HOME, "dictionary")

OV21_DIR = os.path.join(DICT_DIR, "openVirus20210120")
CEV_DICT_DIR = os.path.join(DICT_DIR, "cevopen")
PMR_DIR = os.path.join(DICT_DIR, "pmr")

PROJECTS = os.path.join(HOME, "projects")

OPEN_DIAGRAM = os.path.join(PROJECTS, "openDiagram")
OPEN_DIAGRAM_SEARCH = os.path.join(OPEN_DIAGRAM, "searches")

PHYSCHEM = os.path.join(OPEN_DIAGRAM, "physchem")
PHYSCHEM_RESOURCES = os.path.join(PHYSCHEM, "resources")
DIAGRAMS_DIR = os.path.join(PROJECTS, "openDiagram", "python", "diagrams")
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
        self.section_types = []
        self.word_counter = None
        self.debug = False
        self.do_search = True
        self.do_plot = True
        self.ami_projects = AmiProjects()
        self.cur_section_type = None
#        self.cur_dict = None
        self.cur_proj = None
        self.max_bars = 20
        self.wikidata_label_lang = "en"

        # print every debug_cnt filenamwe
        self.debug_cnt = 10000
        # maximum files to search
        self.max_files = 10000
        self.min_hits = 1
        self.require_wikidata = False

        # look up how sections work
#        self.ami_sections = AmiSections()
        self.ami_dictionaries = AmiDictionaries()

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
            print("amidict keys: ", AmiDictionaries.DICT_LIST)

    def add_dictionary(self, name):
        print("name", name)
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
        if args is None or len(args) == 0:
            print("must give projects; here are some to test with")
            print(AmiProjects().project_dict.keys())
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
        matches_by_amidict = self.match_words_against_dictionaries(words)
        matches_by_pattern = self.match_words_against_pattern(words)

        return matches_by_amidict, matches_by_pattern

    def match_words_against_dictionaries(self, words):
        matches_by_amidict = {}
        found = False
        for dictionary in self.dictionaries:
            hits = dictionary.match(words)
#            print("hits", len(hits))
            if dictionary.entry_by_term is not None:
                wid_hits = self.annotate_hits_with_wikidata(dictionary, hits)
            matches_by_amidict[dictionary.name] = wid_hits
        return matches_by_amidict

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
        if len(sections) == 0:
            self.section_help()
        else:
            AmiSection.check_sections(sections)
            self.section_types = sections

    def section_help(self):
        print("sections to be used; ALL uses whole document (Not yet tested)")
        print(AmiSection.SECTION_LIST)

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
            print("lang:", self.wikidata_label_lang, "\n", min_counter.most_common())

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
            AmiDictionaries.PLANT_COMPOUND,
            AmiDictionaries.PLANT_PART,
            AmiDictionaries.PLANT_GENUS,

#            AmiDictionaries.PLANT,
#            AmiDictionaries.PLANT_PART,

#            AmiDictionaries.GENUS,
#            AmiDictionaries.ELEMENT,
#            AmiDictionaries.SOLVENT,
        ])
        ami_search.use_projects([
#            AmiProjects.OIL26,
            AmiProjects.OIL186,
#            AmiProjects.CCT,
#            AmiProjects.DIFFPROT,
#            AmiProjects.WORC_EXPLOSION,
#            AmiProjects.WORC_SYNTH,

            # minipprjects
#            AmiProjects.C_ACTIVITY,
#            AmiProjects.C_INVASIVE,
#            AmiProjects.C_HYDRODISTIL,
#            AmiProjects.C_PLANT_PART,
        ])
        ami_search.use_filters([
            WordFilter.ORG_STOP
        ])

#        ami_search.add_regex("abb_genus", "^[A-Z]\.$")
#        ami_search.add_regex("all_caps", "^[A-Z]{3,}$")
#        ami_search.use_pattern("^[A-Z]{1,}\d{1,}$", "AB12")
#        ami_search.use_pattern("_ALLCAPS", "all_capz")
#        ami_search.use_pattern("_NUMBERS", "numberz")

        if ami_search.do_search:
            ami_search.run_search()

#    def add_regex(self, name, regex):
#        self.patterns.append(SearchPattern(name, SearchPattern.REGEX, regex))

    @staticmethod
    def ethics_demo():
        ami_search = AmiSearch()
        ami_search.min_hits = 2

        ami_search.use_sections([AmiSection.ETHICS, ])
        ami_search.use_dictionaries([AmiDictionaries.COUNTRY, AmiDictionaries.DISEASE, ])
        ami_search.use_projects([AmiProjects.DISEASE, ])
        ami_search.use_filters([WordFilter.ORG_STOP])

        ami_search.use_pattern("^[A-Z]{1,}[^\s]*\d{1,}$", "AB12")
        ami_search.use_pattern("_ALLCAPS", "all_capz")
        ami_search.use_pattern("_ALL", "_all")

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



class SimpleDict:

    def __init__(self, file=None):
        if file:
            with open(file, "r", encoding="utf-8") as f:
                self.lines = f.read().splitlines()
        print(self.lines)


class AmiProjects:
    """project files"""
    LIION10 = "liion10"
    FFML = "ffml"
    FFML20 = "ffml20"
    OIL186 = "oil186"
    OIL26 = "oil26"
    CCT    = "cct"
    DISEASE = "disease"
    DIFFPROT    = "diffprot"
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
        self.add_with_check(AmiProjects.FFML20, os.path.join(DIAGRAMS_DIR, "luke", "ffml20"))
        self.add_with_check(AmiProjects.OIL26, os.path.join(PHYSCHEM_RESOURCES, "oil26"))
        self.add_with_check(AmiProjects.OIL186, os.path.join(PROJECTS, "CEVOpen/searches/oil186"))
        self.add_with_check(AmiProjects.CCT, os.path.join(PROJECTS, "openDiagram/python/diagrams/satish/cct"))
        self.add_with_check(AmiProjects.DISEASE, os.path.join(MINIPROJ, "disease", "1-part"))
        self.add_with_check(AmiProjects.DIFFPROT, os.path.join(PROJECTS, "openDiagram/python/diagrams/rahul/diffprotexp"))
        self.add_with_check(AmiProjects.WORC_SYNTH, os.path.join(PROJECTS, "worcester", "synthesis"))
        self.add_with_check(AmiProjects.WORC_EXPLOSION, os.path.join(PROJECTS, "worcester", "explosion"))

        # minicorpora
        self.add_with_check(AmiProjects.C_ACTIVITY, os.path.join(MINICORPORA, "activity"))
        self.add_with_check(AmiProjects.C_HYDRODISTIL, os.path.join(MINICORPORA, "hydrodistil"))
        self.add_with_check(AmiProjects.C_INVASIVE, os.path.join(MINICORPORA, "invasive"))
        self.add_with_check(AmiProjects.C_PLANT_PART, os.path.join(MINICORPORA, "plantpart"))


    def add_with_check(self, key, file):
        """checks for existence and adds filename to project_dict
        key: unique name for ami_dict , default ami_dict in AmiProjects"""
        if not os.path.isdir(file):
            print("project files not available for ", file)
            return
        Util.check_exists(file)
        if key in self.project_dict:
            raise Exception (str(key) + " already exists in project_dict,  must be unique")
        self.project_dict[key] = AmiProject(file)

class AmiProject:
    def __init__(self, dir):
        self.dir = dir

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
        self.amidict = ET.parse(file)
        self.root = self.amidict.getroot()
        self.name = self.root.attrib["title"]
        self.ignorecase = ignorecase
        self.entries = list(self.root.findall("entry"))
        self.create_entry_by_term();
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
    SOLVENT = "solvent"

    DICT_LIST = [
        ACTIVITY,
        COMPOUND,
        COUNTRY,
        DISEASE,
        ELEMENT,
        INVASIVE_PLANT,
        PLANT_GENUS,
        ORGANIZATION,
        PLANT,
        PLANT_COMPOUND,
        PLANT_PART,
        SOLVENT,
    ]

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

    @staticmethod
    def check_dicts(dicts):
        for dikt in dicts:
            if dikt not in SearchDictionary.DICT_LIST:
                print("allowed dictionaries", SearchDictionary.DICT_LIST)
                raise Exception ("unknown dictionary: ", dikt)

    def create_search_dictionary_dict(self):
        self.dictionary_dict = {}

        self.make_ami3_dictionaries()

#        / Users / pm286 / projects / CEVOpen / dictionary / eoActivity / eo_activity / Activity.xml
        self.add_with_check(AmiDictionaries.ACTIVITY,
                            os.path.join(CEV_OPEN_DICT_DIR, "eoActivity", "Activity.xml"))
        self.add_with_check(AmiDictionaries.COUNTRY,
                            os.path.join(OV21_DIR, "country", "country.xml"))
        self.add_with_check(AmiDictionaries.DISEASE,
                            os.path.join(OV21_DIR, "disease", "disease.xml"))
        self.add_with_check(AmiDictionaries.COMPOUND,
                            os.path.join(CEV_OPEN_DICT_DIR, "eoCompound", "plant_compound.xml"))
        # /Users/pm286/dictionary/cevopen/plant_genus/eo_plant_genus.xml
#        self.add_with_check(AmiDictionaries.PLANT,
#                            os.path.join(CEV_OPEN_DICT_DIR, "eoPlant", "eoPlant.xml"))
# latest dictionary
        self.add_with_check(AmiDictionaries.PLANT,
                            os.path.join(CEV_OPEN_DICT_DIR, "eoPlant", "Plant.xml"))
        self.add_with_check(AmiDictionaries.PLANT_GENUS,
                            os.path.join(CEV_OPEN_DICT_DIR, "plant_genus", "plant_genus.xml"))
        self.add_with_check(AmiDictionaries.ORGANIZATION,
                            os.path.join(OV21_DIR, "organization", "organization.xml"))
#        / Users / pm286 / projects / CEVOpen / dictionary / eoCompound / plant_compounds.xml
        self.add_with_check(AmiDictionaries.PLANT_COMPOUND,
                            os.path.join(CEV_OPEN_DICT_DIR, "eoCompound", "plant_compound.xml"))
        # /Users/pm286/projects/CEVOpen/dictionary/eoPlantPart/eoplant_part.xml
        self.add_with_check(AmiDictionaries.PLANT_PART,
                            os.path.join(CEV_OPEN_DICT_DIR, "eoPlantPart", "eoplant_part.xml"))
#        self.add_with_check(AmiDictionaries.PLANT,
#                            os.path.join(CEV_OPEN_DICT_DIR, "eoPlant", "eoPlant", "Plant.xml"))
# invasive / Users / pm286 / projects / CEVOpen / dictionary / Invasive_species / invasive_species.xml
        self.add_with_check(AmiDictionaries.INVASIVE_PLANT,
                            os.path.join(CEV_OPEN_DICT_DIR, "Invasive_species", "invasive_species.xml"))

        print ("core dicts", self.dictionary_dict.keys())
# tests - will remove as soon as I have learnt how to do tests
        fail_test = False
        if fail_test:
            self.add_with_check("junk", "none") # should throw missing file
            self.add_with_check(AmiDictionaries.PLANT_PART,
                    os.path.join(CEV_OPEN_DICT_DIR, "eoPlantPart", "eoplant_part.xml"))  # should throw duplicate key

        return self.dictionary_dict

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
        print("adding dictionary", file)
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
    import argparse

    parser = argparse.ArgumentParser(description='Search sections with dictionaries and patterns')
    """
    """
    parser.add_argument('--dict', nargs="*",
                        help='dictionaries to search with (lookup table from JSON (NYI); empty gives list')
    parser.add_argument('--sect', nargs="*",
                        help='sections to search; empty gives all (Not yet tested')
    parser.add_argument('--proj', nargs="*",
                        help='projects to search; empty will give list')
    parser.add_argument('--patt', nargs="+",
                        help='patterns to search with; regex may need quoting')

    args = parser.parse_args()
    if      args.dict is None \
        and args.sect is None \
        and args.proj is None \
        and args.patt is None \
        :
        print("DEMO")
        print(parser.print_help())
#        AmiSearch.ethics_demo()
#        AmiSearch.luke_demo()
#        AmiSearch.plant_parts_demo()
#        AmiSearch.worc_demo()
    else:
        print_args(args)
        # TODO dict on keywords
        ami_search = AmiSearch()
        ami_search.use_sections(args.sect)
        ami_search.use_dictionaries(args.dict)
        ami_search.use_projects(args.proj)
        ami_search.use_patterns(args.patt)

        if ami_search.do_search:
            ami_search.run_search()



# this profiles it
#    test_profile1()
    print("finished search")

def print_args(args):
    print("commandline args")
    print("dicts", args.dict, type(args.dict))
    print("sects", args.sect, type(args.sect))
    print("projs", args.proj, type(args.proj))
    print("patterns", args.patt, type(args.patt))


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