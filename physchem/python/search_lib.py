# https://stackoverflow.com/questions/19917492/how-can-i-use-a-python-script-in-the-command-line-without-cd-ing-to-its-director

from file_lib import AmiPath, PROJ
from text_lib import TextUtil, AmiSection
from xml_lib import XmlLib
#from xml.etree import ElementTree as ET
from collections import Counter
import re
import json
from gutil import Gutil
from dictionary import AmiDictionaries, SearchDictionary
from projects import AmiProjects

# entry
WIKIDATA_ID = "wikidataID"
NS_MAP = {'SPQ': 'http://www.w3.org/2005/sparql-results#'}  # add more as needed
NS_URI = "SPQ:uri"
NS_LITERAL = "SPQ:literal"

class AmiSearch:


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

        self.param_dict = {
            "max_bars" : 10,
            "wikidata_label_lang" : "en",
            "debug_cnt" : 10000,
            "max_files" : 10000,
            "min_hits" : 2,
            "require_wikidata" : False,
            "ami_gui" : None,
        }
#        self.max_bars = 10
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
        self.ami_gui = None

    def make_graph(self, counter, dict_name):
        import matplotlib as mpl
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

        return matches_by_amidict, matches_by_pattern, words

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
                if self.require_wikidata and WIKIDATA_ID not in entry.attrib:
                    print("no wikidataID for ", hit, "in", dictionary.name)
                    continue
#                wikidata_id = entry.attrib[WIKIDATA_ID]
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

        all_lower_words = []
        for index, target_file in enumerate(section_files[:self.max_files]):

            if index % self.debug_cnt == 0:
                print("file", target_file)
            matches_by_amidict, matches_by_pattern, words = self.search(target_file)
            all_lower_words += [w.lower() for w in words]
            self.add_matches_to_counter_dict(dictionary_counter_dict, matches_by_amidict)
            self.add_matches_to_counter_dict(pattern_counter_dict, matches_by_pattern)

        return dictionary_counter_dict, pattern_counter_dict, all_lower_words

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
                self.glob_for_section_files(proj, section_type)
                self.make_counter_and_plot()
                self.extract_keywords()


    def glob_for_section_files(self, proj, section_type):
        self.cur_section_type = section_type
        templates = AmiPath.create_ami_path_from_templates(section_type, {PROJ: proj.dir})
        self.section_files = templates.get_globbed_files()
        print("***** section_files", section_type, len(self.section_files))


    def make_counter_and_plot(self):
        counter_by_tool, pattern_dict, all_words = self.search_and_count(self.section_files)
        self.plot_tool_hits(counter_by_tool)
        self.plot_tool_hits(pattern_dict)
        self.analyze_all_words(all_words)

    def analyze_all_words(self, all_words):
        print(all_words)
        counter = Counter(all_words)
        self.plot_and_make_dictionary(counter, "ALL")
        rake = AmiRake()
        wordz = " ".join(all_words)
        print(wordz)
        rake.analyze_text_with_RAKE(wordz)

    def extract_keywords(self):
        pass

    def plot_tool_hits(self, counter_by_tool):
        for tool in counter_by_tool:
            counter = counter_by_tool[tool]
            self.plot_and_make_dictionary(counter, tool)

    def plot_and_make_dictionary(self, counter, tool):
        min_counter = Counter({k: c for k, c in counter.items() if c >= self.min_hits})
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

        outfile = self.create_word_count_file(tool)
        """ TODO
        with open(outfile, "w") as f:
            print("<dictionary title='" + tool + "'>")
            for k, v in counter.items():
                if v > self.min_hits:
                    print("  <entry term=`" + k.lower() + "'/>")
            print("</dictionary>")
        """

    def create_word_count_file(self, tool):
        pass

    def run_args(self):
        import sys
        from ami_demos import AmiDemos
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
            AmiDemos.run_demos(args.demo)
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
        self.max_bars = 25
        self.ami_gui = ami_gui

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

class AmiRake:
    def __init__(self):
        pass

    def test(self):
        with open("test/materials.txt") as f:
            text = f.read()
        self.analyze_text_with_RAKE(text)

    def analyze_text_with_RAKE(self, text):
        from rake_nltk import Rake
        import RAKE

        stop_dir =  "./SmartStoplist.txt"
        rake_object = RAKE.Rake(stop_dir)
        keywords = self.sort_tuple(rake_object.run(text))  # [-10:]
        print("keywords", keywords)
        rake = Rake()
        keywords = rake.extract_keywords_from_text(text)
        print("keywords", keywords)
        phrases = rake.get_ranked_phrases()  # [0:100]
        print("phrases", phrases)

    def sort_tuple(self, tup):
        """ sort
        :reverse: None sort in ascending order
        uses second elements of sublist as sort key
        """
        tup.sort(key = lambda x: x[1])
        return tup

def test_profile():
    import cProfile
    print("profile")
    cProfile.run("[x for x in range(1500)]")

def test_profile1():
    import cProfile
    print("profile1")
    cProfile.run("AmiSearch.test_sect_dicts()")



def main():
    """ debugging """
    option = "search" # edit this
#    option = "sparql"
    option = "rake"
    if 1 == 2:
        pass
    elif option == "rake":
        AmiRake().test()
    elif option == "search":
        ami_search = AmiSearch()
        ami_search.run_args()
    elif option == "test":
        test = AmiRake()
        test.test()
    elif option == "sparql":
        SearchDictionary.test()
    else:
        print("no option given")

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