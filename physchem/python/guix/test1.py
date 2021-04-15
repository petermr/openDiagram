from tkinter import *
from tkinter.ttk import *
from tkinter import scrolledtext
from tkinter import messagebox


window = Tk()
window.title("Welcome to LikeGeeks app")
window.geometry('350x200')

rowa = 0


combo = Combobox(window)
combo['values']= (1, 2, 3, 4, 5, "Text")
combo.current(1) #set the selected item
combo.grid(column=0, row=rowa)

rowa += 1
chk = Checkbutton(window, text='Choose')
chk_state = BooleanVar()
chk_state.set(True) #set check state
chk = Checkbutton(window, text='Choose', var=chk_state)
chk.grid(column=0, row=rowa)


def clicked():
    res = "Welcome to " + entry.get()
    lbl.configure(text= res)
    print("combo", combo.get())
    print("chk", chk_state.get())
    for r in rad:
        print("rad", r)
    endx = "4.0"
    endx = "30.0"
    linecount = int(txt.index('end-1c').split('.')[0])
    messagebox.showinfo('clicked', 'Textbox'+str(linecount))
    print("text:", "\n", txt.get("1.0", endx))
    txt.delete(1.0, 3.0)
    txt.insert("2.0", "new line xx 3\n")
    txt.insert("3.999", "new line yy 3.999\n")


statex="disabled"
statex="normal"
lbl = Label(window, text="Hello", state=statex)
rowa += 1
lbl.grid(column=0, row=rowa)

btn = Button(window, text="Click Me", command=clicked)
btn.grid(column=2, row=rowa)

rowa += 1
entry = Entry(window,width=10)
entry.grid(column=0, row=rowa)
entry.focus()


rowa += 1
txt = scrolledtext.ScrolledText(window,width=40,height=10)
txt.insert(INSERT,'line 0\nline 1\nline2\n\nline4')

txt.grid(column=0, row=rowa)

rowa += 1
rad = []
chk_sel = IntVar()
for i in range(3):
    rad.append(Radiobutton(window,text='v'+str(i), value=i, variable=chk_sel))

for i, r in enumerate(rad):
    r.grid(column=i, row=rowa)

window.mainloop()

txt.focus()


