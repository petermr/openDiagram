import tkinter as tk
import subprocess
from tkinter import messagebox
from tkinter import scrolledtext
import os
from xml.etree import ElementTree as ET

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
        self.pack()
        self.create_widgets()
        self.menu_stuff()

    def create_widgets(self):

        self.run_query_button = tk.Button(self)
        self.run_query_button["text"] = "Run pygetpapers query"
        self.run_query_button["command"] = self.check_query_widgets
        self.run_query_button.pack(side="top")

        labelText = tk.StringVar()
        labelText.set("output dir")
        labelDir = tk.Label(root, textvariable=labelText, height=1)
        labelDir.pack(side="left")

        self.outdir = tk.StringVar(None)
        dirname = tk.Entry(root, textvariable=self.outdir, width=50)
        dirname.pack(side="left")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

        self.frame = tk.Frame()
        self.frame.pack()

        self.lb1 = self.create_listbox(["morocco", "brazil", "iraq", "india", "singapore", "united kingdom"])
        self.lb2 = self.create_listbox(["lantana camara", "mentha", "abies alba", "ocimum basilicum"])
        plant_parts_list = ["seed", "root", "leaf"]
        plant_parts_list = self.read_plants_part_dictionary_names()
        self.lb3 = self.create_listbox(plant_parts_list)

        self.spin = tk.Spinbox(root, from_ = 1, to = 10, state = "readonly")
        self.spin.pack(side="bottom")



        text_area_flag = False
        if text_area_flag:
            self.make_text_area()

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

    def create_listbox(self, items):
        lb = tk.Listbox(height=5,
                              selectmode=tk.MULTIPLE,
                              exportselection=False,
                              highlightcolor="green",
                              selectbackground="pink",
                              highlightthickness=3, fg="blue")
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
                print("******", hits)
            if "Wrote xml" in line:
                saved += 1
            print(line)
        messagebox.showinfo(title="end search", message="finised search, hits: "+str(hits)+", saved: "+str(saved))

    def check_query_widgets(self):

        limit = self.spin.get()
        print("limit:", limit)
        lbstr1 = self.make_query_string(self.lb1)
        lbstr2 = self.make_query_string(self.lb2)
        lbstr3 = self.make_query_string(self.lb3)
        if lbstr1 == "()" and lbstr2 == "()" and lbstr3 == "()":
            print("must pick at least one listbox")
            return
        lbstr = lbstr1 + " AND " + lbstr2 + " AND " + lbstr3
        print ("str", lbstr)
        outd = self.outdir.get()
        if outd == "":
            print("must give outdir")
            messagebox.showinfo(title="outdir box", message="must give outdir")
            ans = messagebox.askyesno(title="yesno", message="False or True?")
            print("ans", ans)
            ans = messagebox.askyesnocancel(title="yesno", message="Yes No None")
            print("yes no cancel", ans)
            return

        self.run_query_and_get_output(
            ["pygetpapers", "-q", lbstr, "-x", "-o", outd, "-k", limit])

    def print_check(self):
        s = False
        print("check", self.check.getboolean(s))

    def make_query_string(self, lb):
        selected = [lb.get(i) for i in lb.curselection()]
        s = ""
        l = len(selected)
        s = '('
        s += self.quoteme(selected[0]) if l > 0 else ""
        for i in range(1, l):
            s += " OR " + self.quoteme(selected[i])
        s += ')'
        return s

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

    def read_plants_part_dictionary_names(self):
        DICTIONARY_HOME = "/Users/pm286/projects/CEVOpen/dictionary"
        plant_parts_dict = os.path.join(DICTIONARY_HOME, "eoPlantPart/eoplant_part.xml")
        assert(os.path.exists(plant_parts_dict))
        elementTree = ET.parse(plant_parts_dict)
        entries = elementTree.findall("entry")
        print("entries", len(entries))
        names = [entry.attrib["name"] for entry in entries]
        print (len(names))
        return names


root = tk.Tk()
print("ROOT")
app = Application(master=root)
app.mainloop()
