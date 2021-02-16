import os, glob, copy
from file_lib import AmiPath
from text_lib import FileSection

PYDIAG = "../../python/diagrams"

class AmiSearch():

    def __init__(self):
        pass

    
def main():
    print("started search")
    project = os.path.join(PYDIAG, "satish/cct")
    sections_path = AmiPath.create(AmiPath.T_SECTIONS, {"PROJ": "../liion", "SUBSECT": "*_body*", "SUBSUB": "**", "FILE": "*p", })
    files = sections_path.get_globbed_files()
    for file in files:
        print("file", file)
#        file_section = FileSection()
#        file_section.analyze_file_contents(file)
#    for word in {"steel", "continuous"}

    print("files", len(files))
    print("finished search")

if __name__ == "__main__":
    print("running search main")
    main()
else:
#    print("running search main anyway")
#    main()
    pass