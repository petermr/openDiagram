import os, glob, copy, json

class Globber():

    def __init__(self, ami_path, recurse=True, cwd=None):
        self.ami_path = ami_path
        self.recurse = recurse
        self.cwd = os.getcwd() if cwd is None else cwd

    def get_globbed_files(self):
        files = []
        if self.ami_path:
            glob_list = self.ami_path.get_glob_string_list()
            for globb in glob_list:
                ff = glob.glob(globb, recursive=self.recurse)
                files.extend(ff)
        return files


# section keys
_DESC = "_DESC"
PROJ =    "PROJ"
TREE =    "TREE"
SECTS =   "SECTS"
SUBSECT = "SUBSECT"
SUBSUB =  "SUBSUB"
FILE =    "FILE"
SUFFIX =  "SUFFIX"

ALLOWED_SECTS = {_DESC, PROJ, TREE, SECTS, SUBSECT, SUBSUB, FILE, SUFFIX}

# wildcards
STARS    = "**"
STAR     = "*"

# suffixes
S_PDF = "pdf"
S_PNG = "png"
S_SVG = "svg"
S_TXT = "txt"
S_XML = "xml"

# markers for processing
_NULL = "_NULL"
_REQD = "_REQD"

# known section names
SVG        = "svg"
PDFIMAGES  = "pdfimages"
RESULTS    = "results"
SECTIONS   = "sections"

# subsects
IMAGE_STAR  = "image*"

# subsects
OCTREE  = "*octree"

# results
SEARCH   = "search"
WORD     = "word"
EMPTY    = "empty"

# files
FULLTEXT_PAGE = "fulltext-page*"
CHANNEL_STAR = "channel*"
RAW = "raw"



class AmiPath:
    # keys for file scheme templates
    T_FIGURES = "fig_captions"
    T_OCTREE = "octree"
    T_PDFIMAGES = "pdfimages"
    T_RESULTS = "results"
    T_SECTIONS = "sections"
    T_SVG = "svg"

    # dict
    def __init__(self, scheme=None):
        self.scheme = scheme

    def print_scheme(self):
        """for debugging and enlightenment"""
        if self.scheme is not None:
            for key in self.scheme:
                print(key, "=", self.scheme[key])
            print("")


    @staticmethod
    def create(key, edit_dict=None):
        """creates a new AmiPath object from selected template
        key: to template
        edit_dict: dictionary with values to edit in
        """
        if key is None or key not in TEMPLATES:
            print("key", key)
            raise Exception("no scheme for: ", key, "expected", TEMPLATES.keys())
        ami_path = AmiPath()
        # start with default template values
        ami_path.scheme = copy.deepcopy(TEMPLATES[key])
        if edit_dict:
            ami_path.edit_scheme(edit_dict)
        return ami_path

    def edit_scheme(self, edit_dict):
        """edits values in self.scheme using edit_dict"""
        for k, v in edit_dict.items():
            self.scheme[k] = v

    def permute_sets(self):
        self.scheme_list = []
        self.scheme_list.append(self.scheme)
        # if scheme has sets, expand them
        change = True
        while change:
            change = self.expand_sets()

    def expand_sets(self):
        """expands the sets in a scheme
        note: sets are held as lists in JSON

        a scheme with 2 sets of size n and m is
        expanded to n*m schemes covering all permutations
        of the set values

        self.scheme_list contains all the schemes

        returns True if any sets are expanded

        """
        change = False
        for scheme in self.scheme_list:
            for sect, value in scheme.items():
                if type(value) == set:
                    change = True
                    self.scheme_list.remove(scheme) # delete scheme with set, replace by copies
                    for set_value in value:
                        scheme_copy = copy.deepcopy(scheme)
                        self.scheme_list.append(scheme_copy)
                        scheme_copy[sect] = set_value # poke in set value
                    break # after each set processed

        return change

    def get_glob_string_list(self):
        """expand sets in AmiPath
        creates m*n... glob strings for sets with len n and m
        """
        self.permute_sets()
        self.glob_string_list = []
        for scheme in self.scheme_list:
            glob_string = AmiPath.create_glob_string(scheme)
            self.glob_string_list.append(glob_string)
        return self.glob_string_list

    @staticmethod
    def create_glob_string(scheme):
        glob = ""
        for sect, value in scheme.items():
#            print(sect, type(value), value)
            if sect not in ALLOWED_SECTS:
                print("unknown sect:", sect)
            elif _DESC == sect:
                pass
            elif _REQD == value:
                print("must set ", sect)
                glob += _REQD + "/"
            elif _NULL == value:
                pass
            elif FILE == sect:
                glob += AmiPath.wrap_value(value)
            elif STAR in value:
                glob += AmiPath.wrap_value(value) + "/"
            elif SUFFIX == sect:
                glob += "." + AmiPath.wrap_value(value)
            else:
                glob += AmiPath.wrap_value(value) + "/"
        print("glob", glob)
        return glob

    @staticmethod
    def wrap_value(value):
        valuex = value
        if type(value) == list:
            # tacky. string quotes and add commas and parens
            valuex = "("
            for v in value:
                valuex += v + ","
            valuex = valuex[:-1] + ")"
        return valuex

    def get_globbed_files(self):
        files = Globber(self).get_globbed_files()
        print("files", len(files))
        return files


"""
import os
import re

def glob_re(pattern, strings):
    return filter(re.compile(pattern).match, strings)

filenames = glob_re(r'.*(abc|123|a1b).*\.txt', os.listdir())


"""
ff = 'templates.json'
with open(ff, 'r') as json_file:
    TEMPLATES = json.load(json_file)

print (TEMPLATES)

def main():
    print("started file_lib")
    PYDIAG = "../../python/diagrams"
    CCT = PYDIAG + "/" + "satish/cct"
    print("PYDIAG", os.path.exists(PYDIAG), "SATISH", os.path.exists(CCT))
#    globbed_files = AmiPath.create(AmiPath.T_OCTREE, {PROJ: PYDIAG+"/"+"luke/papers20210121"}).get_globbed_files() # Zero?
#    globbed_files = AmiPath.create(AmiPath.T_SECTIONS, {PROJ: PYDIAG + "/" + "satish/cct"}).get_globbed_files() # Zero?
#    AmiPath.create(AmiPath.T_PDFIMAGES, {PROJ: "../liion"}).get_globbed_files()
#    AmiPath.create(AmiPath.T_RESULTS, {PROJ: "../liion"}).get_globbed_files()
#    AmiPath.create(AmiPath.T_SECTIONS, {PROJ: "../liion", SUBSECT: "*_body*", SUBSUB: "**", FILE: "*p", }).get_globbed_files()
    # tables
    globbed_files = AmiPath.create(AmiPath.T_SECTIONS, {PROJ: PYDIAG + "/" + "satish/cct", SUBSECT: "tables", SUBSUB: "**", FILE: "*table*", }).get_globbed_files()
#    AmiPath.create(AmiPath.T_SVG, {PROJ: "../liion"}).get_globbed_files()
    print (len(globbed_files), globbed_files[:5])
    for ami_path in [
        AmiPath.create("abstract", {PROJ: CCT}),
        AmiPath.create("acknowledge", {PROJ: CCT}),
        AmiPath.create("affiliation", {PROJ: CCT}),
        AmiPath.create("author", {PROJ: CCT}),
        AmiPath.create("fig_caption", {PROJ: CCT}),
        AmiPath.create("introduction", {PROJ: CCT}),
        AmiPath.create("jrnl_title", {PROJ: CCT}),
        AmiPath.create("keyword", {PROJ: CCT}),
        AmiPath.create("method", {PROJ: CCT}),
        AmiPath.create("octree", {PROJ: CCT}),
        AmiPath.create("pdfimage", {PROJ: CCT}),
        AmiPath.create("pub_date", {PROJ: CCT}),
        AmiPath.create("publisher", {PROJ: CCT}),
        AmiPath.create("reference", {PROJ: CCT}),
        AmiPath.create("results", {PROJ: CCT}),
        AmiPath.create("results_discuss", {PROJ: CCT}),
        AmiPath.create("svg", {PROJ: CCT}),
        AmiPath.create("table", {PROJ: CCT}),
        AmiPath.create("title", {PROJ: CCT}),
        ]:
        globbed_files = ami_path.get_globbed_files()
        print (len(globbed_files), globbed_files[:5])

    print("finished file_lib")

if __name__ == "__main__":
    print("running file_lib main")
    main()
else:
#    print("running file_lib main anyway")
#    main()
    pass

"""
TEMPLATES = {
    # rahul/rahul1/pdfimages/image.1.1.533_555.28_51/octree/channel.7b93c8.png
    AmiPath.T_OCTREE:    AmiPath.OCTREE_D,
    AmiPath.T_PDFIMAGES: AmiPath.PDFIMAGES_D,
    AmiPath.T_RESULTS:   AmiPath.RESULTS_D,
    # invasive / PMC3485296 / results / search / country / results.xml
    AmiPath.T_SECTIONS:  AmiPath.SECTIONS_D,
    AmiPath.T_SVG:       AmiPath.SVG_D,
}
print(type(TEMPLATES), type(AmiPath.T_OCTREE))
ff = 'templates.json'
with open(ff, 'w') as json_file:
    json.dump(TEMPLATES, json_file, indent=2)
"""

"""
    # scheme templates ; these contain default values which are
    # edited for particular schemes (e.g. PROJ must be edited)
    OCTREE_D = {
        PROJ: _REQD,
        TREE: STAR,
        SECTS: PDFIMAGES,
        SUBSECT: IMAGE_STAR,
        SUBSUB: OCTREE,
        FILE: CHANNEL_STAR,
        SUFFIX: S_PNG
    }

    PDFIMAGES_D = {
        PROJ: _REQD,
        TREE: STAR,
        SECTS: PDFIMAGES,
        SUBSECT: IMAGE_STAR,
        SUBSUB: _NULL,
        FILE: RAW,
        SUFFIX: S_PNG
    }
    RESULTS_D = {
        PROJ: _REQD,
        TREE: STAR,
        SECTS: RESULTS,
        SUBSECT: [SEARCH, WORD],
        SUBSUB: STARS,
        FILE: [RESULTS, EMPTY],
        SUFFIX: S_XML,
    }
    # /Users/pm286/projects/open-battery/    liion/ PMC3776197/ sections/ 1_body/ 5_methods/ 1_synthesis_of_mno_c_nanoco/ 1_p. xml
    #                                        PROJ     TREE       SECTS     SUBSECT  SUBSUB ...                            FILE SUFFIX
    SECTIONS_D = {
        PROJ: _REQD,
        TREE: STAR,
        SECTS: SECTIONS,
        SUBSECT: _REQD,
        SUBSUB: STARS,
        FILE: STAR,
        SUFFIX: S_XML
    }
    SVG_D = {
        PROJ: _REQD,
        TREE: STAR,
        SECTS: SVG,
        SUBSECT: _NULL,
        SUBSUB: _NULL,
        FILE: FULLTEXT_PAGE,
        SUFFIX: S_SVG
    }
"""

