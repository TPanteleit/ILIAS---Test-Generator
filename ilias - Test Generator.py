import Pmw
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
from tkinter import ttk
import sqlite3
import xml.etree.ElementTree as ET
from sympy import *
from tkscrolledframe import ScrolledFrame
import os
import datetime
import pathlib


# -- Git Hub TEst

class GuiMainWindow:

    def __init__(self, master):
        self.master = master
        master.geometry = '800x710'
        master.title('ilias - Test-Generator v1.1')

        # --------------------------    Set PATH for Project

        # print(pathlib.Path().absolute())    Pfad zur Datei die ausgeführt wird
        self.project_root_path = str(pathlib.Path().absolute())
        self.img_file_path_create_folder = str(pathlib.Path().absolute()) + "1590475954__0__tst_1944463/objects/"

        # --------------------------    Static PATHs for Project
        # "orig"_tst and _qti files are empty file templates.
        #
        self.tst_file_path_read = self.project_root_path + r"\orig_qti_tst_files\orig_1590475954__0__tst_1944463.xml"
        self.qti_file_path_read = self.project_root_path + r"\orig_qti_tst_files\orig_1590475954__0__qti_1944463.xml"

        self.tst_file_path_write = self.project_root_path + r"\1590475954__0__tst_1944463\1590475954__0__tst_1944463.xml"
        self.qti_file_path_write = self.project_root_path + r"\1590475954__0__tst_1944463\1590475954__0__qti_1944463.xml"


        self.img_file_path = self.project_root_path + r"\1590475954__0__tst_1944463\objects"

        # --------------------------   Set size of windows
        # Main-window
        self.formula_width = 800
        self.formula_height = 800

        # Main-window
        self.multiplechoice_width = 800
        self.multiplechoice_height = 800

        # Database-window
        self.database_width = 800
        self.database_height = 800

        # Settings-window
        self.settings_width = 800
        self.settings_height = 800



        # <------------ Define Tab Control for different QUestion-Tabs ----------->

        self.tabControl = ttk.Notebook(app)  # Create Tab Control


        # ---- Tab for Formula - Questions
        self.formula_tab_ttk = ttk.Frame(self.tabControl)  # Create a tab
        self.tabControl.add(self.formula_tab_ttk, text='Formelfrage')  # Add the tab

        # Create a ScrolledFrame widget
        self.sf_formula = ScrolledFrame(self.formula_tab_ttk, width=self.formula_width, height=self.formula_height)
        self.sf_formula.pack(expand=1, fill="both")

        # Bind the arrow keys and scroll wheel
        self.sf_formula.bind_arrow_keys(app)
        self.sf_formula.bind_scroll_wheel(app)

        # Create a frame within the ScrolledFrame
        self.formula_tab = self.sf_formula.display_widget(Frame)


        # ---- Tab for Single Choice - Questions
        self.singleChoice_tab = ttk.Frame(self.tabControl)  # Create a tab
        self.tabControl.add(self.singleChoice_tab, text='Single Choice')  # Add the tab


        # ---- Tab for Multiple Choice - Questions
        self.mc_tab_ttk = ttk.Frame(self.tabControl)  # Create a tab
        self.tabControl.add(self.mc_tab_ttk, text='Multiple Choice')  # Add the tab

        # Create a ScrolledFrame widget
        self.sf_mc = ScrolledFrame(self.mc_tab_ttk, width=self.multiplechoice_width, height=self.multiplechoice_height)
        self.sf_mc.pack(expand=1, fill="both")

        # Bind the arrow keys and scroll wheel
        self.sf_mc.bind_arrow_keys(app)
        self.sf_mc.bind_scroll_wheel(app)

        # Create a frame within the ScrolledFrame
        self.multipleChoice_tab = self.sf_mc.display_widget(Frame)


        #self.tabControl.grid()  # Pack to make visible
        self.tabControl.pack(expand=1, fill="both")

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

        self.frame_latex_preview = LabelFrame(self.formula_tab, text="LaTeX Preview", padx=5, pady=5)
        self.frame_latex_preview.grid(row=9, column=0, padx=10, pady=10, sticky="NW")

        self.frame_question_difficulty = LabelFrame(self.formula_tab, text="Difficulty", padx=5, pady=5)
        self.frame_question_difficulty.grid(row=9, column=0, padx=170, pady=10, sticky="NW")

        self.frame_question_category = LabelFrame(self.formula_tab, text="Category", padx=5, pady=5)
        self.frame_question_category.grid(row=9, column=0, padx=10, pady=10, sticky="NE")

        self.frame_question_type = LabelFrame(self.formula_tab, text="Type", padx=5, pady=5)
        self.frame_question_type.grid(row=9, column=1, padx=10, pady=10, sticky="NW")

        # ----------------------------------------------------------  CREATING FRAMES FOR MultipleChoice TAB
        self.frame_mc_latex_preview = LabelFrame(self.multipleChoice_tab, text="MC: LaTeX Preview", padx=5, pady=5)
        self.frame_mc_latex_preview.grid(row=9, column=0, padx=10, pady=10, sticky="NW")

        self.frame_mc_question_difficulty = LabelFrame(self.multipleChoice_tab, text="MC: Difficulty", padx=5, pady=5)
        self.frame_mc_question_difficulty.grid(row=9, column=0, padx=170, pady=10, sticky="NW")

        self.frame_mc_question_category = LabelFrame(self.multipleChoice_tab, text="MC: Category", padx=5, pady=5)
        self.frame_mc_question_category.grid(row=9, column=0, padx=10, pady=10, sticky="NE")

        self.frame_mc_question_type = LabelFrame(self.multipleChoice_tab, text="MC: Type", padx=5, pady=5)
        self.frame_mc_question_type.grid(row=9, column=1, padx=10, pady=10, sticky="NW")

        self.frame_mc_database = LabelFrame(self.multipleChoice_tab, text="Datenbank", padx=5, pady=5)
        self.frame_mc_database.grid(row=10, column=0, padx=10, pady=10, sticky=NW)

        # ----------------------------------------------------------  CREATE SINGLE QUESTION WITH FROM OID
        self.create_formelfrage_btn = Button(self.frame_create_formelfrage, text="Get oid and create", command=lambda: create_formelfrage.__init__(self))
        self.create_formelfrage_btn.grid(row=0, column=0, sticky=W)

        self.create_multiplechoice_btn = Button(self.frame_create_formelfrage, text="mc create", command=lambda: create_multiplechoice.__init__(self))
        #self.create_multiplechoice_btn.grid(row=1, column=0, sticky=W)


        self.create_formelfrage_entry = Entry(self.frame_create_formelfrage, width=15)
        self.create_formelfrage_entry.grid(row=0, column=1, sticky=W, padx=20)

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

        self.database_show_records_btn = Button(self.frame_database, text="Show Records",command=lambda: Database.show_records(self))
        self.database_show_records_btn.grid(row=1, column=0, sticky=W, pady=5)

        self.database_submit_formelfrage_btn = Button(self.frame_database, text="Submit", command=lambda: Database.submit(self))
        self.database_submit_formelfrage_btn.grid(row=2, column=0, sticky=W, pady=5)

        self.database_delete_btn = Button(self.frame_database, text="Delete", command=lambda: Database.delete(self))
        self.database_delete_btn.grid(row=3, column=0, sticky=W, pady=5)

        self.delete_box = Entry(self.frame_database, width=5)
        self.delete_box.grid(row=3, column=1, sticky=W)

        self.database_load_btn = Button(self.frame_database, text="Load", command=lambda: Database.load(self))
        self.database_load_btn.grid(row=4, column=0, sticky=W, pady=5)

        self.load_box = Entry(self.frame_database, width=5)
        self.load_box.grid(row=4, column=1, sticky=W)

        # still working?
        #self.show_test_settings_formula_tab = Button(self.formula_tab, text="Test-Einstellungen",command=lambda: GUI_settings_window.__init__(self.formula_tab))
        self.show_test_settings_formula_tab = Button(self.formula_tab, text="Test-Einstellungen",command=lambda: GUI_settings_window.__init__(self))
        self.show_test_settings_formula_tab.grid(row=4, column=0)

        self.img_select_btn = Button(self.frame_picture, text="Add Image", command=lambda: Database.open_image(self))
        self.img_select_btn.grid(row=2, column=0, sticky=W)

        self.img_remove_btn = Button(self.frame_picture, text="Remove Image", command=lambda: Database.delete_image(self))
        self.img_remove_btn.grid(row=2, column=1, sticky=W)

        self.show_img_from_db_btn = Button(self.frame_db_picture, text="IMG from DB",command=lambda: Database.show_img_from_db(self))
        self.show_img_from_db_btn.grid(row=2, column=3, sticky=W)

        self.myLatex_btn = Button(self.frame_latex_preview, text="LaTeX Preview", command=lambda:LatexPreview.__init__(self) )
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

        self.question_type_entry = Entry(self.frame_question_type, width=15)
        self.question_type_entry.grid(row=0, column=1, pady=5, padx=5)
        self.question_type_entry.insert(0, "Formelfrage")

        self.btn = Button(self.frame_latex_preview, text="add latex-term", command=lambda: Formelfrage.add_term(self))
        self.btn.grid()

        self.picture_name = "EMPTY"


        # ----------------------------- CREATING BUTTONS FOR MultipleChoice TAB
        self.mc_myLatex_btn = Button(self.frame_mc_latex_preview, text="LaTeX Preview", command=lambda: LatexPreview.__init__(self))
        self.mc_myLatex_btn.grid(row=0, column=0, sticky=W)

        self.mc_question_difficulty_label = Label(self.frame_mc_question_difficulty, text="Schwierigkeitsgrad der Frage")
        self.mc_question_difficulty_label.grid(row=0, column=0, pady=5, padx=5)

        self.mc_question_difficulty_entry = Entry(self.frame_mc_question_difficulty, width=10)
        self.mc_question_difficulty_entry.grid(row=0, column=1, pady=5, padx=5)

        self.mc_question_category_label = Label(self.frame_mc_question_category, text="Fragenkategorie")
        self.mc_question_category_label.grid(row=0, column=0, pady=5, padx=5)

        self.mc_question_category_entry = Entry(self.frame_mc_question_category, width=15)
        self.mc_question_category_entry.grid(row=0, column=1, pady=5, padx=5)

        self.mc_question_type_label = Label(self.frame_mc_question_type, text="Fragen-Typ")
        self.mc_question_type_label.grid(row=0, column=0, pady=5, padx=5)

        self.mc_question_type_entry = Entry(self.frame_mc_question_type, width=15)
        self.mc_question_type_entry.grid(row=0, column=1, pady=5, padx=5)
        self.mc_question_type_entry.insert(0, "Multiple Choice")

        self.database_submit_multiplechoice_btn = Button(self.frame_mc_database, text="Submit MC", command=lambda: MultipleChoice.submit_mc(self))
        self.database_submit_multiplechoice_btn.grid(row=2, column=0, sticky=W, pady=5)

        self.database_load_multiplechoice_btn = Button(self.frame_mc_database, text="Load MC", command=lambda: Database.load(self))
        self.database_load_multiplechoice_btn.grid(row=4, column=0, sticky=W, pady=5)

        self.load_multiplechoice_box = Entry(self.frame_mc_database, width=5)
        self.load_multiplechoice_box.grid(row=4, column=1, sticky=W)


        # ---Init Variable Matrix
        Formelfrage.__init__(self)
        MultipleChoice.__init__(self)

    # ---Init MC-TAB
    # MultipleChoice.__init__(self, self.multipleChoice_tab)

    # ---Init MC-TAB
    # SingleChoice.__init__(self, self.singleChoice_tab)




    #create table / Database
    def create_Database(self):
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
                var1_unit text,
                var2_name text,
                var2_min int,
                var2_max int,
                var2_prec int,
                var2_divby int,
                var2_unit text,
                var3_name text,
                var3_min int,
                var3_max int,
                var3_prec int,
                var3_divby int,
                var3_unit text,
                var4_name text,
                var4_min int,
                var4_max int,
                var4_prec int,
                var4_divby int,
                var4_unit text,
                var5_name text,
                var5_min int,
                var5_max int,
                var5_prec int,
                var5_divby int,
                var5_unit text,
                var6_name text,
                var6_min int,
                var6_max int,
                var6_prec int,
                var6_divby int,
                var6_unit text,
                var7_name text,
                var7_min int,
                var7_max int,
                var7_prec int,
                var7_divby int,
                var7_unit text,
                res1_name text,
                res1_min int,
                res1_max int,
                res1_prec int,
                res1_tol int,
                res1_points int,
                res1_unit text,
                res2_name text,
                res2_min int,
                res2_max int,
                res2_prec int,
                res2_tol int,
                res2_points int,
                res2_unit text,
                res3_name text,
                res3_min int,
                res3_max int,
                res3_prec int,
                res3_tol int,
                res3_points int,
                res3_unit text,
                img_name text,
                img_data blop,
                test_time text
                )""")

        # Commit Changes
        conn.commit()

        # Close Connection
        conn.close()


    def create_Profiles_Database(self):
        print("PROFILE DATABASE CREATED!")
        # Create a database or connect to one
        conn = sqlite3.connect('test_settings_profiles_db.db')

        # Create cursor
        c = conn.cursor()

        # Create table
        c.execute("""CREATE TABLE IF NOT EXISTS my_profiles_table (
               
                profile_name TEXT,
                entry_description TEXT,
                radio_select_question INT,
                radio_select_anonymous INT,
                check_online INT,
                check_time_limited INT,
                
                check_introduction INT,
                entry_introduction TEXT,
                check_test_properties INT,
                
                entry_test_start_year TEXT,
                entry_test_start_month TEXT,
                entry_test_start_day TEXT,
                entry_test_start_hour TEXT,
                entry_test_start_minute TEXT,
                
                entry_test_end_year TEXT,
                entry_test_end_month TEXT,
                entry_test_end_day TEXT,
                entry_test_end_hour TEXT,
                entry_test_end_minute TEXT,
                
                entry_test_password TEXT,
                check_specific_users INT,
                entry_limit_users TEXT,
                entry_user_inactivity TEXT,
                entry_limit_test_runs TEXT,
                
                entry_limit_time_betw_test_run_month TEXT,
                entry_limit_time_betw_test_run_day TEXT,
                entry_limit_time_betw_test_run_hour TEXT,
                entry_limit_time_betw_test_run_minute TEXT,
                
                check_processing_time INT,
                entry_processing_time_in_minutes TEXT,
                check_processing_time_reset INT,
                
                check_examview INT,
                check_examview_titel INT,
                check_examview_username INT,
                check_show_ilias_nr INT,
               
                radio_select_show_question_title INT,
                check_autosave INT,
                entry_autosave_interval TEXT,
                check_mix_questions INT,
                check_show_solution_notes INT,
                check_direct_response INT,
                
                radio_select_user_response INT,
                check_mandatory_questions INT,
                check_use_previous_solution INT,
                check_show_test_cancel INT,
                radio_select_not_answered_questions INT,
                
                check_show_question_list_process_status INT,
                check_question_mark INT,
                check_overview_answers INT,
                check_show_end_comment INT,
                entry_end_comment TEXT,
                check_forwarding INT,
                check_notification INT
                
                )""")

        # Commit Changes
        conn.commit()

        # Close Connection
        conn.close()










class Formelfrage(GuiMainWindow):

    def __init__(self):


        #----- Create Databases --- only need to create Databse once
        #self.create_Database()
        #self.create_Profiles_Database()

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
        self.formula_question_entry = Text(self.frame_formula, height=6, width=65, font=('Helvetica', 9))
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
        self.var1_min_entry = Entry(self.frame_formula, textvariable=self.var1_min_text, width=6)
        self.var1_max_entry = Entry(self.frame_formula, textvariable=self.var1_max_text, width=6)
        self.var1_prec_entry = Entry(self.frame_formula, textvariable=self.var1_prec_text, width=6)
        self.var1_divby_entry = Entry(self.frame_formula, textvariable=self.var1_divby_text, width=6)

        self.var2_name_entry = Entry(self.frame_formula, textvariable=self.var2_name_text, width=6)
        self.var2_min_entry = Entry(self.frame_formula, textvariable=self.var2_min_text, width=6)
        self.var2_max_entry = Entry(self.frame_formula, textvariable=self.var2_max_text, width=6)
        self.var2_prec_entry = Entry(self.frame_formula, textvariable=self.var2_prec_text, width=6)
        self.var2_divby_entry = Entry(self.frame_formula, textvariable=self.var2_divby_text, width=6)

        self.var3_name_entry = Entry(self.frame_formula, textvariable=self.var3_name_text, width=6)
        self.var3_min_entry = Entry(self.frame_formula, textvariable=self.var3_min_text, width=6)
        self.var3_max_entry = Entry(self.frame_formula, textvariable=self.var3_max_text, width=6)
        self.var3_prec_entry = Entry(self.frame_formula, textvariable=self.var3_prec_text, width=6)
        self.var3_divby_entry = Entry(self.frame_formula, textvariable=self.var3_divby_text, width=6)

        self.var4_name_entry = Entry(self.frame_formula, textvariable=self.var4_name_text, width=6)
        self.var4_min_entry = Entry(self.frame_formula, textvariable=self.var4_min_text, width=6)
        self.var4_max_entry = Entry(self.frame_formula, textvariable=self.var4_max_text, width=6)
        self.var4_prec_entry = Entry(self.frame_formula, textvariable=self.var4_prec_text, width=6)
        self.var4_divby_entry = Entry(self.frame_formula, textvariable=self.var4_divby_text, width=6)

        self.var5_name_entry = Entry(self.frame_formula, textvariable=self.var5_name_text, width=6)
        self.var5_min_entry = Entry(self.frame_formula, textvariable=self.var5_min_text, width=6)
        self.var5_max_entry = Entry(self.frame_formula, textvariable=self.var5_max_text, width=6)
        self.var5_prec_entry = Entry(self.frame_formula, textvariable=self.var5_prec_text, width=6)
        self.var5_divby_entry = Entry(self.frame_formula, textvariable=self.var5_divby_text, width=6)

        self.var6_name_entry = Entry(self.frame_formula, textvariable=self.var6_name_text, width=6)
        self.var6_min_entry = Entry(self.frame_formula, textvariable=self.var6_min_text, width=6)
        self.var6_max_entry = Entry(self.frame_formula, textvariable=self.var6_max_text, width=6)
        self.var6_prec_entry = Entry(self.frame_formula, textvariable=self.var6_prec_text, width=6)
        self.var6_divby_entry = Entry(self.frame_formula, textvariable=self.var6_divby_text, width=6)

        self.var7_name_entry = Entry(self.frame_formula, textvariable=self.var7_name_text, width=6)
        self.var7_min_entry = Entry(self.frame_formula, textvariable=self.var7_min_text, width=6)
        self.var7_max_entry = Entry(self.frame_formula, textvariable=self.var7_max_text, width=6)
        self.var7_prec_entry = Entry(self.frame_formula, textvariable=self.var7_prec_text, width=6)
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

        ###########################  ADD VARIABLE - UNITS ##############################

        self.select_var_units = ["Unit", "H", "mH", "µH", "nH", "pH", "---", "F", "mF", "µF", "nF", "pF", "---", "MV", "kV", "V", "mV", "µV", "---"]

        self.var1_unit_myCombo = ttk.Combobox(self.frame_formula, value=self.select_var_units, width=5)
        self.var1_unit_myCombo.current(0)
        self.var1_unit_myCombo.grid(row=6, column=0, sticky=E, padx=10)

        self.var2_unit_myCombo = ttk.Combobox(self.frame_formula, value=self.select_var_units, width=5)
        self.var2_unit_myCombo.current(0)

        self.var3_unit_myCombo = ttk.Combobox(self.frame_formula, value=self.select_var_units, width=5)
        self.var3_unit_myCombo.current(0)

        self.var4_unit_myCombo = ttk.Combobox(self.frame_formula, value=self.select_var_units, width=5)
        self.var4_unit_myCombo.current(0)

        self.var5_unit_myCombo = ttk.Combobox(self.frame_formula, value=self.select_var_units, width=5)
        self.var5_unit_myCombo.current(0)

        self.var6_unit_myCombo = ttk.Combobox(self.frame_formula, value=self.select_var_units, width=5)
        self.var6_unit_myCombo.current(0)

        self.var7_unit_myCombo = ttk.Combobox(self.frame_formula, value=self.select_var_units, width=5)
        self.var7_unit_myCombo.current(0)





        ################################################################################

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
            self.var2_unit_myCombo.grid(row=7, column=0, sticky=E, padx=10)

        # -----------------------Place Label & Entry-Boxes for Variable 3 on GUI
        def var3_show():
            self.variable3_label.grid(row=8, column=0, sticky=W, padx=20)
            self.var3_name_entry.grid(row=8, column=1, sticky=W)
            self.var3_min_entry.grid(row=8, column=1, sticky=W, padx=60)
            self.var3_max_entry.grid(row=8, column=1, sticky=W, padx=100)
            self.var3_prec_entry.grid(row=8, column=1, sticky=W, padx=140)
            self.var3_divby_entry.grid(row=8, column=1, sticky=W, padx=180)
            self.var3_unit_myCombo.grid(row=8, column=0, sticky=E, padx=10)

        # -----------------------Place Label & Entry-Boxes for Variable 4 on GUI
        def var4_show():
            self.variable4_label.grid(row=9, column=0, sticky=W, padx=20)
            self.var4_name_entry.grid(row=9, column=1, sticky=W)
            self.var4_min_entry.grid(row=9, column=1, sticky=W, padx=60)
            self.var4_max_entry.grid(row=9, column=1, sticky=W, padx=100)
            self.var4_prec_entry.grid(row=9, column=1, sticky=W, padx=140)
            self.var4_divby_entry.grid(row=9, column=1, sticky=W, padx=180)
            self.var4_unit_myCombo.grid(row=9, column=0, sticky=E, padx=10)

        # -----------------------Place Label & Entry-Boxes for Variable 5 on GUI
        def var5_show():
            self.variable5_label.grid(row=10, column=0, sticky=W, padx=20)
            self.var5_name_entry.grid(row=10, column=1, sticky=W)
            self.var5_min_entry.grid(row=10, column=1, sticky=W, padx=60)
            self.var5_max_entry.grid(row=10, column=1, sticky=W, padx=100)
            self.var5_prec_entry.grid(row=10, column=1, sticky=W, padx=140)
            self.var5_divby_entry.grid(row=10, column=1, sticky=W, padx=180)
            self.var5_unit_myCombo.grid(row=10, column=0, sticky=E, padx=10)

        # -----------------------Place Label & Entry-Boxes for Variable 6 on GUI
        def var6_show():
            self.variable6_label.grid(row=11, column=0, sticky=W, padx=20)
            self.var6_name_entry.grid(row=11, column=1, sticky=W)
            self.var6_min_entry.grid(row=11, column=1, sticky=W, padx=60)
            self.var6_max_entry.grid(row=11, column=1, sticky=W, padx=100)
            self.var6_prec_entry.grid(row=11, column=1, sticky=W, padx=140)
            self.var6_divby_entry.grid(row=11, column=1, sticky=W, padx=180)
            self.var6_unit_myCombo.grid(row=11, column=0, sticky=E, padx=10)

        # -----------------------Place Label & Entry-Boxes for Variable 7 on GUI
        def var7_show():
            self.variable7_label.grid(row=12, column=0, sticky=W, padx=20)
            self.var7_name_entry.grid(row=12, column=1, sticky=W)
            self.var7_min_entry.grid(row=12, column=1, sticky=W, padx=60)
            self.var7_max_entry.grid(row=12, column=1, sticky=W, padx=100)
            self.var7_prec_entry.grid(row=12, column=1, sticky=W, padx=140)
            self.var7_divby_entry.grid(row=12, column=1, sticky=W, padx=180)
            self.var7_unit_myCombo.grid(row=12, column=0, sticky=E, padx=10)

        def var2_remove():
            self.variable2_label.grid_remove()
            self.var2_name_entry.grid_remove()
            self.var2_min_entry.grid_remove()
            self.var2_max_entry.grid_remove()
            self.var2_prec_entry.grid_remove()
            self.var2_divby_entry.grid_remove()
            self.var2_unit_myCombo.grid_remove()

        def var3_remove():
            self.variable3_label.grid_remove()
            self.var3_name_entry.grid_remove()
            self.var3_min_entry.grid_remove()
            self.var3_max_entry.grid_remove()
            self.var3_prec_entry.grid_remove()
            self.var3_divby_entry.grid_remove()
            self.var3_unit_myCombo.grid_remove()

        def var4_remove():
            self.variable4_label.grid_remove()
            self.var4_name_entry.grid_remove()
            self.var4_min_entry.grid_remove()
            self.var4_max_entry.grid_remove()
            self.var4_prec_entry.grid_remove()
            self.var4_divby_entry.grid_remove()
            self.var4_unit_myCombo.grid_remove()

        def var5_remove():
            self.variable5_label.grid_remove()
            self.var5_name_entry.grid_remove()
            self.var5_min_entry.grid_remove()
            self.var5_max_entry.grid_remove()
            self.var5_prec_entry.grid_remove()
            self.var5_divby_entry.grid_remove()
            self.var5_unit_myCombo.grid_remove()

        def var6_remove():
            self.variable6_label.grid_remove()
            self.var6_name_entry.grid_remove()
            self.var6_min_entry.grid_remove()
            self.var6_max_entry.grid_remove()
            self.var6_prec_entry.grid_remove()
            self.var6_divby_entry.grid_remove()
            self.var6_unit_myCombo.grid_remove()

        def var7_remove():
            self.variable7_label.grid_remove()
            self.var7_name_entry.grid_remove()
            self.var7_min_entry.grid_remove()
            self.var7_max_entry.grid_remove()
            self.var7_prec_entry.grid_remove()
            self.var7_divby_entry.grid_remove()
            self.var7_unit_myCombo.grid_remove()

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

        self.res1_unit_myCombo = ttk.Combobox(self.frame_formula, value=self.select_var_units, width=5)
        self.res1_unit_myCombo.current(0)
        self.res1_unit_myCombo.bind("<<ComboboxSelected>>", selected_var)
        self.res1_unit_myCombo.grid(row=21, column=0, sticky=E, padx=10)

        self.res2_unit_myCombo = ttk.Combobox(self.frame_formula, value=self.select_var_units, width=5)
        self.res2_unit_myCombo.current(0)
        self.res2_unit_myCombo.bind("<<ComboboxSelected>>", selected_var)

        self.res3_unit_myCombo = ttk.Combobox(self.frame_formula, value=self.select_var_units, width=5)
        self.res3_unit_myCombo.current(0)
        self.res3_unit_myCombo.bind("<<ComboboxSelected>>", selected_var)


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
            self.res2_unit_myCombo.grid(row=22, column=0, sticky=E, padx=10)

        def res3_show():
            self.result3_label.grid(row=23, column=0, sticky=W, padx=20)
            self.res3_name_entry.grid(row=23, column=1, sticky=W)
            self.res3_min_entry.grid(row=23, column=1, sticky=W, padx=60)
            self.res3_max_entry.grid(row=23, column=1, sticky=W, padx=100)
            self.res3_prec_entry.grid(row=23, column=1, sticky=W, padx=140)
            self.res3_tol_entry.grid(row=23, column=1, sticky=W, padx=180)
            self.res3_points_entry.grid(row=23, column=1, sticky=W, padx=220)
            self.res3_formula_entry.grid(row=23, column=1, sticky=E, padx=20)
            self.res3_unit_myCombo.grid(row=23, column=0, sticky=E, padx=10)

        def res2_remove():
            self.result2_label.grid_remove()
            self.res2_name_entry.grid_remove()
            self.res2_min_entry.grid_remove()
            self.res2_max_entry.grid_remove()
            self.res2_prec_entry.grid_remove()
            self.res2_tol_entry.grid_remove()
            self.res2_points_entry.grid_remove()
            self.res2_unit_myCombo.grid_remove()

        def res3_remove():
            self.result3_label.grid_remove()
            self.res3_name_entry.grid_remove()
            self.res3_min_entry.grid_remove()
            self.res3_max_entry.grid_remove()
            self.res3_prec_entry.grid_remove()
            self.res3_tol_entry.grid_remove()
            self.res3_points_entry.grid_remove()
            self.res3_unit_myCombo.grid_remove()

        # Create Tooltip balloons
        self.tooltip = Pmw.Balloon(self.frame_formula)
        self.tooltip.bind(self.var1_name_entry, "Name der Variable für var1")
        self.tooltip.bind(self.var2_name_entry, "Name der Variable für var2")
        self.tooltip.bind(self.var3_name_entry, "Name der Variable für var3")
        self.tooltip.bind(self.var4_name_entry, "Name der Variable für var4")
        self.tooltip.bind(self.var5_name_entry, "Name der Variable für var5")
        self.tooltip.bind(self.var6_name_entry, "Name der Variable für var6")
        self.tooltip.bind(self.var7_name_entry, "Name der Variable für var7")
        self.tooltip.bind(self.res1_name_entry, "Name der Variable für res1")
        self.tooltip.bind(self.res2_name_entry, "Name der Variable für res2")
        self.tooltip.bind(self.res3_name_entry, "Name der Variable für res3")



    def unit_table(self, selected_unit):
        self.unit_to_ilias_code = { "H" : "125", "mH" : "126", "µH" : "127", "nH" : "128", "kH" : "129", "pH" : "130",
                                    "F" : "131", "mF" : "132", "µF" : "133", "nF" : "134", "kF" : "135",
                                    "W" : "136", "kW" : "137", "MW" : "138", "mW" : "149",
                                    "V" : "139", "kV" : "140", "mV" : "141", "µV" : "142", "MV" : "143",
                                    "A" : "144", "mA" : "145", "µA" : "146", "kA" : "147",
                                    "Ohm" : "148", "kOhm" : "150", "mOhm" : "151"}

        self.varTEST = selected_unit
        #print(self.varTEST)
        self.selected_unit = self.unit_to_ilias_code[self.varTEST]
        return self.selected_unit


    def add_term(self):
        self.formula_question_entry.insert(SEL_FIRST, '\\(', 'RED')
        self.formula_question_entry.insert(SEL_LAST, '\\)', 'RED')
        self.formula_question_entry.tag_config('RED', foreground='red')



class MultipleChoice(Formelfrage):
    def __init__(self):
        # self.my_frame = Frame(master)
        # self.my_frame.grid()

        self.mc_frame = LabelFrame(self.multipleChoice_tab, text="Multiple Choice", padx=5, pady=5)
        self.mc_frame.grid(row=0, column=0, padx=10, pady=10, sticky=NW)

        self.mc_question_title_label = Label(self.mc_frame, text="Titel")
        self.mc_question_title_label.grid(row=0, column=0, sticky=W, padx=10, pady=(10, 0))
        self.mc_question_title_entry = Entry(self.mc_frame, width=60)
        self.mc_question_title_entry.grid(row=0, column=1, pady=(10, 0), sticky=W)

        # mc_author_label = Label(mc_frame, text="Autor")
        # mc_author_label.grid(row=1, column=0, sticky=W, padx=10)
        # mc_author_entry = Entry(mc_frame, width=60)
        # mc_author_entry.grid(row=1, column=1, sticky=W)

        self.mc_question_description_label = Label(self.mc_frame, text="Beschreibung")
        self.mc_question_description_label.grid(row=2, column=0, sticky=W, padx=10)
        self.mc_question_description_entry = Entry(self.mc_frame, width=60)
        self.mc_question_description_entry.grid(row=2, column=1, sticky=W)

        self.mc_question_textfield_label = Label(self.mc_frame, text="Frage")
        self.mc_question_textfield_label.grid(row=3, column=0, sticky=W, padx=10)

        self.mc_bar = Scrollbar(self.mc_frame)
        self.mc_infobox = Text(self.mc_frame, height=6, width=65, font=('Helvetica', 9))
        self.mc_bar.grid(row=3, column=2, sticky=W)
        self.mc_infobox.grid(row=3, column=1, pady=10, sticky=W)
        self.mc_bar.config(command=self.mc_infobox.yview)
        self.mc_infobox.config(yscrollcommand=self.mc_bar.set)

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

        self.mc_processingtime_hours = list(range(24))
        self.mc_processingtime_minutes = list(range(60))
        self.mc_processingtime_seconds = list(range(60))

        self.mc_proc_hours_box = ttk.Combobox(self.mc_frame, value=self.mc_processingtime_hours, width=2)
        self.mc_proc_minutes_box = ttk.Combobox(self.mc_frame, value=self.mc_processingtime_minutes, width=2)
        self.mc_proc_seconds_box = ttk.Combobox(self.mc_frame, value=self.mc_processingtime_seconds, width=2)

        self.mc_proc_hours_box.current(0)
        self.mc_proc_minutes_box.current(0)
        self.mc_proc_seconds_box.current(0)

        self.mc_proc_hours_box.bind("<<ComboboxSelected>>")
        self.mc_proc_hours_box.bind("<<ComboboxSelected>>")
        self.mc_proc_hours_box.bind("<<ComboboxSelected>>")

        self.mc_proc_hours_box.grid(row=4, column=1, sticky=W, padx=25, pady=(5, 0))
        self.mc_proc_minutes_box.grid(row=4, column=1, sticky=W, padx=100, pady=(5, 0))
        self.mc_proc_seconds_box.grid(row=4, column=1, sticky=W, padx=170, pady=(5, 0))

        self.mc_mix_questions_label = Label(self.mc_frame, text="Fragen mischen")
        self.mc_mix_questions_label.grid(row=5, column=0, sticky=W, padx=10, pady=(5, 0))

        self.mc_var_mix_questions = StringVar()
        self.mc_check_mix_questions = Checkbutton(self.mc_frame, text="", variable=self.mc_var_mix_questions, onvalue="1", offvalue="0")
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
        self.numbers_of_answers_box.current(0)

        # self.Label(self.mc_frame, text="Antworten").grid(row=9, column=0, sticky=W, padx=10, pady=(5, 0))
        # self.Label(self.mc_frame, text="Antwort-Text").grid(row=9, column=1, sticky=W, pady=(5, 0))
        self.points_picked_label = Label(self.mc_frame, text="Punkte:\nAusgewählt")
        self.points_picked_label.grid(row=8, column=1, sticky=E, padx=30)
        self.points_not_picked_label = Label(self.mc_frame, text="Punkte:\nNicht ausgewählt")
        self.points_not_picked_label.grid(row=8, column=2)

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

        self.var1_points_picked_entry = Entry(self.mc_frame, textvariable=self.var1_points_picked_text, width=8)
        self.var2_points_picked_entry = Entry(self.mc_frame, textvariable=self.var2_points_picked_text, width=8)
        self.var3_points_picked_entry = Entry(self.mc_frame, textvariable=self.var3_points_picked_text, width=8)
        self.var4_points_picked_entry = Entry(self.mc_frame, textvariable=self.var4_points_picked_text, width=8)
        self.var5_points_picked_entry = Entry(self.mc_frame, textvariable=self.var5_points_picked_text, width=8)
        self.var6_points_picked_entry = Entry(self.mc_frame, textvariable=self.var6_points_picked_text, width=8)
        self.var7_points_picked_entry = Entry(self.mc_frame, textvariable=self.var7_points_picked_text, width=8)

        # ------------------------------- VARIABLES PRECISION - TEXT & ENTRY --------------------------------------------

        self.var1_points_not_picked_entry = Entry(self.mc_frame, textvariable=self.var1_points_not_picked_text, width=8)
        self.var2_points_not_picked_entry = Entry(self.mc_frame, textvariable=self.var2_points_not_picked_text, width=8)
        self.var3_points_not_picked_entry = Entry(self.mc_frame, textvariable=self.var3_points_not_picked_text, width=8)
        self.var4_points_not_picked_entry = Entry(self.mc_frame, textvariable=self.var4_points_not_picked_text, width=8)
        self.var5_points_not_picked_entry = Entry(self.mc_frame, textvariable=self.var5_points_not_picked_text, width=8)
        self.var6_points_not_picked_entry = Entry(self.mc_frame, textvariable=self.var6_points_not_picked_text, width=8)
        self.var7_points_not_picked_entry = Entry(self.mc_frame, textvariable=self.var7_points_not_picked_text, width=8)

        self.answer1_label = Label(self.mc_frame, text="Antwort 1")
        self.answer2_label = Label(self.mc_frame, text="Antwort 2")
        self.answer3_label = Label(self.mc_frame, text="Antwort 3")
        self.answer4_label = Label(self.mc_frame, text="Antwort 4")
        self.answer5_label = Label(self.mc_frame, text="Antwort 5")
        self.answer6_label = Label(self.mc_frame, text="Antwort 6")
        self.answer7_label = Label(self.mc_frame, text="Antwort 7")

        self.answer1_label.grid(row=10, column=0, sticky=W, padx=30)
        self.var1_answer_entry.grid(row=10, column=1, sticky=W)
        self.var1_points_picked_entry.grid(row=10, column=1, sticky=E, padx=40)
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

    def submit_mc(self):
        conn = sqlite3.connect('ilias_questions_db.db')
        c = conn.cursor()

        # format of duration P0Y0M0DT0H30M0S
        self.mc_test_time = "P0Y0M0DT" + self.mc_proc_hours_box.get() + "H" + self.mc_proc_minutes_box.get() + "M" + self.mc_proc_seconds_box.get() + "S"

        # Insert into Table
        c.execute(
            "INSERT INTO my_table VALUES ("
            ":question_difficulty, :question_category, :question_type, "
            ":question_title, :question_title_description, :question_description_main, "
            ":res1_formula, :res2_formula, :res3_formula,  "
            ":var1_name, :var1_min, :var1_max, :var1_prec, :var1_divby, :var1_unit, "
            ":var2_name, :var2_min, :var2_max, :var2_prec, :var2_divby, :var2_unit, "
            ":var3_name, :var3_min, :var3_max, :var3_prec, :var3_divby, :var3_unit, "
            ":var4_name, :var4_min, :var4_max, :var4_prec, :var4_divby, :var4_unit, "
            ":var5_name, :var5_min, :var5_max, :var5_prec, :var5_divby, :var5_unit, "
            ":var6_name, :var6_min, :var6_max, :var6_prec, :var6_divby, :var6_unit, "
            ":var7_name, :var7_min, :var7_max, :var7_prec, :var7_divby, :var7_unit,"
            ":res1_name, :res1_min, :res1_max, :res1_prec, :res1_tol, :res1_points, :res1_unit, "
            ":res2_name, :res2_min, :res2_max, :res2_prec, :res2_tol, :res2_points, :res2_unit, "
            ":res3_name, :res3_min, :res3_max, :res3_prec, :res3_tol, :res3_points, :res3_unit,"
            ":img_name, :img_data, :test_time)",
            {
                'question_difficulty': self.mc_question_difficulty_entry.get(),
                'question_category': self.mc_question_category_entry.get(),
                'question_type': self.mc_question_type_entry.get(),

                'question_title': self.mc_question_title_entry.get(),
                'question_title_description': self.mc_question_description_entry.get(),

                # The first part, "1.0" means that the input should be read from line one, character zero (ie: the very first character).
                # END is an imported constant which is set to the string "end". The END part means to read until the end of the text box is reached.
                # The only issue with this is that it actually adds a newline to our input. "
                # "So, in order to fix it we should change END to end-1c(Thanks Bryan Oakley) The -1c deletes 1 character, while -2c would mean delete two characters, and so on."
                'question_description_main': self.mc_infobox.get("1.0", 'end-1c'),

                # Antwort-Text  in Datenbank-Fach: var_name
                'var1_name': self.var1_answer_text.get(),
                'var1_min': self.var1_points_picked_text.get(),
                'var1_max': self.var1_points_not_picked_text.get(),

                'var2_name': self.var2_answer_text.get(),
                'var2_min': self.var2_points_picked_text.get(),
                'var2_max': self.var2_points_not_picked_text.get(),

                'var3_name': self.var3_answer_text.get(),
                'var3_min': self.var3_points_picked_text.get(),
                'var3_max': self.var3_points_not_picked_text.get(),

                'var4_name': self.var4_answer_text.get(),
                'var4_min': self.var4_points_picked_text.get(),
                'var4_max': self.var4_points_not_picked_text.get(),

                'var5_name': self.var5_answer_text.get(),
                'var5_min': self.var5_points_picked_text.get(),
                'var5_max': self.var5_points_not_picked_text.get(),

                'var6_name': self.var6_answer_text.get(),
                'var6_min': self.var6_points_picked_text.get(),
                'var6_max': self.var6_points_not_picked_text.get(),

                'var7_name': self.var7_answer_text.get(),
                'var7_min': self.var7_points_picked_text.get(),
                'var7_max': self.var7_points_not_picked_text.get(),

                'test_time': self.mc_test_time,


                'res1_formula': "",
                'res2_formula': "",
                'res3_formula': "",
                'var1_prec': "",
                'var1_divby': "",
                'var1_unit': "",
                'var2_prec': "",
                'var2_divby': "",
                'var2_unit': "",
                'var3_prec': "",
                'var3_divby': "",
                'var3_unit': "",
                'var4_prec': "",
                'var4_divby': "",
                'var4_unit': "",
                'var5_prec': "",
                'var5_divby': "",
                'var5_unit': "",
                'var6_prec': "",
                'var6_divby': "",
                'var6_unit': "",
                'var7_prec': "",
                'var7_divby': "",
                'var7_unit': "",

                'res1_name': "",
                'res1_min': "",
                'res1_max': "",
                'res1_prec': "",
                'res1_tol': "",
                'res1_points': "",
                'res1_unit': "",

                'res2_name': "",
                'res2_min': "",
                'res2_max': "",
                'res2_prec': "",
                'res2_tol': "",
                'res2_points': "",
                'res2_unit': "",

                'res3_name': "",
                'res3_min': "",
                'res3_max': "",
                'res3_prec': "",
                'res3_tol': "",
                'res3_points': "",
                'res3_unit': "",

                'img_name': "",
                'img_data': ""



            }
        )
        conn.commit()
        conn.close()
        print("mc question in databank")



class create_multiplechoice(MultipleChoice):

    def __init__(self):
        #self.mytree = ET.parse(self.qti_file_path_read)
        #self.myroot = self.mytree.getroot()

        self.frame_mc_create = LabelFrame(self.formula_tab, text="Create Multiplechoice", padx=5, pady=5)
        self.frame_mc_create.grid(row=1, column=2)

        #create_multiplechoice.create_mc_question(self)


    def create_mc_question(self,mytree, myroot, qti_file_path_read, qti_file_path_write, entry_split, x):

        #self.mytree = ET.parse(qti_file_path_read)
        #self.myroot = self.mytree.getroot()

        self.mytree = mytree
        self.myroot = myroot

        conn = sqlite3.connect('ilias_questions_db.db')
        c = conn.cursor()
        c.execute("SELECT *, oid FROM my_table")

        records = c.fetchall()

        for record in records:
            if str(record[len(record) - 1]) == entry_split[x]:

                self.answer1 = str(record[9])
                self.answer1_points_picked = str(record[10])
                self.answer1_points_not_picked = str(record[11])

                self.answer2 = str(record[15])
                self.answer2_points_picked = str(record[16])
                self.answer2_points_not_picked = str(record[17])

                self.answer3 = str(record[21])
                self.answer3_points_picked = str(record[22])
                self.answer3_points_not_picked = str(record[23])

                self.answer4 = str(record[27])
                self.answer4_points_picked = str(record[28])
                self.answer4_points_not_picked = str(record[29])

                self.answer5 = str(record[33])
                self.answer5_points_picked = str(record[34])
                self.answer5_points_not_picked = str(record[35])

                self.answer6 = str(record[39])
                self.answer6_points_picked = str(record[40])
                self.answer6_points_not_picked = str(record[41])

                self.answer7 = str(record[45])
                self.answer7_points_picked = str(record[46])
                self.answer7_points_not_picked = str(record[47])

                self.mc_test_time = str(record[74])






                questestinterop = ET.Element('questestinterop')
                assessment = ET.SubElement(questestinterop, 'assessment')
                section = ET.SubElement(assessment, 'section')
                item = ET.SubElement(section, 'item')
                item.set('ident', "il_0_qst_000001")
                item.set('title', "MC: 1. Frage")
                item.set('maxattempts', "0")
                qticomment = ET.SubElement(item, 'qticomment')
                # qticomment.text = self.mc_question_description_title
                duration = ET.SubElement(item, 'duration')
                duration.text = self.mc_test_time

                # append ITEM in the last "myroot"-Element. Here it is Element "section" in myroot
                self.myroot[0][len(self.myroot[0]) - 1].append(item)


                itemmetadata = ET.SubElement(item, 'itemmetadata')
                presentation = ET.SubElement(item, 'presentation')
                flow = ET.SubElement(presentation, 'flow')
                material = ET.SubElement(flow, 'material')
                response_lid = ET.SubElement(flow, 'response_lid')
                render_choice = ET.SubElement(response_lid, 'render_choice')
                response_label = ET.SubElement(render_choice, 'response_label')







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

                presentation.set('label', "MC: 1. Frage")
                mattext = ET.SubElement(material, 'mattext')
                mattext.set('texttype', "text/html")
                mattext.text = "<p>" + "TEST - Was kommt in der Natur vor?" + "</p>"

                response_lid.set('ident', "MCMR")
                response_lid.set('rcardinality', "Multiple")

                render_choice.set('shuffle', "Yes")
                # -------------------------- Antwort 1
                response_label.set('ident', "0")
                material = ET.SubElement(response_label, 'material')
                mattext = ET.SubElement(material, 'mattext')
                mattext.set('texttype', "text/plain")
                mattext.text = self.answer1

                # -------------------------- Antwort 2
                response_label = ET.SubElement(render_choice, 'response_label')
                response_label.set('ident', "1")
                material = ET.SubElement(response_label, 'material')
                mattext = ET.SubElement(material, 'mattext')
                mattext.set('texttype', "text/plain")
                mattext.text = self.answer2

                # -------------------------- Antwort 3
                response_label = ET.SubElement(render_choice, 'response_label')
                response_label.set('ident', "2")
                material = ET.SubElement(response_label, 'material')
                mattext = ET.SubElement(material, 'mattext')
                mattext.set('texttype', "text/plain")
                mattext.text = self.answer3

                resprocessing = ET.SubElement(item, 'resprocessing')
                outcomes = ET.SubElement(resprocessing, 'outcomes')
                decvar = ET.SubElement(outcomes, 'decvar')

                # -------------------------- Zusatz für Antwort 1
                respcondition = ET.SubElement(resprocessing, 'respcondition')
                respcondition.set('continue', "Yes")
                conditionvar = ET.SubElement(respcondition, 'conditionvar')
                varequal = ET.SubElement(conditionvar, 'varequal')
                varequal.set('respident', "MCMR")
                varequal.text = "0"
                setvar = ET.SubElement(respcondition, 'setvar')
                setvar.set('action', "Add")
                setvar.text = "1"
                displayfeedback = ET.SubElement(respcondition, 'displayfeedback')
                displayfeedback.set('feedbacktype', "Response")
                displayfeedback.set('linkrefid', "response_0")
                respcondition = ET.SubElement(resprocessing, 'respcondition')
                respcondition.set('continue', "Yes")
                conditionvar = ET.SubElement(respcondition, 'conditionvar')
                mc_not = ET.SubElement(conditionvar, 'mc_not')
                varequal = ET.SubElement(mc_not, 'varequal')
                varequal.set('respident', "MCMR")
                varequal.text = "0"
                setvar = ET.SubElement(respcondition, 'setvar')
                setvar.set('action', "Add")
                setvar.text = "0"

                # -------------------------- Zusatz für Antwort 2
                respcondition = ET.SubElement(resprocessing, 'respcondition')
                respcondition.set('continue', "Yes")
                conditionvar = ET.SubElement(respcondition, 'conditionvar')
                varequal = ET.SubElement(conditionvar, 'varequal')
                varequal.set('respident', "MCMR")
                varequal.text = "1"
                setvar = ET.SubElement(respcondition, 'setvar')
                setvar.set('action', "Add")
                setvar.text = "1"
                displayfeedback = ET.SubElement(respcondition, 'displayfeedback')
                displayfeedback.set('feedbacktype', "Response")
                displayfeedback.set('linkrefid', "response_1")
                respcondition = ET.SubElement(resprocessing, 'respcondition')
                respcondition.set('continue', "Yes")
                conditionvar = ET.SubElement(respcondition, 'conditionvar')
                mc_not = ET.SubElement(conditionvar, 'mc_not')
                varequal = ET.SubElement(mc_not, 'varequal')
                varequal.set('respident', "MCMR")
                varequal.text = "1"
                setvar = ET.SubElement(respcondition, 'setvar')
                setvar.set('action', "Add")
                setvar.text = "0"

                # -------------------------- Zusatz für Antwort 3
                respcondition = ET.SubElement(resprocessing, 'respcondition')
                respcondition.set('continue', "Yes")
                conditionvar = ET.SubElement(respcondition, 'conditionvar')
                varequal = ET.SubElement(conditionvar, 'varequal')
                varequal.set('respident', "MCMR")
                varequal.text = "2"
                setvar = ET.SubElement(respcondition, 'setvar')
                setvar.set('action', "Add")
                setvar.text = "1"
                displayfeedback = ET.SubElement(respcondition, 'displayfeedback')
                displayfeedback.set('feedbacktype', "Response")
                displayfeedback.set('linkrefid', "response_2")
                respcondition = ET.SubElement(resprocessing, 'respcondition')
                respcondition.set('continue', "Yes")
                conditionvar = ET.SubElement(respcondition, 'conditionvar')
                mc_not = ET.SubElement(conditionvar, 'mc_not')
                varequal = ET.SubElement(mc_not, 'varequal')
                varequal.set('respident', "MCMR")
                varequal.text = "2"
                setvar = ET.SubElement(respcondition, 'setvar')
                setvar.set('action', "Add")
                setvar.text = "0"


                itemfeedback = ET.SubElement(item, 'itemfeedback')
                itemfeedback.set('ident', "response_0")
                itemfeedback.set('view', "All")
                flow_mat = ET.SubElement(itemfeedback, 'flow_mat')
                material = ET.SubElement(flow_mat, 'material')
                mattext = ET.SubElement(material, 'mattext')
                mattext.set('texttype', "text/plain")

                itemfeedback = ET.SubElement(item, 'itemfeedback')
                itemfeedback.set('ident', "response_1")
                itemfeedback.set('view', "All")
                flow_mat = ET.SubElement(itemfeedback, 'flow_mat')
                material = ET.SubElement(flow_mat, 'material')
                mattext = ET.SubElement(material, 'mattext')
                mattext.set('texttype', "text/plain")

                itemfeedback = ET.SubElement(item, 'itemfeedback')
                itemfeedback.set('ident', "response_2")
                itemfeedback.set('view', "All")
                flow_mat = ET.SubElement(itemfeedback, 'flow_mat')
                material = ET.SubElement(flow_mat, 'material')
                mattext = ET.SubElement(material, 'mattext')
                mattext.set('texttype', "text/plain")


                self.mytree.write(qti_file_path_write)
                print("MC Question created")

        conn.commit()
        conn.close()

        create_multiplechoice.mc_replace_characters(self, qti_file_path_write)



    def mc_replace_characters(self, qti_file_path_write):
        # with open("xml_form_edit\\" + 'NEW_1590230409__0__qti_1948621.xml') as xml_file:
        with open(qti_file_path_write, 'r') as xml_file:
            xml_str = xml_file.read()
        xml_str = xml_str.replace('mc_not', 'not')  #replace "x" with "new value for x"

        with open(qti_file_path_write, 'w') as replaced_xml_file:
            replaced_xml_file.write(xml_str)

        print("\"mc_not\" replaced with \"not\"... done ")


class Database(Formelfrage):

    def __init__(self):

        self.database_window = Tk()
        self.database_window.title("Datenbank")

        # Create a ScrolledFrame widget
        #self.sf_database = ScrolledFrame(self.database_window, width=600, height=600)
        self.sf_database = ScrolledFrame(self.database_window, width=self.database_width, height=self.database_height)
        self.sf_database.pack(expand=1, fill="both")

        # Bind the arrow keys and scroll wheel
        self.sf_database.bind_arrow_keys(app)
        self.sf_database.bind_scroll_wheel(app)

        # Create a frame within the ScrolledFrame
        self.db_inner_frame = self.sf_database.display_widget(Frame)



        # CREATE LISTBOXES ON GUI

        self.oid_listbox_label = Label(self.db_inner_frame, text=" DB\nID")
        self.oid_listbox_label.grid(row=25, column=1, sticky=W)

        self.question_difficulty_listbox_label = Label(self.db_inner_frame, text="Question\nDifficulty")
        self.question_difficulty_listbox_label.grid(row=25, column=2, sticky=W)

        self.question_category_listbox_label = Label(self.db_inner_frame, text="Question\nCategory")
        self.question_category_listbox_label.grid(row=25, column=3, sticky=W)

        self.question_type_listbox_label = Label(self.db_inner_frame, text="Question\nType")
        self.question_type_listbox_label.grid(row=25, column=4, sticky=W)

        self.question_title_listbox_label = Label(self.db_inner_frame, text="Question\nTitle", width=15)
        self.question_title_listbox_label.grid(row=25, column=5, sticky=W)

        self.question_description_title_listbox_label = Label(self.db_inner_frame, text="Description\nTitle", width=15)
        self.question_description_title_listbox_label.grid(row=25, column=6, sticky=W)

        self.question_description_main_listbox_label = Label(self.db_inner_frame, text="Description\nMain", width=15)
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
        self.var1_unit_listbox_label = Label(self.db_inner_frame, text="var1\nunit")
        self.var1_unit_listbox_label.grid(row=25, column=16, sticky=W)

        self.var2_name_listbox_label = Label(self.db_inner_frame, text="var2\nname")
        self.var2_name_listbox_label.grid(row=25, column=17, sticky=W)
        self.var2_min_listbox_label = Label(self.db_inner_frame, text="var2\nmin")
        self.var2_min_listbox_label.grid(row=25, column=18, sticky=W)
        self.var2_max_listbox_label = Label(self.db_inner_frame, text="var2\nmax")
        self.var2_max_listbox_label.grid(row=25, column=19, sticky=W)
        self.var2_prec_listbox_label = Label(self.db_inner_frame, text="var2\nprec")
        self.var2_prec_listbox_label.grid(row=25, column=20, sticky=W)
        self.var2_divby_listbox_label = Label(self.db_inner_frame, text="var2\ndivby")
        self.var2_divby_listbox_label.grid(row=25, column=21, sticky=W)
        self.var2_unit_listbox_label = Label(self.db_inner_frame, text="var2\nunit")
        self.var2_unit_listbox_label.grid(row=25, column=22, sticky=W)

        self.var3_name_listbox_label = Label(self.db_inner_frame, text="var3\nname")
        self.var3_name_listbox_label.grid(row=25, column=23, sticky=W)
        self.var3_min_listbox_label = Label(self.db_inner_frame, text="var3\nmin")
        self.var3_min_listbox_label.grid(row=25, column=24, sticky=W)
        self.var3_max_listbox_label = Label(self.db_inner_frame, text="var3\nmax")
        self.var3_max_listbox_label.grid(row=25, column=25, sticky=W)
        self.var3_prec_listbox_label = Label(self.db_inner_frame, text="var3\nprec")
        self.var3_prec_listbox_label.grid(row=25, column=26, sticky=W)
        self.var3_divby_listbox_label = Label(self.db_inner_frame, text="var3\ntol")
        self.var3_divby_listbox_label.grid(row=25, column=27, sticky=W)
        self.var3_unit_listbox_label = Label(self.db_inner_frame, text="var3\nunit")
        self.var3_unit_listbox_label.grid(row=25, column=28, sticky=W)

        self.var4_name_listbox_label = Label(self.db_inner_frame, text="var4\nname")
        self.var4_name_listbox_label.grid(row=25, column=29, sticky=W)
        self.var4_min_listbox_label = Label(self.db_inner_frame, text="var4\nmin")
        self.var4_min_listbox_label.grid(row=25, column=30, sticky=W)
        self.var4_max_listbox_label = Label(self.db_inner_frame, text="var4\nmax")
        self.var4_max_listbox_label.grid(row=25, column=31, sticky=W)
        self.var4_prec_listbox_label = Label(self.db_inner_frame, text="var4\nprec")
        self.var4_prec_listbox_label.grid(row=25, column=32, sticky=W)
        self.var4_divby_listbox_label = Label(self.db_inner_frame, text="var4\ntol")
        self.var4_divby_listbox_label.grid(row=25, column=33, sticky=W)
        self.var4_unit_listbox_label = Label(self.db_inner_frame, text="var4\nunit")
        self.var4_unit_listbox_label.grid(row=25, column=34, sticky=W)

        self.var5_name_listbox_label = Label(self.db_inner_frame, text="var5\nname")
        self.var5_name_listbox_label.grid(row=25, column=35, sticky=W)
        self.var5_min_listbox_label = Label(self.db_inner_frame, text="var5\nmin")
        self.var5_min_listbox_label.grid(row=25, column=36, sticky=W)
        self.var5_max_listbox_label = Label(self.db_inner_frame, text="var5\nmax")
        self.var5_max_listbox_label.grid(row=25, column=37, sticky=W)
        self.var5_prec_listbox_label = Label(self.db_inner_frame, text="var5\nprec")
        self.var5_prec_listbox_label.grid(row=25, column=38, sticky=W)
        self.var5_divby_listbox_label = Label(self.db_inner_frame, text="var5\ntol")
        self.var5_divby_listbox_label.grid(row=25, column=39, sticky=W)
        self.var5_unit_listbox_label = Label(self.db_inner_frame, text="var5\nunit")
        self.var5_unit_listbox_label.grid(row=25, column=40, sticky=W)

        self.var6_name_listbox_label = Label(self.db_inner_frame, text="var6\nname")
        self.var6_name_listbox_label.grid(row=25, column=41, sticky=W)
        self.var6_min_listbox_label = Label(self.db_inner_frame, text="var6\nmin")
        self.var6_min_listbox_label.grid(row=25, column=42, sticky=W)
        self.var6_max_listbox_label = Label(self.db_inner_frame, text="var6\nmax")
        self.var6_max_listbox_label.grid(row=25, column=43, sticky=W)
        self.var6_prec_listbox_label = Label(self.db_inner_frame, text="var6\nprec")
        self.var6_prec_listbox_label.grid(row=25, column=44, sticky=W)
        self.var6_divby_listbox_label = Label(self.db_inner_frame, text="var6\ntol")
        self.var6_divby_listbox_label.grid(row=25, column=45, sticky=W)
        self.var6_unit_listbox_label = Label(self.db_inner_frame, text="var6\nunit")
        self.var6_unit_listbox_label.grid(row=25, column=46, sticky=W)

        self.var7_name_listbox_label = Label(self.db_inner_frame, text="var1\nname")
        self.var7_name_listbox_label.grid(row=25, column=47, sticky=W)
        self.var7_min_listbox_label = Label(self.db_inner_frame, text="var7\nmin")
        self.var7_min_listbox_label.grid(row=25, column=48, sticky=W)
        self.var7_max_listbox_label = Label(self.db_inner_frame, text="var7\nmax")
        self.var7_max_listbox_label.grid(row=25, column=49, sticky=W)
        self.var7_prec_listbox_label = Label(self.db_inner_frame, text="var7\nprec")
        self.var7_prec_listbox_label.grid(row=25, column=50, sticky=W)
        self.var7_divby_listbox_label = Label(self.db_inner_frame, text="var7\ntol")
        self.var7_divby_listbox_label.grid(row=25, column=51, sticky=W)
        self.var7_unit_listbox_label = Label(self.db_inner_frame, text="var7\nunit")
        self.var7_unit_listbox_label.grid(row=25, column=52, sticky=W)

        self.res1_name_listbox_label = Label(self.db_inner_frame, text="res1\nname")
        self.res1_name_listbox_label.grid(row=25, column=53, sticky=W)
        self.res1_min_listbox_label = Label(self.db_inner_frame, text="res1\nmin")
        self.res1_min_listbox_label.grid(row=25, column=54, sticky=W)
        self.res1_max_listbox_label = Label(self.db_inner_frame, text="res1\nmax")
        self.res1_max_listbox_label.grid(row=25, column=55, sticky=W)
        self.res1_prec_listbox_label = Label(self.db_inner_frame, text="res1\nprec")
        self.res1_prec_listbox_label.grid(row=25, column=56, sticky=W)
        self.res1_tol_listbox_label = Label(self.db_inner_frame, text="res1\ntol")
        self.res1_tol_listbox_label.grid(row=25, column=57, sticky=W)
        self.res1_points_listbox_label = Label(self.db_inner_frame, text="res1\npts")
        self.res1_points_listbox_label.grid(row=25, column=58, sticky=W)
        self.res1_unit_listbox_label = Label(self.db_inner_frame, text="res1\nunit")
        self.res1_unit_listbox_label.grid(row=25, column=59, sticky=W)

        self.res2_name_listbox_label = Label(self.db_inner_frame, text="res2\nname")
        self.res2_name_listbox_label.grid(row=25, column=60, sticky=W)
        self.res2_min_listbox_label = Label(self.db_inner_frame, text="res2\nmin")
        self.res2_min_listbox_label.grid(row=25, column=61, sticky=W)
        self.res2_max_listbox_label = Label(self.db_inner_frame, text="res2\nmax")
        self.res2_max_listbox_label.grid(row=25, column=62, sticky=W)
        self.res2_prec_listbox_label = Label(self.db_inner_frame, text="res2\nprec")
        self.res2_prec_listbox_label.grid(row=25, column=63, sticky=W)
        self.res2_tol_listbox_label = Label(self.db_inner_frame, text="res2\ntol")
        self.res2_tol_listbox_label.grid(row=25, column=64, sticky=W)
        self.res2_points_listbox_label = Label(self.db_inner_frame, text="res2\npts")
        self.res2_points_listbox_label.grid(row=25, column=65, sticky=W)
        self.res2_unit_listbox_label = Label(self.db_inner_frame, text="res2\nunit")
        self.res2_unit_listbox_label.grid(row=25, column=66, sticky=W)

        self.res3_name_listbox_label = Label(self.db_inner_frame, text="res3\nname")
        self.res3_name_listbox_label.grid(row=25, column=67, sticky=W)
        self.res3_min_listbox_label = Label(self.db_inner_frame, text="res3\nmin")
        self.res3_min_listbox_label.grid(row=25, column=68, sticky=W)
        self.res3_max_listbox_label = Label(self.db_inner_frame, text="res3\nmax")
        self.res3_max_listbox_label.grid(row=25, column=69, sticky=W)
        self.res3_prec_listbox_label = Label(self.db_inner_frame, text="res3\nprec")
        self.res3_prec_listbox_label.grid(row=25, column=70, sticky=W)
        self.res3_tol_listbox_label = Label(self.db_inner_frame, text="res3\ntol")
        self.res3_tol_listbox_label.grid(row=25, column=71, sticky=W)
        self.res3_points_listbox_label = Label(self.db_inner_frame, text="res3\npts")
        self.res3_points_listbox_label.grid(row=25, column=72, sticky=W)
        self.res3_unit_listbox_label = Label(self.db_inner_frame, text="res3\nunit")
        self.res3_unit_listbox_label.grid(row=25, column=73, sticky=W)


        self.img_name_listbox_label = Label(self.db_inner_frame, text=" img\n name")
        self.img_name_listbox_label.grid(row=25, column=74, sticky=W)

        self.img_data_label = Label(self.db_inner_frame, text=" img\n data")
        #self.img_data_label.grid(row=25, column=55, sticky=W)


        self.test_time_listbox_label = Label(self.db_inner_frame, text="test\ntime", width=10)
        self.test_time_listbox_label.grid(row=25, column=75, sticky=W)



        # CREATE FULL-LISTBOX ENTRYS IN NEW WINDOW

        self.my_listbox_oid = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_oid.grid(row=30, column=1, sticky=W)

        self.my_listbox_question_difficulty = Listbox(self.db_inner_frame, width=15, height=30)
        self.my_listbox_question_difficulty.grid(row=30, column=2, sticky=W)

        self.my_listbox_question_category = Listbox(self.db_inner_frame, width=15, height=30)
        self.my_listbox_question_category.grid(row=30, column=3, sticky=W)

        self.my_listbox_question_type = Listbox(self.db_inner_frame, width=15, height=30)
        self.my_listbox_question_type.grid(row=30, column=4, sticky=W)

        self.my_listbox_question_title = Listbox(self.db_inner_frame, width=15, height=30)
        self.my_listbox_question_title.grid(row=30, column=5, sticky=W, pady=20)
        self.my_listbox_question_description_title = Listbox(self.db_inner_frame, width=15, height=30)
        self.my_listbox_question_description_title.grid(row=30, column=6, sticky=W)
        self.my_listbox_question_description_main = Listbox(self.db_inner_frame, width=15, height=30)
        self.my_listbox_question_description_main.grid(row=30, column=7, sticky=W)

        self.my_listbox_res1_formula = Listbox(self.db_inner_frame, width=15, height=30)
        self.my_listbox_res1_formula.grid(row=30, column=8, sticky=W)
        self.my_listbox_res2_formula = Listbox(self.db_inner_frame, width=15, height=30)
        self.my_listbox_res2_formula.grid(row=30, column=9, sticky=W)
        self.my_listbox_res3_formula = Listbox(self.db_inner_frame, width=15, height=30)
        self.my_listbox_res3_formula.grid(row=30, column=10, sticky=W)

        self.my_listbox_var1_name = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var1_name.grid(row=30, column=11, sticky=W)
        self.my_listbox_var1_min = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var1_min.grid(row=30, column=12, sticky=W)
        self.my_listbox_var1_max = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var1_max.grid(row=30, column=13, sticky=W)
        self.my_listbox_var1_prec = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var1_prec.grid(row=30, column=14, sticky=W)
        self.my_listbox_var1_divby = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var1_divby.grid(row=30, column=15, sticky=W)
        self.my_listbox_var1_unit = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var1_unit.grid(row=30, column=16, sticky=W)

        self.my_listbox_var2_name = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var2_name.grid(row=30, column=17, sticky=W)
        self.my_listbox_var2_min = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var2_min.grid(row=30, column=18, sticky=W)
        self.my_listbox_var2_max = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var2_max.grid(row=30, column=19, sticky=W)
        self.my_listbox_var2_prec = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var2_prec.grid(row=30, column=20, sticky=W)
        self.my_listbox_var2_divby = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var2_divby.grid(row=30, column=21, sticky=W)
        self.my_listbox_var2_unit = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var2_unit.grid(row=30, column=22, sticky=W)

        self.my_listbox_var3_name = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var3_name.grid(row=30, column=23, sticky=W)
        self.my_listbox_var3_min = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var3_min.grid(row=30, column=24, sticky=W)
        self.my_listbox_var3_max = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var3_max.grid(row=30, column=25, sticky=W)
        self.my_listbox_var3_prec = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var3_prec.grid(row=30, column=26, sticky=W)
        self.my_listbox_var3_divby = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var3_divby.grid(row=30, column=27, sticky=W)
        self.my_listbox_var3_unit = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var3_unit.grid(row=30, column=28, sticky=W)

        self.my_listbox_var4_name = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var4_name.grid(row=30, column=29, sticky=W)
        self.my_listbox_var4_min = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var4_min.grid(row=30, column=30, sticky=W)
        self.my_listbox_var4_max = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var4_max.grid(row=30, column=31, sticky=W)
        self.my_listbox_var4_prec = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var4_prec.grid(row=30, column=32, sticky=W)
        self.my_listbox_var4_divby = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var4_divby.grid(row=30, column=33, sticky=W)
        self.my_listbox_var4_unit = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var4_unit.grid(row=30, column=34, sticky=W)

        self.my_listbox_var5_name = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var5_name.grid(row=30, column=35, sticky=W)
        self.my_listbox_var5_min = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var5_min.grid(row=30, column=36, sticky=W)
        self.my_listbox_var5_max = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var5_max.grid(row=30, column=37, sticky=W)
        self.my_listbox_var5_prec = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var5_prec.grid(row=30, column=38, sticky=W)
        self.my_listbox_var5_divby = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var5_divby.grid(row=30, column=39, sticky=W)
        self.my_listbox_var5_unit = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var5_unit.grid(row=30, column=40, sticky=W)

        self.my_listbox_var6_name = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var6_name.grid(row=30, column=41, sticky=W)
        self.my_listbox_var6_min = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var6_min.grid(row=30, column=42, sticky=W)
        self.my_listbox_var6_max = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var6_max.grid(row=30, column=43, sticky=W)
        self.my_listbox_var6_prec = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var6_prec.grid(row=30, column=44, sticky=W)
        self.my_listbox_var6_divby = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var6_divby.grid(row=30, column=45, sticky=W)
        self.my_listbox_var6_unit = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var6_unit.grid(row=30, column=46, sticky=W)

        self.my_listbox_var7_name = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var7_name.grid(row=30, column=47, sticky=W)
        self.my_listbox_var7_min = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var7_min.grid(row=30, column=48, sticky=W)
        self.my_listbox_var7_max = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var7_max.grid(row=30, column=49, sticky=W)
        self.my_listbox_var7_prec = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var7_prec.grid(row=30, column=50, sticky=W)
        self.my_listbox_var7_divby = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var7_divby.grid(row=30, column=51, sticky=W)
        self.my_listbox_var7_unit = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var7_unit.grid(row=30, column=52, sticky=W)

        self.my_listbox_res1_name = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_res1_name.grid(row=30, column=53, sticky=W)
        self.my_listbox_res1_min = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_res1_min.grid(row=30, column=54, sticky=W)
        self.my_listbox_res1_max = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_res1_max.grid(row=30, column=55, sticky=W)
        self.my_listbox_res1_prec = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_res1_prec.grid(row=30, column=56, sticky=W)
        self.my_listbox_res1_tol = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_res1_tol.grid(row=30, column=57, sticky=W)
        self.my_listbox_res1_points = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_res1_points.grid(row=30, column=58, sticky=W)
        self.my_listbox_res1_unit = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_res1_unit.grid(row=30, column=59, sticky=W)

        self.my_listbox_res2_name = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_res2_name.grid(row=30, column=60, sticky=W)
        self.my_listbox_res2_min = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_res2_min.grid(row=30, column=61, sticky=W)
        self.my_listbox_res2_max = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_res2_max.grid(row=30, column=62, sticky=W)
        self.my_listbox_res2_prec = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_res2_prec.grid(row=30, column=63, sticky=W)
        self.my_listbox_res2_tol = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_res2_tol.grid(row=30, column=64, sticky=W)
        self.my_listbox_res2_points = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_res2_points.grid(row=30, column=65, sticky=W)
        self.my_listbox_res2_unit = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_res2_unit.grid(row=30, column=66, sticky=W)

        self.my_listbox_res3_name = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_res3_name.grid(row=30, column=67, sticky=W)
        self.my_listbox_res3_min = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_res3_min.grid(row=30, column=68, sticky=W)
        self.my_listbox_res3_max = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_res3_max.grid(row=30, column=69, sticky=W)
        self.my_listbox_res3_prec = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_res3_prec.grid(row=30, column=70, sticky=W)
        self.my_listbox_res3_tol = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_res3_tol.grid(row=30, column=71, sticky=W)
        self.my_listbox_res3_points = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_res3_points.grid(row=30, column=72, sticky=W)
        self.my_listbox_res3_unit = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_res3_unit.grid(row=30, column=73, sticky=W)

        self.my_listbox_img_name = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_img_name.grid(row=30, column=74, sticky=W)

        self.my_listbox_img_data = Listbox(self.db_inner_frame, width=10, height=30)
        # self.my_listbox_img_data.grid(row=30, column=50, sticky=W)          #IMG_data need to get a database_entry, but would not "grid()" the entry to GUI. Otherwise it is real slow

        self.my_listbox_test_time = Listbox(self.db_inner_frame, width=20, height=30)
        self.my_listbox_test_time.grid(row=30, column=75, sticky=W)

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
            self.my_listbox_var1_unit.yview(*args)

            self.my_listbox_var2_name.yview(*args)
            self.my_listbox_var2_min.yview(*args)
            self.my_listbox_var2_max.yview(*args)
            self.my_listbox_var2_prec.yview(*args)
            self.my_listbox_var2_divby.yview(*args)
            self.my_listbox_var2_unit.yview(*args)

            self.my_listbox_var3_name.yview(*args)
            self.my_listbox_var3_min.yview(*args)
            self.my_listbox_var3_max.yview(*args)
            self.my_listbox_var3_prec.yview(*args)
            self.my_listbox_var3_divby.yview(*args)
            self.my_listbox_var3_unit.yview(*args)

            self.my_listbox_var4_name.yview(*args)
            self.my_listbox_var4_min.yview(*args)
            self.my_listbox_var4_max.yview(*args)
            self.my_listbox_var4_prec.yview(*args)
            self.my_listbox_var4_divby.yview(*args)
            self.my_listbox_var4_unit.yview(*args)

            self.my_listbox_var5_name.yview(*args)
            self.my_listbox_var5_min.yview(*args)
            self.my_listbox_var5_max.yview(*args)
            self.my_listbox_var5_prec.yview(*args)
            self.my_listbox_var5_divby.yview(*args)
            self.my_listbox_var5_unit.yview(*args)

            self.my_listbox_var6_name.yview(*args)
            self.my_listbox_var6_min.yview(*args)
            self.my_listbox_var6_max.yview(*args)
            self.my_listbox_var6_prec.yview(*args)
            self.my_listbox_var6_divby.yview(*args)
            self.my_listbox_var6_unit.yview(*args)

            self.my_listbox_var7_name.yview(*args)
            self.my_listbox_var7_min.yview(*args)
            self.my_listbox_var7_max.yview(*args)
            self.my_listbox_var7_prec.yview(*args)
            self.my_listbox_var7_divby.yview(*args)
            self.my_listbox_var7_unit.yview(*args)

            self.my_listbox_res1_name.yview(*args)
            self.my_listbox_res1_min.yview(*args)
            self.my_listbox_res1_max.yview(*args)
            self.my_listbox_res1_prec.yview(*args)
            self.my_listbox_res1_tol.yview(*args)
            self.my_listbox_res1_points.yview(*args)
            self.my_listbox_res1_unit.yview(*args)

            self.my_listbox_res2_name.yview(*args)
            self.my_listbox_res2_min.yview(*args)
            self.my_listbox_res2_max.yview(*args)
            self.my_listbox_res2_prec.yview(*args)
            self.my_listbox_res2_tol.yview(*args)
            self.my_listbox_res2_points.yview(*args)
            self.my_listbox_res2_unit.yview(*args)

            self.my_listbox_res3_name.yview(*args)
            self.my_listbox_res3_min.yview(*args)
            self.my_listbox_res3_max.yview(*args)
            self.my_listbox_res3_prec.yview(*args)
            self.my_listbox_res3_tol.yview(*args)
            self.my_listbox_res3_points.yview(*args)
            self.my_listbox_res3_unit.yview(*args)

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
        self.my_listbox_var1_unit.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)

        self.my_listbox_var2_name.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var2_min.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var2_max.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var2_prec.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var2_divby.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var2_unit.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)

        self.my_listbox_var3_name.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var3_min.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var3_max.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var3_prec.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var3_divby.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var3_unit.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)

        self.my_listbox_var4_name.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var4_min.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var4_max.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var4_prec.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var4_divby.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var4_unit.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)

        self.my_listbox_var5_name.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var5_min.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var5_max.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var5_prec.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var5_divby.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var5_unit.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)

        self.my_listbox_var6_name.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var6_min.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var6_max.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var6_prec.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var6_divby.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var6_unit.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)

        self.my_listbox_var7_name.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var7_min.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var7_max.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var7_prec.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var7_divby.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var7_unit.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)

        self.my_listbox_res1_name.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_res1_min.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_res1_max.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_res1_prec.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_res1_tol.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_res1_points.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_res1_unit.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)

        self.my_listbox_res2_name.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_res2_min.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_res2_max.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_res2_prec.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_res2_tol.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_res2_points.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_res2_unit.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)

        self.my_listbox_res3_name.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_res3_min.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_res3_max.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_res3_prec.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_res3_tol.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_res3_points.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_res3_unit.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)

        self.my_listbox_img_name.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        #self.my_listbox_img_data.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_test_time.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_oid.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)

        self.searchbox_question_difficulty = Entry(self.db_inner_frame, width=13)
        self.searchbox_question_difficulty.grid(row=1, column=2, sticky=E)
        self.tooltip.bind(self.searchbox_question_difficulty, "Nach \"Schwierigkeit\" filtern")

        self.searchbox_question_category = Entry(self.db_inner_frame, width=13)
        self.searchbox_question_category.grid(row=1, column=3, sticky=E)
        self.tooltip.bind(self.searchbox_question_category, "Nach \"Kategorie\" filtern")

        self.searchbox_question_type = Entry(self.db_inner_frame, width=13)
        self.searchbox_question_type.grid(row=1, column=4, sticky=E)
        self.tooltip.bind(self.searchbox_question_type, "Nach \"Typ\" filtern")

        self.filter_btn = Button(self.db_inner_frame, text="Filtern", command=lambda: Database.filter_database(self))
        self.filter_btn.grid(row=2, column=4, sticky=E, ipadx = 23)

        Database.show_records(self)


    def remove_database(self):
        self.frame_database.grid_forget()


    def submit(self):
        conn = sqlite3.connect('ilias_questions_db.db')
        c =conn.cursor()



        # format of duration P0Y0M0DT0H30M0S
        self.test_time = "P0Y0M0DT" + self.proc_hours_box.get() + "H" + self.proc_minutes_box.get() + "M" + self.proc_seconds_box.get() + "S"

        #Dieser String muss modifiziert werden. In der xml ist ein Zeilenumbrauch als "&lt;/p&gt;&#13;&#10;&lt;p&gt;" definiert und nur 1 Zeile!

        #print(self.picture_name)

        if self.picture_name != "EMPTY":
            # read image data in byte format
            with open(self.picture_name, 'rb') as image_file:
                self.picture_data = image_file.read()


        else:
            self.picture_name_new = "EMPTY"
            self.picture_data = "EMPTY"


        # Insert into Table
        c.execute(
            "INSERT INTO my_table VALUES ("
            ":question_difficulty, :question_category, :question_type, "
            ":question_title, :question_title_description, :question_description_main, "
            ":res1_formula, :res2_formula, :res3_formula,  "
            ":var1_name, :var1_min, :var1_max, :var1_prec, :var1_divby, :var1_unit, "
            ":var2_name, :var2_min, :var2_max, :var2_prec, :var2_divby, :var2_unit, "
            ":var3_name, :var3_min, :var3_max, :var3_prec, :var3_divby, :var3_unit, "
            ":var4_name, :var4_min, :var4_max, :var4_prec, :var4_divby, :var4_unit, "
            ":var5_name, :var5_min, :var5_max, :var5_prec, :var5_divby, :var5_unit, "
            ":var6_name, :var6_min, :var6_max, :var6_prec, :var6_divby, :var6_unit, "
            ":var7_name, :var7_min, :var7_max, :var7_prec, :var7_divby, :var7_unit,"
            ":res1_name, :res1_min, :res1_max, :res1_prec, :res1_tol, :res1_points, :res1_unit, "
            ":res2_name, :res2_min, :res2_max, :res2_prec, :res2_tol, :res2_points, :res2_unit, "
            ":res3_name, :res3_min, :res3_max, :res3_prec, :res3_tol, :res3_points, :res3_unit,"
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
                'var1_unit': self.var1_unit_myCombo.get(),

                'var2_name': self.var2_name_text.get(),
                'var2_min': self.var2_min_text.get(),
                'var2_max': self.var2_max_text.get(),
                'var2_prec': self.var2_prec_text.get(),
                'var2_divby': self.var2_divby_text.get(),
                'var2_unit': self.var2_unit_myCombo.get(),

                'var3_name': self.var3_name_text.get(),
                'var3_min': self.var3_min_text.get(),
                'var3_max': self.var3_max_text.get(),
                'var3_prec': self.var3_prec_text.get(),
                'var3_divby': self.var3_divby_text.get(),
                'var3_unit': self.var3_unit_myCombo.get(),

                'var4_name': self.var4_name_text.get(),
                'var4_min': self.var4_min_text.get(),
                'var4_max': self.var4_max_text.get(),
                'var4_prec': self.var4_prec_text.get(),
                'var4_divby': self.var4_divby_text.get(),
                'var4_unit': self.var4_unit_myCombo.get(),

                'var5_name': self.var5_name_text.get(),
                'var5_min': self.var5_min_text.get(),
                'var5_max': self.var5_max_text.get(),
                'var5_prec': self.var5_prec_text.get(),
                'var5_divby': self.var5_divby_text.get(),
                'var5_unit': self.var5_unit_myCombo.get(),

                'var6_name': self.var6_name_text.get(),
                'var6_min': self.var6_min_text.get(),
                'var6_max': self.var6_max_text.get(),
                'var6_prec': self.var6_prec_text.get(),
                'var6_divby': self.var6_divby_text.get(),
                'var6_unit': self.var6_unit_myCombo.get(),

                'var7_name': self.var7_name_text.get(),
                'var7_min': self.var7_min_text.get(),
                'var7_max': self.var7_max_text.get(),
                'var7_prec': self.var7_prec_text.get(),
                'var7_divby': self.var7_divby_text.get(),
                'var7_unit': self.var7_unit_myCombo.get(),

                'res1_name': self.res1_name_text.get(),
                'res1_min': self.res1_min_text.get(),
                'res1_max': self.res1_max_text.get(),
                'res1_prec': self.res1_prec_text.get(),
                'res1_tol': self.res1_tol_text.get(),
                'res1_points': self.res1_points_text.get(),
                'res1_unit': self.res1_unit_myCombo.get(),

                'res2_name': self.res2_name_text.get(),
                'res2_min': self.res2_min_text.get(),
                'res2_max': self.res2_max_text.get(),
                'res2_prec': self.res2_prec_text.get(),
                'res2_tol': self.res2_tol_text.get(),
                'res2_points': self.res2_points_text.get(),
                'res2_unit': self.res2_unit_myCombo.get(),

                'res3_name': self.res3_name_text.get(),
                'res3_min': self.res3_min_text.get(),
                'res3_max': self.res3_max_text.get(),
                'res3_prec': self.res3_prec_text.get(),
                'res3_tol': self.res3_tol_text.get(),
                'res3_points': self.res3_points_text.get(),
                'res3_unit': self.res3_unit_myCombo.get(),

                'img_name': self.picture_name_new,
                'img_data': self.picture_data,

                'test_time': self.test_time
            }
        )
        conn.commit()
        conn.close()

    def load(self):
        conn = sqlite3.connect('ilias_questions_db.db')
        c = conn.cursor()
        record_id = self.load_box.get()
        c.execute("SELECT * FROM my_table WHERE oid =" + record_id)
        records = c.fetchall()

        self.question_difficulty_entry.delete(0, END)
        self.question_category_entry.delete(0, END)
        self.question_type_entry.delete(0, END)

        self.question_title_entry.delete(0, END)
        self.question_description_entry.delete(0, END)
        self.formula_question_entry.delete('1.0', 'end-1c')

        self.res1_formula_entry.delete(0, END)
        self.res2_formula_entry.delete(0, END)
        self.res3_formula_entry.delete(0, END)

        self.var1_name_entry.delete(0, END)
        self.var1_min_entry.delete(0, END)
        self.var1_max_entry.delete(0, END)
        self.var1_prec_entry.delete(0, END)
        self.var1_divby_entry.delete(0, END)

        self.var2_name_entry.delete(0, END)
        self.var2_min_entry.delete(0, END)
        self.var2_max_entry.delete(0, END)
        self.var2_prec_entry.delete(0, END)
        self.var2_divby_entry.delete(0, END)

        self.var3_name_entry.delete(0, END)
        self.var3_min_entry.delete(0, END)
        self.var3_max_entry.delete(0, END)
        self.var3_prec_entry.delete(0, END)
        self.var3_divby_entry.delete(0, END)

        self.var4_name_entry.delete(0, END)
        self.var4_min_entry.delete(0, END)
        self.var4_max_entry.delete(0, END)
        self.var4_prec_entry.delete(0, END)
        self.var4_divby_entry.delete(0, END)

        self.var5_name_entry.delete(0, END)
        self.var5_min_entry.delete(0, END)
        self.var5_max_entry.delete(0, END)
        self.var5_prec_entry.delete(0, END)
        self.var5_divby_entry.delete(0, END)

        self.var6_name_entry.delete(0, END)
        self.var6_min_entry.delete(0, END)
        self.var6_max_entry.delete(0, END)
        self.var6_prec_entry.delete(0, END)
        self.var6_divby_entry.delete(0, END)

        self.var7_name_entry.delete(0, END)
        self.var7_min_entry.delete(0, END)
        self.var7_max_entry.delete(0, END)
        self.var7_prec_entry.delete(0, END)
        self.var7_divby_entry.delete(0, END)

        self.res1_name_entry.delete(0, END)
        self.res1_min_entry.delete(0, END)
        self.res1_max_entry.delete(0, END)
        self.res1_prec_entry.delete(0, END)
        self.res1_tol_entry.delete(0, END)
        self.res1_points_entry.delete(0, END)

        self.res2_name_entry.delete(0, END)
        self.res2_min_entry.delete(0, END)
        self.res2_max_entry.delete(0, END)
        self.res2_prec_entry.delete(0, END)
        self.res2_tol_entry.delete(0, END)
        self.res2_points_entry.delete(0, END)

        self.res3_name_entry.delete(0, END)
        self.res3_min_entry.delete(0, END)
        self.res3_max_entry.delete(0, END)
        self.res3_prec_entry.delete(0, END)
        self.res3_tol_entry.delete(0, END)
        self.res3_points_entry.delete(0, END)


        for record in records:
            self.question_difficulty_entry.insert(END, record[0])
            self.question_category_entry.insert(END, record[1])
            self.question_type_entry.insert(END, record[2])

            self.question_title_entry.insert(END, record[3])
            self.question_description_entry.insert(END, record[4])
            self.formula_question_entry.insert(END, record[5])

            self.res1_formula_entry.insert(END, record[6])
            self.res2_formula_entry.insert(END, record[7])
            self.res3_formula_entry.insert(END, record[8])

            self.var1_name_entry.insert(END, record[9])
            self.var1_min_entry.insert(END, record[10])
            self.var1_max_entry.insert(END, record[11])
            self.var1_prec_entry.insert(END, record[12])
            self.var1_divby_entry.insert(END, record[13])
            self.var1_unit_myCombo.set(record[14])

            self.var2_name_entry.insert(END, record[15])
            self.var2_min_entry.insert(END, record[16])
            self.var2_max_entry.insert(END, record[17])
            self.var2_prec_entry.insert(END, record[18])
            self.var2_divby_entry.insert(END, record[19])
            self.var2_unit_myCombo.set(record[20])

            self.var3_name_entry.insert(END, record[21])
            self.var3_min_entry.insert(END, record[22])
            self.var3_max_entry.insert(END, record[23])
            self.var3_prec_entry.insert(END, record[24])
            self.var3_divby_entry.insert(END, record[25])
            self.var3_unit_myCombo.set(record[26])

            self.var4_name_entry.insert(END, record[27])
            self.var4_min_entry.insert(END, record[28])
            self.var4_max_entry.insert(END, record[29])
            self.var4_prec_entry.insert(END, record[30])
            self.var4_divby_entry.insert(END, record[31])
            self.var4_unit_myCombo.set(record[32])

            self.var5_name_entry.insert(END, record[33])
            self.var5_min_entry.insert(END, record[34])
            self.var5_max_entry.insert(END, record[35])
            self.var5_prec_entry.insert(END, record[36])
            self.var5_divby_entry.insert(END, record[37])
            self.var5_unit_myCombo.set(record[38])

            self.var6_name_entry.insert(END, record[39])
            self.var6_min_entry.insert(END, record[40])
            self.var6_max_entry.insert(END, record[41])
            self.var6_prec_entry.insert(END, record[42])
            self.var6_divby_entry.insert(END, record[43])
            self.var6_unit_myCombo.set(record[44])

            self.var7_name_entry.insert(END, record[45])
            self.var7_min_entry.insert(END, record[46])
            self.var7_max_entry.insert(END, record[47])
            self.var7_prec_entry.insert(END, record[48])
            self.var7_divby_entry.insert(END, record[49])
            self.var7_unit_myCombo.set(record[50])

            self.res1_name_entry.insert(END, record[51])
            self.res1_min_entry.insert(END, record[52])
            self.res1_max_entry.insert(END, record[53])
            self.res1_prec_entry.insert(END, record[54])
            self.res1_tol_entry.insert(END, record[55])
            self.res1_points_entry.insert(END, record[56])
            self.res1_unit_myCombo.set(record[57])

            self.res2_name_entry.insert(END, record[58])
            self.res2_min_entry.insert(END, record[59])
            self.res2_max_entry.insert(END, record[60])
            self.res2_prec_entry.insert(END, record[61])
            self.res2_tol_entry.insert(END, record[62])
            self.res2_points_entry.insert(END, record[63])
            self.res2_unit_myCombo.set(record[64])

            self.res3_name_entry.insert(END, record[65])
            self.res3_min_entry.insert(END, record[66])
            self.res3_max_entry.insert(END, record[67])
            self.res3_prec_entry.insert(END, record[68])
            self.res3_tol_entry.insert(END, record[69])
            self.res3_points_entry.insert(END, record[70])
            self.res3_unit_myCombo.set(record[71])

        conn.commit()
        conn.close()

    def show_records(self):

        conn = sqlite3.connect('ilias_questions_db.db')
        c = conn.cursor()

        c.execute("SELECT *, oid FROM my_table")
        records = c.fetchall()

        # Clear List Boxes
        Database.clear_listboxes(self)


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
            self.my_listbox_var1_unit.insert(END, record[14])

            self.my_listbox_var2_name.insert(END, record[15])
            self.my_listbox_var2_min.insert(END, record[16])
            self.my_listbox_var2_max.insert(END, record[17])
            self.my_listbox_var2_prec.insert(END, record[18])
            self.my_listbox_var2_divby.insert(END, record[19])
            self.my_listbox_var2_unit.insert(END, record[20])

            self.my_listbox_var3_name.insert(END, record[21])
            self.my_listbox_var3_min.insert(END, record[22])
            self.my_listbox_var3_max.insert(END, record[23])
            self.my_listbox_var3_prec.insert(END, record[24])
            self.my_listbox_var3_divby.insert(END, record[25])
            self.my_listbox_var3_unit.insert(END, record[26])

            self.my_listbox_var4_name.insert(END, record[27])
            self.my_listbox_var4_min.insert(END, record[28])
            self.my_listbox_var4_max.insert(END, record[29])
            self.my_listbox_var4_prec.insert(END, record[30])
            self.my_listbox_var4_divby.insert(END, record[31])
            self.my_listbox_var4_unit.insert(END, record[32])

            self.my_listbox_var5_name.insert(END, record[33])
            self.my_listbox_var5_min.insert(END, record[34])
            self.my_listbox_var5_max.insert(END, record[35])
            self.my_listbox_var5_prec.insert(END, record[36])
            self.my_listbox_var5_divby.insert(END, record[37])
            self.my_listbox_var5_unit.insert(END, record[38])

            self.my_listbox_var6_name.insert(END, record[39])
            self.my_listbox_var6_min.insert(END, record[40])
            self.my_listbox_var6_max.insert(END, record[41])
            self.my_listbox_var6_prec.insert(END, record[42])
            self.my_listbox_var6_divby.insert(END, record[43])
            self.my_listbox_var6_unit.insert(END, record[44])

            self.my_listbox_var7_name.insert(END, record[45])
            self.my_listbox_var7_min.insert(END, record[46])
            self.my_listbox_var7_max.insert(END, record[47])
            self.my_listbox_var7_prec.insert(END, record[48])
            self.my_listbox_var7_divby.insert(END, record[49])
            self.my_listbox_var7_unit.insert(END, record[50])

            self.my_listbox_res1_name.insert(END, record[51])
            self.my_listbox_res1_min.insert(END, record[52])
            self.my_listbox_res1_max.insert(END, record[53])
            self.my_listbox_res1_prec.insert(END, record[54])
            self.my_listbox_res1_tol.insert(END, record[55])
            self.my_listbox_res1_points.insert(END, record[56])
            self.my_listbox_res1_unit.insert(END, record[57])

            self.my_listbox_res2_name.insert(END, record[58])
            self.my_listbox_res2_min.insert(END, record[59])
            self.my_listbox_res2_max.insert(END, record[60])
            self.my_listbox_res2_prec.insert(END, record[61])
            self.my_listbox_res2_tol.insert(END, record[62])
            self.my_listbox_res2_points.insert(END, record[63])
            self.my_listbox_res2_unit.insert(END, record[64])

            self.my_listbox_res3_name.insert(END, record[65])
            self.my_listbox_res3_min.insert(END, record[66])
            self.my_listbox_res3_max.insert(END, record[67])
            self.my_listbox_res3_prec.insert(END, record[68])
            self.my_listbox_res3_tol.insert(END, record[69])
            self.my_listbox_res3_points.insert(END, record[70])
            self.my_listbox_res3_unit.insert(END, record[71])

            self.my_listbox_img_name.insert(END, record[72])
            #self.my_listbox_img_data.insert(END, record[63])
            #img_data slows "show records" down, therefore not inserted

            self.my_listbox_test_time.insert(END, record[74])
            self.my_listbox_oid.insert(END, record[75])

        conn.commit()
        conn.close()


    def delete(self):

        conn = sqlite3.connect('ilias_questions_db.db')
        c = conn.cursor()

        c.execute("DELETE from my_table WHERE oid= " + self.delete_box.get())

        self.delete_box.delete(0, END)

        conn.commit()
        conn.close()

        #Database.show_records(self)

    def open_image(self):
        #global file_image  # needs to be global to print Image to Desktop
        #global filename_label
        #global file_image_label


        try:
            app.filename = filedialog.askopenfilename(initialdir="/", title="Select a File")
            self.picture_name = app.filename
            self.sorted_picture_name = self.picture_name
            self.last_char_index = self.sorted_picture_name.rfind("/")
            self.foo = ([pos for pos, char in enumerate(self.sorted_picture_name) if char == '/'])
            self.foo_len = len(self.foo)
            self.picture_name_new = self.sorted_picture_name[self.foo[self.foo_len - 1] + 1:-4]   #letzten char des bildnamens ist das dateiformat: Testbild.jpg
            self.image_format_new = self.picture_name[-4:]

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



    #def save_image_to_db(self):
        #print("SAVE_to_IMG called")
        #conn = sqlite3.connect('ilias_questions_db.db')
        #c = conn.cursor()
        #self.img_name = self.app_filename
        #print("img1" + self.img_name)
        #self.s = self.img_name
        #self.last_char_index = self.s.rfind("/")
        #print(self.s)
        #self.foo = ([pos for pos, char in enumerate(self.s) if char == '/'])
        #print(self.foo)
        #print(len(self.s))
        #self.foo_len = len(self.foo)
       # print("NEW TRY")
        #self.img_name_new = self.s[self.foo[self.foo_len-1]+1:]
        #with open(self.img_name, 'rb') as f:
        #    self.img_data = f.read()
        #c.execute("""
        #    INSERT INTO my_table (img_name, img_data) VALUES (?,?)""", (self.img_name_new, self.img_data))
        #conn.commit()
        #conn.close()


    def show_img_from_db(self):
        conn = sqlite3.connect('ilias_questions_db.db')
        c = conn.cursor()

        records = c.execute("""
            SELECT *, oid FROM my_table
        """)


        for record in records:

            if str(record[len(record) - 1]) == self.create_formelfrage_entry.get():

                #print(record[63])

                self.rec_data = record[73]  #record[63] -> img_data_raw (as byte)

                #Picture need to have the name"il_0_mob_xxxxxxx" for ilias to work
                with open('il_0_mob_TEST.png', 'wb') as image_file:
                    image_file.write(self.rec_data)


                self.picture_name = "il_0_mob_TEST.png"
                self.db_file_image = ImageTk.PhotoImage(Image.open(self.picture_name).resize((250, 250)))
                self.db_file_image_label = Label(self.frame_db_picture, image=self.db_file_image)
                self.db_file_image_label.image = self.db_file_image
                self.db_file_image_label.grid(row=2, column=0)

        conn.commit()
        conn.close()


    def filter_database(self):
        conn = sqlite3.connect('ilias_questions_db.db')
        c = conn.cursor()
        c.execute("SELECT *, oid FROM my_table")
        records = c.fetchall()

        self.search_term_difficulty = self.searchbox_question_difficulty.get()
        self.search_term_category = self.searchbox_question_category.get()
        self.search_term_type = self.searchbox_question_type.get()

        Database.clear_listboxes(self)

        for record in records:

            if self.search_term_difficulty != "":
                if record[0].lower() == self.search_term_difficulty.lower():
                    Database.insert_to_database(self, record)

            elif self.search_term_category != "":
                if record[1].lower() == self.search_term_category.lower():
                    Database.insert_to_database(self, record)

            elif self.search_term_type != "":
                if record[2].lower() == self.search_term_type.lower():
                    Database.insert_to_database(self, record)

            elif self.search_term_difficulty != "" and self.search_term_category != "":
                if record[0].lower() == self.search_term_difficulty.lower() and record[1].lower() == self.search_term_category.lower():
                    Database.insert_to_database(self, record)

            elif self.search_term_difficulty != "" and self.search_term_type != "":
                if record[0].lower() == self.search_term_difficulty.lower() and record[2].lower() == self.search_term_type.lower():
                    Database.insert_to_database(self, record)

            elif self.search_term_category != "" and self.search_term_type != "":
                if record[1].lower() == self.search_term_category.lower() and record[2].lower() == self.search_term_type.lower():
                    Database.insert_to_database(self, record)

            elif self.search_term_difficulty != "" and self.search_term_category != "" and self.search_term_type != "":
                if record[0].lower() == self.search_term_difficulty.lower() and record[1].lower() == self.search_term_category.lower() and record[2].lower() == self.search_term_type.lower():
                    Database.insert_to_database(self, record)

            else:
                Database.show_records(self)

        conn.commit()
        conn.close()

    def clear_listboxes(self):
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
        self.my_listbox_var1_unit.delete(0, END)

        self.my_listbox_var2_name.delete(0, END)
        self.my_listbox_var2_min.delete(0, END)
        self.my_listbox_var2_max.delete(0, END)
        self.my_listbox_var2_prec.delete(0, END)
        self.my_listbox_var2_divby.delete(0, END)
        self.my_listbox_var2_unit.delete(0, END)

        self.my_listbox_var3_name.delete(0, END)
        self.my_listbox_var3_min.delete(0, END)
        self.my_listbox_var3_max.delete(0, END)
        self.my_listbox_var3_prec.delete(0, END)
        self.my_listbox_var3_divby.delete(0, END)
        self.my_listbox_var3_unit.delete(0, END)

        self.my_listbox_var4_name.delete(0, END)
        self.my_listbox_var4_min.delete(0, END)
        self.my_listbox_var4_max.delete(0, END)
        self.my_listbox_var4_prec.delete(0, END)
        self.my_listbox_var4_divby.delete(0, END)
        self.my_listbox_var4_unit.delete(0, END)

        self.my_listbox_var5_name.delete(0, END)
        self.my_listbox_var5_min.delete(0, END)
        self.my_listbox_var5_max.delete(0, END)
        self.my_listbox_var5_prec.delete(0, END)
        self.my_listbox_var5_divby.delete(0, END)
        self.my_listbox_var5_unit.delete(0, END)

        self.my_listbox_var6_name.delete(0, END)
        self.my_listbox_var6_min.delete(0, END)
        self.my_listbox_var6_max.delete(0, END)
        self.my_listbox_var6_prec.delete(0, END)
        self.my_listbox_var6_divby.delete(0, END)
        self.my_listbox_var6_unit.delete(0, END)

        self.my_listbox_var7_name.delete(0, END)
        self.my_listbox_var7_min.delete(0, END)
        self.my_listbox_var7_max.delete(0, END)
        self.my_listbox_var7_prec.delete(0, END)
        self.my_listbox_var7_divby.delete(0, END)
        self.my_listbox_var7_unit.delete(0, END)

        self.my_listbox_res1_name.delete(0, END)
        self.my_listbox_res1_min.delete(0, END)
        self.my_listbox_res1_max.delete(0, END)
        self.my_listbox_res1_prec.delete(0, END)
        self.my_listbox_res1_tol.delete(0, END)
        self.my_listbox_res1_points.delete(0, END)
        self.my_listbox_res1_unit.delete(0, END)

        self.my_listbox_res2_name.delete(0, END)
        self.my_listbox_res2_min.delete(0, END)
        self.my_listbox_res2_max.delete(0, END)
        self.my_listbox_res2_prec.delete(0, END)
        self.my_listbox_res2_tol.delete(0, END)
        self.my_listbox_res2_points.delete(0, END)
        self.my_listbox_res2_unit.delete(0, END)

        self.my_listbox_res3_name.delete(0, END)
        self.my_listbox_res3_min.delete(0, END)
        self.my_listbox_res3_max.delete(0, END)
        self.my_listbox_res3_prec.delete(0, END)
        self.my_listbox_res3_tol.delete(0, END)
        self.my_listbox_res3_points.delete(0, END)
        self.my_listbox_res3_unit.delete(0, END)

        self.my_listbox_img_name.delete(0, END)
        self.my_listbox_img_data.delete(0, END)

        self.my_listbox_test_time.delete(0, END)
        self.my_listbox_oid.delete(0, END)

    def insert_to_database(self, record):

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
        self.my_listbox_var1_unit.insert(END, record[14])

        self.my_listbox_var2_name.insert(END, record[15])
        self.my_listbox_var2_min.insert(END, record[16])
        self.my_listbox_var2_max.insert(END, record[17])
        self.my_listbox_var2_prec.insert(END, record[18])
        self.my_listbox_var2_divby.insert(END, record[19])
        self.my_listbox_var1_unit.insert(END, record[20])

        self.my_listbox_var3_name.insert(END, record[21])
        self.my_listbox_var3_min.insert(END, record[22])
        self.my_listbox_var3_max.insert(END, record[23])
        self.my_listbox_var3_prec.insert(END, record[24])
        self.my_listbox_var3_divby.insert(END, record[25])
        self.my_listbox_var1_unit.insert(END, record[26])

        self.my_listbox_var4_name.insert(END, record[27])
        self.my_listbox_var4_min.insert(END, record[28])
        self.my_listbox_var4_max.insert(END, record[29])
        self.my_listbox_var4_prec.insert(END, record[30])
        self.my_listbox_var4_divby.insert(END, record[31])
        self.my_listbox_var1_unit.insert(END, record[32])

        self.my_listbox_var5_name.insert(END, record[33])
        self.my_listbox_var5_min.insert(END, record[34])
        self.my_listbox_var5_max.insert(END, record[35])
        self.my_listbox_var5_prec.insert(END, record[36])
        self.my_listbox_var5_divby.insert(END, record[37])
        self.my_listbox_var1_unit.insert(END, record[38])

        self.my_listbox_var6_name.insert(END, record[39])
        self.my_listbox_var6_min.insert(END, record[40])
        self.my_listbox_var6_max.insert(END, record[41])
        self.my_listbox_var6_prec.insert(END, record[42])
        self.my_listbox_var6_divby.insert(END, record[43])
        self.my_listbox_var1_unit.insert(END, record[44])

        self.my_listbox_var7_name.insert(END, record[45])
        self.my_listbox_var7_min.insert(END, record[46])
        self.my_listbox_var7_max.insert(END, record[47])
        self.my_listbox_var7_prec.insert(END, record[48])
        self.my_listbox_var7_divby.insert(END, record[49])
        self.my_listbox_var1_unit.insert(END, record[50])

        self.my_listbox_res1_name.insert(END, record[51])
        self.my_listbox_res1_min.insert(END, record[52])
        self.my_listbox_res1_max.insert(END, record[53])
        self.my_listbox_res1_prec.insert(END, record[54])
        self.my_listbox_res1_tol.insert(END, record[55])
        self.my_listbox_res1_points.insert(END, record[56])
        self.my_listbox_var1_unit.insert(END, record[57])

        self.my_listbox_res2_name.insert(END, record[58])
        self.my_listbox_res2_min.insert(END, record[59])
        self.my_listbox_res2_max.insert(END, record[60])
        self.my_listbox_res2_prec.insert(END, record[61])
        self.my_listbox_res2_tol.insert(END, record[62])
        self.my_listbox_res2_points.insert(END, record[63])
        self.my_listbox_var1_unit.insert(END, record[64])

        self.my_listbox_res3_name.insert(END, record[65])
        self.my_listbox_res3_min.insert(END, record[66])
        self.my_listbox_res3_max.insert(END, record[67])
        self.my_listbox_res3_prec.insert(END, record[68])
        self.my_listbox_res3_tol.insert(END, record[69])
        self.my_listbox_res3_points.insert(END, record[70])
        self.my_listbox_var1_unit.insert(END, record[71])

        self.my_listbox_img_name.insert(END, record[72])
        # self.my_listbox_img_data.insert(END, record[63])
        # img_data slows "show records" down, therefore not inserted
        self.my_listbox_test_time.insert(END, record[74])
        self.my_listbox_oid.insert(END, record[75])

class LatexPreview(Formelfrage):

    def __init__(self):
        self.latex_preview_window = Toplevel()
        self.latex_frame = LabelFrame(self.latex_preview_window, text="LaTeX-Preview", padx=5, pady=5)
        self.latex_frame.grid(row=0, column=0, padx=10, pady=10, sticky=NW)

        self.latex_textblock_1_label = Label(self.latex_frame, text="Textblock 1:", width=40)
        self.latex_textblock_1_label.grid(row=0, column=0, pady=(10, 0))
        self.latex_textblock_1_entry = Entry(self.latex_frame, width=60)
        self.latex_textblock_1_entry.grid(row=1, column=0)

        self.latex_formelblock_1_label = Label(self.latex_frame, text="Formelblock 1:", width=40)
        self.latex_formelblock_1_label.grid(row=2, column=0, pady=(10, 0))
        self.latex_formelblock_1_entry = Entry(self.latex_frame, width=60)
        self.latex_formelblock_1_entry.grid(row=3, column=0)

        self.latex_textblock_2_label = Label(self.latex_frame, text="Textblock 2:", width=40)
        self.latex_textblock_2_label.grid(row=4, column=0, pady=(10, 0))
        self.latex_textblock_2_entry = Entry(self.latex_frame, width=60)
        self.latex_textblock_2_entry.grid(row=5, column=0)

        self.latex_formelblock_2_label = Label(self.latex_frame, text="Formelblock 2:", width=40)
        self.latex_formelblock_2_label.grid(row=6, column=0, pady=(10, 0))
        self.latex_formelblock_2_entry = Entry(self.latex_frame, width=60)
        self.latex_formelblock_2_entry.grid(row=7, column=0)

        self.latex_preview_btn = Button(self.latex_frame, text="show LaTeX preview", command=lambda: LatexPreview.show_latex_preview(self))
        self.latex_preview_btn.grid(row=10, ipadx=100, pady=10)

        self.latex_preview_btn = Button(self.latex_frame, text="clear LaTeX preview",command=lambda: LatexPreview.clear_latex_preview(self))
        self.latex_preview_btn.grid(row=11, ipadx=100, pady=10)



    def show_latex_preview(self):
        self.latex = r"{\text{" + str(self.latex_textblock_1_entry.get()) +"}}\ {"+ str(self.latex_formelblock_1_entry.get()) + "}\ {\\text{" + str(self.latex_textblock_2_entry.get()) + "}}\ {" + str(self.latex_formelblock_2_entry.get()) + "}"
        self.expr = r'$$' + self.latex + '$$'
        preview(self.expr, viewer='file', filename='LaTeX-Preview.png')

        self.file_image = ImageTk.PhotoImage(Image.open('LaTeX-Preview.png'))
        self.file_image_label = Label(self.latex_preview_window, image=self.file_image)
        self.file_image_label.image = self.file_image

        self.file_image_label.grid(row=20, column=0, pady=20)

    def clear_latex_preview(self):
        self.file_image_label.grid_forget()





class create_formelfrage(Formelfrage):

    def __init__(self):

        self.mytree = ET.parse(self.tst_file_path_read)
        self.myroot = self.mytree.getroot()

        for title in self.myroot.iter('Title'):
            title.text = self.test_title_entry.get()
            if title.text == "":
                title.text = "DEFAULT"

        self.mytree.write(self.tst_file_path_write)



        # ----------------------------------- Datei .xml Einlesen
       #self.mytree = ET.parse("xml_form_orig\\" + '1590230409__0__qti_1948621.xml')
        self.mytree = ET.parse(self.qti_file_path_read)
        self.myroot = self.mytree.getroot()

        self.frame_create = LabelFrame(self.formula_tab, text="Create Formelfrage", padx=5, pady=5)
        self.frame_create.grid(row=1, column=2)

        self.entry_split = self.create_formelfrage_entry.get()
        self.entry_split = self.entry_split.split(",")

        #print(self.entry_split[0])
        #print(len(self.entry_split))

        conn = sqlite3.connect('ilias_questions_db.db')
        c = conn.cursor()
        c.execute("SELECT *, oid FROM my_table")

        records = c.fetchall()


        for x in range(len(self.entry_split)):
            for record in records:
                if str(record[len(record) - 1]) == self.entry_split[x]:
                    if record[2].lower() == "formelfrage":
                        print("formelfrage found!")


                        self.question_difficulty = str(record[0])
                        self.question_category = str(record[1])
                        self.question_type = str(record[2])

                        self.question_title = str(record[3])
                        self.question_description_title = str(record[4])
                        self.question_description_main_raw = str(record[5])
                        self.formula_question_entry_multi_replaced = self.question_description_main_raw.replace('\n', "&lt;/p&gt;&#13;&#10;&lt;p&gt;")
                        self.question_description_main_test = self.formula_question_entry_multi_replaced
                        self.question_description_main_latex1 = self.question_description_main_test.replace('\\)', "</span>")
                        self.question_description_main = self.question_description_main_latex1.replace('\\(', "<span class=\"latex\">")

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
                        self.var1_unit = str(record[14])
                        self.var1_unit_length = str(len(self.var1_unit))

                        self.var2_name = str(record[15])
                        self.var2_min = str(record[16])
                        self.var2_max = str(record[17])
                        self.var2_prec = str(record[18])
                        self.var2_divby = str(record[19])
                        self.var2_divby_length = str(len(self.var2_divby))
                        self.var2_unit = str(record[20])
                        self.var2_unit_length = str(len(self.var2_unit))

                        self.var3_name = str(record[21])
                        self.var3_min = str(record[22])
                        self.var3_max = str(record[23])
                        self.var3_prec = str(record[24])
                        self.var3_divby = str(record[25])
                        self.var3_divby_length = str(len(self.var3_divby))
                        self.var3_unit = str(record[26])
                        self.var3_unit_length = str(len(self.var3_unit))

                        self.var4_name = str(record[27])
                        self.var4_min = str(record[28])
                        self.var4_max = str(record[29])
                        self.var4_prec = str(record[30])
                        self.var4_divby = str(record[31])
                        self.var4_divby_length = str(len(self.var4_divby))
                        self.var4_unit = str(record[32])
                        self.var4_unit_length = str(len(self.var4_unit))

                        self.var5_name = str(record[33])
                        self.var5_min = str(record[34])
                        self.var5_max = str(record[35])
                        self.var5_prec = str(record[36])
                        self.var5_divby = str(record[37])
                        self.var5_divby_length = str(len(self.var5_divby))
                        self.var5_unit = str(record[38])
                        self.var5_unit_length = str(len(self.var5_unit))

                        self.var6_name = str(record[39])
                        self.var6_min = str(record[40])
                        self.var6_max = str(record[41])
                        self.var6_prec = str(record[42])
                        self.var6_divby = str(record[43])
                        self.var6_divby_length = str(len(self.var6_divby))
                        self.var6_unit = str(record[44])
                        self.var6_unit_length = str(len(self.var6_unit))

                        self.var7_name = str(record[45])
                        self.var7_min = str(record[46])
                        self.var7_max = str(record[47])
                        self.var7_prec = str(record[48])
                        self.var7_divby = str(record[49])
                        self.var7_divby_length = str(len(self.var7_divby))
                        self.var7_unit = str(record[50])
                        self.var7_unit_length = str(len(self.var7_unit))

                        self.res1_name = str(record[51])
                        self.res1_min = str(record[52])
                        self.res1_min_length = str(len(self.res1_min))
                        self.res1_max = str(record[53])
                        self.res1_max_length = str(len(self.res1_max))
                        self.res1_prec = str(record[54])
                        self.res1_tol = str(record[55])
                        self.res1_tol_length = str(len(self.res1_tol))
                        self.res1_points = str(record[56])
                        self.res1_unit = str(record[57])
                        self.res1_unit_length = str(len(self.res1_unit))


                        self.res2_name = str(record[58])
                        self.res2_min = str(record[59])
                        self.res2_min_length = str(len(self.res2_min))
                        self.res2_max = str(record[60])
                        self.res2_max_length = str(len(self.res2_max))
                        self.res2_prec = str(record[61])
                        self.res2_tol = str(record[62])
                        self.res2_tol_length = str(len(self.res2_tol))
                        self.res2_points = str(record[63])
                        self.res2_unit = str(record[64])
                        self.res2_unit_length = str(len(self.res2_unit))


                        self.res3_name = str(record[65])
                        self.res3_min = str(record[66])
                        self.res3_min_length = str(len(self.res3_min))
                        self.res3_max = str(record[67])
                        self.res3_max_length = str(len(self.res3_max))
                        self.res3_prec = str(record[68])
                        self.res3_tol = str(record[69])
                        self.res3_tol_length = str(len(self.res3_tol))
                        self.res3_points = str(record[70])
                        self.res3_unit = str(record[71])
                        self.res3_unit_length = str(len(self.res3_unit))

                        self.img_name = str(record[72])
                        self.img_data_raw = record[73]
                        self.img_data = str(record[73])

                        self.test_time = str(record[74])

                        self.oid = str(record[len(record)-1]) #oid ist IMMER letztes Fach
                        create_formelfrage.create_question(self, x)  #
                        print("Formelfrage generated with Title:")
                        print(self.question_title)
                        print("\n")


                    elif record[2].lower() == "multiple choice":
                        print("Question type with 'multiple choice' found")
                        create_multiplechoice.create_mc_question(MultipleChoice,self.mytree, self.myroot, self.qti_file_path_read, self.qti_file_path_write, self.entry_split, x)
                # create_formelfrage.create_question(self, x)   LAST CHANGE
        conn.commit()
        conn.close()


    def create_question(self, x):
        # print("IN CREATE QUESTION")
        # print(Formelfrage.unit_table(self, self.var1_unit_myCombo.get()))
        # print(self.var1_unit_myCombo.get())
        # print("IN CREATE QUESTION")

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

        createFolder(self.img_file_path_create_folder + 'il_0_mob_000000' + str(x) + '/')


        for record in records:

            #Ohne If Abfrage werden ALLE Fragen aus der Datenbank erstellt
            if str(record[len(record)-1]) == self.entry_split[x]:

                if self.img_data_raw != "EMPTY":
                    #img wird immer als PNG Datei abgelegt.
                    with open(self.img_file_path + "\\il_0_mob_000000" + str(x) + "\\" + self.img_name + ".png", 'wb') as image_file:
                        image_file.write(self.img_data_raw)

                    self.image = Image.open(self.img_file_path + "\\il_0_mob_000000" + str(x) + "\\" + self.img_name + ".png")
                    self.image.save(self.img_file_path + "\\il_0_mob_000000" + str(x) + "\\" + self.img_name + ".png")





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


                # append ITEM in the last "myroot"-Element. Here it is Element "section" in myroot
                self.myroot[0][len(self.myroot[0])-1].append(item)



                if duration.text == "":
                    duration.text = "P0Y0M0DT1H0M0S"


                for assessment in self.myroot.iter('assessment'):


                    assessment.set('title', str(self.test_title_entry.get()))

                    if assessment.get('title') == "":
                        assessment.set('title', "DEFAULT")


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
                # -----------------------------------------------------------------------POINTS
                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "points"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
                fieldentry.text = str(self.res1_points)
                # -----------------------------------------------------------------------Variables and Results
                #
                # To prevent the program to crash when no units are selected for ALL variables and results
                # those will be by default selected as "H" - Henry

                if self.var1_unit == "Unit":
                    self.var1_unit = ""
                    self.var1_unit_length = len(self.var1_unit)


                if self.var2_unit == "Unit":
                    self.var2_unit = ""
                    self.var2_unit_length = len(self.var2_unit)


                if self.var3_unit == "Unit":
                    self.var3_unit = ""
                    self.var3_unit_length = len(self.var3_unit)


                if self.var4_unit == "Unit":
                    self.var4_unit = ""
                    self.var4_unit_length = len(self.var4_unit)


                if self.var5_unit == "Unit":
                    self.var5_unit = ""
                    self.var5_unit_length = len(self.var5_unit)


                if self.var6_unit == "Unit":
                    self.var6_unit = ""
                    self.var6_unit_length = len(self.var6_unit)


                if self.var7_unit == "Unit":
                    self.var7_unit = ""
                    self.var7_unit_length = len(self.var7_unit)


                if self.res1_unit == "Unit":
                    self.res1_unit = ""
                    self.res1_unit_length = len(self.res1_unit)


                if self.res2_unit == "Unit":
                    self.res2_unit = ""
                    self.res2_unit_length = len(self.res2_unit)


                if self.res3_unit == "Unit":
                    self.res3_unit = ""
                    self.res3_unit_length = len(self.res3_unit)




                # -----------------------------------------------------------------------Variable 1

                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "$v1"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')

                if self.var1_unit != "":
                    fieldentry.text = "a:6:{" \
                                      "s:9:\"precision\";i:" + self.var1_prec + ";" \
                                      "s:12:\"intprecision\";s:" + self.var1_divby_length + ":\"" + self.var1_divby + "\";" \
                                      "s:8:\"rangemin\";d:" + self.var1_min + ";" \
                                      "s:8:\"rangemax\";d:" + self.var1_max + ";" \
                                      "s:4:\"unit\";s:" + str(self.var1_unit_length) + ":\"" + self.var1_unit + "\";" \
                                      "s:9:\"unitvalue\";s:" + str(len(Formelfrage.unit_table(self, self.var1_unit))) + ":\"" + Formelfrage.unit_table(self, self.var1_unit) + "\";" \
                                      "}"
                else:
                    fieldentry.text = "a:6:{" \
                                      "s:9:\"precision\";i:" + self.var1_prec + ";" \
                                      "s:12:\"intprecision\";s:" + self.var1_divby_length + ":\"" + self.var1_divby + "\";" \
                                      "s:8:\"rangemin\";d:" + self.var1_min + ";" \
                                      "s:8:\"rangemax\";d:" + self.var1_max + ";" \
                                      "s:4:\"unit\";s:0:\"\";" \
                                      "s:9:\"unitvalue\";s:0:\"\";" \
                                      "}"
                    print("VAR_1 no UNIT")
                # -----------------------------------------------------------------------Variable 2

                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "$v2"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')

                if self.var2_unit != "":
                    fieldentry.text = "a:6:{" \
                                      "s:9:\"precision\";i:" + self.var2_prec + ";" \
                                      "s:12:\"intprecision\";s:" + self.var2_divby_length + ":\"" + self.var2_divby + "\";" \
                                      "s:8:\"rangemin\";d:" + self.var2_min + ";" \
                                      "s:8:\"rangemax\";d:" + self.var2_max + ";" \
                                      "s:4:\"unit\";s:" + str(self.var2_unit_length) + ":\"" + self.var2_unit + "\";" \
                                      "s:9:\"unitvalue\";s:" + str(len(Formelfrage.unit_table(self, self.var2_unit))) + ":\"" + Formelfrage.unit_table(self, self.var2_unit) + "\";" \
                                      "}"
                else:
                    fieldentry.text = "a:6:{" \
                                      "s:9:\"precision\";i:" + self.var2_prec + ";" \
                                      "s:12:\"intprecision\";s:" + self.var2_divby_length + ":\"" + self.var2_divby + "\";" \
                                      "s:8:\"rangemin\";d:" + self.var2_min + ";" \
                                      "s:8:\"rangemax\";d:" + self.var2_max + ";" \
                                      "s:4:\"unit\";s:0:\"\";" \
                                      "s:9:\"unitvalue\";s:0:\"\";" \
                                      "}"
                    print("VAR_2 no UNIT")

                # -----------------------------------------------------------------------Variable 3

                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "$v3"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')

                if self.var3_unit != "":
                    fieldentry.text = "a:6:{" \
                                      "s:9:\"precision\";i:" + self.var3_prec + ";" \
                                       "s:12:\"intprecision\";s:" + self.var3_divby_length + ":\"" + self.var3_divby + "\";" \
                                       "s:8:\"rangemin\";d:" + self.var3_min + ";" \
                                       "s:8:\"rangemax\";d:" + self.var3_max + ";" \
                                       "s:4:\"unit\";s:" + str(self.var3_unit_length) + ":\"" + self.var3_unit + "\";" \
                                      "s:9:\"unitvalue\";s:" + str(len(Formelfrage.unit_table(self, self.var3_unit))) + ":\"" + Formelfrage.unit_table(self, self.var3_unit) + "\";" \
                                      "}"
                else:
                    fieldentry.text = "a:6:{" \
                                      "s:9:\"precision\";i:" + self.var3_prec + ";" \
                                      "s:12:\"intprecision\";s:" + self.var3_divby_length + ":\"" + self.var3_divby + "\";" \
                                      "s:8:\"rangemin\";d:" + self.var3_min + ";" \
                                      "s:8:\"rangemax\";d:" + self.var3_max + ";" \
                                      "s:4:\"unit\";s:0:\"\";" \
                                      "s:9:\"unitvalue\";s:0:\"\";" \
                                      "}"
                    print("VAR_3 no UNIT")
                # -----------------------------------------------------------------------Variable 4

                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "$v4"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')

                if self.var4_unit != "":
                    fieldentry.text = "a:6:{" \
                                      "s:9:\"precision\";i:" + self.var4_prec + ";" \
                                      "s:12:\"intprecision\";s:" + self.var4_divby_length + ":\"" + self.var4_divby + "\";" \
                                      "s:8:\"rangemin\";d:" + self.var4_min + ";" \
                                      "s:8:\"rangemax\";d:" + self.var4_max + ";" \
                                      "s:4:\"unit\";s:" + str(self.var4_unit_length) + ":\"" + self.var4_unit + "\";" \
                                      "s:9:\"unitvalue\";s:" + str(len(Formelfrage.unit_table(self, self.var4_unit))) + ":\"" + Formelfrage.unit_table(self, self.var4_unit) + "\";" \
                                      "}"
                else:
                    fieldentry.text = "a:6:{" \
                                      "s:9:\"precision\";i:" + self.var4_prec + ";" \
                                      "s:12:\"intprecision\";s:" + self.var1_divby_length + ":\"" + self.var4_divby + "\";" \
                                      "s:8:\"rangemin\";d:" + self.var4_min + ";" \
                                      "s:8:\"rangemax\";d:" + self.var4_max + ";" \
                                      "s:4:\"unit\";s:0:\"\";" \
                                      "s:9:\"unitvalue\";s:0:\"\";" \
                                      "}"
                    print("VAR_4 no UNIT")
                # -----------------------------------------------------------------------Variable 5

                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "$v5"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')

                if self.var5_unit != "":
                    fieldentry.text = "a:6:{" \
                                      "s:9:\"precision\";i:" + self.var5_prec + ";" \
                                      "s:12:\"intprecision\";s:" + self.var5_divby_length + ":\"" + self.var5_divby + "\";" \
                                      "s:8:\"rangemin\";d:" + self.var5_min + ";" \
                                      "s:8:\"rangemax\";d:" + self.var5_max + ";" \
                                      "s:4:\"unit\";s:" + str(self.var5_unit_length) + ":\"" + self.var5_unit + "\";" \
                                      "s:9:\"unitvalue\";s:" + str(len(Formelfrage.unit_table(self, self.var5_unit))) + ":\"" + Formelfrage.unit_table(self, self.var5_unit) + "\";" \
                                      "}"

                else:
                    fieldentry.text = "a:6:{" \
                                      "s:9:\"precision\";i:" + self.var5_prec + ";" \
                                      "s:12:\"intprecision\";s:" + self.var5_divby_length + ":\"" + self.var5_divby + "\";" \
                                      "s:8:\"rangemin\";d:" + self.var5_min + ";" \
                                      "s:8:\"rangemax\";d:" + self.var5_max + ";" \
                                      "s:4:\"unit\";s:0:\"\";" \
                                      "s:9:\"unitvalue\";s:0:\"\";" \
                                      "}"
                    print("VAR_5 no UNIT")

                # -----------------------------------------------------------------------Variable 6

                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "$v6"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')

                if self.var6_unit != "":
                    fieldentry.text = "a:6:{" \
                                      "s:9:\"precision\";i:" + self.var6_prec + ";" \
                                      "s:12:\"intprecision\";s:" + self.var6_divby_length + ":\"" + self.var6_divby + "\";" \
                                      "s:8:\"rangemin\";d:" + self.var6_min + ";" \
                                      "s:8:\"rangemax\";d:" + self.var6_max + ";" \
                                      "s:4:\"unit\";s:" + str(self.var6_unit_length) + ":\"" + self.var6_unit + "\";" \
                                      "s:9:\"unitvalue\";s:" + str(len(Formelfrage.unit_table(self, self.var6_unit))) + ":\"" + Formelfrage.unit_table(self, self.var6_unit) + "\";" \
                                      "}"

                else:
                    fieldentry.text = "a:6:{" \
                                      "s:9:\"precision\";i:" + self.var6_prec + ";" \
                                      "s:12:\"intprecision\";s:" + self.var6_divby_length + ":\"" + self.var6_divby + "\";" \
                                      "s:8:\"rangemin\";d:" + self.var6_min + ";" \
                                      "s:8:\"rangemax\";d:" + self.var6_max + ";" \
                                      "s:4:\"unit\";s:0:\"\";" \
                                      "s:9:\"unitvalue\";s:0:\"\";" \
                                      "}"
                    print("VAR_6 no UNIT")

                # -----------------------------------------------------------------------Variable 7

                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "$v7"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')

                if self.var7_unit != "":
                    fieldentry.text = "a:6:{" \
                                      "s:9:\"precision\";i:" + self.var7_prec + ";" \
                                      "s:12:\"intprecision\";s:" + self.var7_divby_length + ":\"" + self.var7_divby + "\";" \
                                      "s:8:\"rangemin\";d:" + self.var7_min + ";" \
                                      "s:8:\"rangemax\";d:" + self.var7_max + ";" \
                                      "s:4:\"unit\";s:" + str(self.var7_unit_length) + ":\"" + self.var7_unit + "\";" \
                                      "s:9:\"unitvalue\";s:" + str(len(Formelfrage.unit_table(self, self.var7_unit))) + ":\"" + Formelfrage.unit_table(self, self.var7_unit) + "\";" \
                                      "}"

                else:
                    fieldentry.text = "a:6:{" \
                                      "s:9:\"precision\";i:" + self.var7_prec + ";" \
                                      "s:12:\"intprecision\";s:" + self.var7_divby_length + ":\"" + self.var7_divby + "\";" \
                                      "s:8:\"rangemin\";d:" + self.var7_min + ";" \
                                      "s:8:\"rangemax\";d:" + self.var7_max + ";" \
                                      "s:4:\"unit\";s:0:\"\";" \
                                      "s:9:\"unitvalue\";s:0:\"\";" \
                                      "}"
                    print("VAR_7 no UNIT")

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

                if self.res1_unit != "":
                    fieldentry.text = "a:10:{" \
                                      "s:9:\"precision\";i:" + self.res1_prec + ";" \
                                      "s:9:\"tolerance\";s:" + self.res1_tol_length + ":\"" + self.res1_tol + "\";" \
                                      "s:8:\"rangemin\";s:" + self.res1_min_length + ":\"" + self.res1_min + "\";" \
                                      "s:8:\"rangemax\";s:" + self.res1_max_length + ":\"" + self.res1_max + "\";" \
                                      "s:6:\"points\";s:1:\"" + self.res1_points + "\";" \
                                      "s:7:\"formula\";s:" + self.res1_formula_length + ":\"" + self.res1_formula + "\";" \
                                      "s:6:\"rating\";s:0:\"\";" \
                                      "s:4:\"unit\";s:" + str(self.res1_unit_length) + ":\"" + self.res1_unit + "\";" \
                                      "s:9:\"unitvalue\";s:" + str(len(Formelfrage.unit_table(self, self.res1_unit))) + ":\"" + Formelfrage.unit_table(self, self.res1_unit) + "\";" \
                                      "s:11:\"resultunits\";a:27:{i:0;a:2:{s:4:\"unit\";s:1:\"H\";s:9:\"unitvalue\";s:3:\"125\";}" \
                                                                    "i:1;a:2:{s:4:\"unit\";s:2:\"mH\";s:9:\"unitvalue\";s:3:\"126\";}" \
                                                                    "i:2;a:2:{s:4:\"unit\";s:3:\"µH\";s:9:\"unitvalue\";s:3:\"127\";}" \
                                                                    "i:3;a:2:{s:4:\"unit\";s:2:\"nH\";s:9:\"unitvalue\";s:3:\"128\";}" \
                                                                    "i:4;a:2:{s:4:\"unit\";s:2:\"kH\";s:9:\"unitvalue\";s:3:\"129\";}" \
                                                                    "i:5;a:2:{s:4:\"unit\";s:2:\"pH\";s:9:\"unitvalue\";s:3:\"130\";}" \
                                                                    "i:6;a:2:{s:4:\"unit\";s:1:\"F\";s:9:\"unitvalue\";s:3:\"131\";}" \
                                                                    "i:7;a:2:{s:4:\"unit\";s:2:\"mF\";s:9:\"unitvalue\";s:3:\"132\";}" \
                                                                    "i:8;a:2:{s:4:\"unit\";s:3:\"µF\";s:9:\"unitvalue\";s:3:\"133\";}" \
                                                                    "i:9;a:2:{s:4:\"unit\";s:2:\"nF\";s:9:\"unitvalue\";s:3:\"134\";}" \
                                                                    "i:10;a:2:{s:4:\"unit\";s:2:\"pF\";s:9:\"unitvalue\";s:3:\"135\";}" \
                                                                    "i:11;a:2:{s:4:\"unit\";s:1:\"W\";s:9:\"unitvalue\";s:3:\"136\";}" \
                                                                    "i:12;a:2:{s:4:\"unit\";s:2:\"kW\";s:9:\"unitvalue\";s:3:\"137\";}" \
                                                                    "i:13;a:2:{s:4:\"unit\";s:2:\"MW\";s:9:\"unitvalue\";s:3:\"138\";}" \
                                                                    "i:14;a:2:{s:4:\"unit\";s:1:\"V\";s:9:\"unitvalue\";s:3:\"139\";}" \
                                                                    "i:15;a:2:{s:4:\"unit\";s:2:\"kV\";s:9:\"unitvalue\";s:3:\"140\";}" \
                                                                    "i:16;a:2:{s:4:\"unit\";s:2:\"mV\";s:9:\"unitvalue\";s:3:\"141\";}" \
                                                                    "i:17;a:2:{s:4:\"unit\";s:3:\"µV\";s:9:\"unitvalue\";s:3:\"142\";}" \
                                                                    "i:18;a:2:{s:4:\"unit\";s:2:\"MV\";s:9:\"unitvalue\";s:3:\"143\";}" \
                                                                    "i:19;a:2:{s:4:\"unit\";s:1:\"A\";s:9:\"unitvalue\";s:3:\"144\";}" \
                                                                    "i:20;a:2:{s:4:\"unit\";s:2:\"mA\";s:9:\"unitvalue\";s:3:\"145\";}" \
                                                                    "i:21;a:2:{s:4:\"unit\";s:3:\"µA\";s:9:\"unitvalue\";s:3:\"146\";}" \
                                                                    "i:22;a:2:{s:4:\"unit\";s:2:\"kA\";s:9:\"unitvalue\";s:3:\"147\";}" \
                                                                    "i:23;a:2:{s:4:\"unit\";s:3:\"Ohm\";s:9:\"unitvalue\";s:3:\"148\";}" \
                                                                    "i:24;a:2:{s:4:\"unit\";s:2:\"mW\";s:9:\"unitvalue\";s:3:\"149\";}" \
                                                                    "i:25;a:2:{s:4:\"unit\";s:4:\"kOhm\";s:9:\"unitvalue\";s:3:\"150\";}" \
                                                                    "i:26;a:2:{s:4:\"unit\";s:4:\"mOhm\";s:9:\"unitvalue\";s:3:\"151\";}}" \
                                      "}"

                else:
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

                if self.res2_unit != "":
                    fieldentry.text = "a:10:{" \
                                      "s:9:\"precision\";i:" + self.res2_prec + ";" \
                                      "s:9:\"tolerance\";s:" + self.res2_tol_length + ":\"" + self.res2_tol + "\";" \
                                      "s:8:\"rangemin\";s:" + self.res2_min_length + ":\"" + self.res2_min + "\";" \
                                      "s:8:\"rangemax\";s:" + self.res2_max_length + ":\"" + self.res2_max + "\";" \
                                      "s:6:\"points\";s:1:\"" + self.res2_points + "\";" \
                                      "s:7:\"formula\";s:" + self.res2_formula_length + ":\"" + self.res2_formula + "\";" \
                                      "s:6:\"rating\";s:0:\"\";" \
                                      "s:4:\"unit\";s:" + str(self.res2_unit_length) + ":\"" + self.res2_unit + "\";" \
                                      "s:9:\"unitvalue\";s:" + str(len(Formelfrage.unit_table(self, self.res2_unit))) + ":\"" + Formelfrage.unit_table(self, self.res2_unit) + "\";" \
                                      "s:11:\"resultunits\";a:27:{i:0;a:2:{s:4:\"unit\";s:1:\"H\";s:9:\"unitvalue\";s:3:\"125\";}" \
                                                                    "i:1;a:2:{s:4:\"unit\";s:2:\"mH\";s:9:\"unitvalue\";s:3:\"126\";}" \
                                                                    "i:2;a:2:{s:4:\"unit\";s:3:\"µH\";s:9:\"unitvalue\";s:3:\"127\";}" \
                                                                    "i:3;a:2:{s:4:\"unit\";s:2:\"nH\";s:9:\"unitvalue\";s:3:\"128\";}" \
                                                                    "i:4;a:2:{s:4:\"unit\";s:2:\"kH\";s:9:\"unitvalue\";s:3:\"129\";}" \
                                                                    "i:5;a:2:{s:4:\"unit\";s:2:\"pH\";s:9:\"unitvalue\";s:3:\"130\";}" \
                                                                    "i:6;a:2:{s:4:\"unit\";s:1:\"F\";s:9:\"unitvalue\";s:3:\"131\";}" \
                                                                    "i:7;a:2:{s:4:\"unit\";s:2:\"mF\";s:9:\"unitvalue\";s:3:\"132\";}" \
                                                                    "i:8;a:2:{s:4:\"unit\";s:3:\"µF\";s:9:\"unitvalue\";s:3:\"133\";}" \
                                                                    "i:9;a:2:{s:4:\"unit\";s:2:\"nF\";s:9:\"unitvalue\";s:3:\"134\";}" \
                                                                    "i:10;a:2:{s:4:\"unit\";s:2:\"pF\";s:9:\"unitvalue\";s:3:\"135\";}" \
                                                                    "i:11;a:2:{s:4:\"unit\";s:1:\"W\";s:9:\"unitvalue\";s:3:\"136\";}" \
                                                                    "i:12;a:2:{s:4:\"unit\";s:2:\"kW\";s:9:\"unitvalue\";s:3:\"137\";}" \
                                                                    "i:13;a:2:{s:4:\"unit\";s:2:\"MW\";s:9:\"unitvalue\";s:3:\"138\";}" \
                                                                    "i:14;a:2:{s:4:\"unit\";s:1:\"V\";s:9:\"unitvalue\";s:3:\"139\";}" \
                                                                    "i:15;a:2:{s:4:\"unit\";s:2:\"kV\";s:9:\"unitvalue\";s:3:\"140\";}" \
                                                                    "i:16;a:2:{s:4:\"unit\";s:2:\"mV\";s:9:\"unitvalue\";s:3:\"141\";}" \
                                                                    "i:17;a:2:{s:4:\"unit\";s:3:\"µV\";s:9:\"unitvalue\";s:3:\"142\";}" \
                                                                    "i:18;a:2:{s:4:\"unit\";s:2:\"MV\";s:9:\"unitvalue\";s:3:\"143\";}" \
                                                                    "i:19;a:2:{s:4:\"unit\";s:1:\"A\";s:9:\"unitvalue\";s:3:\"144\";}" \
                                                                    "i:20;a:2:{s:4:\"unit\";s:2:\"mA\";s:9:\"unitvalue\";s:3:\"145\";}" \
                                                                    "i:21;a:2:{s:4:\"unit\";s:3:\"µA\";s:9:\"unitvalue\";s:3:\"146\";}" \
                                                                    "i:22;a:2:{s:4:\"unit\";s:2:\"kA\";s:9:\"unitvalue\";s:3:\"147\";}" \
                                                                    "i:23;a:2:{s:4:\"unit\";s:3:\"Ohm\";s:9:\"unitvalue\";s:3:\"148\";}" \
                                                                    "i:24;a:2:{s:4:\"unit\";s:2:\"mW\";s:9:\"unitvalue\";s:3:\"149\";}" \
                                                                    "i:25;a:2:{s:4:\"unit\";s:4:\"kOhm\";s:9:\"unitvalue\";s:3:\"150\";}" \
                                                                    "i:26;a:2:{s:4:\"unit\";s:4:\"mOhm\";s:9:\"unitvalue\";s:3:\"151\";}}" \
                                      "}"

                else:
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

                if self.res3_unit != "":
                    fieldentry.text = "a:10:{" \
                                      "s:9:\"precision\";i:" + self.res3_prec + ";" \
                                      "s:9:\"tolerance\";s:" + self.res3_tol_length + ":\"" + self.res3_tol + "\";" \
                                      "s:8:\"rangemin\";s:" + self.res3_min_length + ":\"" + self.res3_min + "\";" \
                                      "s:8:\"rangemax\";s:" + self.res3_max_length + ":\"" + self.res3_max + "\";" \
                                      "s:6:\"points\";s:1:\"" + self.res3_points + "\";" \
                                      "s:7:\"formula\";s:" + self.res3_formula_length + ":\"" + self.res3_formula + "\";" \
                                      "s:6:\"rating\";s:0:\"\";" \
                                      "s:4:\"unit\";s:" + str(self.res3_unit_length) + ":\"" + self.res3_unit + "\";" \
                                      "s:9:\"unitvalue\";s:" + str(len(Formelfrage.unit_table(self, self.res3_unit))) + ":\"" + Formelfrage.unit_table(self, self.res3_unit) + "\";" \
                                      "s:11:\"resultunits\";a:27:{i:0;a:2:{s:4:\"unit\";s:1:\"H\";s:9:\"unitvalue\";s:3:\"125\";}" \
                                                                    "i:1;a:2:{s:4:\"unit\";s:2:\"mH\";s:9:\"unitvalue\";s:3:\"126\";}" \
                                                                    "i:2;a:2:{s:4:\"unit\";s:3:\"µH\";s:9:\"unitvalue\";s:3:\"127\";}" \
                                                                    "i:3;a:2:{s:4:\"unit\";s:2:\"nH\";s:9:\"unitvalue\";s:3:\"128\";}" \
                                                                    "i:4;a:2:{s:4:\"unit\";s:2:\"kH\";s:9:\"unitvalue\";s:3:\"129\";}" \
                                                                    "i:5;a:2:{s:4:\"unit\";s:2:\"pH\";s:9:\"unitvalue\";s:3:\"130\";}" \
                                                                    "i:6;a:2:{s:4:\"unit\";s:1:\"F\";s:9:\"unitvalue\";s:3:\"131\";}" \
                                                                    "i:7;a:2:{s:4:\"unit\";s:2:\"mF\";s:9:\"unitvalue\";s:3:\"132\";}" \
                                                                    "i:8;a:2:{s:4:\"unit\";s:3:\"µF\";s:9:\"unitvalue\";s:3:\"133\";}" \
                                                                    "i:9;a:2:{s:4:\"unit\";s:2:\"nF\";s:9:\"unitvalue\";s:3:\"134\";}" \
                                                                    "i:10;a:2:{s:4:\"unit\";s:2:\"pF\";s:9:\"unitvalue\";s:3:\"135\";}" \
                                                                    "i:11;a:2:{s:4:\"unit\";s:1:\"W\";s:9:\"unitvalue\";s:3:\"136\";}" \
                                                                    "i:12;a:2:{s:4:\"unit\";s:2:\"kW\";s:9:\"unitvalue\";s:3:\"137\";}" \
                                                                    "i:13;a:2:{s:4:\"unit\";s:2:\"MW\";s:9:\"unitvalue\";s:3:\"138\";}" \
                                                                    "i:14;a:2:{s:4:\"unit\";s:1:\"V\";s:9:\"unitvalue\";s:3:\"139\";}" \
                                                                    "i:15;a:2:{s:4:\"unit\";s:2:\"kV\";s:9:\"unitvalue\";s:3:\"140\";}" \
                                                                    "i:16;a:2:{s:4:\"unit\";s:2:\"mV\";s:9:\"unitvalue\";s:3:\"141\";}" \
                                                                    "i:17;a:2:{s:4:\"unit\";s:3:\"µV\";s:9:\"unitvalue\";s:3:\"142\";}" \
                                                                    "i:18;a:2:{s:4:\"unit\";s:2:\"MV\";s:9:\"unitvalue\";s:3:\"143\";}" \
                                                                    "i:19;a:2:{s:4:\"unit\";s:1:\"A\";s:9:\"unitvalue\";s:3:\"144\";}" \
                                                                    "i:20;a:2:{s:4:\"unit\";s:2:\"mA\";s:9:\"unitvalue\";s:3:\"145\";}" \
                                                                    "i:21;a:2:{s:4:\"unit\";s:3:\"µA\";s:9:\"unitvalue\";s:3:\"146\";}" \
                                                                    "i:22;a:2:{s:4:\"unit\";s:2:\"kA\";s:9:\"unitvalue\";s:3:\"147\";}" \
                                                                    "i:23;a:2:{s:4:\"unit\";s:3:\"Ohm\";s:9:\"unitvalue\";s:3:\"148\";}" \
                                                                    "i:24;a:2:{s:4:\"unit\";s:2:\"mW\";s:9:\"unitvalue\";s:3:\"149\";}" \
                                                                    "i:25;a:2:{s:4:\"unit\";s:4:\"kOhm\";s:9:\"unitvalue\";s:3:\"150\";}" \
                                                                    "i:26;a:2:{s:4:\"unit\";s:4:\"mOhm\";s:9:\"unitvalue\";s:3:\"151\";}}" \
                                      "}"

                else:
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

                self.mytree.write(self.qti_file_path_write)
                print("DONE")

        conn.commit()
        conn.close()


        create_formelfrage.replace_characters(self)
        #GUI_settings_window.create_settings(self)


    def replace_characters(self):

        #open xml file to replace specific characters
        with open(self.qti_file_path_write, 'r') as xml_file:
            xml_str = xml_file.read()
        xml_str = xml_str.replace('&amp;', '&') #replace 'x' with 'new_x'
         
        #write to file
        with open(self.qti_file_path_write, 'w') as replaced_xml_file:
            replaced_xml_file.write(xml_str)

        print("WORKOVER FINISHED!")







class GUI_settings_window(Formelfrage):

    def __init__(self):


        # New Window must be "Toplevel" not "Tk()" in order to get Radiobuttons to work properly
        self.test_settings_window = Toplevel()
        self.test_settings_window.title("Test-Settings")

        # Create a ScrolledFrame widget
        self.sf_test_settings = ScrolledFrame(self.test_settings_window, width=self.settings_width, height=self.settings_height)
        self.sf_test_settings.pack(expand=1, fill="both")

        # Bind the arrow keys and scroll wheel
        self.sf_test_settings.bind_arrow_keys(app)
        self.sf_test_settings.bind_scroll_wheel(app)

        # Create a frame within the ScrolledFrame
        self.test_settings = self.sf_test_settings.display_widget(Frame)



        self.frame1 = LabelFrame(self.test_settings, text="Test Settings Frame1...", padx=5, pady=5)
        self.frame1.grid(row=0, column=0, padx=20, pady=10, sticky=NW)

        self.frame2 = LabelFrame(self.test_settings, text="Test Settings Frame2...", padx=5, pady=5)
        self.frame2.grid(row=0, column=1, padx=20, pady=10, sticky=NW)

        self.frame3 = LabelFrame(self.test_settings, text="Test Settings Frame3...", padx=5, pady=5)
        self.frame3.grid(row=0, column=2, padx=20, pady=10, sticky=NW)


        self.res12_min_listbox_label = Label(self.frame1, text="EINSTELLUNGEN DES TESTS", font=('Helvetica', 10, 'bold'))
        self.res12_min_listbox_label.grid(row=0, column=0, sticky=W, padx=10, pady=(20, 0))

        self.res90_min_listbox_label = Label(self.frame1, text="Test-Titel")
        self.res90_min_listbox_label.grid(row=1, column=0, sticky=W, padx=10)
        self.res91_max_listbox_label = Label(self.frame1, text="Beschreibung")
        self.res91_max_listbox_label.grid(row=2, column=0, sticky=W, padx=10)

        self.res1_max_listbox_label = Label(self.frame1, text="Auswahl der Testfragen")
        self.res1_max_listbox_label.grid(row=4, column=0, sticky=W, padx=10)
        self.res1_prec_listbox_label = Label(self.frame1, text="Datenschutz")
        self.res1_prec_listbox_label.grid(row=7, column=0, sticky=W, padx=10)

        self.res1_tol_listbox_label = Label(self.frame1, text="VERFÜGBARKEIT", font=('Helvetica', 10, 'bold'))
        self.res1_tol_listbox_label.grid(row=9, column=0, sticky=W, padx=10, pady=(20, 0))
        self.res1_points_listbox_label = Label(self.frame1, text="Online   ---   not working")
        self.res1_points_listbox_label.grid(row=10, column=0, sticky=W, padx=10)
        self.res13_points_listbox_label = Label(self.frame1, text="Zeitlich begrenzte Verfügbarkeit   ---   not working")
        self.res13_points_listbox_label.grid(row=11, column=0, sticky=W, padx=10)

        self.res22_tol_listbox_label = Label(self.frame1, text="INFORMATIONEN ZUM EINSTIEG", font=('Helvetica', 10, 'bold'))
        self.res22_tol_listbox_label.grid(row=14, column=0, sticky=W, padx=10, pady=(20, 0))
        self.res23_points_listbox_label = Label(self.frame1, text="Einleitung")
        self.res23_points_listbox_label.grid(row=15, column=0, sticky=W, padx=10)
        self.res24_points_listbox_label = Label(self.frame1, text="Testeigenschaften anzeigen")
        self.res24_points_listbox_label.grid(row=16, column=0, sticky=W, padx=10)

        self.res31_tol_listbox_label = Label(self.frame1, text="DURCHFÜHRUNG: ZUGANG", font=('Helvetica', 10, 'bold'))
        self.res31_tol_listbox_label.grid(row=17, column=0, sticky=W, padx=10, pady=(20, 0))

        self.test_time_year_label = Label(self.frame1, text="Jahr")
        self.test_time_year_label.grid(row=17, column=1, sticky=W)
        self.test_time_month_label = Label(self.frame1, text="Mon.")
        self.test_time_month_label.grid(row=17, column=1, sticky=W, padx=35)
        self.test_time_day_label = Label(self.frame1, text="Tag")
        self.test_time_day_label.grid(row=17, column=1, sticky=W, padx=70)
        self.test_time_hour_label = Label(self.frame1, text="Std.")
        self.test_time_hour_label.grid(row=17, column=1, sticky=W, padx=105)
        self.test_time_minute_label = Label(self.frame1, text="Min.")
        self.test_time_minute_label.grid(row=17, column=1, sticky=W, padx=140)



        self.res32_points_listbox_label = Label(self.frame1, text="Test-Start")
        self.res32_points_listbox_label.grid(row=18, column=0, sticky=W, padx=10)
        self.res33_points_listbox_label = Label(self.frame1, text="Test-Ende")
        self.res33_points_listbox_label.grid(row=19, column=0, sticky=W, padx=10)
        self.res34_tol_listbox_label = Label(self.frame1, text="Test-Passwort")
        self.res34_tol_listbox_label.grid(row=20, column=0, sticky=W, padx=10)
        self.res35_points_listbox_label = Label(self.frame1, text="Nur ausgewählte Teilnehmer")
        self.res35_points_listbox_label.grid(row=21, column=0, sticky=W, padx=10)
        self.res36_points_listbox_label = Label(self.frame1, text="Anzahl gleichzeitiger Teilnehmer begrenzen")
        self.res36_points_listbox_label.grid(row=22, column=0, sticky=W, padx=10)
        self.res37_points_listbox_label = Label(self.frame1, text="Inaktivitätszeit der Teilnehmner (in Sek.)")
        self.res37_points_listbox_label.grid(row=23, column=0, sticky=W, padx=30)

        self.res41_tol_listbox_label = Label(self.frame1, text="DURCHFÜHRUNG: STEUERUNG TESTDURCHLAUF", font=('Helvetica', 10, 'bold'))
        self.res41_tol_listbox_label.grid(row=24, column=0, sticky=W, padx=10, pady=(20, 0))
        self.res42_points_listbox_label = Label(self.frame1, text="Anzahl von Testdurchläufen begrenzen")
        self.res42_points_listbox_label.grid(row=25, column=0, sticky=W, padx=10)
        self.res43_points_listbox_label = Label(self.frame1, text="Wartezeit zwischen Durchläufen erzwingen")
        self.res43_points_listbox_label.grid(row=26, column=0, sticky=W, padx=10)
        self.res44_tol_listbox_label = Label(self.frame1, text="Bearbeitungsdauer begrenzen")
        self.res44_tol_listbox_label.grid(row=27, column=0, sticky=W, padx=10)
        self.res44_tol_listbox_label = Label(self.frame1, text="Bearbeitungsdauer (in Min).")
        self.res44_tol_listbox_label.grid(row=28, column=0, sticky=W, padx=30)
        self.res44_tol_listbox_label = Label(self.frame1, text="Max. Bearbeitungsdauer für jeden Testlauf zurücksetzen")
        self.res44_tol_listbox_label.grid(row=29, column=0, sticky=W, padx=30)
        self.res45_points_listbox_label = Label(self.frame1, text="Prüfungsansicht")
        self.res45_points_listbox_label.grid(row=30, column=0, sticky=W, padx=10)
        self.res45_1_points_listbox_label = Label(self.frame1, text="Titel des Tests")
        self.res45_1_points_listbox_label.grid(row=31, column=0, sticky=W, padx=30)
        self.res45_2_points_listbox_label = Label(self.frame1, text="Name des Teilnehmers")
        self.res45_2_points_listbox_label.grid(row=32, column=0, sticky=W, padx=30)
        self.res46_points_listbox_label = Label(self.frame1, text="ILIAS-Prüfungsnummer anzeigen")
        self.res46_points_listbox_label.grid(row=33, column=0, sticky=W, padx=10)

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
        self.res56_points_listbox_label = Label(self.frame2, text="Direkte Rückmeldung   ---   not working")
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

        # --------------------------- DEFINE CHECKBOXES WITH ENTRYS ---------------------------------------



        # --------------------------- CHECKBOXES ---------------------------------------

        self.var_online = IntVar()
        self.check_online = Checkbutton(self.frame1, text="", variable=self.var_online, onvalue=1, offvalue=0)
        self.check_online.deselect()
        self.check_online.grid(row=10, column=1, sticky=W)

        self.var_time_limited = IntVar()
        self.time_limited_start_label = Label(self.frame1, text="Start")
        self.time_limited_start_day_label = Label(self.frame1, text="Tag")
        self.time_limited_start_day_entry = Entry(self.frame1, width=3)
        self.time_limited_start_month_label = Label(self.frame1, text="Mo")
        self.time_limited_start_month_entry = Entry(self.frame1, width=3)
        self.time_limited_start_year_label = Label(self.frame1, text="Jahr")
        self.time_limited_start_year_entry = Entry(self.frame1, width=4)
        self.time_limited_start_hour_label = Label(self.frame1, text="Std")
        self.time_limited_start_hour_entry = Entry(self.frame1, width=3)
        self.time_limited_start_minute_label = Label(self.frame1, text="Min")
        self.time_limited_start_minute_entry = Entry(self.frame1, width=3)

        self.time_limited_end_label = Label(self.frame1, text="Ende")
        self.time_limited_end_day_label = Label(self.frame1, text="Tag")
        self.time_limited_end_day_entry = Entry(self.frame1, width=3)
        self.time_limited_end_month_label = Label(self.frame1, text="Mo")
        self.time_limited_end_month_entry = Entry(self.frame1, width=3)
        self.time_limited_end_year_label = Label(self.frame1, text="Jahr")
        self.time_limited_end_year_entry = Entry(self.frame1, width=4)
        self.time_limited_end_hour_label = Label(self.frame1, text="Std")
        self.time_limited_end_hour_entry = Entry(self.frame1, width=3)
        self.time_limited_end_minute_label = Label(self.frame1, text="Min")
        self.time_limited_end_minute_entry = Entry(self.frame1, width=3)


        #self.entry.grid(row=11, column=1, sticky=W, padx=20)
        self.check_time_limited = Checkbutton(self.frame1, text="", variable=self.var_time_limited, onvalue=1, offvalue=0,
                                              command=lambda v=self.var_time_limited: GUI_settings_window.show_entry_time_limited_start(self, v))
        self.check_time_limited.deselect()
        self.check_time_limited.grid(row=11, column=1, sticky=W)

        self.var_introduction = IntVar()
        self.check_introduction = Checkbutton(self.frame1, text="", variable=self.var_introduction, onvalue=1, offvalue=0,
                                              command=lambda v=self.var_introduction: GUI_settings_window.show_introduction_textfield(self, v))
        self.check_introduction.deselect()
        self.check_introduction.grid(row=15, column=1, sticky=W)

        self.var_test_prop = IntVar()
        self.check_test_prop = Checkbutton(self.frame1, text="", variable=self.var_test_prop, onvalue=1, offvalue=0)
        self.check_test_prop.deselect()
        self.check_test_prop.grid(row=16, column=1, sticky=W)

        #self.var_test_password = IntVar()
        #self.check_test_password = Checkbutton(self.frame1, text="", variable=self.var_test_password, onvalue=1, offvalue=0)
        #self.check_test_password.deselect()
        #self.check_test_password.grid(row=20, column=1, sticky=W)

        self.var_specific_users = IntVar()
        self.check_specific_users = Checkbutton(self.frame1, text="", variable=self.var_specific_users, onvalue=1, offvalue=0)
        self.check_specific_users.deselect()
        self.check_specific_users.grid(row=21, column=1, sticky=W)

        #self.var_fixed_users = IntVar()
        #self.check_fixed_users = Checkbutton(self.frame1, text="", variable=self.var_fixed_users, onvalue=1, offvalue=0)
        #self.check_fixed_users.deselect()
        #self.check_fixed_users.grid(row=22, column=1, sticky=W)

        #self.var_limit_test_runs = IntVar()
        #self.check_limit_test_runs = Checkbutton(self.frame1, text="", variable=self.var_limit_test_runs, onvalue=1, offvalue=0)
        #self.check_limit_test_runs.deselect()
        #self.check_limit_test_runs.grid(row=22, column=1, sticky=W)

        #self.var_time_betw_test_runs = IntVar()
        #self.check_time_betw_test_runs = Checkbutton(self.frame1, text="", variable=self.var_time_betw_test_runs, onvalue=1, offvalue=0)
        #self.check_time_betw_test_runs.deselect()
        #self.check_time_betw_test_runs.grid(row=25, column=1, sticky=W)

        self.var_processing_time = IntVar()
        self.check_processing_time = Checkbutton(self.frame1, text="", variable=self.var_processing_time, onvalue=1, offvalue=0)
        self.check_processing_time.deselect()
        self.check_processing_time.grid(row=27, column=1, sticky=W)

        self.var_processing_time_reset = IntVar()
        self.check_processing_time_reset = Checkbutton(self.frame1, text="", variable=self.var_processing_time_reset, onvalue=1, offvalue=0)
        self.check_processing_time_reset.deselect()
        self.check_processing_time_reset.grid(row=29, column=1, sticky=W)

        self.var_examview = IntVar()
        self.check_examview = Checkbutton(self.frame1, text="", variable=self.var_examview, onvalue=1, offvalue=0)
        self.check_examview.deselect()
        self.check_examview.grid(row=30, column=1, sticky=W)

        self.var_examview_test_title = IntVar()
        self.check_examview_test_title = Checkbutton(self.frame1, text="", variable=self.var_examview_test_title, onvalue=1, offvalue=0)
        self.check_examview_test_title.deselect()
        self.check_examview_test_title.grid(row=31, column=1, sticky=W)

        self.var_examview_user_name = IntVar()
        self.check_examview_user_name = Checkbutton(self.frame1, text="", variable=self.var_examview_user_name, onvalue=1, offvalue=0)
        self.check_examview_user_name.deselect()
        self.check_examview_user_name.grid(row=32, column=1, sticky=W)

        self.var_show_ilias_nr = IntVar()
        self.check_show_ilias_nr = Checkbutton(self.frame1, text="", variable=self.var_show_ilias_nr, onvalue=1, offvalue=0)
        self.check_show_ilias_nr.deselect()
        self.check_show_ilias_nr.grid(row=33, column=1, sticky=W)

        self.var_autosave = IntVar()
        self.check_autosave = Checkbutton(self.frame2, text="", variable=self.var_autosave, onvalue=1, offvalue=0,
                                          command=lambda v=self.var_autosave: GUI_settings_window.enable_autosave(self, v))

        self.check_autosave_interval_label = Label(self.frame2, text="Speicherintervall (in Sek.):")
        self.check_autosave_interval_entry = Entry(self.frame2, width=10)
        self.check_autosave.deselect()
        self.check_autosave.grid(row=4, column=3, sticky=W)

        self.var_mix_questions = IntVar()
        self.check_mix_questions = Checkbutton(self.frame2, text="", variable=self.var_mix_questions, onvalue=1, offvalue=0)
        self.check_mix_questions.deselect()
        self.check_mix_questions.grid(row=5, column=3, sticky=W)

        self.var_show_solution_notes = IntVar()
        self.check_show_solution_notes = Checkbutton(self.frame2, text="", variable=self.var_show_solution_notes, onvalue=1, offvalue=0)
        self.check_show_solution_notes.deselect()
        self.check_show_solution_notes.grid(row=6, column=3, sticky=W)

        self.var_direct_response = IntVar()
        self.check_direct_response = Checkbutton(self.frame2, text="", variable=self.var_direct_response, onvalue=1, offvalue=0)
        self.check_direct_response.deselect()
        self.check_direct_response.grid(row=7, column=3, sticky=W)

        self.var_mandatory_questions = IntVar()
        self.check_mandatory_questions = Checkbutton(self.frame2, text="", variable=self.var_mandatory_questions, onvalue=1, offvalue=0)
        self.check_mandatory_questions.deselect()
        self.check_mandatory_questions.grid(row=12, column=3, sticky=W)

        self.var_use_previous_solution = IntVar()
        self.check_use_previous_solution = Checkbutton(self.frame2, text="", variable=self.var_use_previous_solution, onvalue=1, offvalue=0)
        self.check_use_previous_solution.deselect()
        self.check_use_previous_solution.grid(row=14, column=3, sticky=W)

        self.var_show_test_cancel = IntVar()
        self.check_show_test_cancel = Checkbutton(self.frame2, text="", variable=self.var_show_test_cancel, onvalue=1, offvalue=0)
        self.check_show_test_cancel.deselect()
        self.check_show_test_cancel.grid(row=15, column=3, sticky=W)

        self.var_show_question_list_process_status = IntVar()
        self.check_show_question_list_process_status = Checkbutton(self.frame2, text="", variable=self.var_show_question_list_process_status, onvalue=1, offvalue=0)
        self.check_show_question_list_process_status.deselect()
        self.check_show_question_list_process_status.grid(row=18, column=3, sticky=W)

        self.var_question_mark = IntVar()
        self.check_question_mark = Checkbutton(self.frame2, text="", variable=self.var_question_mark, onvalue=1, offvalue=0)
        self.check_question_mark.deselect()
        self.check_question_mark.grid(row=19, column=3, sticky=W)

        self.var_overview_answers = IntVar()
        self.check_overview_answers = Checkbutton(self.frame2, text="", variable=self.var_overview_answers, onvalue=1, offvalue=0)
        self.check_overview_answers.grid(row=21, column=3, sticky=W)

        self.var_show_end_comment = IntVar()
        self.check_show_end_comment = Checkbutton(self.frame2, text="", variable=self.var_show_end_comment, onvalue=1, offvalue=0,
                                                  command=lambda v=self.var_show_end_comment: GUI_settings_window.show_concluding_remarks(self, v))
        self.check_show_end_comment.deselect()
        self.check_show_end_comment.grid(row=22, column=3, sticky=W)

        self.var_forwarding = IntVar()
        self.check_forwarding = Checkbutton(self.frame2, text="", variable=self.var_forwarding, onvalue=1, offvalue=0)
        self.check_forwarding.deselect()
        self.check_forwarding.grid(row=23, column=3, sticky=W)

        self.var_notification = IntVar()
        self.check_notification = Checkbutton(self.frame2, text="", variable=self.var_notification, onvalue=1, offvalue=0)
        self.check_notification.deselect()
        self.check_notification.grid(row=24, column=3, sticky=W)

        # --------------------------- RADIO BUTTONS ---------------------------------------

        self.select_question = IntVar()
        self.select_question.set(0)
        self.select_question_radiobtn1 = Radiobutton(self.frame1, text="Fest definierte Fragenauswahl", variable=self.select_question, value=0)
        self.select_question_radiobtn1.grid(row=4, column=1, pady=0, sticky=W)          # FIXED_QUEST_SET
        self.select_question_radiobtn2 = Radiobutton(self.frame1, text="Zufällige Fragenauswahl", variable=self.select_question, value=1)
        self.select_question_radiobtn2.grid(row=5, column=1, pady=0, sticky=W)          # RANDOM_QUEST_SET
        self.select_question_radiobtn3 = Radiobutton(self.frame1, text="Wiedervorlagemodus - alle Fragen eines Fragenpools", variable=self.select_question, value=2)
        self.select_question_radiobtn3.grid(row=6, column=1, pady=0, sticky=W)          # DYNAMIC_QUEST_SET

        self.select_anonym = IntVar()
        self.select_anonym.set(0)
        self.select_anonym_radiobtn1 = Radiobutton(self.frame1, text="Testergebnisse ohne Namen", variable=self.select_anonym, value=0, borderwidth=0, command=self.select_anonym.get())
        self.select_anonym_radiobtn1.grid(row=7, column=1, pady=0, sticky=W)
        self.select_anonym_radiobtn2 = Radiobutton(self.frame1, text="Testergebnisse mit Namen", variable=self.select_anonym, value=1, borderwidth=0, command=self.select_anonym.get())
        self.select_anonym_radiobtn2.grid(row=8, column=1, pady=0, sticky=W)

        self.select_show_question_title = IntVar()
        self.select_show_question_title.set(0)
        self.select_show_question_title_radiobtn1 = Radiobutton(self.frame2, text="Fragentitel und erreichbare Punkte", variable=self.select_show_question_title, value=0, borderwidth=0, command=self.select_show_question_title.get())
        self.select_show_question_title_radiobtn1.grid(row=1, column=3, pady=0, sticky=W)
        self.select_show_question_title_radiobtn2 = Radiobutton(self.frame2, text="Nur Fragentitel", variable=self.select_show_question_title, value=1, borderwidth=0, command=self.select_show_question_title.get())
        self.select_show_question_title_radiobtn2.grid(row=2, column=3, pady=0, sticky=W)
        self.select_show_question_title_radiobtn3 = Radiobutton(self.frame2, text="Weder Fragentitel noch erreichbare Punkte", variable=self.select_show_question_title, value=2, borderwidth=0, command=self.select_show_question_title.get())
        self.select_show_question_title_radiobtn3.grid(row=3, column=3, pady=0, sticky=W)

        self.select_user_response = IntVar()
        self.select_user_response.set(0)
        self.select_user_response_radiobtn1 = Radiobutton(self.frame2, text="Antworten während des Testdurchlaufs nicht festschreiben", variable=self.select_user_response,value=0, borderwidth=0, command=self.select_user_response.get())
        self.select_user_response_radiobtn1.grid(row=8, column=3, pady=0, sticky=W)
        self.select_user_response_radiobtn2 = Radiobutton(self.frame2, text="Antworten bei Anzeige der Rückmeldung festschreiben", variable=self.select_user_response, value=1, borderwidth=0, command=self.select_user_response.get())
        self.select_user_response_radiobtn2.grid(row=9, column=3, pady=0, sticky=W)
        self.select_user_response_radiobtn3 = Radiobutton(self.frame2, text="Antworten bei Anzeige der Folgefrage festschreiben", variable=self.select_user_response, value=2, borderwidth=0, command=self.select_user_response.get())
        self.select_user_response_radiobtn3.grid(row=10, column=3, pady=0, sticky=W)
        self.select_user_response_radiobtn4 = Radiobutton(self.frame2, text="Antworten mit der Anzeige von Rückmeldungen oder der Folgefrage festschreiben",variable=self.select_user_response, value=3, borderwidth=0, command=self.select_user_response.get())
        self.select_user_response_radiobtn4.grid(row=11, column=3,pady=0, sticky=W)

        self.select_not_answered_questions = IntVar()
        self.select_not_answered_questions.set(0)
        self.select_not_answered_questions_radiobtn1 = Radiobutton(self.frame2, text="Nicht beantwortete Fragen bleiben an ihrem Platz", variable=self.select_not_answered_questions,value=0, borderwidth=0, command=self.select_not_answered_questions.get())
        self.select_not_answered_questions_radiobtn1.grid(row=16, column=3, pady=0, sticky=W)
        self.select_not_answered_questions_radiobtn2 = Radiobutton(self.frame2, text="Nicht beantwortete Fragen werden ans Testende gesschoben", variable=self.select_not_answered_questions, value=1, borderwidth=0, command=self.select_not_answered_questions.get())
        self.select_not_answered_questions_radiobtn2.grid(row=17, column=3, pady=0, sticky=W)

        # --------------------------- ENTRY BOXES ---------------------------------------

        self.titel_entry = Entry(self.frame1, width=47)
        self.titel_entry.grid(row=1, column=1)
        self.introduction_bar = Scrollbar(self.frame1)
        self.introduction_infobox = Text(self.frame1, height=4, width=40, font=('Helvetica', 9))



        self.test_start_year_entry = Entry(self.frame1, width=5)
        self.test_start_year_entry.grid(row=18, column=1, sticky=W)
        self.test_start_year_entry.insert(0, "YYYY")
        self.test_start_month_entry = Entry(self.frame1, width=5)
        self.test_start_month_entry.grid(row=18, column=1, sticky=W, padx=35)
        self.test_start_month_entry.insert(0, "MM")
        self.test_start_day_entry = Entry(self.frame1, width=5)
        self.test_start_day_entry.grid(row=18, column=1, sticky=W, padx=70)
        self.test_start_day_entry.insert(0, "DD")
        self.test_start_hour_entry = Entry(self.frame1, width=5)
        self.test_start_hour_entry.grid(row=18, column=1, sticky=W, padx=105)
        self.test_start_hour_entry.insert(0, "HH")
        self.test_start_minute_entry = Entry(self.frame1, width=5)
        self.test_start_minute_entry.grid(row=18, column=1, sticky=W, padx=140)
        self.test_start_minute_entry.insert(0, "mm")

        self.test_end_year_entry = Entry(self.frame1, width=5)
        self.test_end_year_entry.grid(row=19, column=1, sticky=W, pady=5)
        self.test_end_year_entry.insert(0, "YYYY")
        self.test_end_month_entry = Entry(self.frame1, width=5)
        self.test_end_month_entry.grid(row=19, column=1, sticky=W, padx=35)
        self.test_end_month_entry.insert(0, "MM")
        self.test_end_day_entry = Entry(self.frame1, width=5)
        self.test_end_day_entry.grid(row=19, column=1, sticky=W, padx=70)
        self.test_end_day_entry.insert(0, "DD")
        self.test_end_hour_entry = Entry(self.frame1, width=5)
        self.test_end_hour_entry.grid(row=19, column=1, sticky=W, padx=105)
        self.test_end_hour_entry.insert(0, "HH")
        self.test_end_minute_entry = Entry(self.frame1, width=5)
        self.test_end_minute_entry.grid(row=19, column=1, sticky=W, padx=140)
        self.test_end_minute_entry.insert(0, "mm")




        self.test_password_entry = Entry(self.frame1, width=20)
        self.test_password_entry.grid(row=20, column=1, sticky=W, pady=3)

        self.description_bar = Scrollbar(self.frame1)
        self.description_infobox = Text(self.frame1, height=4, width=40, font=('Helvetica', 9))
        self.description_bar.grid(row=2, column=2)
        self.description_infobox.grid(row=2, column=1, pady=10)
        self.description_bar.config(command=self.description_infobox.yview)
        self.description_infobox.config(yscrollcommand=self.description_bar.set)

        self.limit_users_max_amount_entry = Entry(self.frame1, width=5)
        self.limit_users_max_amount_entry.grid(row=22, column=1, sticky=W)
        self.inactivity_time_for_users_entry = Entry(self.frame1, width=5)
        self.inactivity_time_for_users_entry.grid(row=23, column=1, sticky=W)
        self.inactivity_time_for_users_entry.insert(0, "300")

        self.limit_test_runs_entry = Entry(self.frame1, width=10)
        self.limit_test_runs_entry.grid(row=25, column=1, sticky=W)
        self.limit_test_runs_entry.insert(0, "3")


        self.limit_time_betw_test_runs_month_entry = Entry(self.frame1, width=5)
        self.limit_time_betw_test_runs_month_entry.grid(row=26, column=1, sticky=W, pady=5)
        self.limit_time_betw_test_runs_month_entry.insert(0, "MM")
        self.limit_time_betw_test_runs_day_entry = Entry(self.frame1, width=5)
        self.limit_time_betw_test_runs_day_entry.grid(row=26, column=1, sticky=W, padx=35)
        self.limit_time_betw_test_runs_day_entry.insert(0, "DD")
        self.limit_time_betw_test_runs_hour_entry = Entry(self.frame1, width=5)
        self.limit_time_betw_test_runs_hour_entry.grid(row=26, column=1, sticky=W, padx=70)
        self.limit_time_betw_test_runs_hour_entry.insert(0, "HH")
        self.limit_time_betw_test_runs_minute_entry = Entry(self.frame1, width=5)
        self.limit_time_betw_test_runs_minute_entry.grid(row=26, column=1, sticky=W, padx=105)
        self.limit_time_betw_test_runs_minute_entry.insert(0, "mm")

        self.limit_processing_time_minutes_entry = Entry(self.frame1, width=5)
        self.limit_processing_time_minutes_entry.grid(row=28, column=1, sticky=W)
        self.limit_processing_time_minutes_entry.insert(0, "90")


        self.concluding_remarks_bar = Scrollbar(self.frame2)
        self.concluding_remarks_infobox = Text(self.frame2, height=4, width=40, font=('Helvetica', 9))



        self.profile_name_label = Label(self.frame3, text="Choose Profilname to save")
        self.profile_name_label.grid(row=0, column=0)

        self.profile_name_entry = Entry(self.frame3, width=15)
        self.profile_name_entry.grid(row=0, column=1)



        #self.profile_oid_label = Label(self.frame3, text="Choose oid to delete")
        #self.profile_oid_label.grid(row=4, column=0)

        self.profile_oid_entry = Entry(self.frame3, width=10)
        self.profile_oid_entry.grid(row=4, column=1)




        self.load_settings_entry = Entry(self.frame3, width=10)
        self.load_settings_entry.grid(row=3, column=1)

        #self.delete_settings_btn = Button(self.frame3, text="Delete Profile from ID", command=GUI_settings_window.profile_save_settings(self))
        #self.delete_settings_btn.grid(row=4, column=0)





        self.profile_oid_listbox_label = Label(self.frame3, text=" DB\nID")
        self.profile_oid_listbox_label.grid(row=1, column=4, sticky=W)

        self.profile_name_listbox_label = Label(self.frame3, text="Name")
        self.profile_name_listbox_label.grid(row=1, column=5, sticky=W)

        self.my_listbox_profile_oid = Listbox(self.frame3, width=5)
        self.my_listbox_profile_oid.grid(row=2, column=4, sticky=W)

        self.my_listbox_profile_name = Listbox(self.frame3, width=15)
        self.my_listbox_profile_name.grid(row=2, column=5, sticky=W)


        self.show_profiles_btn = Button(self.frame3, text="Show Profile from ID", command=lambda: GUI_settings_window.profile_show_db(self))
        self.show_profiles_btn.grid(row=5, column=0)

        self.save_settings_btn = Button(self.frame3, text="Save Settings", command=lambda: GUI_settings_window.profile_save_settings(self))
        self.save_settings_btn.grid(row=2, column=0)

        self.load_settings_btn = Button(self.frame3, text="Load Settings", command=lambda: GUI_settings_window.profile_load_settings(self))
        self.load_settings_btn.grid(row=3, column=0)

        self.delete_profile_btn = Button(self.frame3, text="Delete Profile", command=lambda: GUI_settings_window.profile_delete(self))
        self.delete_profile_btn.grid(row=4, column=0)

        self.create_profile_btn = Button(self.frame3, text="Create Profile-Settings", command=lambda: GUI_settings_window.create_settings(self))
        self.create_profile_btn.grid(row=6, column=0)

    def show_entry_time_limited_start(self, var):
        if var.get() == 0:
            self.time_limited_start_label.grid_forget()
            self.time_limited_start_year_label.grid_forget()
            self.time_limited_start_year_entry.grid_forget()
            self.time_limited_start_month_label.grid_forget()
            self.time_limited_start_month_entry.grid_forget()
            self.time_limited_start_day_label.grid_forget()
            self.time_limited_start_day_entry.grid_forget()
            self.time_limited_start_hour_label.grid_forget()
            self.time_limited_start_hour_entry.grid_forget()
            self.time_limited_start_minute_label.grid_forget()
            self.time_limited_start_minute_entry.grid_forget()

            self.time_limited_end_label.grid_forget()
            self.time_limited_end_year_label.grid_forget()
            self.time_limited_end_year_entry.grid_forget()
            self.time_limited_end_month_label.grid_forget()
            self.time_limited_end_month_entry.grid_forget()
            self.time_limited_end_day_label.grid_forget()
            self.time_limited_end_day_entry.grid_forget()
            self.time_limited_end_hour_label.grid_forget()
            self.time_limited_end_hour_entry.grid_forget()
            self.time_limited_end_minute_label.grid_forget()
            self.time_limited_end_minute_entry.grid_forget()

        else:
            self.time_limited_start_label.grid(row=10, column=1, sticky=W, padx=50)
            self.time_limited_start_day_label.grid(row=11, column=1, sticky=W, padx=30)
            self.time_limited_start_month_label.grid(row=11, column=1, sticky=W, padx=55)
            self.time_limited_start_year_label.grid(row=11, column=1, sticky=W, padx=80)
            self.time_limited_start_hour_label.grid(row=11, column=1, sticky=W, padx=110)
            self.time_limited_start_minute_label.grid(row=11, column=1, sticky=W, padx=135)

            self.time_limited_end_label.grid(row=10, column=1, sticky=E, padx=50)
            self.time_limited_end_day_label.grid(row=11, column=1, sticky=E, padx=110)
            self.time_limited_end_month_label.grid(row=11, column=1, sticky=E, padx=85)
            self.time_limited_end_year_label.grid(row=11, column=1, sticky=E, padx=55)
            self.time_limited_end_hour_label.grid(row=11, column=1, sticky=E, padx=30)
            self.time_limited_end_minute_label.grid(row=11, column=1, sticky=E, padx=5)

            self.time_limited_start_day_entry.grid(row=12, column=1, sticky=W, padx=30)
            self.time_limited_start_month_entry.grid(row=12, column=1, sticky=W, padx=55)
            self.time_limited_start_year_entry.grid(row=12, column=1, sticky=W, padx=80)
            self.time_limited_start_hour_entry.grid(row=12, column=1, sticky=W, padx=110)
            self.time_limited_start_minute_entry.grid(row=12, column=1, sticky=W, padx=135)

            self.time_limited_end_day_entry.grid(row=12, column=1, sticky=E, padx=110)
            self.time_limited_end_month_entry.grid(row=12, column=1, sticky=E, padx=85)
            self.time_limited_end_year_entry.grid(row=12, column=1, sticky=E, padx=55)
            self.time_limited_end_hour_entry.grid(row=12, column=1, sticky=E, padx=30)
            self.time_limited_end_minute_entry.grid(row=12, column=1, sticky=E, padx=5)

    def show_introduction_textfield(self, introduction_var):
        print(introduction_var.get())
        if introduction_var.get() == 0:

            self.introduction_bar.grid_forget()
            self.introduction_infobox.grid_forget()

        else:
            self.introduction_bar.grid(row=15, column=1, sticky=E)
            self.introduction_infobox.grid(row=15, column=1, padx=30)
            self.introduction_bar.config(command=self.introduction_infobox.yview)
            self.introduction_infobox.config(yscrollcommand=self.introduction_bar.set)

    def enable_autosave(self, var):
        if var.get() == 0:
           self.check_autosave_interval_entry.grid_forget()
           self.check_autosave_interval_label.grid_forget()

        else:
            self.check_autosave_interval_entry.grid(row=4, column=3, padx=10)
            self.check_autosave_interval_label.grid(row=4, column=3, padx=50, sticky=W)

    def show_concluding_remarks(self, var):
        if var.get() == 0:
            self.concluding_remarks_bar.grid_forget()
            self.concluding_remarks_infobox.grid_forget()

        else:
            self.concluding_remarks_bar.grid(row=22, column=3, sticky=E)
            self.concluding_remarks_infobox.grid(row=22, column=3, padx=30)
            self.concluding_remarks_bar.config(command=self.concluding_remarks_infobox.yview)
            self.concluding_remarks_infobox.config(yscrollcommand=self.concluding_remarks_bar.set)

    def profile_show_db(self):

        conn = sqlite3.connect('test_settings_profiles_db.db')
        c = conn.cursor()

        c.execute("SELECT *, oid FROM my_profiles_table")
        profile_records = c.fetchall()

        # Clear List Boxes

        self.my_listbox_profile_name.delete(0, END)
        self.my_listbox_profile_oid.delete(0, END)

        # Loop thru Results
        for profile_record in profile_records:
            self.my_listbox_profile_name.insert(END, profile_record[0])
            self.my_listbox_profile_oid.insert(END, profile_record[len(profile_record)-1])



        self.profile_records_len = len(profile_records)
        #print(profile_records[len(profile_records)-1])

        conn.commit()
        conn.close()
        print("LOOP THROUGH... SHOW PROFILES!")



    def profile_save_settings(self):


        conn = sqlite3.connect('test_settings_profiles_db.db')
        c = conn.cursor()

        # Insert into Table
        c.execute(
            "INSERT INTO my_profiles_table VALUES ("
            ":profile_name, :entry_description, :radio_select_question, :radio_select_anonymous, :check_online, :check_time_limited, "
            ":check_introduction, :entry_introduction, :check_test_properties, "
            ":entry_test_start_year, :entry_test_start_month, :entry_test_start_day, :entry_test_start_hour, :entry_test_start_minute,"
            ":entry_test_end_year, :entry_test_end_month, :entry_test_end_day, :entry_test_end_hour, :entry_test_end_minute,"
            ":entry_test_password, :check_specific_users, :entry_limit_users, :entry_user_inactivity, :entry_limit_test_runs,"
            ":entry_limit_time_betw_test_run_month, :entry_limit_time_betw_test_run_day, :entry_limit_time_betw_test_run_hour, :entry_limit_time_betw_test_run_minute,"
            ":check_processing_time, :entry_processing_time_in_minutes, :check_processing_time_reset,"
            ":check_examview, :check_examview_titel, :check_examview_username, :check_show_ilias_nr,"
            ":radio_select_show_question_title, :check_autosave, :entry_autosave_interval, :check_mix_questions, :check_show_solution_notes, :check_direct_response,"
            ":radio_select_user_response, :check_mandatory_questions, :check_use_previous_solution, :check_show_test_cancel, :radio_select_not_answered_questions,"
            ":check_show_question_list_process_status, :check_question_mark, :check_overview_answers, :check_show_end_comment, :entry_end_comment, :check_forwarding, :check_notification)",
            {
                'profile_name': self.profile_name_entry.get(),
                'entry_description': self.description_infobox.get("1.0", 'end-1c'),
                'radio_select_question': self.select_question.get(),
                'radio_select_anonymous': self.select_anonym.get(),
                'check_online': self.var_online.get(),
                'check_time_limited': self.var_time_limited.get(),

                'check_introduction': self.var_introduction.get(),
                'entry_introduction': self.introduction_infobox.get("1.0", 'end-1c'),
                'check_test_properties': self.var_test_prop.get(),

                'entry_test_start_year': self.test_start_year_entry.get(),
                'entry_test_start_month': self.test_start_month_entry.get(),
                'entry_test_start_day': self.test_start_day_entry.get(),
                'entry_test_start_hour': self.test_start_hour_entry.get(),
                'entry_test_start_minute': self.test_start_minute_entry.get(),

                'entry_test_end_year': self.test_end_year_entry.get(),
                'entry_test_end_month': self.test_end_month_entry.get(),
                'entry_test_end_day': self.test_end_day_entry.get(),
                'entry_test_end_hour': self.test_end_hour_entry.get(),
                'entry_test_end_minute': self.test_end_minute_entry.get(),


                'entry_test_password': self.test_password_entry.get(),
                'check_specific_users': self.var_specific_users.get(),
                'entry_limit_users': self.limit_users_max_amount_entry.get(),
                'entry_user_inactivity': self.inactivity_time_for_users_entry.get(),
                'entry_limit_test_runs': self.limit_test_runs_entry.get(),

                'entry_limit_time_betw_test_run_month': self.limit_time_betw_test_runs_month_entry.get(),
                'entry_limit_time_betw_test_run_day': self.limit_time_betw_test_runs_day_entry.get(),
                'entry_limit_time_betw_test_run_hour': self.limit_time_betw_test_runs_hour_entry.get(),
                'entry_limit_time_betw_test_run_minute': self.limit_time_betw_test_runs_minute_entry.get(),

                'check_processing_time': self.var_processing_time.get(),
                'entry_processing_time_in_minutes': self.limit_processing_time_minutes_entry.get(),
                'check_processing_time_reset': self.var_processing_time_reset.get(),
                
                'check_examview': self.var_examview.get(),
                'check_examview_titel': self.var_examview_test_title.get(),
                'check_examview_username': self.var_examview_user_name.get(),
                'check_show_ilias_nr': self.var_show_ilias_nr.get(),

                'radio_select_show_question_title': self.select_show_question_title.get(),
                'check_autosave': self.var_autosave.get(),
                'entry_autosave_interval': self.check_autosave_interval_entry.get(),
                'check_mix_questions': self.var_mix_questions.get(),
                'check_show_solution_notes': self.var_show_solution_notes.get(),
                'check_direct_response': self.var_direct_response.get(),

                'radio_select_user_response': self.select_user_response.get(),
                'check_mandatory_questions': self.var_mandatory_questions.get(),
                'check_use_previous_solution' : self.var_use_previous_solution.get(),
                'check_show_test_cancel': self.var_show_test_cancel.get(),
                'radio_select_not_answered_questions': self.select_not_answered_questions.get(),

                'check_show_question_list_process_status': self.var_show_question_list_process_status.get(),
                'check_question_mark': self.var_question_mark.get(),
                'check_overview_answers': self.var_overview_answers.get(),
                'check_show_end_comment': self.var_show_end_comment.get(),
                'entry_end_comment': self.concluding_remarks_infobox.get("1.0", 'end-1c'),
                'check_forwarding': self.var_forwarding.get(),
                'check_notification': self.var_notification.get()


            }
        )
        conn.commit()
        conn.close()
        print("GOT VALUES")

    def profile_load_settings(self):
        print("LOAD")

        conn = sqlite3.connect('test_settings_profiles_db.db')
        c = conn.cursor()

        c.execute("SELECT * FROM my_profiles_table WHERE oid =" + self.load_settings_entry.get())



        profile_records = c.fetchall()
        # Loop thru Results
        for profile_record in profile_records:
            self.profile_name_entry.get()
        #   profil_name_entry -> profile_record[0]
            self.description_infobox.delete('1.0', END)
            self.description_infobox.insert('1.0', profile_record[1])
            self.select_question.set(profile_record[2])
            self.select_anonym.set(profile_record[3])
            self.var_online.set(profile_record[4])
            self.var_time_limited.set(profile_record[5])
            self.var_introduction.set(profile_record[6])
            self.introduction_infobox.delete('1.0', END)
            self.introduction_infobox.insert('1.0', profile_record[7])
            self.var_test_prop.set(profile_record[8])

            self.test_start_year_entry.delete(0, END)
            self.test_start_year_entry.insert(0, profile_record[9])
            self.test_start_month_entry.delete(0, END)
            self.test_start_month_entry.insert(0, profile_record[10])
            self.test_start_day_entry.delete(0, END)
            self.test_start_day_entry.insert(0, profile_record[11])
            self.test_start_hour_entry.delete(0, END)
            self.test_start_hour_entry.insert(0, profile_record[12])
            self.test_start_minute_entry.delete(0, END)
            self.test_start_minute_entry.insert(0, profile_record[13])

            self.test_end_year_entry.delete(0, END)
            self.test_end_year_entry.insert(0, profile_record[14])
            self.test_end_month_entry.delete(0, END)
            self.test_end_month_entry.insert(0, profile_record[15])
            self.test_end_day_entry.delete(0, END)
            self.test_end_day_entry.insert(0, profile_record[16])
            self.test_end_hour_entry.delete(0, END)
            self.test_end_hour_entry.insert(0, profile_record[17])
            self.test_end_minute_entry.delete(0, END)
            self.test_end_minute_entry.insert(0, profile_record[18])

            self.test_password_entry.delete(0, END)
            self.test_password_entry.insert(0, profile_record[19])
            self.var_specific_users.set(profile_record[20])
            self.limit_users_max_amount_entry.delete(0, END)
            self.limit_users_max_amount_entry.insert(0, profile_record[21])
            self.inactivity_time_for_users_entry.delete(0, END)
            self.inactivity_time_for_users_entry.insert(0, profile_record[22])
            self.limit_test_runs_entry.delete(0, END)
            self.limit_test_runs_entry.insert(0, profile_record[23])

            self.limit_time_betw_test_runs_month_entry.delete(0, END)
            self.limit_time_betw_test_runs_month_entry.insert(0, profile_record[24])
            self.limit_time_betw_test_runs_day_entry.delete(0, END)
            self.limit_time_betw_test_runs_day_entry.insert(0, profile_record[25])
            self.limit_time_betw_test_runs_hour_entry.delete(0, END)
            self.limit_time_betw_test_runs_hour_entry.insert(0, profile_record[26])
            self.limit_time_betw_test_runs_minute_entry.delete(0, END)
            self.limit_time_betw_test_runs_minute_entry.insert(0, profile_record[27])

            self.var_processing_time.set(profile_record[28])
            self.limit_processing_time_minutes_entry.delete(0, END)
            self.limit_processing_time_minutes_entry.insert(0, profile_record[29])
            self.var_processing_time_reset.set(profile_record[30])

            self.var_examview.set(profile_record[31])
            self.var_examview_test_title.set(profile_record[32])
            self.var_examview_user_name.set(profile_record[33])
            self.var_show_ilias_nr.set(profile_record[34])
            self.select_show_question_title.set(profile_record[35])
            self.var_autosave.set(profile_record[36])
            self.check_autosave_interval_entry.delete(0, END)
            self.check_autosave_interval_entry.insert(0, profile_record[37])
            self.var_mix_questions.set(profile_record[38])
            self.var_show_solution_notes.set(profile_record[39])
            self.var_direct_response.set(profile_record[40])
            self.select_user_response.set(profile_record[41])
            self.var_mandatory_questions.set(profile_record[42])
            self.var_use_previous_solution.set(profile_record[43])
            self.var_show_test_cancel.set(profile_record[44])
            self.select_not_answered_questions.set(profile_record[45])
            self.var_show_question_list_process_status.set(profile_record[46])
            self.var_question_mark.set(profile_record[47])
            self.var_overview_answers.set(profile_record[48])
            self.var_show_end_comment.set(profile_record[49])
            self.concluding_remarks_infobox.delete('1.0', END)
            self.concluding_remarks_infobox.insert('1.0', profile_record[50])
            self.var_forwarding.set(profile_record[51])
            self.var_notification.set(profile_record[52])

        conn.commit()
        conn.close()

    def profile_delete(self):

        conn = sqlite3.connect('test_settings_profiles_db.db')
        c = conn.cursor()

        c.execute("DELETE from my_profiles_table WHERE oid= " + self.profile_oid_entry.get())

        #self.profile_oid_entry(0, END)

        conn.commit()
        conn.close()

    def profile_delete_last(self):

        conn = sqlite3.connect('test_settings_profiles_db.db')
        c = conn.cursor()
        self.profile_oid_entry.insert(0, self.profile_records_len)
        c.execute("DELETE from my_profiles_table WHERE oid= " + self.profile_oid_entry.get())
        print("LAST DB ENTRY DELETED")
        #self.profile_oid_entry(0, END)

        conn.commit()
        conn.close()




    def create_settings(self):

        #profile_name --> profile_record[0]_
        self.description = self.description_infobox.get("1.0", 'end-1c')
        self.question_type = self.select_question.get()
        self.anonym = self.select_anonym.get()
        self.online = self.var_online.get()
        self.time_limited = self.var_time_limited.get()
        self.introduction_check = self.var_introduction.get()
        self.introduction_text = self.introduction_infobox.get("1.0", 'end-1c')
        self.test_prop = self.var_test_prop.get()

        self.test_start_year = self.test_start_year_entry.get()
        self.test_start_month=  self.test_start_month_entry.get()
        self.test_start_day=  self.test_start_day_entry.get()
        self.test_start_hour=  self.test_start_hour_entry.get()
        self.test_start_minute=  self.test_start_minute_entry.get()

        self.test_end_year = self.test_end_year_entry.get()
        self.test_end_month= self.test_end_month_entry.get()
        self.test_end_day= self.test_end_day_entry.get()
        self.test_end_hour= self.test_end_hour_entry.get()
        self.test_end_minute= self.test_end_minute_entry.get()

        self.test_password = self.test_password_entry.get()
        self.specific_users = self.var_specific_users.get()
        self.limit_users_max = self.limit_users_max_amount_entry.get()
        self.inactivity_time_for_users = self.inactivity_time_for_users_entry.get()
        self.limit_test_runs = self.limit_test_runs_entry.get()

        self.limit_time_betw_test_runs_month = self.limit_time_betw_test_runs_month_entry.get()
        self.limit_time_betw_test_runs_day = self.limit_time_betw_test_runs_day_entry.get()
        self.limit_time_betw_test_runs_hour = self.limit_time_betw_test_runs_hour_entry.get()
        self.limit_time_betw_test_runs_minute = self.limit_time_betw_test_runs_minute_entry.get()

        self.processing_time = self.var_processing_time.get()
        self.limit_processing_time_minutes = self.limit_processing_time_minutes_entry.get()
        self.check_processing_time_reset = self.var_processing_time_reset.get()

        self.examview = self.var_examview.get()
        self.examview_test_title = self.var_examview_test_title.get()
        self.examview_user_name = self.var_examview_user_name.get()
        self.show_ilias_nr = self.var_show_ilias_nr.get()
        self.show_question_title = self.select_show_question_title.get()
        self.autosave = self.var_autosave.get()
        self.autosave_interval = self.check_autosave_interval_entry.get()

        self.mix_questions = self.var_mix_questions.get()
        self.show_solution_notes = self.var_show_solution_notes.get()
        self.direct_response = self.var_direct_response.get()
        self.user_response = self.select_user_response.get()
        self.mandatory_questions = self.var_mandatory_questions.get()
        self.use_previous_solution = self.var_use_previous_solution.get()
        self.show_test_cancel = self.var_show_test_cancel.get()
        self.not_answered_questions = self.select_not_answered_questions.get()
        self.show_question_list_process_status = self.var_show_question_list_process_status.get()
        self.question_mark = self.var_question_mark.get()
        self.overview_answers = self.var_overview_answers.get()
        self.show_end_comment = self.var_show_end_comment.get()
        self.concluding_remarks = self.concluding_remarks_infobox.get("1.0", 'end-1c')
        self.forwarding = self.var_forwarding.get()
        self.notification = self.var_notification.get()


        self.mytree = ET.parse(self.qti_file_path_write)
        self.myroot = self.mytree.getroot()


        for qtimetadatafield in self.myroot.iter('qtimetadatafield'):

            if qtimetadatafield.find('fieldlabel').text == "anonymity":
                qtimetadatafield.find('fieldentry').text = self.anonym
                if self.anonym == "":
                    qtimetadatafield.find('fieldentry').text = "0"
                    print("NO ENTRY IN <ANONYM>")


            if qtimetadatafield.find('fieldlabel').text == "question_set_type":
                if self.question_type == 0:
                    qtimetadatafield.find('fieldentry').text = "FIXED_QUEST_SET"
                    print("WRITE FIXED")

                elif self.question_type == 1:
                    qtimetadatafield.find('fieldentry').text = "RANDOM_QUEST_SET"
                    print("WRITE RANDOM")

                elif self.question_type == 2:
                    qtimetadatafield.find('fieldentry').text = "DYNAMIC_QUEST_SET"
                    print("WRITE DYNAMIC")
                else:
                    qtimetadatafield.find('fieldentry').text = "FIXED_QUEST_SET"
                    print("NO ENTRY IN <QUESTION_TYPE> ")

            #if qtimetadatafield.find('fieldlabel').text == "author":
                #qtimetadatafield.find('fieldentry').text = str(Formelfrage.autor_entry.get())

            if qtimetadatafield.find('fieldlabel').text == "reset_processing_time":
                qtimetadatafield.find('fieldentry').text = str(self.check_processing_time_reset)
                if self.check_processing_time_reset == "":
                    qtimetadatafield.find('fieldentry').text = "0"
                    print("NO ENTRY IN <RESET PROCESSING TIME>")

            if qtimetadatafield.find('fieldlabel').text == "password":
                qtimetadatafield.find('fieldentry').text = str(self.test_password)


            if qtimetadatafield.find('fieldlabel').text == "allowedUsers":
                qtimetadatafield.find('fieldentry').text = str(self.limit_users_max)

            if qtimetadatafield.find('fieldlabel').text == "allowedUsersTimeGap":
                qtimetadatafield.find('fieldentry').text = str(self.inactivity_time_for_users)

            if qtimetadatafield.find('fieldlabel').text == "nr_of_tries":
                qtimetadatafield.find('fieldentry').text = str(self.limit_test_runs)

            if qtimetadatafield.find('fieldlabel').text == "pass_waiting":
               qtimetadatafield.find('fieldentry').text = str(self.limit_time_betw_test_runs_month) + ":0" + str(self.limit_time_betw_test_runs_day) + ":" + str(self.limit_time_betw_test_runs_hour) + ":" + str(self.limit_time_betw_test_runs_minute) + ":00"
               if self.limit_time_betw_test_runs_month == "MM":
                    qtimetadatafield.find('fieldentry').text = "00:000:00:00:00"
                    print(" >WARNING< NO limit_time_betw_test_runs SET")
                    print("--> set limit_time to \"00:000:00:00:00\" ")

            #Prüfungsansicht: Alle drei haken (Titel+Ansicht): "7" / Zwei Haken (Titel) = "3" / Zwei Haken (Name) = "5" / Ein Haken = "1" / "0" -> deaktiviert
            if qtimetadatafield.find('fieldlabel').text == "kiosk":
                if self.examview == 0:
                    qtimetadatafield.find('fieldentry').text = "0"
                elif self.examview == 1:
                    qtimetadatafield.find('fieldentry').text = "1"
                elif self.examview == 1 and self.examview_test_title == 1:
                    qtimetadatafield.find('fieldentry').text = "3"
                elif self.examview == 1 and self.examview_user_name == 1:
                    qtimetadatafield.find('fieldentry').text = "5"
                elif self.examview == 1 and self.examview_user_name == 1 and self.examview_test_title == 1:
                    qtimetadatafield.find('fieldentry').text = "7"




            #if qtimetadatafield.find('fieldlabel').text == "use_previous_answers":
                #qtimetadatafield.find('fieldentry').text = "0"

            #if qtimetadatafield.find('fieldlabel').text == "title_output":
                #qtimetadatafield.find('fieldentry').text = "0"

            #if qtimetadatafield.find('fieldlabel').text == "examid_in_test_pass":
                #qtimetadatafield.find('fieldentry').text = "0"

           #if qtimetadatafield.find('fieldlabel').text == "show_summary":
                #qtimetadatafield.find('fieldentry').text = "0"

            if qtimetadatafield.find('fieldlabel').text == "show_cancel":
                qtimetadatafield.find('fieldentry').text = str(self.show_test_cancel)

            #if qtimetadatafield.find('fieldlabel').text == "show_marker":
                #qtimetadatafield.find('fieldentry').text = "99"

            #if qtimetadatafield.find('fieldlabel').text == "fixed_participants":
               #qtimetadatafield.find('fieldentry').text = "99"

          #  if qtimetadatafield.find('fieldlabel').text == "showinfo":
                #qtimetadatafield.find('fieldentry').text = "99"

            if qtimetadatafield.find('fieldlabel').text == "shuffle_questions":
                qtimetadatafield.find('fieldentry').text = str(self.mix_questions)

            if qtimetadatafield.find('fieldlabel').text == "processing_time":

                #self.minutes = self.limit_processing_time_minutes
                hour_to_minutes = str(datetime.timedelta(minutes=int(self.limit_processing_time_minutes)))
                qtimetadatafield.find('fieldentry').text = "0" + hour_to_minutes

            if qtimetadatafield.find('fieldlabel').text == "enable_examview":
                qtimetadatafield.find('fieldentry').text = str(self.examview)

            #if qtimetadatafield.find('fieldlabel').text == "show_examview_pdf":
                #qtimetadatafield.find('fieldentry').text = "99"

            if qtimetadatafield.find('fieldlabel').text == "starting_time":
                qtimetadatafield.find('fieldentry').text = "P" + str(self.test_start_year) + "Y" + str(self.test_start_month) + "M" +  str(self.test_start_day) + "DT" + str(self.test_start_hour) + "H" + str(self.test_start_minute) + "M" + "0S"
                if self.test_start_year == "YYYY":
                    qtimetadatafield.find('fieldentry').text = "P2020Y1M1DT00H0M0S"
                    print(" >WARNING< NO STARTING TIME SET")
                    print("--> set START to \"P2020Y1M1DT00H0M0S\"")

            if qtimetadatafield.find('fieldlabel').text == "ending_time":
                qtimetadatafield.find('fieldentry').text = "P" + str(self.test_end_year) + "Y" + str(self.test_end_month) + "M" +  str(self.test_end_day) + "DT" + str(self.test_end_hour) + "H" + str(self.test_end_minute) + "M" + "0S"
                if self.test_end_year == "YYYY":
                    qtimetadatafield.find('fieldentry').text = "P2020Y12M30DT00H0M0S"
                    print(" >WARNING< NO ENDING TIME SET")
                    print("--> set END to \"P2020Y12M30DT00H0M0S\"")

            if qtimetadatafield.find('fieldlabel').text == "autosave":
                qtimetadatafield.find('fieldentry').text = str(self.autosave)

            if qtimetadatafield.find('fieldlabel').text == "autosave_ival":
                qtimetadatafield.find('fieldentry').text = str(self.autosave_interval)

            #if qtimetadatafield.find('fieldlabel').text == "offer_question_hints":
                #qtimetadatafield.find('fieldentry').text = "99"

            #if qtimetadatafield.find('fieldlabel').text == "obligations_enabled":
                #qtimetadatafield.find('fieldentry').text = "99"

            if qtimetadatafield.find('fieldlabel').text == "enable_processing_time":
                qtimetadatafield.find('fieldentry').text = str(self.processing_time)

            #if qtimetadatafield.find('fieldlabel').text == "mark_step_0":
                #qtimetadatafield.find('fieldentry').text = "99"

            #if qtimetadatafield.find('fieldlabel').text == "mark_step_1":
                #qtimetadatafield.find('fieldentry').text = "99"

            #tree = ET.ElementTree(questestinterop)
            #tree.write("WORKED_neuerAnfang.xml")

        print("Write Test_Settings to File")
        self.mytree.write(self.qti_file_path_write)

# print("--------------------3-----------------------------")


app = Tk()
GUI = GuiMainWindow(app)
app.mainloop()
#def save_settings_to_database():









def trash_class():
    """
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