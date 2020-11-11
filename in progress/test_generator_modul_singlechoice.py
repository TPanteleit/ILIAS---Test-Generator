
import xml.etree.ElementTree as ET
from tkinter import *                  # Stellt die Funktionen für z.B. Labels & Entrys zur Verfügung
from tkinter import ttk                # Stellt die Funktionen der Comboboxen (Auswahlboxen) zur Verfügung
from tkinter import filedialog
import base64
import pathlib
import sqlite3
import os
import pprint
import pandas as pd
from datetime import datetime

### Eigene Dateien / Module
import test_generator_modul_datenbanken_anzeigen



class SingleChoice:
    def __init__(self, app, singlechoice_tab, project_root_path):
        self.singlechoice_tab = singlechoice_tab
        
        
        ###### DEFINE SINGLECHOICE PATHS
        
        self.project_root_path = project_root_path
        self.singlechoice_files_path = os.path.normpath(os.path.join(self.project_root_path, "SingleChoice"))
        
        

        self.singlechoice_test_qti_file_path_template = os.path.normpath(os.path.join(self.singlechoice_files_path, "sc_test_qti_und_tst_dateien_vorlage", "ilias_test_vorlage__qti__.xml"))
        self.singlechoice_test_tst_file_path_template = os.path.normpath(os.path.join(self.singlechoice_files_path, "sc_test_qti_und_tst_dateien_vorlage", "ilias_test_vorlage__tst__.xml"))
        
        self.singlechoice_pool_qti_file_path_template = os.path.normpath(os.path.join(self.singlechoice_files_path, "sc_pool_qti_und_qpl_dateien_vorlage", "ilias_pool_vorlage__qti__.xml"))
        self.singlechoice_pool_qpl_file_path_template = os.path.normpath(os.path.join(self.singlechoice_files_path, "sc_pool_qti_und_qpl_dateien_vorlage", "ilias_pool_vorlage__qti__.xml"))
        
        
        self.singlechoice_test_qti_file_path_output = os.path.normpath(os.path.join(self.singlechoice_files_path,"sc_ilias_test_abgabe", "1604407426__0__qti_2040314.xml"))
        self.singlechoice_test_tst_file_path_output = os.path.normpath(os.path.join(self.singlechoice_files_path,"sc_ilias_test_abgabe", "1604407426__0__tst_2040314.xml"))
        
        

        ###### FRAMES
        self.sc_frame_ilias_test_title = LabelFrame(self.singlechoice_tab, text="Testname & Autor", padx=5, pady=5)
        self.sc_frame_ilias_test_title.grid(row=0, column=0, padx=10, pady=10, sticky=NW)
        
        self.sc_frame = LabelFrame(self.singlechoice_tab, text="Single Choice", padx=5, pady=5)
        self.sc_frame.grid(row=1, column=0, padx=10, pady=10, sticky=NW)

        self.sc_frame_question_attributes = LabelFrame(self.singlechoice_tab, text="Fragen Attribute", padx=5, pady=5)
        self.sc_frame_question_attributes.grid(row=9, column=0, padx=170, pady=10, sticky="NW")

        self.sc_frame_question_description_functions = LabelFrame(self.singlechoice_tab, text="Fragentext Funktionen", padx=5, pady=5)
        self.sc_frame_question_description_functions.grid(row=9, column=0, padx=10, pady=10, sticky="NW")

        self.sc_frame_database = LabelFrame(self.singlechoice_tab, text="SingleChoice-Datenbank", padx=5, pady=5)
        self.sc_frame_database.grid(row=10, column=0, padx=10, pady=10, sticky=NW)
        
        self.sc_frame_create_singlechoice_test = LabelFrame(self.singlechoice_tab, text="Singlechoice-Test erstellen", padx=5, pady=5)
        self.sc_frame_create_singlechoice_test.grid(row=10, column=0, padx=0, pady=10, sticky="NE")
        
 
    
 ###################### "Testname % Autor" - FRAME   -------- LABELS / ENTRYS / BUTTONS  ################
 
        self.sc_ilias_test_title_label = Label(self.sc_frame_ilias_test_title, text="Name des Tests")
        self.sc_ilias_test_title_label.grid(row=0, column=0, sticky=W)

        self.sc_ilias_test_title_entry = Entry(self.sc_frame_ilias_test_title, width=60)
        self.sc_ilias_test_title_entry.grid(row=0, column=1, sticky=W, padx=30)

        self.sc_ilias_autor_label = Label(self.sc_frame_ilias_test_title, text="Autor")
        self.sc_ilias_autor_label.grid(row=1, column=0, sticky=W)

        self.sc_ilias_autor_entry = Entry(self.sc_frame_ilias_test_title, width=60)
        self.sc_ilias_autor_entry.grid(row=1, column=1, sticky=W, padx=30) 
        
        
 ###################### "Single Choice" - FRAME   -------- LABELS / ENTRYS / BUTTONS  ###################
       
        self.sc_question_title_label = Label(self.sc_frame, text="Fragen-Titel")
        self.sc_question_title_label.grid(row=0, column=0, sticky=W, padx=10, pady=(10, 0))
        self.sc_question_title_entry = Entry(self.sc_frame, width=60)
        self.sc_question_title_entry.grid(row=0, column=1, pady=(10, 0), sticky=W)

        # sc_author_label = Label(sc_frame, text="Autor")
        # sc_author_label.grid(row=1, column=0, sticky=W, padx=10)
        # sc_author_entry = Entry(sc_frame, width=60)
        # sc_author_entry.grid(row=1, column=1, sticky=W)

        self.sc_question_description_label = Label(self.sc_frame, text="Fragen-Beschreibung")
        self.sc_question_description_label.grid(row=2, column=0, sticky=W, padx=10)
        self.sc_question_description_entry = Entry(self.sc_frame, width=60)
        self.sc_question_description_entry.grid(row=2, column=1, sticky=W)

        self.sc_question_textfield_label = Label(self.sc_frame, text="Fragen-Text")
        self.sc_question_textfield_label.grid(row=3, column=0, sticky=W, padx=10)

        self.sc_bar = Scrollbar(self.sc_frame)
        self.sc_infobox = Text(self.sc_frame, height=6, width=80, font=('Helvetica', 9))
        self.sc_bar.grid(row=3, column=2, sticky=W)
        self.sc_infobox.grid(row=3, column=1, pady=10, sticky=W)
        self.sc_bar.config(command=self.sc_infobox.yview)
        self.sc_infobox.config(yscrollcommand=self.sc_bar.set)

        self.sc_processing_time_label = Label(self.sc_frame, text="Bearbeitungsdauer")
        self.sc_processing_time_label.grid(row=4, column=0, sticky=W, pady=(5, 0), padx=10)

        self.sc_processing_time_label = Label(self.sc_frame, text="Std:")
        self.sc_processing_time_label.grid(row=4, column=1, sticky=W, pady=(5, 0))
        self.sc_processing_time_label = Label(self.sc_frame, text="Min:")
        self.sc_processing_time_label.grid(row=4, column=1, sticky=W, padx=70, pady=(5, 0))
        self.sc_processing_time_label = Label(self.sc_frame, text="Sek:")
        self.sc_processing_time_label.grid(row=4, column=1, sticky=W, padx=145, pady=(5, 0))

        ### Preview LaTeX
        # expr = r'$$  {\text{Zu berechnen ist:  }}\  sin(x^2)\ {\text{Textblock 2}}\ {formel2} $$'
        # preview(expr, viewer='file', filename='output.png')

        # file_image = ImageTk.PhotoImage(Image.open('output.png'))
        # file_image_label = Label(self.sc_frame, image=file_image)
        # file_image_label.image = file_image

        # def latex_preview():
        #    file_image_label.grid(row=20, column=1, pady=20)

        # self.myLatex_btn = Button(self.sc_frame, text="show LaTeX Preview", command=latex_preview)
        # self.myLatex_btn.grid(row=4, column=1, sticky=E)

        ###

        self.sc_processingtime_hours = list(range(24))
        self.sc_processingtime_minutes = list(range(60))
        self.sc_processingtime_seconds = list(range(60))

        self.sc_proc_hours_box = ttk.Combobox(self.sc_frame, value=self.sc_processingtime_hours, width=2)
        self.sc_proc_minutes_box = ttk.Combobox(self.sc_frame, value=self.sc_processingtime_minutes, width=2)
        self.sc_proc_seconds_box = ttk.Combobox(self.sc_frame, value=self.sc_processingtime_seconds, width=2)

        self.sc_proc_hours_box.current(0)
        self.sc_proc_minutes_box.current(0)
        self.sc_proc_seconds_box.current(0)

        self.sc_proc_hours_box.bind("<<ComboboxSelected>>")
        self.sc_proc_hours_box.bind("<<ComboboxSelected>>")
        self.sc_proc_hours_box.bind("<<ComboboxSelected>>")

        self.sc_proc_hours_box.grid(row=4, column=1, sticky=W, padx=25, pady=(5, 0))
        self.sc_proc_minutes_box.grid(row=4, column=1, sticky=W, padx=100, pady=(5, 0))
        self.sc_proc_seconds_box.grid(row=4, column=1, sticky=W, padx=170, pady=(5, 0))

        self.sc_mix_questions_label = Label(self.sc_frame, text="Fragen mischen")
        self.sc_mix_questions_label.grid(row=5, column=0, sticky=W, padx=10, pady=(5, 0))

        self.sc_var_mix_questions = StringVar()
        self.sc_check_mix_questions = Checkbutton(self.sc_frame, text="", variable=self.sc_var_mix_questions,
                                                  onvalue="1", offvalue="0")
        self.sc_check_mix_questions.deselect()
        self.sc_check_mix_questions.grid(row=5, column=1, sticky=W, pady=(5, 0))

        def sc_answer_selected(event):  # "event" is necessary here to react, although it is not used "officially"

            if self.sc_numbers_of_answers_box.get() == '1':
                sc_var2_remove()
                sc_var3_remove()
                sc_var4_remove()
                sc_var5_remove()
                sc_var6_remove()
                sc_var7_remove()


            elif self.sc_numbers_of_answers_box.get() == '2':
                sc_var2_show()
                sc_var3_remove()
                sc_var4_remove()
                sc_var5_remove()
                sc_var6_remove()
                sc_var7_remove()


            elif self.sc_numbers_of_answers_box.get() == '3':
                sc_var2_show()
                sc_var3_show()
                sc_var4_remove()
                sc_var5_remove()
                sc_var6_remove()
                sc_var7_remove()


            elif self.sc_numbers_of_answers_box.get() == '4':
                sc_var2_show()
                sc_var3_show()
                sc_var4_show()
                sc_var5_remove()
                sc_var6_remove()
                sc_var7_remove()


            elif self.sc_numbers_of_answers_box.get() == '5':
                sc_var2_show()
                sc_var3_show()
                sc_var4_show()
                sc_var5_show()
                sc_var6_remove()
                sc_var7_remove()


            elif self.sc_numbers_of_answers_box.get() == '6':
                sc_var2_show()
                sc_var3_show()
                sc_var4_show()
                sc_var5_show()
                sc_var6_show()
                sc_var7_remove()


            elif self.sc_numbers_of_answers_box.get() == '7':
                sc_var2_show()
                sc_var3_show()
                sc_var4_show()
                sc_var5_show()
                sc_var6_show()
                sc_var7_show()

        self.sc_numbers_of_answers_box_label = Label(self.sc_frame, text="Anzahl der Antworten")
        self.sc_numbers_of_answers_box_label.grid(row=8, column=0, sticky=W, padx=10, pady=(5, 0))
        self.sc_numbers_of_answers_value = ["1", "2", "3", "4", "5", "6", "7"]
        self.sc_numbers_of_answers_box = ttk.Combobox(self.sc_frame, value=self.sc_numbers_of_answers_value, width=20)
        self.sc_numbers_of_answers_box.bind("<<ComboboxSelected>>", sc_answer_selected)
        self.sc_numbers_of_answers_box.grid(row=8, column=1, sticky=W, pady=(5, 0))
        self.sc_numbers_of_answers_box.current(0)

        # self.Label(self.sc_frame, text="Antworten").grid(row=9, column=0, sticky=W, padx=10, pady=(5, 0))
        # self.Label(self.sc_frame, text="Antwort-Text").grid(row=9, column=1, sticky=W, pady=(5, 0))
        self.sc_response_img_label = Label(self.sc_frame, text="Antwort-Grafik")
        self.sc_response_img_label.grid(row=8, column=1, sticky=E, padx=40)
        self.sc_response_points_label = Label(self.sc_frame, text="Punkte")
        self.sc_response_points_label.grid(row=8, column=2, sticky=W, padx=20)

        # ------------------------------- VARIABLES - TEXT & ENTRY --------------------------------------------
        self.sc_var1_answer_text, self.sc_var1_points_text, self.sc_var1_img_label_text = StringVar(), StringVar(), StringVar()
        self.sc_var2_answer_text, self.sc_var2_points_text, self.sc_var2_img_label_text = StringVar(), StringVar(), StringVar()
        self.sc_var3_answer_text, self.sc_var3_points_text, self.sc_var3_img_label_text = StringVar(), StringVar(), StringVar()
        self.sc_var4_answer_text, self.sc_var4_points_text, self.sc_var4_img_label_text = StringVar(), StringVar(), StringVar()
        self.sc_var5_answer_text, self.sc_var5_points_text, self.sc_var5_img_label_text = StringVar(), StringVar(), StringVar()
        self.sc_var6_answer_text, self.sc_var6_points_text, self.sc_var6_img_label_text = StringVar(), StringVar(), StringVar()
        self.sc_var7_answer_text, self.sc_var7_points_text, self.sc_var7_img_label_text = StringVar(), StringVar(), StringVar()

        self.sc_var1_img_data = ""
        self.sc_var2_img_data = ""
        self.sc_var3_img_data = ""
        self.sc_var3_img_data = ""
        self.sc_var4_img_data = ""
        self.sc_var5_img_data = ""
        self.sc_var6_img_data = ""
        self.sc_var7_img_data = ""

        self.sc_var1_answer_entry = Entry(self.sc_frame, textvariable=self.sc_var1_answer_text, width=40)
        self.sc_var2_answer_entry = Entry(self.sc_frame, textvariable=self.sc_var2_answer_text, width=40)
        self.sc_var3_answer_entry = Entry(self.sc_frame, textvariable=self.sc_var3_answer_text, width=40)
        self.sc_var4_answer_entry = Entry(self.sc_frame, textvariable=self.sc_var4_answer_text, width=40)
        self.sc_var5_answer_entry = Entry(self.sc_frame, textvariable=self.sc_var5_answer_text, width=40)
        self.sc_var6_answer_entry = Entry(self.sc_frame, textvariable=self.sc_var6_answer_text, width=40)
        self.sc_var7_answer_entry = Entry(self.sc_frame, textvariable=self.sc_var7_answer_text, width=40)


        self.sc_var1_points_entry = Entry(self.sc_frame, textvariable=self.sc_var1_points_text, width=8)
        self.sc_var2_points_entry = Entry(self.sc_frame, textvariable=self.sc_var2_points_text, width=8)
        self.sc_var3_points_entry = Entry(self.sc_frame, textvariable=self.sc_var3_points_text, width=8)
        self.sc_var4_points_entry = Entry(self.sc_frame, textvariable=self.sc_var4_points_text, width=8)
        self.sc_var5_points_entry = Entry(self.sc_frame, textvariable=self.sc_var5_points_text, width=8)
        self.sc_var6_points_entry = Entry(self.sc_frame, textvariable=self.sc_var6_points_text, width=8)
        self.sc_var7_points_entry = Entry(self.sc_frame, textvariable=self.sc_var7_points_text, width=8)

        # ------------------------------- VARIABLES BUTTONS - SELECT IMAGE --------------------------------------------
        self.sc_var1_select_img_btn = Button(self.sc_frame, text="Datei wählen", command=lambda: SingleChoice.sc_open_image(self, self.sc_var1_img_label_entry, self.sc_var1_img_data))
        self.sc_var2_select_img_btn = Button(self.sc_frame, text="Datei wählen", command=lambda: SingleChoice.sc_open_image(self, self.sc_var2_img_label_entry, self.sc_var2_img_data))
        self.sc_var3_select_img_btn = Button(self.sc_frame, text="Datei wählen", command=lambda: SingleChoice.sc_open_image(self, self.sc_var3_img_label_entry, self.sc_var3_img_data))
        self.sc_var4_select_img_btn = Button(self.sc_frame, text="Datei wählen", command=lambda: SingleChoice.sc_open_image(self, self.sc_var4_img_label_entry, self.sc_var4_img_data))
        self.sc_var5_select_img_btn = Button(self.sc_frame, text="Datei wählen", command=lambda: SingleChoice.sc_open_image(self, self.sc_var5_img_label_entry, self.sc_var5_img_data))
        self.sc_var6_select_img_btn = Button(self.sc_frame, text="Datei wählen", command=lambda: SingleChoice.sc_open_image(self, self.sc_var6_img_label_entry, self.sc_var6_img_data))
        self.sc_var7_select_img_btn = Button(self.sc_frame, text="Datei wählen", command=lambda: SingleChoice.sc_open_image(self, self.sc_var7_img_label_entry, self.sc_var7_img_data))


###################### "SingleChoice-Datenbank" - FRAME   -------- LABELS / ENTRYS / BUTTONS  ###################
        
        ### LABELS
        self.sc_delete_all_label = Label(self.sc_frame_database, text="Alle DB Einträge löschen?")
        self.sc_delete_all_label.grid(row=4, column=0, pady=5, padx=5)
        
        
        
        ### ENTRIES
        self.sc_delete_box = Entry(self.sc_frame_database, width=10)
        self.sc_delete_box.grid(row=3, column=1, sticky=W)
        
        
        ### BUTTONS
        self.sc_database_save_id_to_db_singlechoice_btn = Button(self.sc_frame_database, text="Speichern unter neuer ID", command=lambda: SingleChoice.sc_save_id_to_db(self))
        self.sc_database_save_id_to_db_singlechoice_btn.grid(row=0, column=0, sticky=W, pady=5)

        self.sc_database_save_id_to_db_singlechoice_btn = Button(self.sc_frame_database, text="SC - Datenbank anzeigen", command=lambda: test_generator_modul_datenbanken_anzeigen.MainGUI.__init__(self, app, "ilias_singlechoice_db", "singlechoice_table"))
        self.sc_database_save_id_to_db_singlechoice_btn.grid(row=1, column=0, sticky=W, pady=5)

        self.sc_excel_import_to_db_singlechoice_btn = Button(self.sc_frame_database, text="Excel-Datei importieren (SC)", command=lambda: SingleChoice.sc_excel_import_to_db(self))
        self.sc_excel_import_to_db_singlechoice_btn.grid(row=2, column=0, sticky=W, pady=5)
        
        self.sc_database_delete_id_from_db_btn = Button(self.sc_frame_database, text="ID Löschen", command=lambda: SingleChoice.sc_delete_id_from_db(self))
        self.sc_database_delete_id_from_db_btn.grid(row=3, column=0, sticky=W, pady=5)
        
        
        ### CHECKBOXES
        self.sc_var_delete_all = IntVar()
        self.sc_check_delete_all = Checkbutton(self.sc_frame_database, text="", variable=self.sc_var_delete_all, onvalue=1, offvalue=0)
        self.sc_check_delete_all.deselect()
        self.sc_check_delete_all.grid(row=4, column=1, sticky=W)



# ------------------------------- VARIABLES  - TEXT & ENTRY --------------------------------------------

        self.sc_var1_img_label_entry = Entry(self.sc_frame, textvariable=self.sc_var1_img_label_text, width=30)
        self.sc_var2_img_label_entry = Entry(self.sc_frame, textvariable=self.sc_var2_img_label_text, width=30)
        self.sc_var3_img_label_entry = Entry(self.sc_frame, textvariable=self.sc_var3_img_label_text, width=30)
        self.sc_var4_img_label_entry = Entry(self.sc_frame, textvariable=self.sc_var4_img_label_text, width=30)
        self.sc_var5_img_label_entry = Entry(self.sc_frame, textvariable=self.sc_var5_img_label_text, width=30)
        self.sc_var6_img_label_entry = Entry(self.sc_frame, textvariable=self.sc_var6_img_label_text, width=30)
        self.sc_var7_img_label_entry = Entry(self.sc_frame, textvariable=self.sc_var7_img_label_text, width=30)

        self.sc_answer1_label = Label(self.sc_frame, text="Antwort-Text 1")
        self.sc_answer2_label = Label(self.sc_frame, text="Antwort-Text 2")
        self.sc_answer3_label = Label(self.sc_frame, text="Antwort-Text 3")
        self.sc_answer4_label = Label(self.sc_frame, text="Antwort-Text 4")
        self.sc_answer5_label = Label(self.sc_frame, text="Antwort-Text 5")
        self.sc_answer6_label = Label(self.sc_frame, text="Antwort-Text 6")
        self.sc_answer7_label = Label(self.sc_frame, text="Antwort-Text 7")

        self.sc_answer1_label.grid(row=10, column=0, sticky=W, padx=30)
        self.sc_var1_answer_entry.grid(row=10, column=1, sticky=W)
        self.sc_var1_img_label_entry.grid(row=10, column=1, sticky=E, padx=0)
        self.sc_var1_points_entry.grid(row=10, column=2, sticky=W, padx=20)
        self.sc_var1_select_img_btn.grid(row=10, column=1, sticky=E, padx=200)

        def sc_var2_show():
            self.sc_answer2_label.grid(row=11, column=0, sticky=W, padx=30)
            self.sc_var2_answer_entry.grid(row=11, column=1, sticky=W)
            self.sc_var2_img_label_entry.grid(row=11, column=1, sticky=E, padx=0)
            self.sc_var2_points_entry.grid(row=11, column=2)
            self.sc_var2_select_img_btn.grid(row=11, column=1, sticky=E, padx=200)

        def sc_var3_show():
            self.sc_answer3_label.grid(row=12, column=0, sticky=W, padx=30)
            self.sc_var3_answer_entry.grid(row=12, column=1, sticky=W)
            self.sc_var3_img_label_entry.grid(row=12, column=1, sticky=E, padx=0)
            self.sc_var3_points_entry.grid(row=12, column=2)
            self.sc_var3_select_img_btn.grid(row=12, column=1, sticky=E, padx=200)

        def sc_var4_show():
            self.sc_answer4_label.grid(row=13, column=0, sticky=W, padx=30)
            self.sc_var4_answer_entry.grid(row=13, column=1, sticky=W)
            self.sc_var4_img_label_entry.grid(row=13, column=1, sticky=E, padx=0)
            self.sc_var4_points_entry.grid(row=13, column=2)
            self.sc_var4_select_img_btn.grid(row=13, column=1, sticky=E, padx=200)

        def sc_var5_show():
            self.sc_answer5_label.grid(row=14, column=0, sticky=W, padx=30)
            self.sc_var5_answer_entry.grid(row=14, column=1, sticky=W)
            self.sc_var5_img_label_entry.grid(row=14, column=1, sticky=E, padx=0)
            self.sc_var5_points_entry.grid(row=14, column=2)
            self.sc_var5_select_img_btn.grid(row=14, column=1, sticky=E, padx=200)

        def sc_var6_show():
            self.sc_answer6_label.grid(row=15, column=0, sticky=W, padx=30)
            self.sc_var6_answer_entry.grid(row=15, column=1, sticky=W)
            self.sc_var6_img_label_entry.grid(row=15, column=1, sticky=E, padx=0)
            self.sc_var6_points_entry.grid(row=15, column=2)
            self.sc_var6_select_img_btn.grid(row=15, column=1, sticky=E, padx=200)

        def sc_var7_show():
            self.sc_answer7_label.grid(row=16, column=0, sticky=W, padx=30)
            self.sc_var7_answer_entry.grid(row=16, column=1, sticky=W)
            self.sc_var7_img_label_entry.grid(row=16, column=1, sticky=E, padx=0)
            self.sc_var7_points_entry.grid(row=16, column=2, sticky=W, padx=20)
            self.sc_var7_select_img_btn.grid(row=16, column=1, sticky=E, padx=200)

        def sc_var2_remove():
            self.sc_answer2_label.grid_remove()
            self.sc_var2_answer_entry.grid_remove()
            self.sc_var2_img_label_entry.grid_remove()
            self.sc_var2_points_entry.grid_remove()
            self.sc_var2_select_img_btn.grid_remove()

        def sc_var3_remove():
            self.sc_answer3_label.grid_remove()
            self.sc_var3_answer_entry.grid_remove()
            self.sc_var3_img_label_entry.grid_remove()
            self.sc_var3_points_entry.grid_remove()
            self.sc_var3_select_img_btn.grid_remove()

        def sc_var4_remove():
            self.sc_answer4_label.grid_remove()
            self.sc_var4_answer_entry.grid_remove()
            self.sc_var4_img_label_entry.grid_remove()
            self.sc_var4_points_entry.grid_remove()
            self.sc_var4_select_img_btn.grid_remove()

        def sc_var5_remove():
            self.sc_answer5_label.grid_remove()
            self.sc_var5_answer_entry.grid_remove()
            self.sc_var5_img_label_entry.grid_remove()
            self.sc_var5_points_entry.grid_remove()
            self.sc_var5_select_img_btn.grid_remove()

        def sc_var6_remove():
            self.sc_answer6_label.grid_remove()
            self.sc_var6_answer_entry.grid_remove()
            self.sc_var6_img_label_entry.grid_remove()
            self.sc_var6_points_entry.grid_remove()
            self.sc_var6_select_img_btn.grid_remove()

        def sc_var7_remove():
            self.sc_answer7_label.grid_remove()
            self.sc_var7_answer_entry.grid_remove()
            self.sc_var7_img_label_entry.grid_remove()
            self.sc_var7_points_entry.grid_remove()
            self.sc_var7_select_img_btn.grid_remove()

 ###################### "Fragen Attribute" - FRAME   -------- LABELS / ENTRYS / BUTTONS  ###################
        self.sc_question_difficulty_label = Label(self.sc_frame_question_attributes, text="Schwierigkeitsgrad der Frage")
        self.sc_question_difficulty_label.grid(row=0, column=0, pady=5, padx=5, sticky=W)

        self.sc_question_difficulty_entry = Entry(self.sc_frame_question_attributes, width=10)
        self.sc_question_difficulty_entry.grid(row=0, column=1, pady=5, padx=5, sticky=W)

        self.sc_question_category_label = Label(self.sc_frame_question_attributes, text="Fragenkategorie")
        self.sc_question_category_label.grid(row=1, column=0, pady=5, padx=5, sticky=W)

        self.sc_question_category_entry = Entry(self.sc_frame_question_attributes, width=15)
        self.sc_question_category_entry.grid(row=1, column=1, pady=5, padx=5, sticky=W)

        self.sc_question_type_label = Label(self.sc_frame_question_attributes, text="Fragen-Typ")
        self.sc_question_type_label.grid(row=2, column=0, pady=5, padx=5, sticky=W)

        self.sc_question_type_entry = Entry(self.sc_frame_question_attributes, width=15)
        self.sc_question_type_entry.grid(row=2, column=1, pady=5, padx=5, sticky=W)
        self.sc_question_type_entry.insert(0, "Singlechoice")

        """
        ###################### -------- LABELS / ENTRYS / BUTTONS for "Fragentext Funktionen" - FRAME ------- ############################
        self.sc_add_latex_term_btn = Button( self.sc_frame_question_description_functions, text="Text \"Latex\"", command=lambda: Ilias_Test_Generator.Formelfrage.text_latex(self))
        self.sc_add_latex_term_btn.grid(row=1, column=0, padx=10, sticky="W")

        self.sc_set_text_sub_btn = Button( self.sc_frame_question_description_functions, text="Text \"Tiefgestellt\"", command=lambda: Ilias_Test_Generator.Formelfrage.text_sub(self))
        self.sc_set_text_sub_btn .grid(row=2, column=0, padx=10, pady=(10, 0), sticky="W")

        self.sc_set_text_sup_btn = Button( self.sc_frame_question_description_functions, text="Text \"Hochgestellt\"", command=lambda: Ilias_Test_Generator.Formelfrage.text_sup(self))
        self.sc_set_text_sup_btn.grid(row=3, column=0, padx=10, sticky="W")

        self.sc_set_text_italic_btn = Button( self.sc_frame_question_description_functions, text="Text \"Kursiv\"",command=lambda: Ilias_Test_Generator.Formelfrage.text_italic(self))
        self.sc_set_text_italic_btn.grid(row=4, column=0, padx=10, sticky="W")
        """

        ######  VARIABLES
        self.sc_var1_img_data_encoded64_string = ""
        self.sc_var2_img_data_encoded64_string = ""
        self.sc_var3_img_data_encoded64_string = ""
        self.sc_var4_img_data_encoded64_string = ""
        self.sc_var5_img_data_encoded64_string = ""
        self.sc_var6_img_data_encoded64_string = ""
        self.sc_var7_img_data_encoded64_string = ""




 ###################### "SingleChoice-Test erstellen" - FRAME   -------- LABELS / ENTRYS / BUTTONS  ###################
        
        self.sc_test_title_label = Label(self.sc_frame_create_singlechoice_test, text="Test-Titel")
        self.sc_test_title_label.grid(row=0, column=0, sticky=W)
        
        self.sc_test_title_entry = Entry(self.sc_frame_create_singlechoice_test, width=30)
        self.sc_test_title_entry.grid(row=0, column=1, sticky=W, padx=30)
        
        
        self.sc_autor_label = Label(self.sc_frame_create_singlechoice_test, text="Autor")
        self.sc_autor_label.grid(row=1, column=0, sticky=W)

        self.sc_autor_entry = Entry(self.sc_frame_create_singlechoice_test, width=30)
        self.sc_autor_entry.grid(row=1, column=1, sticky=W, padx=30)
        
        
        
        self.create_singlechoice_test_btn = Button(self.sc_frame_create_singlechoice_test, text="Singlechoice-Test erstellen", command=lambda: Create_SingleChoice_Test.__init__(self))
        self.create_singlechoice_test_btn.grid(row=2, column=0, sticky=W)
        self.create_singlechoice_test_entry = Entry(self.sc_frame_create_singlechoice_test, width=15)
        self.create_singlechoice_test_entry.grid(row=2, column=1, sticky=W, padx=20)
 
        
            

    def sc_open_image(self, var_img_label_entry, var_img_data_encoded64_string):


        ### Dateipfad auswählen

        self.sc_picture_name = filedialog.askopenfilename(initialdir=pathlib.Path().absolute(), title="Select a File")
        #self.sc_picture_name = filename
        self.sc_sorted_picture_name = self.sc_picture_name
        self.sc_last_char_index = self.sc_sorted_picture_name.rfind("/")
        self.sc_foo = ([pos for pos, char in enumerate(self.sc_sorted_picture_name) if char == '/'])
        self.sc_foo_len = len(self.sc_foo)
        self.sc_picture_name_new = self.sc_sorted_picture_name[self.sc_foo[self.sc_foo_len - 1] + 1:-4]  # letzten char des bildnamens ist das dateiformat: Testbild.jpg
        self.sc_image_format_new = self.sc_picture_name[-4:]

        ### Bild-Namen entsprechendes Eingabefeld übertragen
        var_img_label_entry.insert(0, str(self.sc_picture_name_new) + str(self.sc_image_format_new))

        ### Bild-Daten in base64 speichern. Die XML Datei enthält die Bilder der Antworten in base64 encoded
        # "encoded64_string_raw enthält die Daten als String in der Form b'String'
        # Um die Daten in der richtigen Form zu erhalten (nur den String ohne b''), wird die Funktion .decode('utf-8') verwendet
        # Dieser String kann in der .xml Datei verwendet werden um im Ilias ein Bild zu erzeugen
        with open(self.sc_picture_name, "rb") as image_file:
            encoded64_string_raw = base64.b64encode(image_file.read())
            encoded64_string = encoded64_string_raw.decode('utf-8')
            var_img_data_encoded64_string = encoded64_string

        print(self.sc_picture_name)

    def sc_save_id_to_db(self):
        conn = sqlite3.connect('ilias_singlechoice_db.db')
        c = conn.cursor()

        # format of duration P0Y0M0DT0H30M0S
        self.sc_test_time = "P0Y0M0DT" + self.sc_proc_hours_box.get() + "H" + self.sc_proc_minutes_box.get() + "M" + self.sc_proc_seconds_box.get() + "S"

        # Insert into Table
        # Reihenfolge muss mit der Datenbank übereinstimmen
        c.execute(
            "INSERT INTO singlechoice_table VALUES ("
            ":question_difficulty, :question_category, :question_type, :question_title, :question_description_title, :question_description_main, "
            ":response_1_text,:response_2_text,:response_3_text,:response_4_text,:response_5_text,:response_6_text,:response_7_text,:response_8_text,:response_9_text,:response_10_text, "
            ":response_1_pts, :response_2_pts, :response_3_pts, :response_4_pts, :response_5_pts, :response_6_pts, :response_7_pts, :response_8_pts, :response_9_pts, :response_10_pts, "
            ":response_1_img_label, :response_2_img_label, :response_3_img_label, :response_4_img_label, :response_5_img_label, :response_6_img_label, :response_7_img_label, :response_8_img_label, :response_9_img_label, :response_10_img_label, "
            ":response_1_img_string_base64_encoded, :response_2_img_string_base64_encoded, :response_3_img_string_base64_encoded, :response_4_img_string_base64_encoded, :response_5_img_string_base64_encoded, "
            ":response_6_img_string_base64_encoded, :response_7_img_string_base64_encoded, :response_8_img_string_base64_encoded, :response_9_img_string_base64_encoded, :response_10_img_string_base64_encoded, "
            ":description_img_name,:description_img_data,:test_time, :var_number, :res_number, :question_pool_tag)",
            {
                'question_difficulty': self.sc_question_difficulty_entry.get(),
                'question_category': self.sc_question_category_entry.get(),
                'question_type': self.sc_question_type_entry.get(),

                'question_title': self.sc_question_title_entry.get(),
                'question_description_title': self.sc_question_description_entry.get(),

                # The first part, "1.0" means that the input should be read from line one, character zero (ie: the very first character).
                # END is an imported constant which is set to the string "end". The END part means to read until the end of the text box is reached.
                # The only issue with this is that it actually adds a newline to our input. "
                # "So, in order to fix it we should change END to end-1c(Thanks Bryan Oakley) The -1c deletes 1 character, while -2c would mean delete two characters, and so on."
                'question_description_main': self.sc_infobox.get("1.0", 'end-1c'),

                # Antwort-Text  in Datenbank-Fach: var_name
                'response_1_text': self.sc_var1_answer_text.get(),
                'response_1_pts': self.sc_var1_points_text.get(),
                'response_1_img_label': self.sc_var1_img_label_text.get(),
                'response_1_img_string_base64_encoded':  self.sc_var1_img_data_encoded64_string,

                'response_2_text': self.sc_var2_answer_text.get(),
                'response_2_pts': self.sc_var2_points_text.get(),
                'response_2_img_label': self.sc_var2_img_label_text.get(),
                'response_2_img_string_base64_encoded':  self.sc_var2_img_data_encoded64_string,

                'response_3_text': self.sc_var3_answer_text.get(),
                'response_3_pts': self.sc_var3_points_text.get(),
                'response_3_img_label': self.sc_var3_img_label_text.get(),
                'response_3_img_string_base64_encoded':  self.sc_var3_img_data_encoded64_string,

                'response_4_text': self.sc_var4_answer_text.get(),
                'response_4_pts': self.sc_var4_points_text.get(),
                'response_4_img_label': self.sc_var4_img_label_text.get(),
                'response_4_img_string_base64_encoded':  self.sc_var4_img_data_encoded64_string,

                'response_5_text': self.sc_var5_answer_text.get(),
                'response_5_pts': self.sc_var5_points_text.get(),
                'response_5_img_label': self.sc_var5_img_label_text.get(),
                'response_5_img_string_base64_encoded':  self.sc_var5_img_data_encoded64_string,

                'response_6_text': self.sc_var6_answer_text.get(),
                'response_6_pts': self.sc_var6_points_text.get(),
                'response_6_img_label': self.sc_var6_img_label_text.get(),
                'response_6_img_string_base64_encoded':  self.sc_var6_img_data_encoded64_string,

                'response_7_text': self.sc_var7_answer_text.get(),
                'response_7_pts': self.sc_var7_points_text.get(),
                'response_7_img_label': self.sc_var7_img_label_text.get(),
                'response_7_img_string_base64_encoded':  self.sc_var7_img_data_encoded64_string,

                'response_8_text': " ",
                'response_8_pts': " ",
                'response_8_img_label': " ",
                'response_8_img_string_base64_encoded': " ",

                'response_9_text': " ",
                'response_9_pts': " ",
                'response_9_img_label': " ",
                'response_9_img_string_base64_encoded': " ",

                'response_10_text': " ",
                'response_10_pts': " ",
                'response_10_img_label': " ",
                'response_10_img_string_base64_encoded': " ",

                'description_img_name': "",
                'description_img_data': "",

                'test_time': self.sc_test_time,

                'var_number': "",
                'res_number': "",
                'question_pool_tag': ""

            }
        )
        conn.commit()
        conn.close()

        print("Neuer Eintrag in die SingleChoice-Datenbank --> Fragentitel: " + str(self.sc_question_title_entry.get()))
    
    """
    def sc_load_id_from_db(self):
        conn = sqlite3.connect('ilias_singlechoice_db.db')
        c = conn.cursor()
        record_id = self.load_box.get()
        c.execute("SELECT * FROM singlechoice_table WHERE oid =" + record_id)
        records = c.fetchall()

        self.sc_question_difficulty_entry.delete(0, END)
        self.sc_question_category_entry.delete(0, END)
        self.sc_question_type_entry.delete(0, END)

        self.sc_question_title_entry.delete(0, END)
        self.sc_question_description_entry.delete(0, END)
        self.sc_formula_question_entry.delete('1.0', 'end-1c')

        self.res1_formula_entry.delete(0, END)
        self.res2_formula_entry.delete(0, END)
        self.res3_formula_entry.delete(0, END)
        self.res4_formula_entry.delete(0, END)
        self.res5_formula_entry.delete(0, END)
        self.res6_formula_entry.delete(0, END)
        self.res7_formula_entry.delete(0, END)
        self.res8_formula_entry.delete(0, END)
        self.res9_formula_entry.delete(0, END)
        self.res10_formula_entry.delete(0, END)

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

        self.var8_name_entry.delete(0, END)
        self.var8_min_entry.delete(0, END)
        self.var8_max_entry.delete(0, END)
        self.var8_prec_entry.delete(0, END)
        self.var8_divby_entry.delete(0, END)

        self.var9_name_entry.delete(0, END)
        self.var9_min_entry.delete(0, END)
        self.var9_max_entry.delete(0, END)
        self.var9_prec_entry.delete(0, END)
        self.var9_divby_entry.delete(0, END)

        self.var10_name_entry.delete(0, END)
        self.var10_min_entry.delete(0, END)
        self.var10_max_entry.delete(0, END)
        self.var10_prec_entry.delete(0, END)
        self.var10_divby_entry.delete(0, END)

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

        self.res4_name_entry.delete(0, END)
        self.res4_min_entry.delete(0, END)
        self.res4_max_entry.delete(0, END)
        self.res4_prec_entry.delete(0, END)
        self.res4_tol_entry.delete(0, END)
        self.res4_points_entry.delete(0, END)

        self.res5_name_entry.delete(0, END)
        self.res5_min_entry.delete(0, END)
        self.res5_max_entry.delete(0, END)
        self.res5_prec_entry.delete(0, END)
        self.res5_tol_entry.delete(0, END)
        self.res5_points_entry.delete(0, END)

        self.res6_name_entry.delete(0, END)
        self.res6_min_entry.delete(0, END)
        self.res6_max_entry.delete(0, END)
        self.res6_prec_entry.delete(0, END)
        self.res6_tol_entry.delete(0, END)
        self.res6_points_entry.delete(0, END)

        self.res7_name_entry.delete(0, END)
        self.res7_min_entry.delete(0, END)
        self.res7_max_entry.delete(0, END)
        self.res7_prec_entry.delete(0, END)
        self.res7_tol_entry.delete(0, END)
        self.res7_points_entry.delete(0, END)

        self.res8_name_entry.delete(0, END)
        self.res8_min_entry.delete(0, END)
        self.res8_max_entry.delete(0, END)
        self.res8_prec_entry.delete(0, END)
        self.res8_tol_entry.delete(0, END)
        self.res8_points_entry.delete(0, END)

        self.res9_name_entry.delete(0, END)
        self.res9_min_entry.delete(0, END)
        self.res9_max_entry.delete(0, END)
        self.res9_prec_entry.delete(0, END)
        self.res9_tol_entry.delete(0, END)
        self.res9_points_entry.delete(0, END)

        self.res10_name_entry.delete(0, END)
        self.res10_min_entry.delete(0, END)
        self.res10_max_entry.delete(0, END)
        self.res10_prec_entry.delete(0, END)
        self.res10_tol_entry.delete(0, END)
        self.res10_points_entry.delete(0, END)


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
            self.res4_formula_entry.insert(END, record[9])
            self.res5_formula_entry.insert(END, record[10])
            self.res6_formula_entry.insert(END, record[11])
            self.res7_formula_entry.insert(END, record[12])
            self.res8_formula_entry.insert(END, record[13])
            self.res9_formula_entry.insert(END, record[14])
            self.res10_formula_entry.insert(END, record[15])

            self.var1_name_entry.insert(END, record[16])
            self.var1_min_entry.insert(END, record[17])
            self.var1_max_entry.insert(END, record[18])
            self.var1_prec_entry.insert(END, record[19])
            self.var1_divby_entry.insert(END, record[20])
            self.var1_unit_myCombo.set(record[21])

            self.var2_name_entry.insert(END, record[22])
            self.var2_min_entry.insert(END, record[23])
            self.var2_max_entry.insert(END, record[24])
            self.var2_prec_entry.insert(END, record[25])
            self.var2_divby_entry.insert(END, record[26])
            self.var2_unit_myCombo.set(record[27])

            self.var3_name_entry.insert(END, record[28])
            self.var3_min_entry.insert(END, record[29])
            self.var3_max_entry.insert(END, record[30])
            self.var3_prec_entry.insert(END, record[31])
            self.var3_divby_entry.insert(END, record[32])
            self.var3_unit_myCombo.set(record[33])

            self.var4_name_entry.insert(END, record[34])
            self.var4_min_entry.insert(END, record[35])
            self.var4_max_entry.insert(END, record[36])
            self.var4_prec_entry.insert(END, record[37])
            self.var4_divby_entry.insert(END, record[38])
            self.var4_unit_myCombo.set(record[39])

            self.var5_name_entry.insert(END, record[40])
            self.var5_min_entry.insert(END, record[41])
            self.var5_max_entry.insert(END, record[42])
            self.var5_prec_entry.insert(END, record[43])
            self.var5_divby_entry.insert(END, record[44])
            self.var5_unit_myCombo.set(record[45])

            self.var6_name_entry.insert(END, record[46])
            self.var6_min_entry.insert(END, record[47])
            self.var6_max_entry.insert(END, record[48])
            self.var6_prec_entry.insert(END, record[49])
            self.var6_divby_entry.insert(END, record[50])
            self.var6_unit_myCombo.set(record[51])

            self.var7_name_entry.insert(END, record[52])
            self.var7_min_entry.insert(END, record[53])
            self.var7_max_entry.insert(END, record[54])
            self.var7_prec_entry.insert(END, record[55])
            self.var7_divby_entry.insert(END, record[56])
            self.var7_unit_myCombo.set(record[57])

            self.var8_name_entry.insert(END, record[58])
            self.var8_min_entry.insert(END, record[59])
            self.var8_max_entry.insert(END, record[60])
            self.var8_prec_entry.insert(END, record[61])
            self.var8_divby_entry.insert(END, record[62])
            #self.var8_unit_myCombo.set(record[63])

            self.var9_name_entry.insert(END, record[64])
            self.var9_min_entry.insert(END, record[65])
            self.var9_max_entry.insert(END, record[66])
            self.var9_prec_entry.insert(END, record[67])
            self.var9_divby_entry.insert(END, record[68])
            #self.var9_unit_myCombo.set(record[69])

            self.var10_name_entry.insert(END, record[70])
            self.var10_min_entry.insert(END, record[71])
            self.var10_max_entry.insert(END, record[72])
            self.var10_prec_entry.insert(END, record[73])
            self.var10_divby_entry.insert(END, record[74])
            #self.var10_unit_myCombo.set(record[75])

            self.res1_name_entry.insert(END, record[76])
            self.res1_min_entry.insert(END, record[77])
            self.res1_max_entry.insert(END, record[78])
            self.res1_prec_entry.insert(END, record[79])
            self.res1_tol_entry.insert(END, record[80])
            self.res1_points_entry.insert(END, record[81])
            self.res1_unit_myCombo.set(record[82])

            self.res2_name_entry.insert(END, record[83])
            self.res2_min_entry.insert(END, record[84])
            self.res2_max_entry.insert(END, record[85])
            self.res2_prec_entry.insert(END, record[86])
            self.res2_tol_entry.insert(END, record[87])
            self.res2_points_entry.insert(END, record[88])
            self.res2_unit_myCombo.set(record[89])

            self.res3_name_entry.insert(END, record[90])
            self.res3_min_entry.insert(END, record[91])
            self.res3_max_entry.insert(END, record[92])
            self.res3_prec_entry.insert(END, record[93])
            self.res3_tol_entry.insert(END, record[94])
            self.res3_points_entry.insert(END, record[95])
            self.res3_unit_myCombo.set(record[96])

            self.res4_name_entry.insert(END, record[97])
            self.res4_min_entry.insert(END, record[98])
            self.res4_max_entry.insert(END, record[99])
            self.res4_prec_entry.insert(END, record[100])
            self.res4_tol_entry.insert(END, record[101])
            self.res4_points_entry.insert(END, record[102])
            #self.res4_unit_myCombo.set(record[103])

            self.res5_name_entry.insert(END, record[104])
            self.res5_min_entry.insert(END, record[105])
            self.res5_max_entry.insert(END, record[106])
            self.res5_prec_entry.insert(END, record[107])
            self.res5_tol_entry.insert(END, record[108])
            self.res5_points_entry.insert(END, record[109])
            #self.res5_unit_myCombo.set(record[110])

            self.res6_name_entry.insert(END, record[111])
            self.res6_min_entry.insert(END, record[112])
            self.res6_max_entry.insert(END, record[113])
            self.res6_prec_entry.insert(END, record[114])
            self.res6_tol_entry.insert(END, record[115])
            self.res6_points_entry.insert(END, record[116])
            #self.res6_unit_myCombo.set(record[117])

            self.res7_name_entry.insert(END, record[118])
            self.res7_min_entry.insert(END, record[119])
            self.res7_max_entry.insert(END, record[120])
            self.res7_prec_entry.insert(END, record[121])
            self.res7_tol_entry.insert(END, record[122])
            self.res7_points_entry.insert(END, record[123])
            #self.res7_unit_myCombo.set(record[124])

            self.res8_name_entry.insert(END, record[125])
            self.res8_min_entry.insert(END, record[126])
            self.res8_max_entry.insert(END, record[127])
            self.res8_prec_entry.insert(END, record[128])
            self.res8_tol_entry.insert(END, record[129])
            self.res8_points_entry.insert(END, record[130])
            #self.res8_unit_myCombo.set(record[131])

            self.res9_name_entry.insert(END, record[132])
            self.res9_min_entry.insert(END, record[133])
            self.res9_max_entry.insert(END, record[134])
            self.res9_prec_entry.insert(END, record[135])
            self.res9_tol_entry.insert(END, record[136])
            self.res9_points_entry.insert(END, record[137])
            #self.res9_unit_myCombo.set(record[138])

            self.res10_name_entry.insert(END, record[139])
            self.res10_min_entry.insert(END, record[140])
            self.res10_max_entry.insert(END, record[141])
            self.res10_prec_entry.insert(END, record[142])
            self.res10_tol_entry.insert(END, record[143])
            self.res10_points_entry.insert(END, record[144])
            #self.res10_unit_myCombo.set(record[145])

            # self.img_name.insert(END, record[146])
            # self.img_data.insert(END, record[147])

            self.test_time_from_db = record[148]
            self.var_number = record[149]
            self.myCombo.set(record[149])
            self.res_number = record[150]
            self.myCombo_res.set(record[150])

        conn.commit()
        conn.close()

        Formelfrage.selected_var_from_db(self, self.myCombo.get())
        Formelfrage.selected_res_from_db(self, self.myCombo_res.get())
    
    #def sc_delete_id_from_db(self):
    #def sc_edit_id(self):
    """

    def sc_excel_import_to_db(self):
        self.sc_xlsx_path = filedialog.askopenfilename(initialdir=pathlib.Path().absolute(), title="Select a File")
        self.sc_xlsx_data = pd.read_excel(self.sc_xlsx_path)

        self.sc_xlsx_file_column_labels = []
        self.sc_sql_values_question_marks = "("
        self.sc_sql_labels_param = ""


        # Dataframe erstellen
        self.sc_dataframe = pd.DataFrame(self.sc_xlsx_data)

        # Über die Excel Spalten iterieren
        for col in self.sc_dataframe.columns:
            self.sc_xlsx_file_column_labels.append(str(col))

        # Dataframe mit neuen Labels belegen
        self.sc_dataframe.columns = self.sc_xlsx_file_column_labels


        # Leere Einträge entfernen
        self.sc_dataframe = self.sc_dataframe.fillna("")

        


        for i in range(len(self.sc_xlsx_file_column_labels)-1):
            self.sc_sql_values_question_marks += "?,"
            
            if i == (len(self.sc_xlsx_file_column_labels)-2):
                self.sc_sql_values_question_marks += "?)"
                


        

        # Mit SingleChoice Datenbank verbinden
        conn = sqlite3.connect('ilias_singlechoice_db.db')
        c = conn.cursor()
        
        
        #c.execute("INSERT INTO table VALUES (?, ?, ?)", (var1, var2, var3))
        
        
        
        
        for row in self.sc_dataframe.itertuples():
            c.execute("INSERT INTO singlechoice_table VALUES " + self.sc_sql_values_question_marks, (
                   row.question_difficulty,
                   row.question_category,
                   row.question_type,
                   row.question_title,
                   row.question_description_title,
                   row.question_description_main,
                   row.response_1_text,
                   row.response_2_text,
                   row.response_3_text,
                   row.response_4_text,
                   row.response_5_text,
                   row.response_6_text,
                   row.response_7_text,
                   row.response_8_text,
                   row.response_9_text,
                   row.response_10_text,
                   row.response_1_pts,
                   row.response_2_pts,
                   row.response_3_pts,
                   row.response_4_pts,
                   row.response_5_pts,
                   row.response_6_pts,
                   row.response_7_pts,
                   row.response_8_pts,
                   row.response_9_pts,
                   row.response_10_pts,
                   row.response_1_img_label,
                   row.response_2_img_label,
                   row.response_3_img_label,
                   row.response_4_img_label,
                   row.response_5_img_label,
                   row.response_6_img_label,
                   row.response_7_img_label,
                   row.response_8_img_label,
                   row.response_9_img_label,
                   row.response_10_img_label,
                   row.response_1_img_string_base64_encoded,
                   row.response_2_img_string_base64_encoded,
                   row.response_3_img_string_base64_encoded,
                   row.response_4_img_string_base64_encoded,
                   row.response_5_img_string_base64_encoded,
                   row.response_6_img_string_base64_encoded,
                   row.response_7_img_string_base64_encoded,
                   row.response_8_img_string_base64_encoded,
                   row.response_9_img_string_base64_encoded,
                   row.response_10_img_string_base64_encoded,
                   row.description_img_name,
                   row.description_img_data,
                   row.test_time,
                   row.var_number,
                   row.res_number,
                   row.question_pool_tag
                 ))
    
        
      
        conn.commit()
        conn.close()
        
        print("Load File: \"" + self.sc_xlsx_path + "\" in singlechoice_table...done!")
       
        
    def sc_delete_id_from_db(self):
        
        # Variablen
        self.sc_delete_list = []
        self.sc_delete_all_list = []
        
        
        
        # Zur Datenbank connecten
        conn = sqlite3.connect('ilias_singlechoice_db.db')
        c = conn.cursor()
        
        # Wenn in das EIngabefeld Kommagetrenne ID's eingetragen wurden, dann ->
        # den String nehmen, nach Komma trennen "," und einzelne DB-ID's löschen
        self.sc_delete_list = self.sc_delete_box.get().split(",")
       
        
        # Wenn in das Eingabefeld z.B. "1-5" eingetragen wurde, dann ->
        # den String nehmen, und nach Bindestrick "-" splitten
        # ID in Fach 1 = Start, ID in Fach [-1] (letztes Fach)
         
        self.sc_delete_mult = self.sc_delete_box.get()
        self.sc_delete_mult_start = self.sc_delete_mult.split('-')[0]
        self.sc_delete_mult_end = self.sc_delete_mult.split('-')[-1]
        self.sc_delete_mult_symbol = "-" in self.sc_delete_mult
        #print(self.sc_delete_mult_start)
        #print(self.sc_delete_mult_end)
        #print(self.sc_delete_mult_symbol)

        if self.sc_var_delete_all.get() == 1:
            now = datetime.now()  # current date and time
            date_time = now.strftime("%d.%m.%Y_%Hh-%Mm")
            actual_time = str(date_time)
            #Database.sql_db_to_excel_export(self, "BACKUP_Export_from_SQL__" + str(actual_time) + ".xlsx")
            c.execute("SELECT *, oid FROM singlechoice_table")
            records = c.fetchall()
            for record in records:
                self.sc_delete_all_list.append(int(record[len(record) - 1]))
                
                # Das Erste Feld enthält Variablen Namen
            
            self.sc_delete_all_list.pop(0)
            

            for x in range(len(self.sc_delete_all_list)):
                c.execute("DELETE from singlechoice_table WHERE oid= " + str(self.sc_delete_all_list[x]))
            print("All Entries removed!")


        elif self.sc_delete_mult_symbol == True:

            for x in range(int(self.sc_delete_mult_start), int(self.sc_delete_mult_end)+1):
                c.execute("DELETE from singlechoice_table WHERE oid= " + str(x))
                print("Entry with ID " + str(x) + " removed!")


        else:
            for x in range(len(self.sc_delete_list)):
                c.execute("DELETE from singlechoice_table WHERE oid= " + str(self.sc_delete_list[x]))
                print("Entry with ID " + str(self.sc_delete_list[x]) + " removed!")

        self.sc_delete_box.delete(0, END)

        conn.commit()
        conn.close()
        
class Create_SingleChoice_Test:
    def __init__(self):
       
        """
        Ein ILIAS-Test besteht immer aus den beiden Dateien "*_qti_*.xml" und "*_tst_*.xml".
        Die "tst" beinhaltelt eine Auflistung der Fragen und den Test-Titel, sowie die Test-id
        Die "qti" beinhaltet die Test-Einstellungen und die eigentliche Beschreibung der einzelnen Fragen
        Dazu gehört die Fragenbeschreibung, Lösungen, Punkte, Bilder etc.
        
        _________________________________________________________________
       
        Beispiel für einen Test, bestehend aus 3 Fragen für die _tst_:
        ...
        ...
        Test-Titel: <Title Language="de">SingleChoice</Title>
        ...
        ...
        Test-ID: <Identifier Catalog="ILIAS" Entry="il_0_tst_2040314"/>
        ...
        ...
        Auflistung der Fragen:
            <Question QRef="il_0_qst_457015"/>
            <Question QRef="il_0_qst_526726"/>
            <Question QRef="il_0_qst_457016"/>
            ...
            ...
            <TriggerQuestion Id="457015"/>
            <TriggerQuestion Id="526726"/>
		    <TriggerQuestion Id="457016"/>
        __________________________________________________________________
        
        Beispiel für einen Test, bestehend aus 3 Fragen für die _qti_:
        ...
        ...
        <assessment ident="il_0_tst_8869" title="SingleChoice">
        ...
        // diverse Test-Einstellungen //
        ...
        <item ident="il_0_qst_457015" title="Arbeitspunkt" maxattempts="0">                         -- Erste Frage
        // Fragenbeschreibung, Lösungen, Punktevergabe                                              -- Eigentliche Darstellung der Frage
        ...
        ...
        <item ident="il_0_qst_526726" title="SingleChoice Test" maxattempts="0">                    -- Zweite Frage
        // Fragenbeschreibung, Lösungen, Punktevergabe                                              -- Eigentliche Darstellung der Frage
        ...
        ...
        <item ident="il_0_qst_457016" title="Eigenschaften der Asynchronmaschine" maxattempts="0">  -- Dritte Frage
        // Fragenbeschreibung, Lösungen, Punktevergabe                                              -- Eigentliche Darstellung der Frage
        ...
        
        """
        
        ##### VARIABLES
        self.sc_test_entry_splitted = []
        
        self.sc_db_find_entries = []
        self.sc_db_find_indexes = []
        
        
        #### Auslesen der SingleChoice-Datenbank einträgen

        # Create a database or connect to one
        connect = sqlite3.connect('ilias_singlechoice_db.db')

        # Create cursor
        cursor = connect.cursor()

        ### Nur das erste Fach auslesen um einen Zusammenhang zwischen Variablen und Indexen herzustellen
        cursor.execute("SELECT * FROM singlechoice_table LIMIT 1")

        sc_db_records = cursor.fetchall()

        for sc_db_record in sc_db_records:
            for k in range(len(sc_db_record)):
                self.sc_db_find_entries.append(str(sc_db_record[k]))
                self.sc_db_find_indexes.append(int(k))

        # Dictionary aus zwei Listen erstellen
        self.sc_db_entry_to_index_dict = dict(zip((self.sc_db_find_entries), (self.sc_db_find_indexes)))



        #print("DICTIONARY")
        #pprint.pprint(self.sc_db_entry_to_index_dict)

        #for x in range(len(self.sc_db_find_entries)):
        #    print(self.sc_db_find_entries[x], self.sc_db_find_indexes[x])


        # Commit Changes
        #connect.commit()

        # Close Connection
        #connect.close()



        ##### Einlesen der "SingleChoice" _tst_.xml zum ändern des Test-Titel
        self.sc_mytree = ET.parse(self.singlechoice_test_tst_file_path_template)
        self.sc_myroot = self.sc_mytree.getroot()
        
        # Titel-Eintrag ändern (Voreinstellung in der Vorlage: Titel = sc_test_vorlage)
        for ContentObject in self.sc_myroot.iter('ContentObject'):
            for MetaData in ContentObject.iter('MetaData'):
                for General in MetaData.iter('General'):
                    for Title in General.iter('Title'):
                        Title.text = self.sc_ilias_test_title_entry.get()
                        print("Title - Text")
                        print(Title.text)
                        # .XML Datei kann keine "&" verarbeiten. 
                        # "&" muss gegen "&amp" ausgetauscht werden sonst kann Ilias die Datei hinterher nicht verwerten.
                        Title.text = Title.text.replace('&', "&amp;")
        
        print(self.sc_var1_answer_entry.get())
        print(self.sc_test_title_entry.get())
        print(self.sc_question_description_entry.get())
        
        
        
        # Sollte kein Namen vergeben werden, wird der Test-Titel auf "DEFAULT" gesetzt
        if Title.text == "sc_test_vorlage" or Title.text == "":
            Title.text = "DEFAULT"
        
        # Änderungen der .XML in eine neue Datei schreiben
        # Die Datei wird nach dem ILIAS-Import "Standard" benannt "1604407426__0__tst_2040314.xml"
        # Die Ziffernfolge der 10 Ziffern am Anfang sowie der 7 Ziffern zum Schluss können nach belieben variiert werden.
        self.sc_mytree.write(self.singlechoice_test_tst_file_path_output)
        
        
        print("TST FILE geschrieben!")
        print(self.singlechoice_test_tst_file_path_output)
        
        
        
        ##### Einlesen der "SingleChoice" _qti_.xml zum hinzufügen von Fragen
        self.sc_mytree = ET.parse(self.singlechoice_test_qti_file_path_template)
        self.sc_myroot = self.sc_mytree.getroot()


        self.sc_test_entry_splitted = self.create_singlechoice_test_entry.get()
        self.sc_test_entry_splitted = self.sc_test_entry_splitted.split(",")



        connect_sc_db = sqlite3.connect('ilias_singlechoice_db.db')
        cursor = connect_sc_db.cursor()


        # Sämtliche Datenbank Einträge auslesen mit der entsprechenden "oid" (Datenbank ID)
        # Datenbank ID wird automatisch bei einem neuen Eintrag erstellt (fortlaufend) und kann nicht beeinflusst werden
        cursor.execute("SELECT *, oid FROM singlechoice_table")
        sc_db_records = cursor.fetchall()

        for i in range(len(self.sc_test_entry_splitted)):
            for sc_db_record in sc_db_records:               
                if str(sc_db_record[len(sc_db_record) - 1]) == self.sc_test_entry_splitted[i]:
                    for t in range(len(sc_db_record)):
                        if sc_db_record[self.sc_db_entry_to_index_dict['question_type']].lower() == "singlechoice" or sc_db_record[self.sc_db_entry_to_index_dict['question_type']].lower() == "single choice":

                            self.sc_question_difficulty                     = sc_db_record[self.sc_db_entry_to_index_dict['question_difficulty']]
                            self.sc_question_category                       = sc_db_record[self.sc_db_entry_to_index_dict['question_category']]
                            self.sc_question_type                           = sc_db_record[self.sc_db_entry_to_index_dict['question_type']]
                            self.sc_question_title                          = sc_db_record[self.sc_db_entry_to_index_dict['question_title']]
                            self.sc_question_description_title              = sc_db_record[self.sc_db_entry_to_index_dict['question_description_title']]
                            self.sc_question_description_main               = sc_db_record[self.sc_db_entry_to_index_dict['question_description_main']]
                            self.sc_response_1_text                         = sc_db_record[self.sc_db_entry_to_index_dict['response_1_text']]
                            self.sc_response_2_text	                        = sc_db_record[self.sc_db_entry_to_index_dict['response_2_text']]
                            self.sc_response_3_text	                        = sc_db_record[self.sc_db_entry_to_index_dict['response_3_text']]
                            self.sc_response_4_text	                        = sc_db_record[self.sc_db_entry_to_index_dict['response_4_text']]
                            self.sc_response_5_text	                        = sc_db_record[self.sc_db_entry_to_index_dict['response_5_text']]
                            self.sc_response_6_text	                        = sc_db_record[self.sc_db_entry_to_index_dict['response_6_text']]
                            self.sc_response_7_text	                        = sc_db_record[self.sc_db_entry_to_index_dict['response_7_text']]
                            self.sc_response_8_text	                        = sc_db_record[self.sc_db_entry_to_index_dict['response_8_text']]
                            self.sc_response_9_text	                        = sc_db_record[self.sc_db_entry_to_index_dict['response_9_text']]
                            self.sc_response_10_text	                    = sc_db_record[self.sc_db_entry_to_index_dict['response_10_text']]
                            self.sc_response_1_pts	                        = sc_db_record[self.sc_db_entry_to_index_dict['response_1_pts']]
                            self.sc_response_2_pts	                        = sc_db_record[self.sc_db_entry_to_index_dict['response_2_pts']]
                            self.sc_response_3_pts	                        = sc_db_record[self.sc_db_entry_to_index_dict['response_3_pts']]
                            self.sc_response_4_pts	                        = sc_db_record[self.sc_db_entry_to_index_dict['response_4_pts']]
                            self.sc_response_5_pts	                        = sc_db_record[self.sc_db_entry_to_index_dict['response_5_pts']]
                            self.sc_response_6_pts	                        = sc_db_record[self.sc_db_entry_to_index_dict['response_6_pts']]
                            self.sc_response_7_pts	                        = sc_db_record[self.sc_db_entry_to_index_dict['response_7_pts']]
                            self.sc_response_8_pts	                        = sc_db_record[self.sc_db_entry_to_index_dict['response_8_pts']]
                            self.sc_response_9_pts	                        = sc_db_record[self.sc_db_entry_to_index_dict['response_9_pts']]
                            self.sc_response_10_pts	                        = sc_db_record[self.sc_db_entry_to_index_dict['response_10_pts']]
                            self.sc_response_1_img_label	                = sc_db_record[self.sc_db_entry_to_index_dict['response_1_img_label']]
                            self.sc_response_2_img_label	                = sc_db_record[self.sc_db_entry_to_index_dict['response_2_img_label']]
                            self.sc_response_3_img_label	                = sc_db_record[self.sc_db_entry_to_index_dict['response_3_img_label']]
                            self.sc_response_4_img_label	                = sc_db_record[self.sc_db_entry_to_index_dict['response_4_img_label']]
                            self.sc_response_5_img_label	                = sc_db_record[self.sc_db_entry_to_index_dict['response_5_img_label']]
                            self.sc_response_6_img_label	                = sc_db_record[self.sc_db_entry_to_index_dict['response_6_img_label']]
                            self.sc_response_7_img_label	                = sc_db_record[self.sc_db_entry_to_index_dict['response_7_img_label']]
                            self.sc_response_8_img_label	                = sc_db_record[self.sc_db_entry_to_index_dict['response_8_img_label']]
                            self.sc_response_9_img_label	                = sc_db_record[self.sc_db_entry_to_index_dict['response_9_img_label']]
                            self.sc_response_10_img_label	                = sc_db_record[self.sc_db_entry_to_index_dict['response_10_img_label']]
                            self.sc_response_1_img_string_base64_encoded	= sc_db_record[self.sc_db_entry_to_index_dict['response_1_img_string_base64_encoded']]
                            self.sc_response_2_img_string_base64_encoded	= sc_db_record[self.sc_db_entry_to_index_dict['response_2_img_string_base64_encoded']]
                            self.sc_response_3_img_string_base64_encoded	= sc_db_record[self.sc_db_entry_to_index_dict['response_3_img_string_base64_encoded']]
                            self.sc_response_4_img_string_base64_encoded	= sc_db_record[self.sc_db_entry_to_index_dict['response_4_img_string_base64_encoded']]
                            self.sc_response_5_img_string_base64_encoded	= sc_db_record[self.sc_db_entry_to_index_dict['response_5_img_string_base64_encoded']]
                            self.sc_response_6_img_string_base64_encoded	= sc_db_record[self.sc_db_entry_to_index_dict['response_6_img_string_base64_encoded']]
                            self.sc_response_7_img_string_base64_encoded	= sc_db_record[self.sc_db_entry_to_index_dict['response_7_img_string_base64_encoded']]
                            self.sc_response_8_img_string_base64_encoded	= sc_db_record[self.sc_db_entry_to_index_dict['response_8_img_string_base64_encoded']]
                            self.sc_response_9_img_string_base64_encoded 	= sc_db_record[self.sc_db_entry_to_index_dict['response_9_img_string_base64_encoded']]
                            self.sc_response_10_img_string_base64_encoded	= sc_db_record[self.sc_db_entry_to_index_dict['response_10_img_string_base64_encoded']]
                            self.sc_description_img_name	                = sc_db_record[self.sc_db_entry_to_index_dict['description_img_name']]
                            self.sc_description_img_data	                = sc_db_record[self.sc_db_entry_to_index_dict['description_img_data']]
                            self.sc_test_time	                            = sc_db_record[self.sc_db_entry_to_index_dict['test_time']]
                            self.sc_var_number	                            = sc_db_record[self.sc_db_entry_to_index_dict['var_number']]
                            self.sc_res_number	                            = sc_db_record[self.sc_db_entry_to_index_dict['res_number']]
                            self.sc_question_pool_tag                       = sc_db_record[self.sc_db_entry_to_index_dict['question_pool_tag']]
                            
                            
            Create_SingleChoice_Test.sc_create_question(self, i)
                            
    def sc_create_question(self, id_nr):
        """Diese Funktion wandelt die SQL-Einträge in die .xml um, welche anschließend in ILIAS eingespielt werden kann"""
        

        # VARIABLEN
        self.sc_response_counter = 0    #wird verwendet zu zählen, wieviele Anworten pro Frage verwendet werden. Bei einer neuer Antwort -> +1


        # Neuen Ordner erstellen um den Test darin abzulegen
        """ ... """
        
        
        # Verbindung zur SC-Datenank
        sc_connect = sqlite3.connect('ilias_singlechoice_db.db')
        sc_cursor = sc_connect.cursor()
        
        # Alle Einträge auslesen
        sc_cursor.execute("SELECT *, oid FROM singlechoice_table")
        sc_db_records = sc_cursor.fetchall()
        
        
        for sc_db_record in sc_db_records:
            
            if str(sc_db_record[len(sc_db_record)-1]) == self.sc_test_entry_splitted[id_nr]:
                
                # XML Struktur aus XML Datei festlegen. Muss nur einmal angelegt werden
                questestinterop = ET.Element('questestinterop')
                assessment = ET.SubElement(questestinterop, 'assessment')
                section = ET.SubElement(assessment, 'section')
               
                
                
                
                
                Create_SingleChoice_Test.sc_add_answer_to_xml(self, self.sc_response_1_text, section)  
                Create_SingleChoice_Test.sc_add_answer_to_xml(self, self.sc_response_2_text, section)
                Create_SingleChoice_Test.sc_add_answer_to_xml(self, self.sc_response_3_text, section)
                Create_SingleChoice_Test.sc_add_answer_to_xml(self, self.sc_response_4_text, section)
                Create_SingleChoice_Test.sc_add_answer_to_xml(self, self.sc_response_5_text, section)
  

        # Diese Funktion fügt die möglichen Antworten in die XML Struktur ein
        # response_sql -> Der Antwort Text aus der SQL-Datenbank (z.B. aus der Spalte "response_1_text)
        # response_label_xml -> Eintrag gibt die "ID" der Antwort wider. Beginnt bei "0" und wird mit jeder zusätzlichen Antowort inkrementiert
        def sc_add_answer_to_xml(self, response_sql, section):
                   
                    # Struktur für den SingleChoice - Fragen/Antworten Teil  -- HEADER
                    # Muss für jede Frage neu angelegt/hinzugefügt werden
                    item = ET.SubElement(section, 'item')
                    qticomment = ET.SubElement(item, 'qticomment')
                    duration = ET.SubElement(item, 'duration')
                    itemmetadata = ET.SubElement(item, 'itemmetadata')
                    presentation = ET.SubElement(item, 'presentation')
                    
                            
                    # Struktur für den SingleCHoice - Fragen/Antworten Teil  -- MAIN
                    # Muss für jede Frage neu angelegt/hinzugefügt werden
                    flow = ET.SubElement(presentation, 'flow')
                    question_description_material = ET.SubElement(flow, 'material')
                    question_description_mattext = ET.SubElement(question_description_material, 'mattext')
                    response_lid = ET.SubElement(flow, 'response_lid')
                    render_choice = ET.SubElement(response_lid, 'render_choice')
                    response_label = ET.SubElement(render_choice, 'response_label')
                    question_answer_material = ET.SubElement(response_label, 'material')
                    question_answer_mattext = ET.SubElement(question_answer_material, 'mattext')
                
                
                    qtimetadata = ET.SubElement(itemmetadata, 'qtimetadata')
                    qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                    
                    
                    
                    ### ------------------------------------------------------- XML Einträge mit Werten füllen
                    
                    # Fragen-Titel -- "item title" in xml
                    item.set('title', self.sc_question_title.replace('&', "&amp;"))
                    
                    # Fragen-Titel Beschreibung
                    qticomment.text = self.sc_question_description_title
                    
                    # Testdauer -- "duration" in xml
                    # wird keine Testzeit eingetragen, wird 1h vorausgewählt
                    duration.text = self.sc_test_time
                    if duration.text == "":
                        duration.text = "P0Y0M0DT1H0M0S"
                        
                    
                    
                    
                    """ Prüfen ob ILIAS Version ausgelesen werden kann"""
                    # -----------------------------------------------------------------------ILIAS VERSION
                    qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                    fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                    fieldlabel.text = "ILIAS_VERSION"
                    fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
                    fieldentry.text = "5.4.14 2020-07-31"
                    # -----------------------------------------------------------------------QUESTIONTYPE
                    qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                    fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                    fieldlabel.text = "QUESTIONTYPE"
                    fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
                    fieldentry.text = "SINGLE CHOICE QUESTION"
                    # -----------------------------------------------------------------------AUTHOR
                    qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                    fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                    fieldlabel.text = "AUTHOR"
                    fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
                    self.sc_autor_replaced = str(self.sc_autor_entry.get())
                    fieldentry.text = self.sc_autor_replaced.replace('&', "&amp;")
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
                    fieldentry.text = "5f11d3ed9af3e5.53678796"
                    # -----------------------------------------------------------------------THUMB_SIZE
                    qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                    fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                    fieldlabel.text = "thumb_size"
                    fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
                    fieldentry.text = ""
                    # -----------------------------------------------------------------------FEEDBACK_SETTING
                    qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                    fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                    fieldlabel.text = "feedback_setting"
                    fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
                    fieldentry.text = "2"
                    # -----------------------------------------------------------------------SINGLELINE
                    qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                    fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                    fieldlabel.text = "singleline"
                    fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
                    fieldentry.text = "1"
                    
                    
                    # Fragentitel einsetzen -- "presentation label" in xml
                    presentation.set('label', self.sc_question_title)
                    
                    
                    
                    
                    #Fragen-Text -- "mattext_texttype" in xml -- Gibt das Format des Textes an
                    question_description_mattext.set('texttype', "text/html")
                    
    
                
                    #Fragen-Text -- "mattext_texttype" in xml -- Gibt die eigentliche Fragen-Beschreibung an
                    question_description_mattext.text = "<p>" + "TEST - Was kommt in der Natur vor?" + "</p>"
                
                
                    # -----------------------------------------------------------------------AUFLISTUNG DER ANTWORTEN (SINGLECHOICE)
                    
                    
                    ###### Auslesen der Anzahl der Antworten
                    if isinstance(self.sc_response_1_text, str) == True:
                        self.sc_response_counter = self.sc_response_counter + 1
                    elif isinstance(self.sc_response_2_text, str) == True:
                        self.sc_response_counter = self.sc_response_counter + 1
                    elif isinstance(self.sc_response_3_text, str) == True:
                        self.sc_response_counter = self.sc_response_counter + 1
                    elif isinstance(self.sc_response_4_text, str) == True:
                        self.sc_response_counter = self.sc_response_counter + 1
                    elif isinstance(self.sc_response_5_text, str) == True:
                        self.sc_response_counter = self.sc_response_counter + 1
                    elif isinstance(self.sc_response_6_text, str) == True:
                        self.sc_response_counter = self.sc_response_counter + 1
                    elif isinstance(self.sc_response_7_text, str) == True:
                        self.sc_response_counter = self.sc_response_counter + 1
                    elif isinstance(self.sc_response_8_text, str) == True:
                        self.sc_response_counter = self.sc_response_counter + 1
                    elif isinstance(self.sc_response_9_text, str) == True:
                        self.sc_response_counter = self.sc_response_counter + 1
                    elif isinstance(self.sc_response_1_text, str) == True:
                        self.sc_response_counter = self.sc_response_counter + 1
                    
                    
                    
                    
                    # "MCSR --> Singlechoice Identifier für xml datei
                    response_lid.set('ident', "MCSR")
                    response_lid.set('rcardinality', "Single")
                    render_choice.set('shuffle', "Yes")
                    
                    
                    for nr in range(self.sc_response_counter):
                        #response_lid = ET.SubElement(flow, 'response_lid')
                        #render_choice = ET.SubElement(response_lid, 'render_choice')
                        response_label = ET.SubElement(render_choice, 'response_label')
                        question_answer_material = ET.SubElement(response_label, 'material')
                        question_answer_mattext = ET.SubElement(question_answer_material, 'mattext')
            
                        if response_sql != "":
                            response_label.set('ident', str(nr+1))
                            question_answer_mattext.set('texttype', "text/plain")
                            question_answer_mattext.text = response_sql

            
            

                    # Neues "Item" an xml anhängen
                    self.sc_myroot[0][len(self.sc_myroot[0])-1].append(item)

            #sc_create_question.(self, self.sc_response_1_text)


                
                    
                
                
            # -----------------------------------------------------------------------ANTWORT 1

            """  
            # Create_SingleChoice_Test.sc_add_answer_to_xml(self, presentation, question_description_mattext, response_lid, render_choice,  self.sc_response_1_text, response_label,  self.sc_response_counter, flow)
            # Create_SingleChoice_Test.sc_add_answer_to_xml(self, presentation, question_description_mattext, response_lid, render_choice,  self.sc_response_2_text, response_label,  self.sc_response_counter, flow)
            # Create_SingleChoice_Test.sc_add_answer_to_xml(self, presentation, question_description_mattext, response_lid, render_choice,  self.sc_response_3_text, response_label,  self.sc_response_counter, flow)
            # Create_SingleChoice_Test.sc_add_answer_to_xml(self, presentation, question_description_mattext, response_lid, render_choice,  self.sc_response_4_text, response_label,  self.sc_response_counter, flow)
            # Create_SingleChoice_Test.sc_add_answer_to_xml(self, presentation, question_description_mattext, response_lid, render_choice,  self.sc_response_5_text, response_label,  self.sc_response_counter, flow)
             
             

             #response_lid = ET.SubElement(flow, 'response_lid')
             #render_choice = ET.SubElement(response_lid, 'render_choice')
             #response_label = ET.SubElement(render_choice, 'response_label')
             #question_answer_material = ET.SubElement(response_label, 'material')
             #question_answer_mattext = ET.SubElement(question_answer_material, 'mattext')
             #Create_SingleChoice_Test.sc_add_answer_to_xml(self, self.sc_response_1_text, response_label, question_answer_mattext, self.sc_response_counter)
             if self.sc_response_1_text != "":
                 response_label.set('ident', str(self.sc_response_counter))
                 question_answer_mattext.set('texttype', "text/plain")
                 question_answer_mattext.text = self.sc_response_1_text
                 self.sc_response_counter = self.sc_response_counter + 1
             # -----------------------------------------------------------------------ANTWORT 2
             #response_lid = ET.SubElement(flow, 'response_lid')
             #render_choice = ET.SubElement(response_lid, 'render_choice')
             response_label = ET.SubElement(render_choice, 'response_label')
             question_answer_material = ET.SubElement(response_label, 'material')
             question_answer_mattext = ET.SubElement(question_answer_material, 'mattext')
             # Create_SingleChoice_Test.sc_add_answer_to_xml(self, self.sc_response_1_text, response_label, question_answer_mattext, self.sc_response_counter)
             if self.sc_response_2_text != "":
                 response_label.set('ident', str(self.sc_response_counter))
                 question_answer_mattext.set('texttype', "text/plain")
                 question_answer_mattext.text = self.sc_response_2_text
                 self.sc_response_counter = self.sc_response_counter + 1
             # -----------------------------------------------------------------------ANTWORT 3
             #response_lid = ET.SubElement(flow, 'response_lid')
             #render_choice = ET.SubElement(response_lid, 'render_choice')
             response_label = ET.SubElement(render_choice, 'response_label')
             question_answer_material = ET.SubElement(response_label, 'material')
             question_answer_mattext = ET.SubElement(question_answer_material, 'mattext')
             # Create_SingleChoice_Test.sc_add_answer_to_xml(self, self.sc_response_1_text, response_label, question_answer_mattext, self.sc_response_counter)
             if self.sc_response_3_text != "":
                 response_label.set('ident', str(self.sc_response_counter))
                 question_answer_mattext.set('texttype', "text/plain")
                 question_answer_mattext.text = self.sc_response_3_text
                 self.sc_response_counter = self.sc_response_counter + 1
             # -----------------------------------------------------------------------ANTWORT 4
             #response_lid = ET.SubElement(flow, 'response_lid')
             #render_choice = ET.SubElement(response_lid, 'render_choice')
             response_label = ET.SubElement(render_choice, 'response_label')
             question_answer_material = ET.SubElement(response_label, 'material')
             question_answer_mattext = ET.SubElement(question_answer_material, 'mattext')
             # Create_SingleChoice_Test.sc_add_answer_to_xml(self, self.sc_response_1_text, response_label, question_answer_mattext, self.sc_response_counter)
             if self.sc_response_4_text != "":
                 response_label.set('ident', str(self.sc_response_counter))
                 question_answer_mattext.set('texttype', "text/plain")
                 question_answer_mattext.text = self.sc_response_4_text
                 self.sc_response_counter = self.sc_response_counter + 1
             
             # -----------------------------------------------------------------------ANTWORT 4
             #response_lid = ET.SubElement(flow, 'response_lid')
             #render_choice = ET.SubElement(response_lid, 'render_choice')
             response_label = ET.SubElement(render_choice, 'response_label')
             question_answer_material = ET.SubElement(response_label, 'material')
             question_answer_mattext = ET.SubElement(question_answer_material, 'mattext')
             # Create_SingleChoice_Test.sc_add_answer_to_xml(self, self.sc_response_1_text, response_label, question_answer_mattext, self.sc_response_counter)
             if self.sc_response_4_text != "":
                 response_label.set('ident', str(self.sc_response_counter))
                 question_answer_mattext.set('texttype', "text/plain")
                 question_answer_mattext.text = self.sc_response_4_text
                 self.sc_response_counter = self.sc_response_counter + 1
             """




            self.sc_mytree.write(self.singlechoice_test_qti_file_path_output)
            print("SingleChoice Frage erstellt!")
                
                

       




                

                
                
        sc_connect.commit()
        sc_connect.close()     
                   