from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
from tkinter import ttk
import sqlite3
import xml.etree.ElementTree as ET
import webbrowser
from sympy import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
from tkscrolledframe import ScrolledFrame
import os


class GuiMainWindow:

    def __init__(self, master):
        self.master = master
        master.geometry = '800x710'
        master.title('ilias - Test-Generator')

        self.project_root = "C:\\Users\\tpantele\\Neues Projekt\\"
        
        # <------------ Define Tab Control for different QUestion-Tabs ----------->

        self.tabControl = ttk.Notebook(app)  # Create Tab Control

        # ---- Tab for Formula - Questions
        self.formula_tab = ttk.Frame(self.tabControl)  # Create a tab
        self.tabControl.add(self.formula_tab, text='Formelfrage')  # Add the tab

        # ---- Tab for Single Choice - Questions
        self.singleChoice_tab = ttk.Frame(self.tabControl)  # Create a tab
        self.tabControl.add(self.singleChoice_tab, text='Single Choice')  # Add the tab

        # ---- Tab for Multiple Choice - Questions
        self.multipleChoice_tab = ttk.Frame(self.tabControl)  # Create a tab
        self.tabControl.add(self.multipleChoice_tab, text='Multiple Choice')  # Add the tab

        self.tabControl.grid()  # Pack to make visible

        self.frame_test_title = LabelFrame(self.formula_tab, text="Testname & Autor", padx=5, pady=5)
        self.frame_test_title.grid(row=0, column=0, padx=10, pady=10, sticky=NW)

        self.frame_database = LabelFrame(self.formula_tab, text="Datenbank", padx=5, pady=5)
        self.frame_database.grid(row=10, column=0, padx=10, pady=10, sticky=NW)

        self.frame_picture = LabelFrame(self.formula_tab, text="Vorschau Bild", padx=5, pady=5)
        self.frame_picture.grid(row=1, column=1, padx=10, pady=10, sticky=NW)

        self.frame_db_picture = LabelFrame(self.formula_tab, text="DB Preview - Bild", padx=5, pady=5)
        self.frame_db_picture.grid(row=10, column=1, padx=10, pady=10, sticky="NW")

        self.frame_create_formelfrage = LabelFrame(self.formula_tab, text="Formelfrage erstellen", padx=5, pady=5)
        self.frame_create_formelfrage.grid(row=10, column=0, padx=10, pady=10, sticky="NE")

        #self.frame_edit_formelfrage = LabelFrame(self.formula_tab, text="Formelfrage editieren", padx=5, pady=5)
        #self.frame_edit_formelfrage.grid(row=11, column=0, padx=10, pady=10, sticky="NE")

        self.frame_latex_preview = LabelFrame(self.formula_tab, text="LaTeX Preview", padx=5, pady=5)
        self.frame_latex_preview.grid(row=9, column=0, padx=10, pady=10, sticky="NW")

        self.frame_question_difficulty = LabelFrame(self.formula_tab, text="Difficulty", padx=5, pady=5)
        self.frame_question_difficulty.grid(row=9, column=0, padx=170, pady=10, sticky="NW")

        self.frame_question_category = LabelFrame(self.formula_tab, text="Category", padx=5, pady=5)
        self.frame_question_category.grid(row=9, column=0, padx=10, pady=10, sticky="NE")

        self.frame_question_type = LabelFrame(self.formula_tab, text="Type", padx=5, pady=5)
        self.frame_question_type.grid(row=9, column=1, padx=10, pady=10, sticky="NW")

        # -------------------------------------------------------------------------------------------------------CREATE SINGLE QUESTION WITH FROM OID
        self.create_formelfrage_btn = Button(self.frame_create_formelfrage, text="Get oid and create", command=lambda: create_formelfrage.__init__(self))
        self.create_formelfrage_btn.grid(row=0, column=0, sticky=W)

        self.create_formelfrage_entry = Entry(self.frame_create_formelfrage, width=15)
        self.create_formelfrage_entry.grid(row=0, column=1, sticky=W, padx=20)

        #self.update_formelfrage_btn = Button(self.frame_create_formelfrage, text="Update Formelfrage", command=lambda: updateFormelFrage.__init__(self))
        #self.update_formelfrage_btn.grid(row=1, column=0, sticky=W)

        #self.update_formelfrage_entry = Entry(self.frame_create_formelfrage, width=6)
        #self.update_formelfrage_entry.grid(row=1, column=1, sticky=W, padx=20, pady=20)

        self.test_title_label = Label(self.frame_test_title, text="Name des Tests")
        self.test_title_label.grid(row=0, column=0, sticky=W)

        self.test_title_entry = Entry(self.frame_test_title, width=60)
        self.test_title_entry.grid(row=0, column=1, sticky=W, padx=30)

        self.autor_label = Label(self.frame_test_title, text="Autor")
        self.autor_label.grid(row=1, column=0, sticky=W)

        self.autor_entry = Entry(self.frame_test_title, width=60)
        self.autor_entry.grid(row=1, column=1, sticky=W, padx=30)




        self.show_frame_btn = Button(self.frame_database, text="Datenbank show", command=lambda: Database.__init__(self))
        self.show_frame_btn.grid(row=0, column=0)

        #self.remove_frame_btn = Button(self.formula_tab, text="Datenbank remove",command=lambda: Database.remove_database(self))
        #self.remove_frame_btn.grid(row=3, column=0)

        self.database_show_records_btn = Button(self.frame_database, text="Show Records",command=lambda: Database.show_records(self))
        self.database_show_records_btn.grid(row=1, column=0, sticky=W, pady=5)

        self.database_submit_btn = Button(self.frame_database, text="Submit", command=lambda: Database.submit(self))
        self.database_submit_btn.grid(row=2, column=0, sticky=W, pady=5)

        self.database_delete_btn = Button(self.frame_database, text="Delete", command=lambda: Database.delete(self))
        self.database_delete_btn.grid(row=3, column=0, sticky=W, pady=5)

        self.delete_box = Entry(self.frame_database, width=5)
        self.delete_box.grid(row=3, column=1, sticky=W)

        show_test_settings_formula_tab = Button(self.formula_tab, text="Test-Einstellungen",command=lambda: self.test_settings())
        show_test_settings_formula_tab.grid(row=4, column=0)




        self.img_select_btn = Button(self.frame_picture, text="Add Image", command=lambda: Database.open_image(self))
        self.img_select_btn.grid(row=2, column=0, sticky=W)

        self.img_remove_btn = Button(self.frame_picture, text="Remove Image", command=lambda: Database.delete_image(self))
        self.img_remove_btn.grid(row=2, column=1, sticky=W)

        self.save_img_to_db_btn = Button(self.frame_picture, text="Save to DB",command=lambda: Database.save_image_to_db(self))
        self.save_img_to_db_btn.grid(row=2, column=2, sticky=W)

        self.show_img_from_db_btn = Button(self.frame_db_picture, text="IMG from DB",command=lambda: Database.show_img_from_db(self))
        self.show_img_from_db_btn.grid(row=2, column=3, sticky=W)

        self.myLatex_btn = Button(self.frame_latex_preview, text="show LaTeX Preview", command=lambda:LatexPreview.__init__(self) )
        self.myLatex_btn.grid(row=0, column=0, sticky=W)

        self.question_difficulty_label = Label(self.frame_question_difficulty, text="Schwierigkeitsgrad der Frage")
        self.question_difficulty_label.grid(row=0, column=0, pady=5, padx=5)

        self.question_difficulty_entry = Entry(self.frame_question_difficulty, width=10)
        self.question_difficulty_entry.grid(row=0, column=1, pady=5, padx=5)

        self.question_category_label = Label(self.frame_question_category, text="Fragenkategorie")
        self.question_category_label.grid(row=0, column=0, pady=5, padx=5)

        self.question_category_entry = Entry(self.frame_question_category, width=15)
        self.question_category_entry.grid(row=0, column=1, pady=5, padx=5)

        self.question_type_label = Label(self.frame_question_type, text="Fragen-Typ")
        self.question_type_label.grid(row=0, column=0, pady=5, padx=5)

        self.question_type_entry = Entry(self.frame_question_type, width=10)
        self.question_type_entry.grid(row=0, column=1, pady=5, padx=5)

        #filename_label = Label(self.frame_picture, text="EMTPY")
        self.picture_name = "EMPTY"
        # ---Init Variable Matrix
        Formelfrage.__init__(self)
        #MultipleChoice.__init__(self)

        # ---Init MC-TAB
    # MultipleChoice.__init__(self, self.multipleChoice_tab)

    # ---Init MC-TAB
    # SingleChoice.__init__(self, self.singleChoice_tab)


    #create table / Database
    def createDatabase(self):
        print("DATABASE CREATED!")
        # Create a database or connect to one
        conn = sqlite3.connect('ilias_questions_db.db')

        # Create cursor
        c = conn.cursor()

        # Create table
        c.execute("""CREATE TABLE IF NOT EXISTS my_table (
                question_difficulty text,
                question_category text,
                question_type text,
                question_title text,
                question_description_title text,
                question_description_main text,
                res1_formula text,
                res2_formula text,
                res3_formula text,
                var1_name text,
                var1_min int,
                var1_max int,
                var1_prec int,
                var1_divby int,
                var2_name text,
                var2_min int,
                var2_max int,
                var2_prec int,
                var2_divby int,
                var3_name text,
                var3_min int,
                var3_max int,
                var3_prec int,
                var3_divby int,
                var4_name text,
                var4_min int,
                var4_max int,
                var4_prec int,
                var4_divby int,
                var5_name text,
                var5_min int,
                var5_max int,
                var5_prec int,
                var5_divby int,
                var6_name text,
                var6_min int,
                var6_max int,
                var6_prec int,
                var6_divby int,
                var7_name text,
                var7_min int,
                var7_max int,
                var7_prec int,
                var7_divby int,
                res1_name text,
                res1_min int,
                res1_max int,
                res1_prec int,
                res1_tol int,
                res1_points int,
                res2_name text,
                res2_min int,
                res2_max int,
                res2_prec int,
                res2_tol int,
                res2_points int,
                res3_name text,
                res3_min int,
                res3_max int,
                res3_prec int,
                res3_tol int,
                res3_points int,
                img_name text,
                img_data blop,
                test_time text
                )""")

        # Commit Changes
        conn.commit()

        # Close Connection
        conn.close()
    def test_settings(self):
        GUI_settings_window.__init__(self, self.formula_tab)
class Formelfrage(GuiMainWindow):

    def __init__(self):
        #only need to create Databse once
        #self.createDatabase()
        self.frame_formula = LabelFrame(self.formula_tab, text="Formelfrage", padx=5, pady=5)
        self.frame_formula.grid(row=1, column=0, padx=10, pady=10, sticky=NW)

        ###############

        self.question_title_label = Label(self.frame_formula, text="Titel")
        self.question_title_label.grid(row=0, column=0, sticky=W, padx=10, pady=(10, 0))
        self.question_title_entry = Entry(self.frame_formula, width=60)
        self.question_title_entry.grid(row=0, column=1, pady=(10, 0), sticky=W)

        self.question_description_label = Label(self.frame_formula, text="Beschreibung")
        self.question_description_label.grid(row=2, column=0, sticky=W, padx=10)
        self.question_description_entry = Entry(self.frame_formula, width=60)
        self.question_description_entry.grid(row=2, column=1, sticky=W)

        self.question_description_textfield_label = Label(self.frame_formula, text="Frage")
        self.question_description_textfield_label.grid(row=3, column=0, sticky=W, padx=10)

        self.bar = Scrollbar(self.frame_formula)
        self.formula_question_entry = Text(self.frame_formula, height=4, width=52, font=('Helvetica', 9))
        self.bar.grid(row=3, column=2, sticky=W)
        self.formula_question_entry.grid(row=3, column=1, pady=10, sticky=W)
        self.bar.config(command=self.formula_question_entry.yview)
        self.formula_question_entry.config(yscrollcommand=self.bar.set)

        self.formula_processing_time_label = Label(self.frame_formula, text="Bearbeitungsdauer")
        self.formula_processing_time_label.grid(row=4, column=0, sticky=W, pady=(5, 0), padx=10)

        self.formula_processing_time_label = Label(self.frame_formula, text="Std:")
        self.formula_processing_time_label.grid(row=4, column=1, sticky=W, pady=(5, 0))
        self.formula_processing_time_label = Label(self.frame_formula, text="Min:")
        self.formula_processing_time_label.grid(row=4, column=1, sticky=W, padx=70, pady=(5, 0))
        self.formula_processing_time_label = Label(self.frame_formula, text="Sek:")
        self.formula_processing_time_label.grid(row=4, column=1, sticky=W, padx=145, pady=(5, 0))






        #########




        self.processingtime_hours = list(range(24))
        self.processingtime_minutes = list(range(60))
        self.processingtime_seconds = list(range(60))

        self.proc_hours_box = ttk.Combobox(self.frame_formula, value=self.processingtime_hours, width=2)
        self.proc_minutes_box = ttk.Combobox(self.frame_formula, value=self.processingtime_minutes, width=2)
        self.proc_seconds_box = ttk.Combobox(self.frame_formula, value=self.processingtime_seconds, width=2)

        self.proc_hours_box.current(0)
        self.proc_minutes_box.current(0)
        self.proc_seconds_box.current(0)

        def selected_hours(event):
            self.selected_hours = self.proc_hours_box.get()
            print(self.selected_hours)

        def selected_minutes(event):
            self.selected_minutes = self.proc_minutes_box.get()
            print(self.selected_minutes)

        def selected_seconds(event):
            self.selected_seconds = self.proc_seconds_box.get()
            print(self.selected_seconds)

        self.proc_hours_box.bind("<<ComboboxSelected>>", selected_hours)
        self.proc_minutes_box.bind("<<ComboboxSelected>>", selected_minutes)
        self.proc_seconds_box.bind("<<ComboboxSelected>>", selected_seconds)

        self.proc_hours_box.grid(row=4, column=1, sticky=W, padx=25, pady=(5, 0))
        self.proc_minutes_box.grid(row=4, column=1, sticky=W, padx=100, pady=(5, 0))
        self.proc_seconds_box.grid(row=4, column=1, sticky=W, padx=170, pady=(5, 0))

        ################
        self.var_min_label = Label(self.frame_formula, text=' min')
        self.var_min_label.grid(row=5, column=1, sticky=W, pady=(20, 0), padx=60)

        self.var_max_label = Label(self.frame_formula, text=' max')
        self.var_max_label.grid(row=5, column=1, sticky=W, pady=(20, 0), padx=100)

        self.var_prec_label = Label(self.frame_formula, text=' prec')
        self.var_prec_label.grid(row=5, column=1, sticky=W, pady=(20, 0), padx=140)

        self.var_divby_label = Label(self.frame_formula, text=' divby')
        self.var_divby_label.grid(row=5, column=1, sticky=W, pady=(20, 0), padx=180)

        # ------------------------------- VARIABLES - TEXT & ENTRY --------------------------------------------
        self.var1_name_text, self.var1_min_text, self.var1_max_text, self.var1_prec_text, self.var1_divby_text = StringVar(), StringVar(), StringVar(), StringVar(), StringVar()
        self.var2_name_text, self.var2_min_text, self.var2_max_text, self.var2_prec_text, self.var2_divby_text = StringVar(), StringVar(), StringVar(), StringVar(), StringVar()
        self.var3_name_text, self.var3_min_text, self.var3_max_text, self.var3_prec_text, self.var3_divby_text = StringVar(), StringVar(), StringVar(), StringVar(), StringVar()
        self.var4_name_text, self.var4_min_text, self.var4_max_text, self.var4_prec_text, self.var4_divby_text = StringVar(), StringVar(), StringVar(), StringVar(), StringVar()
        self.var5_name_text, self.var5_min_text, self.var5_max_text, self.var5_prec_text, self.var5_divby_text = StringVar(), StringVar(), StringVar(), StringVar(), StringVar()
        self.var6_name_text, self.var6_min_text, self.var6_max_text, self.var6_prec_text, self.var6_divby_text = StringVar(), StringVar(), StringVar(), StringVar(), StringVar()
        self.var7_name_text, self.var7_min_text, self.var7_max_text, self.var7_prec_text, self.var7_divby_text = StringVar(), StringVar(), StringVar(), StringVar(), StringVar()

        self.var1_name_entry = Entry(self.frame_formula, textvariable=self.var1_name_text, width=6)
        self.var2_name_entry = Entry(self.frame_formula, textvariable=self.var2_name_text, width=6)
        self.var3_name_entry = Entry(self.frame_formula, textvariable=self.var3_name_text, width=6)
        self.var4_name_entry = Entry(self.frame_formula, textvariable=self.var4_name_text, width=6)
        self.var5_name_entry = Entry(self.frame_formula, textvariable=self.var5_name_text, width=6)
        self.var6_name_entry = Entry(self.frame_formula, textvariable=self.var6_name_text, width=6)
        self.var7_name_entry = Entry(self.frame_formula, textvariable=self.var7_name_text, width=6)

        self.var1_min_entry = Entry(self.frame_formula, textvariable=self.var1_min_text, width=6)
        self.var2_min_entry = Entry(self.frame_formula, textvariable=self.var2_min_text, width=6)
        self.var3_min_entry = Entry(self.frame_formula, textvariable=self.var3_min_text, width=6)
        self.var4_min_entry = Entry(self.frame_formula, textvariable=self.var4_min_text, width=6)
        self.var5_min_entry = Entry(self.frame_formula, textvariable=self.var5_min_text, width=6)
        self.var6_min_entry = Entry(self.frame_formula, textvariable=self.var6_min_text, width=6)
        self.var7_min_entry = Entry(self.frame_formula, textvariable=self.var7_min_text, width=6)

        # ------------------------------- VARIABLES RANGE:  MAXIMUM - TEXT & ENTRY --------------------------------------------

        self.var1_max_entry = Entry(self.frame_formula, textvariable=self.var1_max_text, width=6)
        self.var2_max_entry = Entry(self.frame_formula, textvariable=self.var2_max_text, width=6)
        self.var3_max_entry = Entry(self.frame_formula, textvariable=self.var3_max_text, width=6)
        self.var4_max_entry = Entry(self.frame_formula, textvariable=self.var4_max_text, width=6)
        self.var5_max_entry = Entry(self.frame_formula, textvariable=self.var5_max_text, width=6)
        self.var6_max_entry = Entry(self.frame_formula, textvariable=self.var6_max_text, width=6)
        self.var7_max_entry = Entry(self.frame_formula, textvariable=self.var7_max_text, width=6)

        # ------------------------------- VARIABLES PRECISION - TEXT & ENTRY --------------------------------------------

        self.var1_prec_entry = Entry(self.frame_formula, textvariable=self.var1_prec_text, width=6)
        self.var2_prec_entry = Entry(self.frame_formula, textvariable=self.var2_prec_text, width=6)
        self.var3_prec_entry = Entry(self.frame_formula, textvariable=self.var3_prec_text, width=6)
        self.var4_prec_entry = Entry(self.frame_formula, textvariable=self.var4_prec_text, width=6)
        self.var5_prec_entry = Entry(self.frame_formula, textvariable=self.var5_prec_text, width=6)
        self.var6_prec_entry = Entry(self.frame_formula, textvariable=self.var6_prec_text, width=6)
        self.var7_prec_entry = Entry(self.frame_formula, textvariable=self.var7_prec_text, width=6)

        # ------------------------------- VARIABLES DIVISIBLE BY - TEXT & ENTRY --------------------------------------------

        self.var1_divby_entry = Entry(self.frame_formula, textvariable=self.var1_divby_text, width=6)
        self.var2_divby_entry = Entry(self.frame_formula, textvariable=self.var2_divby_text, width=6)
        self.var3_divby_entry = Entry(self.frame_formula, textvariable=self.var3_divby_text, width=6)
        self.var4_divby_entry = Entry(self.frame_formula, textvariable=self.var4_divby_text, width=6)
        self.var5_divby_entry = Entry(self.frame_formula, textvariable=self.var5_divby_text, width=6)
        self.var6_divby_entry = Entry(self.frame_formula, textvariable=self.var6_divby_text, width=6)
        self.var7_divby_entry = Entry(self.frame_formula, textvariable=self.var7_divby_text, width=6)

        def selected_var(event):  # "variable" need for comboBox Binding

            if self.myCombo.get() == '1':
                var2_remove()
                var3_remove()
                var4_remove()
                var5_remove()
                var6_remove()
                var7_remove()

            elif self.myCombo.get() == '2':
                var2_show()
                var3_remove()
                var4_remove()
                var5_remove()
                var6_remove()
                var7_remove()

            elif self.myCombo.get() == '3':
                var2_show()
                var3_show()
                var4_remove()
                var5_remove()
                var6_remove()
                var7_remove()

            elif self.myCombo.get() == '4':
                var2_show()
                var3_show()
                var4_show()
                var5_remove()
                var6_remove()
                var7_remove()

            elif self.myCombo.get() == '5':
                var2_show()
                var3_show()
                var4_show()
                var5_show()
                var6_remove()
                var7_remove()

            elif self.myCombo.get() == '6':
                var2_show()
                var3_show()
                var4_show()
                var5_show()
                var6_show()
                var7_remove()

            elif self.myCombo.get() == '7':
                var2_show()
                var3_show()
                var4_show()
                var5_show()
                var6_show()
                var7_show()

        self.num_of_vari_label = Label(self.frame_formula, text="Anzahl der Variablen: ")
        self.num_of_vari_label.grid(row=5, column=0, sticky=W, padx=10, pady=(20, 0))

        self.options_var = ["1", "2", "3", "4", "5", "6", "7"]

        self.myCombo = ttk.Combobox(self.frame_formula, value=self.options_var, width=3)
        self.myCombo.current(0)
        self.myCombo.bind("<<ComboboxSelected>>", selected_var)
        self.myCombo.grid(row=5, column=1, sticky=W, pady=(20, 0))

        self.variable1_label = Label(self.frame_formula, text='Variable 1')
        self.variable1_label.grid(row=6, column=0, sticky=W, padx=20)
        self.variable2_label = Label(self.frame_formula, text='Variable 2')
        self.variable3_label = Label(self.frame_formula, text='Variable 3')
        self.variable4_label = Label(self.frame_formula, text='Variable 4')
        self.variable5_label = Label(self.frame_formula, text='Variable 5')
        self.variable6_label = Label(self.frame_formula, text='Variable 6')
        self.variable7_label = Label(self.frame_formula, text='Variable 7')

        # -----------------------Place Label & Entry-Boxes for Variable 1 on GUI

        self.var1_name_entry.grid(row=6, column=1, sticky=W)
        self.var1_min_entry.grid(row=6, column=1, sticky=W, padx=60)
        self.var1_max_entry.grid(row=6, column=1, sticky=W, padx=100)
        self.var1_prec_entry.grid(row=6, column=1, sticky=W, padx=140)
        self.var1_divby_entry.grid(row=6, column=1, sticky=W, padx=180)

        # -----------------------Place Label & Entry-Boxes for Variable 2 on GUI
        def var2_show():
            self.variable2_label.grid(row=7, column=0, sticky=W, padx=20)
            self.var2_name_entry.grid(row=7, column=1, sticky=W)
            self.var2_min_entry.grid(row=7, column=1, sticky=W, padx=60)
            self.var2_max_entry.grid(row=7, column=1, sticky=W, padx=100)
            self.var2_prec_entry.grid(row=7, column=1, sticky=W, padx=140)
            self.var2_divby_entry.grid(row=7, column=1, sticky=W, padx=180)

        # -----------------------Place Label & Entry-Boxes for Variable 3 on GUI
        def var3_show():
            self.variable3_label.grid(row=8, column=0, sticky=W, padx=20)
            self.var3_name_entry.grid(row=8, column=1, sticky=W)
            self.var3_min_entry.grid(row=8, column=1, sticky=W, padx=60)
            self.var3_max_entry.grid(row=8, column=1, sticky=W, padx=100)
            self.var3_prec_entry.grid(row=8, column=1, sticky=W, padx=140)
            self.var3_divby_entry.grid(row=8, column=1, sticky=W, padx=180)

        # -----------------------Place Label & Entry-Boxes for Variable 4 on GUI
        def var4_show():
            self.variable4_label.grid(row=9, column=0, sticky=W, padx=20)
            self.var4_name_entry.grid(row=9, column=1, sticky=W)
            self.var4_min_entry.grid(row=9, column=1, sticky=W, padx=60)
            self.var4_max_entry.grid(row=9, column=1, sticky=W, padx=100)
            self.var4_prec_entry.grid(row=9, column=1, sticky=W, padx=140)
            self.var4_divby_entry.grid(row=9, column=1, sticky=W, padx=180)

        # -----------------------Place Label & Entry-Boxes for Variable 5 on GUI
        def var5_show():
            self.variable5_label.grid(row=10, column=0, sticky=W, padx=20)
            self.var5_name_entry.grid(row=10, column=1, sticky=W)
            self.var5_min_entry.grid(row=10, column=1, sticky=W, padx=60)
            self.var5_max_entry.grid(row=10, column=1, sticky=W, padx=100)
            self.var5_prec_entry.grid(row=10, column=1, sticky=W, padx=140)
            self.var5_divby_entry.grid(row=10, column=1, sticky=W, padx=180)

        # -----------------------Place Label & Entry-Boxes for Variable 6 on GUI
        def var6_show():
            self.variable6_label.grid(row=11, column=0, sticky=W, padx=20)
            self.var6_name_entry.grid(row=11, column=1, sticky=W)
            self.var6_min_entry.grid(row=11, column=1, sticky=W, padx=60)
            self.var6_max_entry.grid(row=11, column=1, sticky=W, padx=100)
            self.var6_prec_entry.grid(row=11, column=1, sticky=W, padx=140)
            self.var6_divby_entry.grid(row=11, column=1, sticky=W, padx=180)

        # -----------------------Place Label & Entry-Boxes for Variable 7 on GUI
        def var7_show():
            self.variable7_label.grid(row=12, column=0, sticky=W, padx=20)
            self.var7_name_entry.grid(row=12, column=1, sticky=W)
            self.var7_min_entry.grid(row=12, column=1, sticky=W, padx=60)
            self.var7_max_entry.grid(row=12, column=1, sticky=W, padx=100)
            self.var7_prec_entry.grid(row=12, column=1, sticky=W, padx=140)
            self.var7_divby_entry.grid(row=12, column=1, sticky=W, padx=180)

        def var2_remove():
            self.variable2_label.grid_remove()
            self.var2_name_entry.grid_remove()
            self.var2_min_entry.grid_remove()
            self.var2_max_entry.grid_remove()
            self.var2_prec_entry.grid_remove()
            self.var2_divby_entry.grid_remove()

        def var3_remove():
            self.variable3_label.grid_remove()
            self.var3_name_entry.grid_remove()
            self.var3_min_entry.grid_remove()
            self.var3_max_entry.grid_remove()
            self.var3_prec_entry.grid_remove()
            self.var3_divby_entry.grid_remove()

        def var4_remove():
            self.variable4_label.grid_remove()
            self.var4_name_entry.grid_remove()
            self.var4_min_entry.grid_remove()
            self.var4_max_entry.grid_remove()
            self.var4_prec_entry.grid_remove()
            self.var4_divby_entry.grid_remove()

        def var5_remove():
            self.variable5_label.grid_remove()
            self.var5_name_entry.grid_remove()
            self.var5_min_entry.grid_remove()
            self.var5_max_entry.grid_remove()
            self.var5_prec_entry.grid_remove()
            self.var5_divby_entry.grid_remove()

        def var6_remove():
            self.variable6_label.grid_remove()
            self.var6_name_entry.grid_remove()
            self.var6_min_entry.grid_remove()
            self.var6_max_entry.grid_remove()
            self.var6_prec_entry.grid_remove()
            self.var6_divby_entry.grid_remove()

        def var7_remove():
            self.variable7_label.grid_remove()
            self.var7_name_entry.grid_remove()
            self.var7_min_entry.grid_remove()
            self.var7_max_entry.grid_remove()
            self.var7_prec_entry.grid_remove()
            self.var7_divby_entry.grid_remove()

        # ------------------------Result 1 - Min/Max Range / Precision / Tolerance / Points

        # res1_label = Label(self.frame_formula, text='Result 1')

        self.res1_name_text, self.res1_min_text, self.res1_max_text, self.res1_prec_text, self.res1_tol_text, self.res1_points_text = StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar()
        self.res2_name_text, self.res2_min_text, self.res2_max_text, self.res2_prec_text, self.res2_tol_text, self.res2_points_text = StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar()
        self.res3_name_text, self.res3_min_text, self.res3_max_text, self.res3_prec_text, self.res3_tol_text, self.res3_points_text = StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar()
        self.res1_formula_text, self.res2_formula_text, self.res3_formula_text = StringVar(), StringVar(), StringVar()

        self.res_name_label = Label(self.frame_formula, text=' result')
        self.res_min_label = Label(self.frame_formula, text=' min')
        self.res_max_label = Label(self.frame_formula, text=' max')
        self.res_prec_label = Label(self.frame_formula, text=' prec')
        self.res_tol_label = Label(self.frame_formula, text='  tol')
        self.res_points_label = Label(self.frame_formula, text='points')
        self.res_formula_label = Label(self.frame_formula, text='formula')

        self.res_min_label.grid(row=20, column=1, sticky=W, pady=(10, 0), padx=60)
        self.res_max_label.grid(row=20, column=1, sticky=W, pady=(10, 0), padx=100)
        self.res_prec_label.grid(row=20, column=1, sticky=W, pady=(10, 0), padx=140)
        self.res_tol_label.grid(row=20, column=1, sticky=W, pady=(10, 0), padx=180)
        self.res_points_label.grid(row=20, column=1, sticky=W, pady=(10, 0), padx=220)
        self.res_formula_label.grid(row=20, column=1, sticky=E, pady=(10, 0), padx=100)

        self.res1_name_entry = Entry(self.frame_formula, textvariable=self.res1_name_text, width=6)
        self.res1_min_entry = Entry(self.frame_formula, textvariable=self.res1_min_text, width=6)
        self.res1_max_entry = Entry(self.frame_formula, textvariable=self.res1_max_text, width=6)
        self.res1_prec_entry = Entry(self.frame_formula, textvariable=self.res1_prec_text, width=6)
        self.res1_tol_entry = Entry(self.frame_formula, textvariable=self.res1_tol_text, width=6)
        self.res1_points_entry = Entry(self.frame_formula, textvariable=self.res1_points_text, width=6)
        self.res1_formula_entry = Entry(self.frame_formula, textvariable=self.res1_formula_text, width=30)

        self.res2_name_entry = Entry(self.frame_formula, textvariable=self.res2_name_text, width=6)
        self.res2_min_entry = Entry(self.frame_formula, textvariable=self.res2_min_text, width=6)
        self.res2_max_entry = Entry(self.frame_formula, textvariable=self.res2_max_text, width=6)
        self.res2_prec_entry = Entry(self.frame_formula, textvariable=self.res2_prec_text, width=6)
        self.res2_tol_entry = Entry(self.frame_formula, textvariable=self.res2_tol_text, width=6)
        self.res2_points_entry = Entry(self.frame_formula, textvariable=self.res2_points_text, width=6)
        self.res2_formula_entry = Entry(self.frame_formula, textvariable=self.res2_formula_text, width=30)


        self.res3_name_entry = Entry(self.frame_formula, textvariable=self.res3_name_text, width=6)
        self.res3_min_entry = Entry(self.frame_formula, textvariable=self.res3_min_text, width=6)
        self.res3_max_entry = Entry(self.frame_formula, textvariable=self.res3_max_text, width=6)
        self.res3_prec_entry = Entry(self.frame_formula, textvariable=self.res3_prec_text, width=6)
        self.res3_tol_entry = Entry(self.frame_formula, textvariable=self.res3_tol_text, width=6)
        self.res3_points_entry = Entry(self.frame_formula, textvariable=self.res3_points_text, width=6)
        self.res3_formula_entry = Entry(self.frame_formula, textvariable=self.res3_formula_text, width=30)


        self.res1_name_entry.grid(row=21, column=1, sticky=W)
        self.res1_min_entry.grid(row=21, column=1, sticky=W, padx=60)
        self.res1_max_entry.grid(row=21, column=1, sticky=W, padx=100)
        self.res1_prec_entry.grid(row=21, column=1, sticky=W, padx=140)
        self.res1_tol_entry.grid(row=21, column=1, sticky=W, padx=180)
        self.res1_points_entry.grid(row=21, column=1, sticky=W, padx=220)
        self.res1_formula_entry.grid(row=21, column=1, sticky=E, padx=20)

        def selected_res(event):  # "variable" need for comboBox Binding

            if self.myCombo_res.get() == '1':
                res2_remove()
                res3_remove()

            elif self.myCombo_res.get() == '2':
                res2_show()
                res3_remove()

            elif self.myCombo_res.get() == '3':
                res2_show()
                res3_show()

        self.num_of_res_label = Label(self.frame_formula, text="Anzahl der Ergebnisse: ")
        self.num_of_res_label.grid(row=20, column=0, sticky=W, padx=10, pady=(20, 0))

        self.options_res = ["1", "2", "3"]

        self.myCombo_res = ttk.Combobox(self.frame_formula, value=self.options_res, width=3)
        self.myCombo_res.current(0)
        self.myCombo_res.bind("<<ComboboxSelected>>", selected_res)
        self.myCombo_res.grid(row=20, column=1, sticky=W, pady=(20, 0))

        self.result1_label = Label(self.frame_formula, text='Ergebnis 1')
        self.result1_label.grid(row=21, column=0, sticky=W, padx=20)
        self.result2_label = Label(self.frame_formula, text='Ergebnis 2')
        self.result3_label = Label(self.frame_formula, text='Ergebnis 3')


        def res2_show():
            self.result2_label.grid(row=22, column=0, sticky=W, padx=20)
            self.res2_name_entry.grid(row=22, column=1, sticky=W)
            self.res2_min_entry.grid(row=22, column=1, sticky=W, padx=60)
            self.res2_max_entry.grid(row=22, column=1, sticky=W, padx=100)
            self.res2_prec_entry.grid(row=22, column=1, sticky=W, padx=140)
            self.res2_tol_entry.grid(row=22, column=1, sticky=W, padx=180)
            self.res2_points_entry.grid(row=22, column=1, sticky=W, padx=220)
            self.res2_formula_entry.grid(row=22, column=1, sticky=E, padx=20)

        def res3_show():
            self.result3_label.grid(row=23, column=0, sticky=W, padx=20)
            self.res3_name_entry.grid(row=23, column=1, sticky=W)
            self.res3_min_entry.grid(row=23, column=1, sticky=W, padx=60)
            self.res3_max_entry.grid(row=23, column=1, sticky=W, padx=100)
            self.res3_prec_entry.grid(row=23, column=1, sticky=W, padx=140)
            self.res3_tol_entry.grid(row=23, column=1, sticky=W, padx=180)
            self.res3_points_entry.grid(row=23, column=1, sticky=W, padx=220)
            self.res3_formula_entry.grid(row=23, column=1, sticky=E, padx=20)

        def res2_remove():
            self.result2_label.grid_remove()
            self.res2_name_entry.grid_remove()
            self.res2_min_entry.grid_remove()
            self.res2_max_entry.grid_remove()
            self.res2_prec_entry.grid_remove()
            self.res2_tol_entry.grid_remove()
            self.res2_points_entry.grid_remove()

        def res3_remove():
            self.result3_label.grid_remove()
            self.res3_name_entry.grid_remove()
            self.res3_min_entry.grid_remove()
            self.res3_max_entry.grid_remove()
            self.res3_prec_entry.grid_remove()
            self.res3_tol_entry.grid_remove()
            self.res3_points_entry.grid_remove()




class Database(Formelfrage):

    def __init__(self):

        self.database_window = Tk()
        self.database_window.title("Datenbank")


        #self.expand_db_btn = Button(self.frame_picture, text="<< Expand View >>", command=lambda: Database.expand_db(self))
        #self.expand_db_btn.grid(row=2, column=3, sticky=W)

        # Create a ScrolledFrame widget
        self.sf = ScrolledFrame(self.database_window, width=1000, height=300)
        self.sf.grid()

        # Bind the arrow keys and scroll wheel
        self.sf.bind_arrow_keys(app)
        self.sf.bind_scroll_wheel(app)

        # Create a frame within the ScrolledFrame
        self.db_inner_frame = self.sf.display_widget(Frame)


        # CREATE LISTBOXES ON GUI

        self.oid_listbox_label = Label(self.db_inner_frame, text=" DB\nID")
        self.oid_listbox_label.grid(row=25, column=1, sticky=W)

        self.question_difficulty_listbox_label = Label(self.db_inner_frame, text="Question Difficulty")
        self.question_difficulty_listbox_label.grid(row=25, column=2, sticky=W)

        self.question_category_listbox_label = Label(self.db_inner_frame, text="Question Category")
        self.question_category_listbox_label.grid(row=25, column=3, sticky=W)

        self.question_type_listbox_label = Label(self.db_inner_frame, text="Question Type")
        self.question_type_listbox_label.grid(row=25, column=4, sticky=W)


        self.question_title_listbox_label = Label(self.db_inner_frame, text="Title", width=15)
        self.question_title_listbox_label.grid(row=25, column=5, sticky=W)

        self.question_description_title_listbox_label = Label(self.db_inner_frame, text="Description Title", width=15)
        self.question_description_title_listbox_label.grid(row=25, column=6, sticky=W)

        self.question_description_main_listbox_label = Label(self.db_inner_frame, text="Description Main", width=15)
        self.question_description_main_listbox_label.grid(row=25, column=7, sticky=W)


        self.res1_formula_listbox_label = Label(self.db_inner_frame, text="Formula 1", width=15)
        self.res1_formula_listbox_label.grid(row=25, column=8, sticky=W)

        self.res2_formula_listbox_label = Label(self.db_inner_frame, text="Formula 2", width=15)
        self.res2_formula_listbox_label.grid(row=25, column=9, sticky=W)

        self.res3_formula_listbox_label = Label(self.db_inner_frame, text="Formula 3", width=15)
        self.res3_formula_listbox_label.grid(row=25, column=10, sticky=W)

        self.var1_name_listbox_label = Label(self.db_inner_frame, text="var1\nname")
        self.var1_name_listbox_label.grid(row=25, column=11, sticky=W)
        self.var1_min_listbox_label = Label(self.db_inner_frame, text="var1\nmin")
        self.var1_min_listbox_label.grid(row=25, column=12, sticky=W)
        self.var1_max_listbox_label = Label(self.db_inner_frame, text="var1\nmax")
        self.var1_max_listbox_label.grid(row=25, column=13, sticky=W)
        self.var1_prec_listbox_label = Label(self.db_inner_frame, text="var1\nprec")
        self.var1_prec_listbox_label.grid(row=25, column=14, sticky=W)
        self.var1_divby_listbox_label = Label(self.db_inner_frame, text="var1\ndivby")
        self.var1_divby_listbox_label.grid(row=25, column=15, sticky=W)

        self.var2_name_listbox_label = Label(self.db_inner_frame, text="var2\nname")
        self.var2_name_listbox_label.grid(row=25, column=16, sticky=W)
        self.var2_min_listbox_label = Label(self.db_inner_frame, text="var2\nmin")
        self.var2_min_listbox_label.grid(row=25, column=17, sticky=W)
        self.var2_max_listbox_label = Label(self.db_inner_frame, text="var2\nmax")
        self.var2_max_listbox_label.grid(row=25, column=18, sticky=W)
        self.var2_prec_listbox_label = Label(self.db_inner_frame, text="var2\nprec")
        self.var2_prec_listbox_label.grid(row=25, column=19, sticky=W)
        self.var2_divby_listbox_label = Label(self.db_inner_frame, text="var2\ndivby")
        self.var2_divby_listbox_label.grid(row=25, column=20, sticky=W)

        self.var3_name_listbox_label = Label(self.db_inner_frame, text="var3\nname")
        self.var3_name_listbox_label.grid(row=25, column=21, sticky=W)
        self.var3_min_listbox_label = Label(self.db_inner_frame, text="var3\nmin")
        self.var3_min_listbox_label.grid(row=25, column=22, sticky=W)
        self.var3_max_listbox_label = Label(self.db_inner_frame, text="var3\nmax")
        self.var3_max_listbox_label.grid(row=25, column=23, sticky=W)
        self.var3_prec_listbox_label = Label(self.db_inner_frame, text="var3\nprec")
        self.var3_prec_listbox_label.grid(row=25, column=24, sticky=W)
        self.var3_divby_listbox_label = Label(self.db_inner_frame, text="var3\ntol")
        self.var3_divby_listbox_label.grid(row=25, column=25, sticky=W)

        self.var4_name_listbox_label = Label(self.db_inner_frame, text="var4\nname")
        self.var4_name_listbox_label.grid(row=25, column=26, sticky=W)
        self.var4_min_listbox_label = Label(self.db_inner_frame, text="var4\nmin")
        self.var4_min_listbox_label.grid(row=25, column=27, sticky=W)
        self.var4_max_listbox_label = Label(self.db_inner_frame, text="var4\nmax")
        self.var4_max_listbox_label.grid(row=25, column=28, sticky=W)
        self.var4_prec_listbox_label = Label(self.db_inner_frame, text="var4\nprec")
        self.var4_prec_listbox_label.grid(row=25, column=29, sticky=W)
        self.var4_divby_listbox_label = Label(self.db_inner_frame, text="var4\ntol")
        self.var4_divby_listbox_label.grid(row=25, column=30, sticky=W)

        self.var5_name_listbox_label = Label(self.db_inner_frame, text="var5\nname")
        self.var5_name_listbox_label.grid(row=25, column=31, sticky=W)
        self.var5_min_listbox_label = Label(self.db_inner_frame, text="var5\nmin")
        self.var5_min_listbox_label.grid(row=25, column=32, sticky=W)
        self.var5_max_listbox_label = Label(self.db_inner_frame, text="var5\nmax")
        self.var5_max_listbox_label.grid(row=25, column=33, sticky=W)
        self.var5_prec_listbox_label = Label(self.db_inner_frame, text="var5\nprec")
        self.var5_prec_listbox_label.grid(row=25, column=34, sticky=W)
        self.var5_divby_listbox_label = Label(self.db_inner_frame, text="var5\ntol")
        self.var5_divby_listbox_label.grid(row=25, column=35, sticky=W)

        self.var6_name_listbox_label = Label(self.db_inner_frame, text="var6\nname")
        self.var6_name_listbox_label.grid(row=25, column=36, sticky=W)
        self.var6_min_listbox_label = Label(self.db_inner_frame, text="var6\nmin")
        self.var6_min_listbox_label.grid(row=25, column=37, sticky=W)
        self.var6_max_listbox_label = Label(self.db_inner_frame, text="var6\nmax")
        self.var6_max_listbox_label.grid(row=25, column=38, sticky=W)
        self.var6_prec_listbox_label = Label(self.db_inner_frame, text="var6\nprec")
        self.var6_prec_listbox_label.grid(row=25, column=39, sticky=W)
        self.var6_divby_listbox_label = Label(self.db_inner_frame, text="var6\ntol")
        self.var6_divby_listbox_label.grid(row=25, column=40, sticky=W)

        self.var7_name_listbox_label = Label(self.db_inner_frame, text="var1\nname")
        self.var7_name_listbox_label.grid(row=25, column=41, sticky=W)
        self.var7_min_listbox_label = Label(self.db_inner_frame, text="var7\nmin")
        self.var7_min_listbox_label.grid(row=25, column=42, sticky=W)
        self.var7_max_listbox_label = Label(self.db_inner_frame, text="var7\nmax")
        self.var7_max_listbox_label.grid(row=25, column=43, sticky=W)
        self.var7_prec_listbox_label = Label(self.db_inner_frame, text="var7\nprec")
        self.var7_prec_listbox_label.grid(row=25, column=44, sticky=W)
        self.var7_divby_listbox_label = Label(self.db_inner_frame, text="var7\ntol")
        self.var7_divby_listbox_label.grid(row=25, column=45, sticky=W)

        self.res1_name_listbox_label = Label(self.db_inner_frame, text="res1\nname")
        self.res1_name_listbox_label.grid(row=25, column=46, sticky=W)
        self.res1_min_listbox_label = Label(self.db_inner_frame, text="res1\nmin")
        self.res1_min_listbox_label.grid(row=25, column=47, sticky=W)
        self.res1_max_listbox_label = Label(self.db_inner_frame, text="res1\nmax")
        self.res1_max_listbox_label.grid(row=25, column=48, sticky=W)
        self.res1_prec_listbox_label = Label(self.db_inner_frame, text="res1\nprec")
        self.res1_prec_listbox_label.grid(row=25, column=49, sticky=W)
        self.res1_tol_listbox_label = Label(self.db_inner_frame, text="res1\ntol")
        self.res1_tol_listbox_label.grid(row=25, column=50, sticky=W)
        self.res1_points_listbox_label = Label(self.db_inner_frame, text="res1\npts")
        self.res1_points_listbox_label.grid(row=25, column=51, sticky=W)

        self.res2_name_listbox_label = Label(self.db_inner_frame, text="res2\nname")
        self.res2_name_listbox_label.grid(row=25, column=52, sticky=W)
        self.res2_min_listbox_label = Label(self.db_inner_frame, text="res2\nmin")
        self.res2_min_listbox_label.grid(row=25, column=53, sticky=W)
        self.res2_max_listbox_label = Label(self.db_inner_frame, text="res2\nmax")
        self.res2_max_listbox_label.grid(row=25, column=54, sticky=W)
        self.res2_prec_listbox_label = Label(self.db_inner_frame, text="res2\nprec")
        self.res2_prec_listbox_label.grid(row=25, column=55, sticky=W)
        self.res2_tol_listbox_label = Label(self.db_inner_frame, text="res2\ntol")
        self.res2_tol_listbox_label.grid(row=25, column=56, sticky=W)
        self.res2_points_listbox_label = Label(self.db_inner_frame, text="res2\npts")
        self.res2_points_listbox_label.grid(row=25, column=57, sticky=W)

        self.res3_name_listbox_label = Label(self.db_inner_frame, text="res3\nname")
        self.res3_name_listbox_label.grid(row=25, column=58, sticky=W)
        self.res3_min_listbox_label = Label(self.db_inner_frame, text="res3\nmin")
        self.res3_min_listbox_label.grid(row=25, column=59, sticky=W)
        self.res3_max_listbox_label = Label(self.db_inner_frame, text="res3\nmax")
        self.res3_max_listbox_label.grid(row=25, column=60, sticky=W)
        self.res3_prec_listbox_label = Label(self.db_inner_frame, text="res3\nprec")
        self.res3_prec_listbox_label.grid(row=25, column=61, sticky=W)
        self.res3_tol_listbox_label = Label(self.db_inner_frame, text="res3\ntol")
        self.res3_tol_listbox_label.grid(row=25, column=62, sticky=W)
        self.res3_points_listbox_label = Label(self.db_inner_frame, text="res3\npts")
        self.res3_points_listbox_label.grid(row=25, column=63, sticky=W)


        self.img_name_listbox_label = Label(self.db_inner_frame, text=" img\n name")
        self.img_name_listbox_label.grid(row=25, column=64, sticky=W)

        self.img_data_label = Label(self.db_inner_frame, text=" img\n data")
        #self.img_data_label.grid(row=25, column=55, sticky=W)


        self.test_time_listbox_label = Label(self.db_inner_frame, text="test\ntime", width=10)
        self.test_time_listbox_label.grid(row=25, column=65, sticky=W)


        # CREATE FULL-LISTBOX ENTRYS IN NEW WINDOW

        self.my_listbox_oid = Listbox(self.db_inner_frame, width=5)
        self.my_listbox_oid.grid(row=30, column=1, sticky=W)

        self.my_listbox_question_difficulty = Listbox(self.db_inner_frame, width=15)
        self.my_listbox_question_difficulty.grid(row=30, column=2, sticky=W)

        self.my_listbox_question_category = Listbox(self.db_inner_frame, width=15)
        self.my_listbox_question_category.grid(row=30, column=3, sticky=W)

        self.my_listbox_question_type = Listbox(self.db_inner_frame, width=15)
        self.my_listbox_question_type.grid(row=30, column=4, sticky=W)


        self.my_listbox_question_title = Listbox(self.db_inner_frame, width=15)
        self.my_listbox_question_title.grid(row=30, column=5, sticky=W, pady=20)
        self.my_listbox_question_description_title = Listbox(self.db_inner_frame, width=15)
        self.my_listbox_question_description_title.grid(row=30, column=6, sticky=W)
        self.my_listbox_question_description_main = Listbox(self.db_inner_frame, width=15)
        self.my_listbox_question_description_main.grid(row=30, column=7, sticky=W)


        self.my_listbox_res1_formula = Listbox(self.db_inner_frame, width=15)
        self.my_listbox_res1_formula.grid(row=30, column=8, sticky=W)
        self.my_listbox_res2_formula = Listbox(self.db_inner_frame, width=15)
        self.my_listbox_res2_formula.grid(row=30, column=9, sticky=W)
        self.my_listbox_res3_formula = Listbox(self.db_inner_frame, width=15)
        self.my_listbox_res3_formula.grid(row=30, column=10, sticky=W)

        self.my_listbox_var1_name = Listbox(self.db_inner_frame, width=5)
        self.my_listbox_var1_name.grid(row=30, column=11, sticky=W)
        self.my_listbox_var1_min = Listbox(self.db_inner_frame, width=5)
        self.my_listbox_var1_min.grid(row=30, column=12, sticky=W)
        self.my_listbox_var1_max = Listbox(self.db_inner_frame, width=5)
        self.my_listbox_var1_max.grid(row=30, column=13, sticky=W)
        self.my_listbox_var1_prec = Listbox(self.db_inner_frame, width=5)
        self.my_listbox_var1_prec.grid(row=30, column=14, sticky=W)
        self.my_listbox_var1_divby = Listbox(self.db_inner_frame, width=5)
        self.my_listbox_var1_divby.grid(row=30, column=15, sticky=W)

        self.my_listbox_var2_name = Listbox(self.db_inner_frame, width=5)
        self.my_listbox_var2_name.grid(row=30, column=16, sticky=W)
        self.my_listbox_var2_min = Listbox(self.db_inner_frame, width=5)
        self.my_listbox_var2_min.grid(row=30, column=17, sticky=W)
        self.my_listbox_var2_max = Listbox(self.db_inner_frame, width=5)
        self.my_listbox_var2_max.grid(row=30, column=18, sticky=W)
        self.my_listbox_var2_prec = Listbox(self.db_inner_frame, width=5)
        self.my_listbox_var2_prec.grid(row=30, column=19, sticky=W)
        self.my_listbox_var2_divby = Listbox(self.db_inner_frame, width=5)
        self.my_listbox_var2_divby.grid(row=30, column=20, sticky=W)

        self.my_listbox_var3_name = Listbox(self.db_inner_frame, width=5)
        self.my_listbox_var3_name.grid(row=30, column=21, sticky=W)
        self.my_listbox_var3_min = Listbox(self.db_inner_frame, width=5)
        self.my_listbox_var3_min.grid(row=30, column=22, sticky=W)
        self.my_listbox_var3_max = Listbox(self.db_inner_frame, width=5)
        self.my_listbox_var3_max.grid(row=30, column=23, sticky=W)
        self.my_listbox_var3_prec = Listbox(self.db_inner_frame, width=5)
        self.my_listbox_var3_prec.grid(row=30, column=24, sticky=W)
        self.my_listbox_var3_divby = Listbox(self.db_inner_frame, width=5)
        self.my_listbox_var3_divby.grid(row=30, column=25, sticky=W)

        self.my_listbox_var4_name = Listbox(self.db_inner_frame, width=5)
        self.my_listbox_var4_name.grid(row=30, column=26, sticky=W)
        self.my_listbox_var4_min = Listbox(self.db_inner_frame, width=5)
        self.my_listbox_var4_min.grid(row=30, column=27, sticky=W)
        self.my_listbox_var4_max = Listbox(self.db_inner_frame, width=5)
        self.my_listbox_var4_max.grid(row=30, column=28, sticky=W)
        self.my_listbox_var4_prec = Listbox(self.db_inner_frame, width=5)
        self.my_listbox_var4_prec.grid(row=30, column=29, sticky=W)
        self.my_listbox_var4_divby = Listbox(self.db_inner_frame, width=5)
        self.my_listbox_var4_divby.grid(row=30, column=30, sticky=W)

        self.my_listbox_var5_name = Listbox(self.db_inner_frame, width=5)
        self.my_listbox_var5_name.grid(row=30, column=31, sticky=W)
        self.my_listbox_var5_min = Listbox(self.db_inner_frame, width=5)
        self.my_listbox_var5_min.grid(row=30, column=32, sticky=W)
        self.my_listbox_var5_max = Listbox(self.db_inner_frame, width=5)
        self.my_listbox_var5_max.grid(row=30, column=33, sticky=W)
        self.my_listbox_var5_prec = Listbox(self.db_inner_frame, width=5)
        self.my_listbox_var5_prec.grid(row=30, column=34, sticky=W)
        self.my_listbox_var5_divby = Listbox(self.db_inner_frame, width=5)
        self.my_listbox_var5_divby.grid(row=30, column=35, sticky=W)

        self.my_listbox_var6_name = Listbox(self.db_inner_frame, width=5)
        self.my_listbox_var6_name.grid(row=30, column=36, sticky=W)
        self.my_listbox_var6_min = Listbox(self.db_inner_frame, width=5)
        self.my_listbox_var6_min.grid(row=30, column=37, sticky=W)
        self.my_listbox_var6_max = Listbox(self.db_inner_frame, width=5)
        self.my_listbox_var6_max.grid(row=30, column=38, sticky=W)
        self.my_listbox_var6_prec = Listbox(self.db_inner_frame, width=5)
        self.my_listbox_var6_prec.grid(row=30, column=39, sticky=W)
        self.my_listbox_var6_divby = Listbox(self.db_inner_frame, width=5)
        self.my_listbox_var6_divby.grid(row=30, column=40, sticky=W)

        self.my_listbox_var7_name = Listbox(self.db_inner_frame, width=5)
        self.my_listbox_var7_name.grid(row=30, column=41, sticky=W)
        self.my_listbox_var7_min = Listbox(self.db_inner_frame, width=5)
        self.my_listbox_var7_min.grid(row=30, column=42, sticky=W)
        self.my_listbox_var7_max = Listbox(self.db_inner_frame, width=5)
        self.my_listbox_var7_max.grid(row=30, column=43, sticky=W)
        self.my_listbox_var7_prec = Listbox(self.db_inner_frame, width=5)
        self.my_listbox_var7_prec.grid(row=30, column=44, sticky=W)
        self.my_listbox_var7_divby = Listbox(self.db_inner_frame, width=5)
        self.my_listbox_var7_divby.grid(row=30, column=45, sticky=W)

        self.my_listbox_res1_name = Listbox(self.db_inner_frame, width=5)
        self.my_listbox_res1_name.grid(row=30, column=46, sticky=W)
        self.my_listbox_res1_min = Listbox(self.db_inner_frame, width=5)
        self.my_listbox_res1_min.grid(row=30, column=47, sticky=W)
        self.my_listbox_res1_max = Listbox(self.db_inner_frame, width=5)
        self.my_listbox_res1_max.grid(row=30, column=48, sticky=W)
        self.my_listbox_res1_prec = Listbox(self.db_inner_frame, width=5)
        self.my_listbox_res1_prec.grid(row=30, column=49, sticky=W)
        self.my_listbox_res1_tol = Listbox(self.db_inner_frame, width=5)
        self.my_listbox_res1_tol.grid(row=30, column=50, sticky=W)
        self.my_listbox_res1_points = Listbox(self.db_inner_frame, width=5)
        self.my_listbox_res1_points.grid(row=30, column=51, sticky=W)

        self.my_listbox_res2_name = Listbox(self.db_inner_frame, width=5)
        self.my_listbox_res2_name.grid(row=30, column=52, sticky=W)
        self.my_listbox_res2_min = Listbox(self.db_inner_frame, width=5)
        self.my_listbox_res2_min.grid(row=30, column=53, sticky=W)
        self.my_listbox_res2_max = Listbox(self.db_inner_frame, width=5)
        self.my_listbox_res2_max.grid(row=30, column=54, sticky=W)
        self.my_listbox_res2_prec = Listbox(self.db_inner_frame, width=5)
        self.my_listbox_res2_prec.grid(row=30, column=55, sticky=W)
        self.my_listbox_res2_tol = Listbox(self.db_inner_frame, width=5)
        self.my_listbox_res2_tol.grid(row=30, column=56, sticky=W)
        self.my_listbox_res2_points = Listbox(self.db_inner_frame, width=5)
        self.my_listbox_res2_points.grid(row=30, column=57, sticky=W)

        self.my_listbox_res3_name = Listbox(self.db_inner_frame, width=5)
        self.my_listbox_res3_name.grid(row=30, column=58, sticky=W)
        self.my_listbox_res3_min = Listbox(self.db_inner_frame, width=5)
        self.my_listbox_res3_min.grid(row=30, column=59, sticky=W)
        self.my_listbox_res3_max = Listbox(self.db_inner_frame, width=5)
        self.my_listbox_res3_max.grid(row=30, column=60, sticky=W)
        self.my_listbox_res3_prec = Listbox(self.db_inner_frame, width=5)
        self.my_listbox_res3_prec.grid(row=30, column=61, sticky=W)
        self.my_listbox_res3_tol = Listbox(self.db_inner_frame, width=5)
        self.my_listbox_res3_tol.grid(row=30, column=62, sticky=W)
        self.my_listbox_res3_points = Listbox(self.db_inner_frame, width=5)
        self.my_listbox_res3_points.grid(row=30, column=63, sticky=W)




        self.my_listbox_img_name = Listbox(self.db_inner_frame, width=5)
        self.my_listbox_img_name.grid(row=30, column=64, sticky=W)

        self.my_listbox_img_data = Listbox(self.db_inner_frame, width=10)
        #self.my_listbox_img_data.grid(row=30, column=50, sticky=W)          #IMG_data need to get a database_entry, but would not "grid()" the entry to GUI. Otherwise it is real slow


        self.my_listbox_test_time = Listbox(self.db_inner_frame, width=20)
        self.my_listbox_test_time.grid(row=30, column=65, sticky=W)

        # CREATE LISTBOX SCROLLBARS

        def yview (*args):

            self.my_listbox_question_difficulty.yview(*args)
            self.my_listbox_question_category.yview(*args)
            self.my_listbox_question_type.yview(*args)
            self.my_listbox_question_title.yview(*args)
            self.my_listbox_question_description_title.yview(*args)
            self.my_listbox_question_description_main.yview(*args)

            self.my_listbox_res1_formula.yview(*args)
            self.my_listbox_res2_formula.yview(*args)
            self.my_listbox_res3_formula.yview(*args)

            self.my_listbox_var1_name.yview(*args)
            self.my_listbox_var1_min.yview(*args)
            self.my_listbox_var1_max.yview(*args)
            self.my_listbox_var1_prec.yview(*args)
            self.my_listbox_var1_divby.yview(*args)

            self.my_listbox_var2_name.yview(*args)
            self.my_listbox_var2_min.yview(*args)
            self.my_listbox_var2_max.yview(*args)
            self.my_listbox_var2_prec.yview(*args)
            self.my_listbox_var2_divby.yview(*args)

            self.my_listbox_var3_name.yview(*args)
            self.my_listbox_var3_min.yview(*args)
            self.my_listbox_var3_max.yview(*args)
            self.my_listbox_var3_prec.yview(*args)
            self.my_listbox_var3_divby.yview(*args)

            self.my_listbox_var4_name.yview(*args)
            self.my_listbox_var4_min.yview(*args)
            self.my_listbox_var4_max.yview(*args)
            self.my_listbox_var4_prec.yview(*args)
            self.my_listbox_var4_divby.yview(*args)

            self.my_listbox_var5_name.yview(*args)
            self.my_listbox_var5_min.yview(*args)
            self.my_listbox_var5_max.yview(*args)
            self.my_listbox_var5_prec.yview(*args)
            self.my_listbox_var5_divby.yview(*args)

            self.my_listbox_var6_name.yview(*args)
            self.my_listbox_var6_min.yview(*args)
            self.my_listbox_var6_max.yview(*args)
            self.my_listbox_var6_prec.yview(*args)
            self.my_listbox_var6_divby.yview(*args)

            self.my_listbox_var7_name.yview(*args)
            self.my_listbox_var7_min.yview(*args)
            self.my_listbox_var7_max.yview(*args)
            self.my_listbox_var7_prec.yview(*args)
            self.my_listbox_var7_divby.yview(*args)

            self.my_listbox_res1_name.yview(*args)
            self.my_listbox_res1_min.yview(*args)
            self.my_listbox_res1_max.yview(*args)
            self.my_listbox_res1_prec.yview(*args)
            self.my_listbox_res1_tol.yview(*args)
            self.my_listbox_res1_points.yview(*args)

            self.my_listbox_res2_name.yview(*args)
            self.my_listbox_res2_min.yview(*args)
            self.my_listbox_res2_max.yview(*args)
            self.my_listbox_res2_prec.yview(*args)
            self.my_listbox_res2_tol.yview(*args)
            self.my_listbox_res2_points.yview(*args)

            self.my_listbox_res3_name.yview(*args)
            self.my_listbox_res3_min.yview(*args)
            self.my_listbox_res3_max.yview(*args)
            self.my_listbox_res3_prec.yview(*args)
            self.my_listbox_res3_tol.yview(*args)
            self.my_listbox_res3_points.yview(*args)

            self.my_listbox_img_name.yview(*args)
            #self.my_listbox_img_data.yview(*args)
            self.my_listbox_test_time.yview(*args)

            self.my_listbox_oid.yview(*args)

        self.listbox_entry_scrollbar_y = Scrollbar(self.db_inner_frame, command=yview)
        self.listbox_entry_scrollbar_y.grid(row=1, column=0)

        self.my_listbox_question_difficulty.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_question_category.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_question_type.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_question_title.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_question_description_title.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_question_description_main.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)

        self.my_listbox_res1_formula.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_res2_formula.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_res3_formula.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)

        self.my_listbox_var1_name.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var1_min.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var1_max.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var1_prec.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var1_divby.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)

        self.my_listbox_var2_name.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var2_min.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var2_max.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var2_prec.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var2_divby.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)

        self.my_listbox_var3_name.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var3_min.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var3_max.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var3_prec.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var3_divby.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)

        self.my_listbox_var4_name.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var4_min.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var4_max.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var4_prec.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var4_divby.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)

        self.my_listbox_var5_name.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var5_min.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var5_max.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var5_prec.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var5_divby.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)

        self.my_listbox_var6_name.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var6_min.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var6_max.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var6_prec.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var6_divby.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)

        self.my_listbox_var7_name.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var7_min.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var7_max.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var7_prec.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var7_divby.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)

        self.my_listbox_res1_name.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_res1_min.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_res1_max.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_res1_prec.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_res1_tol.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_res1_points.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)

        self.my_listbox_res2_name.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_res2_min.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_res2_max.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_res2_prec.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_res2_tol.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_res2_points.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)

        self.my_listbox_res3_name.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_res3_min.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_res3_max.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_res3_prec.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_res3_tol.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_res3_points.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_img_name.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        #self.my_listbox_img_data.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_test_time.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_oid.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)

    def remove_database(self):
        self.frame_database.grid_forget()


    def submit(self):
        conn = sqlite3.connect('ilias_questions_db.db')
        c =conn.cursor()



        # format of duration P0Y0M0DT0H30M0S
        self.test_time = "P0Y0M0DT" + self.proc_hours_box.get() + "H" + self.proc_minutes_box.get() + "M" + self.proc_seconds_box.get() + "S"

        #Dieser String muss modifiziert werden. In der xml ist ein Zeilenumbrauch als "&lt;/p&gt;&#13;&#10;&lt;p&gt;" definiert und nur 1 Zeile!

        print(self.picture_name)

        if self.picture_name != "EMPTY":
            with open(self.picture_name, 'rb') as f:
                self.picture_data = f.read()


        else:
            self.picture_name_new = "EMPTY"
            self.picture_data = "EMPTY"


        # Insert into Table
        c.execute(
            "INSERT INTO my_table VALUES ("
            ":question_difficulty, :question_category, :question_type, "
            ":question_title, :question_title_description, :question_description_main, "
            ":res1_formula, :res2_formula, :res3_formula,  "
            ":var1_name, :var1_min, :var1_max, :var1_prec, :var1_divby, "
            ":var2_name, :var2_min, :var2_max, :var2_prec, :var2_divby, "
            ":var3_name, :var3_min, :var3_max, :var3_prec, :var3_divby, "
            ":var4_name, :var4_min, :var4_max, :var4_prec, :var4_divby, "
            ":var5_name, :var5_min, :var5_max, :var5_prec, :var5_divby, "
            ":var6_name, :var6_min, :var6_max, :var6_prec, :var6_divby, "
            ":var7_name, :var7_min, :var7_max, :var7_prec, :var7_divby,"
            ":res1_name, :res1_min, :res1_max, :res1_prec, :res1_tol, :res1_points, "
            ":res2_name, :res2_min, :res2_max, :res2_prec, :res2_tol, :res2_points, "
            ":res3_name, :res3_min, :res3_max, :res3_prec, :res3_tol, :res3_points,"
            ":img_name, :img_data, :test_time)",
            {
                'question_difficulty': self.question_difficulty_entry.get(),
                'question_category': self.question_category_entry.get(),
                'question_type': self.question_type_entry.get(),

                'question_title': self.question_title_entry.get(),
                'question_title_description': self.question_description_entry.get(),

                # The first part, "1.0" means that the input should be read from line one, character zero (ie: the very first character).
                # END is an imported constant which is set to the string "end". The END part means to read until the end of the text box is reached.
                # The only issue with this is that it actually adds a newline to our input. "
                # "So, in order to fix it we should change END to end-1c(Thanks Bryan Oakley) The -1c deletes 1 character, while -2c would mean delete two characters, and so on."
                'question_description_main': self.formula_question_entry.get("1.0", 'end-1c'),

                'res1_formula': self.res1_formula_text.get(),
                'res2_formula': self.res2_formula_text.get(),
                'res3_formula': self.res3_formula_text.get(),

                'var1_name': self.var1_name_text.get(),
                'var1_min': self.var1_min_text.get(),
                'var1_max': self.var1_max_text.get(),
                'var1_prec': self.var1_prec_text.get(),
                'var1_divby': self.var1_divby_text.get(),

                'var2_name': self.var2_name_text.get(),
                'var2_min': self.var2_min_text.get(),
                'var2_max': self.var2_max_text.get(),
                'var2_prec': self.var2_prec_text.get(),
                'var2_divby': self.var2_divby_text.get(),

                'var3_name': self.var3_name_text.get(),
                'var3_min': self.var3_min_text.get(),
                'var3_max': self.var3_max_text.get(),
                'var3_prec': self.var3_prec_text.get(),
                'var3_divby': self.var3_divby_text.get(),

                'var4_name': self.var4_name_text.get(),
                'var4_min': self.var4_min_text.get(),
                'var4_max': self.var4_max_text.get(),
                'var4_prec': self.var4_prec_text.get(),
                'var4_divby': self.var4_divby_text.get(),

                'var5_name': self.var5_name_text.get(),
                'var5_min': self.var5_min_text.get(),
                'var5_max': self.var5_max_text.get(),
                'var5_prec': self.var5_prec_text.get(),
                'var5_divby': self.var5_divby_text.get(),

                'var6_name': self.var6_name_text.get(),
                'var6_min': self.var6_min_text.get(),
                'var6_max': self.var6_max_text.get(),
                'var6_prec': self.var6_prec_text.get(),
                'var6_divby': self.var6_divby_text.get(),

                'var7_name': self.var7_name_text.get(),
                'var7_min': self.var7_min_text.get(),
                'var7_max': self.var7_max_text.get(),
                'var7_prec': self.var7_prec_text.get(),
                'var7_divby': self.var7_divby_text.get(),

                'res1_name': self.res1_name_text.get(),
                'res1_min': self.res1_min_text.get(),
                'res1_max': self.res1_max_text.get(),
                'res1_prec': self.res1_prec_text.get(),
                'res1_tol': self.res1_tol_text.get(),
                'res1_points': self.res1_points_text.get(),

                'res2_name': self.res2_name_text.get(),
                'res2_min': self.res2_min_text.get(),
                'res2_max': self.res2_max_text.get(),
                'res2_prec': self.res2_prec_text.get(),
                'res2_tol': self.res2_tol_text.get(),
                'res2_points': self.res2_points_text.get(),

                'res3_name': self.res3_name_text.get(),
                'res3_min': self.res3_min_text.get(),
                'res3_max': self.res3_max_text.get(),
                'res3_prec': self.res3_prec_text.get(),
                'res3_tol': self.res3_tol_text.get(),
                'res3_points': self.res3_points_text.get(),

                'img_name': self.picture_name_new,
                'img_data': self.picture_data,

                'test_time': self.test_time
            }
        )
        conn.commit()
        conn.close()



    def show_records(self):
        conn = sqlite3.connect('ilias_questions_db.db')
        c = conn.cursor()

        c.execute("SELECT *, oid FROM my_table")
        records = c.fetchall()

        # Clear List Boxes

        self.my_listbox_question_difficulty.delete(0, END)
        self.my_listbox_question_category.delete(0, END)
        self.my_listbox_question_type.delete(0, END)

        self.my_listbox_question_title.delete(0, END)
        self.my_listbox_question_description_title.delete(0, END)
        self.my_listbox_question_description_main.delete(0, END)

        self.my_listbox_res1_formula.delete(0, END)
        self.my_listbox_res2_formula.delete(0, END)
        self.my_listbox_res3_formula.delete(0, END)

        self.my_listbox_var1_name.delete(0, END)
        self.my_listbox_var1_min.delete(0, END)
        self.my_listbox_var1_max.delete(0, END)
        self.my_listbox_var1_prec.delete(0, END)
        self.my_listbox_var1_divby.delete(0, END)

        self.my_listbox_var2_name.delete(0, END)
        self.my_listbox_var2_min.delete(0, END)
        self.my_listbox_var2_max.delete(0, END)
        self.my_listbox_var2_prec.delete(0, END)
        self.my_listbox_var2_divby.delete(0, END)

        self.my_listbox_var3_name.delete(0, END)
        self.my_listbox_var3_min.delete(0, END)
        self.my_listbox_var3_max.delete(0, END)
        self.my_listbox_var3_prec.delete(0, END)
        self.my_listbox_var3_divby.delete(0, END)

        self.my_listbox_var4_name.delete(0, END)
        self.my_listbox_var4_min.delete(0, END)
        self.my_listbox_var4_max.delete(0, END)
        self.my_listbox_var4_prec.delete(0, END)
        self.my_listbox_var4_divby.delete(0, END)

        self.my_listbox_var5_name.delete(0, END)
        self.my_listbox_var5_min.delete(0, END)
        self.my_listbox_var5_max.delete(0, END)
        self.my_listbox_var5_prec.delete(0, END)
        self.my_listbox_var5_divby.delete(0, END)

        self.my_listbox_var6_name.delete(0, END)
        self.my_listbox_var6_min.delete(0, END)
        self.my_listbox_var6_max.delete(0, END)
        self.my_listbox_var6_prec.delete(0, END)
        self.my_listbox_var6_divby.delete(0, END)

        self.my_listbox_var7_name.delete(0, END)
        self.my_listbox_var7_min.delete(0, END)
        self.my_listbox_var7_max.delete(0, END)
        self.my_listbox_var7_prec.delete(0, END)
        self.my_listbox_var7_divby.delete(0, END)

        self.my_listbox_res1_name.delete(0, END)
        self.my_listbox_res1_min.delete(0, END)
        self.my_listbox_res1_max.delete(0, END)
        self.my_listbox_res1_prec.delete(0, END)
        self.my_listbox_res1_tol.delete(0, END)
        self.my_listbox_res1_points.delete(0, END)

        self.my_listbox_res2_name.delete(0, END)
        self.my_listbox_res2_min.delete(0, END)
        self.my_listbox_res2_max.delete(0, END)
        self.my_listbox_res2_prec.delete(0, END)
        self.my_listbox_res2_tol.delete(0, END)
        self.my_listbox_res2_points.delete(0, END)

        self.my_listbox_res3_name.delete(0, END)
        self.my_listbox_res3_min.delete(0, END)
        self.my_listbox_res3_max.delete(0, END)
        self.my_listbox_res3_prec.delete(0, END)
        self.my_listbox_res3_tol.delete(0, END)
        self.my_listbox_res3_points.delete(0, END)

        self.my_listbox_img_name.delete(0, END)
        self.my_listbox_img_data.delete(0, END)

        self.my_listbox_test_time.delete(0, END)
        self.my_listbox_oid.delete(0, END)

        # Loop thru Results
        for record in records:


            self.my_listbox_question_difficulty.insert(END, record[0])
            self.my_listbox_question_category.insert(END, record[1])
            self.my_listbox_question_type.insert(END, record[2])

            self.my_listbox_question_title.insert(END, record[3])
            self.my_listbox_question_description_title.insert(END, record[4])
            self.my_listbox_question_description_main.insert(END, record[5])

            self.my_listbox_res1_formula.insert(END, record[6])
            self.my_listbox_res2_formula.insert(END, record[7])
            self.my_listbox_res3_formula.insert(END, record[8])

            self.my_listbox_var1_name.insert(END, record[9])
            self.my_listbox_var1_min.insert(END, record[10])
            self.my_listbox_var1_max.insert(END, record[11])
            self.my_listbox_var1_prec.insert(END, record[12])
            self.my_listbox_var1_divby.insert(END, record[13])

            self.my_listbox_var2_name.insert(END, record[14])
            self.my_listbox_var2_min.insert(END, record[15])
            self.my_listbox_var2_max.insert(END, record[16])
            self.my_listbox_var2_prec.insert(END, record[17])
            self.my_listbox_var2_divby.insert(END, record[18])

            self.my_listbox_var3_name.insert(END, record[19])
            self.my_listbox_var3_min.insert(END, record[20])
            self.my_listbox_var3_max.insert(END, record[21])
            self.my_listbox_var3_prec.insert(END, record[22])
            self.my_listbox_var3_divby.insert(END, record[23])

            self.my_listbox_var4_name.insert(END, record[24])
            self.my_listbox_var4_min.insert(END, record[25])
            self.my_listbox_var4_max.insert(END, record[26])
            self.my_listbox_var4_prec.insert(END, record[27])
            self.my_listbox_var4_divby.insert(END, record[28])

            self.my_listbox_var5_name.insert(END, record[29])
            self.my_listbox_var5_min.insert(END, record[30])
            self.my_listbox_var5_max.insert(END, record[31])
            self.my_listbox_var5_prec.insert(END, record[32])
            self.my_listbox_var5_divby.insert(END, record[33])

            self.my_listbox_var6_name.insert(END, record[34])
            self.my_listbox_var6_min.insert(END, record[35])
            self.my_listbox_var6_max.insert(END, record[36])
            self.my_listbox_var6_prec.insert(END, record[37])
            self.my_listbox_var6_divby.insert(END, record[38])

            self.my_listbox_var7_name.insert(END, record[39])
            self.my_listbox_var7_min.insert(END, record[40])
            self.my_listbox_var7_max.insert(END, record[41])
            self.my_listbox_var7_prec.insert(END, record[42])
            self.my_listbox_var7_divby.insert(END, record[43])

            self.my_listbox_res1_name.insert(END, record[44])
            self.my_listbox_res1_min.insert(END, record[45])
            self.my_listbox_res1_max.insert(END, record[46])
            self.my_listbox_res1_prec.insert(END, record[47])
            self.my_listbox_res1_tol.insert(END, record[48])
            self.my_listbox_res1_points.insert(END, record[49])

            self.my_listbox_res2_name.insert(END, record[50])
            self.my_listbox_res2_min.insert(END, record[51])
            self.my_listbox_res2_max.insert(END, record[52])
            self.my_listbox_res2_prec.insert(END, record[53])
            self.my_listbox_res2_tol.insert(END, record[54])
            self.my_listbox_res2_points.insert(END, record[55])

            self.my_listbox_res3_name.insert(END, record[56])
            self.my_listbox_res3_min.insert(END, record[57])
            self.my_listbox_res3_max.insert(END, record[58])
            self.my_listbox_res3_prec.insert(END, record[59])
            self.my_listbox_res3_tol.insert(END, record[60])
            self.my_listbox_res3_points.insert(END, record[61])

            self.my_listbox_img_name.insert(END, record[62])
            self.my_listbox_img_data.insert(END, record[63])

            self.my_listbox_test_time.insert(END, record[64]),
            self.my_listbox_oid.insert(END, record[65])

        conn.commit()
        conn.close()


    def delete(self):

        conn = sqlite3.connect('ilias_questions_db.db')
        c = conn.cursor()

        c.execute("DELETE from my_table WHERE oid= " + self.delete_box.get())

        self.delete_box.delete(0, END)

        conn.commit()
        conn.close()

        Database.show_records(self)

    def open_image(self):
        #global file_image  # needs to be global to print Image to Desktop
        #global filename_label
        #global file_image_label


        try:
            app.filename = filedialog.askopenfilename(initialdir="/", title="Select a File")
            self.picture_name = app.filename
            print(self.picture_name)
            self.sorted_picture_name = self.picture_name
            self.last_char_index = self.sorted_picture_name.rfind("/")
            self.foo = ([pos for pos, char in enumerate(self.sorted_picture_name) if char == '/'])
            self.foo_len = len(self.foo)
            self.picture_name_new = self.sorted_picture_name[self.foo[self.foo_len - 1] + 1:-4]   #letzten char des bildnamens ist das dateiformat: Testbild.jpg
            self.image_format_new = self.picture_name[-4:]
            print(self.image_format_new)
            print(self.picture_name_new)

            self.filename_label = Label(self.frame_picture, text=self.picture_name_new)
            self.filename_label.grid(row=0, column=0, sticky=W)


            self.file_image = ImageTk.PhotoImage(Image.open(app.filename).resize((250, 250)))
            self.file_image_label = Label(self.frame_picture, image=self.file_image)
            self.file_image_label.image = self.file_image
            self.file_image_label.grid(row=1, column=0)
        except:
            print("Error2")


    def delete_image(self):
        self.filename_label.grid_remove()
        self.file_image_label.grid_remove()
        self.picture_name ="EMPTY"



    def save_image_to_db(self):
        conn = sqlite3.connect('ilias_questions_db.db')
        c = conn.cursor()

        self.img_name = self.app_filename
        print("img1" + self.img_name)


        self.s = self.img_name

        self.last_char_index = self.s.rfind("/")

        print(self.s)
        self.foo = ([pos for pos, char in enumerate(self.s) if char == '/'])
        print(self.foo)
        print(len(self.s))

        self.foo_len = len(self.foo)

        print("NEW TRY")
        self.img_name_new = self.s[self.foo[self.foo_len-1]+1:]

        with open(self.img_name, 'rb') as f:
            self.img_data = f.read()



        c.execute("""
            INSERT INTO my_table (img_name, img_data) VALUES (?,?)""", (self.img_name_new, self.img_data))

        conn.commit()
        conn.close()


    def show_img_from_db(self):
        conn = sqlite3.connect('ilias_questions_db.db')
        c = conn.cursor()

        records = c.execute("""
            SELECT *, oid FROM my_table
        """)


        for record in records:

            if str(record[len(record) - 1]) == self.create_formelfrage_entry.get():

                print(record[63])

                self.rec_data = record[63]  #record[63] -> img_data_raw (as byte)

                #Picture need to have the name"il_0_mob_xxxxxxx" for ilias to work
                with open('il_0_mob_TEST.png', 'wb') as f:
                    f.write(self.rec_data)
                    print("IN IT 2")

                self.picture_name = "il_0_mob_TEST.png"
                self.db_file_image = ImageTk.PhotoImage(Image.open(self.picture_name).resize((250, 250)))
                self.db_file_image_label = Label(self.frame_db_picture, image=self.db_file_image)
                self.db_file_image_label.image = self.db_file_image
                self.db_file_image_label.grid(row=2, column=0)




        conn.commit()
        conn.close()


class LatexPreview(Formelfrage):

    def __init__(self):
        self.latex_preview_window = Toplevel()



        self.latex = r"{\text{Zu berechnen ist: AAAAAA  }}\ {sin(x^2)}\ {\text{Textblock 2}}\ {formel2}"
        self.expr = r'$$' + self.latex + '$$'
        preview(self.expr, viewer='file', filename='LaTeX-Preview.png')

        self.file_image = ImageTk.PhotoImage(Image.open('LaTeX-Preview.png'))
        self.file_image_label = Label(self.latex_preview_window, image=self.file_image)
        self.file_image_label.image = self.file_image

        self.file_image_label.grid(row=20, column=1)







class create_formelfrage(Formelfrage):

    def __init__(self):
        #C:\Users\tpantele\Neues Projekt\1590475954__0__tst_1944463
        self.mytree = ET.parse(self.project_root + "1590475954__0__tst_1944463\\" + '1590475954__0__tst_1944463.xml')
        self.myroot = self.mytree.getroot()

        print("-------------------------------------------------")
        for title in self.myroot.iter('Title'):
            print(title.text)
            title.text = self.test_title_entry.get()
            print(title.text)
        print("-------------------------------------------------")

        self.mytree.write(self.project_root + "1590475954__0__tst_1944463\\" + '1590475954__0__tst_1944463.xml')



        # ----------------------------------- Datei .xml Einlesen
       #self.mytree = ET.parse("xml_form_orig\\" + '1590230409__0__qti_1948621.xml')
        self.mytree = ET.parse(self.project_root + "1590475954__0__tst_1944463\\" +'orig_1590475954__0__qti_1944463.xml')
        self.myroot = self.mytree.getroot()

        self.frame_create = LabelFrame(self.formula_tab, text="Create Formelfrage", padx=5, pady=5)
        self.frame_create.grid(row=1, column=2)

        self.entry_split = self.create_formelfrage_entry.get()
        self.entry_split = self.entry_split.split(",")

        print(self.entry_split[0])
        print(len(self.entry_split))

        conn = sqlite3.connect('ilias_questions_db.db')
        c = conn.cursor()
        c.execute("SELECT *, oid FROM my_table")

        records = c.fetchall()


        for x in range(len(self.entry_split)):
            for record in records:
                if str(record[len(record) - 1]) == self.entry_split[x]:



                    self.question_difficulty = str(record[0])
                    self.question_category = str(record[1])
                    self.question_type = str(record[2])

                    self.question_title = str(record[3])
                    self.question_description_title = str(record[4])
                    self.question_description_main_raw = str(record[5])
                    self.formula_question_entry_multi_replaced = self.question_description_main_raw.replace('\n', "&lt;/p&gt;&#13;&#10;&lt;p&gt;")
                    self.question_description_main = self.formula_question_entry_multi_replaced

                    self.res1_formula = str(record[6])
                    self.res1_formula_length = str(len(self.res1_formula))
                    self.res2_formula = str(record[7])
                    self.res2_formula_length = str(len(self.res2_formula))
                    self.res3_formula = str(record[8])
                    self.res3_formula_length = str(len(self.res3_formula))

                    self.var1_name = str(record[9])
                    self.var1_min = str(record[10])
                    self.var1_max = str(record[11])
                    self.var1_prec = str(record[12])
                    self.var1_divby = str(record[13])
                    self.var1_divby_length = str(len(self.var1_divby))

                    self.var2_name = str(record[14])
                    self.var2_min = str(record[15])
                    self.var2_max = str(record[16])
                    self.var2_prec = str(record[17])
                    self.var2_divby = str(record[18])
                    self.var2_divby_length = str(len(self.var2_divby))

                    self.var3_name = str(record[19])
                    self.var3_min = str(record[20])
                    self.var3_max = str(record[21])
                    self.var3_prec = str(record[22])
                    self.var3_divby = str(record[23])
                    self.var3_divby_length = str(len(self.var3_divby))

                    self.var4_name = str(record[24])
                    self.var4_min = str(record[25])
                    self.var4_max = str(record[26])
                    self.var4_prec = str(record[27])
                    self.var4_divby = str(record[28])
                    self.var4_divby_length = str(len(self.var4_divby))

                    self.var5_name = str(record[29])
                    self.var5_min = str(record[30])
                    self.var5_max = str(record[31])
                    self.var5_prec = str(record[32])
                    self.var5_divby = str(record[33])
                    self.var5_divby_length = str(len(self.var5_divby))

                    self.var6_name = str(record[34])
                    self.var6_min = str(record[35])
                    self.var6_max = str(record[36])
                    self.var6_prec = str(record[37])
                    self.var6_divby = str(record[38])
                    self.var6_divby_length = str(len(self.var6_divby))

                    self.var7_name = str(record[39])
                    self.var7_min = str(record[40])
                    self.var7_max = str(record[41])
                    self.var7_prec = str(record[42])
                    self.var7_divby = str(record[43])
                    self.var7_divby_length = str(len(self.var7_divby))

                    self.res1_name = str(record[44])
                    self.res1_min = str(record[45])
                    self.res1_min_length = str(len(self.res1_min))
                    self.res1_max = str(record[46])
                    self.res1_max_length = str(len(self.res1_max))
                    self.res1_prec = str(record[47])
                    self.res1_tol = str(record[48])
                    self.res1_tol_length = str(len(self.res1_tol))
                    self.res1_points = str(record[49])


                    self.res2_name = str(record[50])
                    self.res2_min = str(record[51])
                    self.res2_min_length = str(len(self.res2_min))
                    self.res2_max = str(record[52])
                    self.res2_max_length = str(len(self.res2_max))
                    self.res2_prec = str(record[53])
                    self.res2_tol = str(record[54])
                    self.res2_tol_length = str(len(self.res2_tol))
                    self.res2_points = str(record[55])


                    self.res3_name = str(record[56])
                    self.res3_min = str(record[57])
                    self.res3_min_length = str(len(self.res3_min))
                    self.res3_max = str(record[58])
                    self.res3_max_length = str(len(self.res3_max))
                    self.res3_prec = str(record[59])
                    self.res3_tol = str(record[60])
                    self.res3_tol_length = str(len(self.res3_tol))
                    self.res3_points = str(record[61])

                    self.img_name = str(record[62])
                    self.img_data_raw = record[63]
                    self.img_data = str(record[63])

                    self.test_time = str(record[64])

                    self.oid = str(record[65]) #oid ist IMMER letztes Fach


            create_formelfrage.create_question(self,x)

        conn.commit()
        conn.close()


    def create_question(self, x):

        conn = sqlite3.connect('ilias_questions_db.db')
        c = conn.cursor()
        c.execute("SELECT *, oid FROM my_table")

        records = c.fetchall()

        def createFolder(directory):
            try:
                if not os.path.exists(directory):
                    os.makedirs(directory)
            except OSError:
                print('Error: Creating directory. ' + directory)

        #createFolder('.C:/Users/tpantele/Neues Projekt/1590475954__0__tst_1944463/objects/il_0_mob_000000' + str(x) + '/')
        #createFolder('1590475954__0__tst_1944463')

        for record in records:
            print(len(record))
            #print(record)
            #Ohne If Abfrage werden ALLE Fragen aus der Datenbank erstellt
            if str(record[len(record)-1]) == self.entry_split[x]:

                if self.img_data_raw != "EMPTY":
                    #img wird immer als PNG Datei abgelegt.
                    with open(self.project_root + "1590475954__0__tst_1944463\\objects\\" + "il_0_mob_000000" + str(x) + "\\" + self.img_name + ".png", 'wb') as f:
                        f.write(self.img_data_raw)


                    self.image = Image.open(self.project_root + "1590475954__0__tst_1944463\\objects\\" + "il_0_mob_000000" + str(x) + "\\" + self.img_name + ".png")
                    self.image.save(self.project_root + "1590475954__0__tst_1944463\\objects\\" + "il_0_mob_000000" + str(x) + "\\" + self.img_name + ".png")





                # print("q_titel: " + str(self.question_title))

                # cast int from len() function to string! cant use int in concatenated string
                # the string is used down below in "SOLUTION STRING"

                r1_rating = "0"
                r1_rating_length = len(r1_rating)
                # print(r1_rating_length)

                r1_unit = ""
                r1_unit_length = len(r1_unit)
                # print(r1_unit_length)

                r1_unitvalue = ""
                r1_unitv_length = len(r1_unitvalue)
                # print(r1_unitv_length)

                r1_resultunits = ""
                r1_resultu_length = len(r1_resultunits)
                # print(r1_resultu_length)

                question_name = str(self.question_title)

                questestinterop = ET.Element('questestinterop')
                assessment = ET.SubElement(questestinterop, 'assessment')
                section = ET.SubElement(assessment, 'section')
                item = ET.SubElement(section, 'item')
                item.set('ident', "il_0_qst_000000")
                item.set('title', question_name)
                qticomment = ET.SubElement(item, 'qticomment')
                #qticomment.text = self.question_description_title
                duration = ET.SubElement(item, 'duration')
                duration.text = self.test_time

                self.myroot[0][4].append(item)


                if duration.text != "":
                    duration.text = "P0Y0M0DT1H0M0S"

                print(self.myroot[0][0])
                print(self.myroot[0][1])
                print(self.myroot[0][2])
                print(self.myroot[0][3])
                print(self.myroot[0][4])
                #print(self.myroot[0][5])
                # print(self.myroot[0][6])

                print("root element is:", self.myroot)



                for assessment in self.myroot.iter('assessment'):
                    print(assessment.attrib)
                    assessment.set('title', str(self.test_title_entry.get()))

                itemmetadata = ET.SubElement(item, 'itemmetadata')
                presentation = ET.SubElement(item, 'presentation')
                presentation.set('label', question_name)
                flow = ET.SubElement(presentation, 'flow')
                material = ET.SubElement(flow, 'material')

                mattext = ET.SubElement(material, 'mattext')
                mattext.set('texttype', "text/html")


                if self.img_data != "EMPTY":
                    #mattext.text = "<p>" + self.question_description_main + "</p>" + "<p><img height=\"378\" src=\"il_0_mob_0000000\" width=\"482\" /></p>"
                    mattext.text = "<p>" + self.question_description_main + "</p>" + "<p><img height=\"378\" src=\"il_0_mob_000000" + str(x) + "\" width=\"482\" /></p>"


                    matimage = ET.SubElement(material, 'matimage')
                    matimage.set('label', "il_0_mob_000000" + str(x))  # Object -> Filename
                    matimage.set('uri', "objects/il_0_mob_000000" + str(x) + "/" + self.img_name + ".png")


                else:
                    mattext.text = "<p>" + self.question_description_main + "</p>"  # + "<p><img height=\"378\" src=\"il_0_mob_1955056\" width=\"482\" /></p>"

                qtimetadata = ET.SubElement(itemmetadata, 'qtimetadata')
                # -----------------------------------------------------------------------ILIAS VERSION
                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "ILIAS_VERSION"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
                fieldentry.text = "5.4.10 2020-03-04"
                # -----------------------------------------------------------------------QUESTION_TYPE
                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "QUESTIONTYPE"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
                fieldentry.text = "assFormulaQuestion"
                # -----------------------------------------------------------------------AUTHOR
                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "AUTHOR"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
                fieldentry.text = str(self.autor_entry.get())
                print(str(self.autor_entry.get()))
                # -----------------------------------------------------------------------POINTS
                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "points"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
                fieldentry.text = str(self.res1_points)

                # -----------------------------------------------------------------------Variable 1

                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "$v1"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
                fieldentry.text = "a:6:{" \
                                  "s:9:\"precision\";i:" + self.var1_prec + ";" \
                                  "s:12:\"intprecision\";s:" + self.var1_divby_length + ":\"" + self.var1_divby + "\";" \
                                  "s:8:\"rangemin\";d:" + self.var1_min + ";" \
                                  "s:8:\"rangemax\";d:" + self.var1_max + ";" \
                                  "s:4:\"unit\";s:0:\"\";" \
                                  "s:9:\"unitvalue\";s:0:\"\";" \
                                  "}"

                # -----------------------------------------------------------------------Variable 2

                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "$v2"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
                fieldentry.text = "a:6:{" \
                                  "s:9:\"precision\";i:" + self.var2_prec + ";" \
                                  "s:12:\"intprecision\";s:" + self.var2_divby_length + ":\"" + self.var2_divby + "\";" \
                                  "s:8:\"rangemin\";d:" + self.var2_min + ";" \
                                  "s:8:\"rangemax\";d:" + self.var2_max + ";" \
                                  "s:4:\"unit\";s:0:\"\";" \
                                  "s:9:\"unitvalue\";s:0:\"\";" \
                                  "}"

                # -----------------------------------------------------------------------Variable 3

                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "$v3"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
                fieldentry.text = "a:6:{" \
                                  "s:9:\"precision\";i:" + self.var3_prec + ";" \
                                   "s:12:\"intprecision\";s:" + self.var3_divby_length + ":\"" + self.var3_divby + "\";" \
                                   "s:8:\"rangemin\";d:" + self.var3_min + ";" \
                                   "s:8:\"rangemax\";d:" + self.var3_max + ";" \
                                   "s:4:\"unit\";s:0:\"\";" \
                                   "s:9:\"unitvalue\";s:0:\"\";" \
                                   "}"

                # -----------------------------------------------------------------------Variable 4

                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "$v4"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
                fieldentry.text = "a:6:{" \
                                  "s:9:\"precision\";i:" + self.var4_prec + ";" \
                                  "s:12:\"intprecision\";s:" + self.var4_divby_length + ":\"" + self.var4_divby + "\";" \
                                  "s:8:\"rangemin\";d:" + self.var4_min + ";" \
                                  "s:8:\"rangemax\";d:" + self.var4_max + ";" \
                                  "s:4:\"unit\";s:0:\"\";" \
                                  "s:9:\"unitvalue\";s:0:\"\";" \
                                  "}"

                # -----------------------------------------------------------------------Variable 5

                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "$v5"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
                fieldentry.text = "a:6:{" \
                                  "s:9:\"precision\";i:" + self.var5_prec + ";" \
                                  "s:12:\"intprecision\";s:" + self.var5_divby_length + ":\"" + self.var5_divby + "\";" \
                                  "s:8:\"rangemin\";d:" + self.var5_min + ";" \
                                  "s:8:\"rangemax\";d:" + self.var5_max + ";" \
                                  "s:4:\"unit\";s:0:\"\";" \
                                  "s:9:\"unitvalue\";s:0:\"\";" \
                                  "}"

                # -----------------------------------------------------------------------Variable 6

                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "$v6"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
                fieldentry.text = "a:6:{" \
                                  "s:9:\"precision\";i:" + self.var6_prec + ";" \
                                  "s:12:\"intprecision\";s:" + self.var6_divby_length + ":\"" + self.var6_divby + "\";" \
                                  "s:8:\"rangemin\";d:" + self.var6_min + ";" \
                                  "s:8:\"rangemax\";d:" + self.var6_max + ";" \
                                  "s:4:\"unit\";s:0:\"\";" \
                                  "s:9:\"unitvalue\";s:0:\"\";" \
                                  "}"

                # -----------------------------------------------------------------------Variable 7

                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "$v7"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
                fieldentry.text = "a:6:{" \
                                  "s:9:\"precision\";i:" + self.var7_prec + ";" \
                                  "s:12:\"intprecision\";s:" + self.var7_divby_length + ":\"" + self.var7_divby + "\";" \
                                  "s:8:\"rangemin\";d:" + self.var7_min + ";" \
                                  "s:8:\"rangemax\";d:" + self.var7_max + ";" \
                                  "s:4:\"unit\";s:0:\"\";" \
                                  "s:9:\"unitvalue\";s:0:\"\";" \
                                  "}"

                # -----------------------------------------------------------------------Solution 1
                # s for string length: "9" -> precision = "9" characters
                # rangemin: "i" for negative numbers, ...
                #           "d" for (negativ?) float numbers
                #           "i" for negativ whole numbers
                #           "s" for positiv whole numbers

                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "$r1"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
                fieldentry.text = "a:10:{" \
                                  "s:9:\"precision\";i:" + self.res1_prec + ";" \
                                  "s:9:\"tolerance\";s:" + self.res1_tol_length + ":\"" + self.res1_tol + "\";" \
                                  "s:8:\"rangemin\";s:" + self.res1_min_length + ":\"" + self.res1_min + "\";" \
                                  "s:8:\"rangemax\";s:" + self.res1_max_length + ":\"" + self.res1_max + "\";" \
                                  "s:6:\"points\";s:1:\"" + self.res1_points + "\";" \
                                  "s:7:\"formula\";s:" + self.res1_formula_length + ":\"" + self.res1_formula + "\";" \
                                  "s:6:\"rating\";s:0:\"\";" \
                                  "s:4:\"unit\";s:0:\"\";" \
                                  "s:9:\"unitvalue\";s:0:\"\";" \
                                  "s:11:\"resultunits\";a:0:{}" \
                                  "}"
                    # -----------------------------------------------------------------------Solution 2
                # s for string length: "9" -> precision = "9" characters
                # rangemin: "i" for negative numbers, ...
                #           "d" for (negativ?) float numbers
                #           "i" for negativ whole numbers
                #           "s" for positiv whole numbers

                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "$r2"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
                fieldentry.text = "a:10:{" \
                                  "s:9:\"precision\";i:" + self.res2_prec + ";" \
                                  "s:9:\"tolerance\";s:" + self.res2_tol_length + ":\"" + self.res2_tol + "\";" \
                                  "s:8:\"rangemin\";s:" + self.res2_min_length + ":\"" + self.res2_min + "\";" \
                                  "s:8:\"rangemax\";s:" + self.res2_max_length + ":\"" + self.res2_max + "\";" \
                                  "s:6:\"points\";s:1:\"" + self.res2_points + "\";" \
                                  "s:7:\"formula\";s:" + self.res2_formula_length + ":\"" + self.res2_formula + "\";" \
                                  "s:6:\"rating\";s:0:\"\";" \
                                  "s:4:\"unit\";s:0:\"\";" \
                                  "s:9:\"unitvalue\";s:0:\"\";" \
                                  "s:11:\"resultunits\";a:0:{}" \
                                  "}"
                # -----------------------------------------------------------------------Solution 3
                # s for string length: "9" -> precision = "9" characters
                # rangemin: "i" for negative numbers, ...
                #           "d" for (negativ?) float numbers
                #           "i" for negativ whole numbers
                #           "s" for positiv whole numbers

                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "$r3"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
                fieldentry.text = "a:10:{" \
                                  "s:9:\"precision\";i:" + self.res3_prec + ";" \
                                  "s:9:\"tolerance\";s:" + self.res3_tol_length + ":\"" + self.res3_tol + "\";" \
                                  "s:8:\"rangemin\";s:" + self.res3_min_length + ":\"" + self.res3_min + "\";" \
                                  "s:8:\"rangemax\";s:" + self.res3_max_length + ":\"" + self.res3_max + "\";" \
                                  "s:6:\"points\";s:1:\"" + self.res3_points + "\";" \
                                  "s:7:\"formula\";s:" + self.res3_formula_length + ":\"" + self.res3_formula + "\";" \
                                  "s:6:\"rating\";s:0:\"\";" \
                                  "s:4:\"unit\";s:0:\"\";" \
                                  "s:9:\"unitvalue\";s:0:\"\";" \
                                  "s:11:\"resultunits\";a:0:{}" \
                                  "}"





                # -----------------------------------------------------------------------ADDITIONAL_CONT_EDIT_MODE
                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "additional_cont_edit_mode"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
                fieldentry.text = "default"
                # -----------------------------------------------------------------------EXTERNAL_ID
                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "externalId"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
                fieldentry.text = "5ea15be69c1e96.43933468"

                self.mytree.write(self.project_root + "1590475954__0__tst_1944463\\" +'1590475954__0__qti_1944463.xml')
                print("DONE")

        conn.commit()
        conn.close()

        replace_characters()
        print("" + str(x))


def replace_characters():
    # with open("xml_form_edit\\" + 'NEW_1590230409__0__qti_1948621.xml') as f:
    with open(self.project_root + "1590475954__0__tst_1944463\\" +'1590475954__0__qti_1944463.xml') as f:
        xml_str = f.read()
    xml_str = xml_str.replace('&amp;', '&')

    # with open("xml_form_edit\\"+'ESCAPED_1590230409__0__qti_1948621.xml', "w") as f:
    with open(self.project_root + "1590475954__0__tst_1944463\\" + '1590475954__0__qti_1944463.xml', "w") as f:
        f.write(xml_str)

    print("WORKOVER FINISHED!")



class GUI_settings_window(Formelfrage):

    def __init__(self, master):



        self.test_settings = Tk()
        self.test_settings.title('Set Test-Settings')
        #self.test_settings.geometry('800x700')

        #self.frame_settings = LabelFrame(master, text="Settings Frame...", padx=5, pady=5)
        #self.frame_settings.grid(row=0, column=0, padx=10, pady=10, sticky=NW)

        self.frame1 = LabelFrame(self.test_settings, text="Test Settings Frame1...", padx=5, pady=5)
        self.frame1.grid(row=0, column=0, padx=20, pady=10, sticky=NW)

        self.frame2 = LabelFrame(self.test_settings, text="Test Settings Frame2...", padx=5, pady=5)
        self.frame2.grid(row=0, column=2, padx=20, pady=10, sticky=NW)

        self.res12_min_listbox_label = Label(self.frame1, text="EINSTELLUNGEN DES TESTS", font=('Helvetica', 10, 'bold'))
        self.res12_min_listbox_label.grid(row=0, column=0, sticky=W, padx=10, pady=(20, 0))

        self.res90_min_listbox_label = Label(self.frame1, text="Titel")
        self.res90_min_listbox_label.grid(row=1, column=0, sticky=W, padx=10)
        self.res91_max_listbox_label = Label(self.frame1, text="Beschreibung")
        self.res91_max_listbox_label.grid(row=2, column=0, sticky=W, padx=10)

        self.res1_max_listbox_label = Label(self.frame1, text="Auswahl der Testfragen")
        self.res1_max_listbox_label.grid(row=4, column=0, sticky=W, padx=10)
        self.res1_prec_listbox_label = Label(self.frame1, text="Datenschutz")
        self.res1_prec_listbox_label.grid(row=7, column=0, sticky=W, padx=10)

        self.res1_tol_listbox_label = Label(self.frame1, text="VERFÜGBARKEIT", font=('Helvetica', 10, 'bold'))
        self.res1_tol_listbox_label.grid(row=9, column=0, sticky=W, padx=10, pady=(20, 0))
        self.res1_points_listbox_label = Label(self.frame1, text="Online")
        self.res1_points_listbox_label.grid(row=10, column=0, sticky=W, padx=10)
        self.res13_points_listbox_label = Label(self.frame1, text="Zeitlich begrenzte Verfügbarkeit")
        self.res13_points_listbox_label.grid(row=11, column=0, sticky=W, padx=10)

        self.res22_tol_listbox_label = Label(self.frame1, text="INFORMATIONEN ZUM EINSTIEG", font=('Helvetica', 10, 'bold'))
        self.res22_tol_listbox_label.grid(row=12, column=0, sticky=W, padx=10, pady=(20, 0))
        self.res23_points_listbox_label = Label(self.frame1, text="Einleitung")
        self.res23_points_listbox_label.grid(row=13, column=0, sticky=W, padx=10)
        self.res24_points_listbox_label = Label(self.frame1, text="Testeigenschaften anzeigen")
        self.res24_points_listbox_label.grid(row=14, column=0, sticky=W, padx=10)

        self.res31_tol_listbox_label = Label(self.frame1, text="DURCHFÜHRUNG: ZUGANG", font=('Helvetica', 10, 'bold'))
        self.res31_tol_listbox_label.grid(row=15, column=0, sticky=W, padx=10, pady=(20, 0))
        self.res32_points_listbox_label = Label(self.frame1, text="Start")
        self.res32_points_listbox_label.grid(row=16, column=0, sticky=W, padx=10)
        self.res33_points_listbox_label = Label(self.frame1, text="Ende")
        self.res33_points_listbox_label.grid(row=17, column=0, sticky=W, padx=10)
        self.res34_tol_listbox_label = Label(self.frame1, text="Testpasswort")
        self.res34_tol_listbox_label.grid(row=18, column=0, sticky=W, padx=10)
        self.res35_points_listbox_label = Label(self.frame1, text="Nur ausgewählte Teilnehmer")
        self.res35_points_listbox_label.grid(row=19, column=0, sticky=W, padx=10)
        self.res36_points_listbox_label = Label(self.frame1, text="Anzahl gleichzeitiger Teilnehmer begrenzen")
        self.res36_points_listbox_label.grid(row=20, column=0, sticky=W, padx=10)

        self.res41_tol_listbox_label = Label(self.frame1, text="DURCHFÜHRUNG: STEUERUNG TESTDURCHLAUF",
                                        font=('Helvetica', 10, 'bold'))
        self.res41_tol_listbox_label.grid(row=21, column=0, sticky=W, padx=10, pady=(20, 0))
        self.res42_points_listbox_label = Label(self.frame1, text="Anzahl von Testdurchläufen begrenzen")
        self.res42_points_listbox_label.grid(row=22, column=0, sticky=W, padx=10)
        self.res43_points_listbox_label = Label(self.frame1, text="Wartezeit zwischen Durchläufen erzwingen")
        self.res43_points_listbox_label.grid(row=23, column=0, sticky=W, padx=10)
        self.res44_tol_listbox_label = Label(self.frame1, text="Bearbeitungsdauer begrenzen")
        self.res44_tol_listbox_label.grid(row=24, column=0, sticky=W, padx=10)
        self.res45_points_listbox_label = Label(self.frame1, text="Prüfungsansicht")
        self.res45_points_listbox_label.grid(row=25, column=0, sticky=W, padx=10)
        self.res46_points_listbox_label = Label(self.frame1, text="ILIAS-Prüfungsnummer anzeigen")
        self.res46_points_listbox_label.grid(row=26, column=0, sticky=W, padx=10)

        self.res51_tol_listbox_label = Label(self.frame2, text="DURCHFÜHRUNG: VERHALTEN DER FRAGE", font=('Helvetica', 10, 'bold'))
        self.res51_tol_listbox_label.grid(row=0, column=2, sticky=W, padx=10, pady=(20, 0))
        self.res52_points_listbox_label = Label(self.frame2, text="Anzeige der Fragentitel")
        self.res52_points_listbox_label.grid(row=1, column=2, sticky=W, padx=10)
        self.res53_points_listbox_label = Label(self.frame2, text="Automatisches speichern")
        self.res53_points_listbox_label.grid(row=4, column=2, sticky=W, padx=10)
        self.res54_tol_listbox_label = Label(self.frame2, text="Fragen mischen")
        self.res54_tol_listbox_label.grid(row=5, column=2, sticky=W, padx=10)
        self.res55_points_listbox_label = Label(self.frame2, text="Lösungshinweise")
        self.res55_points_listbox_label.grid(row=6, column=2, sticky=W, padx=10)
        self.res56_points_listbox_label = Label(self.frame2, text="Direkte Rückmeldung")
        self.res56_points_listbox_label.grid(row=7, column=2, sticky=W, padx=10)
        self.res57_tol_listbox_label = Label(self.frame2, text="Teilnehmerantworten")
        self.res57_tol_listbox_label.grid(row=8, column=2, sticky=W, padx=10)
        self.res58_points_listbox_label = Label(self.frame2, text="Verpflichtende Fragen")
        self.res58_points_listbox_label.grid(row=12, column=2, sticky=W, padx=10)

        self.res61_tol_listbox_label = Label(self.frame2, text="DURCHFÜHRUNG: FUNKTIONEN FÜR TEILNEHMER",
                                        font=('Helvetica', 10, 'bold'))
        self.res61_tol_listbox_label.grid(row=13, column=2, sticky=W, padx=10, pady=(20, 0))
        self.res62_points_listbox_label = Label(self.frame2, text="Verwendung vorheriger Lösungen")
        self.res62_points_listbox_label.grid(row=14, column=2, sticky=W, padx=10)
        self.res63_points_listbox_label = Label(self.frame2, text="\"Test unterbrechen\" anzeigen")
        self.res63_points_listbox_label.grid(row=15, column=2, sticky=W, padx=10)
        self.res64_tol_listbox_label = Label(self.frame2, text="Nicht beantwortete Fragen")
        self.res64_tol_listbox_label.grid(row=16, column=2, sticky=W, padx=10)
        self.res65_points_listbox_label = Label(self.frame2, text="Fragenliste und Bearbeitungsstand anzeigen")
        self.res65_points_listbox_label.grid(row=18, column=2, sticky=W, padx=10)
        self.res66_points_listbox_label = Label(self.frame2, text="Fragen markieren")
        self. res66_points_listbox_label.grid(row=19, column=2, sticky=W, padx=10)

        self.res71_tol_listbox_label = Label(self.frame2, text="TEST ABSCHLIESSEN", font=('Helvetica', 10, 'bold'))
        self.res71_tol_listbox_label.grid(row=20, column=2, sticky=W, padx=10, pady=(20, 0))
        self.res72_points_listbox_label = Label(self.frame2, text="Übersicht gegebener Antworten")
        self.res72_points_listbox_label.grid(row=21, column=2, sticky=W, padx=10)
        self.res73_points_listbox_label = Label(self.frame2, text="Abschließende Bemerkung")
        self.res73_points_listbox_label.grid(row=22, column=2, sticky=W, padx=10)
        self.res74_tol_listbox_label = Label(self.frame2, text="Weiterleitung")
        self.res74_tol_listbox_label.grid(row=23, column=2, sticky=W, padx=10)
        self.res75_points_listbox_label = Label(self.frame2, text="Benachrichtigung")
        self.res75_points_listbox_label.grid(row=24, column=2, sticky=W, padx=10)

        # --------------------------- CHECKBOXES ---------------------------------------

        self.var_online = StringVar()
        self.check_online = Checkbutton(self.frame1, text="", variable=self.var_online, onvalue="1", offvalue="0")
        self.check_online.deselect()
        self.check_online.grid(row=10, column=1, sticky=W)

        self.var_limited = StringVar()
        self.check_limited = Checkbutton(self.frame1, text="", variable=self.var_limited, onvalue="1", offvalue="0")
        self.check_limited.deselect()
        self.check_limited.grid(row=11, column=1, sticky=W)

        self.var_introduction = StringVar()
        self.check_introduction = Checkbutton(self.frame1, text="", variable=self.var_introduction, onvalue="1", offvalue="0")
        self.check_introduction.deselect()
        self.check_introduction.grid(row=13, column=1, sticky=W)

        self.var_test_prop = StringVar()
        self.check_test_prop = Checkbutton(self.frame1, text="", variable=self.var_test_prop, onvalue="1", offvalue="0")
        self.check_test_prop.deselect()
        self.check_test_prop.grid(row=14, column=1, sticky=W)

        self.var_test_password = StringVar()
        self.check_test_password = Checkbutton(self.frame1, text="", variable=self.var_test_password, onvalue="1", offvalue="0")
        self.check_test_password.deselect()
        self.check_test_password.grid(row=18, column=1, sticky=W)

        self.var_specific_users = StringVar()
        self.check_specific_users = Checkbutton(self.frame1, text="", variable=self.var_specific_users, onvalue="1", offvalue="0")
        self.check_specific_users.deselect()
        self.check_specific_users.grid(row=19, column=1, sticky=W)

        self.var_fixed_users = StringVar()
        self.check_fixed_users = Checkbutton(self.frame1, text="", variable=self.var_fixed_users, onvalue="1", offvalue="0")
        self.check_fixed_users.deselect()
        self.check_fixed_users.grid(row=20, column=1, sticky=W)

        self.var_limit_test_runs = StringVar()
        self.check_limit_test_runs = Checkbutton(self.frame1, text="", variable=self.var_limit_test_runs, onvalue="1", offvalue="0")
        self.check_limit_test_runs.deselect()
        self.check_limit_test_runs.grid(row=22, column=1, sticky=W)

        self.var_time_betw_test_runs = StringVar()
        self.check_time_betw_test_runs = Checkbutton(self.frame1, text="", variable=self.var_time_betw_test_runs, onvalue="1",
                                                offvalue="0")
        self.check_time_betw_test_runs.deselect()
        self.check_time_betw_test_runs.grid(row=23, column=1, sticky=W)

        self.var_processing_time = StringVar()
        self.check_processing_time = Checkbutton(self.frame1, text="", variable=self.var_processing_time, onvalue="1", offvalue="0")
        self.check_processing_time.deselect()
        self.check_processing_time.grid(row=24, column=1, sticky=W)

        self.var_examview = StringVar()
        self.check_examview = Checkbutton(self.frame1, text="", variable=self.var_examview, onvalue="1", offvalue="0")
        self.check_examview.deselect()
        self.check_examview.grid(row=25, column=1, sticky=W)

        self.var_show_ilias_nr = StringVar()
        self.check_show_ilias_nr = Checkbutton(self.frame1, text="", variable=self.var_show_ilias_nr, onvalue="1", offvalue="0")
        self.check_show_ilias_nr.deselect()
        self.check_show_ilias_nr.grid(row=26, column=1, sticky=W)

        self.var_autosave = StringVar()
        self.check_autosave = Checkbutton(self.frame2, text="", variable=self.var_autosave, onvalue="1", offvalue="0")
        self.check_autosave.deselect()
        self.check_autosave.grid(row=4, column=3, sticky=W)

        self.var_mix_questions = StringVar()
        self.check_mix_questions = Checkbutton(self.frame2, text="", variable=self.var_mix_questions, onvalue="1", offvalue="0")
        self.check_mix_questions.deselect()
        self.check_mix_questions.grid(row=5, column=3, sticky=W)

        self.var_show_solution_notes = StringVar()
        self.check_show_solution_notes = Checkbutton(self.frame2, text="", variable=self.var_show_solution_notes, onvalue="1",
                                                offvalue="0")
        self.check_show_solution_notes.deselect()
        self.check_show_solution_notes.grid(row=6, column=3, sticky=W)

        self.var_direct_response = StringVar()
        self.check_direct_response = Checkbutton(self.frame2, text="", variable=self.var_direct_response, onvalue="1", offvalue="0")
        self.check_direct_response.deselect()
        self.check_direct_response.grid(row=7, column=3, sticky=W)

        self.var_mandatory_questions = StringVar()
        self.check_mandatory_questions = Checkbutton(self.frame2, text="", variable=self.var_mandatory_questions, onvalue="1",
                                                offvalue="0")
        self.check_mandatory_questions.deselect()
        self.check_mandatory_questions.grid(row=12, column=3, sticky=W)

        self.var_use_previous_solution = StringVar()
        self.check_use_previous_solution = Checkbutton(self.frame2, text="", variable=self.var_use_previous_solution, onvalue="1",
                                                  offvalue="0")
        self.check_use_previous_solution.deselect()
        self.check_use_previous_solution.grid(row=14, column=3, sticky=W)

        self.var_show_test_cancel = StringVar()
        self.check_show_test_cancel = Checkbutton(self.frame2, text="", variable=self.var_show_test_cancel, onvalue="1", offvalue="0")
        self.check_show_test_cancel.deselect()
        self.check_show_test_cancel.grid(row=15, column=3, sticky=W)

        self.var_show_question_list_process_status = StringVar()
        self.check_show_question_list_process_status = Checkbutton(self.frame2, text="", variable=self.var_show_question_list_process_status, onvalue="1", offvalue="0")
        self.check_show_question_list_process_status.deselect()
        self.check_show_question_list_process_status.grid(row=18, column=3, sticky=W)

        self.var_question_mark = StringVar()
        self.check_question_mark = Checkbutton(self.frame2, text="", variable=self.var_question_mark, onvalue="1", offvalue="0")
        self.check_question_mark.deselect()
        self.check_question_mark.grid(row=19, column=3, sticky=W)

        self.var_overview_answers = StringVar()
        self.check_overview_answers = Checkbutton(self.frame2, text="", variable=self.var_overview_answers, onvalue="1", offvalue="0")
        self.check_overview_answers.deselect()
        self.check_overview_answers.grid(row=21, column=3, sticky=W)

        self.var_show_end_comment = StringVar()
        self.check_show_end_comment = Checkbutton(self.frame2, text="", variable=self.var_show_end_comment, onvalue="1", offvalue="0")
        self.check_show_end_comment.deselect()
        self.check_show_end_comment.grid(row=22, column=3, sticky=W)

        self.var_forwarding = StringVar()
        self.check_forwarding = Checkbutton(self.frame2, text="", variable=self.var_forwarding, onvalue="1", offvalue="0")
        self.check_forwarding.deselect()
        self.check_forwarding.grid(row=23, column=3, sticky=W)

        self.var_notification = StringVar()
        self.check_notification = Checkbutton(self.frame2, text="", variable=self.var_notification, onvalue="1", offvalue="0")
        self.check_notification.deselect()
        self.check_notification.grid(row=24, column=3, sticky=W)

        # --------------------------- RADIO BUTTONS ---------------------------------------

        self.select_question = IntVar()
        self.select_question.set('1')
        self.select_question_radiobtn1 = Radiobutton(self.frame1, text="Fest definierte Fragenauswahl", variable=self.select_question, value=1)
        self.select_question_radiobtn1.grid(row=4, column=1, pady=0, sticky=W)
        self.select_question_radiobtn2 = Radiobutton(self.frame1, text="Zufällige Fragenauswahl", variable=self.select_question, value=2)
        self.select_question_radiobtn2.grid(row=5, column=1, pady=0, sticky=W)
        self.select_question_radiobtn3 = Radiobutton(self.frame1, text="Wiedervorlagemodus - alle Fragen eines Fragenpools", variable=self.select_question, value=3)
        self.select_question_radiobtn3.grid(row=6, column=1, pady=0, sticky=W)
        # rb2.bind('<Motion>', lambda e: print(str(select_question.get())))

        self.anonym = StringVar()
        self.anonym.set = "1"
        Radiobutton(self.frame1, text="Testergebnisse mit Namen", variable=self.anonym, value="1", borderwidth=0, command=self.anonym.get()).grid(row=7, column=1, pady=0, sticky=W)
        Radiobutton(self.frame1, text="Testergebnisse ohne Namen", variable=self.anonym, value="2", borderwidth=0,command=self.anonym.get()).grid(row=8, column=1, pady=0, sticky=W)

        self.show_question_title = StringVar()
        self.show_question_title.set = "1"
        Radiobutton(self.frame2, text="Fragentitel und erreichbare Punkte", variable=self.show_question_title, value="1",borderwidth=0, command=self.show_question_title.get()).grid(row=1, column=3, pady=0, sticky=W)
        Radiobutton(self.frame2, text="Nur Fragentitel", variable=self.show_question_title, value="2", borderwidth=0,command=self.show_question_title.get()).grid(row=2, column=3, pady=0, sticky=W)
        Radiobutton(self.frame2, text="Weder Fragentitel noch erreichbare Punkte", variable=self.show_question_title, value="3",borderwidth=0, command=self.show_question_title.get()).grid(row=3, column=3, pady=0, sticky=W)

        self.user_response = StringVar()
        self.user_response.set = "1"
        Radiobutton(self.frame2, text="Antworten während des Testdurchlaufs nicht festschreiben", variable=self.user_response,value="1", borderwidth=0, command=self.user_response.get()).grid(row=8, column=3, pady=0, sticky=W)
        Radiobutton(self.frame2, text="Antworten bei Anzeige der Rückmeldung festschreiben", variable=self.user_response, value="2",borderwidth=0, command=self.user_response.get()).grid(row=9, column=3, pady=0, sticky=W)
        Radiobutton(self.frame2, text="Antworten bei Anzeige der Folgefrage festschreiben", variable=self.user_response, value="3",borderwidth=0, command=self.user_response.get()).grid(row=10, column=3, pady=0, sticky=W)
        Radiobutton(self.frame2, text="Antworten mit der Anzeige von Rückmeldungen oder der Folgefrage festschreiben",variable=self.user_response, value="4", borderwidth=0, command=self.user_response.get()).grid(row=11, column=3,pady=0, sticky=W)

        self.not_answered_questions = StringVar()
        self.not_answered_questions.set = "1"
        Radiobutton(self.frame2, text="Nicht beantwortete Fragen bleiben an ihrem Platz", variable=self.not_answered_questions,value="1", borderwidth=0, command=self.not_answered_questions.get()).grid(row=16, column=3, pady=0, sticky=W)
        Radiobutton(self.frame2, text="Nicht beantwortete Fragen werden ans Testende gesschoben", variable=self.not_answered_questions, value="2", borderwidth=0, command=self.not_answered_questions.get()).grid(row=17, column=3, pady=0, sticky=W)

        # --------------------------- ENTRY BOXES ---------------------------------------

        self.titel_entry = Entry(self.frame1, width=47)
        self.titel_entry.grid(row=1, column=1)

        self.start_entry = Entry(self.frame1, width=30)
        self.start_entry.grid(row=16, column=1, sticky=W)

        self.ende_entry = Entry(self.frame1, width=30)
        self.ende_entry.grid(row=17, column=1, sticky=W)

        self.bar = Scrollbar(self.frame1)
        self.infobox = Text(self.frame1, height=4, width=40, font=('Helvetica', 9))
        self.bar.grid(row=2, column=2)
        self.infobox.grid(row=2, column=1, pady=10)
        self.bar.config(command=self.infobox.yview)
        self.infobox.config(yscrollcommand=self.bar.set)




# print("--------------------3-----------------------------")

app = Tk()
GUI = GuiMainWindow(app)
app.mainloop()

def trash_class():
    """
    class MultipleChoice(Formelfrage):
        def __init__(self):
            # self.my_frame = Frame(master)
            # self.my_frame.grid()

            self.mc_frame = LabelFrame(self.multipleChoice_tab, text="Multiple Choice", padx=5, pady=5)
            self.mc_frame.grid(row=0, column=0, padx=10, pady=10, sticky=NW)

            self.mc_title_label = Label(self.mc_frame, text="Titel")
            self.mc_title_label.grid(row=0, column=0, sticky=W, padx=10, pady=(10, 0))
            self.mc_title_entry = Entry(self.mc_frame, width=60)
            self.mc_title_entry.grid(row=0, column=1, pady=(10, 0), sticky=W)

            # mc_author_label = Label(mc_frame, text="Autor")
            # mc_author_label.grid(row=1, column=0, sticky=W, padx=10)
            # mc_author_entry = Entry(mc_frame, width=60)
            # mc_author_entry.grid(row=1, column=1, sticky=W)

            self.mc_description_label = Label(self.mc_frame, text="Beschreibung")
            self.mc_description_label.grid(row=2, column=0, sticky=W, padx=10)
            self.mc_description_entry = Entry(self.mc_frame, width=60)
            self.mc_description_entry.grid(row=2, column=1, sticky=W)

            self.mc_question_textfield_label = Label(self.mc_frame, text="Frage")
            self.mc_question_textfield_label.grid(row=3, column=0, sticky=W, padx=10)

            # self.bar = Scrollbar(self.mc_frame)
            # self.infobox = Text(self.mc_frame, height=4, width=52, font=('Helvetica', 9))
            # self.bar.grid(row=3, column=2, sticky=W)
            # self.infobox.grid(row=3, column=1, pady=10, sticky=W)
            # self.bar.config(command=self.infobox.yview)
            # self.infobox.config(yscrollcommand=self.bar.set)

            self.mc_processing_time_label = Label(self.mc_frame, text="Bearbeitungsdauer")
            self.mc_processing_time_label.grid(row=4, column=0, sticky=W, pady=(5, 0), padx=10)

            self.mc_processing_time_label = Label(self.mc_frame, text="Std:")
            self.mc_processing_time_label.grid(row=4, column=1, sticky=W, pady=(5, 0))
            self.mc_processing_time_label = Label(self.mc_frame, text="Min:")
            self.mc_processing_time_label.grid(row=4, column=1, sticky=W, padx=70, pady=(5, 0))
            self.mc_processing_time_label = Label(self.mc_frame, text="Sek:")
            self.mc_processing_time_label.grid(row=4, column=1, sticky=W, padx=145, pady=(5, 0))

            ### Preview LaTeX
            expr = r'$$  {\text{Zu berechnen ist:  }}\  sin(x^2)\ {\text{Textblock 2}}\ {formel2} $$'
            preview(expr, viewer='file', filename='output.png')

            file_image = ImageTk.PhotoImage(Image.open('output.png'))
            file_image_label = Label(self.mc_frame, image=file_image)
            file_image_label.image = file_image

            def latex_preview():
                file_image_label.grid(row=20, column=1, pady=20)

            self.myLatex_btn = Button(self.mc_frame, text="show LaTeX Preview", command=latex_preview)
            self.myLatex_btn.grid(row=4, column=1, sticky=E)

            ###

            self.processingtime_hours = list(range(24))
            self.processingtime_minutes = list(range(60))
            self.processingtime_seconds = list(range(60))

            self.proc_hours_box = ttk.Combobox(self.mc_frame, value=self.processingtime_hours, width=2)
            self.proc_minutes_box = ttk.Combobox(self.mc_frame, value=self.processingtime_minutes, width=2)
            self.proc_seconds_box = ttk.Combobox(self.mc_frame, value=self.processingtime_seconds, width=2)

            self.proc_hours_box.current(0)
            self.proc_minutes_box.current(0)
            self.proc_seconds_box.current(0)

            self.proc_hours_box.bind("<<ComboboxSelected>>")
            self.proc_hours_box.bind("<<ComboboxSelected>>")
            self.proc_hours_box.bind("<<ComboboxSelected>>")

            self.proc_hours_box.grid(row=4, column=1, sticky=W, padx=25, pady=(5, 0))
            self.proc_minutes_box.grid(row=4, column=1, sticky=W, padx=100, pady=(5, 0))
            self.proc_seconds_box.grid(row=4, column=1, sticky=W, padx=170, pady=(5, 0))

            self.mc_mix_questions_label = Label(self.mc_frame, text="Fragen mischen")
            self.mc_mix_questions_label.grid(row=5, column=0, sticky=W, padx=10, pady=(5, 0))

            self.mc_var_mix_questions = StringVar()
            self.mc_check_mix_questions = Checkbutton(self.mc_frame, text="", variable=self.mc_var_mix_questions,
                                                      onvalue="1",
                                                      offvalue="0")
            self.mc_check_mix_questions.deselect()
            self.mc_check_mix_questions.grid(row=5, column=1, sticky=W, pady=(5, 0))

            self.mc_answer_limitation_label = Label(self.mc_frame, text="Antwortbeschränkung")
            self.mc_answer_limitation_label.grid(row=6, column=0, sticky=W, padx=10, pady=(5, 0))
            self.mc_answer_limitation_entry = Entry(self.mc_frame, width=10)
            self.mc_answer_limitation_entry.grid(row=6, column=1, sticky=W, pady=(5, 0))

            self.answer_editor_box_label = Label(self.mc_frame, text="Antwort-Editor")
            self.answer_editor_box_label.grid(row=7, column=0, sticky=W, padx=10, pady=(5, 0))
            self.answer_editor_value = ("Einzeilige Antwort", "Mehrzeilige Antwort")
            self.answer_editor_box = ttk.Combobox(self.mc_frame, value=self.answer_editor_value, width=20)
            self.answer_editor_box.bind("<<ComboboxSelected>>")
            self.answer_editor_box.grid(row=7, column=1, sticky=W, pady=(5, 0))

            def mc_answer_selected(event):  # "event" is necessary here to react, although it is not used "officially"

                if self.numbers_of_answers_box.get() == '1':
                    mc_var2_remove()
                    mc_var3_remove()
                    mc_var4_remove()
                    mc_var5_remove()
                    mc_var6_remove()
                    mc_var7_remove()


                elif self.numbers_of_answers_box.get() == '2':
                    mc_var2_show()
                    mc_var3_remove()
                    mc_var4_remove()
                    mc_var5_remove()
                    mc_var6_remove()
                    mc_var7_remove()


                elif self.numbers_of_answers_box.get() == '3':
                    mc_var2_show()
                    mc_var3_show()
                    mc_var4_remove()
                    mc_var5_remove()
                    mc_var6_remove()
                    mc_var7_remove()


                elif self.numbers_of_answers_box.get() == '4':
                    mc_var2_show()
                    mc_var3_show()
                    mc_var4_show()
                    mc_var5_remove()
                    mc_var6_remove()
                    mc_var7_remove()


                elif self.numbers_of_answers_box.get() == '5':
                    mc_var2_show()
                    mc_var3_show()
                    mc_var4_show()
                    mc_var5_show()
                    mc_var6_remove()
                    mc_var7_remove()


                elif self.numbers_of_answers_box.get() == '6':
                    mc_var2_show()
                    mc_var3_show()
                    mc_var4_show()
                    mc_var5_show()
                    mc_var6_show()
                    mc_var7_remove()


                elif self.numbers_of_answers_box.get() == '7':
                    mc_var2_show()
                    mc_var3_show()
                    mc_var4_show()
                    mc_var5_show()
                    mc_var6_show()
                    mc_var7_show()

            self.numbers_of_answers_box_label = Label(self.mc_frame, text="Anzahl der Antworten")
            self.numbers_of_answers_box_label.grid(row=8, column=0, sticky=W, padx=10, pady=(5, 0))
            self.numbers_of_answers_value = ["1", "2", "3", "4", "5", "6", "7"]
            self.numbers_of_answers_box = ttk.Combobox(self.mc_frame, value=self.numbers_of_answers_value, width=20)
            self.numbers_of_answers_box.bind("<<ComboboxSelected>>", mc_answer_selected)
            self.numbers_of_answers_box.grid(row=8, column=1, sticky=W, pady=(5, 0))

            # self.Label(self.mc_frame, text="Antworten").grid(row=9, column=0, sticky=W, padx=10, pady=(5, 0))
            # self.Label(self.mc_frame, text="Antwort-Text").grid(row=9, column=1, sticky=W, pady=(5, 0))
            # self.Label(self.mc_frame, text="Punkte:\nAusgewählt").grid(row=9, column=1, sticky=E, padx=20)
            # self.Label(self.mc_frame, text="Punkte:\nNicht ausgewählt").grid(row=9, column=2)

            # ------------------------------- VARIABLES RANGE: MINIMUM - TEXT & ENTRY --------------------------------------------
            self.var1_answer_text, self.var1_points_picked_text, self.var1_points_not_picked_text = StringVar(), StringVar(), StringVar()
            self.var2_answer_text, self.var2_points_picked_text, self.var2_points_not_picked_text = StringVar(), StringVar(), StringVar()
            self.var3_answer_text, self.var3_points_picked_text, self.var3_points_not_picked_text = StringVar(), StringVar(), StringVar()
            self.var4_answer_text, self.var4_points_picked_text, self.var4_points_not_picked_text = StringVar(), StringVar(), StringVar()
            self.var5_answer_text, self.var5_points_picked_text, self.var5_points_not_picked_text = StringVar(), StringVar(), StringVar()
            self.var6_answer_text, self.var6_points_picked_text, self.var6_points_not_picked_text = StringVar(), StringVar(), StringVar()
            self.var7_answer_text, self.var7_points_picked_text, self.var7_points_not_picked_text = StringVar(), StringVar(), StringVar()

            self.var1_answer_entry = Entry(self.mc_frame, textvariable=self.var1_answer_text, width=40)
            self.var2_answer_entry = Entry(self.mc_frame, textvariable=self.var2_answer_text, width=40)
            self.var3_answer_entry = Entry(self.mc_frame, textvariable=self.var3_answer_text, width=40)
            self.var4_answer_entry = Entry(self.mc_frame, textvariable=self.var4_answer_text, width=40)
            self.var5_answer_entry = Entry(self.mc_frame, textvariable=self.var5_answer_text, width=40)
            self.var6_answer_entry = Entry(self.mc_frame, textvariable=self.var6_answer_text, width=40)
            self.var7_answer_entry = Entry(self.mc_frame, textvariable=self.var7_answer_text, width=40)

            # ------------------------------- VARIABLES RANGE:  MAXIMUM - TEXT & ENTRY --------------------------------------------

            self.var1_points_picked_entry = Entry(self.mc_frame, textvariable=self.var1_points_picked_text, width=6)
            self.var2_points_picked_entry = Entry(self.mc_frame, textvariable=self.var2_points_picked_text, width=6)
            self.var3_points_picked_entry = Entry(self.mc_frame, textvariable=self.var3_points_picked_text, width=6)
            self.var4_points_picked_entry = Entry(self.mc_frame, textvariable=self.var4_points_picked_text, width=6)
            self.var5_points_picked_entry = Entry(self.mc_frame, textvariable=self.var5_points_picked_text, width=6)
            self.var6_points_picked_entry = Entry(self.mc_frame, textvariable=self.var6_points_picked_text, width=6)
            self.var7_points_picked_entry = Entry(self.mc_frame, textvariable=self.var7_points_picked_text, width=6)

            # ------------------------------- VARIABLES PRECISION - TEXT & ENTRY --------------------------------------------

            self.var1_points_not_picked_entry = Entry(self.mc_frame, textvariable=self.var1_points_not_picked_text,
                                                      width=6)
            self.var2_points_not_picked_entry = Entry(self.mc_frame, textvariable=self.var2_points_not_picked_text,
                                                      width=6)
            self.var3_points_not_picked_entry = Entry(self.mc_frame, textvariable=self.var3_points_not_picked_text,
                                                      width=6)
            self.var4_points_not_picked_entry = Entry(self.mc_frame, textvariable=self.var4_points_not_picked_text,
                                                      width=6)
            self.var5_points_not_picked_entry = Entry(self.mc_frame, textvariable=self.var5_points_not_picked_text,
                                                      width=6)
            self.var6_points_not_picked_entry = Entry(self.mc_frame, textvariable=self.var6_points_not_picked_text,
                                                      width=6)
            self.var7_points_not_picked_entry = Entry(self.mc_frame, textvariable=self.var7_points_not_picked_text,
                                                      width=6)

            self.answer1_label = Label(self.mc_frame, text="Antwort 1")
            self.answer2_label = Label(self.mc_frame, text="Antwort 2")
            self.answer3_label = Label(self.mc_frame, text="Antwort 3")
            self.answer4_label = Label(self.mc_frame, text="Antwort 4")
            self.answer5_label = Label(self.mc_frame, text="Antwort 5")
            self.answer6_label = Label(self.mc_frame, text="Antwort 6")
            self.answer7_label = Label(self.mc_frame, text="Antwort 7")

            self.answer1_label.grid(row=10, column=0, sticky=W, padx=30)
            self.var1_answer_entry.grid(row=10, column=1, sticky=W)
            self.var1_points_picked_entry.grid(row=10, column=1, sticky=E, padx=30)
            self.var1_points_not_picked_entry.grid(row=10, column=2)

            def mc_var2_show():
                self.answer2_label.grid(row=11, column=0, sticky=W, padx=30)
                self.var2_answer_entry.grid(row=11, column=1, sticky=W)
                self.var2_points_picked_entry.grid(row=11, column=1, sticky=E, padx=30)
                self.var2_points_not_picked_entry.grid(row=11, column=2)

            def mc_var3_show():
                self.answer3_label.grid(row=12, column=0, sticky=W, padx=30)
                self.var3_answer_entry.grid(row=12, column=1, sticky=W)
                self.var3_points_picked_entry.grid(row=12, column=1, sticky=E, padx=30)
                self.var3_points_not_picked_entry.grid(row=12, column=2)

            def mc_var4_show():
                self.answer4_label.grid(row=13, column=0, sticky=W, padx=30)
                self.var4_answer_entry.grid(row=13, column=1, sticky=W)
                self.var4_points_picked_entry.grid(row=13, column=1, sticky=E, padx=30)
                self.var4_points_not_picked_entry.grid(row=13, column=2)

            def mc_var5_show():
                self.answer5_label.grid(row=14, column=0, sticky=W, padx=30)
                self.var5_answer_entry.grid(row=14, column=1, sticky=W)
                self.var5_points_picked_entry.grid(row=14, column=1, sticky=E, padx=30)
                self.var5_points_not_picked_entry.grid(row=14, column=2)

            def mc_var6_show():
                self.answer6_label.grid(row=15, column=0, sticky=W, padx=30)
                self.var6_answer_entry.grid(row=15, column=1, sticky=W)
                self.var6_points_picked_entry.grid(row=15, column=1, sticky=E, padx=30)
                self.var6_points_not_picked_entry.grid(row=15, column=2)

            def mc_var7_show():
                self.answer7_label.grid(row=16, column=0, sticky=W, padx=30)
                self.var7_answer_entry.grid(row=16, column=1, sticky=W)
                self.var7_points_picked_entry.grid(row=16, column=1, sticky=E, padx=30)
                self.var7_points_not_picked_entry.grid(row=16, column=2)

            def mc_var2_remove():
                self.answer2_label.grid_remove()
                self.var2_answer_entry.grid_remove()
                self.var2_points_picked_entry.grid_remove()
                self.var2_points_not_picked_entry.grid_remove()

            def mc_var3_remove():
                self.answer3_label.grid_remove()
                self.var3_answer_entry.grid_remove()
                self.var3_points_picked_entry.grid_remove()
                self.var3_points_not_picked_entry.grid_remove()

            def mc_var4_remove():
                self.answer4_label.grid_remove()
                self.var4_answer_entry.grid_remove()
                self.var4_points_picked_entry.grid_remove()
                self.var4_points_not_picked_entry.grid_remove()

            def mc_var5_remove():
                self.answer5_label.grid_remove()
                self.var5_answer_entry.grid_remove()
                self.var5_points_picked_entry.grid_remove()
                self.var5_points_not_picked_entry.grid_remove()

            def mc_var6_remove():
                self.answer6_label.grid_remove()
                self.var6_answer_entry.grid_remove()
                self.var6_points_picked_entry.grid_remove()
                self.var6_points_not_picked_entry.grid_remove()

            def mc_var7_remove():
                self.answer7_label.grid_remove()
                self.var7_answer_entry.grid_remove()
                self.var7_points_picked_entry.grid_remove()
                self.var7_points_not_picked_entry.grid_remove()

    class create_multiplechoice(MultipleChoice):
        def __init__(self):
            self.mytree = ET.parse("xml_form_orig\\" + 'testing_formular.xml')
            self.myroot = self.mytree.getroot()

            self.frame_mc_create = LabelFrame(self.formula_tab, text="Create Multiplechoice", padx=5, pady=5)
            self.frame_mc_create.grid(row=1, column=2)

        def create_mc_question(self):
            questestinterop = ET.Element('questestinterop')
            assessment = ET.SubElement(questestinterop, 'assessment')
            section = ET.SubElement(assessment, 'section')
            item = ET.SubElement(section, 'item')

            duration = ET.SubElement(item, 'duration')
            duration.text = self.test_time

            qticomment = ET.SubElement(item, 'qticomment')
            # qticomment.text = self.mc_question_description_title

            itemmetadata = ET.SubElement(item, 'itemmetadata')
            presentation = ET.SubElement(item, 'presentation')
            # presentation.set('label', self.mc_q)
            flow = ET.SubElement(presentation, 'flow')
            material = ET.SubElement(flow, 'material')

            mattext = ET.SubElement(material, 'mattext')
            mattext.set('texttype', "text/html")

            # item.set('ident', "il_0_qst_000000")
            # item.set('title', question_name)

            self.myroot[0][4].append(item)

            qtimetadata = ET.SubElement(itemmetadata, 'qtimetadata')
            # -----------------------------------------------------------------------ILIAS VERSION
            qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
            fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
            fieldlabel.text = "ILIAS_VERSION"
            fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
            fieldentry.text = "5.4.10 2020-03-04"
            # -----------------------------------------------------------------------QUESTION_TYPE
            qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
            fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
            fieldlabel.text = "QUESTIONTYPE"
            fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
            fieldentry.text = "MULTIPLE CHOICE QUESTION"
            # -----------------------------------------------------------------------AUTHOR
            qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
            fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
            fieldlabel.text = "AUTHOR"
            fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
            fieldentry.text = "Tobias Panteleit"
            # -----------------------------------------------------------------------additional_cont_edit_mode
            qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
            fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
            fieldlabel.text = "additional_cont_edit_mode"
            fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
            fieldentry.text = "default"
            # -----------------------------------------------------------------------externalId
            qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
            fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
            fieldlabel.text = "externalId"
            fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
            fieldentry.text = "59a32416e65da6.54228908"
            # -----------------------------------------------------------------------thumb_size
            qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
            fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
            fieldlabel.text = "thumb_size"
            fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
            fieldentry.text = ""
            # -----------------------------------------------------------------------feedback_setting
            qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
            fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
            fieldlabel.text = "feedback_setting"
            fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
            fieldentry.text = "1"
            # -----------------------------------------------------------------------singleline
            qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
            fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
            fieldlabel.text = "singleline"
            fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
            fieldentry.text = "1"
            """
def trash():
    """   
        class updateFormelFrage(Formelfrage):
    def __init__(self):
        conn = sqlite3.connect('ilias_questions_db.db')
        c = conn.cursor()
        records = c.fetchall()
        self.record_id = self.create_formelfrage_entry.get()

       ##### FILL ENTRY FIELDS TO EDIT

        # Loop thru Results
        for record in records:
            #formula_entry_editor.insert(0, record[0])

            self.formula_title_entry = str(record[0])
            self.formula_description_entry = str(record[1])
            self.formula_question_entry = str(record[2])



            self.var1_min_entry = str(record[4])
            self.var1_max_entry = str(record[5])
            self.var1_prec_entry = str(record[6])
            self.var1_divby_entry = str(record[7])

            self.var2_min_entry = str(record[8])
            self.var2_max_entry = str(record[9])
            self.var2_prec_entry = str(record[10])
            self.var2_divby_entry = str(record[11])

            self.var3_min_entry = str(record[12])
            self.var3_max_entry = str(record[13])
            self.var3_prec_entry = str(record[14])
            self.var3_divby_entry = str(record[15])

            self.var4_min_entry = str(record[16])
            self.var4_max_entry = str(record[17])
            self.var4_prec_entry = str(record[18])
            self.var4_divby_entry = str(record[19])

            self.var5_min_entry = str(record[20])
            self.var5_max_entry = str(record[21])
            self.var5_prec_entry = str(record[22])
            self.var5_divby_entry = str(record[23])

            self.var6_min_entry = str(record[24])
            self.var6_max_entry = str(record[25])
            self.var6_prec_entry = str(record[26])
            self.var6_divby_entry = str(record[27])

            self.var7_min_entry = str(record[28])
            self.var7_max_entry = str(record[29])
            self.var7_prec_entry = str(record[30])
            self.var7_divby_entry = str(record[31])

            self.res1_min_entry = str(record[32])
            self.res1_max_entry = str(record[33])
            self.res1_prec_entry = str(record[34])
            self.res1_tol_entry = str(record[35])
            self.res1_points_entry = str(record[36])
            self.res1_formula_entry = str(record[3])

            self.res2_min_entry = str(record[37])
            self.res2_max_entry = str(record[38])
            self.res2_prec_entry = str(record[39])
            self.res2_tol_entry = str(record[40])
            self.res2_points_entry = str(record[41])
            self.res2_formula_entry = str(record[49])

            self.res3_min_entry = str(record[42])
            self.res3_max_entry = str(record[43])
            self.res3_prec_entry = str(record[44])
            self.res3_tol_entry = str(record[45])
            self.res3_points_entry = str(record[46])
            self.res3_formula_entry = str(record[50])

            #self.img_name_entry = str(record[47])
            #self.img_data_entry = str(record[48])
            #self.test_time_entry = str(record[51])
            #self.oid_entry = str(record[52])


       #### UPDATE DATABASE ENTRY
        c.execute(""""""UPDATE my_table SET
                
                formula_title = :formula_title
                formula_description_title = :formula_description_title
                formula_description = :formula_description
                
                res1_formula = :res1_formula
                var1_min = :var1_min,
                var1_max = :var1_max,
                var1_prec = :var1_prec,
                var1_divby = :var1_divby,

                var2_min = :var2_min,
                var2_max = :var2_max,
                var2_prec = :var2_prec,
                var2_divby = :var2_divby,

                var3_min = :var3_min,
                var3_max = :var3_max,
                var3_prec = :var3_prec,
                var3_divby = :var3_divby,
                
                var4_min = :var4_min,
                var4_max = :var4_max,
                var4_prec = :var4_prec,
                var4_divby = :var4_divby,
                
                var5_min = :var5_min,
                var5_max = :var5_max,
                var5_prec = :var5_prec,
                var5_divby = :var5_divby,
                
                var6_min = :var6_min,
                var6_max = :var6_max,
                var6_prec = :var6_prec,
                var6_divby = :var6_divby,
                
                var7_min = :var7_min,
                var7_max = :var7_max,
                var7_prec = :var7_prec,
                var7_divby = :var7_divby,


                res1_min = :res1_min,
                res1_max = :res1_max,
                res1_prec = :res1_prec,
                res1_tol = :res1_tol,
                res1_points = :res1_points
                
                
                res2_min = :res2_min,
                res2_max = :res2_max,
                res2_prec = :res2_prec,
                res2_tol = :res2_tol,
                res2_points = :res2_points
                res3_formula = :res2_formula   
                
                res3_min = :res3_min,
                res3_max = :res3_max,
                res3_prec = :res3_prec,
                res3_tol = :res3_tol,
                res3_points = :res3_points
                res3_formula = :res3_formula
                
                WHERE oid = :oid"""""",
                  {'formula': self.res1_formula_entry.get(),
                   'var1_min': self.var1_min_entry.get(),
                   'var1_max': self.var1_max_entry.get(),
                   'var1_prec': self.var1_prec_entry.get(),
                   'var1_divby': self.var1_divby_entry.get(),

                   'var2_min': self.var2_min_entry.get(),
                   'var2_max': self.var2_max_entry.get(),
                   'var2_prec': self.var2_prec_entry.get(),
                   'var2_divby': self.var2_divby_entry.get(),

                   'var3_min': self.var3_min_entry.get(),
                   'var3_max': self.var3_max_entry.get(),
                   'var3_prec': self.var3_prec_entry.get(),
                   'var3_divby': self.var3_divby_entry.get(),

                   'var4_min': self.var4_min_entry.get(),
                   'var4_max': self.var4_max_entry.get(),
                   'var4_prec': self.var4_prec_entry.get(),
                   'var4_divby': self.var4_divby_entry.get(),

                   'var5_min': self.var5_min_entry.get(),
                   'var5_max': self.var5_max_entry.get(),
                   'var5_prec': self.var5_prec_entry.get(),
                   'var5_divby': self.var5_divby_entry.get(),

                   'var6_min': self.var6_min_entry.get(),
                   'var6_max': self.var6_max_entry.get(),
                   'var6_prec': self.var6_prec_entry.get(),
                   'var6_divby': self.var6_divby_entry.get(),

                   'var7_min': self.var7_min_entry.get(),
                   'var7_max': self.var7_max_entry.get(),
                   'var7_prec': self.var7_prec_entry.get(),
                   'var7_divby': self.var7_divby_entry.get(),

                   'res1_min': self.res1_min_entry.get(),
                   'res1_max': self.res1_max_entry.get(),
                   'res1_prec': self.res1_prec_entry.get(),
                   'res1_tol': self.res1_tol_entry.get(),
                   'res1_points': self.res1_points_entry.get(),

                   'res2_min': self.res2_min_entry.get(),
                   'res2_max': self.res2_max_entry.get(),
                   'res2_prec': self.res2_prec_entry.get(),
                   'res2_tol': self.res2_tol_entry.get(),
                   'res2_points': self.res2_points_entry.get(),

                   'res3_min': self.res3_min_entry.get(),
                   'res3_max': self.res3_max_entry.get(),
                   'res3_prec': self.res3_prec_entry.get(),
                   'res3_tol': self.res3_tol_entry.get(),
                   'res3_points': self.res3_points_entry.get(),

                   'oid': self.record_id
                   })
     
        
     
    

        def expand_db(self):

        #self.expand_db_window = Tk()
        #self.expand_db_window.geometry('300x500')

        self.test_window = Tk()

        # Create a ScrolledFrame widget
        self.sf = ScrolledFrame(self.test_window, width=800, height=300)
        self.sf.grid()

        # Bind the arrow keys and scroll wheel
        self.sf.bind_arrow_keys(app)
        self.sf.bind_scroll_wheel(app)

        # Create a frame within the ScrolledFrame
        self.inner_frame = self.sf.display_widget(Frame)


        # CREATE FULL-LISTBOX LABELS IN NEW WINDOW
        self.title_listbox_label = Label(self.inner_frame, text="Title", width=15)
        # self.title_listbox_label.grid(row=25, column=1, sticky=W, pady=(20, 0))


        self.description_listbox_label = Label(self.inner_frame, text="Description", width=15)
        self.description_listbox_label.grid(row=25, column=2, sticky=W)

        self.formula_listbox_label = Label(self.inner_frame, text="Formula", width=15)
        self.formula_listbox_label.grid(row=25, column=3, sticky=W)

        self.var1_min_listbox_label = Label(self.inner_frame, text="var1\nmin")
        self.var1_min_listbox_label.grid(row=25, column=4, sticky=W)
        self.var1_max_listbox_label = Label(self.inner_frame, text="var1\nmax")
        self.var1_max_listbox_label.grid(row=25, column=5, sticky=W)
        self.var1_prec_listbox_label = Label(self.inner_frame, text="var1\nprec")
        self.var1_prec_listbox_label.grid(row=25, column=6, sticky=W)
        self.var1_divby_listbox_label = Label(self.inner_frame, text="var1\ndivby")
        self.var1_divby_listbox_label.grid(row=25, column=7, sticky=W)

        self.var2_min_listbox_label = Label(self.inner_frame, text="var2\nmin")
        self.var2_min_listbox_label.grid(row=25, column=8, sticky=W)
        self.var2_max_listbox_label = Label(self.inner_frame, text="var2\nmax")
        self.var2_max_listbox_label.grid(row=25, column=9, sticky=W)
        self.var2_prec_listbox_label = Label(self.inner_frame, text="var2\nprec")
        self.var2_prec_listbox_label.grid(row=25, column=10, sticky=W)
        self.var2_divby_listbox_label = Label(self.inner_frame, text="var2\ndivby")
        self.var2_divby_listbox_label.grid(row=25, column=11, sticky=W)

        self.var3_min_listbox_label = Label(self.inner_frame, text="var3\nmin")
        self.var3_min_listbox_label.grid(row=25, column=12, sticky=W)
        self.var3_max_listbox_label = Label(self.inner_frame, text="var3\nmax")
        self.var3_max_listbox_label.grid(row=25, column=13, sticky=W)
        self.var3_prec_listbox_label = Label(self.inner_frame, text="var3\nprec")
        self.var3_prec_listbox_label.grid(row=25, column=14, sticky=W)
        self.var3_divby_listbox_label = Label(self.inner_frame, text="var3\ntol")
        self.var3_divby_listbox_label.grid(row=25, column=15, sticky=W)

        self.var4_min_listbox_label = Label(self.inner_frame, text="var4\nmin")
        self.var4_min_listbox_label.grid(row=25, column=16, sticky=W)
        self.var4_max_listbox_label = Label(self.inner_frame, text="var4\nmax")
        self.var4_max_listbox_label.grid(row=25, column=17, sticky=W)
        self.var4_prec_listbox_label = Label(self.inner_frame, text="var4\nprec")
        self.var4_prec_listbox_label.grid(row=25, column=18, sticky=W)
        self.var4_divby_listbox_label = Label(self.inner_frame, text="var4\ntol")
        self.var4_divby_listbox_label.grid(row=25, column=19, sticky=W)

        self.var5_min_listbox_label = Label(self.inner_frame, text="var5\nmin")
        self.var5_min_listbox_label.grid(row=25, column=20, sticky=W)
        self.var5_max_listbox_label = Label(self.inner_frame, text="var5\nmax")
        self.var5_max_listbox_label.grid(row=25, column=21, sticky=W)
        self.var5_prec_listbox_label = Label(self.inner_frame, text="var5\nprec")
        self.var5_prec_listbox_label.grid(row=25, column=22, sticky=W)
        self.var5_divby_listbox_label = Label(self.inner_frame, text="var5\ntol")
        self.var5_divby_listbox_label.grid(row=25, column=23, sticky=W)

        self.var6_min_listbox_label = Label(self.inner_frame, text="var6\nmin")
        self.var6_min_listbox_label.grid(row=25, column=24, sticky=W)
        self.var6_max_listbox_label = Label(self.inner_frame, text="var6\nmax")
        self.var6_max_listbox_label.grid(row=25, column=25, sticky=W)
        self.var6_prec_listbox_label = Label(self.inner_frame, text="var6\nprec")
        self.var6_prec_listbox_label.grid(row=25, column=26, sticky=W)
        self.var6_divby_listbox_label = Label(self.inner_frame, text="var6\ntol")
        self.var6_divby_listbox_label.grid(row=25, column=27, sticky=W)

        self.var7_min_listbox_label = Label(self.inner_frame, text="var7\nmin")
        self.var7_min_listbox_label.grid(row=25, column=28, sticky=W)
        self.var7_max_listbox_label = Label(self.inner_frame, text="var7\nmax")
        self.var7_max_listbox_label.grid(row=25, column=29, sticky=W)
        self.var7_prec_listbox_label = Label(self.inner_frame, text="var7\nprec")
        self.var7_prec_listbox_label.grid(row=25, column=30, sticky=W)
        self.var7_divby_listbox_label = Label(self.inner_frame, text="var7\ntol")
        self.var7_divby_listbox_label.grid(row=25, column=31, sticky=W)

        self.res1_min_listbox_label = Label(self.inner_frame, text="res1\nmin")
        self.res1_min_listbox_label.grid(row=25, column=32, sticky=W)
        self.res1_max_listbox_label = Label(self.inner_frame, text="res1\nmax")
        self.res1_max_listbox_label.grid(row=25, column=33, sticky=W)
        self.res1_prec_listbox_label = Label(self.inner_frame, text="res1\nprec")
        self.res1_prec_listbox_label.grid(row=25, column=34, sticky=W)
        self.res1_tol_listbox_label = Label(self.inner_frame, text="res1\ntol")
        self.res1_tol_listbox_label.grid(row=25, column=35, sticky=W)
        self.res1_points_listbox_label = Label(self.inner_frame, text="res1\npts")
        self.res1_points_listbox_label.grid(row=25, column=36, sticky=W)

        self.res2_min_listbox_label = Label(self.inner_frame, text="res2\nmin")
        self.res2_min_listbox_label.grid(row=25, column=37, sticky=W)
        self.res2_max_listbox_label = Label(self.inner_frame, text="res2\nmax")
        self.res2_max_listbox_label.grid(row=25, column=38, sticky=W)
        self.res2_prec_listbox_label = Label(self.inner_frame, text="res2\nprec")
        self.res2_prec_listbox_label.grid(row=25, column=39, sticky=W)
        self.res2_tol_listbox_label = Label(self.inner_frame, text="res2\ntol")
        self.res2_tol_listbox_label.grid(row=25, column=40, sticky=W)
        self.res2_points_listbox_label = Label(self.inner_frame, text="res2\npts")
        self.res2_points_listbox_label.grid(row=25, column=41, sticky=W)

        self.res3_min_listbox_label = Label(self.inner_frame, text="res3\nmin")
        self.res3_min_listbox_label.grid(row=25, column=42, sticky=W)
        self.res3_max_listbox_label = Label(self.inner_frame, text="res3\nmax")
        self.res3_max_listbox_label.grid(row=25, column=43, sticky=W)
        self.res3_prec_listbox_label = Label(self.inner_frame, text="res3\nprec")
        self.res3_prec_listbox_label.grid(row=25, column=44, sticky=W)
        self.res3_tol_listbox_label = Label(self.inner_frame, text="res3\ntol")
        self.res3_tol_listbox_label.grid(row=25, column=45, sticky=W)
        self.res3_points_listbox_label = Label(self.inner_frame, text="res3\npts")
        self.res3_points_listbox_label.grid(row=25, column=46, sticky=W)

        self.img_name_listbox_label = Label(self.inner_frame, text=" img\n name")
        self.img_name_listbox_label.grid(row=25, column=47, sticky=W)

        self.img_data_label = Label(self.inner_frame, text=" img\n data")
        self.img_data_label.grid(row=25, column=48, sticky=W)

        self.oid_listbox_label = Label(self.inner_frame, text=" oid")
        self.oid_listbox_label.grid(row=25, column=49, sticky=W)

        # CREATE FULL-LISTBOX ENTRYS IN NEW WINDOW

        self.my_listbox_title = Listbox(self.inner_frame, width=15)
        self.my_listbox_title.grid(row=30, column=1, sticky=W, pady=20)
        self.my_listbox_description = Listbox(self.inner_frame, width=15)
        self.my_listbox_description.grid(row=30, column=2, sticky=W)
        self.my_listbox_formula = Listbox(self.inner_frame, width=15)
        self.my_listbox_formula.grid(row=30, column=3, sticky=W)

        self.my_listbox_var1_min = Listbox(self.inner_frame, width=5)
        self.my_listbox_var1_min.grid(row=30, column=4, sticky=W)
        self.my_listbox_var1_max = Listbox(self.inner_frame, width=5)
        self.my_listbox_var1_max.grid(row=30, column=5, sticky=W)
        self.my_listbox_var1_prec = Listbox(self.inner_frame, width=5)
        self.my_listbox_var1_prec.grid(row=30, column=6, sticky=W)
        self.my_listbox_var1_divby = Listbox(self.inner_frame, width=5)
        self.my_listbox_var1_divby.grid(row=30, column=7, sticky=W)

        self.my_listbox_var2_min = Listbox(self.inner_frame, width=5)
        self.my_listbox_var2_min.grid(row=30, column=8, sticky=W)
        self.my_listbox_var2_max = Listbox(self.inner_frame, width=5)
        self.my_listbox_var2_max.grid(row=30, column=9, sticky=W)
        self.my_listbox_var2_prec = Listbox(self.inner_frame, width=5)
        self.my_listbox_var2_prec.grid(row=30, column=10, sticky=W)
        self.my_listbox_var2_divby = Listbox(self.inner_frame, width=5)
        self.my_listbox_var2_divby.grid(row=30, column=11, sticky=W)

        self.my_listbox_var3_min = Listbox(self.inner_frame, width=5)
        self.my_listbox_var3_min.grid(row=30, column=12, sticky=W)
        self.my_listbox_var3_max = Listbox(self.inner_frame, width=5)
        self.my_listbox_var3_max.grid(row=30, column=13, sticky=W)
        self.my_listbox_var3_prec = Listbox(self.inner_frame, width=5)
        self.my_listbox_var3_prec.grid(row=30, column=14, sticky=W)
        self.my_listbox_var3_divby = Listbox(self.inner_frame, width=5)
        self.my_listbox_var3_divby.grid(row=30, column=15, sticky=W)

        self.my_listbox_var4_min = Listbox(self.inner_frame, width=5)
        self.my_listbox_var4_min.grid(row=30, column=16, sticky=W)
        self.my_listbox_var4_max = Listbox(self.inner_frame, width=5)
        self.my_listbox_var4_max.grid(row=30, column=17, sticky=W)
        self.my_listbox_var4_prec = Listbox(self.inner_frame, width=5)
        self.my_listbox_var4_prec.grid(row=30, column=18, sticky=W)
        self.my_listbox_var4_divby = Listbox(self.inner_frame, width=5)
        self.my_listbox_var4_divby.grid(row=30, column=19, sticky=W)

        self.my_listbox_var5_min = Listbox(self.inner_frame, width=5)
        self.my_listbox_var5_min.grid(row=30, column=20, sticky=W)
        self.my_listbox_var5_max = Listbox(self.inner_frame, width=5)
        self.my_listbox_var5_max.grid(row=30, column=21, sticky=W)
        self.my_listbox_var5_prec = Listbox(self.inner_frame, width=5)
        self.my_listbox_var5_prec.grid(row=30, column=22, sticky=W)
        self.my_listbox_var5_divby = Listbox(self.inner_frame, width=5)
        self.my_listbox_var5_divby.grid(row=30, column=23, sticky=W)

        self.my_listbox_var6_min = Listbox(self.inner_frame, width=5)
        self.my_listbox_var6_min.grid(row=30, column=24, sticky=W)
        self.my_listbox_var6_max = Listbox(self.inner_frame, width=5)
        self.my_listbox_var6_max.grid(row=30, column=25, sticky=W)
        self.my_listbox_var6_prec = Listbox(self.inner_frame, width=5)
        self.my_listbox_var6_prec.grid(row=30, column=26, sticky=W)
        self.my_listbox_var6_divby = Listbox(self.inner_frame, width=5)
        self.my_listbox_var6_divby.grid(row=30, column=27, sticky=W)

        self.my_listbox_var7_min = Listbox(self.inner_frame, width=5)
        self.my_listbox_var7_min.grid(row=30, column=28, sticky=W)
        self.my_listbox_var7_max = Listbox(self.inner_frame, width=5)
        self.my_listbox_var7_max.grid(row=30, column=29, sticky=W)
        self.my_listbox_var7_prec = Listbox(self.inner_frame, width=5)
        self.my_listbox_var7_prec.grid(row=30, column=30, sticky=W)
        self.my_listbox_var7_divby = Listbox(self.inner_frame, width=5)
        self.my_listbox_var7_divby.grid(row=30, column=31, sticky=W)

        self.my_listbox_res1_min = Listbox(self.inner_frame, width=5)
        self.my_listbox_res1_min.grid(row=30, column=32, sticky=W)
        self.my_listbox_res1_max = Listbox(self.inner_frame, width=5)
        self.my_listbox_res1_max.grid(row=30, column=33, sticky=W)
        self.my_listbox_res1_prec = Listbox(self.inner_frame, width=5)
        self.my_listbox_res1_prec.grid(row=30, column=34, sticky=W)
        self.my_listbox_res1_tol = Listbox(self.inner_frame, width=5)
        self.my_listbox_res1_tol.grid(row=30, column=35, sticky=W)
        self.my_listbox_res1_points = Listbox(self.inner_frame, width=5)
        self.my_listbox_res1_points.grid(row=30, column=36, sticky=W)

        self.my_listbox_res2_min = Listbox(self.inner_frame, width=5)
        self.my_listbox_res2_min.grid(row=30, column=37, sticky=W)
        self.my_listbox_res2_max = Listbox(self.inner_frame, width=5)
        self.my_listbox_res2_max.grid(row=30, column=38, sticky=W)
        self.my_listbox_res2_prec = Listbox(self.inner_frame, width=5)
        self.my_listbox_res2_prec.grid(row=30, column=39, sticky=W)
        self.my_listbox_res2_tol = Listbox(self.inner_frame, width=5)
        self.my_listbox_res2_tol.grid(row=30, column=40, sticky=W)
        self.my_listbox_res2_points = Listbox(self.inner_frame, width=5)
        self.my_listbox_res2_points.grid(row=30, column=41, sticky=W)

        self.my_listbox_res3_min = Listbox(self.inner_frame, width=5)
        self.my_listbox_res3_min.grid(row=30, column=42, sticky=W)
        self.my_listbox_res3_max = Listbox(self.inner_frame, width=5)
        self.my_listbox_res3_max.grid(row=30, column=43, sticky=W)
        self.my_listbox_res3_prec = Listbox(self.inner_frame, width=5)
        self.my_listbox_res3_prec.grid(row=30, column=44, sticky=W)
        self.my_listbox_res3_tol = Listbox(self.inner_frame, width=5)
        self.my_listbox_res3_tol.grid(row=30, column=45, sticky=W)
        self.my_listbox_res3_points = Listbox(self.inner_frame, width=5)
        self.my_listbox_res3_points.grid(row=30, column=46, sticky=W)

        self.my_listbox_img_name = Listbox(self.inner_frame, width=5)
        self.my_listbox_img_name.grid(row=30, column=47, sticky=W)

        self.my_listbox_img_data = Listbox(self.inner_frame, width=5)
        self.my_listbox_img_data.grid(row=30, column=48, sticky=W)

        self.my_listbox_oid = Listbox(self.inner_frame, width=5)
        self.my_listbox_oid.grid(row=30, column=49, sticky=W)




        conn = sqlite3.connect('ilias_questions_db.db')
        c = conn.cursor()

        c.execute("SELECT *, oid FROM my_table")
        records = c.fetchall()

        # Clear List Boxes
        self.my_listbox_formula.delete(0, END)
        self.my_listbox_var1_min.delete(0, END)
        self.my_listbox_var1_max.delete(0, END)
        self.my_listbox_var1_prec.delete(0, END)
        self.my_listbox_var1_divby.delete(0, END)
        self.my_listbox_var2_min.delete(0, END)
        self.my_listbox_var2_max.delete(0, END)
        self.my_listbox_var2_prec.delete(0, END)
        self.my_listbox_var2_divby.delete(0, END)
        self.my_listbox_var3_min.delete(0, END)
        self.my_listbox_var3_max.delete(0, END)
        self.my_listbox_var3_prec.delete(0, END)
        self.my_listbox_var3_divby.delete(0, END)
        self.my_listbox_res1_min.delete(0, END)
        self.my_listbox_res1_max.delete(0, END)
        self.my_listbox_res1_prec.delete(0, END)
        self.my_listbox_res1_tol.delete(0, END)
        self.my_listbox_res1_points.delete(0, END)
        self.my_listbox_oid.delete(0, END)

        # Loop thru Results
        for record in records:
            self.my_listbox_formula.insert(END, record[0])
            self.my_listbox_var1_min.insert(END, record[1])
            self.my_listbox_var1_max.insert(END, record[2])
            self.my_listbox_var1_prec.insert(END, record[3])
            self.my_listbox_var1_divby.insert(END, record[4])
            self.my_listbox_var2_min.insert(END, record[5])
            self.my_listbox_var2_max.insert(END, record[6])
            self.my_listbox_var2_prec.insert(END, record[7])
            self.my_listbox_var2_divby.insert(END, record[8])
            self.my_listbox_var3_min.insert(END, record[9])
            self.my_listbox_var3_max.insert(END, record[10])
            self.my_listbox_var3_prec.insert(END, record[11])
            self.my_listbox_var3_divby.insert(END, record[12])
            self.my_listbox_res1_min.insert(END, record[13])
            self.my_listbox_res1_max.insert(END, record[14])
            self.my_listbox_res1_prec.insert(END, record[15])
            self.my_listbox_res1_tol.insert(END, record[16])
            self.my_listbox_res1_points.insert(END, record[17])
            self.my_listbox_oid.insert(END, record[18])

            print(record)
        conn.commit()
        conn.close()





    """