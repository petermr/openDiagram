import tkinter as tk
import subprocess


def button1(event):
    print("button1", event)
    print(dir(event))
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

        self.entry_print_button = tk.Button(self)
        self.entry_print_button["text"] = "Run query"
        self.entry_print_button["command"] = self.print_entry
        self.entry_print_button.pack(side="top")

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

        self.lb1 = self.create_listbox(["morocco", "brazil", "iraq", "united kingdom"])
        self.lb2 = self.create_listbox(["lantana camara", "mentha", "abies alba", "ocimum basilicum"])
        self.lb3 = self.create_listbox(["seed", "root", "leaf"])

        self.spin = tk.Spinbox(root, from_ = 1, to = 10, state = "readonly")
        self.spin.pack(side="bottom")

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

    def donothing(self):
        print("do nothing")

    def menu(self, text):
        print("menu", text)

    def query_print(self, args):
        print("args", args)
        result = str(subprocess.run(args, capture_output=True))
        bits = result.split("\\n")
        for bit in bits:
            print(bit)

    def print_entry(self):

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
            return

        self.query_print(
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

root = tk.Tk()
print("ROOT")
app = Application(master=root)
app.mainloop()
