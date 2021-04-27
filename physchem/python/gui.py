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

def button1(event):
    print("button1", event)
    print(dir(event))
    if True:
        return
    tup = event.widget.curselection()
    print("tup", tup, type(tup),)
    if (len(tup) > 0):
        print(tup[0], event.widget.get(tup[0]))

def button2(event):
    print("button2", event)

def button3(event):
    print("button3", event)

class Application(tk.Frame):

    def quoteme(self,ss):
        return '"' + ss + '"'

    def __init__(self, master=None):
        super().__init__(master)
        print("master", type(master), master, master.children, dir(master))
        self.master = master
        self.max_max_hits = 90
        self.selected_boxes = []
        self.current_project = "None"

        self.pack()
        self.create_widgets()
#        self.menu_stuff()


    def create_widgets(self):

        self.make_outdir_box(root, "top")

        self.make_entry_box(root, text="query")


        DICTIONARY_HOME = "/Users/pm286/dictionary"
        CEV_DICTIONARY_HOME = "/Users/pm286/projects/CEVOpen/dictionary"

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


        selected_dict_names = ["country", "ethics",
                               "parkinsons"]
#        self.dictlistbox = self.create_listbox(dictionary_dict.keys(), master=root,
#                        command=lambda: self.make_dictionary_boxes0(
#                            dictionary_dict, selected_dict_names))
        self.dictlistbox0 = self.create_listbox(dictionary_dict.keys(), master=root,
                        command=lambda: self.make_dictionary_boxes(
                            dictionary_dict,
                            self.get_selections_from_box(self.dictlistbox0)))

#        self.dictlistbox.pack(side=BOTTOM)
        self.dictlistbox0.pack(side=BOTTOM)

        dictionary_names = dictionary_dict.keys()
#        for i, dict_key in enumerate(dictionary_names):
#            self.dictlistbox.insert(i, dict_key)


#        self.make_dictionary_boxes(dictionary_dict, selected_dict_names)cc

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
        self.checkbox_dict = {
            "xml" : {
                "box": self.xml_box,
                "var": self.xml_var,
                "text": "output XML",
                "on":ONVAL,
                "off": OFFVAL,
                "default" : ONVAL,
                "brief": "-x",
                "full": "--xml",
            },
            "pdf": {
                "box": self.pdf_box,
                "var": self.pdf_var,
                "text": "output PDF",
                "on": ONVAL,
                "off": OFFVAL,
                "default": OFFVAL,
                "brief": "-p",
                "full": "--pdf",
            },
            "supp": {
                "box": self.supp_box,
                "var": self.supp_var,
                "text": "output SUPP",
                "on": ONVAL,
                "off": OFFVAL,
                "default": OFFVAL,
                "brief": "-s",
                "full": "--supp",
            },
            "noexec": {
                "box": self.noexec_box,
                "var": self.noexec_var,
                "text": "no download",
                "on": ONVAL,
                "off": OFFVAL,
                "default": ONVAL,
                "brief": "-n",
                "full": "--noexecute",
            },
            "csv": {
                "box": self.csv_box,
                "var": self.csv_var,
                "text": "output metadata CSV",
                "on": ONVAL,
                "off": OFFVAL,
                "default": OFFVAL,
                "brief": "-c",
                "full": "--makecsv",
            },
            "sections": {
                "box": self.section_box,
                "var": self.section_var,
                "text": "make sections",
                "on": ONVAL,
                "off": OFFVAL,
                "default": OFFVAL,
                "brief": "-z",
                "full": "--sections",
            },
        }

        self.make_check_button("xml")
        self.make_check_button("pdf")
        self.make_check_button("csv")
        self.make_check_button("noexec")
        self.make_check_button("supp")
        self.make_check_button("sections")
#        cbox = self.checkbox_dict["xml"]
#        onval = cbox["on"]
#        print("ONV", onval)
#        cbox["box"], cbox["var"] = self.create_check_box(root, text=cbox["text"], default=cbox["default"])
#        self.xml_box, self.xml_var = self.create_check_box(root, text="output XML")
#        self.pdf_box, self.pdf_var = self.create_check_box(root, text="output PDF")
#        self.supp_box, self.supp_var = self.create_check_box(root, text="download suppdata")
#        self.noexec_box, self.noexec_var = self.create_check_box(root, text="don't run query")

        self.make_spinbox(root, "maximum hits (-k)", min=1, max=self.max_max_hits)

        text_area_flag = False
        if text_area_flag:
            self.make_text_area()

        self.create_run_button()
        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

    def make_check_button(self, key):
        option_dict = self.checkbox_dict[key]
        print("option", option_dict)
        cbox = self.checkbox_dict[key]
        onval = cbox["on"]
        print("ONVAL", onval)
        cbox["box"], cbox["var"] = self.create_check_box(root, text=cbox["text"], default=cbox["default"])



    def create_check_box(self, window, text, **kwargs):
        from tkinter import ttk
        print("master", window)

        print("KW", kwargs)
        self.checkVar = tk.IntVar()
        defval = kwargs["default"] if "default" in kwargs else None
        if defval is not None and defval == ONVAL:
            self.checkVar.get()
        print("def", self.checkVar)
        checkbutton = ttk.Checkbutton(window, text=text, variable=self.checkVar,
                    onvalue=ONVAL, offvalue=OFFVAL)
        if defval is not None and defval == ONVAL:
#            checkbutton.select()
            self.checkVar.set(ONVAL)

        print("checkvar", self.checkVar.get())

        checkbutton.pack()

        return checkbutton, self.checkVar
#        def test():
#            print(CheckVar2.get())  # Notice the .get()

    def create_run_button(self):
        self.run_query_button = tk.Button(self)
        self.run_query_button["text"] = "Run pygetpapers query"
        self.run_query_button["command"] = self.create_query_and_run
        self.run_query_button.pack(side="bottom")

    def make_dictionary_boxes0(self):

        print("make_dictionary_boxes0")

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
            root,
            text='Output directory',
            command=self.select_directory
        )
        open_button.pack()

        open_button.pack(expand=True)
        labelText = tk.StringVar()
        labelText.set("output dir")
        labelDir = tk.Label(root, textvariable=labelText, height=1)
        labelDir.pack(side="top")

        default_dir = os.path.join(os.path.expanduser("~"), "temp")
        self.outdir = tk.StringVar(None)
        dirname = tk.Entry(root, textvariable=self.outdir, width=25)
        dirname.delete(0, tk.END)
        dirname.insert(0, default_dir)
        dirname.pack(side="top")

    #        directory = tkFileDialog.askdirectory()

    def select_directory(self):
        from tkinter import filedialog as fd
        from tkinter import messagebox
        filetypes = (
            ('text files', '*.txt'),
            ('All files', '*')
        )

        filename = fd.askdirectory(
            title='Output directory',
            initialdir=os.path.expanduser("~"),  # HOME directory
        )

        messagebox.showinfo(
            title='Selected Directory',
            message=filename
        )

    def make_entry_box(self, master, **kwargs):
        entry_frame = tk.Frame(master=master, bd=3, bg="#ffddaa")
        entry_frame.pack()

        labelText = tk.StringVar()
        txt = kwargs["text"] if "text" in kwargs else ""
        labelText.set(txt)
        entry_label = tk.Label(master, textvariable=labelText)
        entry_label.pack(side="top")

        default_text = kwargs["default"] if "default" in kwargs else None
        self.entry_text = tk.StringVar(None)
        entry = tk.Entry(master, textvariable=self.entry_text, width=25)
        entry.delete(0, tk.END)
        if default_text is not None:
            entry.insert(0, default_text)
        entry.pack(side="top")

    #        directory = tkFileDialog.askdirectory()

    def make_spinbox(self, master, title, min=1, max=100):

        print("master", master)
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
#        return dictbox
        return box

    def create_listbox(self, items, master=None, command=None):
        print("items", items)
        print("listbox master", master)
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
        lb.pack(side="bottom")
        #        self.lb1.bind('<Button-1>', button1)
        return lb

    def make_dictboxes(self):
        print("make dictboxes")
        pass

# frames and windows
    """
    https://stackoverflow.com/questions/24656138/python-tkinter-attach-scrollbar-to-listbox-as-opposed-to-window/24656407
    """

    def run_query_and_get_output(self, args):
        print("args", args)
        result = str(subprocess.run(args, capture_output=True))
        lines = result.split("\\n")
        saved = 0
        for line in lines:
            if line.startswith("CompletedProcess"):
                hits = line.split("Total Hits are")[-1]
                hits = hits.split("args=")[-1]
                hits = hits.split(", returncode")[0]
                print("HITS", hits)
            if "Wrote xml" in line:
                saved += 1
            print(line)
        messagebox.showinfo(title="end search", message="finished search, hits: "+str(hits)+", saved: "+str(saved))

    def create_query_and_run(self):

        limit = self.spin.get()
        print("limit:", limit)
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

        cmd_options = ["pygetpapers", "-q", query_string, "-o", self.project_dir, "-k", limit]

        self.add_boolean_flags(cmd_options)

        self.run_query_and_get_output(cmd_options)

        section_dict = self.checkbox_dict["sections"]
        if section_dict["var"].get() == ONVAL:
            self.create_sections()

    def create_sections(self):
        import subprocess
        args = ["ami", "-p", self.project_dir, "section"]
        print("making sections", args)
        result = str(subprocess.run(args, capture_output=True))
        print("section:", result)


    def add_boolean_flags(self, cmd_options):
        pygetpapers_flags = ["xml", "noexec", "pdf", "csv", "supp"]
        for k, v in self.checkbox_dict.items():
            print("K,V", k, v)
            if k in pygetpapers_flags:
                if v["var"].get() == ONVAL:
                    cmd_options.append(v["brief"])

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

    def read_entry_names(self, dictionary_file):
        print(dictionary_file)
        assert (os.path.exists(dictionary_file))
        elementTree = ET.parse(dictionary_file)
        entries = elementTree.findall("entry")
        names = [entry.attrib["name"] for entry in entries]
        print("entries", len(names))
        names = sorted(names)
        return names


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

"""unused"""
def make_text_area(self):
    # Title Label
    lab = tk.Label(root,
                   text="ScrolledText Widget Example",
                   font=("Times New Roman", 15),
                   background='green',
                   foreground="white")
    lab.pack(side="bottom")
    #            .grid(column=0, row=0)

    # Creating scrolled text area
    # widget with Read only by
    # disabling the state
    text_area = scrolledtext.ScrolledText(root,
                                width=30,
                                height=8,
                                font=("Times New Roman",
                                      15))
    text_area.pack(side="bottom")
    print("text", text_area)

    # Inserting Text which is read only
    text_area.insert(tk.INSERT,
                     """\
This is a scrolledtext widget to make tkinter text 
one
two
three
four
five
six
seven
eight
nine
ten
                     """)
    text_area.bind("<Button-1>", button1)
    # Making the text read only
#        text_area.configure(state='disabled')
    return text_area

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