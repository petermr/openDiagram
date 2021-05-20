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

    def __init__(self, file, **kwargs):
        self.amidict = None
        self.root = None
        self.name = None
        self.entries = []
        self.entry_by_wikidata_id = {}
        self.file = file
        self.ignorecase = None
        self.entries = []
        self.term_set = set()

        if not os.path.exists(file):
            raise IOError("cannot find file " + str(file))
        self.read_dictionary(file)
        self.name = file.split("/")[-1:][0].split(".")[0]
        self.options = {} if not "options" in kwargs else kwargs["options"]
        if "synonyms" in self.options:
            print("use synonyms")
        if "noignorecase" in self.options:
            print("use case")
        self.split_terms = True
        self.split_terms = False

    def read_dictionary(self, file, ignorecase=True):
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
            uri = list(result.findall("SPQ:binding[@name='%s']/SPQ:uri" % id_element, NS_MAP))[0]
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
        entry.append(entry_child)
#        print(">>", ET.tostring(entry))

    def write(self, file):
        from lxml import etree
        et = etree.ElementTree(self.root)
        with open(file, 'wb') as f:
            et.write(f, encoding="utf-8", xml_declaration=True, pretty_print=True)

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
        ff = dictionary_file[:-(len(".xml"))]+"_update"+".xml"
        print("saving to", ff)
        dictionary.write(ff)


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
    if option == "sparql":
        SearchDictionary.test()
    else:
        print("no option given")


if __name__ == "__main__":
    print("running search main")
    main()
else:

    #    print("running search main anyway")
    #    main()
    pass

