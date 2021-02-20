import os, glob, copy
from file_lib import AmiPath, PROJ
from text_lib import ProjectCorpus, Document, TerminalPage, Sentence, TextUtil

PYDIAG = "../../python/diagrams"
LIION = "../liion"
class AmiSearch():

    def __init__(self):
        self.dictionaries = []

    def add_dictionary(self, dictionary):
        self.dictionaries.append(dictionary)

    def search(self, file):
        words = get_words(file)
        for dictionary in self.dictionaries:
            dictionary.match(words)


class SimpleDict():

    def __init__(self, file=None):
        if file:
            with open(file, "r") as f:
                self.lines = f.read().splitlines()
        print (self.lines)


def main():
    print("started search")
    test()
    print("finished search")


def test():
    ami_search = AmiSearch()
    dictionary = SimpleDict("simple_dict.txt")
    ami_search.add_dictionary(dictionary)
    methods = AmiPath.create("method", {PROJ: LIION})
    files = methods.get_globbed_files()
    for file in files:
        print("file", file)
        ami_search.search(file)
    print("files", len(files))


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