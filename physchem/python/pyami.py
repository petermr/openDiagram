import logging
import sys
import os
from file_lib import FileLib
from xml_lib import XmlLib
import pprint


class PyAMI:
    """ """
    OUTFILE       = "outfile"

    # flags
    APPLY         = "apply"
    ASSERT        = "assert"
    CHECK_URLS    = "check_urls"
    COMBINE       = "combine"
    GLOB          = "glob"
    PRINT_SYMBOLS = "print_symbols"
    PROJ          = "proj"
    RECURSE       = "recurse"
    SECT          = "sect"
    # methods
    REMOVE_TAGS   = "remove_tags"
    CONCAT_STR    = "concat_str"
    # assertions
    FILE_EXISTS   = "file_exists"
    # symbols to update table
    NEW_SYMBOLS   = ["proj"]
    LOGLEVEL      = "loglevel"

    logger = None
    def __init__(self):
        if self.logger is None:
            self.logger = PyAMI.set_logger("pyami", ch_level=logging.INFO, fh_level=logging.DEBUG, log_file="logs/pyami.log", logger_level=logging.ERROR)

        self.args = {} # args captured in here as name/value without "-" or "--"
        self.apply = []
        self.combine = None
        self.config = None
        self.current_file = None
        self.fileset = None
        self.file_dict = {}
        self.func_dict = {}
        self.set_flags()
        self.symbol_ini = SymbolIni(self)
        self.set_funcs()
        self.show_symbols = False
        if self.show_symbols:
            pprint.pp(f"SYMBOLS\n {self.symbol_ini.symbols}")

    @classmethod
    def set_logger(cls, module, ch_level=logging.INFO, fh_level=logging.DEBUG, log_file=None, logger_level=logging.WARNING):
        """create console and stream loggers
        
        taken from https://docs.python.org/3/howto/logging-cookbook.html#logging-cookbook

        :param module: module to create logger for
        :param ch_level: 
        :param fh_level: 
        :param log_file: 
        :param logger_level:
        :returns: singleton logger for module
        :rtype logger:

        """
        _logger = logging.getLogger(module)
        _logger.setLevel(logger_level)
        # create file handler

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        if log_file is not None:
            fh = logging.FileHandler(log_file)
            fh.setLevel(fh_level)
            fh.setFormatter(formatter)
            _logger.addHandler(fh)

        # create console handler
        ch = logging.StreamHandler()
        ch.setLevel(ch_level)
        ch.setFormatter(formatter)
        _logger.addHandler(ch)

        _logger.debug(f"PyAMI {_logger.level}{_logger.name}")
        return _logger

    def set_flags(self):
        """ """
        self.flag_dict = {}
        self.flag_dict[self.APPLY] = None
        self.flag_dict[self.CHECK_URLS] = None
        self.flag_dict[self.COMBINE] = None
        self.flag_dict[self.PRINT_SYMBOLS] = None
        self.flag_dict[self.RECURSE] = True

    def set_funcs(self):
        """ """
        self.func_dict[self.REMOVE_TAGS] = XmlLib.remove_all_tags

    def create_arg_parser(self):
        """creates adds the arguments for pyami commandline"""
        import argparse
        parser = argparse.ArgumentParser(description='Search sections with dictionaries and patterns')
        parser.add_argument('--apply', nargs="+",
                            help='list of sequential transformations to apply to pipeline')
        parser.add_argument('--assert', nargs="+",
                            help='assertions; failure gives error message (prototype)')
        parser.add_argument('--combine', nargs=1,
                            help='operation to combine files into final object')
        parser.add_argument('-c', '--config', nargs="*", default="PYAMI",
                            help='file (e.g. ~/pyami/config.ini) with list of config file(s) or config vars')
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
        parser.add_argument('-p', '--proj', nargs="+",
                            help='projects to search; _help will give list')
        parser.add_argument('-s', '--sect', nargs="+",  # default=[AmiSection.INTRO, AmiSection.RESULTS],
                            help='sections to search; _help gives all(?)')
        parser.add_argument('--plot', action="store_false",
                            help='plot params (NYI)')
        return parser

    def run_commands(self, arglist=None):
        """parses cmdline, runs cmds and outputs symbols

        :param arglist:  (Default value = None)

        """

        self.logger.info(f"********** raw arglist {arglist}")
        self.parse_and_run_args(arglist)
        if self.flagged(self.PRINT_SYMBOLS):
            self.symbol_ini.print_symbols()


    def parse_and_run_args(self, arglist):
        """runs cmds and makes substitutions (${...} then runs workflow

        :param arglist: 

        """
        if arglist is None:
            arglist = []
        parser = self.create_arg_parser()
        self.args = self.extract_parsed_arg_tuples(arglist, parser)
        self.logger.info("ARGS: "+str(self.args))
        self.substitute_args()
        self.set_loglevel_from_args()
        self.run_workflows()

    def substitute_args(self):
        """ """
        new_items = {}
        for item in self.args.items():
            new_item = self.make_substitutions(item)
            self.logger.debug(f"++++++++{item} ==> {new_item}")
            new_items[new_item[0]] = new_item[1]
        self.args = new_items
        self.logger.info(f"******** substituted ARGS {self.args}")

    def run_workflows(self):
        """ """
        # file workflow
        self.logger.warning(f"commandline args {self.args}")
        if self.PROJ in self.args \
                and (self.SECT in self.args or self.GLOB in self.args):
            self.run_file_workflow()

    def make_substitutions(self, item):
        """

        :param item: 

        """
        old_val = item[1]
        key = item[0]
        new_val = None
        if old_val is None:
            new_val = None
        elif isinstance(old_val, list) and len(old_val) ==1: # single string in list
            # not sure of list, is often used when only one value
            val_item = old_val[0]
            new_val = self.symbol_ini.replace_symbols_in_arg(val_item)
        elif isinstance(old_val, list):
            new_list = []
            for val_item in old_val:
                new_v = self.symbol_ini.replace_symbols_in_arg(val_item)
                new_list.append(new_v)
            self.logger.debug(f"UPDATED LIST ITEMS: {new_list}")
            new_val = new_list
        elif isinstance(old_val, (int, bool, float, complex)):
            new_val = old_val
        elif isinstance(old_val, str):
            if "${" in old_val:
                self.logger.debug(f"Unresolved reference : {old_val}")
                new_val = self.symbol_ini.replace_symbols_in_arg(old_val)
            else:
                new_val = old_val
                # new_items[key] = new_val
        else:
            self.logger.error(f"{old_val} unknown arg type {type(old_val)}")
            new_val = old_val
        self.add_selected_keys_to_symbols_ini(key, new_val)
        return (key, new_val)

    def extract_parsed_arg_tuples(self, arglist, parser):
        """

        :param arglist: 
        :param parser: 

        """
        parsed_args = parser.parse_args() if not arglist else parser.parse_args(arglist)
        self.logger.info(f"PARSED_ARGS {parsed_args}")
        args = {}
        arg_vars = vars(parsed_args)
        new_items = {}
        for item in arg_vars.items():
            new_item = self.make_substitutions(item)
            new_items[new_item[0]] = new_item[1]
        return new_items

    def add_selected_keys_to_symbols_ini(self, key, value):
        """

        :param key: 
        :param value: 

        """
        if key in self.NEW_SYMBOLS:
            self.symbol_ini.symbols[key] = value

    def set_loglevel_from_args(self):
        """ """
        levels = {
            "debug" : logging.DEBUG,
            "info" : logging.INFO,
            "warning": logging.WARNING,
            "error": logging.ERROR,
        }

        if self.LOGLEVEL in self.args:
            loglevel = self.args[self.LOGLEVEL]
            self.logger.info(f"loglevel {loglevel}")
            if loglevel is not None:
                loglevel = str(loglevel)
            if loglevel is not None and loglevel.lower() in levels:
                level = levels[loglevel.lower()]
                self.logger.setLevel(level)

    def run_file_workflow(self):
        """ """
        import glob
        import pathlib
        import file_lib
        self.logger.info("globbing")
        if not self.args[self.PROJ]:
            self.logger.error("glob requires proj")
        else:
            glob_recurse=self.flagged(self.RECURSE)
            glob_ = self.args[self.GLOB]
            self.logger.info(f"glob: {glob_}")
            self.file_dict = {file:None for file in glob.glob(glob_, recursive=glob_recurse)}
            self.logger.info(f"glob file count {len(self.file_dict)}")
        if self.APPLY in self.args:
            self.apply_apply()
        if self.COMBINE in self.args:
            self.combine_files_to_object()
        if self.OUTFILE in self.args:
            self.write_output()
        if self.ASSERT in self.args:
            self.run_assertions()

    def apply_apply(self):
        """ """
        self.read_file_content()
        apply = self.args.get(self.APPLY)
        if apply :
            self.logger.info(f"apply {apply}")
            func = self.func_dict[apply]
            if (func is None):
                self.logger.error(f"Cannot find func for {apply}")
            else:
                # apply = XmlLib.remove_all_tags
                self.apply_to_file_content(func)

    def read_file_content(self, to_str=True):
        """read file content as bytes into file_dict
        
        :to_str: if true convert content to strings

        :param to_str:  (Default value = True)

        """
        for file in self.file_dict:
            with open(file, "r", encoding="utf-8") as f:
                try:
                    data = f.read()
                    if to_str and isinstance(data, bytes):
                        data = data.decode("utf-8")
                    self.file_dict[file] = data
                except UnicodeDecodeError as ude:
                    self.logger.error(f"skipped decoding error {ude}")

    def apply_to_file_content(self, func):
        """applies func to all string content in file_dict

        :param func: 

        """
        for file in self.file_dict:
            data = self.file_dict.get(file)
            new_data = func(data)
            self.file_dict[file] = new_data

    def combine_files_to_object(self):
        """ """
        methods = self.args.get(self.COMBINE)
        if methods and methods == self.CONCAT_STR:
            self.result = "\n".join(self.file_dict.values())
            # print(self.result)

    def write_output(self):
        """ """
        if self.result: # single output
            self.outfile = self.args[self.OUTFILE]
            FileLib.force_write(self.outfile, self.result, overwrite=True)
            self.logger.warning(f"wrote results {self.outfile}")

    def run_assertions(self):
        """ """
        assertions = self.args.get(self.ASSERT)
        if assertions is not None:
            if isinstance(assertions, str):
                assertions = [assertions]
            for assertion in assertions:
                self.run_assertion(assertion)

    def run_assertion(self, assertion):
        """

        :param assertion: 

        """
        if assertion.startswith(self.FILE_EXISTS + "("):
            self.assert_file_exists(assertion[len(self.FILE_EXISTS +"("):-1])

    def assert_file_exists(self, file):
        """

        :param file: 

        """
        if not os.path.exists(file):
            self.assert_error(f"file {file} does not exist")
        else:
            self.logger.info(f"File exists: {file}")
            pass

    def assert_error(self, msg):
        """

        :param msg: 

        """
        self.logger.error(msg)

    def flagged(self, flag):
        """is flag set in flag_dict
        
        if flag is in flag_dict and not falsy return true
        :flag:

        :param flag: 

        """
        return True if self.flag_dict.get(flag) else False

    def test_glob(self):
        """ """
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
        self.run_commands([
                        "--proj", "${oil26.p}",
                        "--glob", "${proj}/**/sections/**/*abstract.xml",
                        "--dict", "${eo_plant.d}", "${ov_country.d}",
                        "--apply", "remove_tags",
                        "--combine", "concat_str",
                        "--outfile", "${proj}/files/shweata_10.txt",
                        "--assert", "file_exists(${proj}/files/xml_files.txt)",
                        ])


# "--config", # defaults to config.ini,~/pyami/config.ini if omitted

# on the commandline:
# python physchem/python/pyami.py --proj '${oil26.p}' --glob '${proj}/**/sections/**/*abstract.xml' --dict '${eo_plant.d}' '${ov_country.d}' --apply remove_tags --combine concat_str --outfile '${proj}/files/shweata_1.txt'
# whihc expands to
# python physchem/python/pyami.py --apply remove_tags --combine concat_str --dict '/Users/pm286/projects/CEVOpen/dictionary/eoPlant/eo_plant.xml' '/Users/pm286/dictionary/openvirus20210120/country/country.xml' --glob '/Users/pm286/projects/openDiagram/physchem/resources/oil26/**/sections/**/*abstract.xml' --outfile '/Users/pm286/projects/openDiagram/physchem/resources/oil26/files/shweata_1.txt' --proj '/Users/pm286/projects/openDiagram/physchem/resources/oil26'

class SymbolIni:
    """processes config/ini files and stores symbols created"""
    NS = "${ns}"
    PARENT = "__parent__" # indicates parent directory of an INI or similar file
    CONFIG = "config"
    PYAMI = "PYAMI"
    PRIMITIVES = ["<class 'int'>", "<class 'bool'>", "<class 'float'>"]

    logger = None

    def __init__(self, pyami):
        # SymbolIni.logger = PyAMI.set_logger("symbol_ini", ch_level=logging.INFO, fh_level=logging.DEBUG, log_file="symbol_ini.log", logger_level=logging.ERROR)
        SymbolIni.logger = PyAMI.set_logger("symbol_ini", logger_level=logging.INFO, log_file="logs/symbol_ini.log")
        SymbolIni.logger.error("SYMBOL_INI")
        self.symbols = None
        self.pyami = pyami
        pyami.symbol_ini = self


        self.setup_environment()
        self.process_config_files()

    def process_config_files(self):
        """ """
        # remove later
        # config file is linked as PYAMI
        self.pyami.args[self.CONFIG] = os.getenv(self.PYAMI)# "/Users/pm286/pyami/config.ini"
        config_files_str = self.pyami.args.get(self.CONFIG)
        config_files = [] if config_files_str is None else config_files_str.split(",")
        self.symbols = {}
        self.fileset = set()
        for config_file in config_files:
            SymbolIni.logger.info(f"processing config: {config_file}")
            self.process_config_file(config_file)
        SymbolIni.logger.debug(f"symbols after config {self.symbols}")

    def process_config_file(self, config_file):
        """

        :param config_file: 

        """
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
                SymbolIni.logger.debug("reading " + file)
                self.apply_config_file(file)
            else:
                SymbolIni.logger.warning(f"*** cannot find config file {file} ***")

    def apply_config_file(self, file):
        """reads config file, recursively replaces {} symbols and '~'
        :file: python config file

        :param file: 

        """
        import configparser
        import os

        if file in self.fileset: # avoid cycles
            SymbolIni.logger.debug(f"{file} already in {self.fileset}")
            return;
        else:
            self.fileset.add(file)

        self.config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
        SymbolIni.logger.info(f"reading config file {file}")
        files_read = self.config.read(file)
        sections = self.config.sections()
        for section in sections:
            self.convert_section_into_symbols_dict(file, section)

        self.check_targets_exist(file)
        self.recurse_ini_files()

    def check_targets_exist(self, file):
        """

        :param file: 

        """
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
                    SymbolIni.logger.error(f"{val} in {file} does not exist as file")
            else:
                print("non-existent: " + val + " in " + file)

    def setup_environment(self):
        """ """
        for key in os.environ.keys():
            SymbolIni.logger.info(f"{key}: {os.environ[key]}")

    def convert_section_into_symbols_dict(self, file, section):
        """

        :param file: 
        :param section: 

        """
        SymbolIni.logger.info("============" + section + "============" + file)
        for name in self.config[section].keys():
            if name in self.symbols:
                SymbolIni.logger.debug(f"{name} already defined, skipped")
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

        SymbolIni.logger.debug(f"symbols for {file} {section}\n {self.symbols}")

    def recurse_ini_files(self):
        """follows links to all *_ini files and runs them recursively
        
        does not check for cycles (yet)


        """
        keys = list(self.symbols.keys())
        # print("KEYS", keys)
        for name in keys:
            if name.endswith("_ini"):
                if name not in self.symbols:
                    SymbolIni.logger.error(f"PROCESSING {self.current_file} ; cannot find symbol: {name} in {self.symbols}")
                else:
                    file = self.symbols[name]
                    self.apply_config_file(file)

    def replace_symbols(self, arg):
        """

        :param arg: 

        """
        # print(f"ARGLIST {type(arglist)} {arglist}")
        if arg is None:
            return None
        elif isinstance(arg, str):
            new_arg = self.replace_symbols_in_arg(arg)
            print(f"{arg} => {new_arg}")
            return new_arg
        elif isinstance(arg, list):
            new_arg = []
            for item in arg:
                print(f"SUBLIST_ITEM {item}")
                new_item = self.replace_symbols_in_arg(item)
                new_arg.append(new_item)
            return new_arg
        elif self.is_primitive(arg):
            return arg
        else:
            print(f"Cannot process arg {arg}")
            return arg
    
    def is_primitive(self, arg):
        """returns true if string of classtype is maps to int, bool, etc. Horrible

        :param arg: 

        """
        return str(type(arg)) in self.PRIMITIVES
    
    def replace_symbols_in_arg(self, arg):
        """replaces ${foo} with value of foo if in symbols
        
        treats any included "${" as literals (this is probably a user error)

        :param arg: 

        """
        import re

        result = ""
        start = 0
        SYM_START = "${"
        SYM_END = "}"
        SymbolIni.logger.info(f"expanding symbols in {arg}")
        while SYM_START in arg[start:]:
            idx0 = arg.index(SYM_START, start)
            result += arg[start:idx0]
            idx1 = arg.index(SYM_END, start)
            symbol = arg[idx0+len(SYM_START):idx1]
            replace = self.symbols.get(symbol)
            if replace != symbol:
                SymbolIni.logger.debug(symbol, " REPLACE", replace)
            end = idx1 + 1
            result += replace if replace is not None else arg[idx0 : idx1 + len(SYM_END)]
            start = end
        result += arg[start:]
        if arg != result:
            SymbolIni.logger.info(f"expanded {arg} to {result}")
        return result


        # return arg[2:-1] if arg.startswith(SYM_START) and arg.endswith(SYM_END) else arg

    def print_symbols(self):
        """ """
        print("symbols>>")
        for name in self.symbols:
            print(f"{name}:{self.symbols[name]}")

def main():
    """ """
    import os
    from util import Util
    print(f"\n============== running pyami main ===============\n{sys.argv[1:]}")
    # this needs commandline
    pyami = PyAMI()
    pyami.run_commands(sys.argv[1:])
#    pyami.test_glob()



if __name__ == "__main__":

    print(f"sys.argv: {sys.argv}")
    main()

else:

    print("running search main anyway")
    main()
    pass

"""
pyami --proj oil26 --section abstract method --transform xml2txt --dict invasive compound my_terms --phrases tool=rake;count=100 --outfile results/
"""