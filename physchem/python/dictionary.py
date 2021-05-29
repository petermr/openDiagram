import os

from constants import CEV_OPEN_DICT_DIR, OV21_DIR, DICT_AMI3, PHYSCHEM_RESOURCES
from util import Util
"""
from text_lib import TextUtil, AmiSection, WordFilter
from xml_lib import XmlLib
from util import Util
"""
#from xml.etree import ElementTree as ET
from lxml import etree as ET
"""
from collections import Counter
import re
import json
from gutil import Gutil
"""


# entry
WIKIDATA_ID = "wikidataID"
NS_MAP = {'SPQ': 'http://www.w3.org/2005/sparql-results#'}  # add more as needed
NS_URI = "SPQ:uri"
NS_LITERAL = "SPQ:literal"

class SearchDictionary:
    """wrapper for an ami dictionary including search flags

    """
    TERM = "term"

    def __init__(self, xml_file=None, name=None, **kwargs):
        self.amidict = None
        self.entries = []
        self.entry_by_wikidata_id = {}
        self.file = xml_file
        self.ignorecase = None
        self.name = None
        self.root = None
        self.split_terms = False
        self.term_set = set()

        if xml_file is not None:
            if not os.path.exists(xml_file):
                raise IOError("cannot find file " + str(xml_file))
            self.read_dictionary_from_xml_file(xml_file)
            self.name = xml_file.split("/")[-1:][0].split(".")[0]
        elif name is None:
            print("must have name for new dictionary")
        else:
            self.name = name

        self.options = {} if not "options" in kwargs else kwargs["options"]
        if "synonyms" in self.options:
            print("use synonyms")
        if "noignorecase" in self.options:
            print("use case")
        self.split_terms = True
        self.split_terms = False

    def read_dictionary_from_xml_file(self, file, ignorecase=True):
        self.file = file
        self.amidict = ET.parse(file, parser=ET.XMLParser(encoding="utf-8"))
        self.root = self.amidict.getroot()
        self.name = self.root.attrib["title"]
        self.ignorecase = ignorecase

        self.entries = list(self.root.findall("entry"))
        self.create_entry_by_term();
        self.term_set = set()
#        print("read dictionary", self.name, "with", len(self.entries), "entries")

    def get_or_create_term_set(self):
        if len(self.term_set) == 0:
            for entry in self.entries:
                if SearchDictionary.TERM in entry.attrib:
                    term = self.term_from_entry(entry)
#                    print("tterm", term)
                    # single word terms
                    if not " " in term:
                        self.add_processed_term(term)
                    elif self.split_terms:
                        # multiword terms
                        for termx in term.split(" "):
#                            print("term", termx)
                            self.add_processed_term(termx)
                    else:
                        # add multiword term
                        self.add_processed_term(term)

        #            print(len(self.term_set), list(sorted(self.term_set)))
        #        print ("terms", len(self.term_set))
        return self.term_set

    def get_or_create_multiword_terms(self):
        return
        """NYI"""
        if len(self.multiwords) == 0:
            for entry in self.entries:
                if SearchDictionary.TERM in entry.attrib:
                    term = self.term_from_entry(entry)
                    # single word terms
                    if not " " in term:
                        self.add_processed_term(term)
                    elif self.split_terms:
                        # multiword terms
                        for term in " ".split(term):
                            self.add_processed_term(term)

        #            print(len(self.term_set), list(sorted(self.term_set)))
        #        print ("terms", len(self.term_set))
        return self.term_set

    def term_from_entry(self, entry):
        if SearchDictionary.TERM not in entry.attrib:
            print("missing term", ET.tostring(entry))
            term = None
        else:
            term = entry.attrib[SearchDictionary.TERM].strip()
        return term.lower() if term is not None and self.ignorecase else term

    def get_xml_and_image_url(self, term):
        entry = self.get_entry(term)
        entry_xml = ET.tostring(entry)
        image_url = entry.find(".//image")
        return entry_xml, image_url.text if image_url is not None else None

    def add_processed_term(self, term):
        if self.ignorecase:
            term = term.lower()
        self.term_set.add(term)  # single word countries

    def match(self, target_words):
        matched = []
        self.term_set = self.get_or_create_term_set()
        for target_word in target_words:
            target_word = target_word.lower()
            if target_word in self.term_set:
                matched.append(target_word)
        return matched

    def match_multiple_word_terms_against_sentences(self, sentence_list):
        """this will be slow with large dictionaries until we optimise the algorithm """
        matched = []

        for term in self.term_set:
            term = term.lower()
            term_words = term.split(" ")
            if len(term_words) > 1:
                for sentence in sentence_list:
                    if term in sentence.lower():
                        matched.append(term)
                        print("MATCHED MULTIWORD", term)
        return matched

    def get_entry(self, term):
        if self.entry_by_term is None:
            self.create_entry_by_term()
        entry = self.entry_by_term[term] if term in self.entry_by_term else None
        if entry is None:
            print("entry by term", self.entry_by_term)
        return entry

    def create_entry_by_term(self):
        self.entry_by_term = {self.term_from_entry(entry) : entry  for entry in self.entries}

    def update_from_sparqlx(self, sparql_file, sparql_to_dictionary):
        self.sparql_to_dictionary = sparql_to_dictionary
        self.check_unique_wikidata_ids()
        self.create_sparql_result_list(sparql_file)
        self.create_sparql_result_by_wikidata_id()
        self.update_dictionary_from_sparql()

    def create_sparql_result_list(self, sparql_file):
        assert(os.path.exists(sparql_file))
        print("sparql file", sparql_file)
        self.current_sparql = ET.parse(sparql_file, parser=ET.XMLParser(encoding="utf-8"))
        self.sparql_result_list = list(self.current_sparql.findall('SPQ:results/SPQ:result', NS_MAP))
        assert(len(self.sparql_result_list) > 0)
        print("results", len(self.sparql_result_list))

    def create_sparql_result_by_wikidata_id(self):
        self.sparql_result_by_wikidata_id = {}
#        print("results", len(self.sparql_result_list))
#        id_element = "item"
        id_element = self.sparql_to_dictionary["id_name"]
        for result in self.sparql_result_list:
            bindings = result.findall("SPQ:binding[@name='%s']/SPQ:uri" % id_element, NS_MAP)
            if len(bindings) == 0:
                print("no bindings for {id_element}")
            else:
                uri = list(bindings)[0]
                wikidata_id = uri.text.split("/")[-1]
                if not wikidata_id in self.sparql_result_by_wikidata_id:
                    self.sparql_result_by_wikidata_id[wikidata_id] = []
                self.sparql_result_by_wikidata_id[wikidata_id].append(result)

    def check_unique_wikidata_ids(self):
        print("entries", len(self.entries))
        self.entry_by_wikidata_id = {}
        for entry in self.entries:
            if WIKIDATA_ID not in entry.attrib:
                print("No wikidata ID for", entry)
            else:
                wikidata_id = entry.attrib[WIKIDATA_ID]
                if wikidata_id in self.entry_by_wikidata_id.keys():
                    print("duplicate Wikidata ID:", wikidata_id, entry)
                else:
                    self.entry_by_wikidata_id[wikidata_id] = entry

    #        print("entry by id", self.entry_by_wikidata_id)

    def update_dictionary_from_sparql(self):

        print("sparql result by id", len(self.sparql_result_by_wikidata_id))
#        sparql_name = "image"
#        dict_name = "image"
        sparql_name = self.sparql_to_dictionary["sparql_name"]
        dict_name = self.sparql_to_dictionary["dict_name"]
        for wikidata_id in self.sparql_result_by_wikidata_id.keys():
            if wikidata_id in self.entry_by_wikidata_id.keys():
                entry = self.entry_by_wikidata_id[wikidata_id]
                result_list = self.sparql_result_by_wikidata_id[wikidata_id]
                for result in result_list:
                    bindings = list(result.findall("SPQ:binding[@name='" + sparql_name + "']", NS_MAP))
                    if len(bindings) > 0:
                        binding = bindings[0]
                        self.update_entry(entry, binding, dict_name)
#                print("dict", ET.tostring(entry))

    def update_entry(self, entry, binding, dict_name):
        updates = list(binding.findall(NS_URI, NS_MAP)) + \
                  list(binding.findall(NS_LITERAL, NS_MAP))
        entry_child = ET.Element(dict_name)
        entry_child.text = updates[0].text
        if entry_child.text is not None and len(entry_child.text.strip()) > 0:
            entry.append(entry_child)
#        print(">>", ET.tostring(entry))

    def write(self, file):
        from lxml import etree
        et = etree.ElementTree(self.root)
        with open(file, 'wb') as f:
            et.write(f, encoding="utf-8", xml_declaration=True, pretty_print=True)

    def add_wikidata_from_terms(self):
        entries = self.root.findall("entry")
        for entry in entries:
            term = entry.attrib["term"]
            self.lookup_wikidata(term)

    def lookup_wikidata(self, term):
        import pprint

        from urllib.request import urlopen
        from urllib.request import quote
        uterm = quote(term.encode('utf8'))
        url = f"https://www.wikidata.org/w/index.php?search={uterm}"
        with urlopen(url) as u:
            content = u.read()
        root = ET.fromstring(content)
        body = root.find("body")
        uls = body.findall(".//ul[@class='mw-search-results']")
        if len(uls) > 0:
            wikidata_dict = {}
            for li in uls[0]:
                result_heading_a = li.find("./div[@class='mw-search-result-heading']/a")
                qitem = result_heading_a.attrib["href"].split("/")[-1]
                if qitem in wikidata_dict:
                    print(f"duplicate wikidata entry {qitem}")
                    continue
                sub_dict = {}
                wikidata_dict[qitem] = sub_dict
                # make title from text children not tooltip
                sub_dict["title"] = ''.join(result_heading_a.itertext()).split("(Q")[0]
                sub_dict["desc"] = li.find("./div[@class='searchresult']/span").text
                # just take statements at present (n statements or 1 statement)
                sub_dict["statements"] = li.find("./div[@class='mw-search-result-data']").text.split(",")[0].split(" statement")[0]

            for item in wikidata_dict.items():
                # print(">", str(item))
                pass
            sort_orders = sorted(wikidata_dict.items(), key=lambda item : int(item[1]["statements"]), reverse=True)
            pprint.pprint(sort_orders[0:3])


    # <li class="mw-search-result">
    # <div class="mw-search-result-heading">
    # <a href="/wiki/Q50887234" title="&#8206;Lantana camara var. nivea&#8206; | &#8206;variety of plant&#8206;" data-serp-pos="13">
    #  <span class="wb-itemlink">
    #   <span class="wb-itemlink-label" lang="en" dir="ltr">
    #    <span class="searchmatch">Lantana</span>
    #    <span class="searchmatch">camara</span>
    #     var. nivea
    #   </span>
    #   <span class="wb-itemlink-id">(Q50887234)</span>
    # </span>
    # </a>
    # </div>
    #     <div class="searchresult">
    #     <span class="wb-itemlink-description">variety of plant</span>
    #     </div>
    #     <div class="mw-search-result-data">12 statements, 0 sitelinks - 17:16, 16 April 2021</div>
    #        </li>'
#         <li>
#         <div class="mw-search-result-heading">
#              <a href="/wiki/Q278809" title="(&#177;)-limonene | chemical compound" data-serp-pos="0">
#                <span class="wb-itemlink">
#                  <span class="wb-itemlink-label" lang="en" dir="ltr">(&#177;)-
#                    <span class="searchmatch">limonene</span>
#                  </span>
#                  <span class="wb-itemlink-id">(Q278809)</span>
#                </span>
#              </a>
#           </div>'
# ..        <div class="searchresult">
#             <span class="wb-itemlink-description">chemical compound</span>
#           </div> '
#         """
        #   < li class ="mw-search-result" >
        #     < div class ="mw-search-result-heading" > < a href="/wiki/Q278809" title="(&#177;)-limonene | chemical compound" data-serp-pos="0" > < span class ="wb-itemlink" > < span class ="wb-itemlink-label" lang="en" dir="ltr" > ( &  # 177;)-<span class="searchmatch">limonene</span></span> <span class="wb-itemlink-id">(Q278809)</span></span></a>    </div><div class="searchresult"><span class="wb-itemlink-description">chemical compound</span></div> <div class="mw-search-result-data">1021 statements, 32 sitelinks - 10:51, 24 May 2021</div></li><li class="mw-search-result"><div class="mw-search-result-heading"><a href="/wiki/Q22282878" title="limonene biosynthetic process | The chemical reactions and pathways resulting in the formation of limonene (4-isopropenyl-1-methyl-cyclohexene), a monocyclic monoterpene." data-serp-pos="1"><span class="wb-itemlink"><span class="wb-itemlink-label" lang="en" dir="ltr"><span class="searchmatch">limonene</span> biosynthetic process</span> <span class="wb-itemlink-id">(Q22282878)</span></span></a>    </div><div class="searchresult"><span class="wb-itemlink-description">The chemical reactions and pathways resulting in the formation of limonene (4-isopropenyl-1-methyl-cyclohexene), a monocyclic monoterpene.</span></div> <div class="mw-search-result-data">8 statements, 0 sitelinks - 08:29, 17 May 2020</div></li><li class="mw-search-result"><div class="mw-search-result-heading"><a href="/wiki/Q22282225" title="limonene catabolic process | The chemical reactions and pathways resulting in the breakdown of limonene (4-isopropenyl-1-methyl-cyclohexene), a monocyclic monoterpene." data-serp-pos="2"><span class="wb-itemlink"><span class="wb-itemlink-label" lang="en" dir="ltr"><span class="searchmatch">limonene</span> catabolic process</span> <span class="wb-itemlink-id">(Q22282225)</span></span></a>    </div><div class="searchresult"><span class="wb-itemlink-description">The chemical reactions and pathways resulting in the breakdown of limonene (4-isopropenyl-1-methyl-cyclohexene), a monocyclic monoterpene.</span></div> <div class="mw-search-result-data">7 statements, 0 sitelinks - 13:16, 17 May 2020</div></li><li class="mw-search-result"><div class="mw-search-result-heading"><a href="/wiki/Q22324407" title="(4S)-limonene synthase activity | Catalysis of the reaction: geranyl diphosphate = (4S)-limonene + diphosphate." data-serp-pos="3"><span class="wb-itemlink"><span class="wb-itemlink-label" lang="en" dir="ltr">(4S)-<span class="searchmatch">limonene</span> synthase activity</span> <span class="wb-itemlink-id">(Q22324407)</span></span></a>    </div><div class="searchresult"><span class="wb-itemlink-description">Catalysis of the reaction: geranyl diphosphate = (4S)-limonene + diphosphate.</span></div> <div class="mw-search-result-data">9 statements, 0 sitelinks - 17:28, 7 April 2021</div></li><li class="mw-search-result"><div class="mw-search-result-heading"><a href="/wiki/Q14916176" title="(S)-limonene 7-monooxygenase activity | Catalysis of the reaction: (4S)-limonene + H(+) + NADPH + O(2) = (4S)-perillyl alcohol + H(2)O + NADP(+)." data-serp-pos="4"><span class="wb-itemlink"><span class="wb-itemlink-label" lang="en" dir="ltr">(S)-<span class="searchmatch">limonene</span> 7-monooxygenase activity</span> <span class="wb-itemlink-id">(Q14916176)</span></span></a>    </div><div class="searchresult"><span class="wb-itemlink-description">Catalysis of the reaction: (4S)-limonene + H(+) + NADPH + O(2) = (4S)-perillyl alcohol + H(2)O + NADP(+).</span></div> <div class="mw-search-result-data">12 statements, 0 sitelinks - 07:50, 8 April 2021</div></li><li class="mw-search-result"><div class="mw-search-result-heading"><a href="/wiki/Q22282223" title="limonene metabolic process | The chemical reactions and pathways involving limonene (4-isopropenyl-1-methyl-cyclohexene), a monocyclic monoterpene." data-serp-pos="5"><span class="wb-itemlink"><span class="wb-itemlink-label" lang="en" dir="ltr"><span class="searchmatch">limonene</span> metabolic process</span> <span class="wb-itemlink-id">(Q22282223)</span></span></a>    </div><div class="searchresult"><span class="wb-itemlink-description">The chemical reactions and pathways involving limonene (4-isopropenyl-1-methyl-cyclohexene), a monocyclic monoterpene.</span></div> <div class="mw-search-result-data">7 statements, 0 sitelinks - 07:32, 17 May 2020</div></li><li class="mw-search-result"><div class="mw-search-result-heading"><a href="/wiki/Q14916175" title="(S)-limonene 6-monooxygenase activity | Catalysis of the reaction: (-)-limonene + NADPH + H+ + O2 = (-)-trans-carveol + NADP+ + H2O." data-serp-pos="6"><span class="wb-itemlink"><span class="wb-itemlink-label" lang="en" dir="ltr">(S)-<span class="searchmatch">limonene</span> 6-monooxygenase activity</span> <span class="wb-itemlink-id">(Q14916175)</span></span></a>    </div><div class="searchresult"><span class="wb-itemlink-description">Catalysis of the reaction: (-)-limonene + NADPH + H+ + O2 = (-)-trans-carveol + NADP+ + H2O.</span></div> <div class="mw-search-result-data">11 statements, 0 sitelinks - 17:43, 7 April 2021</div></li><li class="mw-search-result"><div class="mw-search-result-heading"><a href="/wiki/Q3596292" title="(S)-limonene 3-monooxygenase | class of enzymes" data-serp-pos="7"><span class="wb-itemlink"><span class="wb-itemlink-label" lang="en" dir="ltr">(S)-<span class="searchmatch">limonene</span> 3-monooxygenase</span> <span class="wb-itemlink-id">(Q3596292)</span></span></a>    </div><div class="searchresult"><span class="wb-itemlink-description">class of enzymes</span></div> <div class="mw-search-result-data">6 statements, 5 sitelinks - 06:33, 24 May 2021</div></li><li class="mw-search-result"><div class="mw-search-result-heading"><a href="/wiki/Q22317639" title="(S)-limonene 3-monooxygenase activity | Catalysis of the reaction: (4S)-limonene + H(+) + NADPH + O(2) = (1S,6R)-isopiperitenol + H(2)O + NADP(+)." data-serp-pos="8"><span class="wb-itemlink"><span class="wb-itemlink-label" lang="en" dir="ltr">(S)-<span class="searchmatch">limonene</span> 3-monooxygenase activity</span> <span class="wb-itemlink-id">(Q22317639)</span></span></a>    </div><div class="searchresult"><span class="wb-itemlink-description">Catalysis of the reaction: (4S)-limonene + H(+) + NADPH + O(2) = (1S,6R)-isopiperitenol + H(2)O + NADP(+).</span></div> <div class="mw-search-result-data">12 statements, 0 sitelinks - 17:35, 7 April 2021</div></li><li class="mw-search-result"><div class="mw-search-result-heading"><a href="/wiki/Q27089405" title="(-)-limonene | chemical compound" data-serp-pos="9"><span class="wb-itemlink"><span class="wb-itemlink-label" lang="en" dir="ltr">(-)-<span class="searchmatch">limonene</span></span> <span class="wb-itemlink-id">(Q27089405)</span></span></a>    </div><div class="searchresult"><span class="wb-itemlink-description">chemical compound</span></div> <div class="mw-search-result-data">73 statements, 0 sitelinks - 15:03, 18 April 2021</div></li><li class="mw-search-result"><div class="mw-search-result-heading"><a href="/wiki/Q22317631" title="(R)-limonene 1,2-monooxygenase activity | Catalysis of the reaction: (4R)-limonene + NAD(P)H + H+ + O2 = NAD(P)+ + H2O + (4R)-limonene-1,2-epoxide." data-serp-pos="10"><span class="wb-itemlink"><span class="wb-itemlink-label" lang="en" dir="ltr">(R)-<span class="searchmatch">limonene</span> 1,2-monooxygenase activity</span> <span class="wb-itemlink-id">(Q22317631)</span></span></a>    </div><div class="searchresult"><span class="wb-itemlink-description">Catalysis of the reaction: (4R)-limonene + NAD(P)H + H+ + O2 = NAD(P)+ + H2O + (4R)-limonene-1,2-epoxide.</span></div> <div class="mw-search-result-data">6 statements, 0 sitelinks - 15:06, 18 April 2021</div></li><li class="mw-search-result"><div class="mw-search-result-heading"><a href="/wiki/Q22317627" title="(S)-limonene 1,2-monooxygenase activity | Catalysis of the reaction: (4S)-limonene + NAD(P)H + H+ + O2 = NAD(P)+ + H2O + (4S)-limonene-1,2-epoxide." data-serp-pos="11"><span class="wb-itemlink"><span class="wb-itemlink-label" lang="en" dir="ltr">(S)-<span class="searchmatch">limonene</span> 1,2-monooxygenase activity</span> <span class="wb-itemlink-id">(Q22317627)</span></span></a>    </div><div class="searchresult"><span class="wb-itemlink-description">Catalysis of the reaction: (4S)-limonene + NAD(P)H + H+ + O2 = NAD(P)+ + H2O + (4S)-limonene-1,2-epoxide.</span></div> <div class="mw-search-result-data">6 statements, 0 sitelinks - 15:06, 18 April 2021</div></li><li class="mw-search-result"><div class="mw-search-result-heading"><a href="/wiki/Q16872168" title="Limonene synthase | Wikimedia disambiguation page" data-serp-pos="12"><span class="wb-itemlink"><span class="wb-itemlink-label" lang="en" dir="ltr"><span class="searchmatch">Limonene</span> synthase</span> <span class="wb-itemlink-id">(Q16872168)</span></span></a>    </div><div class="searchresult"><span class="wb-itemlink-description">Wikimedia disambiguation page</span></div> <div class="mw-search-result-data">1 statement, 1 sitelink - 02:59, 4 May 2019</div></li><li class="mw-search-result"><div class="mw-search-result-heading"><a href="/wiki/Q3596284" title="(R)-limonene 6-monooxygenase | class of enzymes" data-serp-pos="13"><span class="wb-itemlink"><span class="wb-itemlink-label" lang="en" dir="ltr">(R)-<span class="searchmatch">limonene</span> 6-monooxygenase</span> <span class="wb-itemlink-id">(Q3596284)</span></span></a>    </div><div class="searchresult"><span class="wb-itemlink-description">class of enzymes</span></div> <div class="mw-search-result-data">6 statements, 5 sitelinks - 17:17, 23 May 2021</div></li><li class="mw-search-result"><div class="mw-search-result-heading"><a href="/wiki/Q76625426" title="Limonene Hydroxylases | Members of the P-450 enzyme family that take part in the hydroxylation of limonene." data-serp-pos="14"><span class="wb-itemlink"><span class="wb-itemlink-label" lang="en" dir="ltr"><span class="searchmatch">Limonene</span> Hydroxylases</span> <span class="wb-itemlink-id">(Q76625426)</span></span></a>    </div><div class="searchresult"><span class="wb-itemlink-description">Members of the P-450 enzyme family that take part in the hydroxylation of limonene.</span></div> <div class="mw-search-result-data">1 statement, 0 sitelinks - 13:57, 27 November 2019</div></li><li class="mw-search-result"><div class="mw-search-result-heading"><a href="/wiki/Q14916177" title="(R)-limonene 6-monooxygenase activity | Catalysis of the reaction: (4R)-limonene + H+ + NADPH + O2 = (1R,5S)-carveol + H2O + NADP+." data-serp-pos="15"><span class="wb-itemlink"><span class="wb-itemlink-label" lang="en" dir="ltr">(R)-<span class="searchmatch">limonene</span> 6-monooxygenase activity</span> <span class="wb-itemlink-id">(Q14916177)</span></span></a>    </div><div class="searchresult"><span class="wb-itemlink-description">Catalysis of the reaction: (4R)-limonene + H+ + NADPH + O2 = (1R,5S)-carveol + H2O + NADP+.</span></div> <div class="mw-search-result-data">12 statements, 0 sitelinks - 17:45, 7 April 2021</div></li><li class="mw-search-result"><div class="mw-search-result-heading"><a href="/wiki/Q22324412" title="(R)-limonene synthase activity | Catalysis of the reaction: geranyl diphosphate = (4R)-limonene + diphosphate." data-serp-pos="16"><span class="wb-itemlink"><span class="wb-itemlink-label" lang="en" dir="ltr">(R)-<span class="searchmatch">limonene</span> synthase activity</span> <span class="wb-itemlink-id">(Q22324412)</span></span></a>    </div><div class="searchresult"><span class="wb-itemlink-description">Catalysis of the reaction: geranyl diphosphate = (4R)-limonene + diphosphate.</span></div> <div class="mw-search-result-data">10 statements, 0 sitelinks - 17:22, 7 April 2021</div></li><li class="mw-search-result"><div class="mw-search-result-heading"><a href="/wiki/Q3596293" title="(S)-limonene 6-monooxygenase | class of enzymes" data-serp-pos="17"><span class="wb-itemlink"><span class="wb-itemlink-label" lang="en" dir="ltr">(S)-<span class="searchmatch">limonene</span> 6-monooxygenase</span> <span class="wb-itemlink-id">(Q3596293)</span></span></a>    </div><div class="searchresult"><span class="wb-itemlink-description">class of enzymes</span></div> <div class="mw-search-result-data">6 statements, 5 sitelinks - 06:41, 24 May 2021</div></li><li class="mw-search-result"><div class="mw-search-result-heading"><a href="/wiki/Q3596295" title="(S)-limonene 7-monooxygenase | class of enzymes" data-serp-pos="18"><span class="wb-itemlink"><span class="wb-itemlink-label" lang="en" dir="ltr">(S)-<span class="searchmatch">limonene</span> 7-monooxygenase</span> <span class="wb-itemlink-id">(Q3596295)</span></span></a>    </div><div class="searchresult"><span class="wb-itemlink-description">class of enzymes</span></div> <div class="mw-search-result-data">6 statements, 5 sitelinks - 06:43, 24 May 2021</div></li><li class="mw-search-result"><div class="mw-search-result-heading"><a href="/wiki/Q4543797" title="(4S)-limonene synthase | class of enzymes" data-serp-pos="19"><span class="wb-itemlink"><span class="wb-itemlink-label" lang="en" dir="ltr">(4S)-<span class="searchmatch">limonene</span> synthase</span> <span class="wb-itemlink-id">(Q4543797)</span></span></a>    </div><div class="searchresult"><span class="wb-itemlink-description">class of enzymes</span></div> <div class="mw-search-result-data">7 statements, 4 sitelinks - 09:04, 15 March 2021</div></li></ul><div class="mw-search-visualclear"/><p class="mw-search-pager-bottom">View (previous 20  |  <a href="/w/index.php?title=Special:Search&amp;limit=20&amp;offset=20&amp;profile=default&amp;search=limonene" title="Next 20 results" class="mw-nextlink">next 20</a>) (<a href="/w/index.php?title=Special:Search&amp;limit=20&amp;offset=0&amp;profile=default&amp;search=limonene" title="Show 20 results per page" class="mw-numlink">20</a> | <a href="/w/index.php?title=Special:Search&amp;limit=50&amp;offset=0&amp;profile=default&amp;search=limonene" title="Show 50 results per page" class="mw-numlink">50</a> | <a href="/w/index.php?title=Special:Search&amp;limit=100&amp;offset=0&amp;profile=default&amp;search=limonene" title="Show 100 results per page" class="mw-numlink">100</a> | <a href="/w/index.php?title=Special:Search&amp;limit=250&amp;offset=0&amp;profile=default&amp;search=limonene" title="Show 250 results per page" class="mw-numlink">250</a> | <a href="/w/index.php?title=Special:Search&amp;limit=500&amp;offset=0&amp;profile=default&amp;search=limonene" title="Show 500 results per page" class="mw-numlink">500</a>)</p>

        # lines = content.split("\\n")
        # for line in lines:
        #     print(">>", line)

    @classmethod
    def create_from_words(cls, terms, name=None, desc=None):
        if name is None:
            name="no_name"
        dictionary = SearchDictionary(name=name)
        dictionary.root = ET.Element("dictionary")
        dictionary.root.attrib["title"] = name
        if desc:
            desc_elem = ET.SubElement(dictionary.root, "desc")
            desc_elem.text = desc
        for term in terms:
            entry = ET.SubElement(dictionary.root, "entry")
            entry.attrib["name"] = term
            entry.attrib["term"] = term
        return dictionary


    @classmethod
    def test_create_from_words(cls):
        words = ["limonene", "alpha-pinene", "lantana camara"]
        dictionary = SearchDictionary.create_from_words(words, "test", "created from words")
        dictionary.add_wikidata_from_terms()
        print("dict", ET.tostring(dictionary.root, pretty_print=False))

    @classmethod
    def test(cls):
        from constants import PHYSCHEM_RESOURCES
        PLANT = os.path.join(PHYSCHEM_RESOURCES, "plant")
        sparql_file = os.path.join(PLANT, "plant_part_sparql.xml")
        dictionary_file = os.path.join(PLANT, "eoplant_part.xml")
        """
        <result>
            <binding name='item'>
                <uri>http://www.wikidata.org/entity/Q2923673</uri>
            </binding>
            <binding name='image'>
                <uri>http://commons.wikimedia.org/wiki/Special:FilePath/White%20Branches.jpg</uri>
            </binding>
        </result>
"""
        sparql_to_dictionary = {
            "id_name": "item",
            "sparql_name": "image",
            "dict_name": "image",
        }
        dictionary = SearchDictionary(dictionary_file)
        dictionary.update_from_sparqlx(sparql_file, sparql_to_dictionary)
        ff = dictionary_file[:-(len(".xml"))] + "_update" + ".xml"
        print("saving to", ff)
        dictionary.write(ff)

    @classmethod
    def test_plant(cls):
        """
        <result>
            <binding name='item'>
                <uri>http://www.wikidata.org/entity/Q2923673</uri>
            </binding>
            <binding name='image'>
                <uri>http://commons.wikimedia.org/wiki/Special:FilePath/White%20Branches.jpg</uri>
            </binding>
        </result>
        """

        from constants import CEV_OPEN_DICT_DIR
        import glob
        from shutil import copyfile

        PLANT_DIR = os.path.join(CEV_OPEN_DICT_DIR, "eoPlant")
        assert (os.path.exists(PLANT_DIR))
        dictionary_file = os.path.join(PLANT_DIR, "eoPlant.xml")
        assert (os.path.exists(dictionary_file))
        PLANT_SPARQL_DIR = os.path.join(PLANT_DIR, "sparql_output")
        assert (os.path.exists(PLANT_SPARQL_DIR))
        rename_file = False

        sparql_files = glob.glob(os.path.join(PLANT_SPARQL_DIR, "sparql_*.xml"))

        sparql_files.sort()
        sparql2amidict_dict = {
            "image" : {
                "id_name": "item",
                "sparql_name": "image_link",
                "dict_name": "image",
            },
            "taxon" : {
                "id_name": "item",
                "sparql_name": "taxon",
                "dict_name": "synonym",
            }
        }

    @classmethod
    def test_invasive(cls):
        """
        """

        from constants import CEV_OPEN_DICT_DIR
        import glob
        from shutil import copyfile

        INVASIVE_DIR = os.path.join(CEV_OPEN_DICT_DIR, "invasive_species")
        assert (os.path.exists(INVASIVE_DIR))
        dictionary_file = os.path.join(INVASIVE_DIR, "invasive_plant.xml")
        assert (os.path.exists(dictionary_file))
        SPARQL_DIR = os.path.join(INVASIVE_DIR, "sparql_output")
        assert (os.path.exists(SPARQL_DIR))
        rename_file = False

        sparql_files = glob.glob(os.path.join(SPARQL_DIR, "sparql_*.xml"))

        sparql_files.sort()
        sparql2amidict_dict = {
            "image": {
                "id_name": "item",
                "sparql_name": "image_link",
                "dict_name": "image",
            },
            "map": {
                "id_name": "item",
                "sparql_name": "taxon_range_map_image",
                "dict_name": "image",
            },
            # "taxon": {
            #     "id_name": "item",
            #     "sparql_name": "taxon",
            #     "dict_name": "synonym",
            # }
        }

        SearchDictionary.apply_dicts_and_sparql(dictionary_file, rename_file, sparql2amidict_dict, sparql_files)

    @classmethod
    def test_plant_genus(cls):
        """
        """

        from constants import CEV_OPEN_DICT_DIR
        import glob
        from shutil import copyfile

        DICT_DIR = os.path.join(CEV_OPEN_DICT_DIR, "plant_genus")
        assert (os.path.exists(DICT_DIR))
        dictionary_file = os.path.join(DICT_DIR, "plant_genus.xml")
        assert (os.path.exists(dictionary_file))
        SPARQL_DIR = os.path.join(DICT_DIR, "raw")
        assert (os.path.exists(SPARQL_DIR))
        rename_file = False

        sparql_files = glob.glob(os.path.join(SPARQL_DIR, "sparql_test_concatenation.xml"))

        sparql_files.sort()
        sparql2amidict_dict = {
            "image": {
                "id_name": "plant_genus",
                "sparql_name": "images",
                "dict_name": "image",
            },
            "map": {
                "id_name": "plant_genus",
                "sparql_name": "taxon_range_map_image",
                "dict_name": "map",
            },
            "wikipedia": {
                "id_name": "plant_genus",
                "sparql_name": "wikipedia",
                "dict_name": "wikipedia",
            },
            # "taxon": {
            #     "id_name": "item",
            #     "sparql_name": "taxon",
            #     "dict_name": "synonym",
            # }
        }

        SearchDictionary.apply_dicts_and_sparql(dictionary_file, rename_file, sparql2amidict_dict, sparql_files)

    @classmethod
    def test_compound(cls):
        """
        """

        from constants import CEV_OPEN_DICT_DIR
        import glob
        from shutil import copyfile

        DICT_DIR = os.path.join(CEV_OPEN_DICT_DIR, "eoCompound")
        assert (os.path.exists(DICT_DIR))
        dictionary_file = os.path.join(DICT_DIR, "plant_compound.xml")
        assert (os.path.exists(dictionary_file))
        SPARQL_DIR = os.path.join(DICT_DIR, "raw")
        SPARQL_DIR = DICT_DIR
        assert (os.path.exists(SPARQL_DIR))
        rename_file = False

        sparql_files = glob.glob(os.path.join(SPARQL_DIR, "sparql_6.xml"))

        sparql_files.sort()
        sparql2amidict_dict = {
            "image": {
                "id_name": "item",
                "sparql_name": "t",
                "dict_name": "image",
            },
            "chemform": {
                "id_name": "item",
                "sparql_name": "chemical_formula",
                "dict_name": "chemical_formula",
            },
            "wikipedia": {
                "id_name": "plant_genus",
                "sparql_name": "wikipedia",
                "dict_name": "wikipedia",
            },
            # "taxon": {
            #     "id_name": "item",
            #     "sparql_name": "taxon",
            #     "dict_name": "taxon",
            # }
        }

        SearchDictionary.apply_dicts_and_sparql(dictionary_file, rename_file, sparql2amidict_dict, sparql_files)

    @classmethod
    def test_plant_part(cls):
        """
        """
        # current dictionary does not need updating

        from constants import CEV_OPEN_DICT_DIR
        import glob
        from shutil import copyfile

        DICT_DIR = os.path.join(CEV_OPEN_DICT_DIR, "eoPlantPart")
        assert (os.path.exists(DICT_DIR))
        dictionary_file = os.path.join(DICT_DIR, "eoplant_part.xml")
        assert (os.path.exists(dictionary_file))
        SPARQL_DIR = os.path.join(DICT_DIR, "raw")
        SPARQL_DIR = DICT_DIR
        assert (os.path.exists(SPARQL_DIR))
        rename_file = False

        sparql_files = glob.glob(os.path.join(SPARQL_DIR, "sparql.xml"))

        sparql_files.sort()
        sparql2amidict_dict = {
            "image": {
                "id_name": "item",
                "sparql_name": "image",
                "dict_name": "image",
            },
        }

        SearchDictionary.apply_dicts_and_sparql(dictionary_file, rename_file, sparql2amidict_dict, sparql_files)

    @classmethod
    def apply_dicts_and_sparql(cls, dictionary_file, rename_file, sparql2amidict_dict, sparql_files):
        from shutil import copyfile

        keystring = ""
        # svae original file
        original_name = dictionary_file
        dictionary_root = os.path.splitext(dictionary_file)[0]
        save_file = dictionary_root + ".xml.save"
        copyfile(dictionary_file, save_file)
        for key in sparql2amidict_dict.keys():
            sparq2dict = sparql2amidict_dict[key]
            keystring += f"_{key}"
            for i, sparql_file in enumerate(sparql_files):
                assert (os.path.exists(sparql_file))
                dictionary = SearchDictionary(dictionary_file)
                dictionary.update_from_sparqlx(sparql_file, sparq2dict)
                dictionary_file = f"{dictionary_root}{keystring}_{i + 1}.xml"
                dictionary.write(dictionary_file)
        if rename_file:
            copyfile(dictionary_file, original_name)



class AmiDictionaries:

    ACTIVITY = "activity"
    COMPOUND = "compound"
    COUNTRY = "country"
    DISEASE = "disease"
    ELEMENT = "elements"
    INVASIVE_PLANT = "invasive_plant"
    PLANT_GENUS = "plant_genus"
    ORGANIZATION = "organization"
    PLANT_COMPOUND = "plant_compound"
    PLANT = "plant"
    PLANT_PART = "plant_part"
    SOLVENT = "solvents"

    ANIMAL_TEST = "animaltest"
    COCHRANE = "cochrane"
    COMP_CHEM = "compchem"
    CRISPR = "crispr"
    CRYSTAL = "crystal"
    DISTRIBUTION = "distributions"
    DITERPENE = "diterpene"
    DRUG = "drugs"
    EDGE_MAMMAL = "edgemammals"
    CHEM_ELEMENT = "elements"
    EPIDEMIC = "epidemic"
    ETHICS = "ethics"
    EUROFUNDER = "eurofunders"
    ILLEGAL_DRUG = "illegaldrugs"
    INN = "inn"
    INSECTICIDE = "insecticide"
    MAGNETISM = "magnetism"
    MONOTERPENE = "monoterpene"
    NAL = "nal"
    NMR = "nmrspectroscopy"
    OBESITY = "obesity"
    OPTOGENETICS = "optogenetics"
    PECTIN = "pectin"
    PHOTOSYNTH = "photosynth"
    PLANT_DEV = "plantDevelopment"
    POVERTY = "poverty"
    PROT_STRUCT = "proteinstruct"
    PROT_PRED = "protpredict"
    REFUGEE = "refugeeUNHCR"
    SESQUITERPENE = "sesquiterpene"
    SOLVENT = "solvents"
    STATISTICS = "statistics"
    TROPICAL_VIRUS = "tropicalVirus"
    WETLANDS = "wetlands"
    WILDLIFE = "wildlife"

    def __init__(self):
        self.create_search_dictionary_dict()

    def create_search_dictionary_dict(self):
        self.dictionary_dict = {}

#        / Users / pm286 / projects / CEVOpen / dictionary / eoActivity / eo_activity / Activity.xml
        self.add_with_check(AmiDictionaries.ACTIVITY,
                            os.path.join(CEV_OPEN_DICT_DIR, "eoActivity", "eo_activity", "activity.xml"))
        self.add_with_check(AmiDictionaries.COUNTRY,
                            os.path.join(OV21_DIR, "country", "country.xml"))
        self.add_with_check(AmiDictionaries.DISEASE,
                            os.path.join(OV21_DIR, "disease", "disease.xml"))
        self.add_with_check(AmiDictionaries.COMPOUND,
                            os.path.join(CEV_OPEN_DICT_DIR, "eoCompound", "plant_compound.xml"))
        self.add_with_check(AmiDictionaries.PLANT,
                            os.path.join(CEV_OPEN_DICT_DIR, "eoPlant", "plant.xml"))
        self.add_with_check(AmiDictionaries.PLANT_GENUS,
                            os.path.join(CEV_OPEN_DICT_DIR, "plant_genus", "plant_genus.xml"))
        self.add_with_check(AmiDictionaries.ORGANIZATION,
                            os.path.join(OV21_DIR, "organization", "organization.xml"))
        self.add_with_check(AmiDictionaries.PLANT_COMPOUND,
                            os.path.join(CEV_OPEN_DICT_DIR, "eoCompound", "plant_compound.xml"))
        self.add_with_check(AmiDictionaries.PLANT_PART,
                            os.path.join(CEV_OPEN_DICT_DIR, "eoPlantPart", "eoplant_part.xml"))
        self.add_with_check(AmiDictionaries.INVASIVE_PLANT,
                            os.path.join(CEV_OPEN_DICT_DIR, "Invasive_species", "invasive_plant.xml"))

        self.make_ami3_dictionaries()

# tests - will remove as soon as I have learnt how to do tests
        fail_test = False
        if fail_test:
            self.add_with_check("junk", "none") # should throw missing file
            self.add_with_check(AmiDictionaries.PLANT_PART,
                    os.path.join(CEV_OPEN_DICT_DIR, "eoPlantPart", "eoplant_part.xml"))  # should throw duplicate key

#        self.print_dicts()
        return self.dictionary_dict

    def print_dicts(self):
        print("DICTIONARIES LOADED")
        dd = dir(self)
        for d in dd:
            if d[0].isupper():
                print(">>", d)

    def make_ami3_dictionaries(self):

        self.ami3_dict_index = {
            AmiDictionaries.ANIMAL_TEST : os.path.join(DICT_AMI3, "animaltest.xml"),
            AmiDictionaries.COCHRANE : os.path.join(DICT_AMI3, "cochrane.xml"),
            AmiDictionaries.COMP_CHEM : os.path.join(DICT_AMI3, "compchem.xml"),
            AmiDictionaries.CRISPR : os.path.join(DICT_AMI3, "crispr.xml"),
            AmiDictionaries.CRYSTAL : os.path.join(DICT_AMI3, "crystal.xml"),
            AmiDictionaries.DISTRIBUTION : os.path.join(DICT_AMI3, "distributions.xml"),
            AmiDictionaries.DITERPENE : os.path.join(DICT_AMI3, "diterpene.xml"),
            AmiDictionaries.DRUG : os.path.join(DICT_AMI3, "drugs.xml"),
            AmiDictionaries.EDGE_MAMMAL : os.path.join(DICT_AMI3, "edgemammals.xml"),
            AmiDictionaries.ETHICS : os.path.join(DICT_AMI3, "ethics.xml"),
            AmiDictionaries.CHEM_ELEMENT : os.path.join(DICT_AMI3, "elements.xml"),
            AmiDictionaries.EPIDEMIC : os.path.join(DICT_AMI3, "epidemic.xml"),
            AmiDictionaries.EUROFUNDER: os.path.join(DICT_AMI3, "eurofunders.xml"),
            AmiDictionaries.ILLEGAL_DRUG : os.path.join(DICT_AMI3, "illegaldrugs.xml"),
            AmiDictionaries.INN : os.path.join(DICT_AMI3, "inn.xml"),
            AmiDictionaries.INSECTICIDE : os.path.join(DICT_AMI3, "insecticide.xml"),
            AmiDictionaries.MAGNETISM : os.path.join(DICT_AMI3, "magnetism.xml"),
            AmiDictionaries.MONOTERPENE : os.path.join(DICT_AMI3, "monoterpene.xml"),
            AmiDictionaries.NAL : os.path.join(DICT_AMI3, "nal.xml"),
            AmiDictionaries.NMR : os.path.join(DICT_AMI3, "nmrspectroscopy.xml"),
            AmiDictionaries.OBESITY : os.path.join(DICT_AMI3, "obesity.xml"),
            AmiDictionaries.OPTOGENETICS : os.path.join(DICT_AMI3, "optogenetics.xml"),
            AmiDictionaries.PECTIN : os.path.join(DICT_AMI3, "pectin.xml"),
            AmiDictionaries.PHOTOSYNTH : os.path.join(DICT_AMI3, "photosynth.xml"),
            AmiDictionaries.PLANT_DEV : os.path.join(DICT_AMI3, "plantDevelopment.xml"),
            AmiDictionaries.POVERTY : os.path.join(DICT_AMI3, "poverty.xml"),
            AmiDictionaries.PROT_STRUCT : os.path.join(DICT_AMI3, "proteinstruct.xml"),
            AmiDictionaries.PROT_PRED : os.path.join(DICT_AMI3, "protpredict.xml"),
            AmiDictionaries.REFUGEE : os.path.join(DICT_AMI3, "refugeeUNHCR.xml"),
            AmiDictionaries.SESQUITERPENE : os.path.join(DICT_AMI3, "sesquiterpene.xml"),
            AmiDictionaries.SOLVENT : os.path.join(DICT_AMI3, "solvents.xml"),
            AmiDictionaries.STATISTICS : os.path.join(DICT_AMI3, "statistics.xml"),
            AmiDictionaries.TROPICAL_VIRUS : os.path.join(DICT_AMI3, "tropicalVirus.xml"),
            AmiDictionaries.WETLANDS : os.path.join(DICT_AMI3, "wetlands.xml"),
            AmiDictionaries.WILDLIFE : os.path.join(DICT_AMI3, "wildlife.xml"),
        }

        for item in self.ami3_dict_index.items():
            self.add_with_check(item[0], item[1])


    def add_with_check(self, key, file):
#        print("adding dictionary", file)
        if key in self.dictionary_dict:
            raise Exception("duplicate dictionary key " + key + " in "+ str(self.dictionary_dict))
        Util.check_exists(file)
        try:
            dictionary = SearchDictionary(file)
            self.dictionary_dict[key] = dictionary
        except Exception as ex:
            print("Failed to read dictionary", file, ex)
#        print(dictionary.get_or_create_term_set())
        return


def main():
    """ debugging """
    option = "sparql"
    option = "plant"
    option = "invasive"
    option = "genus"
    option = "compound"
    option = "plant_part"
    option = "test_dict"
    if option == "sparql":
        SearchDictionary.test()
    elif option == "plant":
        SearchDictionary.test_plant()
    elif option == "invasive":
        SearchDictionary.test_invasive()
    elif option == "genus":
        SearchDictionary.test_plant_genus()
    elif option == "compound":
        SearchDictionary.test_compound()
    elif option == "plant_part":
        SearchDictionary.test_plant_part()
    elif option == "test_dict":
        SearchDictionary.test_create_from_words()
    else:
        print("no option given")


if __name__ == "__main__":
    print("running search main")
    main()
else:

    #    print("running search main anyway")
    #    main()
    pass

