from xml.etree import ElementTree
import os
from collections import Counter
from file_lib import FileLib

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

TERMINAL_IGNORE = {
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



class XmlLib():

    def __init__(self, file=None, outdir=None):
        self.file = file
        self.outdir = outdir
        print("xml", file)
        if file is not None:
            self.parse_file(file)

    def parse_file(self, file):
        if not os.path.exists(file):
            raise IOError("file does not exist", file)
        self.element_tree = ElementTree.parse(file)
        root = self.element_tree.getroot()
        if not self.outdir is None:
            outdir = self.outdir
            FileLib.force_mkdir(outdir)

        indent = 0
        filename = "1" + "_" + root.tag
        print(" " * indent, filename)
        subdir = os.path.join(outdir, filename)
        FileLib.force_mkdir(subdir)
        self.list_children(root, indent, subdir)

    def list_children(self, elem, indent, outdir):
        indent += 1
        tags = Counter()
        recurse = True
        for i, child in enumerate(list(elem)):
            tags[child.tag] += 1
            if child.tag in TERMINAL_COPY:
                print ("TERMINAL COPY", child.tag)
                XmlLib.copy_xml(child)
                recurse = False
            elif child.tag in TERMINAL_IGNORE:
                print ("TERMINAL IGNORE", child.tag)
                recurse = False
            else:
                pass

            title = child.tag
            if child.tag in SEC_TAGS:
                title = XmlLib.get_sec_title(child)
                tags[title] += 1

#            filename = str(tags[title]) + "_" + title
            filename = str(i) + "_" + title
            print(" " * indent, filename)
            if recurse:
                subdir = os.path.join(outdir, filename)
                if not os.path.exists(subdir):
                    os.mkdir(subdir)
                self.list_children(child, indent, subdir)

    @staticmethod
    def get_sec_title(sec):
        child_elems = list(sec)
        for elem in child_elems:
            if elem.tag == "title":
                title = "@" + elem.text
            elif sec.text is None:
                title = "EMPTY"
            else:
                title = "?_"+sec.text[:20]
        title = title.replace(" ", "_")
        print(">>", title)
        return title

    @staticmethod
    def copy_xml(child):
#        print("COPY XML", child.tag)
        pass

    def test(self):
        print("start xml")
        doc = XmlLib("../liion/PMC7077619/fulltext.xml", "../temp/PMC7077619")



class Section():

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
