import logging
class PyAMI:
    def __init__(self):
        pass

    def create_arg_parser(self):
        import argparse
        parser = argparse.ArgumentParser(description='Search sections with dictionaries and patterns')
        """
        """
        parser.add_argument('-d', '--dict', nargs="*",  # default=[AmiDictionaries.COUNTRY],
                            help='dictionaries to search with, empty gives list')
        parser.add_argument('-g', '--glob', nargs="*",  # default=[AmiDictionaries.COUNTRY],
                            help='glob files ')
        parser.add_argument('-s', '--sect', nargs="*",  # default=[AmiSection.INTRO, AmiSection.RESULTS],
                            help='sections to search; empty gives all')
        parser.add_argument('-p', '--proj', nargs="*",
                            help='projects to search; empty will give list')
        parser.add_argument('--patt', nargs="+",
                            help='patterns to search with; regex may need quoting')
        parser.add_argument('--demo', nargs="*",
                            help='simple demos (NYI). empty gives list. May need downloading corpora')
        parser.add_argument('-l', '--loglevel', default="foo",
                            help='debug level (NYI)')
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

        args = []
        if arglist is None:
            arglist = []
        parser = self.create_arg_parser()
        if not arglist:
            # https://stackoverflow.com/questions/31090479/python-argparse-pass-values-without-command-line

            print("NO KWARGS")
            print("ARGS", args)
            print("cmd>>", "sys.argv", sys.argv)
        else:
            parser = self.create_arg_parser()
            args = parser.parse_args(arglist)
            print("ARGS", args)

        if not args:
            logging.info(parser.print_help(sys.stderr))

    def run_glob(self, **kwargs):
        print(f"kwargs{kwargs}")

if __name__ == "__main__":
    print("running pyami main")
    pyami = PyAMI()
    pyami.run_args()
    print("==================")
    pyami.run_args(["--glob", "**", "*.xml" ])

#    test_dict_read()
else:

    #    print("running search main anyway")
    #    main()
    pass

