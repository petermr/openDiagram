import tkinter as tk
import subprocess
from tkinter import messagebox
from tkinter import scrolledtext
import os
from xml.etree import ElementTree as ET
from tkinter import Frame
from tkinter import Label
from tkinter import TOP, BOTTOM, LEFT

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

def button1(event):
    print("button1", event)
    print(dir(event))
    tup = event.widget.curselection
    print("tup", tup, type(tup),)
    if (len(tup) > 0):
        print(tup[0], event.widget.get(tup[0]))

class Application(tk.Frame):

    def quoteme(self,ss):
        return '"' + ss + '"'

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.max_max_hits = 90
        self.selected_boxes = []
        self.current_project = None

        self.pack()
        self.create_widgets()
#        self.menu_stuff()


    def create_widgets(self):

        self.make_outdir_box(root, tk.TOP)

        self.make_entry_box(root, text="query")


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

        selected_dict_names = ["country", "ethics", "parkinsons"]

        self.dictlistbox0 = self.create_listbox(
                                dictionary_dict.keys(),
                                master=root,
                                command=lambda: self.make_dictionary_boxes(
                                    dictionary_dict,
                                    self.get_selections_from_box(self.dictlistbox0))
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
        self.section_box = None
        self.section_var = None

        self.pygetpapers_flags = {
            XML_FLAG : {
                CBOX_BOX: self.xml_box,
                CBOX_VAR: self.xml_var,
                CBOX_TEXT: "XML",
                CBOX_ON:ONVAL,
                CBOX_OFF: OFFVAL,
                CBOX_DEFAULT : ONVAL,
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
        }

        self.mek_getpapers_checkboxes()

        self.ami_section_dict = {
            CBOX_BOX: self.section_box,
            CBOX_VAR: self.section_var,
            CBOX_TEXT: "make sections",
            CBOX_ON: ONVAL,
            CBOX_OFF: OFFVAL,
            CBOX_DEFAULT: OFFVAL,
            CBOX_TOOLTIP: "run ami section to create all sections ",
        }


        self.make_spinbox(root, "maximum hits (-k)", min=1, max=self.max_max_hits)

        text_area_flag = False
        if text_area_flag:
            self.make_text_area()

        self.create_run_button()
        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

        self.make_checkbox_from_dict(root, self.ami_section_dict)

    def mek_getpapers_checkboxes(self):
        self.checkbox_frame = tk.Frame(root,
                                    highlightbackground="black", highlightthickness=2)
        self.checkbox_frame.pack()

        self.make_help_label(self.checkbox_frame, tk.LEFT,
                             "pygetpapers checkboxes")

        self.make_check_button(self.checkbox_frame, XML_FLAG)
        self.make_check_button(self.checkbox_frame, PDF_FLAG)
        self.make_check_button(self.checkbox_frame, CSV_FLAG)
        self.make_check_button(self.checkbox_frame, NOEXEC_FLAG)
        self.make_check_button(self.checkbox_frame, SUPP_FLAG)

    def make_help_label(self, master, side, text):
        label = tk.Label(master, text="?", background="white")
        CreateToolTip(label, text=text)
        label.pack(side=side)

    def make_check_button(self, master, key):
        cbox_dict = self.pygetpapers_flags[key]
        self.make_checkbox_from_dict(master, cbox_dict)

    def make_checkbox_from_dict(self, master,  cbox_dict):
        onval = cbox_dict[CBOX_ON]
        cbox_dict[CBOX_BOX], cbox_dict[CBOX_VAR] = \
            cbox, cvar = self.create_check_box(master, text=cbox_dict[CBOX_TEXT], default=cbox_dict[TEXT_DEFAULT])
        tooltip = cbox_dict[CBOX_TOOLTIP] if CBOX_BOX in cbox_dict.keys() else None
        if tooltip is not None:
            CreateToolTip(cbox, text=tooltip)

    def create_check_box(self, window, text, **kwargs):
        from tkinter import ttk
        self.checkVar = tk.IntVar()
        defval = kwargs[TEXT_DEFAULT] if TEXT_DEFAULT in kwargs else None
        if defval is not None and defval == ONVAL:
            self.checkVar.get()
        checkbutton = ttk.Checkbutton(window, text=text, variable=self.checkVar,
                    onvalue=ONVAL, offvalue=OFFVAL)
        if defval is not None and defval == ONVAL:
            self.checkVar.set(ONVAL)

        checkbutton.pack(side=tk.LEFT)

        return checkbutton, self.checkVar

    def create_run_button(self):
        self.run_query_button = tk.Button(self)
        self.run_query_button[CBOX_TEXT] = "Run pygetpapers query"
        self.run_query_button[CBOX_COMMAND] = self.create_query_and_run
        self.run_query_button.pack(side="bottom")

    def make_dictionary_boxes(self, dictionary_dict, selected_dict_names):
        self.selected_boxes = []
        for dict_name in selected_dict_names:
            dictionary_tup = dictionary_dict[dict_name]
            curbox = self.make_labelled_dictbox(dict_name, dictionary_tup[0], desc=(dictionary_tup[1]))
            self.selected_boxes.append(curbox)

    def make_outdir_box(self, master, box_side):
        from tkinter import ttk
        # TODO display frame
        outdir_frame = tk.Frame(master=master,
                                highlightbackground="red", highlightcolor="blue", highlightthickness=2)
        outdir_frame.pack()

        open_button = ttk.Button(
            outdir_frame,
            text='Output directory',
            command=self.select_directory
        )
        open_button.pack()

        open_button.pack(expand=True)
        labelText = tk.StringVar()
        labelText.set("output dir")
        labelDir = tk.Label(outdir_frame, textvariable=labelText, height=1)
        labelDir.pack(side=tk.TOP)

        default_dir = os.path.join(os.path.expanduser("~"), "temp")
        self.outdir = tk.StringVar(None)
        dirname = tk.Entry(outdir_frame, textvariable=self.outdir, width=25)
        dirname.delete(0, tk.END)
        dirname.insert(0, default_dir)
        dirname.pack(side=tk.TOP)

    def select_directory(self):
        from tkinter import filedialog as fd
        from tkinter import messagebox

        filename = fd.askdirectory(
            title='Output directory',
            initialdir=os.path.expanduser("~"),  # HOME directory
        )

        messagebox.showinfo(
            title='Selected Directory',
            message=filename
        )

    def make_entry_box(self, master, **kwargs):
        entry_frame = tk.Frame(master=master,
                               highlightbackground="purple", highlightthickness=3)
        entry_frame.pack(side=tk.BOTTOM)

        labelText = tk.StringVar()
        txt = kwargs[CBOX_TEXT] if CBOX_TEXT in kwargs else ""
        labelText.set(txt)
        entry_label = tk.Label(entry_frame, textvariable=labelText)
        entry_label.pack(side=tk.LEFT)

        default_text = kwargs[TEXT_DEFAULT] if TEXT_DEFAULT in kwargs else None
        self.entry_text = tk.StringVar(None)
        entry = tk.Entry(entry_frame, textvariable=self.entry_text, width=25)
        entry.delete(0, tk.END)
        if default_text is not None:
            entry.insert(0, default_text)
        entry.pack(side=tk.LEFT)

    #        directory = tkFileDialog.askdirectory()

    def make_spinbox(self, master, title, min=1, max=100):
        spin_frame = tk.Frame(master=master, bg = "#444444", bd = 3,)
        spin_frame.pack()
        label = tk.Label(master=spin_frame, bg="#ffffdd", text=title)
        label.pack(side="left")
        self.spin = tk.Spinbox(spin_frame, from_=min, to=max, state="readonly", width=5)
        self.spin.pack(side="right")

    def make_labelled_dictbox(self, name, amidict, desc="Missing desc"):
        dictbox = Frame()
        dictbox.pack()

        label = Label(master=dictbox, text=name, bg="#ffdddd", bd=3)
        if desc:
            CreateToolTip(label, text=desc)
        label.pack(side=TOP)

        box = self.create_listbox(self.read_entry_names(amidict), master=dictbox)
        box.pack(side=BOTTOM)
        return box

    def create_listbox(self, items, master=None, command=None):
        frame = tk.Frame(master,
                         highlightbackground="blue", highlightcolor="green", highlightthickness=2
                         )
        frame.pack()  #cannot pack frame with "side=bottom", why not??
        if command is not None:
            button = tk.Button(frame, text="create dictboxes",
                          command=command,
                           )
            button.pack(side="top")

        lb = tk.Listbox(master=frame, height=5,
                        selectmode=tk.MULTIPLE,
                        exportselection=False,
                        highlightcolor="green",
                        selectbackground="pink",
                        highlightthickness=3,
                        bg = "#ffffdd", bd = 3,
                        fg="blue")
        for i, item in enumerate(items):
            lb.insert(i + 1, item)
        lb.pack(side=tk.BOTTOM)
        #        self.lb1.bind('<Button-1>', button1)
        return lb

# frames and windows
    """
    https://stackoverflow.com/questions/24656138/python-tkinter-attach-scrollbar-to-listbox-as-opposed-to-window/24656407
    """

    def run_query_and_get_output(self, args):
        _, stderr_lines = self.run_subprocess_get_lines(args)
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

    def run_subprocess_get_lines(self, args):
        """runs subprocess with args
         :return: tuple (stdout as lines, stderr as lines)
         """
        completed_process = subprocess.run(args, capture_output=True)
        completed_process.check_returncode()  # throws error
        # completed_process.stdout returns <bytes>, convert to <str>
        stdout_str = str(completed_process.stdout)
        stderr_str = str(completed_process.stderr)
        args = completed_process.args
        stderr_lines = stderr_str.split(SUBPROC_LINE_END) # the <str> conversion adds a backslash?
        stdout_lines = stdout_str.split(SUBPROC_LINE_END)
        return stdout_lines, stderr_lines

    def create_query_and_run(self):

        limit = self.spin.get()
#        print("limit:", limit)
        query_string = ""
        query_string = self.add_query_entry(query_string)
        query_string = self.add_dictionary_box_terms(query_string)

        if query_string == "":
            print("No query, no submission")
            messagebox.showinfo(title="query_output", message="no query or dictionary boxes selected; no submission")
            return

        self.project_dir = outd = self.outdir.get()
        if self.project_dir == "":
            print("must give outdir")
            messagebox.showinfo(title="outdir box", message="must give outdir")
            return

        cmd_options = [PYGETPAPERS, "-q", query_string, "-o", self.project_dir, "-k", limit]

        self.add_boolean_flags(cmd_options)

        lines = self.run_query_and_get_output(cmd_options)
        self.make_text_area(root, lines)

        if self.ami_section_dict[CBOX_VAR].get() == ONVAL:
            self.create_sections()


    def create_sections(self):
        import subprocess
        args = ["ami", "-p", self.project_dir, "section"]
        print("making sections", args)
#        self.run_subprocess_and_capture(args)
        stdout_lines, _ = self.run_subprocess_get_lines(args)
        print("stdout", stdout_lines)

    def add_boolean_flags(self, cmd_options):

        pygetpapers_flags = [XML_FLAG, NOEXEC_FLAG, PDF_FLAG, CSV_FLAG, SUPP_FLAG]
        for k, v in self.pygetpapers_flags.items():
            if k in pygetpapers_flags:
                if v[CBOX_VAR].get() == ONVAL:
                    cmd_options.append(v[CBOX_BRIEF])

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

    def make_query_string(self, box):
        selected = self.get_selections_from_box(box)
        s = ""
        l = len(selected)
        s = '('
        s += self.quoteme(selected[0]) if l > 0 else ""
        for i in range(1, l):
            s += " OR " + self.quoteme(selected[i])
        s += ')'
        return s

    def get_selections_from_box(self, box):
        return [box.get(i) for i in box.curselection()]

    def test_prog_bar(self):
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

    def make_text_area(self, master, lines):
        # Title Label
        frame = tk.Frame(master)
        frame.pack()
        lab = tk.Label(frame,
                       text="ScrolledText Widget Example",
                       font=("Arial", 15),
                       background='green',
                       foreground="white")
        lab.pack(side="bottom")
        #            .grid(column=0, row=0)

        # Creating scrolled text area
        # widget with Read only by
        # disabling the state
        text_area = scrolledtext.ScrolledText(frame,
                                              width=30,
                                              height=8,
                                              font=("Times New Roman", 15))
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


"""unused"""




class ToolTip(object):

    # https://stackoverflow.com/questions/20399243/display-message-when-hovering-over-something-with-mouse-cursor-in-python

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        from tkinter import Toplevel, SOLID
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 57
        y = y + cy + self.widget.winfo_rooty() + 27
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