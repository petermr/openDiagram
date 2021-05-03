
import tkinter as tk
import tkinter.ttk as ttk

import subprocess
import os

HLBG = "highlightbackground"
HLTHICK = "highlightthickness"
SIDE = "side"
TITLE = "title"
TOOLTIP = "tooltip"


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
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
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



class Gutil:
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

    ONVAL = 1
    OFFVAL = 0

    SUBPROC_LINE_END = "\\n"

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
        onval = dikt[Gutil.CBOX_ON]
        side = kwargs["side"] if "side" in kwargs else None
        dikt[Gutil.CBOX_BOX], dikt[Gutil.CBOX_VAR] = \
            cbox, cvar = Gutil.create_check_box(master, text=dikt[Gutil.CBOX_TEXT], side=side, default=dikt[Gutil.TEXT_DEFAULT])
        tooltip = dikt[Gutil.CBOX_TOOLTIP] if Gutil.CBOX_BOX in dikt.keys() else None
        if tooltip is not None:
            CreateToolTip(cbox, text=tooltip)

    @staticmethod
    def create_check_box(master, text, **kwargs):
        from tkinter import ttk
        checkVar = tk.IntVar()
        defval = kwargs[Gutil.TEXT_DEFAULT] if Gutil.TEXT_DEFAULT in kwargs else None
        if defval is not None and defval == Gutil.ONVAL:
            checkVar.get()
        checkbutton = ttk.Checkbutton(master, text=text, variable=checkVar,
                                      onvalue=Gutil.ONVAL, offvalue=Gutil.OFFVAL)
        if defval is not None and defval == Gutil.ONVAL:
            checkVar.set(Gutil.ONVAL)
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
        txt = kwargs[Gutil.CBOX_TEXT] if Gutil.CBOX_TEXT in kwargs else ""
        labelText.set(txt)
        entry_label = tk.Label(entry_frame, textvariable=labelText)
        entry_label.pack(side=tk.LEFT)

        default_text = kwargs[Gutil.TEXT_DEFAULT] if Gutil.TEXT_DEFAULT in kwargs else None
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
        stderr_lines = stderr_str.split(Gutil.SUBPROC_LINE_END) # the <str> conversion adds a backslash?
        stdout_lines = stdout_str.split(Gutil.SUBPROC_LINE_END)
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


class AmiTree:
    def __init__(self):
        self.tree = None

    def tree1(self):
        master = tk.Tk()
        master.geometry("300x300")
        frame = tk.Frame(master)
        frame.pack()
        tree = ttk.Treeview(frame)
        tree.pack()

        # Inserted at the root, program chooses id:
        tree.insert('', 'end', 'widgets', text='Widget Tour')

        # Same thing, but inserted as first child:
        tree.insert('', 0, 'gallery', text='Applications')

        # Treeview chooses the id:
        id = tree.insert('', 'end', text='Tutorial')

        # Inserted underneath an existing node:
        tree.insert('widgets', 'end', text='Canvas')
        tree.insert(id, 'end', text='Tree')

#        tree.move('widgets', 'gallery', 'end')  # move widgets under gallery

#        tree.detach('widgets')

#        tree.delete('widgets')

#        tree.item('widgets', open=tk.TRUE)
#        isopen = tree.item('widgets', 'open')

#        tree = ttk.Treeview(root, columns=('size', 'modified'))
#        tree['columns'] = ('size', 'modified', 'owner')

        tk.mainloop()

    def table1(self):
        import tkinter as tk
        from tkinter import ttk
        from tkinter.messagebox import showinfo

        root = tk.Tk()
        root.title('Treeview demo')
        root.geometry('620x200')

        # columns
        columns = ('#1', '#2', '#3')

        tree = ttk.Treeview(root, columns=columns, show='headings')

        # define headings
        tree.heading('#1', text='First Name')
        tree.heading('#2', text='Last Name')
        tree.heading('#3', text='Email')

        # generate sample data
        contacts = []
        for n in range(1, 100):
            contacts.append((f'first {n}', f'last {n}', f'email{n}@example.com'))

        # adding data to the treeview
        for contact in contacts:
            tree.insert('', tk.END, values=contact)

        # bind the select event
        def item_selected(event):
            for selected_item in tree.selection():
                # dictionary
                item = tree.item(selected_item)
                # list
                record = item['values']
                #
                showinfo(title='Information',
                         message=','.join(record))

        tree.bind('<<TreeviewSelect>>', item_selected)

        tree.grid(row=0, column=0, sticky='nsew')

        # add a scrollbar
        scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ns')

        # run the app
        root.mainloop()

    def cb(event):
        print(event, tree.selection(), tree.focus())

    def dir1(self):
        import tkinter as tk
        from tkinter import ttk
        from tkinter.messagebox import showinfo

        root = tk.Tk()
        root.title('lantana demo')
        root.geometry('620x200')

        self.tree = ttk.Treeview(root)
        self.color_tags()
        self.tree.pack()

        HOME = os.path.expanduser("~")
        dirx = os.path.join(HOME, "temp", "lantana")
        parent = ''

        self.recursive_display(dirx, parent, self.tree)

        # run the app
        root.mainloop()

    def color_tags(self):
        self.tree.tag_configure('xml', background='pink')
        self.tree.tag_configure('0', background='yellow')

    def itemClicked(self, event):
        print("CLICKED", event, self.tree.focus(), self.tree.selection, dir(self.tree.selection))

    def recursive_display(self, dirx, parent_id, tree):
#        childdirs = [f.path for f in os.scandir(dirx) if f.is_dir()]
        childfiles = [f.path for f in os.scandir(dirx) if os.path.isdir(dirx)]
        sorted_child_files = AmiTree.sorted_alphanumeric(childfiles)
        for f in sorted_child_files:
            filename = AmiTree.path_leaf(f)
            child_id = None
            if self.display_filename(f):
                tag = ""
                if filename.startswith("0"):
                    tag="0"
                elif f.endswith(".xml"):
                    tag="xml"
                child_id = tree.insert(parent_id, 'end', text=filename, tags=(tag, 'simple'))
                tree.tag_bind(tag, '<1>', self.itemClicked)

            if os.path.isdir(f) and child_id is not None:
                self.recursive_display(f, child_id, tree)

    def sorted_alphanumeric(data):
        import re
# https://stackoverflow.com/questions/800197/how-to-get-all-of-the-immediate-subdirectories-in-python
        convert = lambda text: int(text) if text.isdigit() else text.lower()
        alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
        return sorted(data, key=alphanum_key)

    def path_leaf(path):
        import ntpath
        head, tail = ntpath.split(path)
        return tail or ntpath.basename(head)

    def display_filename(self, filename):
        isd = os.path.isdir(filename)
        return isd or filename.endswith(".xml")

print("junk")
amiTree = AmiTree()
# amiTree.dir1() # needs PMR directory
# amiTree.table1() # tableview as stock example
