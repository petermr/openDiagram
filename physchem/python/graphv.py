
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
        "ov_country.d" : "country",
        "ov_disease.d" : "disease",
        "ov_drug.d" : "drug",
        "ov_org.d" : "organization",
        "ov_virus.d" : "virus",
    }

    eo_dict = {
        "e0_activity.d" : "activity",
        "e0_analysis.d" : "Method",
        "e0_compound.d" : "compound",
        "e0_extraction.d" : "eMethod",
        "e0_tpsgene.d" : "e0_Gene",
        "e0_plant.d" : "e0_plant",
        "e0_material.d" : "History",
        "e0_part.d" : "eoplant_part",
        "e0_organism.d" : "Organism",
        "invasive_plant.d" : "invasive_plant",
        "pests.d" : "pests",
        "genus.d" : "plant_genus",
    }

    ami_graph.add_dict("orig", "ov", ov_dict)
    ami_graph.add_dict("orig", "eo", eo_dict)

    ami_graph.view()


def main():
    dictionaries()

if __name__ == '__main__':
    main()