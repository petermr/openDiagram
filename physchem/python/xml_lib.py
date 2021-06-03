from xml.etree import ElementTree as ET
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

HTML_NS = "HTML_NS"
MATHML_NS = "MATHML_NS"
SVG_NS = "SVG_NS"
XMLNS_NS = "XMLNS_NS"
XML_NS = "XML_NS"
XLINK_NS = "XLINK_NS"

XML_LANG = "{" + XML_NS + "}" + 'lang'

NS_MAP = {
    HTML_NS : "http://www.w3.org/1999/xhtml",
    MATHML_NS : "http://www.w3.org/1998/Math/MathML",
    SVG_NS : "http://www.w3.org/2000/svg",
    XLINK_NS : "http://www.w3.org/1999/xlink",
    XML_NS : "http://www.w3.org/XML/1998/namespace",
    XMLNS_NS: "http://www.w3.org/2000/xmlns/",
    }

class XmlLib:

    def __init__(self, file=None, section_dir=SECTIONS):
        if file is not None:
            self.path = Path(file)
            self.parent_path = self.path.parent.absolute()
            self.parse_file(file, section_dir)

    def parse_file(self, file, section_dir):
        root = XmlLib.parse_xml_file_to_root(file)
        if not section_dir is None:
            print("making sections")
            self.section_dir = self.make_sections_path(section_dir)

        indent = 0
        filename = "1" + "_" + root.tag
        print(" " * indent, filename)
        subdir = os.path.join(self.section_dir, filename)
        FileLib.force_mkdir(subdir)
        self.list_children(root, indent, subdir)

    @staticmethod
    def parse_xml_file_to_root(file):
        if not os.path.exists(file):
            raise IOError("file does not exist", file)
        xmlp = ET.XMLParser(encoding="utf-8")
        element_tree = ET.parse(file, xmlp)
        root = element_tree.getroot()
        return root


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
                xml_string = ET.tostring(child)
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

# class Section:
#
#     def __init__(self):
#         pass

class HtmlElement:
    """to provide fluent HTML builder and parser"""
    pass

class DataTable:
    """
<html xmlns="http://www.w3.org/1999/xhtml">
 <head charset="UTF-8">
  <title>ffml</title>
  <link rel="stylesheet" type="text/css" href="http://ajax.aspnetcdn.com/ajax/jquery.dataTables/1.9.4/css/jquery.dataTables.css"/>
  <script src="http://ajax.aspnetcdn.com/ajax/jQuery/jquery-1.8.2.min.js" charset="UTF-8" type="text/javascript"> </script>
  <script src="http://ajax.aspnetcdn.com/ajax/jquery.dataTables/1.9.4/jquery.dataTables.min.js" charset="UTF-8" type="text/javascript"> </script>
  <script charset="UTF-8" type="text/javascript">$(function() { $("#results").dataTable(); }) </script>
 </head>
    """
    def __init__(self, title, colheads=None, rowdata=None):
        """create dataTables
        optionally add column headings (list) and rows (list of conformant lists) """
        self.html = ET.Element("html")
        self.head = None
        self.body = None
        self.create_head(title)
        self.create_body()
        self.add_column_heads(colheads)
        self.add_rows(rowdata)

    def create_head(self, title):
        """
          <title>ffml</title>
          <link rel="stylesheet" type="text/css" href="http://ajax.aspnetcdn.com/ajax/jquery.dataTables/1.9.4/css/jquery.dataTables.css"/>
          <script src="http://ajax.aspnetcdn.com/ajax/jQuery/jquery-1.8.2.min.js" charset="UTF-8" type="text/javascript"> </script>
          <script src="http://ajax.aspnetcdn.com/ajax/jquery.dataTables/1.9.4/jquery.dataTables.min.js" charset="UTF-8" type="text/javascript"> </script>
          <script charset="UTF-8" type="text/javascript">$(function() { $("#results").dataTable(); }) </script>
        """

        self.head = ET.SubElement(self.html, "head")
        self.title = ET.SubElement(self.head, "title")
        self.title.text = title

        link = ET.SubElement(self.head, "link")
        link.attrib["rel"] = "stylesheet"
        link.attrib["type"] = "text/css"
        link.attrib["href"] = "http://ajax.aspnetcdn.com/ajax/jquery.dataTables/1.9.4/css/jquery.dataTables.css"
        link.text = '.' # messy, to stop formatter using "/>" which dataTables doesn't like

        script = ET.SubElement(self.head, "script")
        script.attrib["src"] = "http://ajax.aspnetcdn.com/ajax/jQuery/jquery-1.8.2.min.js"
        script.attrib["charset"] = "UTF-8"
        script.attrib["type"] = "text/javascript"
        script.text = '.' # messy, to stop formatter using "/>" which dataTables doesn't like

        script = ET.SubElement(self.head, "script")
        script.attrib["src"] = "http://ajax.aspnetcdn.com/ajax/jquery.dataTables/1.9.4/jquery.dataTables.min.js"
        script.attrib["charset"] = "UTF-8"
        script.attrib["type"] = "text/javascript"
        script.text = "." # messy, to stop formatter using "/>" which dataTables doesn't like

        script = ET.SubElement(self.head, "script")
        script.attrib["charset"] = "UTF-8"
        script.attrib["type"] = "text/javascript"
        script.text = "$(function() { $(\"#results\").dataTable(); }) "



    def create_body(self):
        """
     <body>
      <div class="bs-example table-responsive">
       <table class="table table-striped table-bordered table-hover" id="results">
        <thead>
         <tr>
          <th>articles</th>
          <th>bibliography</th>
          <th>dic:country</th>
          <th>word:frequencies</th>
         </tr>
        </thead>
        """

        self.body = ET.SubElement(self.html, "body")
        self.div = ET.SubElement(self.body, "div")
        self.div.attrib["class"] = "bs-example table-responsive"
        self.table = ET.SubElement(self.div, "table")
        self.table.attrib["class"] = "table table-striped table-bordered table-hover"
        self.table.attrib["id"]="results"
        self.thead = ET.SubElement(self.table, "thead")
        self.tbody = ET.SubElement(self.table, "tbody")


    def add_column_heads(self, colheads):
        if colheads is not None:
            self.thead_tr = ET.SubElement(self.thead, "tr")
            for colhead in colheads:
                th = ET.SubElement(self.thead_tr, "th")
                th.text = colhead

    def add_rows(self, rowdata):
        if rowdata is not None:
            for row in rowdata:
                self.add_row(row)

    def add_row(self, row):
        if row is not None:
            tr = ET.SubElement(self.tbody, "tr")
            for val in row:
                td = ET.SubElement(tr, "td")
                td.text = val

    def __str__(self):
        s = self.html.text
        print("s", s)
        return s

def main():
    import pprint
    print("start content")
    XmlLib().test()
    print("end content")
    data_table = DataTable("test")
    data_table.add_column_heads(["a", "b", "c"])
    data_table.add_row(["a1", "b1", "c1"])
    data_table.add_row(["a2", "b2", "c2"])
    data_table.add_row(["a3", "b3", "c3"])
    data_table.add_row(["a4", "b4", "c4"])

    html = ET.tostring(data_table.html).decode("UTF-8")
    HOME = os.path.expanduser("~")
    with open(os.path.join(HOME, "junk_html.html"), "w") as f:
        f.write(html)
    pprint.pprint(html)

if __name__ == "__main__":
    print("running file_lib main")
    main()
else:
#    print("running file_lib main anyway")
#    main()
    pass
