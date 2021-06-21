from typing import Tuple
from configparser import ConfigParser, ExtendedInterpolation
import os
from xml.etree import ElementTree as ET


class TrieNode(object):
    """
    Our trie node implementation. Very basic. but does the job

    from https://towardsdatascience.com/implementing-a-trie-data-structure-in-python-in-less-than-100-lines-of-code-a877ea23c1a1
    """

    def __init__(self, char: str):
        """works on STRING"""
        self.char = char
        self.children = []
        # Is it the last character of the word.`
        self.word_finished = False
        # How many times this character appeared in the addition process
        self.counter = 1

    def add(self, word: str):
        """
        Adding a word in the trie structure
        """
        node = self
        for char in word:
            found_in_child = False
            # Search for the character in the children of the present `node`
            for child in node.children:
                if child.char == char:
                    # We found it, increase the counter by 1 to keep track that another
                    # word has it as well
                    child.counter += 1
                    # And point the node to the child that contains this char
                    node = child
                    found_in_child = True
                    break
            # We did not find it so add a new child
            if not found_in_child:
                new_node = TrieNode(char)
                node.children.append(new_node)
                # And then point node to the new child
                node = new_node
        # Everything finished. Mark it as the end of a word.
        node.word_finished = True

    def find_prefix(self, prefix: str) -> Tuple[bool, int]:
        """
        Check and return
          1. If the prefix exists in any of the words we added so far
          2. If yes then how may words actually have the prefix
        """
        node = self
        # If the root node has no children, then return False.
        # Because it means we are trying to search in an empty trie
        if not self.children:
            return False, 0
        for char in prefix:
            char_not_found = True
            # Search through all the children of the present `node`
            for child in node.children:
                if child.char == char:
                    # We found the char existing in the child.
                    char_not_found = False
                    # Assign node as the child containing the char and break
                    node = child
                    break
            # Return False anyway when we did not find a char.
            if char_not_found:
                return False, 0
        # Well, we are here means we have found the prefix. Return true to indicate that
        # And also the counter of the last node. This indicates how many words have this
        # prefix
        return True, node.counter

    @staticmethod
    def test():
        root = TrieNode('*')
        root.add("hackathon")
        root.add('hack')

        for term in ("hac", "hack", "hackathon", "ha", "hammer"):
            print(term, root.find_prefix(term))


import urllib.request

class AmiConfig:

    PYAMI_INI = "pyami.ini"
    DIRS = "DIRS"
    DICTS = "DICTIONARIES"
    LINK_SUFFIX = "_link"
    INI_SUFFIX= "_ini"
    URLINI_SUFFIX= "_urlini"
    URL_SUFFIX = "_url"
    SLASH = "/"

    def __init__(self, **kwargs):
        self.inistring = kwargs.get("inistring")
        self.inifile = kwargs.get("inifile")
        self.parser = None
        self._process_init_args()
        self.dict_id_dict = {}

    def _process_init_args(self):
        if self.inistring is not None:
            pass
        elif self.inifile is None:
            self.inifile = os.path.abspath(AmiConfig.get_default_pyami_ini_file())
        if self.inifile is not None:
            if os.path.exists(self.inifile):
                self.parser, _ = AmiConfig.read_ini_get_parser(self.inifile)
        elif self.inistring is not None:
            self.parser = ConfigParser(allow_no_value=True, interpolation=ExtendedInterpolation())
            self.parser.read_string(self.inistring)
            print("read from string")
        else:
            print("arguments wrong")

    def traverse_dictionary_dirs(self):

        dict_section = self.parser[AmiConfig.DICTS]
        for dict_key in dict_section.keys():
            print("dict key", dict_key)
            if dict_key.endswith(AmiConfig.LINK_SUFFIX):
                print("skipped link: ", dict_key)
            elif dict_key.endswith(AmiConfig.URL_SUFFIX):
                self.read_url_dicts(dict_key, dict_section)
            elif dict_key.endswith(AmiConfig.INI_SUFFIX):
                self.read_file_dicts(dict_key, dict_section)
            elif dict_key.endswith(AmiConfig.URLINI_SUFFIX):
                print("*_urlini not yet implemented")
            elif dict_key == "dict_dir":
                pass
            else:
                print("skipped key:", dict_key)

    def read_file_dicts(self, dict_key, dict_section):
        ini_file = self.create_ini_filename_from_link(dict_key, dict_section)
        print("dictionary ini file", dict_key, ini_file)
        if ini_file is None:
            print(f"no ini_file path for {dict_key}, please create in {AmiConfig.PYAMI_INI}")
        if not os.path.exists(ini_file):
            print("INI file does not exist, needs creating", ini_file)
        else:
            dict_config = AmiConfig(inifile=ini_file)
            sub_section = dict_config.parser[AmiConfig.DICTS]
            self.read_amidicts_in_inifile(dict_key, dict_section, sub_section)

    def read_amidicts_in_inifile(self, dict_ref, dict_section, sub_section):
        for dict_id in sub_section.keys():
            print("dict_id", dict_id)
            if dict_id in self.dict_id_dict:
                print("duplicate dict id: ", dict_id)
            if not dict_section[dict_ref] or not sub_section[dict_id]:
                print("No subsection for ", dict_id)
            else:
                file = self.read_dict_xml(dict_ref, dict_section, dict_id, sub_section)
                if file is not None and dict_id in self.dict_id_dict:
                    self.dict_id_dict[dict_id]

    def create_ini_filename_from_link(self, ini_key, dict_section):
#        ini_key = dict_ref[:-(len(AmiConfig.LINK_SUFFIX))] + AmiConfig.INI_SUFFIX
        ini_file = dict_section[ini_key] if ini_key in dict_section else None
        return ini_file

    def read_dict_xml(self, dict_ref, dict_section, dict_name, sub_section):
        ini_dir = dict_section[dict_ref].rpartition(AmiConfig.SLASH)[0]
        file = os.path.join(ini_dir, sub_section[dict_name])
        file = AmiConfig.transform_file_separator(file)
        if not os.path.exists(file):
            print("dict_ref file does not exist", file)
            file = None
        else:
            file_tree_xml = ET.parse(file)
            self._debug_desc_and_entries(dict_name, file_tree_xml)
        return file

    @staticmethod
    def transform_file_separator(file):
        file = file.replace(AmiConfig.SLASH, os.path.sep)
        return file

    def _debug_desc_and_entries(self, dict_name, file_tree_xml):
        descs = file_tree_xml.findall("desc")
        entries = file_tree_xml.findall("entry")
        wikidata = file_tree_xml.findall("entry[@wikidataID]")

        if descs:
            print(dict_name, "entries", len(entries), "wikidata", len(wikidata))
            for desc in descs:
                print("d: ", desc.text)
        else:
            print("no descs")


    def read_url_dicts(self, dict_key, dict_section):
        ini_url = self.create_ini_url_from_link(dict_key, dict_section)
        import urllib.request
        print("read url dicts", ini_url)
        txt = urllib.request.urlopen(ini_url).read().decode('utf-8')
        ami_config = AmiConfig(inistring=txt)
        parent_url = "/".join(ini_url.split("/")[:-1])
        print("section", parent_url)
        ami_config.process_dict_url(AmiConfig.DICTS, parent_url)

    def process_dict_url(self, section, parent_url):
        for dict_name in self.parser[section].keys():
            dict_terminal = self.parser[section][dict_name]
            dict_url = "/".join([parent_url, dict_terminal])
            tree_xml = self.read_xml_from_url(dict_url)
            entries = tree_xml.findall("entry")
            print(dict_terminal, "=", len(entries))

    def read_xml_from_url(self, dict_url):
        response = urllib.request.urlopen(dict_url).read()
        tree_xml = ET.fromstring(response)
        return tree_xml

    @staticmethod
    def test():
        ami_config = AmiConfig()
        print("ami", ami_config.parser.keys())
        for k in ami_config.parser.keys():
            print("k", k)
        print("cfg", type(ami_config))

    @staticmethod
    def test_dicts():
        """ finds and prints dictionaries"""
        ami_config = AmiConfig()
        dicts_dirs = ami_config.traverse_dictionary_dirs()
        print("dicts", dicts_dirs)

    @classmethod
    def test2_debug(cls):
        ami_config = AmiConfig()
        for sect_name in ami_config.parser.section_types():
            print("\n>>>>", sect_name, "\n>>>>>")
            section = ami_config.parser[sect_name]
            for k in section.keys():
                print(k)
                print(section[k])

    @staticmethod
    def read_ini_get_parser(ini_file):
        """create inifile name and read it

        return: parser, inifile
        """
        from configparser import ConfigParser, ExtendedInterpolation
        parser = ConfigParser(interpolation=ExtendedInterpolation())
        if not os.path.exists(ini_file):
            print("INI file does not exist", ini_file)
        else:
            print("read", AmiConfig.PYAMI_INI, ini_file)
            parser.read(ini_file)
        return parser, ini_file

    @staticmethod
    def get_default_pyami_ini_file():
        inifile = os.path.join(AmiConfig.get_home(), AmiConfig.PYAMI_INI)
        return inifile

    @staticmethod
    def get_home():
        home = os.path.expanduser("~")
        return home

    def create_ini_url_from_link(self, dict_ref, dict_section):
        ini_key = dict_ref[:-(len(AmiConfig.URL_SUFFIX))] + AmiConfig.INI_SUFFIX
        ini_file = dict_section[ini_key] if ini_key in dict_section else None
        return ini_file

    @classmethod
    def tests(cls):
        cls.test()
        cls.test_dicts()
        cls.test2_debug()

class Util:

    def check_exists(file):
        """
        raise exception on null value or non-existent file
        """
        if file is None:
            raise Exception("null file")

        if os.path.isdir(file):
#            print(file, "is directory")
            pass
        elif os.path.isfile(file):
#            print(file, "is file")
            pass
        else:
            try:
                f = open(file, "r")
                print("tried to open", file)
                f.close()
            except:
                raise FileNotFoundError(str(file) + " should exist")

    @staticmethod
    def find_unique_keystart(keys, start):
        """finds keys that start with 'start'
        return a list, empty if none found or null args"""
        return [] if keys is None or start is None else [k for k in keys if k.startswith(start)]

    @staticmethod
    def find_unique_dict_entry(the_dict, start):
        """
        return None if 0 or >= keys found
        """
        keys = Util.find_unique_keystart(the_dict, start)
        if len(keys) == 1:
            return the_dict[keys[0]]
        print("matching keys:", keys)
        return None

    @classmethod
    def read_pydict_from_json(cls, file):
        import ast
        with open(file, "r") as f:
            contents = f.read()
            dictionary = ast.literal_eval(contents)
            return dictionary


class PdfReader:

    def __init__(self):
        pass

    def test(self, file="/Users/pm286/projects/openDiagram/physchem/liion/PMC7040616/fulltext.pdf"):
        from pdfminer3.layout import LAParams, LTTextBox
        from pdfminer3.pdfpage import PDFPage
        from pdfminer3.pdfinterp import PDFResourceManager
        from pdfminer3.pdfinterp import PDFPageInterpreter
        from pdfminer3.converter import PDFPageAggregator
        from pdfminer3.converter import TextConverter
        import io

        resource_manager = PDFResourceManager()
        fake_file_handle = io.StringIO()
        converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
        page_interpreter = PDFPageInterpreter(resource_manager, converter)

        print("FILE", file)
        with open(file, 'rb') as fh:
            for page in PDFPage.get_pages(fh,
                                          caching=True,
                                          check_extractable=True):
                page_interpreter.process_page(page)

            text = fake_file_handle.getvalue()

        # close open handles
        converter.close()
        fake_file_handle.close()

        print(text)

def main():
#    AmiConfig.test()
#    AmiConfig.test2_debug()
#    AmiConfig.test_dicts()
    pdfReader = PdfReader()
    pdfReader.test();


#    TrieNode.test()

if __name__ == "__main__":
    main()
