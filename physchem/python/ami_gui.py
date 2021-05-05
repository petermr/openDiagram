import tkinter as tk
import tkinter.ttk as ttk
import subprocess
from tkinter import messagebox
from tkinter import scrolledtext
import os
from xml.etree import ElementTree as ET
from tkinter import Frame
from tkinter import Label
from tkinter import TOP, BOTTOM, LEFT
from gutil import AmiTree
from gutil import Gutil
from gutil import Gutil as gu
from gutil import CreateToolTip
from search_lib import AmiSearch
from search_lib import AmiSection
from search_lib import AmiDictionaries
from search_lib import AmiProjects


PYGETPAPERS = "pygetpapers"

DICTIONARY_HOME = "/Users/pm286/dictionary"
CEV_DICTIONARY_HOME = "/Users/pm286/projects/CEVOpen/dictionary"

XML_FLAG = "xml"
NOEXEC_FLAG = "noexec"
PDF_FLAG = "pdf"
CSV_FLAG = "csv"
SUPP_FLAG = "supp"
HTML_FLAG = "html"

TOTAL_HITS_ARE = "Total Hits are"
WROTE_XML = "Wrote xml"


#select by typing
# https://stackoverflow.com/questions/47839813/python-tkinter-autocomplete-combobox-with-like-search

def button1(event):
    print("button1", event)
    print(dir(event))
    tup = event.widget.curselection
    print("tup", tup, type(tup),)
    if (len(tup) > 0):
        print(tup[0], event.widget.get(tup[0]))


class AmiGui(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.max_max_hits = 90
        self.selected_boxes = []
        self.current_project = None
        self.ami_tree = None
        self.treeview = None

        self.pack()
        self.create_all_widgets(root)
#        self.menu_stuff()


    def create_all_widgets(self, master):

        self.make_ami_widgets(master)
        self.make_sections(master)
        self.make_ami_search(master)
        self.make_quit(master)

    def make_ami_widgets(self, master):
        pg_frame = tk.Frame(master, highlightbackground="gray",
                                 highlightthickness=2, border=5)
        pg_frame.pack(side=TOP)

        self.make_cproject_frame(pg_frame, tk.TOP)
        self.make_dictionary_names_box(pg_frame)
        self.make_pygetpapers_query_frame(pg_frame, tk.TOP)
        return pg_frame

    def make_sections(self, master):
        section_frame = tk.Frame(master, highlightbackground="gray",
                                 highlightthickness=2, border=2)
        section_frame.pack()

        self.sections_listbox = self.create_generic_listbox(
            AmiSection.SECTION_LIST,
            master=section_frame,
        )
        self.sections_listbox.pack(side=BOTTOM)

        section_box = None
        section_var = None
        self.ami_section_dict = {
            Gutil.CBOX_BOX: section_box,
            Gutil.CBOX_VAR: section_var,
            Gutil.CBOX_TEXT: "make sections",
            Gutil.CBOX_ON: Gutil.ONVAL,
            Gutil.CBOX_OFF: Gutil.OFFVAL,
            Gutil.CBOX_DEFAULT: Gutil.OFFVAL,
            Gutil.CBOX_TOOLTIP: "run ami section to create all sections ",
        }
        # make sections

        Gutil.make_checkbox_from_dict(section_frame, self.ami_section_dict)


    def make_dictionary_names_box(self, master):
        """

        dictionary_dict = {
            "country": (os.path.join(DICTIONARY_HOME, "openVirus20210120", "country", "country.xml"),
                        "ISO countries from wikidata"),
            "ethics": (os.path.join(DICTIONARY_HOME, "ami3", "ethics.xml"),
                       "Ethics section terminology"),
            "invasive": (os.path.join(CEV_DICTIONARY_HOME, "Invasive_species", "invasive_plant.xml"),
                         "Invasive plant species from GISD"),
            "plant_part": (os.path.join(CEV_DICTIONARY_HOME, "eoPlantPart", "eoplant_part.xml"),
                           "Plant parts from EO literature"),
            "parkinsons": (os.path.join(DICTIONARY_HOME, "ami3", "parkinsons.xml"),
                           "Terms related to Parkinson's disease"),
        }
        """
        ami_dictionaries = AmiDictionaries()
        dictionary_dict = ami_dictionaries.dictionary_dict;
        self.dictionary_names_listbox = self.create_generic_listbox(
            dictionary_dict.keys(),
            master=master,
            button_text="select dictionaries",
            command=lambda: self.make_dictionary_content_boxes(
                self.dcb_frame,
                dictionary_dict,
                Gutil.get_selections_from_listbox(self.dictionary_names_listbox)
            )
        )

        dictionary_names = dictionary_dict.keys()
        self.xml_box = None
        self.xml_var = None
        self.pdf_box = None
        self.pdf_var = None
        self.supp_box = None
        self.supp_var = None
        self.noexec_box = None
        self.noexec_var = None
        self.csv_box = None
        self.csv_var = None
        self.html_box = None
        self.html_var = None
        self.pygetpapers_flags = {
            XML_FLAG: {
                Gutil.CBOX_BOX: self.xml_box,
                Gutil.CBOX_VAR: self.xml_var,
                Gutil.CBOX_TEXT: "XML",
                Gutil.CBOX_ON: Gutil.ONVAL,
                Gutil.CBOX_OFF: Gutil.OFFVAL,
                Gutil.CBOX_DEFAULT: Gutil.ONVAL,
                Gutil.CBOX_BRIEF: "-x",
                Gutil.CBOX_FULL: "--xml",
                Gutil.CBOX_TOOLTIP: "output XML",
            },
            PDF_FLAG: {
                Gutil.CBOX_BOX: self.pdf_box,
                Gutil.CBOX_VAR: self.pdf_var,
                Gutil.CBOX_TEXT: "PDF",
                Gutil.CBOX_ON: Gutil.ONVAL,
                Gutil.CBOX_OFF: Gutil.OFFVAL,
                Gutil.CBOX_DEFAULT: Gutil.OFFVAL,
                Gutil.CBOX_BRIEF: "-p",
                Gutil.CBOX_FULL: "--pdf",
                Gutil.CBOX_TOOLTIP: "output PDF",
            },
            SUPP_FLAG: {
                Gutil.CBOX_BOX: self.supp_box,
                Gutil.CBOX_VAR: self.supp_var,
                Gutil.CBOX_TEXT: "SUPP",
                Gutil.CBOX_ON: Gutil.ONVAL,
                Gutil.CBOX_OFF: Gutil.OFFVAL,
                Gutil.CBOX_DEFAULT: Gutil.OFFVAL,
                Gutil.CBOX_BRIEF: "-s",
                Gutil.CBOX_FULL: "--supp",
                Gutil.CBOX_TOOLTIP: "output Supplemental data (often absent)",
            },
            NOEXEC_FLAG: {
                Gutil.CBOX_BOX: self.noexec_box,
                Gutil.CBOX_VAR: self.noexec_var,
                Gutil.CBOX_TEXT: "-n",
                Gutil.CBOX_ON: Gutil.ONVAL,
                Gutil.CBOX_OFF: Gutil.OFFVAL,
                Gutil.CBOX_DEFAULT: Gutil.OFFVAL,
                Gutil.CBOX_BRIEF: "-n",
                Gutil.CBOX_FULL: "--no download",
                Gutil.CBOX_TOOLTIP: "if checked do not download ",
            },
            CSV_FLAG: {
                Gutil.CBOX_BOX: self.csv_box,
                Gutil.CBOX_VAR: self.csv_var,
                Gutil.CBOX_TEXT: "CSV",
                Gutil.CBOX_ON: Gutil.ONVAL,
                Gutil.CBOX_OFF: Gutil.OFFVAL,
                Gutil.CBOX_DEFAULT: Gutil.OFFVAL,
                Gutil.CBOX_BRIEF: "-c",
                Gutil.CBOX_FULL: "--makecsv",
                Gutil.CBOX_TOOLTIP: "output metadata as CSV",
            },
            HTML_FLAG: {
                Gutil.CBOX_BOX: self.html_box,
                Gutil.CBOX_VAR: self.html_var,
                Gutil.CBOX_TEXT: "HTML",
                Gutil.CBOX_ON: Gutil.ONVAL,
                Gutil.CBOX_OFF: Gutil.OFFVAL,
                Gutil.CBOX_DEFAULT: Gutil.OFFVAL,
                Gutil.CBOX_FULL: "--makehtml",
                Gutil.CBOX_TOOLTIP: "output metadata/abstract as HTML",
            },
        }
        self.flags_keys = self.pygetpapers_flags.keys()

    def make_pygetpapers_query_frame(self, master, TOP):

        frame, title_var = Gutil.make_frame(master,
                                           title="pygetpapers query",
                                           tooltip="build query from dictionaries, flags and text; and RUN",
                                           )

        self.create_run_button(frame)
        self.make_getpapers_args(frame)
        self.dcb_frame = self.make_dictionary_content_boxes_frame(frame)
        self.entry_text = Gutil.make_entry_box(frame, text="query")

        return frame, title_var

    def make_ami_search(self, master):

        run_ami_frame, title_var = Gutil.make_frame(master,
                                           title="AMI (runs a demo search, not yet linked to widgets)",
                                           tooltip="run ami search using dictionaries",
                                           )

        run_button_var = tk.StringVar(value="RUN SEARCH")
        ami_button = tk.Button(run_ami_frame, textvariable=run_button_var, command=self.run_ami_search)
        ami_button.pack(side=tk.BOTTOM)

        self.project_names_listbox = self.create_generic_listbox(
            AmiProjects().project_dict.keys(),
            master=run_ami_frame,
        )
        self.project_names_listbox.pack(side=BOTTOM)

        return run_ami_frame, title_var


    def run_ami_search(self):
        ami_search = AmiSearch()
        ami_guix = self
        print(type(ami_search), type(ami_guix))
        ami_search.run_search_from_gui(ami_guix)
#        ami_search.disease_demo()

    def make_getpapers_args(self, frame):
        getpapers_args_frame = tk.Frame(frame,
                                    highlightbackground="black", highlightthickness=2)
        getpapers_args_frame.pack(side=tk.TOP)

        checkbox_frame = tk.Frame(getpapers_args_frame,
                                    highlightbackground="black", highlightthickness=2)
        checkbox_frame.pack(side=tk.TOP)

        Gutil.make_help_label(checkbox_frame, tk.LEFT,
                             "pygetpapers checkboxes")

        for key in self.flags_keys:
            self.make_pygetpapers_check_button(checkbox_frame, key)

        self.spin = Gutil.make_spinbox(getpapers_args_frame, "maximum hits (-k)", min=1, max=self.max_max_hits)


    def make_pygetpapers_check_button(self, master, key):
        cbox_dict = self.pygetpapers_flags[key]
        Gutil.make_checkbox_from_dict(master, cbox_dict, side=tk.LEFT)

    def create_run_button(self, master):
        button = tk.Button(master)
        button[Gutil.CBOX_TEXT] = "Run"
        button[Gutil.CBOX_COMMAND] = self.create_pygetpapers_query_and_run
        button.pack(side="bottom", expand=True)
        self.pygetpapers_command = tk.Entry(master, bg="#ffffdd")
        self.pygetpapers_command.pack(side="bottom", expand=True)



    def make_dictionary_content_boxes(self, master, dictionary_dict, selected_dict_names):
        self.selected_boxes = []
        for dict_name in selected_dict_names:
            dictionary_tup = dictionary_dict[dict_name]
            curbox = self.make_dictionary_content_box(master, dict_name, dictionary_tup[0], desc=(dictionary_tup[1]))
            self.selected_boxes.append(curbox)

    def make_dictionary_content_boxes_NEW(self, master, dictionary_dict, selected_dict_names):
        frame = tk.Frame(master, highlightcolor="red", highlightthickness=10)
        frame.pack()
        n = ttk.Notebook(frame)
        """
        f1 = ttk.Frame(n)  # first page, which would get widgets gridded into it
        button11 = tk.Button(f1, text="button11")
        button11.pack()
        n.add(f1, text='One')
        f2 = ttk.Frame(n)  # second page
        n.add(f2, text='Two')
        button22 = tk.Button(f2, text="button22")
        button22.pack()
        """
        n.pack()

        self.selected_boxes = []
        for dict_name in selected_dict_names:
            dictionary_tup = dictionary_dict[dict_name]

            f1 = tk.Frame(n, highlightcolor="blue", highlightthickness=10)
            n.add(f1, text=dict_name)
            tup_ = dictionary_tup[0]
            description = dictionary_tup[1]
            curbox = self.make_dictionary_content_box(n, dict_name, tup_, desc=description)
            curbox.pack()
            button22 = tk.Button(n, text="b:"+dict_name)
            button22.pack()

            self.selected_boxes.append(curbox)

    def make_cproject_frame(self, master, box_side):
        from tkinter import ttk

        frame, _ = Gutil.make_frame(master,
                                           title="CProject",
                                           tooltip="Project directory",
                                           )
        frame.pack(side=TOP)

        self.display_frame = tk.Frame(frame)
        self.display_frame.pack(side=BOTTOM)

        open_button = ttk.Button(
            frame,
            text='Dir',
            command=self.select_directory
        )
        open_button.pack(side=LEFT, expand=True)
        display_button = ttk.Button(
            frame,
            text='Display',
            command=self.display_directory
        )
        display_button.pack(side=tk.RIGHT, expand=True)

        default_dir = os.path.join(os.path.expanduser("~"), "temp")

        self.outdir_var = tk.StringVar(None)
        self.dir_entry = tk.Entry(frame, textvariable=self.outdir_var, width=25)
        Gutil.refresh_entry(self.dir_entry, default_dir)
        self.dir_entry.pack(side=tk.RIGHT)

        return frame

    def select_directory(self):
        from tkinter import filedialog as fd
        from tkinter import messagebox

        filename = fd.askdirectory(
            title='Output directory',
            initialdir=os.path.expanduser("~"),  # HOME directory
        )
        Gutil.refresh_entry(self.dir_entry, filename)

    def display_directory(self):
        title="dummy title"
        if self.ami_tree is None:
            self.ami_tree = AmiTree()
        self.treeview = self.ami_tree.get_or_create_treeview(self.display_frame, title)

        parent = ''

        self.ami_tree.recursive_display(self.outdir_var.get(), parent, self.treeview)

    def make_dictionary_content_box(self, master, dictionary_name, ami_dictionary, desc="Missing desc"):
        frame, _ = Gutil.make_frame(master,
                                           title=dictionary_name,
                                           tooltip=desc,
                                           )
        frame.pack(side=LEFT)

        box = self.create_generic_listbox(self.read_entry_names(ami_dictionary),
                                          master=frame, title="select dictionary items")
        box.pack(side=BOTTOM)
        return box

    def create_generic_listbox(self, items, master=None, command=None, title=None, tooltip=None, button_text="select"):
        frame, title_var = Gutil.make_frame(master,
                                           title=title,
                                           tooltip=tooltip,
                                           highlightbackground="green",
                                           highlightthickness=3,
                                           )

        lb = Gutil.create_listbox_from_list(frame, items)
        lb.pack(side=tk.BOTTOM)

        #        self.lb1.bind('<Button-1>', button1)

        if command is not None:
            button = tk.Button(frame, text=button_text, command=command,)
            button.pack(side=tk.BOTTOM)

        return lb

    def create_dictionary_listbox_NEW(self, items, master=None, command=None, title="no title"):
        frame, title_var = Gutil.make_frame(master,
                                           title="DICTIONARIES_NEW",
                                           tooltip="contains dictionary names, button will generate content lists",
                                           )

        lb = Gutil.create_listbox_from_list(frame, items)
        lb.pack(side=tk.BOTTOM)

        #        self.lb1.bind('<Button-1>', button1)
        print("command", command)
        if command is not None:
            print("dictbox cmd:", command)
            button = tk.Button(frame, text="create dictboxes NEW",
                          command=command,
                           )
            CreateToolTip(button, str(command))
            button.pack(side=tk.BOTTOM)

        return lb

    # frames and windows
    """
    https://stackoverflow.com/questions/24656138/python-tkinter-attach-scrollbar-to-listbox-as-opposed-to-window/24656407
    """

    def run_query_and_get_output(self, args):
        try:
            _, stderr_lines = Gutil.run_subprocess_get_lines(args)
        except:
            messagebox.showinfo(title="query failed", message="failed, maybe no output")
            return ["failure, probably no hits"]
        saved = 0
        hits = 0
#        print("lines", stderr_lines)
        for line in stderr_lines:
            if TOTAL_HITS_ARE in line:
                hits = line.split(TOTAL_HITS_ARE)[-1]
                print("HITS", hits)
            if WROTE_XML in line:
                saved += 1
        messagebox.showinfo(title="end search", message="finished search, hits: "+str(hits)+", saved: "+str(saved))
        return stderr_lines

    def create_pygetpapers_query_and_run(self):

        limit = self.spin.get()
        query_string = ""
        query_string = self.add_query_entry(query_string)
        query_string = self.add_dictionary_box_terms(query_string)

        if query_string == "":
            print("No query, no submission")
            messagebox.showinfo(title="query_output", message="no query or dictionary boxes selected; no submission")
            return

        self.project_dir = self.outdir_var.get()
        if self.project_dir == "":
            print("must give outdir")
            messagebox.showinfo(title="outdir box", message="must give outdir")
            return

        cmd_options = [PYGETPAPERS, "-q", query_string, "-o", self.project_dir, "-k", limit]

        self.add_flags_to_query_command(cmd_options)

        print("CMD", cmd_options, "\n", str(cmd_options))
        self.pygetpapers_command.insert(0, str(cmd_options))

        lines = self.run_query_and_get_output(cmd_options)

        self.display_query_output(root, lines)

        if self.ami_section_dict[Gutil.CBOX_VAR].get() == Gutil.ONVAL:
            self.run_ami_sections()


    def run_ami_sections(self):
        import subprocess
        args = ["ami", "-p", self.project_dir, "section"]
        print("making sections", args)
        stdout_lines, _ = Gutil.run_subprocess_get_lines(args)
        print("stdout", stdout_lines)

    def add_flags_to_query_command(self, cmd_options):

        for k, v in self.pygetpapers_flags.items():
            if k in self.pygetpapers_flags:
                if v[Gutil.CBOX_VAR].get() == Gutil.ONVAL:
                    option = v[Gutil.CBOX_BRIEF] if Gutil.CBOX_BRIEF in v else None
                    if option is None:
                        option = v[Gutil.CBOX_FULL] if Gutil.CBOX_FULL in v else None
                    if option is None:
                        print("Cannot find keys for", k)
                    else:
                        cmd_options.append(option)

    def add_query_entry(self, query_string):
        query_string = self.entry_text.get()
        if query_string != "":
            query_string = '("' + query_string + '")'
        return query_string

    def add_dictionary_box_terms(self, lbstr):
        for box in self.selected_boxes:
            select_str = self.make_query_string(box)
            if select_str is None or select_str == "":
                continue
            if lbstr != "":
                lbstr += " AND "
            lbstr += select_str
        return lbstr

    def add_if_checked(self, cmd_options, var, val):
        if var is not None and var.get() == gu.ONVAL:
            cmd_options.append(val)

    def print_check(self):
        s = False
        print("check", self.check.getboolean(s))

    def make_query_string(self, listbox):
        selected = Gutil.get_selections_from_listbox(listbox)
        s = ""
        l = len(selected)
        s = '('
        s += Gutil.quoteme(selected[0]) if l > 0 else ""
        for i in range(1, l):
            s += " OR " + Gutil.quoteme(selected[i])
        s += ')'
        return s

    def display_query_output(self, master, lines):
        # Title Label
        frame = tk.Frame(master)
        frame.pack(side=BOTTOM)
        lab = tk.Label(frame,
                       text="output",
                       font=("Arial", 15),
                       background='white',
                       foreground="white")
        lab.pack(side="bottom")
        #            .grid(column=0, row=0)

        # Creating scrolled text area
        # widget with Read only by
        # disabling the state
        text_area = scrolledtext.ScrolledText(frame,
                                              width=30,
                                              height=8,
                                              font=("Arial", 15))
        text_area.pack(side="bottom")
        print("txt", text_area)

        # Inserting Text which is read only
        text = "\n".join(lines)
        text_area.insert(tk.INSERT, text)
        text_area.bind("<Button-1>", button1)
        # Making the text read only
        #        text_area.configure(state='disabled')
        return text_area

    def read_entry_names(self, dictionary_file):
        print(dictionary_file)
        assert (os.path.exists(dictionary_file))
        elementTree = ET.parse(dictionary_file)
        entries = elementTree.findall("entry")
        names = [entry.attrib["name"] for entry in entries]
        print("entries", len(names))
        names = sorted(names)
        return names

    def make_quit(self, master):

        frame, title_var = Gutil.make_frame(master,
                                           title="",
                                           tooltip="quit and destroy windoe",
                                           )

        quit = tk.Button(frame, text="QUIT", fg="red",
                              command=self.master.destroy)
        quit.pack(side=tk.BOTTOM)

        pass

    def make_dictionary_content_boxes_frame(self, master):
        self.dcb_frame, title_var = Gutil.make_frame(master,
                                                     title="select entries in dictionaries",
                                                     tooltip="dictionary content boxes will be added here",
                                                     )
        self.dcb_frame.pack()
        return self.dcb_frame

"""unused"""




# main
root = tk.Tk()
app = AmiGui(master=root)
app.mainloop()

