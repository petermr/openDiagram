"""tests in a single file
This is until I or someone else can figure out relative imports
"""
class ConfigTests:
    from util import AmiConfig
    def tests():
        AmiConfig.test_dicts()

# FILE
class TextTests:
    pass

class UtilTests:
    from util import Util
    def test_dict_read():
        file = "section_templates.json"
        return Util.read_pydict_from_json(file)


class FileTests:
    import os
    from pathlib import Path

    @classmethod
    def test_expand_braces(cls):
        import os
        from file_lib import BraceGlobber as bg
        from glob import glob
        from braceexpand import braceexpand

        home = os.path.expanduser("~")
        file = __file__
        python_dir = os.path.abspath(file + "/../")
        resources_dir = os.path.join(python_dir, "resources")
        print("python", os.path.abspath(python_dir))
        physchem_dir = os.path.abspath(python_dir + "/../")
        open_diagram = os.path.abspath(physchem_dir + "/../")
        print(os.path.abspath(open_diagram))
        opend = os.path.join(open_diagram, "*")
        print("opend", opend)
        print("od0", glob(opend))
        open_diagram01 = os.path.join(physchem_dir, "**", "liion10", "**", "*.*ml")
        print("od01", glob(open_diagram01))

        open_diagram02 = os.path.join(home, "projects", "*iagram", "{*ot*,*.md}")
        print("od02", bg.braced_glob(open_diagram02))
        open_diagram11 = os.path.join(home, "projects", "*iagram", "*", "*", "*.xml")
        print("od", open_diagram11)
        print("b", glob(open_diagram11))
        open_diagram12 = os.path.join(home, "projects", "*iagram", "**", "*.xml")
        print("od", open_diagram12)
#        print("b12", glob(open_diagram12, recursive=True))
        pics = os.path.join(home, "projects", "*iagram", "**", "{*.svg,*.txt,*.png}")
        print("od", pics)
        print("pics", bg.braced_glob(pics, recursive=True))

    @classmethod
    def tests(cls):
        cls.test_expand_braces()

class WikimediaTests:
    @classmethod
    def test_sparql_wrapper(cls):
        """Author Shweata M Hegde
        from wikidata query site"""
        import sys
        from wikimedia import WikidataSparql as WS
        from SPARQLWrapper import SPARQLWrapper

        query = """#research council
        SELECT ?researchcouncil ?researchcouncilLabel 
        WHERE 
        {
          ?researchcouncil wdt:P31 wd:Q10498148.
          SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
        }"""

        results = WS.get_results_xml(query)
        print(results)

class XmlTests:
    import os
    from pathlib import Path

    XSLT_FILE = os.path.join(Path(__file__).parent, "jats2html.xsl")
    @classmethod
    def test_replace_nodes_with_text(cls):
        from xml_lib import XmlLib
        from lxml import etree

        data = '''<everything>
    <m>Some text before <r/></m>
    <m><r/> and some text after.</m>
    <m><r/></m>
    <m>Text before <r/> and after</m>
    <m><b/> Text after a sibling <r/> Text before a sibling<b/></m>
    </everything>
    '''
        result = XmlLib.replace_nodes_with_text(data, "//r", "DELETED")
        print(etree.tostring(result))

    @classmethod
    def test_replace_nodenames(cls):
        from lxml import etree
        data = '''<p>essential oil extracted from
 <italic>T. bovei</italic> was comprised ... on the
 <italic>T. bovei</italic> activities ... activity.
</p>'''

        doc = etree.fromstring(data)
        italics = doc.findall("italic")
        for node in italics:
            node.tag = "i"
        print(etree.tostring(doc))

    """transform = etree.XSLT(xslt_tree)
>>> result = transform(doc, a="'A'")
>>> bytes(result)
b'<?xml version="1.0"?>\n<foo>A</foo>\n'
    """
    @classmethod

    def test_xslt_italic(cls):
        from pathlib import Path
        import os
        from xml_lib import XmlLib
        from lxml import etree

        data = '''<p>essential oil extracted from
 <italic>T. bovei</italic> was comprised ... on the
 <italic>T. bovei</italic> activities ... activity.
</p>'''
        print("italic", XmlLib.xslt_transform_tostring(data, XmlTests.XSLT_FILE))

    @classmethod
    def test_xslt_copy(cls):
        from xml_lib import XmlLib
        from lxml import etree
        data="""<ack>
 <title>Acknowledgements</title>
 <p>The authors acknowledge the assistance of the technicians Mohamad Arar and Linda Esa and for An-Najah National University and Birzeit University for their support.</p>
 <sec id="FPar1">
  <title>Funding</title>
  <p>None.</p>
 </sec>
 <boo>foo</boo>
 <sec id="FPar2">
  <title>Availability of data and materials</title>
  <p>Data are all contained within the article.</p>
 </sec>
</ack>
"""
        print("copy", XmlLib.xslt_transform_tostring(data, XmlTests.XSLT_FILE))

    @classmethod
    def test_jats2html(cls):
        from xml_lib import XmlLib
        from lxml import etree
        print("test_jats2html")
        data = '''<everything>
<m>Some text before <r/></m>
<m><r/> and some text after.</m>
<m><r/></m>
<m>Text before <r/> and after</m>
<m><b/> Text after a sibling <r/> Text before a sibling<b/></m>
</everything>
'''
        result = XmlLib.replace_nodes_with_text(data, "//r", "DELETED")
        print(etree.tostring(result))


if __name__ == "__main__":
    print(f"running {__name__} main")

    config_test = False
    file_test = True
    wiki_test = False
    xml_test = False

    if config_test:
        ConfigTests.tests()
    if file_test:
        FileTests.tests()
    if wiki_test:
        WikimediaTests.test_sparql_wrapper()
    if xml_test:
        XmlTests.test_replace_nodes_with_text()
        XmlTests.test_replace_nodenames()
        XmlTests.test_jats2html()
        XmlTests.test_xslt_italic()
        XmlTests.test_xslt_copy()
