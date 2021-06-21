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



#  html tags/attributes


# elements in amidict
DICTIONARY = "dictionary"
ENTRY = "entry"
IMAGE = "image"
TITLE = "title"
WIKIPEDIA = "wikipedia"

# attributes in amidict
DESC = "desc"
NAME = "name"
TERM = "term"
WIKIDATA_ID = "wikidataID"
WIKIDATA_URL = "wikidataURL"
WIKIDATA_SITE = "https://www.wikidata.org/wiki/"
WIKIPEDIA_PAGE = "wikipediaPage"
# elements

class SearchDictionary:
    """wrapper for an ami dictionary including search flags

    """
    TERM = "term"

    def __init__(self, xml_file=None, name=None, wikilangs=None, **kwargs):
        self.amidict = None
        self.entries = []
        self.entry_by_term = {}
        self.entry_by_wikidata_id = {}
        self.file = xml_file
        self.ignorecase = None
        self.name = None
        self.root = None
        self.sparql_result_list = None
        self.sparql_result_by_wikidata_id = None
        self.sparql_to_dictionary = None
        self.split_terms = False
        self.term_set = set()
        self.wikilangs = wikilangs

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

    @classmethod
    def create_from_words(cls, terms, name=None, desc=None, wikilangs=None):
        """use raw list of words and lookup each. choosing WD page and using languages """
        if name is None:
            name="no_name"
        dictionary = SearchDictionary(name=name, wikilangs=wikilangs)
        dictionary.root = ET.Element(DICTIONARY)
        dictionary.root.attrib[TITLE] = name
        if desc:
            desc_elem = ET.SubElement(dictionary.root, DESC)
            desc_elem.text = desc
        for term in terms:
            entry = ET.SubElement(dictionary.root, ENTRY)
            entry.attrib[NAME] = term
            entry.attrib[TERM] = term
            dictionary.entries.append(entry)
        return dictionary

    def read_dictionary_from_xml_file(self, file, ignorecase=True):
        self.file = file
        self.amidict = ET.parse(file, parser=ET.XMLParser(encoding="utf-8"))
        self.root = self.amidict.getroot()
        self.name = self.root.attrib["title"]
        self.ignorecase = ignorecase

        self.entries = list(self.root.findall(ENTRY))
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
        image_url = entry.find(".//" + IMAGE)
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
        return matched

    def get_entry(self, term):
        if self.entry_by_term is None:
            self.create_entry_by_term()
        entry = self.entry_by_term[term] if term in self.entry_by_term else None
        if entry is None:
            print("entry by term", self.entry_by_term)
            pass
        return entry

    def create_entry_by_term(self):
        self.entry_by_term = {self.term_from_entry(entry) : entry  for entry in self.entries}

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

    def write(self, file):
        from lxml import etree
        et = etree.ElementTree(self.root)
        with open(file, 'wb') as f:
            et.write(f, encoding="utf-8", xml_declaration=True, pretty_print=True)

    def add_wikidata_from_terms(self):
        from wikimedia import WikidataLookup, WikidataPage

        wikidata_lookup = WikidataLookup()
        entries = self.root.findall(ENTRY)
        for entry in entries:
            term = entry.attrib[TERM]
            qitem, desc, qitems = wikidata_lookup.lookup_wikidata(term)
            entry.attrib[WIKIDATA_ID] = qitem
            entry.attrib[WIKIDATA_URL] = WIKIDATA_SITE + qitem
            entry.attrib[DESC] = desc
            synonym = ET.SubElement(entry, "synonym")
            synonym.attrib["type"] = "wikidata_hits"
            synonym.text = str(qitems)
            wikidata_page = WikidataPage(qitem)
            wikipedia_dict = wikidata_page.get_wikipedia_page_links(self.wikilangs)
            self.add_wikipedia_page_links(entry, wikipedia_dict)

    def add_wikipedia_page_links(self, entry, wikipedia_dict):
        for wp in wikipedia_dict.items():
            if wp[0] == "en":
                entry.attrib[WIKIPEDIA_PAGE] = wp[1]
            else:
                wikipedia = ET.SubElement(entry, WIKIPEDIA)
                wikipedia.attrib["lang"] = wp[0]
                wikipedia.text = wp[1]

    def create_wikidata_page(self, entry_element):
        from wikimedia import WikidataPage

        # refactor this - make entry a class
        wikidata_page = None
        qitem = entry_element.attrib[WIKIDATA_ID]
        if qitem is not None:
            wikidata_page = WikidataPage(qitem)

        return wikidata_page


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


if __name__ == "__main__":
    print("running search main")
    main()
else:

    #    print("running search main anyway")
    #    main()
    pass

