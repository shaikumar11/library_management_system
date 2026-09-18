"""
main.py

UI and application logic only. All database reads/writes go through
LibraryRepository (see repository.py) — this file never calls sqlite3
directly.
"""

from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as mb
import tkinter.simpledialog as sd

from repository import LibraryRepository

repo = LibraryRepository("library.db")


# ---------- Helpers ----------

def issuer_card():
    Cid = sd.askstring('Issuer Card ID', 'What is the Issuer\'s Card ID?\t\t\t')
    if not Cid:
        mb.showerror('Issuer ID cannot be zero!', 'Can\'t keep Issuer ID empty, it must have a value')
    else:
        return Cid


def display_records():
    global tree
    tree.delete(*tree.get_children())
    for record in repo.get_all_books():
        tree.insert('', END, values=record)


def clear_fields():
    global bk_status, bk_id, bk_name, author_name, card_id
    bk_status.set('Available')
    bk_id.set('')
    bk_name.set('')
    author_name.set('')
    card_id.set('')
    bk_id_entry.config(state='normal')
    try:
        tree.selection_remove(tree.selection()[0])
    except Exception:
        pass


def clear_and_display():
    clear_fields()
    display_records()


# ---------- CRUD actions (call the repository, no SQL here) ----------

def add_record():
    global bk_name, bk_id, author_name, bk_status, card_id

    if bk_status.get() == 'Issued':
        card_id.set(issuer_card())
    else:
        card_id.set('N/A')

    surety = mb.askyesno(
        'Are you sure?',
        'Are you sure this is the data you want to enter?\n'
        'Please note that Book ID cannot be changed in the future'
    )
    if not surety:
        return

    try:
        repo.add_book(bk_name.get(), bk_id.get(), author_name.get(), bk_status.get(), card_id.get())
        clear_and_display()
        mb.showinfo('Record added', 'The new record was successfully added to your database')
    except Exception:
        mb.showerror(
            'Book ID already in use!',
            'The Book ID you are trying to enter is already in the database, '
            'please alter that book\'s record or check any discrepancies on your side'
        )


def view_record():
    global bk_name, bk_id, bk_status, author_name, card_id, tree

    if not tree.focus():
        mb.showerror('Select a row!', 'To view a record, you must select it in the table. Please do so before continuing.')
        return

    values = tree.item(tree.focus())['values']
    bk_name.set(values[0])
    bk_id.set(values[1])
    author_name.set(values[2])
    bk_status.set(values[3])
    try:
        card_id.set(values[4])
    except IndexError:
        card_id.set('')


def update_record():
    def update():
        global bk_status, bk_name, bk_id, author_name, card_id

        if bk_status.get() == 'Issued':
            card_id.set(issuer_card())
        else:
            card_id.set('N/A')

        repo.update_book(bk_id.get(), bk_name.get(), bk_status.get(), author_name.get(), card_id.get())
        clear_and_display()
        edit.destroy()
        bk_id_entry.config(state='normal')
        clear.config(state='normal')

    view_record()
    bk_id_entry.config(state='disable')
    clear.config(state='disable')
    edit = Button(left_frame, text='Update Record', font=btn_font, bg=btn_hlb_bg, width=20, command=update)
    edit.place(x=50, y=375)


def remove_record():
    if not tree.selection():
        mb.showerror('Error!', 'Please select an item from the database')
        return

    values = tree.item(tree.focus())['values']
    repo.delete_book(values[1])
    mb.showinfo('Done', 'The record you wanted deleted was successfully deleted.')
    clear_and_display()


def delete_inventory():
    if mb.askyesno('Are you sure?', 'Are you sure you want to delete the entire inventory?\n\nThis command cannot be reversed'):
        repo.delete_all_books()
        clear_and_display()


def change_availability():
    if not tree.selection():
        mb.showerror('Error!', 'Please select a book from the database')
        return

    values = tree.item(tree.focus())['values']
    bk_id_val, bk_status_val = values[1], values[3]

    if bk_status_val == 'Issued':
        surety = mb.askyesno('Is return confirmed?', 'Has the book been returned to you?')
        if surety:
            repo.update_status(bk_id_val, 'Available', 'N/A')
        else:
            mb.showinfo('Cannot be returned', 'The book status cannot be set to Available unless it has been returned')
    else:
        repo.update_status(bk_id_val, 'Issued', issuer_card())

    clear_and_display()


# ---------- UI setup ----------

lf_bg = 'LightSkyBlue'
rtf_bg = 'DeepSkyBlue'
rbf_bg = 'DodgerBlue'
btn_hlb_bg = 'SteelBlue'
lbl_font = ('Georgia', 13)
entry_font = ('Times New Roman', 12)
btn_font = ('Gill Sans MT', 13)

root = Tk()
root.title('Library Management System')
root.geometry('1010x530')
root.resizable(0, 0)

Label(root, text='LIBRARY MANAGEMENT SYSTEM', font=("Noto Sans CJK TC", 15, 'bold'), bg=btn_hlb_bg, fg='White').pack(side=TOP, fill=X)

bk_status = StringVar()
bk_name = StringVar()
bk_id = StringVar()
author_name = StringVar()
card_id = StringVar()

left_frame = Frame(root, bg=lf_bg)
left_frame.place(x=0, y=30, relwidth=0.3, relheight=0.96)

RT_frame = Frame(root, bg=rtf_bg)
RT_frame.place(relx=0.3, y=30, relheight=0.2, relwidth=0.7)

RB_frame = Frame(root)
RB_frame.place(relx=0.3, rely=0.24, relheight=0.785, relwidth=0.7)

Label(left_frame, text='Book Name', bg=lf_bg, font=lbl_font).place(x=98, y=25)
Entry(left_frame, width=25, font=entry_font, text=bk_name).place(x=45, y=55)

Label(left_frame, text='Book ID', bg=lf_bg, font=lbl_font).place(x=110, y=105)
bk_id_entry = Entry(left_frame, width=25, font=entry_font, text=bk_id)
bk_id_entry.place(x=45, y=135)

Label(left_frame, text='Author Name', bg=lf_bg, font=lbl_font).place(x=90, y=185)
Entry(left_frame, width=25, font=entry_font, text=author_name).place(x=45, y=215)

Label(left_frame, text='Status of the Book', bg=lf_bg, font=lbl_font).place(x=75, y=265)
dd = OptionMenu(left_frame, bk_status, *['Available', 'Issued'])
dd.configure(font=entry_font, width=12)
dd.place(x=75, y=300)

submit = Button(left_frame, text='Add new record', font=btn_font, bg=btn_hlb_bg, width=20, command=add_record)
submit.place(x=50, y=375)

clear = Button(left_frame, text='Clear fields', font=btn_font, bg=btn_hlb_bg, width=20, command=clear_fields)
clear.place(x=50, y=435)

Button(RT_frame, text='Delete book record', font=btn_font, bg=btn_hlb_bg, width=17, command=remove_record).place(x=8, y=30)
Button(RT_frame, text='Delete full inventory', font=btn_font, bg=btn_hlb_bg, width=17, command=delete_inventory).place(x=178, y=30)
Button(RT_frame, text='Update book details', font=btn_font, bg=btn_hlb_bg, width=17, command=update_record).place(x=348, y=30)
Button(RT_frame, text='Change Book Availability', font=btn_font, bg=btn_hlb_bg, width=19, command=change_availability).place(x=518, y=30)

Label(RB_frame, text='BOOK INVENTORY', bg=rbf_bg, font=("Noto Sans CJK TC", 15, 'bold')).pack(side=TOP, fill=X)
tree = ttk.Treeview(RB_frame, selectmode=BROWSE, columns=('Book Name', 'Book ID', 'Author', 'Status', 'Issuer Card ID'))

XScrollbar = Scrollbar(tree, orient=HORIZONTAL, command=tree.xview)
YScrollbar = Scrollbar(tree, orient=VERTICAL, command=tree.yview)
XScrollbar.pack(side=BOTTOM, fill=X)
YScrollbar.pack(side=RIGHT, fill=Y)
tree.config(xscrollcommand=XScrollbar.set, yscrollcommand=YScrollbar.set)

tree.heading('Book Name', text='Book Name', anchor=CENTER)
tree.heading('Book ID', text='Book ID', anchor=CENTER)
tree.heading('Author', text='Author', anchor=CENTER)
tree.heading('Status', text='Status of the Book', anchor=CENTER)
tree.heading('Issuer Card ID', text='Card ID of the Issuer', anchor=CENTER)
tree.column('#0', width=0, stretch=NO)
tree.column('#1', width=225, stretch=NO)
tree.column('#2', width=70, stretch=NO)
tree.column('#3', width=150, stretch=NO)
tree.column('#4', width=105, stretch=NO)
tree.column('#5', width=132, stretch=NO)
tree.place(y=30, x=0, relheight=0.9, relwidth=1)

clear_and_display()

root.update()
root.mainloop()
