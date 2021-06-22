import logging
import sys
import os
from file_lib import FileLib


class PyAMI:
    PARENT = "__parent__" # indicates parent directory of an INI or similar file
    NS = "${ns}"

    def __init__(self):
        self.args = {}
        self.logger = logging.getLogger()
        self.symbols = None
        self.config = None
        self.current_file = None
        self.symbols = None
        self.fileset = None
        self.check_urls = False


    def create_arg_parser(self):
        """ creates adds the arguments for pyami commandline
        """
        import argparse
        parser = argparse.ArgumentParser(description='Search sections with dictionaries and patterns')
        parser.add_argument('-d', '--dict', nargs="+",
                            help='dictionaries to ami-search with, _help gives list')
        parser.add_argument('-g', '--glob', nargs="+",
                            help='glob files; python syntax (* and ** wildcards supported); '
                                 'include alternatives in {...,...}. ')
        parser.add_argument('-s', '--sect', nargs="+",  # default=[AmiSection.INTRO, AmiSection.RESULTS],
                            help='sections to search; _help gives all(?)')
        parser.add_argument('-p', '--proj', nargs="*",
                            help='projects to search; _help will give list')
        parser.add_argument('-c', '--config', nargs="*", default="${PYAMI}",
                            help='list of config file(s) or environment vars')
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

    def run_commands(self, arglist=None):

        self.setup_environment()

        self.parse_and_run_args(arglist)
        self.print_symbols()

    def print_symbols(self):
        print("symbols>>")
        for name in self.symbols:
            print(f"{name}:{self.symbols[name]}")

    def setup_environment(self):
        for key in os.environ.keys():
            logging.debug(f"{key}: {os.environ[key]}")

    def parse_and_run_args(self, arglist):
        if arglist is None:
            arglist = []
        parser = self.create_arg_parser()
        # https://stackoverflow.com/questions/31090479/python-argparse-pass-values-without-command-line
        self.args = PyAMI.extract_parsed_arg_tuples(arglist, parser)
        logging.info("ARGS: "+str(self.args))
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
        self.symbols = {}
        self.fileset = set()
        for config_file in config_files:
            self.process_config_file(config_file)

    def process_config_file(self, config_file):
        import os
        from file_lib import FileLib
        if config_file.startswith("${") and config_file.endswith("}"):  # python config file
            file = os.environ[config_file[2:-1]]
        elif "/" not in config_file:
            file = os.path.join(FileLib.get_parent_dir(__file__), config_file)
        elif config_file.startswith("~"): # relative to home
            home = os.path.expanduser("~")
            file = home + config_file[len("~"):]
        elif config_file.startswith("/"):  # absolute
            file = config_file
        else:
            file = None

        if file is not None:
            if os.path.exists(file):
                logging.debug("reading "+file)
                self.apply_config_file(file)
            else:
                logging.warning(f"cannot find config file {file}")

    def apply_config_file(self, file):
        """ reads config file, recursively replaces {} symbols and '~'
        :file: python config file
        """
        import configparser
        import os

        if file in self.fileset: # avoid cycles
            logging.debug(f"{file} already in {self.fileset}")
            return;
        else:
            self.fileset.add(file)
# https://stackoverflow.com/questions/54351740/how-can-i-use-f-string-with-a-variable-not-with-a-string-literal

        self.config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
        logging.debug(f"\nreading {file}\n")
        files_read = self.config.read(file)
        sections = self.config.sections()
        for section in sections:
            self.expand_section_into_symbols_dict(file, section)

        self.check_targets_exist(file)
        self.recurse_ini_files()

    def check_targets_exist(self, file):
        for item in self.symbols.items():
            val = item[1];
            if val.startswith("http"):
                if self.check_urls:
                    import urllib.request
                    try:
                        with urllib.request.urlopen(val) as response:
                            html = response.read()
                    except urllib.error.HTTPError as ex:
                        print(f"Cannot read {val} as url {ex}")
            elif "/" in val:  # assume slash means file or url
                if not os.path.exists(val):  # all files
                    logging.error(f"{val} in {file} does not exist as file")
            else:
                print("non-existent: " + val + " in " + file)

    def expand_section_into_symbols_dict(self, file, section):
        print("============" + section + "============" + file)
        for name in self.config[section].keys():
            if name in self.symbols:
                logging.debug(f"{name} already defined, skipped")
            else:
                raw_value = self.config[section][name]
                # make substitutions
                # we replace __file__ with parent dir of dictionary
                parent_dir = str(FileLib.get_parent_dir(file))
                if raw_value.startswith("~"):
                    # home directory on all OS (?)
                    new_value = os.path.expanduser("~") + raw_value[len("~"):]
                elif raw_value.startswith(self.PARENT):
                    #  the prefix __file__ may have been expanded by the parser
                    new_value = parent_dir + raw_value[len(self.PARENT):]
                elif raw_value.startswith("__file__"):
                    print("__file__ is obsolete ", file)
                else:
                    new_value = raw_value

                if name.startswith(self.NS):
                    name = os.environ["LOGNAME"] + name[len(self.NS):]
                    print("NAME", name)

                self.symbols[name] = new_value

        logging.debug(f"symbols for {file} {section}\n {self.symbols}")

    def recurse_ini_files(self):
        """follows links to all *_ini files and runs them recursively

        does not check for cycles (yet)"""
        keys = list(self.symbols.keys())
        for name in keys:
            if name.endswith("_ini"):
                if name not in self.symbols:
                    logging.error(f"PROCESSING {self.current_file} ; cannot find symbol: {name} in {self.symbols}")
                else:
                    file = self.symbols[name]
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
    pyami.run_commands([
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

