
from graphviz import Graph

class AmiGraph():
    def __init__(self):
        self.graph = None

    def create_graph(self, file='graph.gv', engine='sfdp'):
        self.graph = Graph('G', filename=file, engine=engine)

    def add_edge(self, from_node, to_node):
        self.graph.edge(from_node, to_node)

    def view(self):
        self.graph.view()

    def add_dict(self, node0, node1, d_dict):
        self.add_edge(node0, node1)
        for n0 in d_dict:
            print(n0, d_dict[n0])
            self.add_edge(n0, d_dict[n0])
            self.add_edge(node1, n0)

def dictionaries():
    ami_graph = AmiGraph()
    ami_graph.create_graph()

    ov_dict = {
        "ov_country.d" : "country.xml",
        "ov_disease.d" : "disease.xml",
        "ov_drug.d" : "drug.xml",
        "ov_organization.d" : "organization.xml",
        "ov_virus.d" : "virus.xml",
    }

    eo_dict = {
        "e0_activity.d" : "activity.xml",
        "e0_analysis_method.d" : "eoAnalysisMethod.xml",
        "e0_compound.d" : "plant_compound.xml",
        "e0_extraction_method.d" : "eoExtractionMethod.xml",
        "e0_tpsgene.d" : "e0_Gene.xml",
        "e0_plant.d" : "e0_plant.xml",
        "e0_plant_material_history.d" : "eoPlantMaterialHistory.xml",
        "e0_plant_part.d" : "eoplant_part.xml",
        "e0_target_organism.d" : "eoTargetOrganism.xml",
        "invasive_plant.d" : "invasive_plant.xml",
        "pests.d" : "pests.xml",
        "plant_genus.d" : "plant_genus.xml",
    }

    ami_graph.add_dict("orig", "ov", ov_dict)
    ami_graph.add_dict("orig", "eo", eo_dict)

    ami_graph.view()


def main():
    dictionaries()

if __name__ == '__main__':
    main()