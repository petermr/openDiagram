
import xml.etree.ElementTree as ET

import sys, os, glob

class FileLib():

    def __init__(self):
        self.recurse = False
        pass

    def set_glob(self, glob_path, recurse=True):
        self.glob_path = glob_path
        self.recurse = recurse
        self.cwd = os.getcwd()


    def get_globbed_files(self):
        files = glob.glob(self.glob_path, recursive=self.recurse)
        return files


    def test(self):

        print("cwd=", self.cwd, "path=", self.glob_path, "recurse=", self.recurse)
        print("glob_files", self.get_globbed_files())



def main():
    print("started file_lib")
    flib = FileLib();
    flib.cwd = os.getcwd()
    flib.glob_path = "../**/*.py"
    files = flib.get_globbed_files()
    print("glob", str(len(files)), files)
    flib.cwd = os.path.abspath("../liion/")
    print("cwd1", flib.cwd, os.path.exists(flib.cwd))
    flib.recurse = True
    flib.glob_path = "../liion/*/sections/*_body/**/*.xml"
    files = flib.get_globbed_files()
    print("glob1", str(len(files)), files)

    print("finished file_lib")


if __name__ == "__main__":
    main()
else:
    main()