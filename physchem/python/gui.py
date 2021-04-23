import tkinter as tk
import subprocess
from tkinter import messagebox
from tkinter import scrolledtext
import os
from xml.etree import ElementTree as ET
from tkinter import Frame
from tkinter import Label
from tkinter import TOP, BOTTOM, LEFT

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
        self.master = master
        self.max_max_hits = 90

        self.pack()
        self.create_widgets()
        self.menu_stuff()


    def create_widgets(self):

        self.run_query_button = tk.Button(self)
        self.run_query_button["text"] = "Run pygetpapers query"
        self.run_query_button["command"] = self.check_query_widgets
        self.run_query_button.pack(side="top")

        self.make_outdir_box(root, "top")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

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
        }


        self.dictlistbox = self.create_listbox(dictionary_dict.keys(), master=root)
        self.dictlistbox.pack(side=BOTTOM)

        dictionary_names = dictionary_dict.keys()
#        for i, dict_key in enumerate(dictionary_names):
#            self.dictlistbox.insert(i, dict_key)


        selected_dict_names = ["country", "ethics",
                               "plant_part"]


        self.make_dictionary_boxes(dictionary_dict, selected_dict_names)
        self.make_spinbox(root, "maximum hits (-k)", min=1, max=self.max_max_hits)

        text_area_flag = False
        if text_area_flag:
            self.make_text_area()

    def make_dictionary_boxes(self, dictionary_dict, selected_dict_names):
        self.selected_boxes = []
        for dict_name in selected_dict_names:
            dictionary_tup = dictionary_dict[dict_name]
            curbox = self.make_labelled_dictbox(dict_name, dictionary_tup[0], desc=(dictionary_tup[1]))
            self.selected_boxes.append(curbox)

    def make_outdir_box(self, master, box_side):
        outdir_frame = tk.Frame(master=master, bd=3, bg="#ffddaa")
        outdir_frame.pack(side=box_side)

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

    def create_listbox(self, items, master=None):
        lb = tk.Listbox(master=master, height=5,
                        selectmode=tk.MULTIPLE,
                        exportselection=False,
                        highlightcolor="green",
                        selectbackground="pink",
                        highlightthickness=3,
                        bg = "#ffffdd", bd = 3,
                        fg="blue")
        for i, item in enumerate(items):
            lb.insert(i + 1, item)
        lb.pack(side="left")
        #        self.lb1.bind('<Button-1>', button1)
        return lb

# frames and windows
    """
    https://stackoverflow.com/questions/24656138/python-tkinter-attach-scrollbar-to-listbox-as-opposed-to-window/24656407
    """

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

    def run_query_and_get_output(self, args):
        print("args", args)
        result = str(subprocess.run(args, capture_output=True))
        lines = result.split("\\n")
        saved = 0
        for line in lines:
            if line.startswith("CompletedProcess"):
                hits = line.split("Total Hits are")[-1]
                print("HITS", hits)
            if "Wrote xml" in line:
                saved += 1
            print(line)
        messagebox.showinfo(title="end search", message="finised search, hits: "+str(hits)+", saved: "+str(saved))

    def check_query_widgets(self):

        limit = self.spin.get()
        print("limit:", limit)
        lbstr = ""
        for box in self.selected_boxes:
            select_str = self.make_query_string(box)
            if select_str is None or select_str == "":
                continue
            if lbstr != "":
                lbstr += " AND "
            lbstr += select_str
#        lbstr1 = self.make_query_string(self.lb1)

        outd = self.outdir.get()
        if outd == "":
            print("must give outdir")
            messagebox.showinfo(title="outdir box", message="must give outdir")
            return

        self.run_query_and_get_output(
            ["pygetpapers", "-q", lbstr, "-x", "-o", outd, "-k", limit])

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
print("ROOT")
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

