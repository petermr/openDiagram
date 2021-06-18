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
                            help='dictionaries to search with, _help gives list')
        parser.add_argument('-g', '--glob', nargs="*",  # default=[AmiDictionaries.COUNTRY],
                            help='glob files ')
        parser.add_argument('-s', '--sect', nargs="*",  # default=[AmiSection.INTRO, AmiSection.RESULTS],
                            help='sections to search; _help gives all(?)')
        parser.add_argument('-p', '--proj', nargs="*",
                            help='projects to search; _help will give list')
        parser.add_argument('-c', '--config', nargs="*", default="config.ini,~/pyami/config.ini",
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
        args_ns = parser.parse_args() if not arglist else parser.parse_args(arglist)
        self.args = {item[0]:item[1] for item in list(vars(args_ns).items())}
        self.set_loglevel_from_args()
        self.logger.info(f"args_ns {args_ns}")
        print("args ", args_ns)
        self.logger.info(f"args as dict {self.args}")
        if self.args["proj"] and (self.args["sect"] or self.args["glob"]):
            self.make_files()

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
        logging.info("globbing")
        if not self.args["proj"]:
            logging.error("glob requires proj")
        else:
            glob_ = self.args["glob"][0]
            print(f"glob {glob_}")
            logging.info(f"glob: {glob_}")
            files = glob.glob(glob_)
            print(f"files {files}")


def main():
    import os
    print("\n", "============== running pyami main ===============")
    pyami = PyAMI()
    dir_ = "/Users/pm286/projects/openDiagram/physchem/resources/oil26"
    glob_ = "**/*.xml"
    pyami.run_args(["--glob", f"{dir_}/{glob_}", "--proj", "pm286",
                    "-c", "-l", "warn"])


if __name__ == "__main__":
    main()

else:

    print("running search main anyway")
    main()
    pass

