from tkinter import *
import tkinter as tk
from tkinter import ttk
import sqlite3
from Fragen_GUI_integration import Frage_bearbeiten, Neue_Frage


class MyDB_Tree():
    def __init__(self, frame, dbname, *args, **kwargs):
        self.Frame = frame
        #tk.Frame.__init__(self, *args, **kwargs)
        self.create_style()
        #Define Entry Variables
        self.q = StringVar()
        self.q1 = StringVar()
        self.q2 = StringVar()
        self.create_trv()
         #Insert Data from Database
        self.mydb_name = dbname
        self.mydb = sqlite3.connect(self.mydb_name)
        self.cursor = self.mydb.cursor()
        self.query = "SELECT Schwierigkeit, Typ, Titel, Author, Datum FROM testdb"
        self.cursor.execute(self.query)
        self.rows = self.cursor.fetchall()
        self.update()
        #Create Search Area
        self.Searchbox()
        #Bind Button Release to section of Item in Treeview
        self.trv.bind('<Double-Button-1>', self.Select_from_DB)
        self.ent.bind('<Return>', self.search)

    def create_trv(self):
        # Create Treview Frame
        self.DB_frame = tk.Frame(self.Frame)
        self.DB_frame.place(relx=0, rely=.1)
        # create Scrollbar
        self.vsb = ttk.Scrollbar(self.DB_frame)
        self.vsb.pack(side=RIGHT, fill=Y)
        # create Treeview
        self.trv = ttk.Treeview(self.DB_frame, columns=(1, 2, 3, 4, 5), show="headings", height=6,
                                style="mystyle.Treeview")
        self.trv.configure(yscrollcommand=self.vsb.set)
        self.trv.tag_configure('odd', background='#ff5733')
        self.trv.pack()
        # Create Treeview Headings
        self.trv.heading(1, text="Schwierigkeit")
        self.trv.heading(2, text="Typ")
        self.trv.heading(3, text="Titel")
        self.trv.heading(4, text="Author")
        self.trv.heading(5, text="Datum")
        # Format Columns
        self.trv.column(1, width=int(root.winfo_screenwidth() / 15), anchor=CENTER,
                        minwidth=int(root.winfo_screenwidth() / 30))
        self.trv.column(2, width=int(root.winfo_screenwidth() / 15), anchor=CENTER,
                        minwidth=int(root.winfo_screenwidth() / 30))
        self.trv.column(3, width=int(root.winfo_screenwidth() / 15), anchor=W,
                        minwidth=int(root.winfo_screenwidth() / 30))
        self.trv.column(4, width=int(root.winfo_screenwidth() / 15), anchor=W,
                        minwidth=int(root.winfo_screenwidth() / 30))
        self.trv.column(5, width=int(root.winfo_screenwidth() / 15), anchor=CENTER,
                        minwidth=int(root.winfo_screenwidth() / 30))

    def create_style(self):
        # Create Stryle for treeview
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0,
                        font=('Calibri', 11))  # Modify the font of the body
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 13, 'bold'))  # Modify the font of the headings
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])  # Remove the borders

    def get_DB_data(self):
        self.mydb_name = self.DBname
        self.mydb = sqlite3.connect(self.mydb_name)
        self.cursor = self.mydb.cursor()
        self.query = "SELECT Schwierigkeit, Typ, Titel, Author, Datum FROM testdb"
        self.cursor.execute(self.query)
        self.rows = self.cursor.fetchall()
        self.update()

    def selectItem(self, a):
        Auswahl = self.trv.focus()
        result = ''
        result = self.trv.item(Auswahl)

#creates the interaction UI for Treeview search
    def Searchbox(self, color):
        SearchBox = tk.Frame(self.Frame, bg=color)
        SearchBox.place(relwidth=1, relheight=.1)
        lbl = Label(SearchBox, text="Search")
        lbl.pack(side=LEFT, padx=10)
        self.ent = Entry(SearchBox, textvariable=self.q)
        self.ent.pack(side=LEFT, padx=6)
        cbtn = Button(SearchBox, text="Clear", command=self.clear)
        cbtn.pack(side=LEFT, padx=6)
        # todo delete funktionalität unsetzen
        del_btn = Button(SearchBox, text="delete", command=self.delete_selection)
        del_btn.pack(side=LEFT, padx=6)
        add_btn = Button(SearchBox, text="add", command=self.add)
        add_btn.pack(side=LEFT, padx=6)

    def add(self):
        self.nummer = self.nummer+1
        Titel = "Aufgabe "+ str(self.nummer)
        self.cursor.execute(
            "INSERT INTO testdb VALUES ('schwer', 'Typ E', :Titel, 'Waffenschmidt', '12.2.2021','ICH', 'Datum')", {'Titel': Titel})
        self.mydb.commit()
        self.clear()

    def delete_selection(self):
        gesucht = self.trv.item(self.trv.focus())
        print("Der Eintrag mit dem Titel: ", gesucht['values'][2], ", soll gelöscht werden")
        self.cursor.execute("DELETE  FROM testdb WHERE Typ LIKE '%" + gesucht['values'][1] + "%' AND Titel LIKE '%" + gesucht['values'][2] + "%'")
        #self.mydb.commit()
        self.clear()

#selects correlating date from Treeview selection from the Original DB
    def Select_from_DB(self, a):
        Auswahl = self.trv.focus()
        gesucht = self.trv.item(self.trv.focus())
        result = str(self.trv.item(Auswahl))
        print("Auswahl=", Auswahl)
        print(result)
        print("Titel gesucht:", gesucht['values'][2])
        print("Typ gesucht:", gesucht['values'][1])
        Work_on_question = Frage_bearbeiten(self.Frame, gesucht, self.mydb_name, self.clear)


    def give_selection(self):
        #print(len(self.trv.selection()))
        i = 0
        item_list = []

        for selection in self.trv.selection():
            item_list.append(self.trv.item(selection))
            print(self.trv.item(selection))
            print(i)
            i = i + 1

        return item_list

    def input_selected_data(self, selection):
        for item in selection:
            self.trv.insert('', 'end', values=item['values'])
            print(item['values'], "was input into Test")

    def update(self):
        self.trv.delete(*self.trv.get_children())
        for i in self.rows:
            self.trv.insert('', 'end', values=i)
            print(i)
#Searches Treeview

    def search(self, a):
        q2 = self.q.get() #get search text from entry
        self.query = " SELECT Schwierigkeit, Typ, Titel, Author, Datum FROM testdb Where Schwierigkeit LIKE '%" + q2 + "%' OR Typ LIKE '%" + q2 + "%' OR Titel LIKE '%" + q2 +"%' OR Author LIKE '%" + q2 +"%'"
        self.cursor.execute(self.query)
        self.rows = self.cursor.fetchall()
        self.update()

#Restores Datavisibility to its original state
    def clear(self):
        self.query = "SELECT Schwierigkeit, Typ, Titel, Author, Datum FROM testdb"
        self.cursor.execute(self.query)
        self.rows = self.cursor.fetchall()
        self.update()

class Frage_Trv(MyDB_Tree):
    def __init__(self, dbname, frame, *args, **kwargs):
        self.nummer = 5
        self.DBname = dbname
        self.Frame = frame
        self.create_style()
        # Define Entry Variables
        self.q = StringVar() #textvariable of search entry
        self.create_trv()
        # Insert Data from Database
        self.get_DB_data()
        # Create Search Area
        self.Searchbox("red")
        # Create Interaction Area like selction for further use in other Funktions
        self.trv.bind('<Double-Button-1>', self.Select_from_DB)
        self.ent.bind('<Return>', self.search)

class Test_Trv(MyDB_Tree):
    def __init__(self, dbname, frame, *args, **kwargs):
        self.DBname = dbname
        self.Frame = frame
        self.create_style()
        # Define Entry Variables
        self.q = StringVar()#textvariable of search entry
        self.create_trv()
        # Create Search Area
        self.Searchbox("orange")
        self.trv.bind('<Double-Button-1>', self.Select_from_DB) #todo changes questions in question DB
        self.ent.bind('<Return>', self.search)


class Main(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        Left_Frame = tk.Frame()
        Left_Frame.place(relx=0, rely=0, relwidth=.5, relheight=.9)
        Right_Frame = tk.Frame()
        Right_Frame.place(relx=0.5, rely=0, relwidth=.5, relheight=.9)
        bottom_Frame = tk.Frame(bg="blue")
        bottom_Frame.place(relx=0, rely=.9, relwidth=1, relheight=.1)
        mydb_name = '../testdb.db'
        self.trv_Fragen = Frage_Trv(mydb_name, Left_Frame)
        self.trv_Test = Test_Trv(mydb_name, Right_Frame)
        Put_btn = tk.Button(bottom_Frame, text="Add to Test", command=self.Move_data)
        Put_btn.place(relx=0, rely=0)

    def Move_data(self):
        self.trv_Test.input_selected_data(self.trv_Fragen.give_selection())

if __name__ == "__main__":
    root = tk.Tk()
    WIDTH = int(root.winfo_screenwidth() / 1.5)
    HEIGHT = int(root.winfo_screenheight() / 2)
    root.title("DB_List")
    root.resizable(False, False)
    root.geometry("%dx%d" % (WIDTH, HEIGHT))
    MainFrame = Main(root)
    MainFrame.pack(side="top")
    root.mainloop()