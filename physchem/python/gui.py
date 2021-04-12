import tkinter as tk

class Application(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
#        self.create_widgets()
        self.menu_stuff()

    def create_widgets(self):
        self.label = tk.Label(text="foo", font="Courier")
        self.label.pack(side="right")

        self.entry_print_button = tk.Button(self)
        self.entry_print_button["text"] = "Print state\n(click)"
        self.entry_print_button["command"] = self.print_entry
        self.entry_print_button.pack(side="top")

        self.entry = tk.Entry()
        self.entry.pack(side="top")

        self.check = tk.Checkbutton()
        self.check["command"] = self.print_check
        self.check.pack()

        self.spamVar = tk.StringVar()
        self.spamCB = tk.Checkbutton(self, text='Spam?',
                                     variable=self.spamVar, onvalue='yes', offvalue='no')
        self.spamCB.pack()

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

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

    def print_entry(self):
        text = self.entry.get()
        print("text:", text)
        print("check:", self.check)
        print("spam:", self.spamVar.get())

    def print_check(self):
        s = False
        print("check", self.check.getboolean(s))

root = tk.Tk()
app = Application(master=root)
app.mainloop()
