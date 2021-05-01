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
from PIL import ImageTk, Image          # Zur Preview von ausgewählten Bildern
import xlsxwriter                       # import/export von excel Dateien
import shutil                           # Wird verwendet um Verzeichnisse zu kopieren


### Eigene Dateien / Module
from Test_Generator_Module import test_generator_modul_datenbanken_anzeigen
from Test_Generator_Module import test_generator_modul_datenbanken_erstellen
from Test_Generator_Module import test_generator_modul_ilias_test_struktur
from Test_Generator_Module import test_generator_modul_taxonomie_und_textformatierung
from Test_Generator_Module import test_generator_modul_ilias_import_test_datei

class Zuordnungsfrage:
    def __init__(self, app, zuordnungsfrage_tab, project_root_path):

        self.zuordnungsfrage_tab = zuordnungsfrage_tab

############## SET QUESTION_TYPE SPECIFIC NAMES FOR DATABASE AND WORBOOK/SHEET
        # Name des Fragentyps
        self.mq_question_type_name = "zuordnungsfrage"

        # Name für Datenbank und Tabelle
        self.mq_database = "ilias_zuordnungsfrage_db.db"
        self.mq_database_table = "zuordnungsfrage_table"

        # Name für Tabellenkalulations-Datei und Tabelle
        self.mq_xlsx_workbook_name = "Zuordnungsfrage_DB_export_file"
        self.mq_xlsx_worksheet_name = "Zuordnungsfrage - Database"

############## SET IMAGE VARIABLES

        # Die Variablen müssen am Anfang des Programms gesetzt werden, um diese an andere Funktionen weitergeben zu können
        self.mq_description_img_name_1 = ""
        self.mq_description_img_name_2 = ""
        self.mq_description_img_name_3 = ""

        self.mq_description_img_data_1 = ""
        self.mq_description_img_data_2 = ""
        self.mq_description_img_data_3 = ""

        self.mq_description_img_path_1 = ""
        self.mq_description_img_path_2 = ""
        self.mq_description_img_path_3 = ""

        self.mq_mix_answers_value = 0

############## DEFINE MATCHING QUESTIONS PATHS

        # Pfad des Projekts und des MQ-Moduls
        self.project_root_path = project_root_path
        self.zuordnungsfrage_files_path = os.path.normpath(os.path.join(self.project_root_path, "ILIAS-Zuordnungsfrage"))
        self.zuordnungsfrage_files_path_pool_output = os.path.normpath(os.path.join(self.zuordnungsfrage_files_path, "mq_ilias_pool_abgabe"))

        # Pfad für die Datenbank
        self.database_zuordnungsfrage_path = os.path.normpath(os.path.join(self.project_root_path, "Test_Generator_Datenbanken", "ilias_zuordnungsfrage_db.db"))

        # Pfad für ILIAS-Test Vorlage
        self.zuordnungsfrage_test_qti_file_path_template = os.path.normpath(os.path.join(self.zuordnungsfrage_files_path, "mq_test_qti_und_tst_dateien_vorlage", "ilias_test_vorlage__qti__.xml"))
        self.zuordnungsfrage_test_tst_file_path_template = os.path.normpath(os.path.join(self.zuordnungsfrage_files_path, "mq_test_qti_und_tst_dateien_vorlage", "ilias_test_vorlage__tst__.xml"))


        # Pfad für ILIAS-Test Dateien (zum hochladen in ILIAS)
        self.zuordnungsfrage_test_qti_file_path_output = os.path.normpath(os.path.join(self.zuordnungsfrage_files_path,"mq_ilias_test_abgabe", "1604407426__0__tst_2040314", "1604407426__0__qti_2040314.xml"))
        self.zuordnungsfrage_test_tst_file_path_output = os.path.normpath(os.path.join(self.zuordnungsfrage_files_path,"mq_ilias_test_abgabe", "1604407426__0__tst_2040314", "1604407426__0__tst_2040314.xml"))
        self.zuordnungsfrage_test_img_file_path = os.path.normpath(os.path.join(self.zuordnungsfrage_files_path,"mq_ilias_test_abgabe", "1604407426__0__tst_2040314", "objects"))


        # Pfad für ILIAS-Pool Vorlage
        self.zuordnungsfrage_pool_qti_file_path_template = os.path.normpath(os.path.join(self.zuordnungsfrage_files_path, "mq_pool_qti_und_qpl_dateien_vorlage", "ilias_pool_vorlage__qti__.xml"))
        self.zuordnungsfrage_pool_qpl_file_path_template = os.path.normpath(os.path.join(self.zuordnungsfrage_files_path, "mq_pool_qti_und_qpl_dateien_vorlage", "ilias_pool_vorlage__qpl__.xml"))


        # Pfad für ILIAS-Pool Dateien (zum hochladen in ILIAS)
        # Die Pfade für die qti.xml und qpl.xml werden erst zur Laufzeit bestimmt.
        # Die Deklaration ist daher unter "class Create_Zuordnungsfrage_Pool"
        self.zuordnungsfrage_pool_directory_output = os.path.normpath(os.path.join(self.zuordnungsfrage_files_path,"mq_ilias_pool_abgabe"))


###################### "DATENBANK ENTRIES UND INDEX DICT  ###################

        # Dictionary aus zwei Listen erstellen
        self.mq_db_find_entries = []
        self.mq_db_find_indexes = []
        self.mq_db_column_names_list = []
        self.mq_collection_of_question_titles = []

        connect = sqlite3.connect(self.database_zuordnungsfrage_path)
        cursor = connect.execute('select * from ' + self.mq_database_table)
        self.mq_db_column_names_list = list(map(lambda x: x[0], cursor.description))
        self.db_column_names_string = ', :'.join(self.mq_db_column_names_list)
        self.db_column_names_string = ":" + self.db_column_names_string

        for i in range(len(self.mq_db_column_names_list)):
            self.mq_db_find_indexes.append(i)

        """
        # Durch list(map(lambdax: x[0])) werden die Spaltennamen aus der DB ausgelesen
        cursor = conn.execute('select * from ' + self.mq_database_table)
        db_column_names_list = list(map(lambda x: x[0], cursor.description))
        db_column_names_string  = ', :'.join(db_column_names_list)
        db_column_names_string  = ":" + db_column_names_string
        """

        self.mq_db_entry_to_index_dict = dict(zip((self.mq_db_column_names_list), (self.mq_db_find_indexes)))

        connect.commit()
        connect.close()


        # Combobox Entries Dict
        self.assignment_pairs_definitions_to_int_dict = {"Definition 1": 0, "Definition 2": 1, "Definition 3": 2, "Definition 4": 3, "Definition 5": 4,
                                                         "Definition 6": 5, "Definition 7": 6, "Definition 8": 7, "Definition 9": 8, "Definition 10": 9,
                                                          }

        self.assignment_pairs_terms_to_int_dict = {"Term 1": 0, "Term 2": 1, "Term 3": 2, "Term 4": 3, "Term 5": 4,
                                                    "Term 6": 5, "Term 7": 6, "Term 8": 7, "Term 9": 8, "Term 10": 9,
                                                    }

#################### FRAMES
        self.mq_frame_ilias_test_title = LabelFrame(self.zuordnungsfrage_tab, text="Testname & Autor", padx=5, pady=5)
        self.mq_frame_ilias_test_title.grid(row=0, column=0, padx=10, pady=10, sticky="NW")

        self.mq_frame = LabelFrame(self.zuordnungsfrage_tab, text="Zuordnungsfrage", padx=5, pady=5)
        self.mq_frame.grid(row=1, column=0, padx=10, pady=10, sticky="NW")

        self.mq_frame_question_attributes = LabelFrame(self.zuordnungsfrage_tab, text="Fragen Attribute", padx=5, pady=5)
        self.mq_frame_question_attributes.grid(row=2, column=0, padx=10, pady=10, sticky="NE")

        self.mq_frame_database = LabelFrame(self.zuordnungsfrage_tab, text="Zuordnungsfrage-Datenbank", padx=5, pady=5)
        self.mq_frame_database.grid(row=2, column=0, padx=10, pady=10, sticky="NW")

        self.mq_frame_create_zuordnungsfrage_test = LabelFrame(self.zuordnungsfrage_tab, text="MQ-Test erstellen", padx=5, pady=5)
        self.mq_frame_create_zuordnungsfrage_test.grid(row=2, column=0, padx=105, pady=120, sticky="NE")


        self.mq_frame_taxonomy_settings = LabelFrame(self.zuordnungsfrage_tab, text="Taxonomie Einstellungen", padx=5, pady=5)
        self.mq_frame_taxonomy_settings.grid(row=0, column=1, padx=10, pady=10, sticky="NW")

        self.mq_frame_question_description_functions = LabelFrame(self.zuordnungsfrage_tab, text="Fragentext Funktionen", padx=5, pady=5)
        self.mq_frame_question_description_functions.grid(row=1, column=1, padx=10, pady=10, sticky="NW")

        self.mq_frame_excel_import_export = LabelFrame(self.zuordnungsfrage_tab, text="Excel Import/Export", padx=5, pady=5)
        self.mq_frame_excel_import_export.grid(row=2, column=1, padx=10, pady=10, sticky="NW")

        self.mq_frame_question_permutation = LabelFrame(self.zuordnungsfrage_tab, text="Fragen - Permutation", padx=5, pady=5)
        self.mq_frame_question_permutation.grid(row=2, column=1,padx=10, pady=120,   sticky="NW")


        self.mq_frame_description_picture = LabelFrame(self.zuordnungsfrage_tab, text="Fragen-Text Bild", padx=5, pady=5)
        self.mq_frame_description_picture.grid(row=1, column=2, padx=10, pady=10, sticky="NW")
        
        
###################### "Testname & Autor" - FRAME   -------- LABELS / ENTRYS / BUTTONS  ################

        self.mq_ilias_test_title_label = Label(self.mq_frame_ilias_test_title, text="Name des Tests")
        self.mq_ilias_test_title_label.grid(row=0, column=0, sticky=W)

        self.mq_ilias_test_title_entry = Entry(self.mq_frame_ilias_test_title, width=60)
        self.mq_ilias_test_title_entry.grid(row=0, column=1, sticky=W, padx=30)

        self.mq_ilias_test_autor_label = Label(self.mq_frame_ilias_test_title, text="Autor")
        self.mq_ilias_test_autor_label.grid(row=1, column=0, sticky=W)

        self.mq_ilias_test_autor_entry = Entry(self.mq_frame_ilias_test_title, width=60)
        self.mq_ilias_test_autor_entry.grid(row=1, column=1, sticky=W, padx=30)
    
###################### "Fragen-Text Bild" - FRAME   -------- LABELS / ENTRYS / BUTTONS  ################

        # Hinzufügen Bild 1
        self.mq_var_use_image_1 = IntVar()
        self.mq_check_use_image_1_in_description = Checkbutton(self.mq_frame_question_description_functions, text="Bild 1 hochladen?", variable=self.mq_var_use_image_1, onvalue=1, offvalue=0)
        self.mq_check_use_image_1_in_description.deselect()
        self.mq_check_use_image_1_in_description.grid(row=5, column=0, sticky=W, padx=90, pady=(10, 0))

        # Hinzufügen Bild 2
        self.mq_var_use_image_2 = IntVar()
        self.mq_check_use_image_2_in_description = Checkbutton(self.mq_frame_question_description_functions, text="Bild 2 hochladen?", variable=self.mq_var_use_image_2, onvalue=1, offvalue=0)
        self.mq_check_use_image_2_in_description.deselect()
        self.mq_check_use_image_2_in_description.grid(row=6, column=0, sticky=W, padx=90)

        # Hinzufügen Bild 3
        self.mq_var_use_image_3 = IntVar()
        self.mq_check_use_image_3_in_description = Checkbutton(self.mq_frame_question_description_functions, text="Bild 3 hochladen?", variable=self.mq_var_use_image_3, onvalue=1, offvalue=0)
        self.mq_check_use_image_3_in_description.deselect()
        self.mq_check_use_image_3_in_description.grid(row=7, column=0, sticky=W, padx=90)

        # Buttons - Bild hinzufügen & Bild löschen
        self.mq_add_img_to_description_btn = Button(self.mq_frame_question_description_functions, text="Bild hinzufügen", command=lambda: mq_add_image_to_description_and_create_labels())
        self.mq_add_img_to_description_btn.grid(row=8, column=0, sticky=W, padx = 10, pady=(20,0))



        def mq_add_image_to_description_and_create_labels():
            # Erstelle Labels
            self.mq_question_description_img_1_filename_label = Label(self.mq_frame_description_picture, text=self.mq_description_img_name_1)
            self.mq_question_description_img_2_filename_label = Label(self.mq_frame_description_picture, text=self.mq_description_img_name_2)
            self.mq_question_description_img_3_filename_label = Label(self.mq_frame_description_picture, text=self.mq_description_img_name_3)

            self.mq_description_img_name_1, self.mq_description_img_name_2, self.mq_description_img_name_3, self.mq_description_img_path_1, self.mq_description_img_path_2, self.mq_description_img_path_3, self.mq_question_description_img_1_filename_label, self.mq_question_description_img_2_filename_label, self.mq_question_description_img_3_filename_label = test_generator_modul_ilias_test_struktur.Additional_Funtions.add_image_to_description(
                    self,
                    self.mq_var_use_image_1.get(),
                    self.mq_var_use_image_2.get(),
                    self.mq_var_use_image_3.get(),
                    self.mq_frame_description_picture,
                    self.mq_description_img_name_1,
                    self.mq_description_img_name_2,
                    self.mq_description_img_name_3,
                    self.mq_description_img_path_1,
                    self.mq_description_img_path_2,
                    self.mq_description_img_path_3,
                    )


        self.mq_remove_img_from_description_btn = Button(self.mq_frame_question_description_functions, text="Bild entfernen", command=lambda: mq_add_image_to_description_and_delete_labels())
        self.mq_remove_img_from_description_btn.grid(row=8, column=0, sticky=W, padx=120, pady=(20,0))

        def mq_add_image_to_description_and_delete_labels():
            self.mq_description_img_name_1, self.mq_description_img_name_2, self.mq_description_img_name_3 = test_generator_modul_ilias_test_struktur.Additional_Funtions.delete_image_from_description(
                 self,
                 self.mq_var_use_image_1.get(),
                 self.mq_var_use_image_2.get(),
                 self.mq_var_use_image_3.get(),
                 self.mq_question_description_img_1_filename_label,
                 self.mq_question_description_img_2_filename_label,
                 self.mq_question_description_img_3_filename_label,
                 self.mq_description_img_name_1,
                 self.mq_description_img_name_2,
                 self.mq_description_img_name_3,
            )

###################### "Taxonomie Einstellungen" - FRAME   -------- LABELS / ENTRYS / BUTTONS  ################
        self.mq_taxonomy_settings_btn = Button(self.mq_frame_taxonomy_settings, text="Taxonomie-Einstellungen",command=lambda: test_generator_modul_taxonomie_und_textformatierung.Taxonomie.__init__(self))
        self.mq_taxonomy_settings_btn.grid(row=3, column=0, columnspan = 2, padx=10, sticky="W")

###################### "Fragentext Funktionen" - FRAME   -------- LABELS / ENTRYS / BUTTONS  ###################
        self.add_latex_term_btn = Button(self.mq_frame_question_description_functions, text="Text \"Latex\"", command=lambda: test_generator_modul_taxonomie_und_textformatierung.Textformatierung.text_latex(self, self.mq_question_description_main_entry))
        self.add_latex_term_btn.grid(row=1, column=0, padx=10, sticky="W")

        self.set_text_sub_btn = Button(self.mq_frame_question_description_functions, text="Text \"Tiefgestellt\"", command=lambda: test_generator_modul_taxonomie_und_textformatierung.Textformatierung.text_sub(self, self.mq_question_description_main_entry))
        self.set_text_sub_btn .grid(row=2, column=0, padx=10, pady=(10, 0), sticky="W")

        self.set_text_sup_btn = Button(self.mq_frame_question_description_functions, text="Text \"Hochgestellt\"", command=lambda: test_generator_modul_taxonomie_und_textformatierung.Textformatierung.text_sup(self, self.mq_question_description_main_entry))
        self.set_text_sup_btn.grid(row=3, column=0, padx=10, sticky="W")

        self.set_text_italic_btn = Button(self.mq_frame_question_description_functions, text="Text \"Kursiv\"", command=lambda: test_generator_modul_taxonomie_und_textformatierung.Textformatierung.text_italic(self, self.mq_question_description_main_entry))
        self.set_text_italic_btn.grid(row=4, column=0, padx=10, sticky="W")

        self.set_postion_for_picture_1_btn = Button(self.mq_frame_question_description_functions, text="Pos. Bild 1", command=lambda: test_generator_modul_taxonomie_und_textformatierung.Textformatierung.set_position_for_picture_1(self, self.mq_question_description_main_entry))
        self.set_postion_for_picture_1_btn.grid(row=5, column=0, padx=10, pady=(10, 0), sticky="W")

        self.set_postion_for_picture_2_btn = Button(self.mq_frame_question_description_functions, text="Pos. Bild 2", command=lambda: test_generator_modul_taxonomie_und_textformatierung.Textformatierung.set_position_for_picture_2(self, self.mq_question_description_main_entry))
        self.set_postion_for_picture_2_btn.grid(row=6, column=0, padx=10,  sticky="W")

        self.set_postion_for_picture_3_btn = Button(self.mq_frame_question_description_functions, text="Pos. Bild 3", command=lambda: test_generator_modul_taxonomie_und_textformatierung.Textformatierung.set_position_for_picture_3(self, self.mq_question_description_main_entry))
        self.set_postion_for_picture_3_btn.grid(row=7, column=0, padx=10,  sticky="W")



###################### "Fragen Attribute" - FRAME   -------- LABELS / ENTRYS / BUTTONS  ###################

        self.mq_question_difficulty_label = Label(self.mq_frame_question_attributes, text="Schwierigkeit")
        self.mq_question_difficulty_label.grid(row=0, column=0, pady=5, padx=5, sticky=W)

        self.mq_question_difficulty_entry = Entry(self.mq_frame_question_attributes, width=15)
        self.mq_question_difficulty_entry.grid(row=0, column=1, pady=5, padx=5, sticky=W)

        self.mq_question_category_label = Label(self.mq_frame_question_attributes, text="Fragenkategorie")
        self.mq_question_category_label.grid(row=1, column=0, pady=5, padx=5, sticky=W)

        self.mq_question_category_entry = Entry(self.mq_frame_question_attributes, width=15)
        self.mq_question_category_entry.grid(row=1, column=1, pady=5, padx=5, sticky=W)

        self.mq_question_type_label = Label(self.mq_frame_question_attributes, text="Fragen-Typ")
        self.mq_question_type_label.grid(row=0, column=2, pady=5, padx=5, sticky=W)

        self.mq_question_type_entry = Entry(self.mq_frame_question_attributes, width=15)
        self.mq_question_type_entry.grid(row=0, column=3, pady=5, padx=5, sticky=W)
        self.mq_question_type_entry.insert(0, "Zuordnungsfrage")

        self.mq_question_pool_tag_label = Label(self.mq_frame_question_attributes, text="Pool-Tag")
        self.mq_question_pool_tag_label.grid(row=1, column=2, pady=5, padx=5, sticky=W)

        self.mq_question_pool_tag_entry = Entry(self.mq_frame_question_attributes, width=15)
        self.mq_question_pool_tag_entry.grid(row=1, column=3, pady=5, padx=5, sticky=W)    


###################### "Zuordnungsfrage-Test erstellen" - FRAME   -------- LABELS / ENTRYS / BUTTONS  ###################

        # self.create_zuordnungsfrage_test_btn = Button(self.mq_frame_create_zuordnungsfrage_test, text="MQ-Test erstellen", command=lambda:  Create_Zuordnungsfrage_Test.__init__(self, self.mq_db_entry_to_index_dict))
        # self.create_zuordnungsfrage_test_btn.grid(row=2, column=0, sticky=W)
        # self.create_zuordnungsfrage_test_entry = Entry(self.mq_frame_create_zuordnungsfrage_test, width=15)
        # self.create_zuordnungsfrage_test_entry.grid(row=2, column=1, sticky=W, padx=20)
        # 
        # self.create_zuordnungsfrage_pool_btn = Button(self.mq_frame_create_zuordnungsfrage_test, text="MQ-Pool erstellen", command=lambda: Create_Zuordnungsfrage_Pool.__init__(self, self.mq_db_entry_to_index_dict))
        # self.create_zuordnungsfrage_pool_btn.grid(row=3, column=0, sticky=W, pady=10)
        # self.create_zuordnungsfrage_pool_entry = Entry(self.mq_frame_create_zuordnungsfrage_test, width=15)
        # self.create_zuordnungsfrage_pool_entry.grid(row=3, column=1, sticky=W, padx=20, pady=10)
        
        # Button "Zuordnungsfrage-Test erstellen"
        self.create_zuordnungsfrage_test_btn = Button(self.mq_frame_create_zuordnungsfrage_test, text="MQ-Test erstellen", command=lambda: Create_Zuordnungsfrage_Test.__init__(self, self.mq_db_entry_to_index_dict))
        self.create_zuordnungsfrage_test_btn.grid(row=0, column=0, sticky=W)
        self.create_zuordnungsfrage_test_entry = Entry(self.mq_frame_create_zuordnungsfrage_test, width=15)
        self.create_zuordnungsfrage_test_entry.grid(row=0, column=1, sticky=W, padx=0)

        # Checkbox "Test-Einstellungen übernehmen?"
        self.create_test_settings_label = Label(self.mq_frame_create_zuordnungsfrage_test, text="Test-Einstellungen übernehmen?")
        self.create_test_settings_label.grid(row=1, column=0, pady=5, padx=5, sticky=W)
        self.var_test_settings = IntVar()
        self.check_test_settings = Checkbutton(self.mq_frame_create_zuordnungsfrage_test, text="", variable=self.var_test_settings, onvalue=1, offvalue=0)
        self.check_test_settings.deselect()
        self.check_test_settings.grid(row=1, column=1, sticky=W)

        # Checkbox "Latex für Fragentext nutzen?"
        self.mq_use_latex_on_text_label = Label(self.mq_frame_create_zuordnungsfrage_test, text="Latex für Fragentext nutzen?")
        self.mq_use_latex_on_text_label.grid(row=2, column=0, sticky=W, padx=5)
        self.mq_var_use_latex_on_text_check = IntVar()
        self.mq_use_latex_on_text_check = Checkbutton(self.mq_frame_create_zuordnungsfrage_test, text="", variable=self.mq_var_use_latex_on_text_check, onvalue=1, offvalue=0)
        self.mq_use_latex_on_text_check.deselect()
        self.mq_use_latex_on_text_check.grid(row=2, column=1, sticky=W)


        # Checkbox "Alle Einträge aus der DB erzeugen?"
        self.mq_create_question_pool_all_label = Label(self.mq_frame_create_zuordnungsfrage_test, text="Alle Einträge aus der DB erzeugen?")
        self.mq_create_question_pool_all_label.grid(row=4, column=0, pady=(10,0), padx=5, sticky=W)
        self.mq_var_create_question_pool_all_check = IntVar()
        self.mq_create_question_pool_all = Checkbutton(self.mq_frame_create_zuordnungsfrage_test, text="", variable=self.mq_var_create_question_pool_all_check, onvalue=1, offvalue=0)
        #self.mq_var_create_question_pool_all_check.set(0)
        self.mq_create_question_pool_all.grid(row=4, column=1, sticky=W, pady=(10,0))


        # Button "Zuordnungsfrage-Fragenpool erstellen"
        self.create_zuordnungsfrage_pool_btn = Button(self.mq_frame_create_zuordnungsfrage_test, text="MQ-Pool erstellen", command=lambda: Create_Zuordnungsfrage_Pool.__init__(self, self.mq_db_entry_to_index_dict, self.mq_var_create_question_pool_all_check.get()))
        self.create_zuordnungsfrage_pool_btn.grid(row=3, column=0, sticky=W, pady=(30,0))
        self.create_zuordnungsfrage_pool_entry = Entry(self.mq_frame_create_zuordnungsfrage_test, width=15)
        self.create_zuordnungsfrage_pool_entry.grid(row=3, column=1, sticky=W, padx=0, pady=(30,0))





###################### "Zuordnungsfrage-Datenbank" - FRAME   -------- LABELS / ENTRYS / BUTTONS  ###################


        self.mq_database_show_db_zuordnungsfrage_btn = Button(self.mq_frame_database, text="MQ - Datenbank anzeigen", command=lambda: test_generator_modul_datenbanken_anzeigen.MainGUI.__init__(self, self.database_zuordnungsfrage_path, "zuordnungsfrage_table"))
        self.mq_database_show_db_zuordnungsfrage_btn.grid(row=0, column=0, sticky=W, pady=5)

        self.mq_database_save_id_to_db_zuordnungsfrage_btn = Button(self.mq_frame_database, text="Speichern unter neuer ID", command=lambda: Zuordnungsfrage.mq_save_id_to_db(self))
        self.mq_database_save_id_to_db_zuordnungsfrage_btn.grid(row=1, column=0, sticky=W, pady=5)

        self.mq_database_delete_id_from_db_btn = Button(self.mq_frame_database, text="ID Löschen", command=lambda: Zuordnungsfrage.mq_delete_id_from_db(self))
        self.mq_database_delete_id_from_db_btn.grid(row=6, column=0, sticky=W, pady=5)
        self.mq_delete_box = Entry(self.mq_frame_database, width=10)
        self.mq_delete_box.grid(row=6, column=0, padx=80, sticky=W)

        # Noch keine Funktion
        self.mq_database_new_question_btn = Button(self.mq_frame_database, text="GUI Einträge leeren", command=lambda: Zuordnungsfrage.mq_clear_GUI(self))
        self.mq_database_new_question_btn.grid(row=8, column=0, sticky=W, pady=5)

        # Noch keine Funktion
        self.mq_database_edit_btn = Button(self.mq_frame_database, text="Aktuellen Eintrag editieren", command=lambda: Zuordnungsfrage.mq_edit_id_from_db(self))
        self.mq_database_edit_btn.grid(row=3, column=0, sticky=W, pady=5)


        self.mq_database_load_id_btn = Button(self.mq_frame_database, text="ID Laden", command=lambda: Zuordnungsfrage.mq_load_id_from_db(self, self.mq_db_entry_to_index_dict))
        self.mq_database_load_id_btn.grid(row=4, column=0, sticky=W, pady=(15,0))
        self.mq_load_box = Entry(self.mq_frame_database, width=10)
        self.mq_load_box.grid(row=4, column=0, sticky=W, padx=80, pady=(15,0))
        self.mq_hidden_edit_box_entry = Entry(self.mq_frame_database, width=10)

        # Checkbox - "Fragentext mit Highlighting?"
        self.mq_highlight_question_text_label = Label(self.mq_frame_database, text="Fragentext mit Highlighting?")
        self.mq_highlight_question_text_label.grid(row=5, column=0, pady=5, padx=5)

        self.mq_var_highlight_question_text = IntVar()
        self.mq_check_highlight_question_text = Checkbutton(self.mq_frame_database, text="", variable=self.mq_var_highlight_question_text, onvalue=1, offvalue=0)
        self.mq_check_highlight_question_text.deselect()
        self.mq_check_highlight_question_text.grid(row=5, column=0, sticky=E)


        # Checkbox - "Alle DB Einträge löschen?"
        self.mq_delete_all_label = Label(self.mq_frame_database, text="Alle DB Einträge löschen?")
        self.mq_delete_all_label.grid(row=7, column=0, pady=5, padx=5)

        self.mq_var_delete_all = IntVar()
        self.mq_check_delete_all = Checkbutton(self.mq_frame_database, text="", variable=self.mq_var_delete_all, onvalue=1, offvalue=0)
        self.mq_check_delete_all.deselect()
        self.mq_check_delete_all.grid(row=7, column=0, sticky=E)

###################### "Excel Import/Export" - FRAME   -------- LABELS / ENTRYS / BUTTONS  ###################

        #excel_import_btn
        self.mq_excel_import_to_db_zuordnungsfrage_btn = Button(self.mq_frame_excel_import_export, text="Excel-Datei importieren", command=lambda: test_generator_modul_datenbanken_erstellen.Import_Export_Database.excel_import_to_db(self, self.mq_question_type_name, self.mq_db_entry_to_index_dict))
        self.mq_excel_import_to_db_zuordnungsfrage_btn.grid(row=0, column=1, sticky=W, pady=5, padx=10)

        # excel_export_btn
        self.mq_excel_export_to_xlsx_zuordnungsfrage_btn = Button(self.mq_frame_excel_import_export, text="Datenbank exportieren",command=lambda: test_generator_modul_datenbanken_erstellen.Import_Export_Database.excel_export_to_xlsx(self, self.project_root_path, self.mq_db_entry_to_index_dict, self.database_zuordnungsfrage_path, self.mq_database, self.mq_database_table, self.mq_xlsx_workbook_name, self.mq_xlsx_worksheet_name))
        self.mq_excel_export_to_xlsx_zuordnungsfrage_btn.grid(row=1, column=1, sticky=W, pady=5, padx=10)

        # ILIAS_testfile_import
        self.mq_import_ilias_testfile_btn = Button(self.mq_frame_excel_import_export, text="ILIAS-Datei importieren",command=lambda: test_generator_modul_ilias_import_test_datei.Import_ILIAS_Datei_in_DB.__init__(self, self.project_root_path))
        self.mq_import_ilias_testfile_btn.grid(row=2, column=1, sticky=W, pady=(20,0), padx=10)


###################### "Zuordnungsfrage" - FRAME   -------- LABELS / ENTRYS / BUTTONS  ###################

        self.mq_question_author_label = Label(self.mq_frame, text="Fragen-Autor")
        self.mq_question_author_label.grid(row=0, column=0, sticky=W, padx=10, pady=(10, 0))
        self.mq_question_author_entry = Entry(self.mq_frame, width=30)
        self.mq_question_author_entry.grid(row=0, column=1, pady=(10, 0), sticky=W)

        self.mq_question_title_label = Label(self.mq_frame, text="Fragen-Titel")
        self.mq_question_title_label.grid(row=1, column=0, sticky=W, padx=10, pady=(10, 0))
        self.mq_question_title_entry = Entry(self.mq_frame, width=60)
        self.mq_question_title_entry.grid(row=1, column=1, pady=(10, 0), sticky=W)

        self.mq_question_description_title_label = Label(self.mq_frame, text="Fragen-Beschreibung")
        self.mq_question_description_title_label.grid(row=2, column=0, sticky=W, padx=10)
        self.mq_question_description_title_entry = Entry(self.mq_frame, width=60)
        self.mq_question_description_title_entry.grid(row=2, column=1, sticky=W)

        self.mq_question_textfield_label = Label(self.mq_frame, text="Fragen-Text")
        self.mq_question_textfield_label.grid(row=3, column=0, sticky=W, padx=10)

        self.mq_bar = Scrollbar(self.mq_frame)
        self.mq_question_description_main_entry = Text(self.mq_frame, height=6, width=80, font=('Helvetica', 9))
        self.mq_bar.grid(row=3, column=2, sticky=W)
        self.mq_question_description_main_entry.grid(row=3, column=1, pady=10, sticky=W)
        self.mq_bar.config(command=self.mq_question_description_main_entry.yview)
        self.mq_question_description_main_entry.config(yscrollcommand=self.mq_bar.set)

        self.mq_processing_time_label = Label(self.mq_frame, text="Bearbeitungsdauer")
        self.mq_processing_time_label.grid(row=4, column=0, sticky=W, pady=(5, 0), padx=10)

        self.mq_processing_time_label = Label(self.mq_frame, text="Std:")
        self.mq_processing_time_label.grid(row=4, column=1, sticky=W, pady=(5, 0))
        self.mq_processing_time_label = Label(self.mq_frame, text="Min:")
        self.mq_processing_time_label.grid(row=4, column=1, sticky=W, padx=70, pady=(5, 0))
        self.mq_processing_time_label = Label(self.mq_frame, text="Sek:")
        self.mq_processing_time_label.grid(row=4, column=1, sticky=W, padx=145, pady=(5, 0))


        self.mq_processingtime_hours = list(range(24))
        self.mq_processingtime_minutes = list(range(60))
        self.mq_processingtime_seconds = list(range(60))

        self.mq_proc_hours_box = ttk.Combobox(self.mq_frame, value=self.mq_processingtime_hours, width=2)
        self.mq_proc_minutes_box = ttk.Combobox(self.mq_frame, value=self.mq_processingtime_minutes, width=2)
        self.mq_proc_seconds_box = ttk.Combobox(self.mq_frame, value=self.mq_processingtime_seconds, width=2)

        self.mq_proc_hours_box.current(23)
        self.mq_proc_minutes_box.current(0)
        self.mq_proc_seconds_box.current(0)

        def mq_selected_hours(event):
            self.selected_hours = self.mq_proc_hours_box.get()


        def mq_selected_minutes(event):
            self.selected_minutes = self.mq_proc_minutes_box.get()


        def mq_selected_seconds(event):
            self.selected_seconds = self.mq_proc_seconds_box.get()


        self.mq_proc_hours_box.bind("<<ComboboxSelected>>", mq_selected_hours)
        self.mq_proc_hours_box.bind("<<ComboboxSelected>>", mq_selected_minutes)
        self.mq_proc_hours_box.bind("<<ComboboxSelected>>", mq_selected_seconds)

        self.mq_proc_hours_box.grid(row=4, column=1, sticky=W, padx=25, pady=(5, 0))
        self.mq_proc_minutes_box.grid(row=4, column=1, sticky=W, padx=100, pady=(5, 0))
        self.mq_proc_seconds_box.grid(row=4, column=1, sticky=W, padx=170, pady=(5, 0))

        self.mq_picture_preview_pixel_label = Label(self.mq_frame, text="Bild-Vorschaugröße (in Pixel)")
        self.mq_picture_preview_pixel_label.grid(row=4, column=1, sticky=E, padx=70)

        self.mq_picture_preview_pixel_entry = Entry(self.mq_frame, width=10)
        self.mq_picture_preview_pixel_entry.grid(row=4, column=1, sticky=E,  padx=0)
        self.mq_picture_preview_pixel_entry.insert(END, "300")

        self.mq_mix_answers_label = Label(self.mq_frame, text="Antworten mischen")
        self.mq_mix_answers_label.grid(row=5, column=0, sticky=W, padx=10, pady=(5, 0))

        self.mq_mix_answers_options = ["Nein", "Beides (Terme und Definitionen)", "Nur Terme", "Nur Definitionen"]
        self.mq_mix_answers_box = ttk.Combobox(self.mq_frame, value=self.mq_mix_answers_options, width=26)
        self.mq_mix_answers_box.current(0)

        def mq_selected_mix_answers_options(event):
            if self.mq_mix_answers_box.get() == "Nein":
                self.mq_mix_answers_value = 0
            elif self.mq_mix_answers_box.get() == "Beides(Terme und Definitionen)":
                self.mq_mix_answers_value = 1
            elif self.mq_mix_answers_box.get() == "Nur Terme":
                self.mq_mix_answers_value = 2
            elif self.mq_mix_answers_box.get() == "Nur Definitionen":
                self.mq_mix_answers_value = 3
        self.mq_mix_answers_box.bind("<<ComboboxSelected>>", mq_selected_mix_answers_options)
        self.mq_mix_answers_box.grid(row=5, column=1, sticky=W, padx=25, pady=(5, 0))

        self.mq_mix_answers_label = Label(self.mq_frame, text="Zuordnungsmodus")
        self.mq_mix_answers_label.grid(row=6, column=0, sticky=W, padx=10, pady=(5, 0))

        self.selected_matching_option = StringVar()
        self.selected_matching_option.set("1:1")
        self.select_question_option_1_radiobtn = Radiobutton(self.mq_frame, text="Ein Term kann einer Definition zugeordnet werden (1:1)", variable=self.selected_matching_option, value="1:1")
        self.select_question_option_1_radiobtn.grid(row=6, column=1, pady=0, sticky=W)
        self.select_question_option_2_radiobtn = Radiobutton(self.mq_frame, text="Ein oder mehrere Terme können einer oder mehreren Definitionen zugeordnet werden (n:n)", variable=self.selected_matching_option , value="n:n")
        self.select_question_option_2_radiobtn.grid(row=7, column=1, pady=0, sticky=W)


        self.mq_set_definitions_label = Label(self.mq_frame, text="Definitionen")
        self.mq_set_definitions_label.grid(row=10, column=0, sticky=W, padx=10, pady=(25, 0))



        self.mq_set_terms_label = Label(self.mq_frame, text="Terme")
        self.mq_set_terms_label.grid(row=30, column=0, sticky=W, padx=10, pady=(5, 0))

        self.mq_assignment_pairs_label = Label(self.mq_frame, text="Zuordnungspaare")
        self.mq_assignment_pairs_label.grid(row=50, column=0, sticky=W, padx=10, pady=(25, 0))





        self.mq_assignment_pairs_definitions_value = []

        self.mq_assignment_pairs_definitions_value = ["Definition 1", "Definition 2", "Definition 3",
                                                                  "Definition 4", "Definition 5",
                                                                  "Definition 6", "Definition 7", "Definition 8",
                                                                  "Definition 9", "Definition 10"]

        self.mq_assignment_pairs_terms_value = []

        self.mq_assignment_pairs_terms_value = ["Term 1", "Term 2", "Term 3",
                                                                  "Term 4", "Term 5",
                                                                  "Term 6", "Term 7", "Term 8",
                                                                  "Term 9", "Term 10"]

        def mq_definitions_answer_selected(event):  # "event" is necessary here to react, although it is not used "officially"

                if self.mq_definitions_numbers_of_answers_box.get() == '1':
                    #self.mq_assignment_pairs_definitions_value = ["Definition 1"]

                    mq_assignment_pairs_definitions_box_refresh()
                    mq_definitions_var2_remove()
                    mq_definitions_var3_remove()
                    mq_definitions_var4_remove()
                    mq_definitions_var5_remove()
                    mq_definitions_var6_remove()
                    mq_definitions_var7_remove()
                    mq_definitions_var8_remove()
                    mq_definitions_var9_remove()
                    mq_definitions_var10_remove()



                elif self.mq_definitions_numbers_of_answers_box.get() == '2':
                    #self.mq_assignment_pairs_definitions_value = ["Definition 1", "Definition 2"]

                    mq_assignment_pairs_definitions_box_refresh()
                    mq_definitions_var2_show()
                    mq_definitions_var3_remove()
                    mq_definitions_var4_remove()
                    mq_definitions_var5_remove()
                    mq_definitions_var6_remove()
                    mq_definitions_var7_remove()
                    mq_definitions_var8_remove()
                    mq_definitions_var9_remove()
                    mq_definitions_var10_remove()



                elif self.mq_definitions_numbers_of_answers_box.get() == '3':
                    #self.mq_assignment_pairs_definitions_value = ["Definition 1", "Definition 2", "Definition 3"]

                    mq_assignment_pairs_definitions_box_refresh()
                    mq_definitions_var2_show()
                    mq_definitions_var3_show()
                    mq_definitions_var4_remove()
                    mq_definitions_var5_remove()
                    mq_definitions_var6_remove()
                    mq_definitions_var7_remove()
                    mq_definitions_var8_remove()
                    mq_definitions_var9_remove()
                    mq_definitions_var10_remove()




                elif self.mq_definitions_numbers_of_answers_box.get() == '4':
                    #self.mq_assignment_pairs_definitions_value = ["Definition 1", "Definition 2", "Definition 3", "Definition 4"]

                    mq_assignment_pairs_definitions_box_refresh()
                    mq_definitions_var2_show()
                    mq_definitions_var3_show()
                    mq_definitions_var4_show()
                    mq_definitions_var5_remove()
                    mq_definitions_var6_remove()
                    mq_definitions_var7_remove()
                    mq_definitions_var8_remove()
                    mq_definitions_var9_remove()
                    mq_definitions_var10_remove()



                elif self.mq_definitions_numbers_of_answers_box.get() == '5':
                    #self.mq_assignment_pairs_definitions_value = ["Definition 1", "Definition 2", "Definition 3", "Definition 4", "Definition 5"]

                    mq_assignment_pairs_definitions_box_refresh()
                    mq_definitions_var2_show()
                    mq_definitions_var3_show()
                    mq_definitions_var4_show()
                    mq_definitions_var5_show()
                    mq_definitions_var6_remove()
                    mq_definitions_var7_remove()
                    mq_definitions_var8_remove()
                    mq_definitions_var9_remove()
                    mq_definitions_var10_remove()



                elif self.mq_definitions_numbers_of_answers_box.get() == '6':
                    #self.mq_assignment_pairs_definitions_value = ["Definition 1", "Definition 2", "Definition 3", "Definition 4", "Definition 5",
                    #                                              "Definition 6"]

                    mq_assignment_pairs_definitions_box_refresh()
                    mq_definitions_var2_show()
                    mq_definitions_var3_show()
                    mq_definitions_var4_show()
                    mq_definitions_var5_show()
                    mq_definitions_var6_show()
                    mq_definitions_var7_remove()
                    mq_definitions_var8_remove()
                    mq_definitions_var9_remove()
                    mq_definitions_var10_remove()



                elif self.mq_definitions_numbers_of_answers_box.get() == '7':
                    #self.mq_assignment_pairs_definitions_value = ["Definition 1", "Definition 2", "Definition 3", "Definition 4", "Definition 5",
                    #                                              "Definition 6", "Definition 7"]
                    mq_assignment_pairs_definitions_box_refresh()
                    mq_definitions_var2_show()
                    mq_definitions_var3_show()
                    mq_definitions_var4_show()
                    mq_definitions_var5_show()
                    mq_definitions_var6_show()
                    mq_definitions_var7_show()
                    mq_definitions_var8_remove()
                    mq_definitions_var9_remove()
                    mq_definitions_var10_remove()



                elif self.mq_definitions_numbers_of_answers_box.get() == '8':
                    #self.mq_assignment_pairs_definitions_value = ["Definition 1", "Definition 2", "Definition 3", "Definition 4", "Definition 5",
                    #                                              "Definition 6", "Definition 7", "Definition 8"]

                    mq_assignment_pairs_definitions_box_refresh()
                    mq_definitions_var2_show()
                    mq_definitions_var3_show()
                    mq_definitions_var4_show()
                    mq_definitions_var5_show()
                    mq_definitions_var6_show()
                    mq_definitions_var7_show()
                    mq_definitions_var8_show()
                    mq_definitions_var9_remove()
                    mq_definitions_var10_remove()



                elif self.mq_definitions_numbers_of_answers_box.get() == '9':
                    #self.mq_assignment_pairs_definitions_value = ["Definition 1", "Definition 2", "Definition 3", "Definition 4", "Definition 5",
                    #                                              "Definition 6", "Definition 7", "Definition 8", "Definition 9"]

                    mq_assignment_pairs_definitions_box_refresh()
                    mq_definitions_var2_show()
                    mq_definitions_var3_show()
                    mq_definitions_var4_show()
                    mq_definitions_var5_show()
                    mq_definitions_var6_show()
                    mq_definitions_var7_show()
                    mq_definitions_var8_show()
                    mq_definitions_var9_show()
                    mq_definitions_var10_remove()



                elif self.mq_definitions_numbers_of_answers_box.get() == '10':
                   # self.mq_assignment_pairs_definitions_value = ["Definition 1", "Definition 2", "Definition 3", "Definition 4", "Definition 5",
                   #                                               "Definition 6", "Definition 7", "Definition 8", "Definition 9", "Definition 10"]
                    mq_assignment_pairs_definitions_box_refresh()
                    mq_assignment_pairs_terms_box_refresh()
                    mq_definitions_var2_show()
                    mq_definitions_var3_show()
                    mq_definitions_var4_show()
                    mq_definitions_var5_show()
                    mq_definitions_var6_show()
                    mq_definitions_var7_show()
                    mq_definitions_var8_show()
                    mq_definitions_var9_show()
                    mq_definitions_var10_show()



        def mq_terms_answer_selected(event):  # "event" is necessary here to react, although it is not used "officially"

            if self.mq_terms_numbers_of_answers_box.get() == '1':
               # self.mq_assignment_pairs_terms_value = ["Term 1"]
                mq_assignment_pairs_terms_box_refresh()
                mq_terms_var2_remove()
                mq_terms_var3_remove()
                mq_terms_var4_remove()
                mq_terms_var5_remove()
                mq_terms_var6_remove()
                mq_terms_var7_remove()
                mq_terms_var8_remove()
                mq_terms_var9_remove()
                mq_terms_var10_remove()




            elif self.mq_terms_numbers_of_answers_box.get() == '2':
                #self.mq_assignment_pairs_terms_value = ["Term 1", "Term 2"]
                mq_assignment_pairs_terms_box_refresh()
                mq_terms_var2_show()
                mq_terms_var3_remove()
                mq_terms_var4_remove()
                mq_terms_var5_remove()
                mq_terms_var6_remove()
                mq_terms_var7_remove()
                mq_terms_var8_remove()
                mq_terms_var9_remove()
                mq_terms_var10_remove()



            elif self.mq_terms_numbers_of_answers_box.get() == '3':
                #self.mq_assignment_pairs_terms_value = ["Term 1", "Term 2", "Term 3"]
                mq_assignment_pairs_terms_box_refresh()
                mq_terms_var2_show()
                mq_terms_var3_show()
                mq_terms_var4_remove()
                mq_terms_var5_remove()
                mq_terms_var6_remove()
                mq_terms_var7_remove()
                mq_terms_var8_remove()
                mq_terms_var9_remove()
                mq_terms_var10_remove()



            elif self.mq_terms_numbers_of_answers_box.get() == '4':
                #self.mq_assignment_pairs_terms_value = ["Term 1", "Term 2", "Term 3", "Term 4"]
                mq_assignment_pairs_terms_box_refresh()
                mq_terms_var2_show()
                mq_terms_var3_show()
                mq_terms_var4_show()
                mq_terms_var5_remove()
                mq_terms_var6_remove()
                mq_terms_var7_remove()
                mq_terms_var8_remove()
                mq_terms_var9_remove()
                mq_terms_var10_remove()



            elif self.mq_terms_numbers_of_answers_box.get() == '5':
                #self.mq_assignment_pairs_terms_value = ["Term 1", "Term 2", "Term 3", "Term 4", "Term 5"]
                mq_assignment_pairs_terms_box_refresh()
                mq_terms_var2_show()
                mq_terms_var3_show()
                mq_terms_var4_show()
                mq_terms_var5_show()
                mq_terms_var6_remove()
                mq_terms_var7_remove()
                mq_terms_var8_remove()
                mq_terms_var9_remove()
                mq_terms_var10_remove()



            elif self.mq_terms_numbers_of_answers_box.get() == '6':
                #self.mq_assignment_pairs_terms_value = ["Term 1", "Term 2", "Term 3", "Term 4", "Term 5",
                #                                        "Term 6"]
                mq_assignment_pairs_terms_box_refresh()
                mq_terms_var2_show()
                mq_terms_var3_show()
                mq_terms_var4_show()
                mq_terms_var5_show()
                mq_terms_var6_show()
                mq_terms_var7_remove()
                mq_terms_var8_remove()
                mq_terms_var9_remove()
                mq_terms_var10_remove()



            elif self.mq_terms_numbers_of_answers_box.get() == '7':
                #self.mq_assignment_pairs_terms_value = ["Term 1", "Term 2", "Term 3", "Term 4", "Term 5",
                #                                        "Term 6", "Term 7"]
                mq_assignment_pairs_terms_box_refresh()
                mq_terms_var2_show()
                mq_terms_var3_show()
                mq_terms_var4_show()
                mq_terms_var5_show()
                mq_terms_var6_show()
                mq_terms_var7_show()
                mq_terms_var8_remove()
                mq_terms_var9_remove()
                mq_terms_var10_remove()



            elif self.mq_terms_numbers_of_answers_box.get() == '8':
                #self.mq_assignment_pairs_terms_value = ["Term 1", "Term 2", "Term 3", "Term 4", "Term 5",
                #                                        "Term 6", "Term 7", "Term 8"]
                mq_assignment_pairs_terms_box_refresh()
                mq_terms_var2_show()
                mq_terms_var3_show()
                mq_terms_var4_show()
                mq_terms_var5_show()
                mq_terms_var6_show()
                mq_terms_var7_show()
                mq_terms_var8_show()
                mq_terms_var9_remove()
                mq_terms_var10_remove()



            elif self.mq_terms_numbers_of_answers_box.get() == '9':
                #self.mq_assignment_pairs_terms_value = ["Term 1", "Term 2", "Term 3", "Term 4", "Term 5",
                #                                        "Term 6", "Term 7", "Term 8", "Term 9"]
                mq_assignment_pairs_terms_box_refresh()
                mq_terms_var2_show()
                mq_terms_var3_show()
                mq_terms_var4_show()
                mq_terms_var5_show()
                mq_terms_var6_show()
                mq_terms_var7_show()
                mq_terms_var8_show()
                mq_terms_var9_show()
                mq_terms_var10_remove()



            elif self.mq_terms_numbers_of_answers_box.get() == '10':
                #self.mq_assignment_pairs_terms_value = ["Term 1", "Term 2", "Term 3", "Term 4", "Term 5",
                #                                        "Term 6", "Term 7", "Term 8", "Term 9", "Term 10"]
                mq_assignment_pairs_terms_box_refresh()
                mq_terms_var2_show()
                mq_terms_var3_show()
                mq_terms_var4_show()
                mq_terms_var5_show()
                mq_terms_var6_show()
                mq_terms_var7_show()
                mq_terms_var8_show()
                mq_terms_var9_show()
                mq_terms_var10_show()



        def mq_assignment_pairs_definitions_box_refresh():
            self.mq_assignment_pairs_definitions_1_box.destroy()
            self.mq_assignment_pairs_definitions_2_box.destroy()
            self.mq_assignment_pairs_definitions_3_box.destroy()
            self.mq_assignment_pairs_definitions_4_box.destroy()
            self.mq_assignment_pairs_definitions_5_box.destroy()
            self.mq_assignment_pairs_definitions_6_box.destroy()
            self.mq_assignment_pairs_definitions_7_box.destroy()
            self.mq_assignment_pairs_definitions_8_box.destroy()
            self.mq_assignment_pairs_definitions_9_box.destroy()
            self.mq_assignment_pairs_definitions_10_box.destroy()
            self.mq_assignment_pairs_definitions_1_box = ttk.Combobox(self.mq_frame, value=self.mq_assignment_pairs_definitions_value, width=20)
            self.mq_assignment_pairs_definitions_2_box = ttk.Combobox(self.mq_frame, value=self.mq_assignment_pairs_definitions_value, width=20)
            self.mq_assignment_pairs_definitions_3_box = ttk.Combobox(self.mq_frame, value=self.mq_assignment_pairs_definitions_value, width=20)
            self.mq_assignment_pairs_definitions_4_box = ttk.Combobox(self.mq_frame, value=self.mq_assignment_pairs_definitions_value, width=20)
            self.mq_assignment_pairs_definitions_5_box = ttk.Combobox(self.mq_frame, value=self.mq_assignment_pairs_definitions_value, width=20)
            self.mq_assignment_pairs_definitions_6_box = ttk.Combobox(self.mq_frame, value=self.mq_assignment_pairs_definitions_value, width=20)
            self.mq_assignment_pairs_definitions_7_box = ttk.Combobox(self.mq_frame, value=self.mq_assignment_pairs_definitions_value, width=20)
            self.mq_assignment_pairs_definitions_8_box = ttk.Combobox(self.mq_frame, value=self.mq_assignment_pairs_definitions_value, width=20)
            self.mq_assignment_pairs_definitions_9_box = ttk.Combobox(self.mq_frame, value=self.mq_assignment_pairs_definitions_value, width=20)
            self.mq_assignment_pairs_definitions_10_box = ttk.Combobox(self.mq_frame, value=self.mq_assignment_pairs_definitions_value, width=20)
            self.mq_assignment_pairs_definitions_1_box.current(0)
            self.mq_assignment_pairs_definitions_1_box.grid(row=52, column=1, sticky=W, pady=(5, 0))

        def mq_assignment_pairs_terms_box_refresh():
            self.mq_assignment_pairs_terms_1_box.destroy()
            self.mq_assignment_pairs_terms_2_box.destroy()
            self.mq_assignment_pairs_terms_3_box.destroy()
            self.mq_assignment_pairs_terms_4_box.destroy()
            self.mq_assignment_pairs_terms_5_box.destroy()
            self.mq_assignment_pairs_terms_6_box.destroy()
            self.mq_assignment_pairs_terms_7_box.destroy()
            self.mq_assignment_pairs_terms_8_box.destroy()
            self.mq_assignment_pairs_terms_9_box.destroy()
            self.mq_assignment_pairs_terms_10_box.destroy()
            self.mq_assignment_pairs_terms_1_box = ttk.Combobox(self.mq_frame, value=self.mq_assignment_pairs_terms_value, width=20)
            self.mq_assignment_pairs_terms_2_box = ttk.Combobox(self.mq_frame, value=self.mq_assignment_pairs_terms_value, width=20)
            self.mq_assignment_pairs_terms_3_box = ttk.Combobox(self.mq_frame, value=self.mq_assignment_pairs_terms_value, width=20)
            self.mq_assignment_pairs_terms_4_box = ttk.Combobox(self.mq_frame, value=self.mq_assignment_pairs_terms_value, width=20)
            self.mq_assignment_pairs_terms_5_box = ttk.Combobox(self.mq_frame, value=self.mq_assignment_pairs_terms_value, width=20)
            self.mq_assignment_pairs_terms_6_box = ttk.Combobox(self.mq_frame, value=self.mq_assignment_pairs_terms_value, width=20)
            self.mq_assignment_pairs_terms_7_box = ttk.Combobox(self.mq_frame, value=self.mq_assignment_pairs_terms_value, width=20)
            self.mq_assignment_pairs_terms_8_box = ttk.Combobox(self.mq_frame, value=self.mq_assignment_pairs_terms_value, width=20)
            self.mq_assignment_pairs_terms_9_box = ttk.Combobox(self.mq_frame, value=self.mq_assignment_pairs_terms_value, width=20)
            self.mq_assignment_pairs_terms_10_box = ttk.Combobox(self.mq_frame, value=self.mq_assignment_pairs_terms_value, width=20)
            self.mq_assignment_pairs_terms_1_box.grid(row=52, column=1, sticky=E, pady=(5, 0), padx=100)



        def mq_assignment_pairs_selected(event):
            if self.mq_assignment_pairs_numbers_of_answers_box.get() == '1':
                mq_assignment_pair_2_remove()
                mq_assignment_pair_3_remove()
                mq_assignment_pair_4_remove()
                mq_assignment_pair_5_remove()
                mq_assignment_pair_6_remove()
                mq_assignment_pair_7_remove()
                mq_assignment_pair_8_remove()
                mq_assignment_pair_9_remove()
                mq_assignment_pair_10_remove()
            if self.mq_assignment_pairs_numbers_of_answers_box.get() == '2':
                mq_assignment_pair_2_show()
                mq_assignment_pair_3_remove()
                mq_assignment_pair_4_remove()
                mq_assignment_pair_5_remove()
                mq_assignment_pair_6_remove()
                mq_assignment_pair_7_remove()
                mq_assignment_pair_8_remove()
                mq_assignment_pair_9_remove()
                mq_assignment_pair_10_remove()
            if self.mq_assignment_pairs_numbers_of_answers_box.get() == '3':
                mq_assignment_pair_2_show()
                mq_assignment_pair_3_show()
                mq_assignment_pair_4_remove()
                mq_assignment_pair_5_remove()
                mq_assignment_pair_6_remove()
                mq_assignment_pair_7_remove()
                mq_assignment_pair_8_remove()
                mq_assignment_pair_9_remove()
                mq_assignment_pair_10_remove()
            if self.mq_assignment_pairs_numbers_of_answers_box.get() == '4':
                mq_assignment_pair_2_show()
                mq_assignment_pair_3_show()
                mq_assignment_pair_4_show()
                mq_assignment_pair_5_remove()
                mq_assignment_pair_6_remove()
                mq_assignment_pair_7_remove()
                mq_assignment_pair_8_remove()
                mq_assignment_pair_9_remove()
                mq_assignment_pair_10_remove()
            if self.mq_assignment_pairs_numbers_of_answers_box.get() == '5':
                mq_assignment_pair_2_show()
                mq_assignment_pair_3_show()
                mq_assignment_pair_4_show()
                mq_assignment_pair_5_show()
                mq_assignment_pair_6_remove()
                mq_assignment_pair_7_remove()
                mq_assignment_pair_8_remove()
                mq_assignment_pair_9_remove()
                mq_assignment_pair_10_remove()
            if self.mq_assignment_pairs_numbers_of_answers_box.get() == '6':
                mq_assignment_pair_2_show()
                mq_assignment_pair_3_show()
                mq_assignment_pair_4_show()
                mq_assignment_pair_5_show()
                mq_assignment_pair_6_show()
                mq_assignment_pair_7_remove()
                mq_assignment_pair_8_remove()
                mq_assignment_pair_9_remove()
                mq_assignment_pair_10_remove()
            if self.mq_assignment_pairs_numbers_of_answers_box.get() == '7':
                mq_assignment_pair_2_show()
                mq_assignment_pair_3_show()
                mq_assignment_pair_4_show()
                mq_assignment_pair_5_show()
                mq_assignment_pair_6_show()
                mq_assignment_pair_7_show()
                mq_assignment_pair_8_remove()
                mq_assignment_pair_9_remove()
                mq_assignment_pair_10_remove()
            if self.mq_assignment_pairs_numbers_of_answers_box.get() == '8':
                mq_assignment_pair_2_show()
                mq_assignment_pair_3_show()
                mq_assignment_pair_4_show()
                mq_assignment_pair_5_show()
                mq_assignment_pair_6_show()
                mq_assignment_pair_7_show()
                mq_assignment_pair_8_show()
                mq_assignment_pair_9_remove()
                mq_assignment_pair_10_remove()
            if self.mq_assignment_pairs_numbers_of_answers_box.get() == '9':
                mq_assignment_pair_2_show()
                mq_assignment_pair_3_show()
                mq_assignment_pair_4_show()
                mq_assignment_pair_5_show()
                mq_assignment_pair_6_show()
                mq_assignment_pair_7_show()
                mq_assignment_pair_8_show()
                mq_assignment_pair_9_show()
                mq_assignment_pair_10_remove()
            if self.mq_assignment_pairs_numbers_of_answers_box.get() == '10':
                mq_assignment_pair_2_show()
                mq_assignment_pair_3_show()
                mq_assignment_pair_4_show()
                mq_assignment_pair_5_show()
                mq_assignment_pair_6_show()
                mq_assignment_pair_7_show()
                mq_assignment_pair_8_show()
                mq_assignment_pair_9_show()
                mq_assignment_pair_10_show()




        # AUSWAHLBOX FÜR DEFINITIONEN
        self.mq_definitions_numbers_of_answers_box_label = Label(self.mq_frame, text="Anzahl der Antworten")
        self.mq_definitions_numbers_of_answers_box_label.grid(row=8, column=0, sticky=W, padx=10, pady=(5, 0))
        self.mq_definitions_numbers_of_answers_value = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
        self.mq_definitions_numbers_of_answers_box = ttk.Combobox(self.mq_frame, value=self.mq_definitions_numbers_of_answers_value, width=20)
        self.mq_definitions_numbers_of_answers_box.bind("<<ComboboxSelected>>", mq_definitions_answer_selected)
        self.mq_definitions_numbers_of_answers_box.grid(row=8, column=1, sticky=W, pady=(5, 0))
        self.mq_definitions_numbers_of_answers_box.current(0)

        # AUSWAHLBOX FÜR TERME
        self.mq_terms_numbers_of_answers_value = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
        self.mq_terms_numbers_of_answers_box = ttk.Combobox(self.mq_frame, value=self.mq_terms_numbers_of_answers_value, width=20)
        self.mq_terms_numbers_of_answers_box.bind("<<ComboboxSelected>>", mq_terms_answer_selected)
        self.mq_terms_numbers_of_answers_box.grid(row=8, column=1, sticky=E, pady=(5, 0))
        self.mq_terms_numbers_of_answers_box.current(0)

        # AUSWAHLBOX FÜR ZUORDNUNGSPAARE
        self.mq_assignment_pairs_numbers_of_answers_value = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
        self.mq_assignment_pairs_numbers_of_answers_box = ttk.Combobox(self.mq_frame, value=self.mq_assignment_pairs_numbers_of_answers_value, width=20)
        self.mq_assignment_pairs_numbers_of_answers_box.bind("<<ComboboxSelected>>", mq_assignment_pairs_selected)
        self.mq_assignment_pairs_numbers_of_answers_box.grid(row=50, column=1, sticky=W, pady=(25, 0))
        self.mq_assignment_pairs_numbers_of_answers_box.current(0)



        # ZUORDNUNGSPAARE - DEFINITIONEN - AUSWAHLBOXEN
        self.mq_assignment_pairs_definitions_1_box = ttk.Combobox(self.mq_frame, value=self.mq_assignment_pairs_definitions_value, width=20)
        self.mq_assignment_pairs_definitions_2_box = ttk.Combobox(self.mq_frame, value=self.mq_assignment_pairs_definitions_value, width=20)
        self.mq_assignment_pairs_definitions_3_box = ttk.Combobox(self.mq_frame, value=self.mq_assignment_pairs_definitions_value, width=20)
        self.mq_assignment_pairs_definitions_4_box = ttk.Combobox(self.mq_frame, value=self.mq_assignment_pairs_definitions_value, width=20)
        self.mq_assignment_pairs_definitions_5_box = ttk.Combobox(self.mq_frame, value=self.mq_assignment_pairs_definitions_value, width=20)
        self.mq_assignment_pairs_definitions_6_box = ttk.Combobox(self.mq_frame, value=self.mq_assignment_pairs_definitions_value, width=20)
        self.mq_assignment_pairs_definitions_7_box = ttk.Combobox(self.mq_frame, value=self.mq_assignment_pairs_definitions_value, width=20)
        self.mq_assignment_pairs_definitions_8_box = ttk.Combobox(self.mq_frame, value=self.mq_assignment_pairs_definitions_value, width=20)
        self.mq_assignment_pairs_definitions_9_box = ttk.Combobox(self.mq_frame, value=self.mq_assignment_pairs_definitions_value, width=20)
        self.mq_assignment_pairs_definitions_10_box = ttk.Combobox(self.mq_frame, value=self.mq_assignment_pairs_definitions_value, width=20)

        self.mq_assignment_pairs_definitions_1_box.grid(row=52, column=1, sticky=W, pady=(5, 0))

        # ZUORDNUNGSPAARE - TERME - AUSWAHLBOXEN
        self.mq_assignment_pairs_terms_1_box = ttk.Combobox(self.mq_frame, value=self.mq_assignment_pairs_terms_value, width=20)
        self.mq_assignment_pairs_terms_2_box = ttk.Combobox(self.mq_frame, value=self.mq_assignment_pairs_terms_value, width=20)
        self.mq_assignment_pairs_terms_3_box = ttk.Combobox(self.mq_frame, value=self.mq_assignment_pairs_terms_value, width=20)
        self.mq_assignment_pairs_terms_4_box = ttk.Combobox(self.mq_frame, value=self.mq_assignment_pairs_terms_value, width=20)
        self.mq_assignment_pairs_terms_5_box = ttk.Combobox(self.mq_frame, value=self.mq_assignment_pairs_terms_value, width=20)
        self.mq_assignment_pairs_terms_6_box = ttk.Combobox(self.mq_frame, value=self.mq_assignment_pairs_terms_value, width=20)
        self.mq_assignment_pairs_terms_7_box = ttk.Combobox(self.mq_frame, value=self.mq_assignment_pairs_terms_value, width=20)
        self.mq_assignment_pairs_terms_8_box = ttk.Combobox(self.mq_frame, value=self.mq_assignment_pairs_terms_value, width=20)
        self.mq_assignment_pairs_terms_9_box = ttk.Combobox(self.mq_frame, value=self.mq_assignment_pairs_terms_value, width=20)
        self.mq_assignment_pairs_terms_10_box = ttk.Combobox(self.mq_frame, value=self.mq_assignment_pairs_terms_value, width=20)

        self.mq_assignment_pairs_terms_1_box.grid(row=52, column=1, sticky=E, pady=(5, 0), padx=100)


        # PUNKTE FÜR ZUORDNUNGSPAARE

        self.mq_assignment_pairs_pts_1_entry = Entry(self.mq_frame, width=8)
        self.mq_assignment_pairs_pts_2_entry = Entry(self.mq_frame, width=8)
        self.mq_assignment_pairs_pts_3_entry = Entry(self.mq_frame, width=8)
        self.mq_assignment_pairs_pts_4_entry = Entry(self.mq_frame, width=8)
        self.mq_assignment_pairs_pts_5_entry = Entry(self.mq_frame, width=8)
        self.mq_assignment_pairs_pts_6_entry = Entry(self.mq_frame, width=8)
        self.mq_assignment_pairs_pts_7_entry = Entry(self.mq_frame, width=8)
        self.mq_assignment_pairs_pts_8_entry = Entry(self.mq_frame, width=8)
        self.mq_assignment_pairs_pts_9_entry = Entry(self.mq_frame, width=8)
        self.mq_assignment_pairs_pts_10_entry = Entry(self.mq_frame, width=8)



        # self.Label(self.mq_frame, text="Antworten").grid(row=9, column=0, sticky=W, padx=10, pady=(5, 0))
        # self.Label(self.mq_frame, text="Antwort-Text").grid(row=9, column=1, sticky=W, pady=(5, 0))
        self.mq_response_img_label = Label(self.mq_frame, text="Antwort-Grafik")
        self.mq_response_img_label.grid(row=10, column=1, sticky=E, padx=40)


        # ------------------------------- VARIABLES - TEXT & ENTRY --------------------------------------------

        ######  VARIABLES
        # Eintrag-Felder für DEFINITIONEN
        self.mq_definitions_var1_answer_entry = Entry(self.mq_frame, width=45)
        self.mq_definitions_var2_answer_entry = Entry(self.mq_frame, width=45)
        self.mq_definitions_var3_answer_entry = Entry(self.mq_frame, width=45)
        self.mq_definitions_var4_answer_entry = Entry(self.mq_frame, width=45)
        self.mq_definitions_var5_answer_entry = Entry(self.mq_frame, width=45)
        self.mq_definitions_var6_answer_entry = Entry(self.mq_frame, width=45)
        self.mq_definitions_var7_answer_entry = Entry(self.mq_frame, width=45)
        self.mq_definitions_var8_answer_entry = Entry(self.mq_frame, width=45)
        self.mq_definitions_var9_answer_entry = Entry(self.mq_frame, width=45)
        self.mq_definitions_var10_answer_entry = Entry(self.mq_frame, width=45)

        # Eintrag-Felder für TERME
        self.mq_terms_var1_answer_entry = Entry(self.mq_frame, width=45)
        self.mq_terms_var2_answer_entry = Entry(self.mq_frame, width=45)
        self.mq_terms_var3_answer_entry = Entry(self.mq_frame, width=45)
        self.mq_terms_var4_answer_entry = Entry(self.mq_frame, width=45)
        self.mq_terms_var5_answer_entry = Entry(self.mq_frame, width=45)
        self.mq_terms_var6_answer_entry = Entry(self.mq_frame, width=45)
        self.mq_terms_var7_answer_entry = Entry(self.mq_frame, width=45)
        self.mq_terms_var8_answer_entry = Entry(self.mq_frame, width=45)
        self.mq_terms_var9_answer_entry = Entry(self.mq_frame, width=45)
        self.mq_terms_var10_answer_entry = Entry(self.mq_frame, width=45)



##################


        # DEFINITIONEN: BILD-DATEN
        self.mq_definitions_var1_img_data_entry =  Entry(self.mq_frame, width=8)
        self.mq_definitions_var2_img_data_entry =  Entry(self.mq_frame, width=8)
        self.mq_definitions_var3_img_data_entry =  Entry(self.mq_frame, width=8)
        self.mq_definitions_var4_img_data_entry =  Entry(self.mq_frame, width=8)
        self.mq_definitions_var5_img_data_entry =  Entry(self.mq_frame, width=8)
        self.mq_definitions_var6_img_data_entry =  Entry(self.mq_frame, width=8)
        self.mq_definitions_var7_img_data_entry =  Entry(self.mq_frame, width=8)
        self.mq_definitions_var8_img_data_entry =  Entry(self.mq_frame, width=8)
        self.mq_definitions_var9_img_data_entry =  Entry(self.mq_frame, width=8)
        self.mq_definitions_var10_img_data_entry =  Entry(self.mq_frame, width=8)

        # TERME: BILD-DATEN
        self.mq_terms_var1_img_data_entry =  Entry(self.mq_frame, width=8)
        self.mq_terms_var2_img_data_entry =  Entry(self.mq_frame, width=8)
        self.mq_terms_var3_img_data_entry =  Entry(self.mq_frame, width=8)
        self.mq_terms_var4_img_data_entry =  Entry(self.mq_frame, width=8)
        self.mq_terms_var5_img_data_entry =  Entry(self.mq_frame, width=8)
        self.mq_terms_var6_img_data_entry =  Entry(self.mq_frame, width=8)
        self.mq_terms_var7_img_data_entry =  Entry(self.mq_frame, width=8)
        self.mq_terms_var8_img_data_entry =  Entry(self.mq_frame, width=8)
        self.mq_terms_var9_img_data_entry =  Entry(self.mq_frame, width=8)
        self.mq_terms_var10_img_data_entry =  Entry(self.mq_frame, width=8)




        # DEFINITIONEN: BILD_PFAD
        self.mq_definitions_var1_img_path_entry =  Entry(self.mq_frame, width=8)
        self.mq_definitions_var2_img_path_entry =  Entry(self.mq_frame, width=8)
        self.mq_definitions_var3_img_path_entry =  Entry(self.mq_frame, width=8)
        self.mq_definitions_var4_img_path_entry =  Entry(self.mq_frame, width=8)
        self.mq_definitions_var5_img_path_entry =  Entry(self.mq_frame, width=8)
        self.mq_definitions_var6_img_path_entry =  Entry(self.mq_frame, width=8)
        self.mq_definitions_var7_img_path_entry =  Entry(self.mq_frame, width=8)
        self.mq_definitions_var8_img_path_entry =  Entry(self.mq_frame, width=8)
        self.mq_definitions_var9_img_path_entry =  Entry(self.mq_frame, width=8)
        self.mq_definitions_var10_img_path_entry =  Entry(self.mq_frame, width=8)

        # TERME: BILD_PFAD
        self.mq_terms_var1_img_path_entry =  Entry(self.mq_frame, width=8)
        self.mq_terms_var2_img_path_entry =  Entry(self.mq_frame, width=8)
        self.mq_terms_var3_img_path_entry =  Entry(self.mq_frame, width=8)
        self.mq_terms_var4_img_path_entry =  Entry(self.mq_frame, width=8)
        self.mq_terms_var5_img_path_entry =  Entry(self.mq_frame, width=8)
        self.mq_terms_var6_img_path_entry =  Entry(self.mq_frame, width=8)
        self.mq_terms_var7_img_path_entry =  Entry(self.mq_frame, width=8)
        self.mq_terms_var8_img_path_entry =  Entry(self.mq_frame, width=8)
        self.mq_terms_var9_img_path_entry =  Entry(self.mq_frame, width=8)
        self.mq_terms_var10_img_path_entry =  Entry(self.mq_frame, width=8)
################





        # ------------------------------- VARIABLES BUTTONS - SELECT IMAGE --------------------------------------------
        # DEFINITIONEN
        self.mq_definitions_var1_img_label_entry = Entry(self.mq_frame, width=30)
        self.mq_definitions_var2_img_label_entry = Entry(self.mq_frame, width=30)
        self.mq_definitions_var3_img_label_entry = Entry(self.mq_frame, width=30)
        self.mq_definitions_var4_img_label_entry = Entry(self.mq_frame, width=30)
        self.mq_definitions_var5_img_label_entry = Entry(self.mq_frame, width=30)
        self.mq_definitions_var6_img_label_entry = Entry(self.mq_frame, width=30)
        self.mq_definitions_var7_img_label_entry = Entry(self.mq_frame, width=30)
        self.mq_definitions_var8_img_label_entry = Entry(self.mq_frame, width=30)
        self.mq_definitions_var9_img_label_entry = Entry(self.mq_frame, width=30)
        self.mq_definitions_var10_img_label_entry = Entry(self.mq_frame, width=30)

        # TERME
        self.mq_terms_var1_img_label_entry = Entry(self.mq_frame, width=30)
        self.mq_terms_var2_img_label_entry = Entry(self.mq_frame, width=30)
        self.mq_terms_var3_img_label_entry = Entry(self.mq_frame, width=30)
        self.mq_terms_var4_img_label_entry = Entry(self.mq_frame, width=30)
        self.mq_terms_var5_img_label_entry = Entry(self.mq_frame, width=30)
        self.mq_terms_var6_img_label_entry = Entry(self.mq_frame, width=30)
        self.mq_terms_var7_img_label_entry = Entry(self.mq_frame, width=30)
        self.mq_terms_var8_img_label_entry = Entry(self.mq_frame, width=30)
        self.mq_terms_var9_img_label_entry = Entry(self.mq_frame, width=30)
        self.mq_terms_var10_img_label_entry = Entry(self.mq_frame, width=30)

        # DEFINITIONEN BUTTONS
        self.mq_definitions_var1_select_img_btn = Button(self.mq_frame, text="Datei wählen", command=lambda: Zuordnungsfrage.mq_add_image_to_answer(self, self.mq_definitions_var1_img_label_entry, self.mq_definitions_var1_img_data_entry, self.mq_definitions_var1_img_path_entry))
        self.mq_definitions_var2_select_img_btn = Button(self.mq_frame, text="Datei wählen", command=lambda: Zuordnungsfrage.mq_add_image_to_answer(self, self.mq_definitions_var2_img_label_entry, self.mq_definitions_var2_img_data_entry, self.mq_definitions_var2_img_path_entry))
        self.mq_definitions_var3_select_img_btn = Button(self.mq_frame, text="Datei wählen", command=lambda: Zuordnungsfrage.mq_add_image_to_answer(self, self.mq_definitions_var3_img_label_entry, self.mq_definitions_var3_img_data_entry, self.mq_definitions_var3_img_path_entry))
        self.mq_definitions_var4_select_img_btn = Button(self.mq_frame, text="Datei wählen", command=lambda: Zuordnungsfrage.mq_add_image_to_answer(self, self.mq_definitions_var4_img_label_entry, self.mq_definitions_var4_img_data_entry, self.mq_definitions_var4_img_path_entry))
        self.mq_definitions_var5_select_img_btn = Button(self.mq_frame, text="Datei wählen", command=lambda: Zuordnungsfrage.mq_add_image_to_answer(self, self.mq_definitions_var5_img_label_entry, self.mq_definitions_var5_img_data_entry, self.mq_definitions_var5_img_path_entry))
        self.mq_definitions_var6_select_img_btn = Button(self.mq_frame, text="Datei wählen", command=lambda: Zuordnungsfrage.mq_add_image_to_answer(self, self.mq_definitions_var6_img_label_entry, self.mq_definitions_var6_img_data_entry, self.mq_definitions_var6_img_path_entry))
        self.mq_definitions_var7_select_img_btn = Button(self.mq_frame, text="Datei wählen", command=lambda: Zuordnungsfrage.mq_add_image_to_answer(self, self.mq_definitions_var7_img_label_entry, self.mq_definitions_var7_img_data_entry, self.mq_definitions_var7_img_path_entry))
        self.mq_definitions_var8_select_img_btn = Button(self.mq_frame, text="Datei wählen", command=lambda: Zuordnungsfrage.mq_add_image_to_answer(self, self.mq_definitions_var8_img_label_entry, self.mq_definitions_var8_img_data_entry, self.mq_definitions_var8_img_path_entry))
        self.mq_definitions_var9_select_img_btn = Button(self.mq_frame, text="Datei wählen", command=lambda: Zuordnungsfrage.mq_add_image_to_answer(self, self.mq_definitions_var9_img_label_entry, self.mq_definitions_var9_img_data_entry, self.mq_definitions_var9_img_path_entry))
        self.mq_definitions_var10_select_img_btn = Button(self.mq_frame, text="Datei wählen", command=lambda: Zuordnungsfrage.mq_add_image_to_answer(self, self.mq_definitions_var10_img_label_entry, self.mq_definitions_var10_img_data_entry, self.mq_definitions_var10_img_path_entry))

        # TERME BUTTONS
        self.mq_terms_var1_select_img_btn = Button(self.mq_frame, text="Datei wählen", command=lambda: Zuordnungsfrage.mq_add_image_to_answer(self, self.mq_terms_var1_img_label_entry, self.mq_terms_var1_img_data_entry, self.mq_terms_var1_img_path_entry))
        self.mq_terms_var2_select_img_btn = Button(self.mq_frame, text="Datei wählen", command=lambda: Zuordnungsfrage.mq_add_image_to_answer(self, self.mq_terms_var2_img_label_entry, self.mq_terms_var2_img_data_entry, self.mq_terms_var2_img_path_entry))
        self.mq_terms_var3_select_img_btn = Button(self.mq_frame, text="Datei wählen", command=lambda: Zuordnungsfrage.mq_add_image_to_answer(self, self.mq_terms_var3_img_label_entry, self.mq_terms_var3_img_data_entry, self.mq_terms_var3_img_path_entry))
        self.mq_terms_var4_select_img_btn = Button(self.mq_frame, text="Datei wählen", command=lambda: Zuordnungsfrage.mq_add_image_to_answer(self, self.mq_terms_var4_img_label_entry, self.mq_terms_var4_img_data_entry, self.mq_terms_var4_img_path_entry))
        self.mq_terms_var5_select_img_btn = Button(self.mq_frame, text="Datei wählen", command=lambda: Zuordnungsfrage.mq_add_image_to_answer(self, self.mq_terms_var5_img_label_entry, self.mq_terms_var5_img_data_entry, self.mq_terms_var5_img_path_entry))
        self.mq_terms_var6_select_img_btn = Button(self.mq_frame, text="Datei wählen", command=lambda: Zuordnungsfrage.mq_add_image_to_answer(self, self.mq_terms_var6_img_label_entry, self.mq_terms_var6_img_data_entry, self.mq_terms_var6_img_path_entry))
        self.mq_terms_var7_select_img_btn = Button(self.mq_frame, text="Datei wählen", command=lambda: Zuordnungsfrage.mq_add_image_to_answer(self, self.mq_terms_var7_img_label_entry, self.mq_terms_var7_img_data_entry, self.mq_terms_var7_img_path_entry))
        self.mq_terms_var8_select_img_btn = Button(self.mq_frame, text="Datei wählen", command=lambda: Zuordnungsfrage.mq_add_image_to_answer(self, self.mq_terms_var8_img_label_entry, self.mq_terms_var8_img_data_entry, self.mq_terms_var8_img_path_entry))
        self.mq_terms_var9_select_img_btn = Button(self.mq_frame, text="Datei wählen", command=lambda: Zuordnungsfrage.mq_add_image_to_answer(self, self.mq_terms_var9_img_label_entry, self.mq_terms_var9_img_data_entry, self.mq_terms_var9_img_path_entry))
        self.mq_terms_var10_select_img_btn = Button(self.mq_frame, text="Datei wählen", command=lambda: Zuordnungsfrage.mq_add_image_to_answer(self, self.mq_terms_var10_img_label_entry, self.mq_terms_var10_img_data_entry, self.mq_terms_var10_img_path_entry))

        # DEFINITIONEN LABELS
        self.mq_definitions_answer1_label = Label(self.mq_frame, text="Zeile 1")
        self.mq_definitions_answer2_label = Label(self.mq_frame, text="Zeile 2")
        self.mq_definitions_answer3_label = Label(self.mq_frame, text="Zeile 3")
        self.mq_definitions_answer4_label = Label(self.mq_frame, text="Zeile 4")
        self.mq_definitions_answer5_label = Label(self.mq_frame, text="Zeile 5")
        self.mq_definitions_answer6_label = Label(self.mq_frame, text="Zeile 6")
        self.mq_definitions_answer7_label = Label(self.mq_frame, text="Zeile 7")
        self.mq_definitions_answer8_label = Label(self.mq_frame, text="Zeile 8")
        self.mq_definitions_answer9_label = Label(self.mq_frame, text="Zeile 9")
        self.mq_definitions_answer10_label = Label(self.mq_frame, text="Zeile 10")

        # THEMRE LABELS
        self.mq_terms_answer1_label = Label(self.mq_frame, text="Zeile 1")
        self.mq_terms_answer2_label = Label(self.mq_frame, text="Zeile 2")
        self.mq_terms_answer3_label = Label(self.mq_frame, text="Zeile 3")
        self.mq_terms_answer4_label = Label(self.mq_frame, text="Zeile 4")
        self.mq_terms_answer5_label = Label(self.mq_frame, text="Zeile 5")
        self.mq_terms_answer6_label = Label(self.mq_frame, text="Zeile 6")
        self.mq_terms_answer7_label = Label(self.mq_frame, text="Zeile 7")
        self.mq_terms_answer8_label = Label(self.mq_frame, text="Zeile 8")
        self.mq_terms_answer9_label = Label(self.mq_frame, text="Zeile 9")
        self.mq_terms_answer10_label = Label(self.mq_frame, text="Zeile 10")

        # DEFINITIONEN
        self.mq_definitions_answer1_label.grid(row=20, column=0, sticky=W, padx=30)
        self.mq_definitions_var1_answer_entry.grid(row=20, column=1, sticky=W)
        self.mq_definitions_var1_img_label_entry.grid(row=20, column=1, sticky=E, padx=0)
        self.mq_definitions_var1_select_img_btn.grid(row=20, column=1, sticky=E, padx=200)


        def mq_definitions_var2_show():
            self.mq_definitions_answer2_label.grid(row=21, column=0, sticky=W, padx=30)
            self.mq_definitions_var2_answer_entry.grid(row=21, column=1, sticky=W)
            self.mq_definitions_var2_img_label_entry.grid(row=21, column=1, sticky=E, padx=0)
            self.mq_definitions_var2_select_img_btn.grid(row=21, column=1, sticky=E, padx=200)


        def mq_definitions_var3_show():
            self.mq_definitions_answer3_label.grid(row=22, column=0, sticky=W, padx=30)
            self.mq_definitions_var3_answer_entry.grid(row=22, column=1, sticky=W)
            self.mq_definitions_var3_img_label_entry.grid(row=22, column=1, sticky=E, padx=0)
            self.mq_definitions_var3_select_img_btn.grid(row=22, column=1, sticky=E, padx=200)

        def mq_definitions_var4_show():
            self.mq_definitions_answer4_label.grid(row=23, column=0, sticky=W, padx=30)
            self.mq_definitions_var4_answer_entry.grid(row=23, column=1, sticky=W)
            self.mq_definitions_var4_img_label_entry.grid(row=23, column=1, sticky=E, padx=0)
            self.mq_definitions_var4_select_img_btn.grid(row=23, column=1, sticky=E, padx=200)

        def mq_definitions_var5_show():
            self.mq_definitions_answer5_label.grid(row=24, column=0, sticky=W, padx=30)
            self.mq_definitions_var5_answer_entry.grid(row=24, column=1, sticky=W)
            self.mq_definitions_var5_img_label_entry.grid(row=24, column=1, sticky=E, padx=0)
            self.mq_definitions_var5_select_img_btn.grid(row=24, column=1, sticky=E, padx=200)

        def mq_definitions_var6_show():
            self.mq_definitions_answer6_label.grid(row=25, column=0, sticky=W, padx=30)
            self.mq_definitions_var6_answer_entry.grid(row=25, column=1, sticky=W)
            self.mq_definitions_var6_img_label_entry.grid(row=25, column=1, sticky=E, padx=0)
            self.mq_definitions_var6_select_img_btn.grid(row=25, column=1, sticky=E, padx=200)

        def mq_definitions_var7_show():
            self.mq_definitions_answer7_label.grid(row=26, column=0, sticky=W, padx=30)
            self.mq_definitions_var7_answer_entry.grid(row=26, column=1, sticky=W)
            self.mq_definitions_var7_img_label_entry.grid(row=26, column=1, sticky=E, padx=0)
            self.mq_definitions_var7_select_img_btn.grid(row=26, column=1, sticky=E, padx=200)

        def mq_definitions_var8_show():
            self.mq_definitions_answer8_label.grid(row=27, column=0, sticky=W, padx=30)
            self.mq_definitions_var8_answer_entry.grid(row=27, column=1, sticky=W)
            self.mq_definitions_var8_img_label_entry.grid(row=27, column=1, sticky=E, padx=0)
            self.mq_definitions_var8_select_img_btn.grid(row=27, column=1, sticky=E, padx=200)

        def mq_definitions_var9_show():
            self.mq_definitions_answer9_label.grid(row=28, column=0, sticky=W, padx=30)
            self.mq_definitions_var9_answer_entry.grid(row=28, column=1, sticky=W)
            self.mq_definitions_var9_img_label_entry.grid(row=28, column=1, sticky=E, padx=0)
            self.mq_definitions_var9_select_img_btn.grid(row=28, column=1, sticky=E, padx=200)

        def mq_definitions_var10_show():
            self.mq_definitions_answer10_label.grid(row=29, column=0, sticky=W, padx=30)
            self.mq_definitions_var10_answer_entry.grid(row=29, column=1, sticky=W)
            self.mq_definitions_var10_img_label_entry.grid(row=29, column=1, sticky=E, padx=0)
            self.mq_definitions_var10_select_img_btn.grid(row=29, column=1, sticky=E, padx=200)

        def mq_definitions_var2_remove():
            self.mq_definitions_answer2_label.grid_remove()
            self.mq_definitions_var2_answer_entry.grid_remove()
            self.mq_definitions_var2_img_label_entry.grid_remove()
            self.mq_definitions_var2_select_img_btn.grid_remove()

        def mq_definitions_var3_remove():
            self.mq_definitions_answer3_label.grid_remove()
            self.mq_definitions_var3_answer_entry.grid_remove()
            self.mq_definitions_var3_img_label_entry.grid_remove()
            self.mq_definitions_var3_select_img_btn.grid_remove()

        def mq_definitions_var4_remove():
            self.mq_definitions_answer4_label.grid_remove()
            self.mq_definitions_var4_answer_entry.grid_remove()
            self.mq_definitions_var4_img_label_entry.grid_remove()
            self.mq_definitions_var4_select_img_btn.grid_remove()

        def mq_definitions_var5_remove():
            self.mq_definitions_answer5_label.grid_remove()
            self.mq_definitions_var5_answer_entry.grid_remove()
            self.mq_definitions_var5_img_label_entry.grid_remove()
            self.mq_definitions_var5_select_img_btn.grid_remove()

        def mq_definitions_var6_remove():
            self.mq_definitions_answer6_label.grid_remove()
            self.mq_definitions_var6_answer_entry.grid_remove()
            self.mq_definitions_var6_img_label_entry.grid_remove()
            self.mq_definitions_var6_select_img_btn.grid_remove()

        def mq_definitions_var7_remove():
            self.mq_definitions_answer7_label.grid_remove()
            self.mq_definitions_var7_answer_entry.grid_remove()
            self.mq_definitions_var7_img_label_entry.grid_remove()
            self.mq_definitions_var7_select_img_btn.grid_remove()

        def mq_definitions_var8_remove():
            self.mq_definitions_answer8_label.grid_remove()
            self.mq_definitions_var8_answer_entry.grid_remove()
            self.mq_definitions_var8_img_label_entry.grid_remove()
            self.mq_definitions_var8_select_img_btn.grid_remove()

        def mq_definitions_var9_remove():
            self.mq_definitions_answer9_label.grid_remove()
            self.mq_definitions_var9_answer_entry.grid_remove()
            self.mq_definitions_var9_img_label_entry.grid_remove()
            self.mq_definitions_var9_select_img_btn.grid_remove()

        def mq_definitions_var10_remove():
            self.mq_definitions_answer10_label.grid_remove()
            self.mq_definitions_var10_answer_entry.grid_remove()
            self.mq_definitions_var10_img_label_entry.grid_remove()
            self.mq_definitions_var10_select_img_btn.grid_remove()


        # TERME
        self.mq_terms_answer1_label.grid(row=40, column=0, sticky=W, padx=30)
        self.mq_terms_var1_answer_entry.grid(row=40, column=1, sticky=W)
        self.mq_terms_var1_img_label_entry.grid(row=40, column=1, sticky=E, padx=0)
        self.mq_terms_var1_select_img_btn.grid(row=40, column=1, sticky=E, padx=200)

        def mq_terms_var2_show():
            self.mq_terms_answer2_label.grid(row=41, column=0, sticky=W, padx=30)
            self.mq_terms_var2_answer_entry.grid(row=41, column=1, sticky=W)
            self.mq_terms_var2_img_label_entry.grid(row=41, column=1, sticky=E, padx=0)
            self.mq_terms_var2_select_img_btn.grid(row=41, column=1, sticky=E, padx=200)

        def mq_terms_var3_show():
            self.mq_terms_answer3_label.grid(row=42, column=0, sticky=W, padx=30)
            self.mq_terms_var3_answer_entry.grid(row=42, column=1, sticky=W)
            self.mq_terms_var3_img_label_entry.grid(row=42, column=1, sticky=E, padx=0)
            self.mq_terms_var3_select_img_btn.grid(row=42, column=1, sticky=E, padx=200)

        def mq_terms_var4_show():
            self.mq_terms_answer4_label.grid(row=43, column=0, sticky=W, padx=30)
            self.mq_terms_var4_answer_entry.grid(row=43, column=1, sticky=W)
            self.mq_terms_var4_img_label_entry.grid(row=43, column=1, sticky=E, padx=0)
            self.mq_terms_var4_select_img_btn.grid(row=43, column=1, sticky=E, padx=200)

        def mq_terms_var5_show():
            self.mq_terms_answer5_label.grid(row=44, column=0, sticky=W, padx=30)
            self.mq_terms_var5_answer_entry.grid(row=44, column=1, sticky=W)
            self.mq_terms_var5_img_label_entry.grid(row=44, column=1, sticky=E, padx=0)
            self.mq_terms_var5_select_img_btn.grid(row=44, column=1, sticky=E, padx=200)

        def mq_terms_var6_show():
            self.mq_terms_answer6_label.grid(row=45, column=0, sticky=W, padx=30)
            self.mq_terms_var6_answer_entry.grid(row=45, column=1, sticky=W)
            self.mq_terms_var6_img_label_entry.grid(row=45, column=1, sticky=E, padx=0)
            self.mq_terms_var6_select_img_btn.grid(row=45, column=1, sticky=E, padx=200)

        def mq_terms_var7_show():
            self.mq_terms_answer7_label.grid(row=46, column=0, sticky=W, padx=30)
            self.mq_terms_var7_answer_entry.grid(row=46, column=1, sticky=W)
            self.mq_terms_var7_img_label_entry.grid(row=46, column=1, sticky=E, padx=0)
            self.mq_terms_var7_select_img_btn.grid(row=46, column=1, sticky=E, padx=200)

        def mq_terms_var8_show():
            self.mq_terms_answer8_label.grid(row=47, column=0, sticky=W, padx=30)
            self.mq_terms_var8_answer_entry.grid(row=47, column=1, sticky=W)
            self.mq_terms_var8_img_label_entry.grid(row=47, column=1, sticky=E, padx=0)
            self.mq_terms_var8_select_img_btn.grid(row=47, column=1, sticky=E, padx=200)

        def mq_terms_var9_show():
            self.mq_terms_answer9_label.grid(row=48, column=0, sticky=W, padx=30)
            self.mq_terms_var9_answer_entry.grid(row=48, column=1, sticky=W)
            self.mq_terms_var9_img_label_entry.grid(row=48, column=1, sticky=E, padx=0)
            self.mq_terms_var9_select_img_btn.grid(row=48, column=1, sticky=E, padx=200)

        def mq_terms_var10_show():
            self.mq_terms_answer10_label.grid(row=49, column=0, sticky=W, padx=30)
            self.mq_terms_var10_answer_entry.grid(row=49, column=1, sticky=W)
            self.mq_terms_var10_img_label_entry.grid(row=49, column=1, sticky=E, padx=0)
            self.mq_terms_var10_select_img_btn.grid(row=49, column=1, sticky=E, padx=200)

        def mq_terms_var2_remove():
            self.mq_terms_answer2_label.grid_remove()
            self.mq_terms_var2_answer_entry.grid_remove()
            self.mq_terms_var2_img_label_entry.grid_remove()
            self.mq_terms_var2_select_img_btn.grid_remove()

        def mq_terms_var3_remove():
            self.mq_terms_answer3_label.grid_remove()
            self.mq_terms_var3_answer_entry.grid_remove()
            self.mq_terms_var3_img_label_entry.grid_remove()
            self.mq_terms_var3_select_img_btn.grid_remove()

        def mq_terms_var4_remove():
            self.mq_terms_answer4_label.grid_remove()
            self.mq_terms_var4_answer_entry.grid_remove()
            self.mq_terms_var4_img_label_entry.grid_remove()
            self.mq_terms_var4_select_img_btn.grid_remove()

        def mq_terms_var5_remove():
            self.mq_terms_answer5_label.grid_remove()
            self.mq_terms_var5_answer_entry.grid_remove()
            self.mq_terms_var5_img_label_entry.grid_remove()
            self.mq_terms_var5_select_img_btn.grid_remove()

        def mq_terms_var6_remove():
            self.mq_terms_answer6_label.grid_remove()
            self.mq_terms_var6_answer_entry.grid_remove()
            self.mq_terms_var6_img_label_entry.grid_remove()
            self.mq_terms_var6_select_img_btn.grid_remove()

        def mq_terms_var7_remove():
            self.mq_terms_answer7_label.grid_remove()
            self.mq_terms_var7_answer_entry.grid_remove()
            self.mq_terms_var7_img_label_entry.grid_remove()
            self.mq_terms_var7_select_img_btn.grid_remove()

        def mq_terms_var8_remove():
            self.mq_terms_answer8_label.grid_remove()
            self.mq_terms_var8_answer_entry.grid_remove()
            self.mq_terms_var8_img_label_entry.grid_remove()
            self.mq_terms_var8_select_img_btn.grid_remove()

        def mq_terms_var9_remove():
            self.mq_terms_answer9_label.grid_remove()
            self.mq_terms_var9_answer_entry.grid_remove()
            self.mq_terms_var9_img_label_entry.grid_remove()
            self.mq_terms_var9_select_img_btn.grid_remove()

        def mq_terms_var10_remove():
            self.mq_terms_answer10_label.grid_remove()
            self.mq_terms_var10_answer_entry.grid_remove()
            self.mq_terms_var10_img_label_entry.grid_remove()
            self.mq_terms_var10_select_img_btn.grid_remove()

    ### ZUORDNUNGSPAARE ANZEIGEN/AUSBLENDEN

        self.mq_assignment_pairs_pts_1_entry.grid(row=52, column=1, sticky=E, pady=(5, 0))


        def mq_assignment_pair_2_show():
            self.mq_assignment_pairs_definitions_2_box.grid(row=53, column=1, sticky=W, pady=(5, 0))
            self.mq_assignment_pairs_terms_2_box.grid(row=53, column=1, sticky=E, pady=(5, 0), padx=100)
            self.mq_assignment_pairs_pts_2_entry.grid(row=53, column=1, sticky=E, pady=(5, 0))

        def mq_assignment_pair_3_show():
            self.mq_assignment_pairs_definitions_3_box.grid(row=54, column=1, sticky=W, pady=(5, 0))
            self.mq_assignment_pairs_terms_3_box.grid(row=54, column=1, sticky=E, pady=(5, 0), padx=100)
            self.mq_assignment_pairs_pts_3_entry.grid(row=54, column=1, sticky=E, pady=(5, 0))

        def mq_assignment_pair_4_show():
            self.mq_assignment_pairs_definitions_4_box.grid(row=55, column=1, sticky=W, pady=(5, 0))
            self.mq_assignment_pairs_terms_4_box.grid(row=55, column=1, sticky=E, pady=(5, 0), padx=100)
            self.mq_assignment_pairs_pts_4_entry.grid(row=55, column=1, sticky=E, pady=(5, 0))

        def mq_assignment_pair_5_show():
            self.mq_assignment_pairs_definitions_5_box.grid(row=56, column=1, sticky=W, pady=(5, 0))
            self.mq_assignment_pairs_terms_5_box.grid(row=56, column=1, sticky=E, pady=(5, 0), padx=100)
            self.mq_assignment_pairs_pts_5_entry.grid(row=56, column=1, sticky=E, pady=(5, 0))

        def mq_assignment_pair_6_show():
            self.mq_assignment_pairs_definitions_6_box.grid(row=57, column=1, sticky=W, pady=(5, 0))
            self.mq_assignment_pairs_terms_6_box.grid(row=57, column=1, sticky=E, pady=(5, 0), padx=100)
            self.mq_assignment_pairs_pts_6_entry.grid(row=57, column=1, sticky=E, pady=(5, 0))

        def mq_assignment_pair_7_show():
            self.mq_assignment_pairs_definitions_7_box.grid(row=58, column=1, sticky=W, pady=(5, 0))
            self.mq_assignment_pairs_terms_7_box.grid(row=58, column=1, sticky=E, pady=(5, 0), padx=100)
            self.mq_assignment_pairs_pts_7_entry.grid(row=58, column=1, sticky=E, pady=(5, 0))

        def mq_assignment_pair_8_show():
            self.mq_assignment_pairs_definitions_8_box.grid(row=59, column=1, sticky=W, pady=(5, 0))
            self.mq_assignment_pairs_terms_8_box.grid(row=59, column=1, sticky=E, pady=(5, 0), padx=100)
            self.mq_assignment_pairs_pts_8_entry.grid(row=59, column=1, sticky=E, pady=(5, 0))

        def mq_assignment_pair_9_show():
            self.mq_assignment_pairs_definitions_9_box.grid(row=60, column=1, sticky=W, pady=(5, 0))
            self.mq_assignment_pairs_terms_9_box.grid(row=60, column=1, sticky=E, pady=(5, 0), padx=100)
            self.mq_assignment_pairs_pts_9_entry.grid(row=60, column=1, sticky=E, pady=(5, 0))

        def mq_assignment_pair_10_show():
            self.mq_assignment_pairs_definitions_10_box.grid(row=61, column=1, sticky=W, pady=(5, 0))
            self.mq_assignment_pairs_terms_10_box.grid(row=61, column=1, sticky=E, pady=(5, 0), padx=100)
            self.mq_assignment_pairs_pts_10_entry.grid(row=61, column=1, sticky=E, pady=(5, 0))

        def mq_assignment_pair_2_remove():
            self.mq_assignment_pairs_definitions_2_box.grid_remove()
            self.mq_assignment_pairs_terms_2_box.grid_remove()
            self.mq_assignment_pairs_pts_2_entry.grid_remove()
        def mq_assignment_pair_3_remove():
            self.mq_assignment_pairs_definitions_3_box.grid_remove()
            self.mq_assignment_pairs_terms_3_box.grid_remove()
            self.mq_assignment_pairs_pts_3_entry.grid_remove()
        def mq_assignment_pair_4_remove():
            self.mq_assignment_pairs_definitions_4_box.grid_remove()
            self.mq_assignment_pairs_terms_4_box.grid_remove()
            self.mq_assignment_pairs_pts_4_entry.grid_remove()
        def mq_assignment_pair_5_remove():
            self.mq_assignment_pairs_definitions_5_box.grid_remove()
            self.mq_assignment_pairs_terms_5_box.grid_remove()
            self.mq_assignment_pairs_pts_5_entry.grid_remove()
        def mq_assignment_pair_6_remove():
            self.mq_assignment_pairs_definitions_6_box.grid_remove()
            self.mq_assignment_pairs_terms_6_box.grid_remove()
            self.mq_assignment_pairs_pts_6_entry.grid_remove()
        def mq_assignment_pair_7_remove():
            self.mq_assignment_pairs_definitions_7_box.grid_remove()
            self.mq_assignment_pairs_terms_7_box.grid_remove()
            self.mq_assignment_pairs_pts_7_entry.grid_remove()
        def mq_assignment_pair_8_remove():
            self.mq_assignment_pairs_definitions_8_box.grid_remove()
            self.mq_assignment_pairs_terms_8_box.grid_remove()
            self.mq_assignment_pairs_pts_8_entry.grid_remove()
        def mq_assignment_pair_9_remove():
            self.mq_assignment_pairs_definitions_9_box.grid_remove()
            self.mq_assignment_pairs_terms_9_box.grid_remove()
            self.mq_assignment_pairs_pts_9_entry.grid_remove()
        def mq_assignment_pair_10_remove():
            self.mq_assignment_pairs_definitions_10_box.grid_remove()
            self.mq_assignment_pairs_terms_10_box.grid_remove()
            self.mq_assignment_pairs_pts_10_entry.grid_remove()



    # Funktion dient zur Auswahl von Bildern für einzelne Antwortmöglichkeiten
    def mq_add_image_to_answer(self, var_img_label_entry, picture_data_entry, picture_path_entry):

        ### Dateipfad auswählen
        self.mq_picture_path = filedialog.askopenfilename(initialdir=pathlib.Path().absolute(), title="Select a File")

        # "rindex" sucht nach einem bestimmten Zeichen in einem String, beginnend von rechts
        self.mq_picture_name = self.mq_picture_path[self.mq_picture_path.rindex('/')+1:]        # Nach dem "/" befindet sich der Dateiname
        self.mq_image_format = self.mq_picture_path[self.mq_picture_path.rindex('.'):]          # Nach dem "." befindet sich das Dateiformat z.B. .jpg

        ### Bild-Namen in entsprechendes, geleertes, Eingabefeld übertragen
        var_img_label_entry.delete(0, END)
        var_img_label_entry.insert(0, str(self.mq_picture_name))

        ### Bild-Daten in base64 speichern. Die XML Datei enthält die Bilder der Antworten in base64 encoded
        # "encoded64_string_raw enthält die Daten als String in der Form b'String'
        # Um die Daten in der richtigen Form zu erhalten (nur den String ohne b''), wird die Funktion .decode('utf-8') verwendet
        # Dieser String kann in der .xml Datei verwendet werden um im Ilias ein Bild zu erzeugen
        with open(self.mq_picture_path, "rb") as image_file:
            encoded64_string_raw = base64.b64encode(image_file.read())
            picture_data_entry.insert(END, encoded64_string_raw.decode('utf-8'))
            picture_path_entry.insert(END, self.mq_picture_path )




    def mq_save_id_to_db(self):
        conn = sqlite3.connect(self.database_zuordnungsfrage_path)
        c =conn.cursor()



        # format of duration P0Y0M0DT0H30M0S
        self.mq_test_time = "P0Y0M0DT" + self.mq_proc_hours_box.get() + "H" + self.mq_proc_minutes_box.get() + "M" + self.mq_proc_seconds_box.get() + "S"


        # Bild 1
        if self.mq_description_img_name_1 != "" and self.mq_description_img_name_1 != "EMPTY":
            # read image data in byte format

            with open(self.mq_description_img_path_1, 'rb') as image_file_1:
                self.mq_description_img_data_1 = image_file_1.read()


        else:
            self.mq_description_img_name_1 = ""
            self.mq_description_img_path_1 = ""
            self.mq_description_img_data_1 = ""


        # Bild 2
        if self.mq_description_img_name_2 != "" and self.mq_description_img_name_2 != "EMPTY":
            # read image data in byte format

            with open(self.mq_description_img_path_2, 'rb') as image_file_2:
                self.mq_description_img_data_2 = image_file_2.read()


        else:
            self.mq_description_img_name_2 = ""
            self.mq_description_img_path_2 = ""
            self.mq_description_img_data_2 = ""


        # Bild 3
        if self.mq_description_img_name_3 != "" and self.mq_description_img_name_3 != "EMPTY":

            # read image data in byte format

            with open(self.mq_description_img_path_3, 'rb') as image_file_3:
                self.mq_description_img_data_3 = image_file_3.read()


        else:
            self.mq_description_img_name_3 = ""
            self.mq_description_img_path_3 = ""
            self.mq_description_img_data_3 = ""

        def mq_bind_value_for_empty_answer_image(definition_picture_label_entry, definition_picture_data_entry, definition_picture_path_entry, term_picture_label_entry, term_picture_data_entry, term_picture_path_entry):

            if definition_picture_label_entry == "":
                definition_picture_label_entry.insert(0, "")
                definition_picture_data_entry.insert(0, "")
                definition_picture_path_entry.insert(0, "")

            if term_picture_label_entry == "":
                term_picture_label_entry.insert(0, "")
                term_picture_data_entry.insert(0, "")
                term_picture_path_entry.insert(0, "")

        
        mq_bind_value_for_empty_answer_image(self.mq_definitions_var1_img_label_entry, self.mq_definitions_var1_img_data_entry, self.mq_definitions_var1_img_path_entry, self.mq_terms_var1_img_label_entry, self.mq_terms_var1_img_data_entry, self.mq_terms_var1_img_path_entry)
        mq_bind_value_for_empty_answer_image(self.mq_definitions_var2_img_label_entry, self.mq_definitions_var2_img_data_entry, self.mq_definitions_var2_img_path_entry, self.mq_terms_var2_img_label_entry, self.mq_terms_var2_img_data_entry, self.mq_terms_var2_img_path_entry)
        mq_bind_value_for_empty_answer_image(self.mq_definitions_var3_img_label_entry, self.mq_definitions_var3_img_data_entry, self.mq_definitions_var3_img_path_entry, self.mq_terms_var3_img_label_entry, self.mq_terms_var3_img_data_entry, self.mq_terms_var3_img_path_entry)
        mq_bind_value_for_empty_answer_image(self.mq_definitions_var4_img_label_entry, self.mq_definitions_var4_img_data_entry, self.mq_definitions_var4_img_path_entry, self.mq_terms_var4_img_label_entry, self.mq_terms_var4_img_data_entry, self.mq_terms_var4_img_path_entry)
        mq_bind_value_for_empty_answer_image(self.mq_definitions_var6_img_label_entry, self.mq_definitions_var5_img_data_entry, self.mq_definitions_var5_img_path_entry, self.mq_terms_var5_img_label_entry, self.mq_terms_var5_img_data_entry, self.mq_terms_var5_img_path_entry)
        mq_bind_value_for_empty_answer_image(self.mq_definitions_var6_img_label_entry, self.mq_definitions_var6_img_data_entry, self.mq_definitions_var6_img_path_entry, self.mq_terms_var6_img_label_entry, self.mq_terms_var6_img_data_entry, self.mq_terms_var6_img_path_entry)
        mq_bind_value_for_empty_answer_image(self.mq_definitions_var7_img_label_entry, self.mq_definitions_var7_img_data_entry, self.mq_definitions_var7_img_path_entry, self.mq_terms_var7_img_label_entry, self.mq_terms_var7_img_data_entry, self.mq_terms_var7_img_path_entry)
        mq_bind_value_for_empty_answer_image(self.mq_definitions_var8_img_label_entry, self.mq_definitions_var8_img_data_entry, self.mq_definitions_var8_img_path_entry, self.mq_terms_var8_img_label_entry, self.mq_terms_var8_img_data_entry, self.mq_terms_var8_img_path_entry)
        mq_bind_value_for_empty_answer_image(self.mq_definitions_var9_img_label_entry, self.mq_definitions_var9_img_data_entry, self.mq_definitions_var9_img_path_entry, self.mq_terms_var9_img_label_entry, self.mq_terms_var9_img_data_entry, self.mq_terms_var9_img_path_entry)
        mq_bind_value_for_empty_answer_image(self.mq_definitions_var10_img_label_entry, self.mq_definitions_var10_img_data_entry, self.mq_definitions_var10_img_path_entry, self.mq_terms_var10_img_label_entry, self.mq_terms_var10_img_data_entry, self.mq_terms_var10_img_path_entry)
        

        # Insert into Table
        c.execute(
            "INSERT INTO zuordnungsfrage_table VALUES ("
            ":question_difficulty, :question_category, :question_type, "
            ":question_title, :question_description_title, :question_description_main, :mix_answers, :assignment_mode, "
            ":definitions_response_1_text, :definitions_response_1_img_label, :definitions_response_1_img_path, :definitions_response_1_img_string_base64_encoded, "
            ":definitions_response_2_text, :definitions_response_2_img_label, :definitions_response_2_img_path, :definitions_response_2_img_string_base64_encoded, "
            ":definitions_response_3_text, :definitions_response_3_img_label, :definitions_response_3_img_path, :definitions_response_3_img_string_base64_encoded, "
            ":definitions_response_4_text, :definitions_response_4_img_label, :definitions_response_4_img_path, :definitions_response_4_img_string_base64_encoded, "
            ":definitions_response_5_text, :definitions_response_5_img_label, :definitions_response_5_img_path, :definitions_response_5_img_string_base64_encoded, "
            ":definitions_response_6_text, :definitions_response_6_img_label, :definitions_response_6_img_path, :definitions_response_6_img_string_base64_encoded, "
            ":definitions_response_7_text, :definitions_response_7_img_label, :definitions_response_7_img_path, :definitions_response_7_img_string_base64_encoded, "
            ":definitions_response_8_text, :definitions_response_8_img_label, :definitions_response_8_img_path, :definitions_response_8_img_string_base64_encoded, "
            ":definitions_response_9_text, :definitions_response_9_img_label, :definitions_response_9_img_path, :definitions_response_9_img_string_base64_encoded, "
            ":definitions_response_10_text, :definitions_response_10_img_label, :definitions_response_10_img_path, :definitions_response_10_img_string_base64_encoded, "
            ":terms_response_1_text, :terms_response_1_img_label, :terms_response_1_img_path, :terms_response_1_img_string_base64_encoded, "
            ":terms_response_2_text, :terms_response_2_img_label, :terms_response_2_img_path, :terms_response_2_img_string_base64_encoded, "
            ":terms_response_3_text, :terms_response_3_img_label, :terms_response_3_img_path, :terms_response_3_img_string_base64_encoded, "
            ":terms_response_4_text, :terms_response_4_img_label, :terms_response_4_img_path, :terms_response_4_img_string_base64_encoded, "
            ":terms_response_5_text, :terms_response_5_img_label, :terms_response_5_img_path, :terms_response_5_img_string_base64_encoded, "
            ":terms_response_6_text, :terms_response_6_img_label, :terms_response_6_img_path, :terms_response_6_img_string_base64_encoded, "
            ":terms_response_7_text, :terms_response_7_img_label, :terms_response_7_img_path, :terms_response_7_img_string_base64_encoded, "
            ":terms_response_8_text, :terms_response_8_img_label, :terms_response_8_img_path, :terms_response_8_img_string_base64_encoded, "
            ":terms_response_9_text, :terms_response_9_img_label, :terms_response_9_img_path, :terms_response_9_img_string_base64_encoded, "
            ":terms_response_10_text, :terms_response_10_img_label, :terms_response_10_img_path, :terms_response_10_img_string_base64_encoded, "
            ":assignment_pairs_definition_1, :assignment_pairs_term_1, :assignment_pairs_1_pts,"
            ":assignment_pairs_definition_2, :assignment_pairs_term_2, :assignment_pairs_2_pts,"
            ":assignment_pairs_definition_3, :assignment_pairs_term_3, :assignment_pairs_3_pts,"
            ":assignment_pairs_definition_4, :assignment_pairs_term_4, :assignment_pairs_4_pts,"
            ":assignment_pairs_definition_5, :assignment_pairs_term_5, :assignment_pairs_5_pts,"
            ":assignment_pairs_definition_6, :assignment_pairs_term_6, :assignment_pairs_6_pts,"
            ":assignment_pairs_definition_7, :assignment_pairs_term_7, :assignment_pairs_7_pts,"
            ":assignment_pairs_definition_8, :assignment_pairs_term_8, :assignment_pairs_8_pts,"
            ":assignment_pairs_definition_9, :assignment_pairs_term_9, :assignment_pairs_9_pts,"
            ":assignment_pairs_definition_10, :assignment_pairs_term_10, :assignment_pairs_10_pts,"
            ":picture_preview_pixel,"
            ":description_img_name_1, :description_img_data_1, :description_img_path_1, "
            ":description_img_name_2, :description_img_data_2, :description_img_path_2, "
            ":description_img_name_3, :description_img_data_3, :description_img_path_3, "
            ":test_time, :var_number, :res_number, :question_pool_tag, :question_author)",
            {
                'question_difficulty': self.mq_question_difficulty_entry.get(),
                'question_category': self.mq_question_category_entry.get(),
                'question_type': self.mq_question_type_entry.get(),
                'question_title': self.mq_question_title_entry.get(),
                'question_description_title': self.mq_question_description_title_entry.get(),

                # The first part, "1.0" means that the input should be read from line one, character zero (ie: the very first character).
                # END is an imported constant which is set to the string "end". The END part means to read until the end of the text box is reached.
                # The only issue with this is that it actually adds a newline to our input. "
                # "So, in order to fix it we should change END to end-1c(Thanks Bryan Oakley) The -1c deletes 1 character, while -2c would mean delete two characters, and so on."
                'question_description_main': self.mq_question_description_main_entry.get("1.0", 'end-1c'),

                'mix_answers': self.mq_mix_answers_box.get(),
                'assignment_mode': self.selected_matching_option.get(),

                'definitions_response_1_text': self.mq_definitions_var1_answer_entry.get(),
                'definitions_response_2_text': self.mq_definitions_var2_answer_entry.get(),
                'definitions_response_3_text': self.mq_definitions_var3_answer_entry.get(),
                'definitions_response_4_text': self.mq_definitions_var4_answer_entry.get(),
                'definitions_response_5_text': self.mq_definitions_var5_answer_entry.get(),
                'definitions_response_6_text': self.mq_definitions_var6_answer_entry.get(),
                'definitions_response_7_text': self.mq_definitions_var7_answer_entry.get(),
                'definitions_response_8_text': self.mq_definitions_var8_answer_entry.get(),
                'definitions_response_9_text': self.mq_definitions_var9_answer_entry.get(),
                'definitions_response_10_text': self.mq_definitions_var10_answer_entry.get(),
                'definitions_response_1_img_label': self.mq_definitions_var1_img_label_entry.get(),
                'definitions_response_2_img_label': self.mq_definitions_var2_img_label_entry.get(),
                'definitions_response_3_img_label': self.mq_definitions_var3_img_label_entry.get(),
                'definitions_response_4_img_label': self.mq_definitions_var4_img_label_entry.get(),
                'definitions_response_5_img_label': self.mq_definitions_var5_img_label_entry.get(),
                'definitions_response_6_img_label': self.mq_definitions_var6_img_label_entry.get(),
                'definitions_response_7_img_label': self.mq_definitions_var7_img_label_entry.get(),
                'definitions_response_8_img_label': self.mq_definitions_var8_img_label_entry.get(),
                'definitions_response_9_img_label': self.mq_definitions_var9_img_label_entry.get(),
                'definitions_response_10_img_label': self.mq_definitions_var10_img_label_entry.get(),
                'definitions_response_1_img_path': self.mq_definitions_var1_img_path_entry.get(),
                'definitions_response_2_img_path': self.mq_definitions_var2_img_path_entry.get(),
                'definitions_response_3_img_path': self.mq_definitions_var3_img_path_entry.get(),
                'definitions_response_4_img_path': self.mq_definitions_var4_img_path_entry.get(),
                'definitions_response_5_img_path': self.mq_definitions_var5_img_path_entry.get(),
                'definitions_response_6_img_path': self.mq_definitions_var6_img_path_entry.get(),
                'definitions_response_7_img_path': self.mq_definitions_var7_img_path_entry.get(),
                'definitions_response_8_img_path': self.mq_definitions_var8_img_path_entry.get(),
                'definitions_response_9_img_path': self.mq_definitions_var9_img_path_entry.get(),
                'definitions_response_10_img_path': self.mq_definitions_var10_img_path_entry.get(),
                'definitions_response_1_img_string_base64_encoded': self.mq_definitions_var1_img_data_entry.get(),
                'definitions_response_2_img_string_base64_encoded': self.mq_definitions_var2_img_data_entry.get(),
                'definitions_response_3_img_string_base64_encoded': self.mq_definitions_var3_img_data_entry.get(),
                'definitions_response_4_img_string_base64_encoded': self.mq_definitions_var4_img_data_entry.get(),
                'definitions_response_5_img_string_base64_encoded': self.mq_definitions_var5_img_data_entry.get(),
                'definitions_response_6_img_string_base64_encoded': self.mq_definitions_var6_img_data_entry.get(),
                'definitions_response_7_img_string_base64_encoded': self.mq_definitions_var7_img_data_entry.get(),
                'definitions_response_8_img_string_base64_encoded': self.mq_definitions_var8_img_data_entry.get(),
                'definitions_response_9_img_string_base64_encoded': self.mq_definitions_var9_img_data_entry.get(),
                'definitions_response_10_img_string_base64_encoded': self.mq_definitions_var10_img_data_entry.get(),

                'terms_response_1_text': self.mq_terms_var1_answer_entry.get(),
                'terms_response_2_text': self.mq_terms_var2_answer_entry.get(),
                'terms_response_3_text': self.mq_terms_var3_answer_entry.get(),
                'terms_response_4_text': self.mq_terms_var4_answer_entry.get(),
                'terms_response_5_text': self.mq_terms_var5_answer_entry.get(),
                'terms_response_6_text': self.mq_terms_var6_answer_entry.get(),
                'terms_response_7_text': self.mq_terms_var7_answer_entry.get(),
                'terms_response_8_text': self.mq_terms_var8_answer_entry.get(),
                'terms_response_9_text': self.mq_terms_var9_answer_entry.get(),
                'terms_response_10_text': self.mq_terms_var10_answer_entry.get(),
                'terms_response_1_img_label': self.mq_terms_var1_img_label_entry.get(),
                'terms_response_2_img_label': self.mq_terms_var2_img_label_entry.get(),
                'terms_response_3_img_label': self.mq_terms_var3_img_label_entry.get(),
                'terms_response_4_img_label': self.mq_terms_var4_img_label_entry.get(),
                'terms_response_5_img_label': self.mq_terms_var5_img_label_entry.get(),
                'terms_response_6_img_label': self.mq_terms_var6_img_label_entry.get(),
                'terms_response_7_img_label': self.mq_terms_var7_img_label_entry.get(),
                'terms_response_8_img_label': self.mq_terms_var8_img_label_entry.get(),
                'terms_response_9_img_label': self.mq_terms_var9_img_label_entry.get(),
                'terms_response_10_img_label': self.mq_terms_var10_img_label_entry.get(),
                'terms_response_1_img_path': self.mq_terms_var1_img_path_entry.get(),
                'terms_response_2_img_path': self.mq_terms_var2_img_path_entry.get(),
                'terms_response_3_img_path': self.mq_terms_var3_img_path_entry.get(),
                'terms_response_4_img_path': self.mq_terms_var4_img_path_entry.get(),
                'terms_response_5_img_path': self.mq_terms_var5_img_path_entry.get(),
                'terms_response_6_img_path': self.mq_terms_var6_img_path_entry.get(),
                'terms_response_7_img_path': self.mq_terms_var7_img_path_entry.get(),
                'terms_response_8_img_path': self.mq_terms_var8_img_path_entry.get(),
                'terms_response_9_img_path': self.mq_terms_var9_img_path_entry.get(),
                'terms_response_10_img_path': self.mq_terms_var10_img_path_entry.get(),
                'terms_response_1_img_string_base64_encoded': self.mq_terms_var1_img_data_entry.get(),
                'terms_response_2_img_string_base64_encoded': self.mq_terms_var2_img_data_entry.get(),
                'terms_response_3_img_string_base64_encoded': self.mq_terms_var3_img_data_entry.get(),
                'terms_response_4_img_string_base64_encoded': self.mq_terms_var4_img_data_entry.get(),
                'terms_response_5_img_string_base64_encoded': self.mq_terms_var5_img_data_entry.get(),
                'terms_response_6_img_string_base64_encoded': self.mq_terms_var6_img_data_entry.get(),
                'terms_response_7_img_string_base64_encoded': self.mq_terms_var7_img_data_entry.get(),
                'terms_response_8_img_string_base64_encoded': self.mq_terms_var8_img_data_entry.get(),
                'terms_response_9_img_string_base64_encoded': self.mq_terms_var9_img_data_entry.get(),
                'terms_response_10_img_string_base64_encoded': self.mq_terms_var10_img_data_entry.get(),

                'assignment_pairs_definition_1': self.mq_assignment_pairs_definitions_1_box.get(),
                'assignment_pairs_definition_2': self.mq_assignment_pairs_definitions_2_box.get(),
                'assignment_pairs_definition_3': self.mq_assignment_pairs_definitions_3_box.get(),
                'assignment_pairs_definition_4': self.mq_assignment_pairs_definitions_4_box.get(),
                'assignment_pairs_definition_5': self.mq_assignment_pairs_definitions_5_box.get(),
                'assignment_pairs_definition_6': self.mq_assignment_pairs_definitions_6_box.get(),
                'assignment_pairs_definition_7': self.mq_assignment_pairs_definitions_7_box.get(),
                'assignment_pairs_definition_8': self.mq_assignment_pairs_definitions_8_box.get(),
                'assignment_pairs_definition_9': self.mq_assignment_pairs_definitions_9_box.get(),
                'assignment_pairs_definition_10': self.mq_assignment_pairs_definitions_10_box.get(),
                'assignment_pairs_term_1': self.mq_assignment_pairs_terms_1_box.get(),
                'assignment_pairs_term_2': self.mq_assignment_pairs_terms_2_box.get(),
                'assignment_pairs_term_3': self.mq_assignment_pairs_terms_3_box.get(),
                'assignment_pairs_term_4': self.mq_assignment_pairs_terms_4_box.get(),
                'assignment_pairs_term_5': self.mq_assignment_pairs_terms_5_box.get(),
                'assignment_pairs_term_6': self.mq_assignment_pairs_terms_6_box.get(),
                'assignment_pairs_term_7': self.mq_assignment_pairs_terms_7_box.get(),
                'assignment_pairs_term_8': self.mq_assignment_pairs_terms_8_box.get(),
                'assignment_pairs_term_9': self.mq_assignment_pairs_terms_9_box.get(),
                'assignment_pairs_term_10': self.mq_assignment_pairs_terms_10_box.get(),
                'assignment_pairs_1_pts': self.mq_assignment_pairs_pts_1_entry.get(),
                'assignment_pairs_2_pts': self.mq_assignment_pairs_pts_2_entry.get(),
                'assignment_pairs_3_pts': self.mq_assignment_pairs_pts_3_entry.get(),
                'assignment_pairs_4_pts': self.mq_assignment_pairs_pts_4_entry.get(),
                'assignment_pairs_5_pts': self.mq_assignment_pairs_pts_5_entry.get(),
                'assignment_pairs_6_pts': self.mq_assignment_pairs_pts_6_entry.get(),
                'assignment_pairs_7_pts': self.mq_assignment_pairs_pts_7_entry.get(),
                'assignment_pairs_8_pts': self.mq_assignment_pairs_pts_8_entry.get(),
                'assignment_pairs_9_pts': self.mq_assignment_pairs_pts_9_entry.get(),
                'assignment_pairs_10_pts': self.mq_assignment_pairs_pts_10_entry.get(),

                'picture_preview_pixel': self.mq_picture_preview_pixel_entry.get(),


                'description_img_name_1': self.mq_description_img_name_1,
                'description_img_data_1': self.mq_description_img_data_1,
                'description_img_path_1': self.mq_description_img_path_1,

                'description_img_name_2': self.mq_description_img_name_2,
                'description_img_data_2': self.mq_description_img_data_2,
                'description_img_path_2': self.mq_description_img_path_2,

                'description_img_name_3': self.mq_description_img_name_3,
                'description_img_data_3': self.mq_description_img_data_3,
                'description_img_path_3': self.mq_description_img_path_3,

                'test_time': self.mq_test_time,
                'var_number': "",
                'res_number': "",
                'question_pool_tag': self.mq_question_pool_tag_entry.get(),
                'question_author': self.mq_question_author_entry.get()
            }
        )
        conn.commit()
        conn.close()

        print("Neuer Eintrag in die Zuordnungsfragen-Datenbank --> Fragentitel: " + str(self.mq_question_title_entry.get()))

    def mq_load_id_from_db(self, entry_to_index_dict):
        self.mq_db_entry_to_index_dict = entry_to_index_dict
        conn = sqlite3.connect(self.database_zuordnungsfrage_path)
        c = conn.cursor()
        record_id = self.mq_load_box.get()

        self.mq_hidden_edit_box_entry.delete(0, END)
        self.mq_hidden_edit_box_entry.insert(0, self.mq_load_box.get())

        c.execute("SELECT * FROM zuordnungsfrage_table WHERE oid =" + record_id)
        mq_db_records = c.fetchall()

        Zuordnungsfrage.mq_clear_GUI(self)
        
        self.mq_definitions_numbers_of_answers_box.current(9)
        self.mq_terms_numbers_of_answers_box.current(9)

        #Zuordnungsfrage.__init__()

        for mq_db_record in mq_db_records:




            self.mq_question_difficulty_entry.insert(END, mq_db_record[self.mq_db_entry_to_index_dict['question_difficulty']] )
            self.mq_question_category_entry.insert(END, mq_db_record[self.mq_db_entry_to_index_dict['question_category']])
            self.mq_question_type_entry.insert(END, mq_db_record[self.mq_db_entry_to_index_dict['question_type']])

            self.mq_question_title_entry.insert(END, mq_db_record[self.mq_db_entry_to_index_dict['question_title']])
            self.mq_question_description_title_entry.insert(END, mq_db_record[self.mq_db_entry_to_index_dict['question_description_title']])
            self.mq_question_description_main_entry.insert(END, mq_db_record[self.mq_db_entry_to_index_dict['question_description_main']])

            self.mq_definitions_var1_answer_entry.insert(END, mq_db_record[self.mq_db_entry_to_index_dict['definitions_response_1_text']])
            self.mq_definitions_var2_answer_entry.insert(END, mq_db_record[self.mq_db_entry_to_index_dict['definitions_response_2_text']])
            self.mq_definitions_var3_answer_entry.insert(END, mq_db_record[self.mq_db_entry_to_index_dict['definitions_response_3_text']])
            self.mq_definitions_var4_answer_entry.insert(END, mq_db_record[self.mq_db_entry_to_index_dict['definitions_response_4_text']])
            self.mq_definitions_var5_answer_entry.insert(END, mq_db_record[self.mq_db_entry_to_index_dict['definitions_response_5_text']])
            self.mq_definitions_var6_answer_entry.insert(END, mq_db_record[self.mq_db_entry_to_index_dict['definitions_response_6_text']])
            self.mq_definitions_var7_answer_entry.insert(END, mq_db_record[self.mq_db_entry_to_index_dict['definitions_response_7_text']])
            self.mq_definitions_var8_answer_entry.insert(END, mq_db_record[self.mq_db_entry_to_index_dict['definitions_response_8_text']])
            self.mq_definitions_var9_answer_entry.insert(END, mq_db_record[self.mq_db_entry_to_index_dict['definitions_response_9_text']])
            self.mq_definitions_var10_answer_entry.insert(END, mq_db_record[self.mq_db_entry_to_index_dict['definitions_response_10_text']])
            self.mq_definitions_var1_img_label_entry.insert(END, mq_db_record[self.mq_db_entry_to_index_dict['definitions_response_1_img_label']])
            self.mq_definitions_var2_img_label_entry.insert(END, mq_db_record[self.mq_db_entry_to_index_dict['definitions_response_2_img_label']])
            self.mq_definitions_var3_img_label_entry.insert(END, mq_db_record[self.mq_db_entry_to_index_dict['definitions_response_3_img_label']])
            self.mq_definitions_var4_img_label_entry.insert(END, mq_db_record[self.mq_db_entry_to_index_dict['definitions_response_4_img_label']])
            self.mq_definitions_var5_img_label_entry.insert(END, mq_db_record[self.mq_db_entry_to_index_dict['definitions_response_5_img_label']])
            self.mq_definitions_var6_img_label_entry.insert(END, mq_db_record[self.mq_db_entry_to_index_dict['definitions_response_6_img_label']])
            self.mq_definitions_var7_img_label_entry.insert(END, mq_db_record[self.mq_db_entry_to_index_dict['definitions_response_7_img_label']])
            self.mq_definitions_var8_img_label_entry.insert(END, mq_db_record[self.mq_db_entry_to_index_dict['definitions_response_8_img_label']])
            self.mq_definitions_var9_img_label_entry.insert(END, mq_db_record[self.mq_db_entry_to_index_dict['definitions_response_9_img_label']])
            self.mq_definitions_var10_img_label_entry.insert(END, mq_db_record[self.mq_db_entry_to_index_dict['definitions_response_10_img_label']])
            
            self.mq_terms_var1_answer_entry.insert(END, mq_db_record[self.mq_db_entry_to_index_dict['terms_response_1_text']])
            self.mq_terms_var2_answer_entry.insert(END, mq_db_record[self.mq_db_entry_to_index_dict['terms_response_2_text']])
            self.mq_terms_var3_answer_entry.insert(END, mq_db_record[self.mq_db_entry_to_index_dict['terms_response_3_text']])
            self.mq_terms_var4_answer_entry.insert(END, mq_db_record[self.mq_db_entry_to_index_dict['terms_response_4_text']])
            self.mq_terms_var5_answer_entry.insert(END, mq_db_record[self.mq_db_entry_to_index_dict['terms_response_5_text']])
            self.mq_terms_var6_answer_entry.insert(END, mq_db_record[self.mq_db_entry_to_index_dict['terms_response_6_text']])
            self.mq_terms_var7_answer_entry.insert(END, mq_db_record[self.mq_db_entry_to_index_dict['terms_response_7_text']])
            self.mq_terms_var8_answer_entry.insert(END, mq_db_record[self.mq_db_entry_to_index_dict['terms_response_8_text']])
            self.mq_terms_var9_answer_entry.insert(END, mq_db_record[self.mq_db_entry_to_index_dict['terms_response_9_text']])
            self.mq_terms_var10_answer_entry.insert(END, mq_db_record[self.mq_db_entry_to_index_dict['terms_response_10_text']])
            self.mq_terms_var1_img_label_entry.insert(END, mq_db_record[self.mq_db_entry_to_index_dict['terms_response_1_img_label']])
            self.mq_terms_var2_img_label_entry.insert(END, mq_db_record[self.mq_db_entry_to_index_dict['terms_response_2_img_label']])
            self.mq_terms_var3_img_label_entry.insert(END, mq_db_record[self.mq_db_entry_to_index_dict['terms_response_3_img_label']])
            self.mq_terms_var4_img_label_entry.insert(END, mq_db_record[self.mq_db_entry_to_index_dict['terms_response_4_img_label']])
            self.mq_terms_var5_img_label_entry.insert(END, mq_db_record[self.mq_db_entry_to_index_dict['terms_response_5_img_label']])
            self.mq_terms_var6_img_label_entry.insert(END, mq_db_record[self.mq_db_entry_to_index_dict['terms_response_6_img_label']])
            self.mq_terms_var7_img_label_entry.insert(END, mq_db_record[self.mq_db_entry_to_index_dict['terms_response_7_img_label']])
            self.mq_terms_var8_img_label_entry.insert(END, mq_db_record[self.mq_db_entry_to_index_dict['terms_response_8_img_label']])
            self.mq_terms_var9_img_label_entry.insert(END, mq_db_record[self.mq_db_entry_to_index_dict['terms_response_9_img_label']])
            self.mq_terms_var10_img_label_entry.insert(END, mq_db_record[self.mq_db_entry_to_index_dict['terms_response_10_img_label']])

            self.mq_assignment_pairs_pts_1_entry.insert(END, mq_db_record[self.mq_db_entry_to_index_dict['assignment_pairs_1_pts']])
            self.mq_assignment_pairs_pts_2_entry.insert(END, mq_db_record[self.mq_db_entry_to_index_dict['assignment_pairs_2_pts']])
            self.mq_assignment_pairs_pts_3_entry.insert(END, mq_db_record[self.mq_db_entry_to_index_dict['assignment_pairs_3_pts']])
            self.mq_assignment_pairs_pts_4_entry.insert(END, mq_db_record[self.mq_db_entry_to_index_dict['assignment_pairs_4_pts']])
            self.mq_assignment_pairs_pts_5_entry.insert(END, mq_db_record[self.mq_db_entry_to_index_dict['assignment_pairs_5_pts']])
            self.mq_assignment_pairs_pts_6_entry.insert(END, mq_db_record[self.mq_db_entry_to_index_dict['assignment_pairs_6_pts']])
            self.mq_assignment_pairs_pts_7_entry.insert(END, mq_db_record[self.mq_db_entry_to_index_dict['assignment_pairs_7_pts']])
            self.mq_assignment_pairs_pts_8_entry.insert(END, mq_db_record[self.mq_db_entry_to_index_dict['assignment_pairs_8_pts']])
            self.mq_assignment_pairs_pts_9_entry.insert(END, mq_db_record[self.mq_db_entry_to_index_dict['assignment_pairs_9_pts']])
            self.mq_assignment_pairs_pts_10_entry.insert(END, mq_db_record[self.mq_db_entry_to_index_dict['assignment_pairs_10_pts']])



            if mq_db_record[self.mq_db_entry_to_index_dict['assignment_pairs_definition_1']] != "":
                self.mq_assignment_pairs_definitions_1_box.current(self.assignment_pairs_definitions_to_int_dict[mq_db_record[self.mq_db_entry_to_index_dict['assignment_pairs_definition_1']]])
            
            if mq_db_record[self.mq_db_entry_to_index_dict['assignment_pairs_definition_2']] != "":
                self.mq_assignment_pairs_definitions_2_box.current(self.assignment_pairs_definitions_to_int_dict[mq_db_record[self.mq_db_entry_to_index_dict['assignment_pairs_definition_2']]])
            
            if mq_db_record[self.mq_db_entry_to_index_dict['assignment_pairs_definition_3']] != "":
                self.mq_assignment_pairs_definitions_3_box.current(self.assignment_pairs_definitions_to_int_dict[mq_db_record[self.mq_db_entry_to_index_dict['assignment_pairs_definition_3']]])

            if mq_db_record[self.mq_db_entry_to_index_dict['assignment_pairs_definition_4']] != "":
                self.mq_assignment_pairs_definitions_4_box.current(self.assignment_pairs_definitions_to_int_dict[mq_db_record[self.mq_db_entry_to_index_dict['assignment_pairs_definition_4']]])

            if mq_db_record[self.mq_db_entry_to_index_dict['assignment_pairs_definition_5']] != "":
                self.mq_assignment_pairs_definitions_5_box.current(self.assignment_pairs_definitions_to_int_dict[mq_db_record[self.mq_db_entry_to_index_dict['assignment_pairs_definition_5']]])

            if mq_db_record[self.mq_db_entry_to_index_dict['assignment_pairs_definition_6']] != "":
                self.mq_assignment_pairs_definitions_6_box.current(self.assignment_pairs_definitions_to_int_dict[mq_db_record[self.mq_db_entry_to_index_dict['assignment_pairs_definition_6']]])

            if mq_db_record[self.mq_db_entry_to_index_dict['assignment_pairs_definition_7']] != "":
                self.mq_assignment_pairs_definitions_7_box.current(self.assignment_pairs_definitions_to_int_dict[mq_db_record[self.mq_db_entry_to_index_dict['assignment_pairs_definition_7']]])

            if mq_db_record[self.mq_db_entry_to_index_dict['assignment_pairs_definition_8']] != "":
                self.mq_assignment_pairs_definitions_8_box.current(self.assignment_pairs_definitions_to_int_dict[mq_db_record[self.mq_db_entry_to_index_dict['assignment_pairs_definition_8']]])

            if mq_db_record[self.mq_db_entry_to_index_dict['assignment_pairs_definition_9']] != "":
                self.mq_assignment_pairs_definitions_9_box.current(self.assignment_pairs_definitions_to_int_dict[mq_db_record[self.mq_db_entry_to_index_dict['assignment_pairs_definition_9']]])

            if mq_db_record[self.mq_db_entry_to_index_dict['assignment_pairs_definition_10']] != "":
                self.mq_assignment_pairs_definitions_10_box.current(self.assignment_pairs_definitions_to_int_dict[mq_db_record[self.mq_db_entry_to_index_dict['assignment_pairs_definition_10']]])


            if mq_db_record[self.mq_db_entry_to_index_dict['assignment_pairs_term_1']] != "":
                self.mq_assignment_pairs_terms_1_box.current(self.assignment_pairs_terms_to_int_dict[mq_db_record[self.mq_db_entry_to_index_dict['assignment_pairs_term_1']]])

            if mq_db_record[self.mq_db_entry_to_index_dict['assignment_pairs_term_2']] != "":
                self.mq_assignment_pairs_terms_2_box.current(self.assignment_pairs_terms_to_int_dict[mq_db_record[self.mq_db_entry_to_index_dict['assignment_pairs_term_2']]])

            if mq_db_record[self.mq_db_entry_to_index_dict['assignment_pairs_term_3']] != "":
                self.mq_assignment_pairs_terms_3_box.current(self.assignment_pairs_terms_to_int_dict[mq_db_record[self.mq_db_entry_to_index_dict['assignment_pairs_term_3']]])

            if mq_db_record[self.mq_db_entry_to_index_dict['assignment_pairs_term_4']] != "":
                self.mq_assignment_pairs_terms_4_box.current(self.assignment_pairs_terms_to_int_dict[mq_db_record[self.mq_db_entry_to_index_dict['assignment_pairs_term_4']]])

            if mq_db_record[self.mq_db_entry_to_index_dict['assignment_pairs_term_5']] != "":
                self.mq_assignment_pairs_terms_5_box.current(self.assignment_pairs_terms_to_int_dict[mq_db_record[self.mq_db_entry_to_index_dict['assignment_pairs_term_5']]])

            if mq_db_record[self.mq_db_entry_to_index_dict['assignment_pairs_term_6']] != "":
                self.mq_assignment_pairs_terms_6_box.current(self.assignment_pairs_terms_to_int_dict[mq_db_record[self.mq_db_entry_to_index_dict['assignment_pairs_term_6']]])

            if mq_db_record[self.mq_db_entry_to_index_dict['assignment_pairs_term_7']] != "":
                self.mq_assignment_pairs_terms_7_box.current(self.assignment_pairs_terms_to_int_dict[mq_db_record[self.mq_db_entry_to_index_dict['assignment_pairs_term_7']]])

            if mq_db_record[self.mq_db_entry_to_index_dict['assignment_pairs_term_8']] != "":
                self.mq_assignment_pairs_terms_8_box.current(self.assignment_pairs_terms_to_int_dict[mq_db_record[self.mq_db_entry_to_index_dict['assignment_pairs_term_8']]])

            if mq_db_record[self.mq_db_entry_to_index_dict['assignment_pairs_term_9']] != "":
                self.mq_assignment_pairs_terms_9_box.current(self.assignment_pairs_terms_to_int_dict[mq_db_record[self.mq_db_entry_to_index_dict['assignment_pairs_term_9']]])
            
            if mq_db_record[self.mq_db_entry_to_index_dict['assignment_pairs_term_10']] != "":
                self.mq_assignment_pairs_terms_10_box.current(self.assignment_pairs_terms_to_int_dict[mq_db_record[self.mq_db_entry_to_index_dict['assignment_pairs_term_10']]])

    def mq_edit_id_from_db(self):

        # Verbindung mit der Datenbank
        conn = sqlite3.connect(self.database_zuordnungsfrage_path)
        c = conn.cursor()

        # ID der Frage aus dem Eingabefeld "ID editieren" auslesen
        # Eingabefeld ist für den User nicht sichtbar
        record_id = self.mq_hidden_edit_box_entry.get()

        # Format von Testdauer in der XML Datei:  P0Y0M0DT0H30M0S
        self.mq_test_time = "P0Y0M0DT" + self.mq_proc_hours_box.get() + "H" + self.mq_proc_minutes_box.get() + "M" + self.mq_proc_seconds_box.get() + "S"

        # Ist ein Bild-Name vorhanden, dann das Bild über den Pfad einlesen
        # Sonst auf "EMPTY" setzen
        # Bilder werden als byte eingelesen "rb" = read byte

        # Fragen-Text Bild 1
        if self.mq_description_img_name_1 != "" or self.mq_description_img_name_1 != "EMPTY":
            with open(self.mq_description_img_path_1, 'rb') as description_image_file_1:
                self.mq_description_img_data_1 = description_image_file_1.read()

        else:
            self.mq_description_img_name_1 = ""
            self.mq_description_img_data_1 = ""
            self.mq_description_img_path_1 = ""

        # Fragen-Text Bild 2
        if self.mq_description_img_name_2 != "" or self.mq_description_img_name_2 != "EMPTY":
            with open(self.mq_description_img_path_2, 'rb') as description_image_file_2:
                self.mq_description_img_data_2 = description_image_file_2.read()

        else:
            self.mq_description_img_name_2 = ""
            self.mq_description_img_data_2 = ""
            self.mq_description_img_path_2 = ""

        # Fragen-Text Bild 3
        if self.mq_description_img_name_3 != "" or self.mq_description_img_name_3 != "EMPTY":
            with open(self.mq_description_img_path_3, 'rb') as description_image_file_3:
                self.mq_description_img_data_3 = description_image_file_3.read()

        else:
            self.mq_description_img_name_3 = ""
            self.mq_description_img_data_3 = ""
            self.mq_description_img_path_3 = ""

        c.execute("""UPDATE zuordnungsfrage_table SET
                question_difficulty = :question_difficulty,
                question_category = :question_category,
                question_type = :question_type,

                question_title = :question_title,
                question_description_title = :question_description_title,
                question_description_main = :question_description_main,
                mix_answers = :mix_answers,
                assignment_mode = :assignment_mode,

                definitions_response_1_text = :definitions_response_1_text,
                definitions_response_2_text = :definitions_response_2_text,
                definitions_response_3_text = :definitions_response_3_text,
                definitions_response_4_text = :definitions_response_4_text,
                definitions_response_5_text = :definitions_response_5_text,
                definitions_response_6_text = :definitions_response_6_text,
                definitions_response_7_text = :definitions_response_7_text,
                definitions_response_8_text = :definitions_response_8_text,
                definitions_response_9_text = :definitions_response_9_text,
                definitions_response_10_text = :definitions_response_10_text,
                definitions_response_1_img_label = :definitions_response_1_img_label,
                definitions_response_2_img_label = :definitions_response_2_img_label,
                definitions_response_3_img_label = :definitions_response_3_img_label,
                definitions_response_4_img_label = :definitions_response_4_img_label,
                definitions_response_5_img_label = :definitions_response_5_img_label,
                definitions_response_6_img_label = :definitions_response_6_img_label,
                definitions_response_7_img_label = :definitions_response_7_img_label,
                definitions_response_8_img_label = :definitions_response_8_img_label,
                definitions_response_9_img_label = :definitions_response_9_img_label,
                definitions_response_10_img_label = :definitions_response_10_img_label,
                definitions_response_1_img_path = :definitions_response_1_img_path,
                definitions_response_2_img_path = :definitions_response_2_img_path,
                definitions_response_3_img_path = :definitions_response_3_img_path,
                definitions_response_4_img_path = :definitions_response_4_img_path,
                definitions_response_5_img_path = :definitions_response_5_img_path,
                definitions_response_6_img_path = :definitions_response_6_img_path,
                definitions_response_7_img_path = :definitions_response_7_img_path,
                definitions_response_8_img_path = :definitions_response_8_img_path,
                definitions_response_9_img_path = :definitions_response_9_img_path,
                definitions_response_10_img_path = :definitions_response_10_img_path,
                definitions_response_1_img_string_base64_encoded = :definitions_response_1_img_string_base64_encoded,
                definitions_response_2_img_string_base64_encoded = :definitions_response_2_img_string_base64_encoded,
                definitions_response_3_img_string_base64_encoded = :definitions_response_3_img_string_base64_encoded,
                definitions_response_4_img_string_base64_encoded = :definitions_response_4_img_string_base64_encoded,
                definitions_response_5_img_string_base64_encoded = :definitions_response_5_img_string_base64_encoded,
                definitions_response_6_img_string_base64_encoded = :definitions_response_6_img_string_base64_encoded,
                definitions_response_7_img_string_base64_encoded = :definitions_response_7_img_string_base64_encoded,
                definitions_response_8_img_string_base64_encoded = :definitions_response_8_img_string_base64_encoded,
                definitions_response_9_img_string_base64_encoded = :definitions_response_9_img_string_base64_encoded,
                definitions_response_10_img_string_base64_encoded = :definitions_response_10_img_string_base64_encoded,

                terms_response_1_text = :terms_response_1_text ,
                terms_response_2_text = :terms_response_2_text,
                terms_response_3_text = :terms_response_3_text,
                terms_response_4_text = :terms_response_4_text,
                terms_response_5_text = :terms_response_5_text,
                terms_response_6_text = :terms_response_6_text,
                terms_response_7_text = :terms_response_7_text,
                terms_response_8_text = :terms_response_8_text,
                terms_response_9_text = :terms_response_9_text,
                terms_response_10_text = :terms_response_10_text,
                terms_response_1_img_label = :terms_response_1_img_label,
                terms_response_2_img_label = :terms_response_2_img_label,
                terms_response_3_img_label = :terms_response_3_img_label,
                terms_response_4_img_label = :terms_response_4_img_label,
                terms_response_5_img_label = :terms_response_5_img_label,
                terms_response_6_img_label = :terms_response_6_img_label,
                terms_response_7_img_label = :terms_response_7_img_label,
                terms_response_8_img_label = :terms_response_8_img_label,
                terms_response_9_img_label = :terms_response_9_img_label,
                terms_response_10_img_label = :terms_response_10_img_label,
                terms_response_1_img_path = :terms_response_1_img_path,
                terms_response_2_img_path = :terms_response_2_img_path,
                terms_response_3_img_path = :terms_response_3_img_path,
                terms_response_4_img_path = :terms_response_4_img_path,
                terms_response_5_img_path = :terms_response_5_img_path,
                terms_response_6_img_path = :terms_response_6_img_path,
                terms_response_7_img_path = :terms_response_7_img_path,
                terms_response_8_img_path = :terms_response_8_img_path,
                terms_response_9_img_path = :terms_response_9_img_path,
                terms_response_10_img_path = :terms_response_10_img_path,
                terms_response_1_img_string_base64_encoded = :terms_response_1_img_string_base64_encoded ,
                terms_response_2_img_string_base64_encoded = :terms_response_2_img_string_base64_encoded,
                terms_response_3_img_string_base64_encoded = :terms_response_3_img_string_base64_encoded,
                terms_response_4_img_string_base64_encoded = :terms_response_4_img_string_base64_encoded,
                terms_response_5_img_string_base64_encoded = :terms_response_5_img_string_base64_encoded,
                terms_response_6_img_string_base64_encoded = :terms_response_6_img_string_base64_encoded,
                terms_response_7_img_string_base64_encoded = :terms_response_7_img_string_base64_encoded,
                terms_response_8_img_string_base64_encoded = :terms_response_8_img_string_base64_encoded,
                terms_response_9_img_string_base64_encoded = :terms_response_9_img_string_base64_encoded,
                terms_response_10_img_string_base64_encoded = :terms_response_10_img_string_base64_encoded,

                assignment_pairs_definition_1 = :assignment_pairs_definition_1,
                assignment_pairs_definition_2 = :assignment_pairs_definition_2,
                assignment_pairs_definition_3 = :assignment_pairs_definition_3,
                assignment_pairs_definition_4 = :assignment_pairs_definition_4,
                assignment_pairs_definition_5 = :assignment_pairs_definition_5,
                assignment_pairs_definition_6 = :assignment_pairs_definition_6,
                assignment_pairs_definition_7 = :assignment_pairs_definition_7,
                assignment_pairs_definition_8 = :assignment_pairs_definition_8,
                assignment_pairs_definition_9 = :assignment_pairs_definition_9,
                assignment_pairs_definition_10 = :assignment_pairs_definition_10,
                assignment_pairs_term_1 = :assignment_pairs_term_1,
                assignment_pairs_term_2 = :assignment_pairs_term_2,
                assignment_pairs_term_3 = :assignment_pairs_term_3,
                assignment_pairs_term_4 = :assignment_pairs_term_4,
                assignment_pairs_term_5 = :assignment_pairs_term_5,
                assignment_pairs_term_6 = :assignment_pairs_term_6,
                assignment_pairs_term_7 = :assignment_pairs_term_7,
                assignment_pairs_term_8 = :assignment_pairs_term_8,
                assignment_pairs_term_9 = :assignment_pairs_term_9,
                assignment_pairs_term_10 = :assignment_pairs_term_10,
                assignment_pairs_1_pts = :assignment_pairs_1_pts ,
                assignment_pairs_2_pts = :assignment_pairs_2_pts ,
                assignment_pairs_3_pts = :assignment_pairs_3_pts ,
                assignment_pairs_4_pts = :assignment_pairs_4_pts ,
                assignment_pairs_5_pts = :assignment_pairs_5_pts ,
                assignment_pairs_6_pts = :assignment_pairs_6_pts ,
                assignment_pairs_7_pts = :assignment_pairs_7_pts ,
                assignment_pairs_8_pts = :assignment_pairs_8_pts ,
                assignment_pairs_9_pts = :assignment_pairs_9_pts ,
                assignment_pairs_10_pts = :assignment_pairs_10_pts ,

                picture_preview_pixel = :picture_preview_pixel ,


                description_img_name_1 = :description_img_name_1,
                description_img_data_1 = :description_img_data_1,
                description_img_path_1 = :description_img_path_1,

                description_img_name_2 = :description_img_name_2,
                description_img_data_2 = :description_img_data_2,
                description_img_path_2 = :description_img_path_2,

                description_img_name_3 = :description_img_name_3,
                description_img_data_3 = :description_img_data_3,
                description_img_path_3 = :description_img_path_3,

                test_time = :test_time,
                question_pool_tag = :question_pool_tag,
                question_author = :question_author
            
                WHERE oid = :oid""",
                {
                      'question_difficulty': self.mq_question_difficulty_entry.get(),
                      'question_category': self.mq_question_category_entry.get(),
                      'question_type': self.mq_question_type_entry.get(),
                      'question_title': self.mq_question_title_entry.get(),
                      'question_description_title': self.mq_question_description_title_entry.get(),

                      # The first part, "1.0" means that the input should be read from line one, character zero (ie: the very first character).
                      # END is an imported constant which is set to the string "end". The END part means to read until the end of the text box is reached.
                      # The only issue with this is that it actually adds a newline to our input. "
                      # "So, in order to fix it we should change END to end-1c(Thanks Bryan Oakley) The -1c deletes 1 character, while -2c would mean delete two characters, and so on."
                      'question_description_main': self.mq_question_description_main_entry.get("1.0", 'end-1c'),

                      'mix_answers': self.mq_mix_answers_box.get(),
                      'assignment_mode': self.selected_matching_option.get(),

                      'definitions_response_1_text': self.mq_definitions_var1_answer_entry.get(),
                      'definitions_response_2_text': self.mq_definitions_var2_answer_entry.get(),
                      'definitions_response_3_text': self.mq_definitions_var3_answer_entry.get(),
                      'definitions_response_4_text': self.mq_definitions_var4_answer_entry.get(),
                      'definitions_response_5_text': self.mq_definitions_var5_answer_entry.get(),
                      'definitions_response_6_text': self.mq_definitions_var6_answer_entry.get(),
                      'definitions_response_7_text': self.mq_definitions_var7_answer_entry.get(),
                      'definitions_response_8_text': self.mq_definitions_var8_answer_entry.get(),
                      'definitions_response_9_text': self.mq_definitions_var9_answer_entry.get(),
                      'definitions_response_10_text': self.mq_definitions_var10_answer_entry.get(),
                      'definitions_response_1_img_label': self.mq_definitions_var1_img_label_entry.get(),
                      'definitions_response_2_img_label': self.mq_definitions_var2_img_label_entry.get(),
                      'definitions_response_3_img_label': self.mq_definitions_var3_img_label_entry.get(),
                      'definitions_response_4_img_label': self.mq_definitions_var4_img_label_entry.get(),
                      'definitions_response_5_img_label': self.mq_definitions_var5_img_label_entry.get(),
                      'definitions_response_6_img_label': self.mq_definitions_var6_img_label_entry.get(),
                      'definitions_response_7_img_label': self.mq_definitions_var7_img_label_entry.get(),
                      'definitions_response_8_img_label': self.mq_definitions_var8_img_label_entry.get(),
                      'definitions_response_9_img_label': self.mq_definitions_var9_img_label_entry.get(),
                      'definitions_response_10_img_label': self.mq_definitions_var10_img_label_entry.get(),
                      'definitions_response_1_img_path': self.mq_definitions_var1_img_path_entry.get(),
                      'definitions_response_2_img_path': self.mq_definitions_var2_img_path_entry.get(),
                      'definitions_response_3_img_path': self.mq_definitions_var3_img_path_entry.get(),
                      'definitions_response_4_img_path': self.mq_definitions_var4_img_path_entry.get(),
                      'definitions_response_5_img_path': self.mq_definitions_var5_img_path_entry.get(),
                      'definitions_response_6_img_path': self.mq_definitions_var6_img_path_entry.get(),
                      'definitions_response_7_img_path': self.mq_definitions_var7_img_path_entry.get(),
                      'definitions_response_8_img_path': self.mq_definitions_var8_img_path_entry.get(),
                      'definitions_response_9_img_path': self.mq_definitions_var9_img_path_entry.get(),
                      'definitions_response_10_img_path': self.mq_definitions_var10_img_path_entry.get(),
                      'definitions_response_1_img_string_base64_encoded': self.mq_definitions_var1_img_data_entry.get(),
                      'definitions_response_2_img_string_base64_encoded': self.mq_definitions_var2_img_data_entry.get(),
                      'definitions_response_3_img_string_base64_encoded': self.mq_definitions_var3_img_data_entry.get(),
                      'definitions_response_4_img_string_base64_encoded': self.mq_definitions_var4_img_data_entry.get(),
                      'definitions_response_5_img_string_base64_encoded': self.mq_definitions_var5_img_data_entry.get(),
                      'definitions_response_6_img_string_base64_encoded': self.mq_definitions_var6_img_data_entry.get(),
                      'definitions_response_7_img_string_base64_encoded': self.mq_definitions_var7_img_data_entry.get(),
                      'definitions_response_8_img_string_base64_encoded': self.mq_definitions_var8_img_data_entry.get(),
                      'definitions_response_9_img_string_base64_encoded': self.mq_definitions_var9_img_data_entry.get(),
                      'definitions_response_10_img_string_base64_encoded': self.mq_definitions_var10_img_data_entry.get(),

                      'terms_response_1_text': self.mq_terms_var1_answer_entry.get(),
                      'terms_response_2_text': self.mq_terms_var2_answer_entry.get(),
                      'terms_response_3_text': self.mq_terms_var3_answer_entry.get(),
                      'terms_response_4_text': self.mq_terms_var4_answer_entry.get(),
                      'terms_response_5_text': self.mq_terms_var5_answer_entry.get(),
                      'terms_response_6_text': self.mq_terms_var6_answer_entry.get(),
                      'terms_response_7_text': self.mq_terms_var7_answer_entry.get(),
                      'terms_response_8_text': self.mq_terms_var8_answer_entry.get(),
                      'terms_response_9_text': self.mq_terms_var9_answer_entry.get(),
                      'terms_response_10_text': self.mq_terms_var10_answer_entry.get(),
                      'terms_response_1_img_label': self.mq_terms_var1_img_label_entry.get(),
                      'terms_response_2_img_label': self.mq_terms_var2_img_label_entry.get(),
                      'terms_response_3_img_label': self.mq_terms_var3_img_label_entry.get(),
                      'terms_response_4_img_label': self.mq_terms_var4_img_label_entry.get(),
                      'terms_response_5_img_label': self.mq_terms_var5_img_label_entry.get(),
                      'terms_response_6_img_label': self.mq_terms_var6_img_label_entry.get(),
                      'terms_response_7_img_label': self.mq_terms_var7_img_label_entry.get(),
                      'terms_response_8_img_label': self.mq_terms_var8_img_label_entry.get(),
                      'terms_response_9_img_label': self.mq_terms_var9_img_label_entry.get(),
                      'terms_response_10_img_label': self.mq_terms_var10_img_label_entry.get(),
                      'terms_response_1_img_path': self.mq_terms_var1_img_path_entry.get(),
                      'terms_response_2_img_path': self.mq_terms_var2_img_path_entry.get(),
                      'terms_response_3_img_path': self.mq_terms_var3_img_path_entry.get(),
                      'terms_response_4_img_path': self.mq_terms_var4_img_path_entry.get(),
                      'terms_response_5_img_path': self.mq_terms_var5_img_path_entry.get(),
                      'terms_response_6_img_path': self.mq_terms_var6_img_path_entry.get(),
                      'terms_response_7_img_path': self.mq_terms_var7_img_path_entry.get(),
                      'terms_response_8_img_path': self.mq_terms_var8_img_path_entry.get(),
                      'terms_response_9_img_path': self.mq_terms_var9_img_path_entry.get(),
                      'terms_response_10_img_path': self.mq_terms_var10_img_path_entry.get(),
                      'terms_response_1_img_string_base64_encoded': self.mq_terms_var1_img_data_entry.get(),
                      'terms_response_2_img_string_base64_encoded': self.mq_terms_var2_img_data_entry.get(),
                      'terms_response_3_img_string_base64_encoded': self.mq_terms_var3_img_data_entry.get(),
                      'terms_response_4_img_string_base64_encoded': self.mq_terms_var4_img_data_entry.get(),
                      'terms_response_5_img_string_base64_encoded': self.mq_terms_var5_img_data_entry.get(),
                      'terms_response_6_img_string_base64_encoded': self.mq_terms_var6_img_data_entry.get(),
                      'terms_response_7_img_string_base64_encoded': self.mq_terms_var7_img_data_entry.get(),
                      'terms_response_8_img_string_base64_encoded': self.mq_terms_var8_img_data_entry.get(),
                      'terms_response_9_img_string_base64_encoded': self.mq_terms_var9_img_data_entry.get(),
                      'terms_response_10_img_string_base64_encoded': self.mq_terms_var10_img_data_entry.get(),

                      'assignment_pairs_definition_1': self.mq_assignment_pairs_definitions_1_box.get(),
                      'assignment_pairs_definition_2': self.mq_assignment_pairs_definitions_2_box.get(),
                      'assignment_pairs_definition_3': self.mq_assignment_pairs_definitions_3_box.get(),
                      'assignment_pairs_definition_4': self.mq_assignment_pairs_definitions_4_box.get(),
                      'assignment_pairs_definition_5': self.mq_assignment_pairs_definitions_5_box.get(),
                      'assignment_pairs_definition_6': self.mq_assignment_pairs_definitions_6_box.get(),
                      'assignment_pairs_definition_7': self.mq_assignment_pairs_definitions_7_box.get(),
                      'assignment_pairs_definition_8': self.mq_assignment_pairs_definitions_8_box.get(),
                      'assignment_pairs_definition_9': self.mq_assignment_pairs_definitions_9_box.get(),
                      'assignment_pairs_definition_10': self.mq_assignment_pairs_definitions_10_box.get(),
                      'assignment_pairs_term_1': self.mq_assignment_pairs_terms_1_box.get(),
                      'assignment_pairs_term_2': self.mq_assignment_pairs_terms_2_box.get(),
                      'assignment_pairs_term_3': self.mq_assignment_pairs_terms_3_box.get(),
                      'assignment_pairs_term_4': self.mq_assignment_pairs_terms_4_box.get(),
                      'assignment_pairs_term_5': self.mq_assignment_pairs_terms_5_box.get(),
                      'assignment_pairs_term_6': self.mq_assignment_pairs_terms_6_box.get(),
                      'assignment_pairs_term_7': self.mq_assignment_pairs_terms_7_box.get(),
                      'assignment_pairs_term_8': self.mq_assignment_pairs_terms_8_box.get(),
                      'assignment_pairs_term_9': self.mq_assignment_pairs_terms_9_box.get(),
                      'assignment_pairs_term_10': self.mq_assignment_pairs_terms_10_box.get(),
                      'assignment_pairs_1_pts': self.mq_assignment_pairs_pts_1_entry.get(),
                      'assignment_pairs_2_pts': self.mq_assignment_pairs_pts_2_entry.get(),
                      'assignment_pairs_3_pts': self.mq_assignment_pairs_pts_3_entry.get(),
                      'assignment_pairs_4_pts': self.mq_assignment_pairs_pts_4_entry.get(),
                      'assignment_pairs_5_pts': self.mq_assignment_pairs_pts_5_entry.get(),
                      'assignment_pairs_6_pts': self.mq_assignment_pairs_pts_6_entry.get(),
                      'assignment_pairs_7_pts': self.mq_assignment_pairs_pts_7_entry.get(),
                      'assignment_pairs_8_pts': self.mq_assignment_pairs_pts_8_entry.get(),
                      'assignment_pairs_9_pts': self.mq_assignment_pairs_pts_9_entry.get(),
                      'assignment_pairs_10_pts': self.mq_assignment_pairs_pts_10_entry.get(),

                      'picture_preview_pixel': self.mq_picture_preview_pixel_entry.get(),

                      'description_img_name_1': self.mq_description_img_name_1,
                      'description_img_data_1': self.mq_description_img_data_1,
                      'description_img_path_1': self.mq_description_img_path_1,

                      'description_img_name_2': self.mq_description_img_name_2,
                      'description_img_data_2': self.mq_description_img_data_2,
                      'description_img_path_2': self.mq_description_img_path_2,

                      'description_img_name_3': self.mq_description_img_name_3,
                      'description_img_data_3': self.mq_description_img_data_3,
                      'description_img_path_3': self.mq_description_img_path_3,

                      'test_time': self.mq_test_time,
                      'question_pool_tag': self.mq_question_pool_tag_entry.get(),
                      'question_author': self.mq_question_author_entry.get(),
                      'oid': record_id
                  })
            
            
    def mq_delete_id_from_db(self):

        self.mq_delete_box_id = ""
        self.mq_delete_box_id = self.mq_delete_box.get()

        test_generator_modul_datenbanken_erstellen.Delete_Entry_from_Database.__init__(self, self.mq_delete_box_id, self.mq_question_type_name, self.mq_var_delete_all.get(), self.project_root_path, self.mq_db_entry_to_index_dict, self.database_zuordnungsfrage_path, "zuordnungsfrage_db.db", "zuordnungsfrage_table", "Zuordnungsfrage_DB_export_file.xlsx", "Zuordnungsfrage - Database")

        self.mq_delete_box.delete(0, END)
    
    def mq_clear_GUI(self):
        
        self.mq_question_difficulty_entry.delete(0, END)
        self.mq_question_category_entry.delete(0, END)
        #self.mq_question_type_entry.delete(0, END)

        self.mq_question_title_entry.delete(0, END)
        self.mq_question_description_title_entry.delete(0, END)
        self.mq_question_description_main_entry.delete('1.0', 'end-1c')
        
        # Eintragfelder für "DEFINITIONEN" leeren
        self.mq_definitions_var1_answer_entry.delete(0, END)
        self.mq_definitions_var2_answer_entry.delete(0, END)
        self.mq_definitions_var3_answer_entry.delete(0, END)
        self.mq_definitions_var4_answer_entry.delete(0, END)
        self.mq_definitions_var5_answer_entry.delete(0, END)
        self.mq_definitions_var6_answer_entry.delete(0, END)
        self.mq_definitions_var7_answer_entry.delete(0, END)
        self.mq_definitions_var8_answer_entry.delete(0, END)
        self.mq_definitions_var9_answer_entry.delete(0, END)
        self.mq_definitions_var10_answer_entry.delete(0, END)

        self.mq_definitions_var1_img_label_entry.delete(0, END)
        self.mq_definitions_var2_img_label_entry.delete(0, END)
        self.mq_definitions_var3_img_label_entry.delete(0, END)
        self.mq_definitions_var4_img_label_entry.delete(0, END)
        self.mq_definitions_var5_img_label_entry.delete(0, END)
        self.mq_definitions_var6_img_label_entry.delete(0, END)
        self.mq_definitions_var7_img_label_entry.delete(0, END)
        self.mq_definitions_var8_img_label_entry.delete(0, END)
        self.mq_definitions_var9_img_label_entry.delete(0, END)
        self.mq_definitions_var10_img_label_entry.delete(0, END)

        # Eintragfelder für "TERME" leeren
        self.mq_terms_var1_answer_entry.delete(0, END)
        self.mq_terms_var2_answer_entry.delete(0, END)
        self.mq_terms_var3_answer_entry.delete(0, END)
        self.mq_terms_var4_answer_entry.delete(0, END)
        self.mq_terms_var5_answer_entry.delete(0, END)
        self.mq_terms_var6_answer_entry.delete(0, END)
        self.mq_terms_var7_answer_entry.delete(0, END)
        self.mq_terms_var8_answer_entry.delete(0, END)
        self.mq_terms_var9_answer_entry.delete(0, END)
        self.mq_terms_var10_answer_entry.delete(0, END)

        self.mq_terms_var1_img_label_entry.delete(0, END)
        self.mq_terms_var2_img_label_entry.delete(0, END)
        self.mq_terms_var3_img_label_entry.delete(0, END)
        self.mq_terms_var4_img_label_entry.delete(0, END)
        self.mq_terms_var5_img_label_entry.delete(0, END)
        self.mq_terms_var6_img_label_entry.delete(0, END)
        self.mq_terms_var7_img_label_entry.delete(0, END)
        self.mq_terms_var8_img_label_entry.delete(0, END)
        self.mq_terms_var9_img_label_entry.delete(0, END)
        self.mq_terms_var10_img_label_entry.delete(0, END)

        self.mq_assignment_pairs_definitions_1_box.delete(0, "end")
        self.mq_assignment_pairs_definitions_2_box.delete(0, "end")
        self.mq_assignment_pairs_definitions_3_box.delete(0, "end")
        self.mq_assignment_pairs_definitions_4_box.delete(0, "end")
        self.mq_assignment_pairs_definitions_5_box.delete(0, "end")
        self.mq_assignment_pairs_definitions_6_box.delete(0, "end")
        self.mq_assignment_pairs_definitions_7_box.delete(0, "end")
        self.mq_assignment_pairs_definitions_8_box.delete(0, "end")
        self.mq_assignment_pairs_definitions_9_box.delete(0, "end")
        self.mq_assignment_pairs_definitions_10_box.delete(0, "end")

        self.mq_assignment_pairs_terms_1_box.delete(0, "end")
        self.mq_assignment_pairs_terms_2_box.delete(0, "end")
        self.mq_assignment_pairs_terms_3_box.delete(0, "end")
        self.mq_assignment_pairs_terms_4_box.delete(0, "end")
        self.mq_assignment_pairs_terms_5_box.delete(0, "end")
        self.mq_assignment_pairs_terms_6_box.delete(0, "end")
        self.mq_assignment_pairs_terms_7_box.delete(0, "end")
        self.mq_assignment_pairs_terms_8_box.delete(0, "end")
        self.mq_assignment_pairs_terms_9_box.delete(0, "end")
        self.mq_assignment_pairs_terms_10_box.delete(0, "end")




class Create_Zuordnungsfrage_Questions(Zuordnungsfrage):
    def __init__(self, db_entry_to_index_dict, ids_in_entry_box, question_type_test_or_pool, pool_img_dir, ilias_id_pool_qpl_dir, xml_read_qti_template_path, xml_qti_output_file_path, xml_qpl_output_file_path, max_id_pool_qti_xml, max_id, taxonomy_file_question_pool):


        self.mq_db_entry_to_index_dict = db_entry_to_index_dict
        self.mq_test_entry_splitted = ids_in_entry_box.split(",")
        self.qti_file_path_output = xml_qti_output_file_path

        self.zuordnungsfrage_pool_qpl_file_path_output = xml_qpl_output_file_path
        self.mq_mytree = ET.parse(xml_read_qti_template_path)
        self.mq_myroot = self.mq_mytree.getroot()
        self.question_type_test_or_pool = question_type_test_or_pool
        self.zuordnungsfrage_pool_img_file_path = pool_img_dir           # Wird nur bei Erstellung eines Fragen-Pool verwendet. Ordnername wird erst bei Laufzeit erstellt)

        self.all_entries_from_db_list = []
        self.number_of_entrys = []

        self.mq_question_pool_id_list = []
        self.mq_question_title_list = []

        self.mq_ilias_id_pool_qpl_dir = ilias_id_pool_qpl_dir
        self.mq_file_max_id = max_id
        self.mq_taxonomy_file_question_pool = taxonomy_file_question_pool
        self.mq_ilias_id_pool_qti_xml = max_id_pool_qti_xml



        self.assignment_pairs_definitions_terms_to_id_dict = {"Definition 1": 0, "Definition 2": 1, "Definition 3": 2, "Definition 4": 3, "Definition 5": 4,
                                                              "Definition 6": 5, "Definition 7": 6, "Definition 8": 7, "Definition 9": 8, "Definition 10": 9,

                                                              "Term 1": 10, "Term 2": 11, "Term 3": 12, "Term 4": 13, "Term 5": 14,
                                                              "Term 6": 15, "Term 7": 16, "Term 8": 17, "Term 9": 18, "Term 10": 19
                                                        }

        print("\n")


        if self.question_type_test_or_pool == "question_test":
            print("ZUORDNUNGSFRAGE: ILIAS-TEST WIRD ERSTELLT...  ID: " + str(ids_in_entry_box))

        else:
            print("ZUORDNUNGSFRAGE: ILIAS-POOL WIRD ERSTELLT...  ID: " + str(ids_in_entry_box))



        # Mit MQ_Datenbank verknüpfen
        connect_mq_db = sqlite3.connect(self.database_zuordnungsfrage_path)
        cursor = connect_mq_db.cursor()

        # Prüfen ob alle Einträge generiert werden sollen (checkbox gesetzt)
        if self.mq_var_create_question_pool_all_check.get() == 1:
            conn = sqlite3.connect(self.database_zuordnungsfrage_path)
            c = conn.cursor()
            c.execute("SELECT *, oid FROM singlechoice_table")

            mq_db_records = c.fetchall()

            for mq_db_record in mq_db_records:
                self.all_entries_from_db_list.append(int(mq_db_record[len(mq_db_record) - 1]))

            self.string_temp = ','.join(map(str, self.all_entries_from_db_list))
            self.mq_test_entry_splitted = self.string_temp.split(",")

            # Eintrag mit ID "1" entspricht der Vorlage und soll nicht mit erstellt werden
            #self.mq_test_entry_splitted.pop(0)

        
        
        
        
        # Sämtliche Datenbank Einträge auslesen mit der entsprechenden "oid" (Datenbank ID)
        # Datenbank ID wird automatimqh bei einem neuen Eintrag erstellt (fortlaufend) und kann nicht beeinflusst werden
        cursor.execute("SELECT *, oid FROM zuordnungsfrage_table")
        mq_db_records = cursor.fetchall()

        for i in range(len(self.mq_test_entry_splitted)):
            for mq_db_record in mq_db_records:
                if str(mq_db_record[len(mq_db_record) - 1]) == self.mq_test_entry_splitted[i]:
                    for t in range(len(mq_db_record)):
                        if mq_db_record[self.mq_db_entry_to_index_dict['question_type']].lower() == self.mq_question_type_name.lower():

                            self.mq_question_difficulty                                 = mq_db_record[self.mq_db_entry_to_index_dict['question_difficulty']]
                            self.mq_question_category                                   = mq_db_record[self.mq_db_entry_to_index_dict['question_category']]
                            self.mq_question_type                                       = mq_db_record[self.mq_db_entry_to_index_dict['question_type']]
                            self.mq_question_title                                      = mq_db_record[self.mq_db_entry_to_index_dict['question_title']].replace('&', "&amp;")
                            self.mq_question_description_title                          = mq_db_record[self.mq_db_entry_to_index_dict['question_description_title']].replace('&', "&amp;")
                            self.mq_question_description_main                           = mq_db_record[self.mq_db_entry_to_index_dict['question_description_main']].replace('&', "&amp;")

                            self.mq_mix_answers                                         = mq_db_record[self.mq_db_entry_to_index_dict['mix_answers']]
                            self.mq_assignment_mode                                     = mq_db_record[self.mq_db_entry_to_index_dict['assignment_mode']]

                            self.mq_definitions_response_1_text                         = mq_db_record[self.mq_db_entry_to_index_dict['definitions_response_1_text']].replace('&', "&amp;")
                            self.mq_definitions_response_2_text	                        = mq_db_record[self.mq_db_entry_to_index_dict['definitions_response_2_text']].replace('&', "&amp;")
                            self.mq_definitions_response_3_text	                        = mq_db_record[self.mq_db_entry_to_index_dict['definitions_response_3_text']].replace('&', "&amp;")
                            self.mq_definitions_response_4_text	                        = mq_db_record[self.mq_db_entry_to_index_dict['definitions_response_4_text']].replace('&', "&amp;")
                            self.mq_definitions_response_5_text	                        = mq_db_record[self.mq_db_entry_to_index_dict['definitions_response_5_text']].replace('&', "&amp;")
                            self.mq_definitions_response_6_text	                        = mq_db_record[self.mq_db_entry_to_index_dict['definitions_response_6_text']].replace('&', "&amp;")
                            self.mq_definitions_response_7_text	                        = mq_db_record[self.mq_db_entry_to_index_dict['definitions_response_7_text']].replace('&', "&amp;")
                            self.mq_definitions_response_8_text	                        = mq_db_record[self.mq_db_entry_to_index_dict['definitions_response_8_text']].replace('&', "&amp;")
                            self.mq_definitions_response_9_text	                        = mq_db_record[self.mq_db_entry_to_index_dict['definitions_response_9_text']].replace('&', "&amp;")
                            self.mq_definitions_response_10_text	                    = mq_db_record[self.mq_db_entry_to_index_dict['definitions_response_10_text']].replace('&', "&amp;")
                            self.mq_definitions_response_1_img_label                    = mq_db_record[self.mq_db_entry_to_index_dict['definitions_response_1_img_label']]
                            self.mq_definitions_response_2_img_label                    = mq_db_record[self.mq_db_entry_to_index_dict['definitions_response_2_img_label']]
                            self.mq_definitions_response_3_img_label                    = mq_db_record[self.mq_db_entry_to_index_dict['definitions_response_3_img_label']]
                            self.mq_definitions_response_4_img_label                    = mq_db_record[self.mq_db_entry_to_index_dict['definitions_response_4_img_label']]
                            self.mq_definitions_response_5_img_label                    = mq_db_record[self.mq_db_entry_to_index_dict['definitions_response_5_img_label']]
                            self.mq_definitions_response_6_img_label                    = mq_db_record[self.mq_db_entry_to_index_dict['definitions_response_6_img_label']]
                            self.mq_definitions_response_7_img_label                    = mq_db_record[self.mq_db_entry_to_index_dict['definitions_response_7_img_label']]
                            self.mq_definitions_response_8_img_label                    = mq_db_record[self.mq_db_entry_to_index_dict['definitions_response_8_img_label']]
                            self.mq_definitions_response_9_img_label                    = mq_db_record[self.mq_db_entry_to_index_dict['definitions_response_9_img_label']]
                            self.mq_definitions_response_10_img_label                   = mq_db_record[self.mq_db_entry_to_index_dict['definitions_response_10_img_label']]
                            self.mq_definitions_response_1_img_path                     = mq_db_record[self.mq_db_entry_to_index_dict['definitions_response_1_img_path']]
                            self.mq_definitions_response_2_img_path                     = mq_db_record[self.mq_db_entry_to_index_dict['definitions_response_2_img_path']]
                            self.mq_definitions_response_3_img_path                     = mq_db_record[self.mq_db_entry_to_index_dict['definitions_response_3_img_path']]
                            self.mq_definitions_response_4_img_path                     = mq_db_record[self.mq_db_entry_to_index_dict['definitions_response_4_img_path']]
                            self.mq_definitions_response_5_img_path                     = mq_db_record[self.mq_db_entry_to_index_dict['definitions_response_5_img_path']]
                            self.mq_definitions_response_6_img_path                     = mq_db_record[self.mq_db_entry_to_index_dict['definitions_response_6_img_path']]
                            self.mq_definitions_response_7_img_path                     = mq_db_record[self.mq_db_entry_to_index_dict['definitions_response_7_img_path']]
                            self.mq_definitions_response_8_img_path                     = mq_db_record[self.mq_db_entry_to_index_dict['definitions_response_8_img_path']]
                            self.mq_definitions_response_9_img_path                     = mq_db_record[self.mq_db_entry_to_index_dict['definitions_response_9_img_path']]
                            self.mq_definitions_response_10_img_path                    = mq_db_record[self.mq_db_entry_to_index_dict['definitions_response_10_img_path']]
                            self.mq_definitions_response_1_img_string_base64_encoded    = mq_db_record[self.mq_db_entry_to_index_dict['definitions_response_1_img_string_base64_encoded']]
                            self.mq_definitions_response_2_img_string_base64_encoded    = mq_db_record[self.mq_db_entry_to_index_dict['definitions_response_2_img_string_base64_encoded']]
                            self.mq_definitions_response_3_img_string_base64_encoded    = mq_db_record[self.mq_db_entry_to_index_dict['definitions_response_3_img_string_base64_encoded']]
                            self.mq_definitions_response_4_img_string_base64_encoded    = mq_db_record[self.mq_db_entry_to_index_dict['definitions_response_4_img_string_base64_encoded']]
                            self.mq_definitions_response_5_img_string_base64_encoded    = mq_db_record[self.mq_db_entry_to_index_dict['definitions_response_5_img_string_base64_encoded']]
                            self.mq_definitions_response_6_img_string_base64_encoded    = mq_db_record[self.mq_db_entry_to_index_dict['definitions_response_6_img_string_base64_encoded']]
                            self.mq_definitions_response_7_img_string_base64_encoded    = mq_db_record[self.mq_db_entry_to_index_dict['definitions_response_7_img_string_base64_encoded']]
                            self.mq_definitions_response_8_img_string_base64_encoded    = mq_db_record[self.mq_db_entry_to_index_dict['definitions_response_8_img_string_base64_encoded']]
                            self.mq_definitions_response_9_img_string_base64_encoded    = mq_db_record[self.mq_db_entry_to_index_dict['definitions_response_9_img_string_base64_encoded']]
                            self.mq_definitions_response_10_img_string_base64_encoded   = mq_db_record[self.mq_db_entry_to_index_dict['definitions_response_10_img_string_base64_encoded']]

                            self.mq_terms_response_1_text                               = mq_db_record[self.mq_db_entry_to_index_dict['terms_response_1_text']].replace('&', "&amp;")
                            self.mq_terms_response_2_text	                            = mq_db_record[self.mq_db_entry_to_index_dict['terms_response_2_text']].replace('&', "&amp;")
                            self.mq_terms_response_3_text	                            = mq_db_record[self.mq_db_entry_to_index_dict['terms_response_3_text']].replace('&', "&amp;")
                            self.mq_terms_response_4_text	                            = mq_db_record[self.mq_db_entry_to_index_dict['terms_response_4_text']].replace('&', "&amp;")
                            self.mq_terms_response_5_text	                            = mq_db_record[self.mq_db_entry_to_index_dict['terms_response_5_text']].replace('&', "&amp;")
                            self.mq_terms_response_6_text	                            = mq_db_record[self.mq_db_entry_to_index_dict['terms_response_6_text']].replace('&', "&amp;")
                            self.mq_terms_response_7_text	                            = mq_db_record[self.mq_db_entry_to_index_dict['terms_response_7_text']].replace('&', "&amp;")
                            self.mq_terms_response_8_text	                            = mq_db_record[self.mq_db_entry_to_index_dict['terms_response_8_text']].replace('&', "&amp;")
                            self.mq_terms_response_9_text	                            = mq_db_record[self.mq_db_entry_to_index_dict['terms_response_9_text']].replace('&', "&amp;")
                            self.mq_terms_response_10_text	                            = mq_db_record[self.mq_db_entry_to_index_dict['terms_response_10_text']].replace('&', "&amp;")
                            self.mq_terms_response_1_img_label                          = mq_db_record[self.mq_db_entry_to_index_dict['terms_response_1_img_label']]
                            self.mq_terms_response_2_img_label                          = mq_db_record[self.mq_db_entry_to_index_dict['terms_response_2_img_label']]
                            self.mq_terms_response_3_img_label                          = mq_db_record[self.mq_db_entry_to_index_dict['terms_response_3_img_label']]
                            self.mq_terms_response_4_img_label                          = mq_db_record[self.mq_db_entry_to_index_dict['terms_response_4_img_label']]
                            self.mq_terms_response_5_img_label                          = mq_db_record[self.mq_db_entry_to_index_dict['terms_response_5_img_label']]
                            self.mq_terms_response_6_img_label                          = mq_db_record[self.mq_db_entry_to_index_dict['terms_response_6_img_label']]
                            self.mq_terms_response_7_img_label                          = mq_db_record[self.mq_db_entry_to_index_dict['terms_response_7_img_label']]
                            self.mq_terms_response_8_img_label                          = mq_db_record[self.mq_db_entry_to_index_dict['terms_response_8_img_label']]
                            self.mq_terms_response_9_img_label                          = mq_db_record[self.mq_db_entry_to_index_dict['terms_response_9_img_label']]
                            self.mq_terms_response_10_img_label                         = mq_db_record[self.mq_db_entry_to_index_dict['terms_response_10_img_label']]
                            self.mq_terms_response_1_img_path                           = mq_db_record[self.mq_db_entry_to_index_dict['terms_response_1_img_path']]
                            self.mq_terms_response_2_img_path                           = mq_db_record[self.mq_db_entry_to_index_dict['terms_response_2_img_path']]
                            self.mq_terms_response_3_img_path                           = mq_db_record[self.mq_db_entry_to_index_dict['terms_response_3_img_path']]
                            self.mq_terms_response_4_img_path                           = mq_db_record[self.mq_db_entry_to_index_dict['terms_response_4_img_path']]
                            self.mq_terms_response_5_img_path                           = mq_db_record[self.mq_db_entry_to_index_dict['terms_response_5_img_path']]
                            self.mq_terms_response_6_img_path                           = mq_db_record[self.mq_db_entry_to_index_dict['terms_response_6_img_path']]
                            self.mq_terms_response_7_img_path                           = mq_db_record[self.mq_db_entry_to_index_dict['terms_response_7_img_path']]
                            self.mq_terms_response_8_img_path                           = mq_db_record[self.mq_db_entry_to_index_dict['terms_response_8_img_path']]
                            self.mq_terms_response_9_img_path                           = mq_db_record[self.mq_db_entry_to_index_dict['terms_response_9_img_path']]
                            self.mq_terms_response_10_img_path                          = mq_db_record[self.mq_db_entry_to_index_dict['terms_response_10_img_path']]
                            self.mq_terms_response_1_img_string_base64_encoded          = mq_db_record[self.mq_db_entry_to_index_dict['terms_response_1_img_string_base64_encoded']]
                            self.mq_terms_response_2_img_string_base64_encoded          = mq_db_record[self.mq_db_entry_to_index_dict['terms_response_2_img_string_base64_encoded']]
                            self.mq_terms_response_3_img_string_base64_encoded          = mq_db_record[self.mq_db_entry_to_index_dict['terms_response_3_img_string_base64_encoded']]
                            self.mq_terms_response_4_img_string_base64_encoded          = mq_db_record[self.mq_db_entry_to_index_dict['terms_response_4_img_string_base64_encoded']]
                            self.mq_terms_response_5_img_string_base64_encoded          = mq_db_record[self.mq_db_entry_to_index_dict['terms_response_5_img_string_base64_encoded']]
                            self.mq_terms_response_6_img_string_base64_encoded          = mq_db_record[self.mq_db_entry_to_index_dict['terms_response_6_img_string_base64_encoded']]
                            self.mq_terms_response_7_img_string_base64_encoded          = mq_db_record[self.mq_db_entry_to_index_dict['terms_response_7_img_string_base64_encoded']]
                            self.mq_terms_response_8_img_string_base64_encoded          = mq_db_record[self.mq_db_entry_to_index_dict['terms_response_8_img_string_base64_encoded']]
                            self.mq_terms_response_9_img_string_base64_encoded          = mq_db_record[self.mq_db_entry_to_index_dict['terms_response_9_img_string_base64_encoded']]
                            self.mq_terms_response_10_img_string_base64_encoded         = mq_db_record[self.mq_db_entry_to_index_dict['terms_response_10_img_string_base64_encoded']]

                            self.mq_assignment_pairs_definition_1                       = mq_db_record[self.mq_db_entry_to_index_dict['assignment_pairs_definition_1']]
                            self.mq_assignment_pairs_definition_2                       = mq_db_record[self.mq_db_entry_to_index_dict['assignment_pairs_definition_2']]
                            self.mq_assignment_pairs_definition_3                       = mq_db_record[self.mq_db_entry_to_index_dict['assignment_pairs_definition_3']]
                            self.mq_assignment_pairs_definition_4                       = mq_db_record[self.mq_db_entry_to_index_dict['assignment_pairs_definition_4']]
                            self.mq_assignment_pairs_definition_5                       = mq_db_record[self.mq_db_entry_to_index_dict['assignment_pairs_definition_5']]
                            self.mq_assignment_pairs_definition_6                       = mq_db_record[self.mq_db_entry_to_index_dict['assignment_pairs_definition_6']]
                            self.mq_assignment_pairs_definition_7                       = mq_db_record[self.mq_db_entry_to_index_dict['assignment_pairs_definition_7']]
                            self.mq_assignment_pairs_definition_8                       = mq_db_record[self.mq_db_entry_to_index_dict['assignment_pairs_definition_8']]
                            self.mq_assignment_pairs_definition_9                       = mq_db_record[self.mq_db_entry_to_index_dict['assignment_pairs_definition_9']]
                            self.mq_assignment_pairs_definition_10                      = mq_db_record[self.mq_db_entry_to_index_dict['assignment_pairs_definition_10']]
                            self.mq_assignment_pairs_term_1                             = mq_db_record[self.mq_db_entry_to_index_dict['assignment_pairs_term_1']]
                            self.mq_assignment_pairs_term_2                             = mq_db_record[self.mq_db_entry_to_index_dict['assignment_pairs_term_2']]
                            self.mq_assignment_pairs_term_3                             = mq_db_record[self.mq_db_entry_to_index_dict['assignment_pairs_term_3']]
                            self.mq_assignment_pairs_term_4                             = mq_db_record[self.mq_db_entry_to_index_dict['assignment_pairs_term_4']]
                            self.mq_assignment_pairs_term_5                             = mq_db_record[self.mq_db_entry_to_index_dict['assignment_pairs_term_5']]
                            self.mq_assignment_pairs_term_6                             = mq_db_record[self.mq_db_entry_to_index_dict['assignment_pairs_term_6']]
                            self.mq_assignment_pairs_term_7                             = mq_db_record[self.mq_db_entry_to_index_dict['assignment_pairs_term_7']]
                            self.mq_assignment_pairs_term_8                             = mq_db_record[self.mq_db_entry_to_index_dict['assignment_pairs_term_8']]
                            self.mq_assignment_pairs_term_9                             = mq_db_record[self.mq_db_entry_to_index_dict['assignment_pairs_term_9']]
                            self.mq_assignment_pairs_term_10                            = mq_db_record[self.mq_db_entry_to_index_dict['assignment_pairs_term_10']]
                            self.mq_assignment_pairs_1_pts	                            = mq_db_record[self.mq_db_entry_to_index_dict['assignment_pairs_1_pts']]
                            self.mq_assignment_pairs_2_pts	                            = mq_db_record[self.mq_db_entry_to_index_dict['assignment_pairs_2_pts']]
                            self.mq_assignment_pairs_3_pts	                            = mq_db_record[self.mq_db_entry_to_index_dict['assignment_pairs_3_pts']]
                            self.mq_assignment_pairs_4_pts	                            = mq_db_record[self.mq_db_entry_to_index_dict['assignment_pairs_4_pts']]
                            self.mq_assignment_pairs_5_pts	                            = mq_db_record[self.mq_db_entry_to_index_dict['assignment_pairs_5_pts']]
                            self.mq_assignment_pairs_6_pts	                            = mq_db_record[self.mq_db_entry_to_index_dict['assignment_pairs_6_pts']]
                            self.mq_assignment_pairs_7_pts	                            = mq_db_record[self.mq_db_entry_to_index_dict['assignment_pairs_7_pts']]
                            self.mq_assignment_pairs_8_pts	                            = mq_db_record[self.mq_db_entry_to_index_dict['assignment_pairs_8_pts']]
                            self.mq_assignment_pairs_9_pts	                            = mq_db_record[self.mq_db_entry_to_index_dict['assignment_pairs_9_pts']]
                            self.mq_assignment_pairs_10_pts	                            = mq_db_record[self.mq_db_entry_to_index_dict['assignment_pairs_10_pts']]

                            self.mq_picture_preview_pixel                               = mq_db_record[self.mq_db_entry_to_index_dict['picture_preview_pixel']]

                            self.mq_description_img_name_1	                            = mq_db_record[self.mq_db_entry_to_index_dict['description_img_name_1']]
                            self.mq_description_img_data_1	                            = mq_db_record[self.mq_db_entry_to_index_dict['description_img_data_1']]
                            self.mq_description_img_path_1	                            = mq_db_record[self.mq_db_entry_to_index_dict['description_img_path_1']]

                            self.mq_description_img_name_2	                            = mq_db_record[self.mq_db_entry_to_index_dict['description_img_name_2']]
                            self.mq_description_img_data_2	                            = mq_db_record[self.mq_db_entry_to_index_dict['description_img_data_2']]
                            self.mq_description_img_path_2	                            = mq_db_record[self.mq_db_entry_to_index_dict['description_img_path_2']]

                            self.mq_description_img_name_3	                            = mq_db_record[self.mq_db_entry_to_index_dict['description_img_name_3']]
                            self.mq_description_img_data_3	                            = mq_db_record[self.mq_db_entry_to_index_dict['description_img_data_3']]
                            self.mq_description_img_path_3	                            = mq_db_record[self.mq_db_entry_to_index_dict['description_img_path_3']]


                            self.mq_test_time	                                        = mq_db_record[self.mq_db_entry_to_index_dict['test_time']]
                            self.mq_var_number	                                        = mq_db_record[self.mq_db_entry_to_index_dict['var_number']]
                            self.mq_res_number	                                        = mq_db_record[self.mq_db_entry_to_index_dict['res_number']]

                            self.mq_question_pool_tag                                   = mq_db_record[self.mq_db_entry_to_index_dict['question_pool_tag']]
                            self.mq_question_author                                     = mq_db_record[self.mq_db_entry_to_index_dict['question_author']].replace('&', "&amp;")

            Create_Zuordnungsfrage_Questions.mq_question_structure(self, i)



    def mq_question_structure(self, id_nr):
        """Diese Funktion wandelt die SQL-Einträge in die .xml um, welche anschließend in ILIAS eingespielt werden kann"""


        # VARIABLEN
        self.mq_response_counter = 0    #wird verwendet zu zählen, wieviele Anworten pro Frage verwendet werden. Bei einer neuer Antwort -> +1
        self.mq_question_description_main = test_generator_modul_taxonomie_und_textformatierung.Textformatierung.format_description_text_in_xml(self, self.mq_var_use_latex_on_text_check.get(), self.mq_question_description_main)



        # Verbindung zur mq-Datenank
        mq_connect = sqlite3.connect(self.database_zuordnungsfrage_path)
        mq_cursor = mq_connect.cursor()

        # Alle Einträge auslesen
        mq_cursor.execute("SELECT *, oid FROM zuordnungsfrage_table")
        mq_db_records = mq_cursor.fetchall()



        for mq_db_record in mq_db_records:

            if str(mq_db_record[len(mq_db_record)-1]) == self.mq_test_entry_splitted[id_nr]:

                test_generator_modul_ilias_test_struktur.Additional_Funtions.add_dir_for_images(self, self.mq_description_img_name_1, self.mq_description_img_data_1, id_nr, self.question_type_test_or_pool, self.zuordnungsfrage_test_img_file_path, self.zuordnungsfrage_pool_img_file_path)
                test_generator_modul_ilias_test_struktur.Additional_Funtions.add_dir_for_images(self, self.mq_description_img_name_2, self.mq_description_img_data_2, id_nr, self.question_type_test_or_pool, self.zuordnungsfrage_test_img_file_path, self.zuordnungsfrage_pool_img_file_path)
                test_generator_modul_ilias_test_struktur.Additional_Funtions.add_dir_for_images(self, self.mq_description_img_name_3, self.mq_description_img_data_3, id_nr, self.question_type_test_or_pool, self.zuordnungsfrage_test_img_file_path, self.zuordnungsfrage_pool_img_file_path)


                 # Aufbau für  Fragenstruktur "TEST"
                if self.question_type_test_or_pool == "question_test":
                    # XML Struktur aus XML Datei festlegen. Muss nur einmal angelegt werden
                    questestinterop = ET.Element('questestinterop')
                    assessment = ET.SubElement(questestinterop, 'assessment')
                    section = ET.SubElement(assessment, 'section')
                    item = ET.SubElement(section, 'item')

                # Aufbau für  Fragenstruktur "POOL"
                else:
                    # XML Struktur aus XML Datei festlegen. Muss nur einmal angelegt werden
                    questestinterop = ET.Element('questestinterop')
                    item = ET.SubElement(questestinterop, 'item')

                # Zusatz für Taxonomie-Einstellungen
                test_generator_modul_ilias_test_struktur.Additional_Funtions.set_taxonomy_for_question(self,
                                                                                                           id_nr,
                                                                                                           self.number_of_entrys,
                                                                                                           item,
                                                                                                           self.zuordnungsfrage_pool_qpl_file_path_template,
                                                                                                           self.zuordnungsfrage_pool_qpl_file_path_output)



                # Struktur für den Zuordnungsfrage - Fragen/Antworten Teil  -- HEADER
                # Muss für jede Frage neu angelegt/hinzugefügt werden
                qticomment = ET.SubElement(item, 'qticomment')
                duration = ET.SubElement(item, 'duration')
                itemmetadata = ET.SubElement(item, 'itemmetadata')
                presentation = ET.SubElement(item, 'presentation')
                resprocessing = ET.SubElement(item, 'resprocessing')

                # Struktur für den Zuordnungsfrage - Fragen/Antworten Teil  -- MAIN
                # Muss für jede Frage neu angelegt/hinzugefügt werden
                flow = ET.SubElement(presentation, 'flow')
                question_description_material = ET.SubElement(flow, 'material')
                question_description_mattext = ET.SubElement(question_description_material, 'mattext')
                response_grp = ET.SubElement(flow, 'response_grp')
                render_choice = ET.SubElement(response_grp, 'render_choice')

                qtimetadata = ET.SubElement(itemmetadata, 'qtimetadata')
                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')


                ### ------------------------------------------------------- XML Einträge mit Werten füllen

                # Fragen-Titel -- "item title" in xml
                item_ident_nr = format(id_nr, "06")
                item.set('ident', "il_0_qst_" + str(item_ident_nr))
                item.set('title', self.mq_question_title)
                item.set('maxattempts', "0")

                # Fragen-Titel Beschreibung
                qticomment.text = self.mq_question_description_title

                # Testdauer -- "duration" in xml
                # wird keine Testzeit eingetragen, wird 1h vorausgewählt
                duration.text = self.mq_test_time
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
                fieldentry.text = "MATCHING QUESTION"
                # -----------------------------------------------------------------------AUTHOR
                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "AUTHOR"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
                fieldentry.text = self.mq_question_author
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
                # -----------------------------------------------------------------------SHUFFLE
                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "shuffle"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
                fieldentry.text = str(self.mq_mix_answers)
                # -----------------------------------------------------------------------THUMB_GEOMETRY
                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "thumb_geometry"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
                fieldentry.text = str(self.mq_picture_preview_pixel)
                # -----------------------------------------------------------------------MATCHING MODE
                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "matching_mode"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
                fieldentry.text = str(self.mq_assignment_mode)


                # Fragentitel einsetzen -- "presentation label" in xml
                presentation.set('label', self.mq_question_title)

                # Fragen-Text (Format) einsetzen -- "mattext_texttype" in xml -- Gibt das Format des Textes an
                question_description_mattext.set('texttype', "text/html")

                # Fragen-Text (Text) einsetzen   -- "mattext_texttype" in xml -- Gibt die eigentliche Fragen-Beschreibung an
                # Wenn Bild enthalten ist, dann in Fragenbeschreibung einbetten
                if self.mq_description_img_data_1 != "":

                    with open('il_0_mob_TEST.png', 'wb') as image_file:
                        image_file.write(self.mq_description_img_data_1)

                    self.mq_file_image_raw = Image.open('il_0_mob_TEST.png')
                    self.mq_file_image_size_width, self.mq_file_image_size_height = self.mq_file_image_raw.size

                    question_description_mattext.text = "<p>" + self.mq_question_description_main + "</p>" + "<p><img height=\"" + str(self.mq_file_image_size_height) + "\" src=\"il_0_mob_000000" + str(id_nr) + "\" width=\"" + str(self.mq_file_image_size_width) + "\" /></p>"

                    matimage = ET.SubElement(question_description_material, 'matimage')
                    matimage.set('label', "il_0_mob_000000" + str(id_nr))  # Object -> Filename
                    matimage.set('uri', "objects/il_0_mob_000000" + str(id_nr) + "/" + self.mq_description_img_name_1 + ".png")


                else:
                    question_description_mattext.text = "<p>" + self.mq_question_description_main + "</p>"


                # "MQ --> Matching Question Identifier für xml datei
                response_grp.set('ident', "MQ")
                response_grp.set('rcardinality', "Multiple")
                render_choice.set('shuffle', "Yes")



                self.mq_number_of_terms_used = []

                if self.mq_assignment_pairs_term_1 != "":
                    self.mq_number_of_terms_used.append(self.assignment_pairs_definitions_terms_to_id_dict[self.mq_assignment_pairs_term_1])
                if self.mq_assignment_pairs_term_2 != "":
                    self.mq_number_of_terms_used.append(self.assignment_pairs_definitions_terms_to_id_dict[self.mq_assignment_pairs_term_2])
                if self.mq_assignment_pairs_term_3 != "":
                    self.mq_number_of_terms_used.append(self.assignment_pairs_definitions_terms_to_id_dict[self.mq_assignment_pairs_term_3])
                if self.mq_assignment_pairs_term_4 != "":
                    self.mq_number_of_terms_used.append(self.assignment_pairs_definitions_terms_to_id_dict[self.mq_assignment_pairs_term_4])
                if self.mq_assignment_pairs_term_5 != "":
                    self.mq_number_of_terms_used.append(self.assignment_pairs_definitions_terms_to_id_dict[self.mq_assignment_pairs_term_5])
                if self.mq_assignment_pairs_term_6 != "":
                    self.mq_number_of_terms_used.append(self.assignment_pairs_definitions_terms_to_id_dict[self.mq_assignment_pairs_term_6])
                if self.mq_assignment_pairs_term_7 != "":
                    self.mq_number_of_terms_used.append(self.assignment_pairs_definitions_terms_to_id_dict[self.mq_assignment_pairs_term_7])
                if self.mq_assignment_pairs_term_8 != "":
                    self.mq_number_of_terms_used.append(self.assignment_pairs_definitions_terms_to_id_dict[self.mq_assignment_pairs_term_8])
                if self.mq_assignment_pairs_term_9 != "":
                    self.mq_number_of_terms_used.append(self.assignment_pairs_definitions_terms_to_id_dict[self.mq_assignment_pairs_term_9])
                if self.mq_assignment_pairs_term_10 != "":
                    self.mq_number_of_terms_used.append(self.assignment_pairs_definitions_terms_to_id_dict[self.mq_assignment_pairs_term_10])

                self.mq_number_of_terms_used_string = str(self.mq_number_of_terms_used)
                self.mq_number_of_terms_used_string = self.mq_number_of_terms_used_string[1:-1]




                #Antworten erstellen
                # Antworten erstellen
                Create_Zuordnungsfrage_Questions.mq_question_answer_structure_definitions(self, self.mq_definitions_response_1_text, self.mq_definitions_response_1_img_path, self.mq_definitions_response_1_img_string_base64_encoded, render_choice, "0", self.mq_number_of_terms_used_string)
                Create_Zuordnungsfrage_Questions.mq_question_answer_structure_definitions(self, self.mq_definitions_response_2_text, self.mq_definitions_response_2_img_path, self.mq_definitions_response_2_img_string_base64_encoded, render_choice, "1", self.mq_number_of_terms_used_string)
                Create_Zuordnungsfrage_Questions.mq_question_answer_structure_definitions(self, self.mq_definitions_response_3_text, self.mq_definitions_response_3_img_path, self.mq_definitions_response_3_img_string_base64_encoded, render_choice, "2", self.mq_number_of_terms_used_string)
                Create_Zuordnungsfrage_Questions.mq_question_answer_structure_definitions(self, self.mq_definitions_response_4_text, self.mq_definitions_response_4_img_path, self.mq_definitions_response_4_img_string_base64_encoded, render_choice, "3", self.mq_number_of_terms_used_string)
                Create_Zuordnungsfrage_Questions.mq_question_answer_structure_definitions(self, self.mq_definitions_response_5_text, self.mq_definitions_response_5_img_path, self.mq_definitions_response_5_img_string_base64_encoded, render_choice, "4", self.mq_number_of_terms_used_string)
                Create_Zuordnungsfrage_Questions.mq_question_answer_structure_definitions(self, self.mq_definitions_response_6_text, self.mq_definitions_response_6_img_path, self.mq_definitions_response_6_img_string_base64_encoded, render_choice, "5", self.mq_number_of_terms_used_string)
                Create_Zuordnungsfrage_Questions.mq_question_answer_structure_definitions(self, self.mq_definitions_response_7_text, self.mq_definitions_response_7_img_path, self.mq_definitions_response_7_img_string_base64_encoded, render_choice, "6", self.mq_number_of_terms_used_string)
                Create_Zuordnungsfrage_Questions.mq_question_answer_structure_definitions(self, self.mq_definitions_response_8_text, self.mq_definitions_response_8_img_path, self.mq_definitions_response_8_img_string_base64_encoded, render_choice, "7", self.mq_number_of_terms_used_string)
                Create_Zuordnungsfrage_Questions.mq_question_answer_structure_definitions(self, self.mq_definitions_response_9_text, self.mq_definitions_response_9_img_path, self.mq_definitions_response_9_img_string_base64_encoded, render_choice, "8", self.mq_number_of_terms_used_string)
                Create_Zuordnungsfrage_Questions.mq_question_answer_structure_definitions(self, self.mq_definitions_response_10_text, self.mq_definitions_response_10_img_path, self.mq_definitions_response_10_img_string_base64_encoded, render_choice, "9", self.mq_number_of_terms_used_string)

                Create_Zuordnungsfrage_Questions.mq_question_answer_structure_terms(self, self.mq_terms_response_1_text, self.mq_terms_response_1_img_path, self.mq_terms_response_1_img_string_base64_encoded,render_choice, "10")
                Create_Zuordnungsfrage_Questions.mq_question_answer_structure_terms(self, self.mq_terms_response_2_text, self.mq_terms_response_2_img_path, self.mq_terms_response_2_img_string_base64_encoded,render_choice, "11")
                Create_Zuordnungsfrage_Questions.mq_question_answer_structure_terms(self, self.mq_terms_response_3_text, self.mq_terms_response_3_img_path, self.mq_terms_response_3_img_string_base64_encoded,render_choice, "12")
                Create_Zuordnungsfrage_Questions.mq_question_answer_structure_terms(self, self.mq_terms_response_4_text, self.mq_terms_response_4_img_path, self.mq_terms_response_4_img_string_base64_encoded,render_choice, "13")
                Create_Zuordnungsfrage_Questions.mq_question_answer_structure_terms(self, self.mq_terms_response_5_text, self.mq_terms_response_5_img_path, self.mq_terms_response_5_img_string_base64_encoded,render_choice, "14")
                Create_Zuordnungsfrage_Questions.mq_question_answer_structure_terms(self, self.mq_terms_response_6_text, self.mq_terms_response_6_img_path, self.mq_terms_response_6_img_string_base64_encoded,render_choice, "15")
                Create_Zuordnungsfrage_Questions.mq_question_answer_structure_terms(self, self.mq_terms_response_7_text, self.mq_terms_response_7_img_path, self.mq_terms_response_7_img_string_base64_encoded,render_choice, "16")
                Create_Zuordnungsfrage_Questions.mq_question_answer_structure_terms(self, self.mq_terms_response_8_text, self.mq_terms_response_8_img_path, self.mq_terms_response_8_img_string_base64_encoded,render_choice, "17")
                Create_Zuordnungsfrage_Questions.mq_question_answer_structure_terms(self, self.mq_terms_response_9_text, self.mq_terms_response_9_img_path, self.mq_terms_response_9_img_string_base64_encoded,render_choice, "18")
                Create_Zuordnungsfrage_Questions.mq_question_answer_structure_terms(self, self.mq_terms_response_10_text, self.mq_terms_response_10_img_path, self.mq_terms_response_10_img_string_base64_encoded,render_choice, "19")

                Create_Zuordnungsfrage_Questions.mq_question_answer_structure_assignment_pairs(self, self.mq_assignment_pairs_definition_1, self.mq_assignment_pairs_term_1, self.mq_assignment_pairs_1_pts, resprocessing, item)
                Create_Zuordnungsfrage_Questions.mq_question_answer_structure_assignment_pairs(self, self.mq_assignment_pairs_definition_2, self.mq_assignment_pairs_term_2, self.mq_assignment_pairs_2_pts, resprocessing, item)
                Create_Zuordnungsfrage_Questions.mq_question_answer_structure_assignment_pairs(self, self.mq_assignment_pairs_definition_3, self.mq_assignment_pairs_term_3, self.mq_assignment_pairs_3_pts, resprocessing, item)
                Create_Zuordnungsfrage_Questions.mq_question_answer_structure_assignment_pairs(self, self.mq_assignment_pairs_definition_4, self.mq_assignment_pairs_term_4, self.mq_assignment_pairs_4_pts, resprocessing, item)
                Create_Zuordnungsfrage_Questions.mq_question_answer_structure_assignment_pairs(self, self.mq_assignment_pairs_definition_5, self.mq_assignment_pairs_term_5, self.mq_assignment_pairs_5_pts, resprocessing, item)
                Create_Zuordnungsfrage_Questions.mq_question_answer_structure_assignment_pairs(self, self.mq_assignment_pairs_definition_6, self.mq_assignment_pairs_term_6, self.mq_assignment_pairs_6_pts, resprocessing, item)
                Create_Zuordnungsfrage_Questions.mq_question_answer_structure_assignment_pairs(self, self.mq_assignment_pairs_definition_7, self.mq_assignment_pairs_term_7, self.mq_assignment_pairs_7_pts, resprocessing, item)
                Create_Zuordnungsfrage_Questions.mq_question_answer_structure_assignment_pairs(self, self.mq_assignment_pairs_definition_8, self.mq_assignment_pairs_term_8, self.mq_assignment_pairs_8_pts, resprocessing, item)
                Create_Zuordnungsfrage_Questions.mq_question_answer_structure_assignment_pairs(self, self.mq_assignment_pairs_definition_9, self.mq_assignment_pairs_term_9, self.mq_assignment_pairs_9_pts, resprocessing, item)
                Create_Zuordnungsfrage_Questions.mq_question_answer_structure_assignment_pairs(self, self.mq_assignment_pairs_definition_10, self.mq_assignment_pairs_term_10, self.mq_assignment_pairs_10_pts, resprocessing, item)



                # Wenn es sich um einen ILIAS-Test handelt, beinhaltet die XML eine Struktur mit mehreren "Zweigen"
                # Der letzte "Zweig" --> "len(self.mq_myroot[0]) - 1" (beschreibt das letze Fach) beinhaltet die eigentlichen Fragen
                if self.question_type_test_or_pool == "question_test":
                    self.mq_myroot[0][len(self.mq_myroot[0]) - 1].append(item)

                # Wenn es sich um einen ILIAS-Pool handelt, beinhaltet die XML keine Struktur
                # Die Frage kann einfach angehangen werden
                else:
                    self.mq_myroot.append(item)


                self.mq_mytree.write(self.qti_file_path_output)
                print("Zuordnungsfrage erstellt! --> Titel: " + str(self.mq_question_title))


        mq_connect.commit()
        mq_connect.close()

        if self.question_type_test_or_pool == "question_pool":
            ######  Anpassung der Datei "qpl". Akualisierung des Dateinamens
            self.qpl_file = os.path.normpath(os.path.join(self.zuordnungsfrage_files_path,"mq_ilias_pool_abgabe", self.mq_ilias_id_pool_qpl_dir, self.mq_ilias_id_pool_qti_xml))

            self.mytree = ET.parse(self.qpl_file)
            self.myroot = self.mytree.getroot()

            for ident_id in self.myroot.iter('Identifier'):
                ident_id.set('Entry', "il_0_qpl_" + str(self.mq_file_max_id+1))
            self.mytree.write(self.qpl_file)

    ####################### QUESTION_ANSWER STRUCTURE #############################
    def mq_question_answer_structure_definitions(self, mq_definitions_response_var_text, mq_definitions_response_var_img_path, mq_definitions_response_var_img_string_base64_encoded, xml_render_choice, mq_definition_id, mq_number_of_terms_used):
        

        # Antworten für Definitionen
        if mq_definitions_response_var_text != "":
            response_label = ET.SubElement(xml_render_choice, 'response_label')
            question_answer_material = ET.SubElement(response_label, 'material')
            question_answer_mattext = ET.SubElement(question_answer_material, 'mattext')

            response_label.set('ident', str(mq_definition_id))
            response_label.set('match_max', "1")
            response_label.set('match_group', str(self.mq_number_of_terms_used))


            question_answer_mattext.set('texttype', "text/plain")
            question_answer_mattext.text = mq_definitions_response_var_text
            if mq_definitions_response_var_img_string_base64_encoded != "":
                question_answer_matimage = ET.SubElement(question_answer_material, 'matimage')

                if str(mq_definitions_response_var_img_path.rpartition('.')[-1]) == "jpg" or str(mq_definitions_response_var_img_path.rpartition('.')[-1]) == "jpeg":
                    question_answer_matimage.set('imagtype', "image/jpeg")
                elif str(mq_definitions_response_var_img_path.rpartition('.')[-1]) == "png":
                    question_answer_matimage.set('imagtype', "image/png")
                elif str(mq_definitions_response_var_img_path.rpartition('.')[-1]) == "gif":
                    question_answer_matimage.set('imagtype', "image/gif")
                else:
                    print("Bildformat ist nicht jpg/jpeg/png/gif und wird von ILIAS nicht unterstützt!")

                question_answer_matimage.set('label', mq_definitions_response_var_img_path.rpartition('/')[-1])
                question_answer_matimage.set('embedded', "base64")
                question_answer_matimage.text = str(mq_definitions_response_var_img_string_base64_encoded)

    def mq_question_answer_structure_terms(self, mq_terms_response_var_text, mq_terms_response_var_img_path, mq_terms_response_var_img_string_base64_encoded, xml_render_choice, mq_response_counter):

        #Antworten für Terme
        if mq_terms_response_var_text != "":


            response_label = ET.SubElement(xml_render_choice, 'response_label')
            question_answer_material = ET.SubElement(response_label, 'material')
            question_answer_mattext = ET.SubElement(question_answer_material, 'mattext')

            response_label.set('ident', str(mq_response_counter))

            question_answer_mattext.set('texttype', "text/plain")
            question_answer_mattext.text = mq_terms_response_var_text
            if mq_terms_response_var_img_string_base64_encoded != "":
                question_answer_matimage = ET.SubElement(question_answer_material, 'matimage')

                if str(mq_terms_response_var_img_path.rpartition('.')[-1]) == "jpg" or str(mq_terms_response_var_img_path.rpartition('.')[-1]) == "jpeg":
                    question_answer_matimage.set('imagtype', "image/jpeg")
                elif str(mq_terms_response_var_img_path.rpartition('.')[-1]) == "png":
                    question_answer_matimage.set('imagtype', "image/png")
                elif str(mq_terms_response_var_img_path.rpartition('.')[-1]) == "gif":
                    question_answer_matimage.set('imagtype', "image/gif")
                else:
                    print("Bildformat ist nicht jpg/jpeg/png/gif und wird von ILIAS nicht unterstützt!")

                question_answer_matimage.set('label', mq_terms_response_var_img_path.rpartition('/')[-1])
                question_answer_matimage.set('embedded', "base64")
                question_answer_matimage.text = str(mq_terms_response_var_img_string_base64_encoded)

    def mq_question_answer_structure_assignment_pairs(self, mq_assignment_pairs_definition_var, mq_assignment_pairs_term_var, mq_assignment_pairs_var_pts, xml_resprocessing, xml_item):

        if mq_assignment_pairs_term_var != "" and mq_assignment_pairs_definition_var != "":
            #Zuordnugspaare definieren
            respcondition = ET.SubElement(xml_resprocessing, 'respcondition')
            respcondition.set('continue', "Yes")
            outcomes = ET.SubElement(xml_resprocessing, 'outcomes')
            decvar = ET.SubElement(outcomes, 'decvar')
            conditionvar = ET.SubElement(respcondition, 'conditionvar')
            varsubset = ET.SubElement(conditionvar, 'varsubset')
            varsubset.set('respident', "MQ")  # MQ --> Matching Question Ident
            varsubset.text = str(self.assignment_pairs_definitions_terms_to_id_dict[mq_assignment_pairs_term_var]) + "," + str(self.assignment_pairs_definitions_terms_to_id_dict[mq_assignment_pairs_definition_var])  # ID der Antwort inkrementiert für jede Antwort

            setvar = ET.SubElement(respcondition, 'setvar')
            setvar.set('action', "Add")
            setvar.text = str(mq_assignment_pairs_var_pts)  # Punktevergabe für die Antwort
            displayfeedback = ET.SubElement(respcondition, 'displayfeedback')
            displayfeedback.set('feedbacktype', "Response")
            displayfeedback.set('linkrefid', "correct_" + str(self.assignment_pairs_definitions_terms_to_id_dict[mq_assignment_pairs_term_var]) + "_")

            # --------------------------------------------------------ZUSATZ FÜR ANTWORT

            itemfeedback = ET.SubElement(xml_item, 'itemfeedback')
            itemfeedback_flow_mat = ET.SubElement(itemfeedback, 'flow_mat')
            itemfeedback_material = ET.SubElement(itemfeedback_flow_mat, 'material')
            itemfeedback_mattext = ET.SubElement(itemfeedback_material, 'mattext')

            itemfeedback.set('ident', "correct_" + str(self.assignment_pairs_definitions_terms_to_id_dict[mq_assignment_pairs_term_var]) + "_" + str(self.assignment_pairs_definitions_terms_to_id_dict[mq_assignment_pairs_definition_var]))
            itemfeedback.set('view', "All")

class Create_Zuordnungsfrage_Test(Zuordnungsfrage):
    def __init__(self, entry_to_index_dict):

        """
        Ein ILIAS-Test besteht immer aus den beiden Dateien "*_qti_*.xml" und "*_tst_*.xml".
        Die "tst" beinhaltelt eine Auflistung der Fragen und den Test-Titel, sowie die Test-id
        Die "qti" beinhaltet die Test-Einstellungen und die eigentliche Beschreibung der einzelnen Fragen
        Dazu gehört die Fragenbeschreibung, Lösungen, Punkte, Bilder etc.

        _________________________________________________________________

        Beispiel für einen Test, bestehend aus 3 Fragen für die _tst_:
        ...
        ...
        Test-Titel: <Title Language="de">Zuordnungsfrage</Title>
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
        <assessment ident="il_0_tst_8869" title="Zuordnungsfrage">
        ...
        // diverse Test-Einstellungen //
        ...
        <item ident="il_0_qst_457015" title="Arbeitspunkt" maxattempts="0">                         -- Erste Frage
        // Fragenbeschreibung, Lösungen, Punktevergabe                                              -- Eigentliche Darstellung der Frage
        ...
        ...
        <item ident="il_0_qst_526726" title="Zuordnungsfrage Test" maxattempts="0">                    -- Zweite Frage
        // Fragenbeschreibung, Lösungen, Punktevergabe                                              -- Eigentliche Darstellung der Frage
        ...
        ...
        <item ident="il_0_qst_457016" title="Eigenschaften der Asynchronmaschine" maxattempts="0">  -- Dritte Frage
        // Fragenbeschreibung, Lösungen, Punktevergabe                                              -- Eigentliche Darstellung der Frage
        ...

        """

        self.mq_db_entry_to_index_dict = entry_to_index_dict

        test_generator_modul_ilias_test_struktur.Create_ILIAS_Test.__init__(self,
                                                                            self.mq_db_entry_to_index_dict,
                                                                            self.zuordnungsfrage_test_tst_file_path_template,
                                                                            self.zuordnungsfrage_test_tst_file_path_output,
                                                                            self.zuordnungsfrage_test_qti_file_path_template,
                                                                            self.zuordnungsfrage_test_qti_file_path_output,
                                                                            self.mq_ilias_test_title_entry.get(),
                                                                            self.create_zuordnungsfrage_test_entry.get(),
                                                                            self.mq_question_type_entry.get(),
                                                                            )




class Create_Zuordnungsfrage_Pool(Zuordnungsfrage):
    def __init__(self, entry_to_index_dict, var_create_all_questions):

        self.mq_entry_to_index_dict = entry_to_index_dict
        self.mq_var_create_question_pool_all = var_create_all_questions

        # Die __init__ wird bei einem Knopfdruck auf "ILIAS-Fragenpool erstellen" ausgeführt
        # Es werden XML-Dateien und Ordner mit einer aufsteigenden ID erstellt.
        test_generator_modul_ilias_test_struktur.Create_ILIAS_Pool.__init__(self,
                                                                            self.project_root_path,
                                                                            self.zuordnungsfrage_pool_directory_output,
                                                                            self.zuordnungsfrage_files_path_pool_output,
                                                                            self.zuordnungsfrage_pool_qti_file_path_template,
                                                                            self.mq_ilias_test_title_entry.get(),
                                                                            self.create_zuordnungsfrage_pool_entry.get(),
                                                                            self.mq_question_type_name,
                                                                            self.database_zuordnungsfrage_path,
                                                                            self.mq_database_table,
                                                                            self.mq_db_entry_to_index_dict,
                                                                            self.mq_var_create_question_pool_all
                                                                            )
        #shutil.make_archive("test", 'zip', self.zuordnungsfrage_pool_directory_output)


        print("\n ----> Erstellung Fragenpool abgeschlossen! <----")
