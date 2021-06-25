import logging
import sys
import os
from file_lib import FileLib
from xml_lib import XmlLib


class PyAMI:
    OUTFILE = "outfile"

    # flags
    APPLY         = "apply"
    CHECK_URLS    = "check_urls"
    COMBINE       = "combine"
    PRINT_SYMBOLS = "print_symbols"
    RECURSE       = "recurse"
    # methods
    REMOVE_TAGS = "remove_tags"
    CONCAT_STR = "concat_str"

    def __init__(self):
        self.args = {} # args captured in here as name/value without "-" or "--"
        self.logger = logging.getLogger()
        self.apply = []
        self.combine = None
        self.config = None
        self.current_file = None
        self.fileset = None
        self.file_dict = {}
        self.func_dict = {}
        self.set_flags()
        self.set_funcs()
        self.symbol_ini = SymbolIni(self)
        print(f"symbols {self.symbol_ini.symbols}")

    def set_flags(self):
        self.flag_dict = {}
        self.flag_dict[self.APPLY] = None
        self.flag_dict[self.CHECK_URLS] = None
        self.flag_dict[self.COMBINE] = None
        self.flag_dict[self.PRINT_SYMBOLS] = None
        self.flag_dict[self.RECURSE] = True

    def set_funcs(self):
        self.func_dict[self.REMOVE_TAGS] = XmlLib.remove_all_tags

    def create_arg_parser(self):
        """ creates adds the arguments for pyami commandline
        """
        import argparse
        parser = argparse.ArgumentParser(description='Search sections with dictionaries and patterns')
        parser.add_argument('--apply', nargs="+",
                            help='list of sequential transformations to apply to pipeline')
        parser.add_argument('--combine', nargs=1,
                            help='(NYI) operation to combine files into final object')
        parser.add_argument('-c', '--config', nargs="*", default="${PYAMI}",
                            help='list of config file(s) or environment vars')
        parser.add_argument('--debug', nargs="+",
                            help='debugging commands , numbers, (not formalised)')
        parser.add_argument('--demo', nargs="*",
                            help='simple demos (NYI). empty gives list. May need downloading corpora')
        parser.add_argument('-d', '--dict', nargs="+",
                            help='dictionaries to ami-search with, _help gives list')
        parser.add_argument('-g', '--glob', nargs="+",
                            help='glob files; python syntax (* and ** wildcards supported); '
                                 'include alternatives in {...,...}. ')
        parser.add_argument('--languages', nargs="+", default=["en"],
                            help='languages (NYI)')
        parser.add_argument('-l', '--loglevel', default="info",
                            help='log level (NYI)')
        parser.add_argument('--maxbars', nargs="?", type=int, default=25,
                            help='max bars on plot (NYI)')
        parser.add_argument('--nosearch', action="store_true",
                            help='search (NYI)')
        parser.add_argument('--outfile', type=str,
                            help='output file, normally 1. but (NYI) may track multiple input dirs (NYI)')
        parser.add_argument('--patt', nargs="+",
                            help='patterns to search with (NYI); regex may need quoting')
        parser.add_argument('-p', '--proj', nargs="*",
                            help='projects to search; _help will give list')
        parser.add_argument('-s', '--sect', nargs="+",  # default=[AmiSection.INTRO, AmiSection.RESULTS],
                            help='sections to search; _help gives all(?)')
        parser.add_argument('--plot', action="store_false",
                            help='plot params (NYI)')
        return parser

    def run_commands(self, arglist=None):

        arglist = self.symbol_ini.replace_symbols(arglist)
        self.parse_and_run_args(arglist)
        if self.flagged(self.PRINT_SYMBOLS) or True:
            self.symbol_ini.print_symbols()


    def parse_and_run_args(self, arglist):
        if arglist is None:
            arglist = []
        parser = self.create_arg_parser()
        # https://stackoverflow.com/questions/31090479/python-argparse-pass-values-without-command-line
        self.args = PyAMI.extract_parsed_arg_tuples(arglist, parser)
        logging.info("ARGS: "+str(self.args))
        self.set_loglevel_from_args()
        #  workflow needs thinking about...

        if self.args["proj"] and (self.args["sect"] or self.args["glob"]):
            self.run_file_workflow()

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

    def run_file_workflow(self):
        import glob
        import pathlib
        import file_lib
        logging.info("globbing")
        if not self.args["proj"]:
            logging.error("glob requires proj")
        else:
            glob_recurse=self.flagged(self.RECURSE)
            glob_ = self.args["glob"][0]
            logging.info(f"glob: {glob_}")
            self.file_dict = {file:None for file in glob.glob(glob_, recursive=glob_recurse)}
            print(self.file_dict)
        if self.APPLY in self.args:
            self.read_file_content()
            apply_ = self.args[self.APPLY]
            print(f"apply {apply_}")
            if apply_ and len(apply_) > 0:
                apply = apply_[0]
                print("apply", apply)
                func = self.func_dict[apply]
                if (func is None):
                    logging.error(f"Cannot find func for {apply}")
                else:
                # apply = XmlLib.remove_all_tags
                    self.apply_to_file_content(func)
        if self.COMBINE in self.args:
            self.combine_files_to_object()
        if self.OUTFILE in self.args:
            self.write_output()

    def read_file_content(self, to_str=True):
        """read file content as bytes into file_dict

        :to_str: if true convert content to strings
        """
        for file in self.file_dict:
            with open(file, "r") as f:
                data = f.read()
                if to_str and isinstance(data, bytes):
                    data = data.decode("utf-8")
                self.file_dict[file] = data

    def apply_to_file_content(self, func):
        """applies func to all string content in file_dict
        """
        for file in self.file_dict:
            data = self.file_dict.get(file)
            new_data = func(data)
            self.file_dict[file] = new_data

    def combine_files_to_object(self):
        methods = self.args.get(self.COMBINE)
        if methods[0] == self.CONCAT_STR:
            self.result = "\n".join(self.file_dict.values())
            # print(self.result)

    def write_output(self):
        if self.result: # single output
            self.outfile = self.args[self.OUTFILE]
            FileLib.force_write(self.outfile, self.result, overwrite=True)
            logging.warning(f"wrote {self.outfile}")

    def flagged(self, flag):
        """is flag set in flag_dict

        if flag is in flag_dict and not falsy return true
        :flag:

        """
        return True if self.flag_dict.get(flag) else False

class SymbolIni:
    """processes config/ini files and stores symbols created
    """
    NS = "${ns}"
    PARENT = "__parent__" # indicates parent directory of an INI or similar file

    def __init__(self, pyami):
        self.symbols = None
        self.pyami = pyami

        self.setup_environment()
        self.process_config_files()

    def process_config_files(self):
        logging.warning(f"args {self.pyami.args}")
        # remove later
        if not self.pyami.args:
            self.pyami.args["config"] = "/Users/pm286/pyami/config.ini"
        config_files_str = self.pyami.args.get("config")
        config_files = [] if config_files_str is None else config_files_str.split(",")
        self.symbols = {}
        self.fileset = set()
        for config_file in config_files:
            self.process_config_file(config_file)
        print(f"symbols after config {self.symbols}")

    def process_config_file(self, config_file):
        import os
        from file_lib import FileLib
        if config_file.startswith("${") and config_file.endswith("}"):  # python config file
            file = os.environ[config_file[2:-1]]
        elif "/" not in config_file:
            file = os.path.join(FileLib.get_parent_dir(__file__), config_file)
        elif config_file.startswith("~"):  # relative to home
            home = os.path.expanduser("~")
            file = home + config_file[len("~"):]
        elif config_file.startswith("/"):  # absolute
            file = config_file
        else:
            file = None

        if file is not None:
            if os.path.exists(file):
                logging.debug("reading " + file)
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
                if self.pyami.flagged(self.pyami.CHECK_URLS) :
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

    def setup_environment(self):
        for key in os.environ.keys():
            logging.info(f"{key}: {os.environ[key]}")

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
        # print("KEYS", keys)
        for name in keys:
            if name.endswith("_ini"):
                if name not in self.symbols:
                    logging.error(f"PROCESSING {self.current_file} ; cannot find symbol: {name} in {self.symbols}")
                else:
                    file = self.symbols[name]
                    self.apply_config_file(file)

    def replace_symbols(self, arglist):
        return [self.replace_symbolsx(arg) for arg in arglist]

    # TODO extend to multiple occurrences
    def replace_symbolsx(self, arg):
        return arg[2:-1] if arg.startswith("${") and arg.endswith("}") else arg

    def print_symbols(self):
        print("symbols>>")
        for name in self.symbols:
            print(f"{name}:{self.symbols[name]}")

def main():
    import os
    from util import Util
    print("\n", "============== running pyami main ===============")
    # this needs commandline
    pyami = PyAMI()
    # pyami.run_commands(sys.argv[1:])
    test_glob(pyami)


def test_glob(pyami):
    import os
    """
    /Users/pm286/projects/openDiagram/physchem/resources/oil26/PMC4391421/sections/0_front/1_article-meta/17_abstract.xml
    """
    """
    python pyami.py\
        --glob /Users/pm286/projects/openDiagram/physchem/resources/oil26/PMC4391421/sections/0_front/1_article-meta/17_abstract.xml\
        --proj /Users/pm286/projects/openDiagram/physchem/resources/oil26\
        --apply remove_tags\
        --combine concat_str\
        --outfile /Users/pm286/projects/openDiagram/physchem/resources/oil26/files/xml_files.txt\
OR
 python physchem/python/pyami.py --glob '/Users/pm286/projects/openDiagram/physchem/resources/oil26/**/*abstract.xml' --proj /Users/pm286/projects/openDiagram/physchem/resources/oil26 --apply remove_tags --combine concat_str --outfile /Users/pm286/projects/openDiagram/physchem/resources/oil26/files/xml_files.txt
MOVING TO
 python pyami.py --proj ${oil26} --glob '**/*abstract.xml' --apply remove_tags --combine to_csv --outfile ${oil26}/files/abstracts.csv

    """
    dir_ = "/Users/pm286/projects/openDiagram/physchem/resources/oil26"
    projdir = "~/projects/openDiagram/physchem/resources/oil26"
    # glob_ = "**/*.xml"
    # globstring = "--glob", f"{dir_}/{glob_}"
    output_dir = f"{dir_}/files"
    outfile = f"{output_dir}/xml_files.txt"
    pyami.run_commands([
                    "--glob", f"{dir_}/**/sections/**/*abstract.xml",
                    "--proj", "${oil26}",
                    # "--proj", "/Users/pm286/projects/openDiagram/physchem/resources/oil26",
                    # "--dict", "${eo_plant}, ${country}"
                    "--apply", "remove_tags",
                    "--combine", "concat_str",
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

"""
pyami --proj oil26 --section abstract method --transform xml2txt --dict invasive compound my_terms --phrases tool=rake;count=100 --outfile results/
"""