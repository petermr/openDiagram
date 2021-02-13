import os, glob, copy


class Globber():

    def __init__(self, ami_path, recurse=True, cwd=None):
        self.ami_path = ami_path
        self.recurse = recurse
        self.cwd = os.getcwd() if cwd is None else cwd

    def get_globbed_files(self):
        files = []
        glob_list = self.ami_path.get_glob_string_list()
        for glb in glob_list:
            ff = glob.glob(glb, recursive=self.recurse)
            files.extend(ff)
        return files


    def test(self):

        print("cwd=", self.cwd, "path=", self.ami_path, "recurse=", self.recurse)
        print("glob_files", self.get_globbed_files())


# section keys
PROJ =   "PROJ"
TREE =   "TREE"
SECTS =  "SECTS"
SUBSECT = "SUBSECT"
SUBSUB = "SUBSUB"
FILE =   "FILE"
SUFFIX = "SUFFIX"

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
    T_OCTREE = "octree"
    T_PDFIMAGES = "pdfimages"
    T_RESULTS = "results"
    T_SECTIONS = "sections"
    T_SVG = "svg"

    # dict
    def __init__(self, scheme=None):
        self.scheme = scheme

    def print_scheme(self):
        if self.scheme is not None:
            for key in self.scheme:
                print(key, "=", self.scheme[key])
            print("")

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
        SUBSECT: {SEARCH, WORD},
        SUBSUB: STARS,
        FILE: {RESULTS, EMPTY},
        SUFFIX: S_XML,
    }
    SECTIONS_D = {
        PROJ: _REQD,
        TREE: STAR,
        SECTS: SECTIONS,
        SUBSECT: _REQD,
        SUBSUB: STARS,
        FILE: _REQD,
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

    @staticmethod
    def create(key, edit_dict=None):
        """creates a new AmiPath object from selected template
        key: to template
        edit_dict: dictionary with values to edit in
        """
        if key is None or key not in TEMPLATES:
            raise Exception("no scheme for: ", key)
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
            if _REQD == value:
                print("must set ", sect)
                glob += _REQD + "/"
            elif _NULL == value:
                pass
            elif FILE == sect:
                glob += value
            elif STAR in value:
                glob += value + "/"
            elif SUFFIX == sect:
                glob += "." + value
            else:
                glob += value + "/"
        return glob

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

TEMPLATES = {
    # rahul/rahul1/pdfimages/image.1.1.533_555.28_51/octree/channel.7b93c8.png
    AmiPath.T_OCTREE:    AmiPath.OCTREE_D,
    AmiPath.T_PDFIMAGES: AmiPath.PDFIMAGES_D,
    AmiPath.T_RESULTS:   AmiPath.RESULTS_D,
    # invasive / PMC3485296 / results / search / country / results.xml
    AmiPath.T_SECTIONS:  AmiPath.SECTIONS_D,
    AmiPath.T_SVG:       AmiPath.SVG_D,
}

def main():
    print("started file_lib")
    globbed_files = AmiPath.create(AmiPath.T_OCTREE, {PROJ: "../../python/diagrams/luke/papers20210121"}).get_globbed_files() # Zero?
    AmiPath.create(AmiPath.T_PDFIMAGES, {PROJ: "../liion"}).get_globbed_files()
    AmiPath.create(AmiPath.T_RESULTS, {PROJ: "../liion"}).get_globbed_files()
    AmiPath.create(AmiPath.T_SECTIONS, {PROJ: "../liion", SUBSECT: "*_body*", SUBSUB: "**", FILE: "*p",}).get_globbed_files()
    AmiPath.create(AmiPath.T_SVG, {PROJ: "../liion"}).get_globbed_files()

    print("finished file_lib")

if __name__ == "__main__":
    print("running file_lib main")
    main()
else:
#    print("running file_lib main anyway")
#    main()
    pass