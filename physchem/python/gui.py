import tkinter as tk
import subprocess
from tkinter import messagebox
from tkinter import scrolledtext
import os
from xml.etree import ElementTree as ET
from tkinter import Frame
from tkinter import Label
from tkinter import TOP, BOTTOM, LEFT

from search_lib import AmiSearch

ONVAL = 1
OFFVAL = 0

PYGETPAPERS = "pygetpapers"

DICTIONARY_HOME = "/Users/pm286/dictionary"
CEV_DICTIONARY_HOME = "/Users/pm286/projects/CEVOpen/dictionary"

XML_FLAG = "xml"
NOEXEC_FLAG = "noexec"
PDF_FLAG = "pdf"
CSV_FLAG = "csv"
SUPP_FLAG = "supp"
HTML_FLAG = "html"

CBOX_BOX = "box"
CBOX_VAR = "var"
CBOX_TEXT = "text"
CBOX_ON = "on"
CBOX_OFF = "off"
CBOX_BRIEF = "brief"
CBOX_FULL = "full"
CBOX_DEFAULT = "default"
CBOX_COMMAND = "command"
CBOX_TOOLTIP = "tooltip"

TEXT_DEFAULT = "default"

SUBPROC_LINE_END = "\\n"

HLBG = "highlightbackground"
HLTHICK = "highlightthickness"
SIDE = "side"
TITLE = "title"
TOOLTIP = "tooltip"

def button1(event):
    print("button1", event)
    print(dir(event))
    tup = event.widget.curselection
    print("tup", tup, type(tup),)
    if (len(tup) > 0):
        print(tup[0], event.widget.get(tup[0]))

class Gutil:

    @staticmethod
    def create_listbox_from_list(frame, items):
        lb = tk.Listbox(master=frame, height=5,
                        selectmode=tk.MULTIPLE,
                        exportselection=False,
                        highlightcolor="green",
                        selectbackground="pink",
                        highlightthickness=3,
                        bg="#ffffdd",
                        bd=1,  # listbox border
                        fg="blue")
        for i, item in enumerate(items):
            lb.insert(i + 1, item)
        return lb

    @staticmethod
    def quoteme(ss):
        return '"' + ss + '"'

    @staticmethod
    def test_prog_bar():
        """unused demo"""
        import tkinter as tk
        import tkinter.ttk as ttk
        import time

        # Create the master object
        master = tk.Tk()

        # Create a progressbar widget
        progress_bar = ttk.Progressbar(master, orient="horizontal",
                                       mode="determinate", maximum=100, value=0)

        # And a label for it
        label_1 = tk.Label(master, text="Progress Bar")

        # Use the grid manager
        label_1.grid(row=0, column=0)
        progress_bar.grid(row=0, column=1)

        # Necessary, as the master object needs to draw the progressbar widget
        # Otherwise, it will not be visible on the screen
        master.update()

        progress_bar['value'] = 0
        master.update()

        while progress_bar['value'] < 100:
            progress_bar['value'] += 10
            # Keep updating the master object to redraw the progress bar
            master.update()
            time.sleep(0.5)

        # The application mainloop
        tk.mainloop()

    @staticmethod
    def make_checkbox_from_dict(master, dikt, **kwargs):
        onval = dikt[CBOX_ON]
        side = kwargs["side"] if "side" in kwargs else None
        dikt[CBOX_BOX], dikt[CBOX_VAR] = \
            cbox, cvar = Gutil.create_check_box(master, text=dikt[CBOX_TEXT], side=side, default=dikt[TEXT_DEFAULT])
        tooltip = dikt[CBOX_TOOLTIP] if CBOX_BOX in dikt.keys() else None
        if tooltip is not None:
            CreateToolTip(cbox, text=tooltip)

    @staticmethod
    def create_check_box(master, text, **kwargs):
        from tkinter import ttk
        checkVar = tk.IntVar()
        defval = kwargs[TEXT_DEFAULT] if TEXT_DEFAULT in kwargs else None
        if defval is not None and defval == ONVAL:
            checkVar.get()
        checkbutton = ttk.Checkbutton(master, text=text, variable=checkVar,
                                      onvalue=ONVAL, offvalue=OFFVAL)
        if defval is not None and defval == ONVAL:
            checkVar.set(ONVAL)
        side = kwargs[SIDE] if SIDE in kwargs else tk.BOTTOM
        checkbutton.pack(side=side)

        return checkbutton, checkVar

    @staticmethod
    def make_frame(master, **kwargs):
        """ makes a frame with a rim and help tooltip
        (tk uses "highlight" for the rim which other systems call "border";
         there is a separate border outside the rim. So highlightbackground is "border" colour)
        :master: the parent frame
        :kwargs:
               highlightbackground=color,
               highlightthickness=width,
               side=side,
               title=title,
               tooltip=tooltip,

        """
        defaults = {
            HLBG: "brown",
            HLTHICK : 2,
            SIDE : tk.TOP,
            TITLE : "?",
            TOOLTIP : None,
        }
        bg_col = kwargs[HLBG] if HLBG in kwargs else defaults[HLBG]
        bg_thick = kwargs[HLTHICK] if HLTHICK in kwargs else defaults[HLTHICK]
        side = kwargs[SIDE] if SIDE in kwargs else defaults[SIDE]
        title = kwargs[TITLE] if TITLE in kwargs else defaults[TITLE]
        tooltip = kwargs[TOOLTIP] if TOOLTIP in kwargs else defaults[TOOLTIP]

        frame = tk.Frame(master, highlightbackground=bg_col, highlightthickness=bg_thick)
        title_var = None
        if title != "":
            title_var = tk.StringVar(value=title)
            label = tk.Label(frame, textvariable=title_var)
            label.pack(side=side)
            if tooltip is not None:
                CreateToolTip(label, text=tooltip)
        frame.pack(side=side, expand=True, fill=tk.X)
        return frame, title_var

    @staticmethod
    def make_help_label(master, side, text):
        label = tk.Label(master, text="?", background="white")
        CreateToolTip(label, text=text)
        label.pack(side=side)

    @staticmethod
    def refresh_entry(entry, new_text):
        entry.delete(0, tk.END)
        entry.insert(0, new_text)

    @staticmethod
    def make_entry_box(master, **kwargs):
        entry_frame = tk.Frame(master=master,
                               highlightbackground="purple", highlightthickness=3)
        entry_frame.pack(side=tk.BOTTOM)

        labelText = tk.StringVar()
        txt = kwargs[CBOX_TEXT] if CBOX_TEXT in kwargs else ""
        labelText.set(txt)
        entry_label = tk.Label(entry_frame, textvariable=labelText)
        entry_label.pack(side=tk.LEFT)

        default_text = kwargs[TEXT_DEFAULT] if TEXT_DEFAULT in kwargs else None
        entry_text = tk.StringVar(None)
        entry = tk.Entry(entry_frame, textvariable=entry_text, width=25)
        entry.delete(0, tk.END)
        if default_text is not None:
            entry.insert(0, default_text)
        entry.pack(side=tk.LEFT)

        return entry_text

    @staticmethod
    def run_subprocess_get_lines(args):
        """runs subprocess with args
         :return: tuple (stdout as lines, stderr as lines)
         """
        completed_process = subprocess.run(args, capture_output=True)
        completed_process.check_returncode()  # throws error
        # completed_process.stdout returns <bytes>, convert to <str>
        stdout_str = str(completed_process.stdout)
        stderr_str = str(completed_process.stderr)
        argsx = completed_process.args
        stderr_lines = stderr_str.split(SUBPROC_LINE_END) # the <str> conversion adds a backslash?
        stdout_lines = stdout_str.split(SUBPROC_LINE_END)
        return stdout_lines, stderr_lines

    @staticmethod
    def get_selections_from_listbox(box):
        return [box.get(i) for i in box.curselection()]

    @staticmethod
    def make_spinbox(master, title, min=3, max=100):
        spin_frame = tk.Frame(master=master, bg = "#444444", bd = 1,)
        spin_frame.pack(expand=True)
        label = tk.Label(master=spin_frame, bg="#ffffdd", text=title)
        label.pack(side="left")
        spin = tk.Spinbox(spin_frame, from_=min, to=max, state="readonly", width=1)
        spin.pack(side="right")
        return spin



class Application(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.max_max_hits = 90
        self.selected_boxes = []
        self.current_project = None

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
        self.make_dictbox_values(pg_frame)
        self.make_pygetpapers_query_frame(pg_frame, tk.TOP)
        return pg_frame

    def make_sections(self, master):
        frame = tk.Frame(master, highlightbackground="gray",
                                 highlightthickness=2, border=2)
        frame.pack()

        section_box = None
        section_var = None
        self.ami_section_dict = {
            CBOX_BOX: section_box,
            CBOX_VAR: section_var,
            CBOX_TEXT: "make sections",
            CBOX_ON: ONVAL,
            CBOX_OFF: OFFVAL,
            CBOX_DEFAULT: OFFVAL,
            CBOX_TOOLTIP: "run ami section to create all sections ",
        }
        # make sections
        Gutil.make_checkbox_from_dict(frame, self.ami_section_dict)

    def make_dictbox_values(self, master):
        dictionary_dict = {
            "country": (os.path.join(DICTIONARY_HOME, "openVirus20210120", "country", "country.xml"),
                        "ISO countries from wikidata"),
            "ethics": (os.path.join(DICTIONARY_HOME, "ami3", "ethics.xml"),
                       "ISO countries from wikidata"),
            "invasive": (os.path.join(CEV_DICTIONARY_HOME, "Invasive_species", "invasive_plant.xml"),
                         "Invasive plant species from GISD"),
            "plant_part": (os.path.join(CEV_DICTIONARY_HOME, "eoPlantPart", "eoplant_part.xml"),
                           "Plant parts from EO literature"),
            "parkinsons": (os.path.join(DICTIONARY_HOME, "ami3", "parkinsons.xml"),
                           "Terms related to Parkinson's disease"),
        }
        self.dictlistbox0 = self.create_dictionary_listbox(
            dictionary_dict.keys(),
            master=master,
            command=lambda: self.make_dictionary_boxes(
                master,
                dictionary_dict,
                Gutil.get_selections_from_listbox(self.dictlistbox0)
            )
        )
        self.dictlistbox0.pack(side=BOTTOM)
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
                CBOX_BOX: self.xml_box,
                CBOX_VAR: self.xml_var,
                CBOX_TEXT: "XML",
                CBOX_ON: ONVAL,
                CBOX_OFF: OFFVAL,
                CBOX_DEFAULT: ONVAL,
                CBOX_BRIEF: "-x",
                CBOX_FULL: "--xml",
                CBOX_TOOLTIP: "output XML",
            },
            PDF_FLAG: {
                CBOX_BOX: self.pdf_box,
                CBOX_VAR: self.pdf_var,
                CBOX_TEXT: "PDF",
                CBOX_ON: ONVAL,
                CBOX_OFF: OFFVAL,
                CBOX_DEFAULT: OFFVAL,
                CBOX_BRIEF: "-p",
                CBOX_FULL: "--pdf",
                CBOX_TOOLTIP: "output PDF",
            },
            SUPP_FLAG: {
                CBOX_BOX: self.supp_box,
                CBOX_VAR: self.supp_var,
                CBOX_TEXT: "SUPP",
                CBOX_ON: ONVAL,
                CBOX_OFF: OFFVAL,
                CBOX_DEFAULT: OFFVAL,
                CBOX_BRIEF: "-s",
                CBOX_FULL: "--supp",
                CBOX_TOOLTIP: "output Supplemental data (often absent)",
            },
            NOEXEC_FLAG: {
                CBOX_BOX: self.noexec_box,
                CBOX_VAR: self.noexec_var,
                CBOX_TEXT: "-n",
                CBOX_ON: ONVAL,
                CBOX_OFF: OFFVAL,
                CBOX_DEFAULT: OFFVAL,
                CBOX_BRIEF: "-n",
                CBOX_FULL: "--no download",
                CBOX_TOOLTIP: "if checked do not download ",
            },
            CSV_FLAG: {
                CBOX_BOX: self.csv_box,
                CBOX_VAR: self.csv_var,
                CBOX_TEXT: "CSV",
                CBOX_ON: ONVAL,
                CBOX_OFF: OFFVAL,
                CBOX_DEFAULT: OFFVAL,
                CBOX_BRIEF: "-c",
                CBOX_FULL: "--makecsv",
                CBOX_TOOLTIP: "output metadata as CSV",
            },
            HTML_FLAG: {
                CBOX_BOX: self.html_box,
                CBOX_VAR: self.html_var,
                CBOX_TEXT: "HTML",
                CBOX_ON: ONVAL,
                CBOX_OFF: OFFVAL,
                CBOX_DEFAULT: OFFVAL,
                CBOX_FULL: "--makehtml",
                CBOX_TOOLTIP: "output metadata/abstract as HTML",
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
        self.entry_text = Gutil.make_entry_box(frame, text="query")

        return frame, title_var

    def make_ami_search(self, master):

        frame, title_var = Gutil.make_frame(master,
                                           title="AMI",
                                           tooltip="run ami search using dictionaries",
                                           )

        run_button_var = tk.StringVar(value="RUN SEARCH")
        ami_button = tk.Button(frame, textvariable=run_button_var, command=self.run_ami_search)
        ami_button.pack(side=tk.BOTTOM)

        return frame, title_var


    def run_ami_search(self):
        ami_search = AmiSearch()
        ami_search.disease_demo()

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
        button[CBOX_TEXT] = "Run"
        button[CBOX_COMMAND] = self.create_pygetpapers_query_and_run
        button.pack(side="bottom", expand=True)
        self.pygetpapers_command = tk.Entry(master, bg="#ffffdd")
        self.pygetpapers_command.pack(side="bottom", expand=True)



    def make_dictionary_boxes(self, master, dictionary_dict, selected_dict_names):
        self.selected_boxes = []
        for dict_name in selected_dict_names:
            dictionary_tup = dictionary_dict[dict_name]
            curbox = self.make_labelled_dictbox(master, dict_name, dictionary_tup[0], desc=(dictionary_tup[1]))
            self.selected_boxes.append(curbox)

    def make_cproject_frame(self, master, box_side):
        from tkinter import ttk

        frame, _ = Gutil.make_frame(master,
                                           title="CProject",
                                           tooltip="Project directory",
                                           )
        frame.pack()

        open_button = ttk.Button(
            frame,
            text='Dir',
            command=self.select_directory
        )
        open_button.pack(side=LEFT, expand=True)

        default_dir = os.path.join(os.path.expanduser("~"), "temp")

        self.outdir = tk.StringVar(None)
        self.dir_entry = tk.Entry(frame, textvariable=self.outdir, width=25)
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

    def make_labelled_dictbox(self, master, name, amidict, desc="Missing desc"):
        frame, _ = Gutil.make_frame(master,
                                           title="CProject",
                                           tooltip="Project directory",
                                           )
        frame.pack()

        dictbox = Frame()
        dictbox.pack()

        label = Label(master=dictbox, text=name, bg="#ffdddd", bd=3)
        if desc:
            CreateToolTip(label, text=desc)
        label.pack(side=TOP)

        box = self.create_dictionary_listbox(self.read_entry_names(amidict), master=dictbox)
        box.pack(side=BOTTOM)
        return box

    def create_dictionary_listbox(self, items, master=None, command=None):
        frame, title_var = Gutil.make_frame(master,
                                           title="DICTIONARIES",
                                           tooltip="dictionaries for pygetpapers query or AMI search",
                                           )

        lb = Gutil.create_listbox_from_list(frame, items)
        lb.pack(side=tk.BOTTOM)

        #        self.lb1.bind('<Button-1>', button1)

        if command is not None:
            button = tk.Button(frame, text="create dictboxes",
                          command=command,
                           )
            button.pack(side=tk.BOTTOM)

        return lb

    # frames and windows
    """
    https://stackoverflow.com/questions/24656138/python-tkinter-attach-scrollbar-to-listbox-as-opposed-to-window/24656407
    """

    def run_query_and_get_output(self, args):
        _, stderr_lines = Gutil.run_subprocess_get_lines(args)
        saved = 0
        hits = 0
#        print("lines", stderr_lines)
        TOTAL_HITS_ARE = "Total Hits are"
        for line in stderr_lines:
            if TOTAL_HITS_ARE in line:
                hits = line.split(TOTAL_HITS_ARE)[-1]
                print("HITS", hits)
            WROTE_XML = "Wrote xml"
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

        self.project_dir = self.outdir.get()
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

        if self.ami_section_dict[CBOX_VAR].get() == ONVAL:
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
                if v[CBOX_VAR].get() == ONVAL:
                    option = v[CBOX_BRIEF] if CBOX_BRIEF in v else None
                    if option is None:
                        option = v[CBOX_FULL] if CBOX_FULL in v else None
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
        if var is not None and var.get() == ONVAL:
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


"""unused"""




class ToolTip(object):

    # https://stackoverflow.com/questions/20399243/display-message-when-hovering-over-something-with-mouse-cursor-in-python

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        OFFSET_X = 57
        OFFSET_Y = 27

        from tkinter import Toplevel, SOLID
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + OFFSET_X
        y = y + cy + self.widget.winfo_rooty() + OFFSET_Y
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(tw, text=self.text, justify=LEFT,
                      background="#ffffe0", relief=SOLID, borderwidth=1,
                      font=("tahoma", "15", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

def CreateToolTip(widget, text):
    toolTip = ToolTip(widget)

    def enter(event):
        toolTip.showtip(text)

    def leave(event):
        toolTip.hidetip()

    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)

# main
root = tk.Tk()
print("ROOT", root)
app = Application(master=root)
app.mainloop()


# menu - not used
def menu_stuff(self):
    from tkinter import Menu

    menubar = Menu(self.master)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="New", command=self.menu("newxx"))
    filemenu.add_command(label="Open", command=self.menu("openxx"))
    filemenu.add_command(label="Save", command=self.menu("savexx"))
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=root.quit)
    menubar.add_cascade(label="File", menu=filemenu)

    helpmenu = Menu(menubar, tearoff=0)
    helpmenu.add_command(label="Help Index", command=self.menu("help indexx"))
    helpmenu.add_command(label="About...", command=self.menu("ABOUTxx"))
    menubar.add_cascade(label="Help", menu=helpmenu)

    root.config(menu=menubar)
    print("before mainloop")
    root.mainloop()

def menu(self, text):
    print("menu", text)


# https://stackoverflow.com/questions/30004505/how-do-you-find-a-unique-and-constant-id-of-a-widget