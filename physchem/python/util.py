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

class AmiConfig:

    def __init__(self, interpolation=ExtendedInterpolation()):

        self.parser = ConfigParser(allow_no_value=True, interpolation=ExtendedInterpolation())
        home = os.path.expanduser("~")
        inifile = os.path.join(home, "pyami.ini")
        if not os.path.exists(inifile):
            print("no pyami.ini file")
        else:
            print("pyami", inifile)
            self.parser.read(inifile)

    def get_dictionary_dirs(self):
        dict_section = self.parser["DICTIONARIES"]
        link_suffix = "_link"
        ini_suffix = "_ini"
        for dict_ref in dict_section.keys():
            dict_dir = dict_section[dict_ref]
            if dict_ref.endswith(link_suffix):
                ini_key = dict_ref[:-(len(link_suffix))] + ini_suffix
                print(ini_key)
                ini_file = dict_section[ini_key]
                print("dict_ref", dict_ref, ini_file)
                parser = ConfigParser(allow_no_value=True, interpolation=ExtendedInterpolation())
                parser.read(ini_file)
                print("dicts", parser["DICTIONARIES"])
                sub_section = parser["DICTIONARIES"]
                for kk in sub_section.keys():
                    if not dict_section[dict_ref] or not sub_section[kk]:
                        print("No subsection for ", kk)
                    else:
#                        print("OK", kk)
                        file = os.path.join(dict_section[dict_ref], kk, sub_section[kk])
                        if not os.path.exists(file):
                            print("file does not exist", file)
                        else:
                            file_tree = ET.parse(file)
                            desc = file_tree.findall("desc")
                            if desc:
                                print(kk, "\n    ", desc[0].text)
                            else:
                                print("no desc")

    @staticmethod
    def test():
        ami_config = AmiConfig()
        print(type(ami_config))
        """
        for sect_name in cfg.sections():
            section = cfg[sect_name]
            for k in section.keys():
                print(k, "=", section[k])
        """
        cfg = ami_config.parser
        print("home", cfg["DEFAULT"]["home"])
        print("cev", cfg.get("DICTIONARIES", "cev_link"))
        dicts_dirs = ami_config.get_dictionary_dirs()


    @staticmethod
    def test1():
        from configparser import ConfigParser, ExtendedInterpolation
        parser = ConfigParser(interpolation=ExtendedInterpolation())
        parser.read("/Users/pm286/pyami.ini")

        print("foo", parser["DEFAULT"]["home"])
        print("eo", parser.get("DICTIONARIES", "cev_link"))

def main():
    AmiConfig.test()
    print("==============")
    AmiConfig.test1()
#    TrieNode.test()

if __name__ == "__main__":
    main()
