import logging


class PyAMI:
    def __init__(self):
        self.args = {}
        self.logger = logging.getLogger()

    def create_arg_parser(self):
        import argparse
        parser = argparse.ArgumentParser(description='Search sections with dictionaries and patterns')
        """
        """
        parser.add_argument('-d', '--dict', nargs="*",  # default=[AmiDictionaries.COUNTRY],
                            help='dictionaries to ami-search with, _help gives list')
        parser.add_argument('-g', '--glob', nargs="*",
                            help='glob files; python syntax (* and ** wildcards supported); '
                                 'include alternatives in {...,...}. ')
        parser.add_argument('-s', '--sect', nargs="*",  # default=[AmiSection.INTRO, AmiSection.RESULTS],
                            help='sections to search; _help gives all(?)')
        parser.add_argument('-p', '--proj', nargs="*",
                            help='projects to search; _help will give list')
        parser.add_argument('-c', '--config', nargs="*", default="pyami.ini,~/pyami/config.ini,D:/foo/pyami.ini",
                            help='config file(s) (NYI); _help will give list')
        parser.add_argument('--patt', nargs="+",
                            help='patterns to search with (NYI); regex may need quoting')
        parser.add_argument('--demo', nargs="*",
                            help='simple demos (NYI). empty gives list. May need downloading corpora')
        parser.add_argument('-l', '--loglevel', default="info",
                            help='log level (NYI)')
        parser.add_argument('--plot', action="store_false",
                            help='plot params (NYI)')
        parser.add_argument('--nosearch', action="store_true",
                            help='search (NYI)')
        parser.add_argument('--maxbars', nargs="?", type=int, default=25,
                            help='max bars on plot (NYI)')
        parser.add_argument('--outfile', type=str,
                            help='output file, normally 1. but may track multiple input dirs (NYI)')
        parser.add_argument('--languages', nargs="+", default=["en"],
                            help='languages (NYI)')
        parser.add_argument('--debug', nargs="+",
                            help='debugging commands , numbers, (not formalised)')
        return parser

    def run_args(self, arglist=None):
        import sys

        if arglist is None:
            arglist = []
        parser = self.create_arg_parser()
            # https://stackoverflow.com/questions/31090479/python-argparse-pass-values-without-command-line
        self.args = PyAMI.extract_parsed_arg_tuples(arglist, parser)

        self.set_loglevel_from_args()
        self.process_config_files()
        if self.args["proj"] and (self.args["sect"] or self.args["glob"]):
            self.make_files()

    @classmethod
    def extract_parsed_arg_tuples(cls, arglist, parser):
        parsed_args = parser.parse_args() if not arglist else parser.parse_args(arglist)
        args = {item[0]: item[1] for item in list(vars(parsed_args).items())}
        return args

    def set_loglevel_from_args(self):
        levels = {
            "debug" : logging.DEBUG,
            "info" : logging.INFO,
            "warning": logging.WARNING,
            "error": logging.ERROR,
        }
        loglevel = self.args["loglevel"]
        if loglevel is not None and loglevel.lower() in levels:
            level = levels[loglevel.lower()]
            print("LEVEL", level)
            self.logger.setLevel(level)

    def make_files(self):
        import glob
        import pathlib
        import file_lib
        logging.info("globbing")
        if not self.args["proj"]:
            logging.error("glob requires proj")
        else:
            glob_ = self.args["glob"][0]
            logging.info(f"glob: {glob_}")
            files = glob.glob(glob_)
            self.outfile = self.args["outfile"]
            file_lib.FileLib.force_write(self.outfile, str(files), overwrite=True)

    def process_config_files(self):
        config_files_str = self.args["config"]
        config_files = [] if config_files_str is None else config_files_str.split(",")
        for config_file in config_files:
            self.process_config_file(config_file)

    def process_config_file(self, config_file):
        import os
        from file_lib import FileLib
        if "/" not in config_file:
            file = os.path.join(FileLib.get_parent_dir(__file__), config_file)
        elif config_file.startswith("~"): # relative to home
            home = os.path.expanduser("~")
            file = home + config_file[len("~"):]
        elif config_file.startswith("/"): # absolute
            file = config_file
        else:
            file = None

        if file is not None:
            if os.path.exists(file):
                logging.info("reading "+file)
                self.apply_config_file(file)
            else:
                logging.warning(f"cannot find config file {file}")

    def apply_config_file(self, file):
        """ reads config file, recursively replaces {} symbols and '~'
        :file: python config file
        """
        import configparser
        import os
        from file_lib import FileLib

        symbols = {}
# https://stackoverflow.com/questions/54351740/how-can-i-use-f-string-with-a-variable-not-with-a-string-literal

        config = configparser.ConfigParser()
        config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
        logging.warning(f"\nreading {file}\n")
        files_read = config.read(file)
        sections = config.sections()
        for section in sections:
            print ("============"+section+"============")
            for name in config[section].keys():
                if name in symbols:
                    logging.error(f"{name} already defined, skipped")
                else:
                    raw_value = config[section][name]
                    # make substitutions
                    # we replace __file__ with parent dir of dictionary
                    parent_dir = str(FileLib.get_parent_dir(file))
                    if raw_value.startswith("~"):
                        new_value = os.path.expanduser("~")+raw_value[len("~"):]
                    # elif raw_value == "__file__":
                    #     new_value = parent_dir
                    elif raw_value.startswith("__file__"):
                        #  the prefix __file__ has been added by the parser
                        new_value = parent_dir + raw_value[len("__file__"):]
                    else:
                        new_value = raw_value

                    symbols[name] = new_value


        # print(f"\nCONFIG {symbols}\n")
        for item in symbols.items():
            val = item[1];
            if os.path.exists(val):
                pass
            elif val.startswith("http"):
                import urllib.request
                with urllib.request.urlopen('http://python.org/') as response:
                    html = response.read()
            else:
                print("non-existent: "+val+" in " + file)

        self.recurse_ini_files(symbols)

    def recurse_ini_files(self, symbols):
        for name in symbols.keys():
            if name.endswith("_ini"):
                file = symbols[name]
                self.apply_config_file(file)


def main():
    import os
    from util import Util
    print("\n", "============== running pyami main ===============")
    pyami = PyAMI()
    test_glob(pyami)


def test_glob(pyami):
    import os

    dir_ = "/Users/pm286/projects/openDiagram/physchem/resources/oil26"
    projdir = "~/projects/openDiagram/physchem/resources/oil26"
    glob_ = "**/*.xml"
    globstring = "--glob", f"{dir_}/{glob_}"
    output_dir = f"{dir_}/files"
    outfile = f"{output_dir}/xml_files.txt"
    pyami.run_args([
                    "--glob", f"{dir_}/**/*.xml",
                    "--proj", projdir,
                    "--outfile", outfile
                    ])
    assert(os.path.exists(os.path.exists(outfile)))


# "--config", # defaults to config.ini,~/pyami/config.ini if omitted

if __name__ == "__main__":
    main()

else:

    print("running search main anyway")
    main()
    pass

