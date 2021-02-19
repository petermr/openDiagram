import os, glob, copy, json

class Globber():

    def __init__(self, ami_path, recurse=True, cwd=None):
        self.ami_path = ami_path
        self.recurse = recurse
        self.cwd = os.getcwd() if cwd is None else cwd

    def get_globbed_files(self):
        """uses the glob_string_list in ami_path to create a file list"""
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
    """holds a (keyed) scheme for generating lists of file globs
    The scheme has several segments which can be set to create a glob expression.
    """
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
            change = self.expand_set_lists()

    def expand_set_lists(self):
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
                if type(value) == list:
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
                glob += AmiPath.convert_to_glob(value)
            elif STAR in value:
                glob += AmiPath.convert_to_glob(value) + "/"
            elif SUFFIX == sect:
                glob += "." + AmiPath.convert_to_glob(value)
            else:
                glob += AmiPath.convert_to_glob(value) + "/"
        print("glob", glob)
        return glob

    @staticmethod
    def convert_to_glob(value):
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

class FileLib:

    @staticmethod
    def force_mkdir(outdir):
        if not os.path.exists(outdir):
            os.mkdir(outdir)





TEMPLATES_JSON = 'templates.json'
with open(TEMPLATES_JSON, 'r') as json_file:
    TEMPLATES = json.load(json_file)

def main():
    print("started file_lib")
    test_templates()

    print("finished file_lib")


def test_templates():
    PYDIAG = "../../python/diagrams"
#    simple_test()

    
    analyze_sections(PYDIAG + "/" + "luke/papers20210121")  # Zero?
    analyze_sections(PYDIAG + "/" + "../liion")
    analyze_sections(PYDIAG + "/" + "satish/cct")

def simple_test():
    PYDIAG = "../../python/diagrams"
    globbed_files = AmiPath.create("abstract", {PROJ: PYDIAG + "/" + "../liion"}),
    print(len(globbed_files), globbed_files[:5])


def analyze_sections(proj_dir):
    print("proj dir", os.path.exists(proj_dir))
    for ami_path in [
        AmiPath.create("abstract", {PROJ: proj_dir, FILE: "*background*"}),
        AmiPath.create("acknowledge", {PROJ: proj_dir}),
        AmiPath.create("affiliation", {PROJ: proj_dir}),
        AmiPath.create("author", {PROJ: proj_dir}),
        AmiPath.create("fig_caption", {PROJ: proj_dir}),
        AmiPath.create("introduction", {PROJ: proj_dir}),
        AmiPath.create("jrnl_title", {PROJ: proj_dir}),
        AmiPath.create("keyword", {PROJ: proj_dir}),
        AmiPath.create("method", {PROJ: proj_dir}),
        AmiPath.create("octree", {PROJ: proj_dir}),
        AmiPath.create("pdfimage", {PROJ: proj_dir}),
        AmiPath.create("pub_date", {PROJ: proj_dir}),
        AmiPath.create("publisher", {PROJ: proj_dir}),
        AmiPath.create("reference", {PROJ: proj_dir}),
        AmiPath.create("results", {PROJ: proj_dir}),
        AmiPath.create("results_discuss", {PROJ: proj_dir}),
        AmiPath.create("svg", {PROJ: proj_dir}),
        AmiPath.create("table", {PROJ: proj_dir}),
        AmiPath.create("title", {PROJ: proj_dir}),
    ]:
        globbed_files = ami_path.get_globbed_files()
        print(len(globbed_files), globbed_files[:5])


if __name__ == "__main__":
    print("running file_lib main")
    main()
else:
#    print("running file_lib main anyway")
#    main()
    pass

## examples of regex for filenames
import os
import re

def glob_re(pattern, strings):
    return filter(re.compile(pattern).match, strings)

filenames = glob_re(r'.*(abc|123|a1b).*\.txt', os.listdir())

