from xml.etree import ElementTree
import os
from collections import Counter
from file_lib import FileLib
from pathlib import Path

# make leafnodes and copy remaning content as XML
TERMINAL_COPY = {
    "abstract",
    "aff",
    "article-id",
    "article-categories",
    "author-notes",
    "caption",
    "contrib-group",
    "fig",
    "history",
    "issue",
    "journal_id",
    "journal-title-group",
    "kwd-group",
    "name",
    "notes",
    "p",
    "permissions",
    "person-group",
    "pub-date",
    "publisher",
    "ref",
    "table",
    "title",
    "title-group",
    "volume",
}

TITLE = "title"

IGNORE_CHILDREN= {
    "disp-formula",
}

HTML_TAGS = {
    "italic": "i",
    "p": "p",
    "sub": "sub",
    "sup": "sup",
    "tr": "tr",
}

SEC_TAGS = {
    "sec",
}

LINK_TAGS = {
    "xref",
}

SECTIONS = "sections"

#XML_LANG = '{http://www.w3.org/XML/1998/namespace}lang'


class XmlLib:
    XML_NS = 'http://www.w3.org/XML/1998/namespace'
    XML_LANG = "{" + XML_NS + "}" + 'lang'

    def __init__(self, file=None, section_dir=SECTIONS):
        print("xml", file)
        if file is not None:
            self.path = Path(file)
            self.parent_path = self.path.parent.absolute()
            self.parse_file(file, section_dir)

    def parse_file(self, file, section_dir):
        if not os.path.exists(file):
            raise IOError("file does not exist", file)
        self.element_tree = ElementTree.parse(file)
        root = self.element_tree.getroot()
        if not section_dir is None:
            print("making sections")
            self.section_dir = self.make_sections_path(section_dir)

        indent = 0
        filename = "1" + "_" + root.tag
        print(" " * indent, filename)
        subdir = os.path.join(self.section_dir, filename)
        FileLib.force_mkdir(subdir)
        self.list_children(root, indent, subdir)

    def make_sections_path(self, section_dir):
        self.section_path = os.path.join(self.parent_path, section_dir)
        if not os.path.exists(self.section_path):
            FileLib.force_mkdir(self.section_path)
        return self.section_path

    def list_children(self, elem, indent, outdir):
        TERMINAL = "T_"
        IGNORE = "I_"
        for i, child in enumerate(list(elem)):
            flag = ""
            child_child_count = len(list(child))
            if child.tag in TERMINAL_COPY or child_child_count == 0:
                flag = TERMINAL
            elif child.tag in IGNORE_CHILDREN:
                flag = IGNORE

            title = child.tag
            if child.tag in SEC_TAGS:
                title = XmlLib.get_sec_title(child)

            if flag == IGNORE:
                title = flag + title
            filename = str(i) + "_" + title

            if flag == TERMINAL:
                xml_string = ElementTree.tostring(child)
                with open(os.path.join(outdir, filename + '.xml'), "wb") as f:
                    f.write(xml_string)
            else:
                subdir = os.path.join(outdir, filename)
                FileLib.force_mkdir(subdir) # creates empty dir, may be bad idea
                if flag == "":
                    self.list_children(child, indent, subdir)

    @staticmethod
    def get_sec_title(sec):
        title = None
        for elem in list(sec):
            if elem.tag == TITLE:
                title = elem.text
                break

        if title is None:
            if sec.xml_file is None:
                title = "EMPTY"
            else:
                title = "?_"+ sec.xml_file[:20]
        title = title.replace(" ", "_")
        return title

    def test(self):
        print("start xml")
        doc = XmlLib("../liion/PMC7077619/fulltext.xml")

class Section:

    def __init__(self):
        pass

def main():
    print("start content")
    XmlLib().test()
    print("end content")

if __name__ == "__main__":
    print("running file_lib main")
    main()
else:
#    print("running file_lib main anyway")
#    main()
    pass
