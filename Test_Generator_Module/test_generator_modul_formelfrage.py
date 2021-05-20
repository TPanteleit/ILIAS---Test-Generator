from tkinter import ttk
from tkinter import filedialog
from tkinter import *
import sqlite3                              #verwendet für mySQL Datenbank
import xml.etree.ElementTree as ET
from sympy import *
import os
import datetime                             # wird benötigt für "Test-Einstellungen benutzen"
from datetime import datetime               # wird benötigt für "delete all entrys?" ??
import pathlib
import shutil                               # zum kopieren und zippen von Dateien
from PIL import ImageTk, Image          # Zur Preview von ausgewählten Bildern
import pandas as pd
from pandas.core.reshape.util import cartesian_product
import numpy as np
import re
from functools import partial
import time
from tkinter import messagebox
import zipfile
import subprocess
from collections import Counter
from operator import itemgetter


### Eigene Dateien / Module
from Test_Generator_Module import test_generator_modul_datenbanken_anzeigen
from Test_Generator_Module import test_generator_modul_datenbanken_erstellen
from Test_Generator_Module import test_generator_modul_taxonomie_und_textformatierung
from Test_Generator_Module import test_generator_modul_ilias_test_struktur
from Test_Generator_Module import test_generator_modul_ilias_import_test_datei
from Test_Generator_Module import test_generator_modul_test_einstellungen
#from Test_Generator_Module import test_generator_modul_zeigerdiagramme

class Formelfrage:

    ############## SET IMAGE VARIABLES
    ############## DEFINE FORMELFRAGE PATHS
    ############## FRAMES
    # add_image_to_description_and_create_labels
    # add_image_to_description_and_delete_labels
    ############## BEARBEITUNGSDAUER
    # selected_hours
    # selected_minutes
    # selecteds_seconds
    ############## ÜBERSCHRIFTEN / LABELS FÜR EINGABEFELDER-MATRIX
    ############## EINGABEFELDER / ENTRYS FÜR EINGABEFELDER-MATRIX
    # answer_selected
    ############## AUSWAHL DER EINHEITEN FÜR VARIABLEN ---- DERZEIT NICHT AKTIV
    ############## ÜBERSCHRIFTEN / LABELS FÜR EINGABEFELDER-MATRIX
    ############## EINGABEFELDER / ENTRYS FÜR EINGABEFELDER-MATRIX
    ############## EINHEITEN FÜR ERGEBNISSE DERZEIT DEAKTIVIERT
    # result_selected
    #____ INIT end
    # ff_variable_show_or_remove
    # ff_result_show_or_remove
    # unit_table
    # ff_replace_character_in_xml_file
    # ff_calculate_value_range_function_in_GUI
    # ff_calculate_value_range_from_formula_in_GUI
    ############## DATENBANK FUNKTIONEN
    # ff_save_id_to_db
    # ff_load_id_from_db
    # ff_edit_id_from_db
    # ff_delete_id_from_db
    # ff_load_id_from_db
    # ff_clear_GUI



    def __init__(self, app, formelfrage_tab, project_root_path):





        self.formelfrage_tab = formelfrage_tab

############## SET QUESTION_TYPE SPECIFIC NAMES FOR DATABASE AND WORBOOK/SHEET
        # Name des Fragentyps
        self.ff_question_type_name = "formelfrage"

        # Name für Datenbank und Tabelle
        self.ff_database = "ilias_formelfrage_db.db"
        self.ff_database_table = "formelfrage_table"

        self.test_settings_database = "test_settings_profiles_db.db"
        self.test_settings_database_table = "my_profiles_table"
        self.test_settings_database_path = os.path.normpath(os.path.join(self.project_root_path, "Test_Generator_Datenbanken", self.test_settings_database))


        # Name für Tabellenkalulations-Datei und Tabelle
        self.ff_xlsx_workbook_name = "Formelfrage_DB_export_file"
        self.ff_xlsx_worksheet_name = "Formelfrage - Database"



        ############## SET IMAGE VARIABLES

        # Die Variablen müssen am Anfang des Programms gesetzt werden, um diese an andere Funktionen weitergeben zu können
        self.ff_description_img_name_1 = ""
        self.ff_description_img_name_2 = ""
        self.ff_description_img_name_3 = ""

        self.ff_description_img_data_1 = ""
        self.ff_description_img_data_2 = ""
        self.ff_description_img_data_3 = ""

        self.ff_description_img_path_1 = ""
        self.ff_description_img_path_2 = ""
        self.ff_description_img_path_3 = ""



############## DEFINE FORMELFRAGE PATHS

        # Pfad des Projekts und des FF-Moduls
        self.project_root_path = project_root_path
        self.formelfrage_files_path = os.path.normpath(os.path.join(self.project_root_path, "ILIAS-Formelfrage"))
        self.formelfrage_excel_vorlage = os.path.normpath(os.path.join(self.formelfrage_files_path, "ff_excel_vorlage", "ff_excel_vorlage.xlsx"))
        self.formelfrage_files_path_pool_output = os.path.normpath(os.path.join(self.formelfrage_files_path, "ff_ilias_pool_abgabe"))

        # Pfad für die Datenbank
        self.database_formelfrage_path = os.path.normpath(os.path.join(self.project_root_path, "Test_Generator_Datenbanken", self.ff_database))

        # Pfad für ILIAS-Test Vorlage
        self.formelfrage_test_qti_file_path_template = os.path.normpath(os.path.join(self.formelfrage_files_path, "ff_test_qti_und_tst_dateien_vorlage", "ilias_test_vorlage__qti__.xml"))
        self.formelfrage_test_tst_file_path_template = os.path.normpath(os.path.join(self.formelfrage_files_path, "ff_test_qti_und_tst_dateien_vorlage", "ilias_test_vorlage__tst__.xml"))


        # Pfad für ILIAS-Test Dateien (zum hochladen in ILIAS)
        self.formelfrage_test_qti_file_path_output = os.path.normpath(os.path.join(self.formelfrage_files_path, "ff_ilias_test_abgabe", "1604407426__0__tst_2040314", "1604407426__0__qti_2040314.xml"))
        self.formelfrage_test_tst_file_path_output = os.path.normpath(os.path.join(self.formelfrage_files_path, "ff_ilias_test_abgabe", "1604407426__0__tst_2040314", "1604407426__0__tst_2040314.xml"))
        self.formelfrage_test_img_file_path = os.path.normpath(os.path.join(self.formelfrage_files_path, "ff_ilias_test_abgabe", "1604407426__0__tst_2040314", "objects"))


        # Pfad für ILIAS-Pool Vorlage
        self.formelfrage_pool_qti_file_path_template = os.path.normpath(os.path.join(self.formelfrage_files_path, "ff_pool_qti_und_qpl_dateien_vorlage", "ilias_pool_vorlage__qti__.xml"))
        self.formelfrage_pool_qpl_file_path_template = os.path.normpath(os.path.join(self.formelfrage_files_path, "ff_pool_qti_und_qpl_dateien_vorlage", "ilias_pool_vorlage__qpl__.xml"))


        # Pfad für ILIAS-Pool Dateien (zum hochladen in ILIAS)
        # Die Pfade für die qti.xml und qpl.xml werden erst zur Laufzeit bestimmt.
        # Die Deklaration ist daher unter "class Create_Formelfrage_Pool"


###################### DATENBANK ENTRIES UND INDEX DICT ERSTELLEN  ###################


        # Dictionary aus zwei Listen erstellen
        self.ff_db_find_entries = []
        self.ff_db_find_indexes = []
        self.ff_db_column_names_list = []


        connect = sqlite3.connect(self.database_formelfrage_path)
        cursor = connect.execute('select * from ' + self.ff_database_table)

        self.ff_db_column_names_list = list(map(lambda x: x[0], cursor.description))
        self.ff_db_column_names_string = ', :'.join(self.ff_db_column_names_list)
        self.ff_db_column_names_string = ":" + self.ff_db_column_names_string


        for i in range(len(self.ff_db_column_names_list)):
            self.ff_db_find_indexes.append(i)

        """
        # Durch list(map(lambdax: x[0])) werden die Spaltennamen aus der DB ausgelesen
        cursor = conn.execute('select * from ' + self.ff_database_table)
        db_column_names_list = list(map(lambda x: x[0], cursor.description))
        db_column_names_string  = ', :'.join(db_column_names_list)
        db_column_names_string  = ":" + db_column_names_string
        """

        self.ff_db_entry_to_index_dict = dict(zip((self.ff_db_column_names_list), (self.ff_db_find_indexes)))



        connect.commit()
        connect.close()



############## FRAMES
        self.ff_frame_ilias_test_title = LabelFrame(self.formelfrage_tab, text="Testname & Autor", padx=5, pady=5)
        self.ff_frame_ilias_test_title.grid(row=0, column=0, padx=10, pady=10, sticky="NW")

        self.ff_frame = LabelFrame(self.formelfrage_tab, text="Formelfrage", padx=5, pady=5)
        self.ff_frame.grid(row=1, column=0, padx=10, pady=10, sticky="NW")

        self.ff_frame_question_attributes = LabelFrame(self.formelfrage_tab, text="Fragen Attribute", padx=5, pady=5)
        self.ff_frame_question_attributes.grid(row=2, column=0, padx=10, pady=10, sticky="NE")

        self.ff_frame_database = LabelFrame(self.formelfrage_tab, text="Formelfrage-Datenbank", padx=5, pady=5)
        self.ff_frame_database.grid(row=2, column=0, padx=10, pady=10, sticky="NW")

        self.ff_frame_create_formelfrage_test = LabelFrame(self.formelfrage_tab, text="FF-Test erstellen", padx=5, pady=5)
        self.ff_frame_create_formelfrage_test.grid(row=2, column=0, padx=10, pady=120, sticky="NE")

        self.ff_frame_test_settings = LabelFrame(self.formelfrage_tab, text="Test Einstellungen", padx=5, pady=5)
        self.ff_frame_test_settings.grid(row=0, column=0, padx=10, pady=10, sticky="NE")

        self.ff_frame_taxonomy_settings = LabelFrame(self.formelfrage_tab, text="Taxonomie Einstellungen", padx=5, pady=5)
        self.ff_frame_taxonomy_settings.grid(row=0, column=1, padx=10, pady=10, sticky="NW")

        self.ff_frame_question_description_functions = LabelFrame(self.formelfrage_tab, text="Fragentext Funktionen", padx=5, pady=5)
        self.ff_frame_question_description_functions.grid(row=1, column=1, padx=10, pady=10, sticky="NW")

        self.ff_frame_excel_import_export = LabelFrame(self.formelfrage_tab, text="Excel Import/Export", padx=5, pady=5)
        self.ff_frame_excel_import_export.grid(row=2, column=1, padx=10, pady=10, sticky="NW")

        self.ff_frame_calculate_value_range = LabelFrame(self.formelfrage_tab, text="Wertebereich berechnen", padx=5, pady=5)
        self.ff_frame_calculate_value_range.grid(row=1, column=1, padx=10, pady=10, sticky="SW")

        self.ff_frame_description_picture = LabelFrame(self.formelfrage_tab, text="Fragen-Text Bild", padx=5, pady=5)
        self.ff_frame_description_picture.grid(row=1, column=2, padx=10, pady=10, sticky="NW")

        self.ff_frame_vector_diagram = LabelFrame(self.formelfrage_tab, text="Zeigerdiagramme", padx=5, pady=5)
        #self.ff_frame_vector_diagram.grid(row=2, column=1, padx=10, pady=200, sticky="NW")



###################### "Testname & Autor" - FRAME   -------- LABELS / ENTRYS / BUTTONS  ################

        self.ff_ilias_test_title_label = Label(self.ff_frame_ilias_test_title, text="Name des Tests")
        self.ff_ilias_test_title_label.grid(row=0, column=0, sticky=W)

        self.ff_ilias_test_title_entry = Entry(self.ff_frame_ilias_test_title, width=60)
        self.ff_ilias_test_title_entry.grid(row=0, column=1, sticky=W, padx=30)

        self.ff_ilias_test_autor_label = Label(self.ff_frame_ilias_test_title, text="Autor")
        self.ff_ilias_test_autor_label.grid(row=1, column=0, sticky=W)

        self.ff_ilias_test_autor_entry = Entry(self.ff_frame_ilias_test_title, width=60)
        self.ff_ilias_test_autor_entry.grid(row=1, column=1, sticky=W, padx=30)

###################### TEST SETTINGS

        self.show_test_settings_formula_tab = Button(self.ff_frame_test_settings, text="Test Einstellungen",command=lambda: test_generator_modul_test_einstellungen.Test_Einstellungen_GUI.__init__(self, self.project_root_path, self.formelfrage_test_qti_file_path_output))
        self.show_test_settings_formula_tab.grid(row=0, column=0, pady=0, sticky=NE)



######################################



###################### "Fragen-Text Bild" - FRAME   -------- LABELS / ENTRYS / BUTTONS  ################

        # Hinzufügen Bild 1
        self.ff_var_use_image_1 = IntVar()
        self.ff_check_use_image_1_in_description = Checkbutton(self.ff_frame_question_description_functions, text="Bild 1 hochladen?", variable=self.ff_var_use_image_1, onvalue=1, offvalue=0)
        self.ff_check_use_image_1_in_description.deselect()
        self.ff_check_use_image_1_in_description.grid(row=5, column=0, sticky=W, padx=90, pady=(10, 0))

        # Hinzufügen Bild 2
        self.ff_var_use_image_2 = IntVar()
        self.ff_check_use_image_2_in_description = Checkbutton(self.ff_frame_question_description_functions, text="Bild 2 hochladen?", variable=self.ff_var_use_image_2, onvalue=1, offvalue=0)
        self.ff_check_use_image_2_in_description.deselect()
        self.ff_check_use_image_2_in_description.grid(row=6, column=0, sticky=W, padx=90)

        # Hinzufügen Bild 3
        self.ff_var_use_image_3 = IntVar()
        self.ff_check_use_image_3_in_description = Checkbutton(self.ff_frame_question_description_functions, text="Bild 3 hochladen?", variable=self.ff_var_use_image_3, onvalue=1, offvalue=0)
        self.ff_check_use_image_3_in_description.deselect()
        self.ff_check_use_image_3_in_description.grid(row=7, column=0, sticky=W, padx=90)

        # Buttons - Bild hinzufügen & Bild löschen
        self.ff_add_img_to_description_btn = Button(self.ff_frame_question_description_functions, text="Bild hinzufügen", command=lambda: ff_add_image_to_description_and_create_labels())
        self.ff_add_img_to_description_btn.grid(row=8, column=0, sticky=W, padx = 10, pady=(20,0))

        # Bild zum Fragentext hinzufügen
        def ff_add_image_to_description_and_create_labels():
            # Erstelle Labels
            self.ff_question_description_img_1_filename_label = Label(self.ff_frame_description_picture, text=self.ff_description_img_name_1)
            self.ff_question_description_img_2_filename_label = Label(self.ff_frame_description_picture, text=self.ff_description_img_name_2)
            self.ff_question_description_img_3_filename_label = Label(self.ff_frame_description_picture, text=self.ff_description_img_name_3)


            self.ff_description_img_name_1, self.ff_description_img_name_2, self.ff_description_img_name_3, self.ff_description_img_path_1, self.ff_description_img_path_2, self.ff_description_img_path_3, self.ff_question_description_img_1_filename_label, self.ff_question_description_img_2_filename_label, self.ff_question_description_img_3_filename_label = test_generator_modul_ilias_test_struktur.Additional_Funtions.add_image_to_description(
                    self,
                    self.project_root_path,
                    self.ff_var_use_image_1.get(),
                    self.ff_var_use_image_2.get(),
                    self.ff_var_use_image_3.get(),
                    self.ff_frame_description_picture,
                    self.ff_description_img_name_1,
                    self.ff_description_img_name_2,
                    self.ff_description_img_name_3,
                    self.ff_description_img_path_1,
                    self.ff_description_img_path_2,
                    self.ff_description_img_path_3,
                    )



        self.ff_remove_img_from_description_btn = Button(self.ff_frame_question_description_functions, text="Bild entfernen", command=lambda: ff_add_image_to_description_and_delete_labels())
        self.ff_remove_img_from_description_btn.grid(row=8, column=0, sticky=W, padx=120, pady=(20,0))

        # Bild aus Fragentext entfernen
        def ff_add_image_to_description_and_delete_labels():
            self.ff_description_img_name_1, self.ff_description_img_name_2, self.ff_description_img_name_3 = test_generator_modul_ilias_test_struktur.Additional_Funtions.delete_image_from_description(
                 self, self.ff_var_use_image_1.get(),
                 self.ff_var_use_image_2.get(),
                 self.ff_var_use_image_3.get(),
                 self.ff_question_description_img_1_filename_label,
                 self.ff_question_description_img_2_filename_label,
                 self.ff_question_description_img_3_filename_label,
                 self.ff_description_img_name_1,
                 self.ff_description_img_name_2,
                 self.ff_description_img_name_3,
            )



        ###################### "Taxonomie Einstellungen" - FRAME   -------- LABELS / ENTRYS / BUTTONS  ################
        self.ff_taxonomy_settings_btn = Button(self.ff_frame_taxonomy_settings, text="Taxonomie Einstellungen",command=lambda: test_generator_modul_taxonomie_und_textformatierung.Taxonomie.__init__(self))
        self.ff_taxonomy_settings_btn.grid(row=3, column=0, columnspan = 2, padx=10, sticky="W")



        self.ff_question_difficulty_label = Label(self.ff_frame_question_attributes, text="Schwierigkeit")
        self.ff_question_difficulty_label.grid(row=0, column=0, pady=5, padx=5, sticky=W)

        self.ff_question_difficulty_entry = Entry(self.ff_frame_question_attributes, width=15)
        self.ff_question_difficulty_entry.grid(row=0, column=1, pady=5, padx=5, sticky=W)

        self.ff_question_category_label = Label(self.ff_frame_question_attributes, text="Fragenkategorie")
        self.ff_question_category_label.grid(row=1, column=0, pady=5, padx=5, sticky=W)

        self.ff_question_category_entry = Entry(self.ff_frame_question_attributes, width=15)
        self.ff_question_category_entry.grid(row=1, column=1, pady=5, padx=5, sticky=W)

        self.ff_question_type_label = Label(self.ff_frame_question_attributes, text="Fragen-Typ")
        self.ff_question_type_label.grid(row=0, column=2, pady=5, padx=5, sticky=W)

        self.ff_question_type_entry = Entry(self.ff_frame_question_attributes, width=15)
        self.ff_question_type_entry.grid(row=0, column=3, pady=5, padx=5, sticky=W)
        self.ff_question_type_entry.insert(0, "Formelfrage")

        self.ff_question_pool_tag_label = Label(self.ff_frame_question_attributes, text="Pool-Tag")
        self.ff_question_pool_tag_label.grid(row=1, column=2, pady=5, padx=5, sticky=W)

        self.ff_question_pool_tag_entry = Entry(self.ff_frame_question_attributes, width=15)
        self.ff_question_pool_tag_entry.grid(row=1, column=3, pady=5, padx=5, sticky=W)

###################### "Wertebereich berechnen" - FRAME   -------- LABELS / ENTRYS / BUTTONS  ###################
        # Wertebereich berechnen für Formel aus Eingabefeld: formula 1
        self.ff_calculate_value_range_btn = Button(self.ff_frame_calculate_value_range, text="Wertebereich berechnen",command=lambda: Formelfrage.ff_calculate_value_range_function_in_GUI(self, "0"))
        self.ff_calculate_value_range_btn.grid(row=0, column=0, padx=0, sticky=W)

        # Label für Eingabefeld
        self.ff_calculate_value_range_id_label = Label(self.ff_frame_calculate_value_range, text="ID:")
        self.ff_calculate_value_range_id_label.grid(row=0, column=0, pady=5, padx=70, sticky=E)

        # Eingabefeld für ID
        self.ff_calculate_value_range_id_entry = Entry(self.ff_frame_calculate_value_range, width=10)
        self.ff_calculate_value_range_id_entry.grid(row=0, column=0, pady=5, padx=5, sticky=E)

        # Checkbox "Wertebereiche für Fragenpool berechnen?"
        self.ff_var_calculate_value_range_for_all_db_entries_check = IntVar()
        self.ff_calculate_value_range_from_db_entries = Checkbutton(self.ff_frame_calculate_value_range, text="Wertebereiche für alle DB Einträge berechnen?", variable=self.ff_var_calculate_value_range_for_all_db_entries_check, onvalue=1, offvalue=0)
        self.ff_calculate_value_range_from_db_entries.grid(row=1, column=0, sticky=W, pady=(10,0))


###################### "FF-Test erstellen" - FRAME   -------- LABELS / ENTRYS / BUTTONS  ###################

        # Button "Formelfrage-Test erstellen"
        self.create_formelfrage_test_btn = Button(self.ff_frame_create_formelfrage_test, text="FF-Test erstellen", command=lambda: Create_Formelfrage_Test.__init__(self, self.ff_db_entry_to_index_dict))
        self.create_formelfrage_test_btn.grid(row=0, column=0, sticky=W)
        self.create_formelfrage_test_entry = Entry(self.ff_frame_create_formelfrage_test, width=15)
        self.create_formelfrage_test_entry.grid(row=0, column=1, sticky=W, padx=0)



        # Checkbox "Test-Einstellungen verwenden?"
        self.ff_create_test_settings_label = Label(self.ff_frame_create_formelfrage_test, text="Test-Einstellungen verwenden?")
        self.ff_create_test_settings_label.grid(row=1, column=0, pady=5, padx=5, sticky=W)
        self.ff_var_create_test_settings_check = IntVar()
        self.ff_create_test_settings = Checkbutton(self.ff_frame_create_formelfrage_test, text="", variable=self.ff_var_create_test_settings_check, onvalue=1, offvalue=0, command=lambda: refresh_box_test_settings_profiles(self))
        self.ff_create_test_settings.grid(row=1, column=1, sticky=W)



        

        # Combobox Profile für Datenbank
        self.ff_profile_for_test_settings_value = []

        # Datenbank nach Profilen durchsuchen
        conn = sqlite3.connect(self.test_settings_database_path)
        c = conn.cursor()

        c.execute("SELECT *, oid FROM " + self.test_settings_database_table)
        profile_records = c.fetchall()

        # Loop through Results
        for profile_record in profile_records:
            self.ff_profile_for_test_settings_value.append(profile_record[0])

        conn.commit()
        conn.close()
        ###

        def ff_profile_selected(event):
            self.var = event

        self.ff_selected_profile_for_test_settings_box = ttk.Combobox(self.ff_frame_create_formelfrage_test, value=self.ff_profile_for_test_settings_value, width=8)
        self.ff_selected_profile_for_test_settings_box.bind("<<ComboboxSelected>>", ff_profile_selected)
        self.ff_selected_profile_for_test_settings_box.grid(row=1, column=1, sticky=W, padx=(22, 0))


        def refresh_box_test_settings_profiles(self):
            if self.ff_var_create_test_settings_check.get() == 1:
                self.ff_selected_profile_for_test_settings_box.grid_forget()

                # Combobox Profile für Datenbank
                self.ff_profile_for_test_settings_value = []

                # Datenbank nach Profilen durchsuchen
                conn = sqlite3.connect(self.test_settings_database_path)
                c = conn.cursor()

                c.execute("SELECT *, oid FROM " + self.test_settings_database_table)
                profile_records = c.fetchall()

                # Loop through Results
                for profile_record in profile_records:
                    self.ff_profile_for_test_settings_value.append(profile_record[0])

                self.ff_selected_profile_for_test_settings_box = ttk.Combobox(self.ff_frame_create_formelfrage_test, value=self.ff_profile_for_test_settings_value, width=8)
                self.ff_selected_profile_for_test_settings_box.bind("<<ComboboxSelected>>", ff_profile_selected)
                self.ff_selected_profile_for_test_settings_box.grid(row=1, column=1, sticky=W, padx=(22, 0))



        # Checkbox "Latex für Fragentext nutzen?"
        self.ff_use_latex_on_text_label = Label(self.ff_frame_create_formelfrage_test, text="Latex für Fragentext nutzen?")
        self.ff_use_latex_on_text_label.grid(row=2, column=0, sticky=W, padx=5)
        self.ff_var_use_latex_on_text_check = IntVar()
        self.ff_use_latex_on_text_check = Checkbutton(self.ff_frame_create_formelfrage_test, text="", variable=self.ff_var_use_latex_on_text_check, onvalue=1, offvalue=0)
        self.ff_use_latex_on_text_check.deselect()
        self.ff_use_latex_on_text_check.grid(row=2, column=1, sticky=W)




        # Checkbox "Alle Einträge aus der DB erzeugen?"
        self.ff_create_question_pool_all_label = Label(self.ff_frame_create_formelfrage_test, text="Alle Einträge aus der DB erzeugen?")
        self.ff_create_question_pool_all_label.grid(row=4, column=0, pady=(10,0), padx=5, sticky=W)
        self.ff_var_create_question_pool_all_check = IntVar()
        self.ff_create_question_pool_all = Checkbutton(self.ff_frame_create_formelfrage_test, text="", variable=self.ff_var_create_question_pool_all_check, onvalue=1, offvalue=0)
        #self.ff_var_create_question_pool_all_check.set(0)
        self.ff_create_question_pool_all.grid(row=4, column=1, sticky=W, pady=(10,0))

        # Checkbox "Mehrere Fragenpools Taxonomie getrennt erstellen?"
        self.ff_create_multiple_question_pools_from_tax_label = Label(self.ff_frame_create_formelfrage_test, text="Mehrere Fragenpools (Taxonomie getrennt) erstellen?")
        self.ff_create_multiple_question_pools_from_tax_label.grid(row=5, column=0, pady=(10,0), padx=5, sticky=W)
        self.ff_var_create_multiple_question_pools_from_tax_check = IntVar()
        self.ff_create_multiple_question_pools_from_tax = Checkbutton(self.ff_frame_create_formelfrage_test, text="", variable=self.ff_var_create_multiple_question_pools_from_tax_check, onvalue=1, offvalue=0)
        #self.ff_var_create_question_pool_all_check.set(0)
        self.ff_create_multiple_question_pools_from_tax.grid(row=5, column=1, sticky=W, pady=(10,0))

        # Checkbox "Taxonomie für getrennte Pools behalten?"
        self.ff_remove_pool_tags_for_tax_label = Label(self.ff_frame_create_formelfrage_test, text=" ---> Taxonomie für getrennte Pools \"löschen\"?")
        self.ff_remove_pool_tags_for_tax_label.grid(row=6, column=0, pady=(0,0), padx=5, sticky=W)
        self.ff_var_remove_pool_tags_for_tax_check = IntVar()
        self.ff_remove_pool_tags_for_tax = Checkbutton(self.ff_frame_create_formelfrage_test, text="", variable=self.ff_var_remove_pool_tags_for_tax_check, onvalue=1, offvalue=0)
        #self.ff_var_create_question_pool_all_check.set(0)
        self.ff_remove_pool_tags_for_tax.grid(row=6, column=1, sticky=W, pady=(0,0))





        # Button "Formelfrage-Fragenpool erstellen"
        self.create_formelfrage_pool_btn = Button(self.ff_frame_create_formelfrage_test, text="FF-Pool erstellen", command=lambda: Create_Formelfrage_Pool.__init__(self, self.ff_db_entry_to_index_dict, self.ff_var_create_question_pool_all_check.get(), self.ff_var_create_multiple_question_pools_from_tax_check.get()))
        self.create_formelfrage_pool_btn.grid(row=3, column=0, sticky=W, pady=(30,0))
        self.create_formelfrage_pool_entry = Entry(self.ff_frame_create_formelfrage_test, width=15)
        self.create_formelfrage_pool_entry.grid(row=3, column=1, sticky=W, padx=0, pady=(30,0))



###################### "Formelfrage-Datenbank" - FRAME   -------- LABELS / ENTRYS / BUTTONS  ###################

        self.ff_database_show_db_formelfrage_btn = Button(self.ff_frame_database, text="FF - Datenbank anzeigen", command=lambda: test_generator_modul_datenbanken_anzeigen.MainGUI.__init__(self, self.database_formelfrage_path, self.ff_database_table))
        self.ff_database_show_db_formelfrage_btn.grid(row=0, column=0, sticky=W, pady=5)

        self.ff_database_save_id_to_db_formelfrage_btn = Button(self.ff_frame_database, text="Speichern unter neuer ID", command=lambda: Formelfrage.ff_save_id_to_db(self, self.ff_database_table, self.ff_db_column_names_string))
        self.ff_database_save_id_to_db_formelfrage_btn.grid(row=1, column=0, sticky=W, pady=5)

        self.ff_database_delete_id_from_db_btn = Button(self.ff_frame_database, text="ID Löschen", command=lambda: Formelfrage.ff_delete_id_from_db(self))
        self.ff_database_delete_id_from_db_btn.grid(row=6, column=0, sticky=W, pady=5)
        self.ff_delete_box = Entry(self.ff_frame_database, width=10)
        self.ff_delete_box.grid(row=6, column=0, padx=80, sticky=W)

        self.ff_database_new_question_btn = Button(self.ff_frame_database, text="GUI Einträge leeren", command=lambda: Formelfrage.ff_clear_GUI(self))
        self.ff_database_new_question_btn.grid(row=8, column=0, sticky=W, pady=5)

        self.ff_database_edit_btn = Button(self.ff_frame_database, text="Aktuellen Eintrag editieren", command=lambda: Formelfrage.ff_edit_id_from_db(self))
        self.ff_database_edit_btn.grid(row=3, column=0, sticky=W, pady=5)


        self.ff_database_load_id_btn = Button(self.ff_frame_database, text="ID Laden", command=lambda: Formelfrage.ff_load_id_from_db(self, self.ff_db_entry_to_index_dict))
        self.ff_database_load_id_btn.grid(row=4, column=0, sticky=W, pady=(15,0))
        self.ff_load_box = Entry(self.ff_frame_database, width=10)
        self.ff_load_box.grid(row=4, column=0, sticky=W, padx=80, pady=(15,0))
        self.ff_hidden_edit_box_entry = Entry(self.ff_frame_database, width=10)

        # Checkbox - "Fragentext mit Highlighting?"
        self.ff_highlight_question_text_label = Label(self.ff_frame_database, text="Fragentext mit Highlighting?")
        self.ff_highlight_question_text_label.grid(row=5, column=0, pady=5, padx=5)

        self.ff_var_highlight_question_text = IntVar()
        self.ff_check_highlight_question_text = Checkbutton(self.ff_frame_database, text="", variable=self.ff_var_highlight_question_text, onvalue=1, offvalue=0)
        self.ff_check_highlight_question_text.deselect()
        self.ff_check_highlight_question_text.grid(row=5, column=0, sticky=E)


        # Checkbox - "Alle DB Einträge löschen?"
        self.ff_delete_all_label = Label(self.ff_frame_database, text="Alle DB Einträge löschen?")
        self.ff_delete_all_label.grid(row=7, column=0, pady=5, padx=5)

        self.ff_var_delete_all = IntVar()
        self.ff_check_delete_all = Checkbutton(self.ff_frame_database, text="", variable=self.ff_var_delete_all, onvalue=1, offvalue=0)
        self.ff_check_delete_all.deselect()
        self.ff_check_delete_all.grid(row=7, column=0, sticky=E)


###################### "Excel Import/Export" - FRAME   -------- LABELS / ENTRYS / BUTTONS  ###################




        # excel_import_btn
        self.ff_excel_import_to_db_formelfrage_btn = Button(self.ff_frame_excel_import_export, text="Excel-Datei importieren", command=lambda: test_generator_modul_datenbanken_erstellen.Import_Export_Database.excel_import_to_db(self, self.ff_question_type_name, self.ff_db_entry_to_index_dict, self.formelfrage_tab))
        self.ff_excel_import_to_db_formelfrage_btn.grid(row=0, column=1, sticky=W, pady=5, padx=10)

        # excel_export_btn
        self.ff_excel_export_to_xlsx_formelfrage_btn = Button(self.ff_frame_excel_import_export, text="Datenbank exportieren",command=lambda: test_generator_modul_datenbanken_erstellen.Import_Export_Database.excel_export_to_xlsx(self, self.project_root_path, self.ff_db_entry_to_index_dict, self.database_formelfrage_path, self.ff_database, self.ff_database_table, self.ff_xlsx_workbook_name, self.ff_xlsx_worksheet_name))
        self.ff_excel_export_to_xlsx_formelfrage_btn.grid(row=1, column=1, sticky=W, pady=5, padx=10)


        # ILIAS_testfile_import
        self.ff_import_ilias_testfile_btn = Button(self.ff_frame_excel_import_export, text="ILIAS-Datei importieren",command=lambda: test_generator_modul_ilias_import_test_datei.Import_ILIAS_Datei_in_DB.__init__(self, self.project_root_path))
        self.ff_import_ilias_testfile_btn.grid(row=2, column=1, sticky=W, pady=(20,0), padx=10)




###################### "Fragentext Funktionen" - FRAME   -------- LABELS / ENTRYS / BUTTONS  ###################
        self.add_latex_term_btn = Button(self.ff_frame_question_description_functions, text="Text \"Latex\"", command=lambda: test_generator_modul_taxonomie_und_textformatierung.Textformatierung.text_latex(self, self.ff_question_description_main_entry))
        self.add_latex_term_btn.grid(row=1, column=0, padx=10, sticky="W")

        self.set_text_sub_btn = Button(self.ff_frame_question_description_functions, text="Text \"Tiefgestellt\"", command=lambda: test_generator_modul_taxonomie_und_textformatierung.Textformatierung.text_sub(self, self.ff_question_description_main_entry))
        self.set_text_sub_btn .grid(row=2, column=0, padx=10, pady=(10, 0), sticky="W")

        self.set_text_sup_btn = Button(self.ff_frame_question_description_functions, text="Text \"Hochgestellt\"", command=lambda: test_generator_modul_taxonomie_und_textformatierung.Textformatierung.text_sup(self, self.ff_question_description_main_entry))
        self.set_text_sup_btn.grid(row=3, column=0, padx=10, sticky="W")

        self.set_text_italic_btn = Button(self.ff_frame_question_description_functions, text="Text \"Kursiv\"", command=lambda: test_generator_modul_taxonomie_und_textformatierung.Textformatierung.text_italic(self, self.ff_question_description_main_entry))
        self.set_text_italic_btn.grid(row=4, column=0, padx=10, sticky="W")

        self.set_postion_for_picture_1_btn = Button(self.ff_frame_question_description_functions, text="Pos. Bild 1", command=lambda: test_generator_modul_taxonomie_und_textformatierung.Textformatierung.set_position_for_picture_1(self, self.ff_question_description_main_entry))
        self.set_postion_for_picture_1_btn.grid(row=5, column=0, padx=10, pady=(10, 0), sticky="W")

        self.set_postion_for_picture_2_btn = Button(self.ff_frame_question_description_functions, text="Pos. Bild 2", command=lambda: test_generator_modul_taxonomie_und_textformatierung.Textformatierung.set_position_for_picture_2(self, self.ff_question_description_main_entry))
        self.set_postion_for_picture_2_btn.grid(row=6, column=0, padx=10,  sticky="W")

        self.set_postion_for_picture_3_btn = Button(self.ff_frame_question_description_functions, text="Pos. Bild 3", command=lambda: test_generator_modul_taxonomie_und_textformatierung.Textformatierung.set_position_for_picture_3(self, self.ff_question_description_main_entry))
        self.set_postion_for_picture_3_btn.grid(row=7, column=0, padx=10,  sticky="W")

###################### "Zeigerdiagramme" - FRAME   -------- LABELS / ENTRYS / BUTTONS  ###################

        self.ff_vector_diagram_type =["Serienschaltung: RL", "Serienschaltung: RC", "Serienschaltung: RLC"]
        self.ff_vector_diagram_type_box = ttk.Combobox(self.ff_frame_vector_diagram, value=self.ff_vector_diagram_type, width=20)
        self.ff_vector_diagram_type_box.grid(row=0, column=0, sticky=W, pady=10)


        self.ff_vector_diagram_U_label = Label(self.ff_frame_vector_diagram, text='Wert für U:')
        self.ff_vector_diagram_U_label.grid(row=1, column=0, sticky=W)
        self.ff_vector_diagram_U_entry = Entry(self.ff_frame_vector_diagram,  width=10)
        self.ff_vector_diagram_U_entry.grid(row=1, column=0, sticky=W, padx=70)

        self.ff_vector_diagram_R_label = Label(self.ff_frame_vector_diagram, text='Wert für R:')
        self.ff_vector_diagram_R_label.grid(row=2, column=0, sticky=W)
        self.ff_vector_diagram_R_entry = Entry(self.ff_frame_vector_diagram,  width=10)
        self.ff_vector_diagram_R_entry.grid(row=2, column=0, sticky=W, padx=70)

        self.ff_vector_diagram_L_label = Label(self.ff_frame_vector_diagram, text='Wert für L:')
        self.ff_vector_diagram_L_label.grid(row=3, column=0, sticky=W)
        self.ff_vector_diagram_L_entry = Entry(self.ff_frame_vector_diagram,  width=10)
        self.ff_vector_diagram_L_entry.grid(row=3, column=0, sticky=W, padx=70)

        self.ff_vector_diagram_C_label = Label(self.ff_frame_vector_diagram, text='Wert für C:')
        self.ff_vector_diagram_C_label.grid(row=4, column=0, sticky=W)
        self.ff_vector_diagram_C_entry = Entry(self.ff_frame_vector_diagram,  width=10)
        self.ff_vector_diagram_C_entry.grid(row=4, column=0, sticky=W, padx=70)

        self.ff_vector_diagram_freq_label = Label(self.ff_frame_vector_diagram, text='Wert für f:')
        self.ff_vector_diagram_freq_label.grid(row=5, column=0, sticky=W)
        self.ff_vector_diagram_freq_entry = Entry(self.ff_frame_vector_diagram,  width=10)
        self.ff_vector_diagram_freq_entry.grid(row=5, column=0, sticky=W, padx=70)


        # Spannung Diagramm erzeugen
        self.ff_var_create_voltage_current_vector_diagram = IntVar()
        self.ff_check_create_voltage_vector_diagram = Checkbutton(self.ff_frame_vector_diagram, text="Strom-/Spannungsdiagramm", variable=self.ff_var_create_voltage_current_vector_diagram, onvalue=1, offvalue=0)
        self.ff_check_create_voltage_vector_diagram.deselect()
        self.ff_check_create_voltage_vector_diagram.grid(row=1, column=1, sticky=W)

        # Impedanz Diagramm
        self.ff_var_create_impedance_vector_diagram = IntVar()
        self.ff_check_create_impedance_vector_diagram = Checkbutton(self.ff_frame_vector_diagram, text="Impedanz-Diagramm ", variable=self.ff_var_create_impedance_vector_diagram, onvalue=1, offvalue=0)
        self.ff_check_create_impedance_vector_diagram.deselect()
        self.ff_check_create_impedance_vector_diagram.grid(row=2, column=1, sticky=W)

        # Admittanz Diagramm
        self.ff_var_create_admittance_vector_diagram = IntVar()
        self.ff_check_create_admittance_vector_diagram = Checkbutton(self.ff_frame_vector_diagram, text="Admittanz-Diagramm ", variable=self.ff_var_create_admittance_vector_diagram, onvalue=1, offvalue=0)
        self.ff_check_create_admittance_vector_diagram.deselect()
        self.ff_check_create_admittance_vector_diagram.grid(row=3, column=1, sticky=W)

        # Leistungsdiagramm
        self.ff_var_create_power_vector_diagram = IntVar()
        self.ff_check_create_power_vector_diagram = Checkbutton(self.ff_frame_vector_diagram, text="Leistungsdiagramm ", variable=self.ff_var_create_power_vector_diagram, onvalue=1, offvalue=0)
        self.ff_check_create_power_vector_diagram.deselect()
        self.ff_check_create_power_vector_diagram.grid(row=4, column=1, sticky=W)



        self.ff_vector_diagram_btn = Button(self.ff_frame_vector_diagram, text="Zeigerdiagramm erzeugen", command=lambda: test_generator_modul_zeigerdiagramme.Zeigerdiagramme.__init__( self, self.ff_vector_diagram_type_box.get(),

                                                                                                                                                                                         self.ff_var_create_voltage_current_vector_diagram.get(),
                                                                                                                                                                                         self.ff_var_create_impedance_vector_diagram.get(),
                                                                                                                                                                                         self.ff_var_create_admittance_vector_diagram.get(),
                                                                                                                                                                                         self.ff_var_create_power_vector_diagram.get(),

                                                                                                                                                                                         self.ff_vector_diagram_U_entry.get(),
                                                                                                                                                                                         self.ff_vector_diagram_R_entry.get(),
                                                                                                                                                                                         self.ff_vector_diagram_L_entry.get(),
                                                                                                                                                                                         self.ff_vector_diagram_C_entry.get(),
                                                                                                                                                                                         self.ff_vector_diagram_freq_entry.get()
                                                                                                                                                                                         ))
        self.ff_vector_diagram_btn.grid(row=10, column=0, padx=10, pady=(10, 0), sticky="W")
###################### "Formelfrage" - FRAME   -------- LABELS / ENTRYS / BUTTONS  ###################

        self.ff_question_author_label = Label(self.ff_frame, text="Fragen-Autor")
        self.ff_question_author_label.grid(row=0, column=0, sticky=W, pady=(10, 0), padx=10)
        self.ff_question_author_entry = Entry(self.ff_frame, width=20)
        self.ff_question_author_entry.grid(row=0, column=1, sticky=W, pady=(10, 0))

        self.ff_question_title_label = Label(self.ff_frame, text="Fragen-Titel")
        self.ff_question_title_label.grid(row=1, column=0, sticky=W, padx=10, pady=(10, 0))
        self.ff_question_title_entry = Entry(self.ff_frame, width=60)
        self.ff_question_title_entry.grid(row=1, column=1,  sticky=W, pady=(10, 0))

        self.ff_question_description_title_label = Label(self.ff_frame, text="Fragen-Beschreibung")
        self.ff_question_description_title_label.grid(row=2, column=0, sticky=W, padx=10)
        self.ff_question_description_title_entry = Entry(self.ff_frame, width=60)
        self.ff_question_description_title_entry.grid(row=2, column=1, sticky=W)

        self.ff_question_textfield_label = Label(self.ff_frame, text="Fragen-Text")
        self.ff_question_textfield_label.grid(row=3, column=0, sticky=W, padx=10)

        self.ff_bar = Scrollbar(self.ff_frame)
        self.ff_question_description_main_entry = Text(self.ff_frame, height=6, width=65, font=('Helvetica', 9))
        self.ff_bar.grid(row=3, column=2, sticky=W)
        self.ff_question_description_main_entry.grid(row=3, column=1, pady=10, sticky=W)
        self.ff_bar.config(command=self.ff_question_description_main_entry.yview)
        self.ff_question_description_main_entry.config(yscrollcommand=self.ff_bar.set)





############## BEARBEITUNGSDAUER


        self.ff_processing_time_label = Label(self.ff_frame, text="Bearbeitungsdauer")
        self.ff_processing_time_label.grid(row=4, column=0, sticky=W, pady=(5, 0), padx=10)

        self.ff_processing_time_label = Label(self.ff_frame, text="Std:")
        self.ff_processing_time_label.grid(row=4, column=1, sticky=W, pady=(5, 0))
        self.ff_processing_time_label = Label(self.ff_frame, text="Min:")
        self.ff_processing_time_label.grid(row=4, column=1, sticky=W, padx=70, pady=(5, 0))
        self.ff_processing_time_label = Label(self.ff_frame, text="Sek:")
        self.ff_processing_time_label.grid(row=4, column=1, sticky=W, padx=145, pady=(5, 0))

        self.ff_processingtime_hours = list(range(24))
        self.ff_processingtime_minutes = list(range(60))
        self.ff_processingtime_seconds = list(range(60))

        self.ff_proc_hours_box = ttk.Combobox(self.ff_frame, value=self.ff_processingtime_hours, width=2)
        self.ff_proc_minutes_box = ttk.Combobox(self.ff_frame, value=self.ff_processingtime_minutes, width=2)
        self.ff_proc_seconds_box = ttk.Combobox(self.ff_frame, value=self.ff_processingtime_seconds, width=2)

        self.ff_proc_hours_box.current(23)
        self.ff_proc_minutes_box.current(0)
        self.ff_proc_seconds_box.current(0)

        def selected_hours(event):
            self.selected_hours = self.ff_proc_hours_box.get()


        def selected_minutes(event):
            self.selected_minutes = self.ff_proc_minutes_box.get()


        def selected_seconds(event):
            self.selected_seconds = self.ff_proc_seconds_box.get()


        self.ff_proc_hours_box.bind("<<ComboboxSelected>>", selected_hours)
        self.ff_proc_minutes_box.bind("<<ComboboxSelected>>", selected_minutes)
        self.ff_proc_seconds_box.bind("<<ComboboxSelected>>", selected_seconds)

        self.ff_proc_hours_box.grid(row=4, column=1, sticky=W, padx=25, pady=(5, 0))
        self.ff_proc_minutes_box.grid(row=4, column=1, sticky=W, padx=100, pady=(5, 0))
        self.ff_proc_seconds_box.grid(row=4, column=1, sticky=W, padx=170, pady=(5, 0))





        ########################### ÜBERSCHRIFTEN / LABELS FÜR EINGABEFELDER-MATRIX ##############################

        self.var_min_label = Label(self.ff_frame, text=' Min.')
        self.var_min_label.grid(row=5, column=1, sticky=W, pady=(20, 0), padx=60)

        self.var_max_label = Label(self.ff_frame, text=' Max.')
        self.var_max_label.grid(row=5, column=1, sticky=W, pady=(20, 0), padx=100)

        self.var_prec_label = Label(self.ff_frame, text=' Präz.')
        self.var_prec_label.grid(row=5, column=1, sticky=W, pady=(20, 0), padx=140)

        self.var_divby_label = Label(self.ff_frame, text=' Teilbar\ndurch')
        self.var_divby_label.grid(row=5, column=1, sticky=W, pady=(20, 0), padx=180)

        self.variable1_label = Label(self.ff_frame, text='Variable 1')
        self.variable2_label = Label(self.ff_frame, text='Variable 2')
        self.variable3_label = Label(self.ff_frame, text='Variable 3')
        self.variable4_label = Label(self.ff_frame, text='Variable 4')
        self.variable5_label = Label(self.ff_frame, text='Variable 5')
        self.variable6_label = Label(self.ff_frame, text='Variable 6')
        self.variable7_label = Label(self.ff_frame, text='Variable 7')
        self.variable8_label = Label(self.ff_frame, text='Variable 8')
        self.variable9_label = Label(self.ff_frame, text='Variable 9')
        self.variable10_label = Label(self.ff_frame, text='Variable 10')
        self.variable11_label = Label(self.ff_frame, text='Variable 11')
        self.variable12_label = Label(self.ff_frame, text='Variable 12')
        self.variable13_label = Label(self.ff_frame, text='Variable 13')
        self.variable14_label = Label(self.ff_frame, text='Variable 14')
        self.variable15_label = Label(self.ff_frame, text='Variable 15')

        # Label für Var1 ist immer aktiv/ zu sehen. Var2-10 werden je nach Auswahl ein-/ausgeblendet
        self.variable1_label.grid(row=6, column=0, sticky=W, padx=20)







        ########################### EINGABEFELDER / ENTRYS FÜR EINGABEFELDER-MATRIX ##############################

        self.var1_name_entry = Entry(self.ff_frame,  width=6)
        self.var1_min_entry = Entry(self.ff_frame,  width=6)
        self.var1_max_entry = Entry(self.ff_frame,  width=6)
        self.var1_prec_entry = Entry(self.ff_frame,  width=6)
        self.var1_divby_entry = Entry(self.ff_frame,  width=6)

        self.var2_name_entry = Entry(self.ff_frame,  width=6)
        self.var2_min_entry = Entry(self.ff_frame,  width=6)
        self.var2_max_entry = Entry(self.ff_frame,  width=6)
        self.var2_prec_entry = Entry(self.ff_frame,  width=6)
        self.var2_divby_entry = Entry(self.ff_frame,  width=6)

        self.var3_name_entry = Entry(self.ff_frame,  width=6)
        self.var3_min_entry = Entry(self.ff_frame,  width=6)
        self.var3_max_entry = Entry(self.ff_frame,  width=6)
        self.var3_prec_entry = Entry(self.ff_frame,  width=6)
        self.var3_divby_entry = Entry(self.ff_frame,  width=6)

        self.var4_name_entry = Entry(self.ff_frame,  width=6)
        self.var4_min_entry = Entry(self.ff_frame,  width=6)
        self.var4_max_entry = Entry(self.ff_frame,  width=6)
        self.var4_prec_entry = Entry(self.ff_frame,  width=6)
        self.var4_divby_entry = Entry(self.ff_frame,  width=6)

        self.var5_name_entry = Entry(self.ff_frame,  width=6)
        self.var5_min_entry = Entry(self.ff_frame,  width=6)
        self.var5_max_entry = Entry(self.ff_frame,  width=6)
        self.var5_prec_entry = Entry(self.ff_frame,  width=6)
        self.var5_divby_entry = Entry(self.ff_frame,  width=6)

        self.var6_name_entry = Entry(self.ff_frame,  width=6)
        self.var6_min_entry = Entry(self.ff_frame,  width=6)
        self.var6_max_entry = Entry(self.ff_frame,  width=6)
        self.var6_prec_entry = Entry(self.ff_frame,  width=6)
        self.var6_divby_entry = Entry(self.ff_frame,  width=6)

        self.var7_name_entry = Entry(self.ff_frame,  width=6)
        self.var7_min_entry = Entry(self.ff_frame,  width=6)
        self.var7_max_entry = Entry(self.ff_frame, width=6)
        self.var7_prec_entry = Entry(self.ff_frame,  width=6)
        self.var7_divby_entry = Entry(self.ff_frame,  width=6)

        self.var8_name_entry = Entry(self.ff_frame,  width=6)
        self.var8_min_entry = Entry(self.ff_frame,  width=6)
        self.var8_max_entry = Entry(self.ff_frame,  width=6)
        self.var8_prec_entry = Entry(self.ff_frame,  width=6)
        self.var8_divby_entry = Entry(self.ff_frame,  width=6)

        self.var9_name_entry = Entry(self.ff_frame,  width=6)
        self.var9_min_entry = Entry(self.ff_frame,  width=6)
        self.var9_max_entry = Entry(self.ff_frame,  width=6)
        self.var9_prec_entry = Entry(self.ff_frame,  width=6)
        self.var9_divby_entry = Entry(self.ff_frame,  width=6)

        self.var10_name_entry = Entry(self.ff_frame,  width=6)
        self.var10_min_entry = Entry(self.ff_frame, width=6)
        self.var10_max_entry = Entry(self.ff_frame, width=6)
        self.var10_prec_entry = Entry(self.ff_frame, width=6)
        self.var10_divby_entry = Entry(self.ff_frame, width=6)

        self.var11_name_entry = Entry(self.ff_frame,  width=6)
        self.var11_min_entry = Entry(self.ff_frame, width=6)
        self.var11_max_entry = Entry(self.ff_frame, width=6)
        self.var11_prec_entry = Entry(self.ff_frame, width=6)
        self.var11_divby_entry = Entry(self.ff_frame, width=6)

        self.var12_name_entry = Entry(self.ff_frame,  width=6)
        self.var12_min_entry = Entry(self.ff_frame, width=6)
        self.var12_max_entry = Entry(self.ff_frame, width=6)
        self.var12_prec_entry = Entry(self.ff_frame, width=6)
        self.var12_divby_entry = Entry(self.ff_frame, width=6)

        self.var13_name_entry = Entry(self.ff_frame,  width=6)
        self.var13_min_entry = Entry(self.ff_frame, width=6)
        self.var13_max_entry = Entry(self.ff_frame, width=6)
        self.var13_prec_entry = Entry(self.ff_frame, width=6)
        self.var13_divby_entry = Entry(self.ff_frame, width=6)

        self.var14_name_entry = Entry(self.ff_frame,  width=6)
        self.var14_min_entry = Entry(self.ff_frame, width=6)
        self.var14_max_entry = Entry(self.ff_frame, width=6)
        self.var14_prec_entry = Entry(self.ff_frame, width=6)
        self.var14_divby_entry = Entry(self.ff_frame, width=6)

        self.var15_name_entry = Entry(self.ff_frame,  width=6)
        self.var15_min_entry = Entry(self.ff_frame, width=6)
        self.var15_max_entry = Entry(self.ff_frame, width=6)
        self.var15_prec_entry = Entry(self.ff_frame, width=6)
        self.var15_divby_entry = Entry(self.ff_frame, width=6)

        # Variablen Entries in Listen zusammenfassen
        # Die Listen bieten den Vorteil, dass bei der Platzierung auf der GUI eine Schleife verwendet werden kann
        self.var_label_list = [self.variable1_label,  self.variable2_label,  self.variable3_label,  self.variable4_label,  self.variable5_label,  self.variable6_label, self.variable7_label,
                               self.variable8_label, self.variable9_label, self.variable10_label, self.variable11_label, self.variable12_label, self.variable13_label, self.variable14_label, self.variable15_label]

        self.var_name_entry_list = [self.var1_name_entry, self.var2_name_entry, self.var3_name_entry, self.var4_name_entry, self.var5_name_entry, self.var6_name_entry, self.var7_name_entry,
                                    self.var8_name_entry, self.var9_name_entry, self.var10_name_entry, self.var11_name_entry, self.var12_name_entry, self.var13_name_entry, self.var14_name_entry, self.var15_name_entry]

        self.var_min_entry_list = [self.var1_min_entry, self.var2_min_entry, self.var3_min_entry, self.var4_min_entry, self.var5_min_entry, self.var6_min_entry, self.var7_min_entry,
                                   self.var8_min_entry, self.var9_min_entry, self.var10_min_entry, self.var11_min_entry, self.var12_min_entry, self.var13_min_entry, self.var14_min_entry, self.var15_min_entry]


        self.var_max_entry_list = [self.var1_max_entry, self.var2_max_entry, self.var3_max_entry, self.var4_max_entry, self.var5_max_entry, self.var6_max_entry, self.var7_max_entry,
                                   self.var8_max_entry, self.var9_max_entry, self.var10_max_entry, self.var11_max_entry, self.var12_max_entry, self.var13_max_entry, self.var14_max_entry, self.var15_max_entry]


        self.var_prec_entry_list = [self.var1_prec_entry, self.var2_prec_entry, self.var3_prec_entry, self.var4_prec_entry, self.var5_prec_entry, self.var6_prec_entry, self.var7_prec_entry,
                                    self.var8_prec_entry, self.var9_prec_entry, self.var10_prec_entry, self.var11_prec_entry, self.var12_prec_entry, self.var13_prec_entry, self.var14_prec_entry, self.var15_prec_entry]


        self.var_divby_entry_list = [self.var1_divby_entry, self.var2_divby_entry, self.var3_divby_entry, self.var4_divby_entry, self.var5_divby_entry, self.var6_divby_entry, self.var7_divby_entry,
                                     self.var8_divby_entry, self.var9_divby_entry, self.var10_divby_entry, self.var11_divby_entry, self.var12_divby_entry, self.var13_divby_entry, self.var14_divby_entry, self.var15_divby_entry]


        # Eingabefelder für Var1 sind immer aktiv/ zu sehen. Var2-10 werden je nach Auswahl ein-/ausgeblendet
        self.var1_name_entry.grid(row=6, column=1, sticky=W)
        self.var1_min_entry.grid(row=6, column=1, sticky=W, padx=60)
        self.var1_max_entry.grid(row=6, column=1, sticky=W, padx=100)
        self.var1_prec_entry.grid(row=6, column=1, sticky=W, padx=140)
        self.var1_divby_entry.grid(row=6, column=1, sticky=W, padx=180)





        ###########################  EINGABEFELDER-MATRIX (VARIABLEN)  EIN/AUSBLENDEN ##############################

        # Hier werden durch die Funktion "ff_answer_selected" die Variable - Eingabefelder (je nach Wert) ein-/ausgeblendet

        def ff_answer_selected(event):  # "variable" need for comboBox Binding

            self.selected_number_of_variables = int(self.ff_numbers_of_answers_box.get())

            # Schleife zur Platzierung der Entries auf der GUI
            # Bei einer Auswahl von 5 Variablen, werden auf der GUI die Zeilen 1-5 platziert
            for i in range(self.selected_number_of_variables):
                Formelfrage.ff_variable_show_or_remove(self, self.var_label_list[i], self.var_name_entry_list[i], self.var_min_entry_list[i], self.var_max_entry_list[i], self.var_prec_entry_list[i], self.var_divby_entry_list[i], str(i+7), "show")

            # Schleife zum ausblenden der Entries auf der GUI
            # Bei einer Auswahl von 5 Variablen, werden auf der GUI die Zeilen 6-15 ausgeblendet
            for j in range(self.selected_number_of_variables, len(self.var_min_entry_list)):
                Formelfrage.ff_variable_show_or_remove(self, self.var_label_list[j], self.var_name_entry_list[j], self.var_min_entry_list[j], self.var_max_entry_list[j], self.var_prec_entry_list[j], self.var_divby_entry_list[j], str(j+7), "remove")



        self.ff_numbers_of_answers_box_label = Label(self.ff_frame, text="Anzahl der Variablen: ")
        self.ff_numbers_of_answers_box_label.grid(row=5, column=0, sticky=W, padx=10, pady=(20, 0))
        self.ff_numbers_of_answers_value = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"]
        self.ff_numbers_of_answers_box = ttk.Combobox(self.ff_frame, value=self.ff_numbers_of_answers_value, width=3)
        self.ff_numbers_of_answers_box.bind("<<ComboboxSelected>>", ff_answer_selected)
        self.ff_numbers_of_answers_box.grid(row=5, column=1, sticky=W, pady=(20, 0))
        self.ff_numbers_of_answers_box.current(0)


        ###########################  AUSWAHL DER EINHEITEN FÜR VARIABLEN ---- DERZEIT NICHT AKTIV ##############################

        self.select_var_units = ["Unit", "H", "mH", "µH", "nH", "pH", "---", "F", "mF", "µF", "nF", "pF", "---", "MV", "kV", "V", "mV", "µV", "---"]

        self.var1_unit_myCombo = ttk.Combobox(self.ff_frame, value=self.select_var_units, width=5)
        self.var1_unit_myCombo.current(0)

        self.var2_unit_myCombo = ttk.Combobox(self.ff_frame, value=self.select_var_units, width=5)
        self.var2_unit_myCombo.current(0)

        self.var3_unit_myCombo = ttk.Combobox(self.ff_frame, value=self.select_var_units, width=5)
        self.var3_unit_myCombo.current(0)

        self.var4_unit_myCombo = ttk.Combobox(self.ff_frame, value=self.select_var_units, width=5)
        self.var4_unit_myCombo.current(0)

        self.var5_unit_myCombo = ttk.Combobox(self.ff_frame, value=self.select_var_units, width=5)
        self.var5_unit_myCombo.current(0)

        self.var6_unit_myCombo = ttk.Combobox(self.ff_frame, value=self.select_var_units, width=5)
        self.var6_unit_myCombo.current(0)

        self.var7_unit_myCombo = ttk.Combobox(self.ff_frame, value=self.select_var_units, width=5)
        self.var7_unit_myCombo.current(0)


        ########################### ÜBERSCHRIFTEN / LABELS FÜR EINGABEFELDER-MATRIX ##############################

        self.res_min_label = Label(self.ff_frame, text=' Min.')
        self.res_max_label = Label(self.ff_frame, text=' Max.')
        self.res_prec_label = Label(self.ff_frame, text=' Präz.')
        self.res_tol_label = Label(self.ff_frame, text='  Tol.')
        self.res_points_label = Label(self.ff_frame, text='Punkte')
        self.res_formula_label = Label(self.ff_frame, text='Formel')

        self.res_min_label.grid(row=40, column=1, sticky=W, pady=(10, 0), padx=60)
        self.res_max_label.grid(row=40, column=1, sticky=W, pady=(10, 0), padx=100)
        self.res_prec_label.grid(row=40, column=1, sticky=W, pady=(10, 0), padx=140)
        self.res_tol_label.grid(row=40, column=1, sticky=W, pady=(10, 0), padx=180)
        self.res_points_label.grid(row=40, column=1, sticky=W, pady=(10, 0), padx=220)
        self.res_formula_label.grid(row=40, column=1, sticky=E, pady=(10, 0), padx=100)



        self.result1_label = Label(self.ff_frame, text='Ergebnis 1')
        self.result2_label = Label(self.ff_frame, text='Ergebnis 2')
        self.result3_label = Label(self.ff_frame, text='Ergebnis 3')
        self.result4_label = Label(self.ff_frame, text='Ergebnis 4')
        self.result5_label = Label(self.ff_frame, text='Ergebnis 5')
        self.result6_label = Label(self.ff_frame, text='Ergebnis 6')
        self.result7_label = Label(self.ff_frame, text='Ergebnis 7')
        self.result8_label = Label(self.ff_frame, text='Ergebnis 8')
        self.result9_label = Label(self.ff_frame, text='Ergebnis 9')
        self.result10_label = Label(self.ff_frame, text='Ergebnis 10')

        # Label für Res1 ist immer aktiv/ zu sehen. Res2-10 werden je nach Auswahl ein-/ausgeblendet
        self.result1_label.grid(row=41, column=0, sticky=W, padx=20)




        ########################### EINGABEFELDER / ENTRYS FÜR EINGABEFELDER-MATRIX ##############################

        self.res1_name_entry = Entry(self.ff_frame, width=6)
        self.res1_min_entry = Entry(self.ff_frame, width=6)
        self.res1_max_entry = Entry(self.ff_frame, width=6)
        self.res1_prec_entry = Entry(self.ff_frame, width=6)
        self.res1_tol_entry = Entry(self.ff_frame, width=6)
        self.res1_points_entry = Entry(self.ff_frame, width=6)
        self.res1_formula_entry = Entry(self.ff_frame, width=30)

        self.res2_name_entry = Entry(self.ff_frame, width=6)
        self.res2_min_entry = Entry(self.ff_frame, width=6)
        self.res2_max_entry = Entry(self.ff_frame, width=6)
        self.res2_prec_entry = Entry(self.ff_frame, width=6)
        self.res2_tol_entry = Entry(self.ff_frame, width=6)
        self.res2_points_entry = Entry(self.ff_frame, width=6)
        self.res2_formula_entry = Entry(self.ff_frame, width=30)

        self.res3_name_entry = Entry(self.ff_frame, width=6)
        self.res3_min_entry = Entry(self.ff_frame, width=6)
        self.res3_max_entry = Entry(self.ff_frame, width=6)
        self.res3_prec_entry = Entry(self.ff_frame, width=6)
        self.res3_tol_entry = Entry(self.ff_frame, width=6)
        self.res3_points_entry = Entry(self.ff_frame, width=6)
        self.res3_formula_entry = Entry(self.ff_frame, width=30)

        self.res4_name_entry = Entry(self.ff_frame, width=6)
        self.res4_min_entry = Entry(self.ff_frame, width=6)
        self.res4_max_entry = Entry(self.ff_frame, width=6)
        self.res4_prec_entry = Entry(self.ff_frame, width=6)
        self.res4_tol_entry = Entry(self.ff_frame, width=6)
        self.res4_points_entry = Entry(self.ff_frame, width=6)
        self.res4_formula_entry = Entry(self.ff_frame, width=30)

        self.res5_name_entry = Entry(self.ff_frame, width=6)
        self.res5_min_entry = Entry(self.ff_frame, width=6)
        self.res5_max_entry = Entry(self.ff_frame, width=6)
        self.res5_prec_entry = Entry(self.ff_frame, width=6)
        self.res5_tol_entry = Entry(self.ff_frame,  width=6)
        self.res5_points_entry = Entry(self.ff_frame, width=6)
        self.res5_formula_entry = Entry(self.ff_frame, width=30)

        self.res6_name_entry = Entry(self.ff_frame, width=6)
        self.res6_min_entry = Entry(self.ff_frame, width=6)
        self.res6_max_entry = Entry(self.ff_frame, width=6)
        self.res6_prec_entry = Entry(self.ff_frame, width=6)
        self.res6_tol_entry = Entry(self.ff_frame, width=6)
        self.res6_points_entry = Entry(self.ff_frame, width=6)
        self.res6_formula_entry = Entry(self.ff_frame, width=30)

        self.res7_name_entry = Entry(self.ff_frame, width=6)
        self.res7_min_entry = Entry(self.ff_frame, width=6)
        self.res7_max_entry = Entry(self.ff_frame, width=6)
        self.res7_prec_entry = Entry(self.ff_frame, width=6)
        self.res7_tol_entry = Entry(self.ff_frame, width=6)
        self.res7_points_entry = Entry(self.ff_frame, width=6)
        self.res7_formula_entry = Entry(self.ff_frame, width=30)

        self.res8_name_entry = Entry(self.ff_frame,  width=6)
        self.res8_min_entry = Entry(self.ff_frame,  width=6)
        self.res8_max_entry = Entry(self.ff_frame,  width=6)
        self.res8_prec_entry = Entry(self.ff_frame,  width=6)
        self.res8_tol_entry = Entry(self.ff_frame,  width=6)
        self.res8_points_entry = Entry(self.ff_frame,  width=6)
        self.res8_formula_entry = Entry(self.ff_frame,  width=30)

        self.res9_name_entry = Entry(self.ff_frame, width=6)
        self.res9_min_entry = Entry(self.ff_frame, width=6)
        self.res9_max_entry = Entry(self.ff_frame, width=6)
        self.res9_prec_entry = Entry(self.ff_frame, width=6)
        self.res9_tol_entry = Entry(self.ff_frame, width=6)
        self.res9_points_entry = Entry(self.ff_frame, width=6)
        self.res9_formula_entry = Entry(self.ff_frame, width=30)

        self.res10_name_entry = Entry(self.ff_frame, width=6)
        self.res10_min_entry = Entry(self.ff_frame, width=6)
        self.res10_max_entry = Entry(self.ff_frame, width=6)
        self.res10_prec_entry = Entry(self.ff_frame, width=6)
        self.res10_tol_entry = Entry(self.ff_frame, width=6)
        self.res10_points_entry = Entry(self.ff_frame, width=6)
        self.res10_formula_entry = Entry(self.ff_frame, width=30)

        # Eingabefelder für Res1 sind immer aktiv/ zu sehen. Res2-10 werden je nach Auswahl ein-/ausgeblendet
        self.res1_name_entry.grid(row=41, column=1, sticky=W)
        self.res1_min_entry.grid(row=41, column=1, sticky=W, padx=60)
        self.res1_max_entry.grid(row=41, column=1, sticky=W, padx=100)
        self.res1_prec_entry.grid(row=41, column=1, sticky=W, padx=140)
        self.res1_tol_entry.grid(row=41, column=1, sticky=W, padx=180)
        self.res1_points_entry.grid(row=41, column=1, sticky=W, padx=220)
        self.res1_formula_entry.grid(row=41, column=1, sticky=E, padx=20)

        # Ergebnis Entries in Listen zusammenfassen
        # Die Listen bieten den Vorteil, dass bei der Platzierung auf der GUI eine Schleife verwendet werden kann
        self.res_label_list = [self.result1_label, self.result2_label, self.result3_label, self.result4_label, self.result5_label,
                               self.result6_label, self.result7_label, self.result8_label, self.result9_label, self.result10_label]

        self.res_name_entry_list = [self.res1_name_entry, self.res2_name_entry, self.res3_name_entry, self.res4_name_entry, self.res5_name_entry,
                                    self.res6_name_entry, self.res7_name_entry, self.res8_name_entry, self.res9_name_entry, self.res10_name_entry]

        self.res_min_entry_list = [self.res1_min_entry, self.res2_min_entry, self.res3_min_entry, self.res4_min_entry, self.res5_min_entry,
                                   self.res6_min_entry, self.res7_min_entry, self.res8_min_entry, self.res9_min_entry, self.res10_min_entry]

        self.res_max_entry_list = [self.res1_max_entry, self.res2_max_entry, self.res3_max_entry, self.res4_max_entry, self.res5_max_entry,
                                   self.res6_max_entry, self.res7_max_entry, self.res8_max_entry, self.res9_max_entry, self.res10_max_entry]

        self.res_prec_entry_list = [self.res1_prec_entry, self.res2_prec_entry, self.res3_prec_entry, self.res4_prec_entry, self.res5_prec_entry,
                                    self.res6_prec_entry, self.res7_prec_entry, self.res8_prec_entry, self.res9_prec_entry, self.res10_prec_entry]

        self.res_tol_entry_list = [self.res1_tol_entry, self.res2_tol_entry, self.res3_tol_entry, self.res4_tol_entry, self.res5_tol_entry,
                                   self.res6_tol_entry, self.res7_tol_entry, self.res8_tol_entry, self.res9_tol_entry, self.res10_tol_entry]

        self.res_points_entry_list = [self.res1_points_entry, self.res2_points_entry, self.res3_points_entry, self.res4_points_entry, self.res5_points_entry,
                                      self.res6_points_entry, self.res7_points_entry, self.res8_points_entry, self.res9_points_entry, self.res10_points_entry]

        self.res_formula_entry_list = [self.res1_formula_entry, self.res2_formula_entry, self.res3_formula_entry, self.res4_formula_entry, self.res5_formula_entry,
                                       self.res6_formula_entry, self.res7_formula_entry, self.res8_formula_entry, self.res9_formula_entry, self.res10_formula_entry]



        # Liste werden für Wertebereich berechnung verwendet
        self.var_res_combined_min_entries_list = [self.var1_min_entry, self.var2_min_entry, self.var3_min_entry, self.var4_min_entry,
                                            self.var5_min_entry, self.var6_min_entry, self.var7_min_entry,
                                            self.var8_min_entry, self.var9_min_entry, self.var10_min_entry, self.var11_min_entry,
                                            self.var12_min_entry, self.var13_min_entry, self.var14_min_entry,
                                            self.var15_min_entry, self.res1_min_entry, self.res2_min_entry, self.res3_min_entry,
                                         self.res4_min_entry, self.res5_min_entry, self.res6_min_entry, self.res7_min_entry,
                                         self.res8_min_entry, self.res9_min_entry, self.res10_min_entry ]

        self.var_res_combined_max_entries_list = [self.var1_max_entry, self.var2_max_entry, self.var3_max_entry, self.var4_max_entry,
                                   self.var5_max_entry, self.var6_max_entry, self.var7_max_entry,
                                   self.var8_max_entry, self.var9_max_entry, self.var10_max_entry, self.var11_max_entry,
                                   self.var12_max_entry, self.var13_max_entry, self.var14_max_entry,
                                   self.var15_max_entry, self.res1_max_entry, self.res2_max_entry, self.res3_max_entry, self.res4_max_entry,
                                   self.res5_max_entry,
                                   self.res6_max_entry, self.res7_max_entry, self.res8_max_entry, self.res9_max_entry,
                                   self.res10_max_entry]

       #############################



        #################### EINHEITEN FÜR ERGEBNISSE DERZEIT DEAKTIVIERT

        # self.res1_unit_myCombo = ttk.Combobox(self.frame_formula, value=self.select_var_units, width=5)
        # self.res1_unit_myCombo.current(0)
        # self.res1_unit_myCombo.bind("<<ComboboxSelected>>", selected_var)
        # #self.res1_unit_myCombo.grid(row=21, column=0, sticky=E, padx=10)
        #
        # self.res2_unit_myCombo = ttk.Combobox(self.frame_formula, value=self.select_var_units, width=5)
        # self.res2_unit_myCombo.current(0)
        # self.res2_unit_myCombo.bind("<<ComboboxSelected>>", selected_var)
        #
        # self.res3_unit_myCombo = ttk.Combobox(self.frame_formula, value=self.select_var_units, width=5)
        # self.res3_unit_myCombo.current(0)
        # self.res3_unit_myCombo.bind("<<ComboboxSelected>>", selected_var)


        # Hier werden durch die Funktion "ff_result_selected" die Ergebnisse - Eingabefelder (je nach Wert) ein-/ausgeblendet
        def ff_result_selected(event):  # "variable" need for comboBox Binding

            self.selected_number_of_results = int(self.ff_numbers_of_results_box.get())

            # Schleife zur Platzierung der Entries auf der GUI
            # Bei einer Auswahl von 5 Ergebnissen, werden auf der GUI die Zeilen 1-5 platziert
            for i in range(self.selected_number_of_results):
                #Formelfrage.ff_variable_show_or_remove(self, self.var_label_list[i], self.var_name_entry_list[i], self.var_min_entry_list[i], self.var_max_entry_list[i], self.var_prec_entry_list[i], self.var_divby_entry_list[i], str(i+7), "show")
                Formelfrage.ff_result_show_or_remove(self, self.res_label_list[i], self.res_name_entry_list[i], self.res_min_entry_list[i], self.res_max_entry_list[i], self.res_prec_entry_list[i], self.res_tol_entry_list[i], self.res_points_entry_list[i], self.res_formula_entry_list[i], str(i+42), "show")

            # Schleife zum ausblenden der Entries auf der GUI
            # Bei einer Auswahl von 5 Ergebnissen, werden auf der GUI die Zeilen 6-15 ausgeblendet
            for j in range(self.selected_number_of_results, len(self.res_min_entry_list)):
                Formelfrage.ff_result_show_or_remove(self, self.res_label_list[j], self.res_name_entry_list[j], self.res_min_entry_list[j], self.res_max_entry_list[j], self.res_prec_entry_list[j], self.res_tol_entry_list[j], self.res_points_entry_list[j], self.res_formula_entry_list[j], str(j+42), "remove")


        self.ff_numbers_of_results_box_label = Label(self.ff_frame, text="Anzahl der Ergebnisse: ")
        self.ff_numbers_of_results_box_label.grid(row=40, column=0, sticky=W, padx=10, pady=(20, 0))
        self.ff_numbers_of_results_value = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
        self.ff_numbers_of_results_box = ttk.Combobox(self.ff_frame, value=self.ff_numbers_of_results_value, width=3)
        self.ff_numbers_of_results_box.current(0)
        self.ff_numbers_of_results_box.bind("<<ComboboxSelected>>", ff_result_selected)
        self.ff_numbers_of_results_box.grid(row=40, column=1, sticky=W, pady=(20, 0))



    def ff_variable_show_or_remove(self, var_label, var_name_entry, var_min_entry, var_max_entry, var_prec_entry, var_divby_entry, row_nr, var_status):

            if var_status == "show":
                var_label.grid(row=int(row_nr), column=0, sticky=W, padx=20)
                var_name_entry.grid(row=int(row_nr), column=1, sticky=W)
                var_min_entry.grid(row=int(row_nr), column=1, sticky=W, padx=60)
                var_max_entry.grid(row=int(row_nr), column=1, sticky=W, padx=100)
                var_prec_entry.grid(row=int(row_nr), column=1, sticky=W, padx=140)
                var_divby_entry.grid(row=int(row_nr), column=1, sticky=W, padx=180)
                #var_unit_myCombo.grid(row=int(row_nr), column=0, sticky=E, padx=10)


            else:
                var_label.grid_remove()
                var_name_entry.grid_remove()
                var_min_entry.grid_remove()
                var_max_entry.grid_remove()
                var_prec_entry.grid_remove()
                var_divby_entry.grid_remove()
                # var_unit_myCombo.grid_remove()

    def ff_result_show_or_remove(self, res_label, res_name_entry, res_min_entry, res_max_entry, res_prec_entry, res_tol_entry, res_points_entry, res_formula_entry, row_nr, res_status):

        if res_status == "show":
            res_label.grid(row=int(row_nr), column=0, sticky=W, padx=20)
            res_name_entry.grid(row=int(row_nr), column=1, sticky=W)
            res_min_entry.grid(row=int(row_nr), column=1, sticky=W, padx=60)
            res_max_entry.grid(row=int(row_nr), column=1, sticky=W, padx=100)
            res_prec_entry.grid(row=int(row_nr), column=1, sticky=W, padx=140)
            res_tol_entry.grid(row=int(row_nr), column=1, sticky=W, padx=180)
            res_points_entry.grid(row=int(row_nr), column=1, sticky=W, padx=220)
            res_formula_entry.grid(row=int(row_nr), column=1, sticky=E, padx=20)
            #res_unit_myCombo.grid(row=int(row_nr), column=0, sticky=E, padx=10)

        else:
            res_label.grid_remove()
            res_name_entry.grid_remove()
            res_min_entry.grid_remove()
            res_max_entry.grid_remove()
            res_prec_entry.grid_remove()
            res_tol_entry.grid_remove()
            res_points_entry.grid_remove()
            res_formula_entry.grid_remove()
            #var_unit_myCombo.grid_remove()

    def unit_table(self, selected_unit):
        self.unit_to_ilias_code = { "H" : "125", "mH" : "126", "µH" : "127", "nH" : "128", "kH" : "129", "pH" : "130",
                                    "F" : "131", "mF" : "132", "µF" : "133", "nF" : "134", "kF" : "135",
                                    "W" : "136", "kW" : "137", "MW" : "138", "mW" : "149",
                                    "V" : "139", "kV" : "140", "mV" : "141", "µV" : "142", "MV" : "143",
                                    "A" : "144", "mA" : "145", "µA" : "146", "kA" : "147",
                                    "Ohm" : "148", "kOhm" : "150", "mOhm" : "151"}


        self.var_selected_unit = selected_unit
        self.selected_unit = self.unit_to_ilias_code[self.var_selected_unit]
        return self.selected_unit

    def ff_replace_character_in_xml_file(self, file_path_qti_xml):
        # Im Nachgang werden alle "&amp;" wieder gegen "&" getauscht
        # "&" Zeichen kann XML nicht verarbeiten, daher wurde beim schreiben der Texte in die XML "&" gegen "&amp;" getauscht

        # XML Datei zum lesen öffnen 'r' -> "read"
        with open(file_path_qti_xml, 'r') as xml_file:
            xml_str = xml_file.read()
        xml_str = xml_str.replace('&amp;', '&') #replace 'x' with 'new_x'

        # In XML Datei schreiben 'w" -> "write"
        with open(file_path_qti_xml, 'w') as replaced_xml_file:
            replaced_xml_file.write(xml_str)

        print("...XML_DATEI_QTI --  \"&amp;\"-ZEICHEN ÜBERARBEITUNG ABGESCHLOSSEN!")


    # Wertebereich berechnen (für bis zu 4 Variablen in akzeptabler Zeit)
    def ff_calculate_value_range_function_in_GUI(self, ids_in_entry_box):

        self.all_entries_from_db_list = []
        self.ff_test_entry_splitted = self.ff_calculate_value_range_id_entry.get().split(",")

        if self.ff_calculate_value_range_id_entry.get() == "" and self.ff_var_calculate_value_range_for_all_db_entries_check.get() == 0:
             # Formel ausrechnen, wenn eine im Eingabefeld vorhanden ist
            if self.res1_formula_entry.get() != "":
                Formelfrage.ff_calculate_value_range_from_formula_in_GUI(self, self.res1_formula_entry.get(), self.var_res_combined_min_entries_list, self.var_res_combined_max_entries_list, self.var_prec_entry_list,  self.res1_min_entry, self.res1_max_entry, self.res1_prec_entry, self.res_min_entry_list, self.res_max_entry_list, self.ff_var_calculate_value_range_for_all_db_entries_check.get())
            if self.res2_formula_entry.get() != "":
                Formelfrage.ff_calculate_value_range_from_formula_in_GUI(self, self.res2_formula_entry.get(), self.var_res_combined_min_entries_list, self.var_res_combined_max_entries_list, self.var_prec_entry_list,  self.res2_min_entry, self.res2_max_entry, self.res2_prec_entry, self.res_min_entry_list, self.res_max_entry_list, self.ff_var_calculate_value_range_for_all_db_entries_check.get())
            if self.res3_formula_entry.get() != "":
                Formelfrage.ff_calculate_value_range_from_formula_in_GUI(self, self.res3_formula_entry.get(), self.var_res_combined_min_entries_list, self.var_res_combined_max_entries_list, self.var_prec_entry_list,  self.res3_min_entry, self.res3_max_entry, self.res3_prec_entry, self.res_min_entry_list, self.res_max_entry_list, self.ff_var_calculate_value_range_for_all_db_entries_check.get())
            if self.res4_formula_entry.get() != "":
                Formelfrage.ff_calculate_value_range_from_formula_in_GUI(self, self.res4_formula_entry.get(), self.var_res_combined_min_entries_list, self.var_res_combined_max_entries_list, self.var_prec_entry_list,  self.res4_min_entry, self.res4_max_entry, self.res4_prec_entry, self.res_min_entry_list, self.res_max_entry_list, self.ff_var_calculate_value_range_for_all_db_entries_check.get())
            if self.res5_formula_entry.get() != "":
                Formelfrage.ff_calculate_value_range_from_formula_in_GUI(self, self.res5_formula_entry.get(), self.var_res_combined_min_entries_list, self.var_res_combined_max_entries_list, self.var_prec_entry_list,  self.res5_min_entry, self.res5_max_entry, self.res5_prec_entry, self.res_min_entry_list, self.res_max_entry_list, self.ff_var_calculate_value_range_for_all_db_entries_check.get())
            if self.res6_formula_entry.get() != "":
                Formelfrage.ff_calculate_value_range_from_formula_in_GUI(self, self.res6_formula_entry.get(), self.var_res_combined_min_entries_list, self.var_res_combined_max_entries_list, self.var_prec_entry_list,  self.res6_min_entry, self.res6_max_entry, self.res6_prec_entry, self.res_min_entry_list, self.res_max_entry_list, self.ff_var_calculate_value_range_for_all_db_entries_check.get())
            if self.res7_formula_entry.get() != "":
                Formelfrage.ff_calculate_value_range_from_formula_in_GUI(self, self.res7_formula_entry.get(), self.var_res_combined_min_entries_list, self.var_res_combined_max_entries_list, self.var_prec_entry_list,  self.res7_min_entry, self.res7_max_entry, self.res7_prec_entry, self.res_min_entry_list, self.res_max_entry_list, self.ff_var_calculate_value_range_for_all_db_entries_check.get())
            if self.res8_formula_entry.get() != "":
                Formelfrage.ff_calculate_value_range_from_formula_in_GUI(self, self.res8_formula_entry.get(), self.var_res_combined_min_entries_list, self.var_res_combined_max_entries_list, self.var_prec_entry_list,  self.res8_min_entry, self.res8_max_entry, self.res8_prec_entry, self.res_min_entry_list, self.res_max_entry_list, self.ff_var_calculate_value_range_for_all_db_entries_check.get())
            if self.res9_formula_entry.get() != "":
                Formelfrage.ff_calculate_value_range_from_formula_in_GUI(self, self.res9_formula_entry.get(), self.var_res_combined_min_entries_list, self.var_res_combined_max_entries_list, self.var_prec_entry_list,  self.res9_min_entry, self.res9_max_entry, self.res9_prec_entry, self.res_min_entry_list, self.res_max_entry_list, self.ff_var_calculate_value_range_for_all_db_entries_check.get())
            if self.res10_formula_entry.get() != "":
                Formelfrage.ff_calculate_value_range_from_formula_in_GUI(self, self.res10_formula_entry.get(), self.var_res_combined_min_entries_list, self.var_res_combined_max_entries_list, self.var_prec_entry_list,  self.res10_min_entry, self.res10_max_entry, self.res10_prec_entry, self.res_min_entry_list, self.res_max_entry_list, self.ff_var_calculate_value_range_for_all_db_entries_check.get())
        else:

            # Einzelne ID's berechnen
            if self.ff_calculate_value_range_id_entry.get() != "":
                self.ff_test_entry_splitted = self.ff_calculate_value_range_id_entry.get()

            # Alle ID's berechnen
            if self.ff_var_calculate_value_range_for_all_db_entries_check.get() == 1:

                # Für alle DB Einträge Wertebereich berechnen - popup
                # showinfo, showwarning, showerror, askquestion, askokcancel, askyesno
                self.response_calculate_value_for_all_db_entries = messagebox.askquestion("Wertebereich für DB Einträge berechnen", "ACHTUNG!\n\nEs werden für ALLE DB Einträge die Min/Max-Werte überschrieben!\n\nFortfahren?")

                if self.response_calculate_value_for_all_db_entries == "yes":

                    self.ff_test_entry_splitted = ids_in_entry_box.split(",")

                    conn = sqlite3.connect(self.database_formelfrage_path)
                    c = conn.cursor()
                    c.execute("SELECT *, oid FROM %s"  % self.ff_database_table)

                    ff_db_records = c.fetchall()

                    for ff_db_record in ff_db_records:
                        self.all_entries_from_db_list.append(int(ff_db_record[len(ff_db_record) - 1]))

                    self.string_temp = ','.join(map(str, self.all_entries_from_db_list))
                    self.ff_test_entry_splitted = self.string_temp.split(",")

                    # Eintrag mit ID "1" entspricht der Vorlage und soll nicht mit erstellt werden
                    #self.ff_test_entry_splitted.pop(0)

                else:
                    print("Vorgang abgebrochen")

            # Mit Datenbank verbinden
            conn = sqlite3.connect(self.database_formelfrage_path)
            cursor = conn.cursor()
            cursor.execute("SELECT *, oid FROM %s"  % self.ff_database_table)
            ff_db_records = cursor.fetchall()
            for i in range(len(self.ff_test_entry_splitted)):
                for ff_db_record in ff_db_records:
                    if str(ff_db_record[len(ff_db_record) - 1]) == self.ff_test_entry_splitted[i]:
                        Formelfrage.ff_clear_var_res_entries(self)

                        self.var1_min_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['var1_min']])
                        self.var1_max_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['var1_max']])
                        self.var1_prec_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['var1_prec']])

                        self.var2_min_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['var2_min']])
                        self.var2_max_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['var2_max']])
                        self.var2_prec_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['var2_prec']])

                        self.var3_min_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['var3_min']])
                        self.var3_max_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['var3_max']])
                        self.var3_prec_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['var3_prec']])

                        self.var4_min_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['var4_min']])
                        self.var4_max_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['var4_max']])
                        self.var4_prec_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['var4_prec']])

                        self.var5_min_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['var5_min']])
                        self.var5_max_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['var5_max']])
                        self.var5_prec_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['var5_prec']])

                        self.var6_min_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['var6_min']])
                        self.var6_max_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['var6_max']])
                        self.var6_prec_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['var6_prec']])

                        self.var7_min_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['var7_min']])
                        self.var7_max_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['var7_max']])
                        self.var7_prec_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['var7_prec']])

                        self.var8_min_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['var8_min']])
                        self.var8_max_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['var8_max']])
                        self.var8_prec_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['var8_prec']])

                        self.var9_min_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['var9_min']])
                        self.var9_max_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['var9_max']])
                        self.var9_prec_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['var9_prec']])

                        self.var10_min_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['var10_min']])
                        self.var10_max_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['var10_max']])
                        self.var10_prec_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['var10_prec']])

                        self.var11_min_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['var11_min']])
                        self.var11_max_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['var11_max']])
                        self.var11_prec_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['var11_prec']])

                        self.var12_min_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['var12_min']])
                        self.var12_max_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['var12_max']])
                        self.var12_prec_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['var12_prec']])

                        self.var13_min_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['var13_min']])
                        self.var13_max_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['var13_max']])
                        self.var13_prec_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['var13_prec']])

                        self.var14_min_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['var14_min']])
                        self.var14_max_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['var14_max']])
                        self.var14_prec_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['var14_prec']])

                        self.var15_min_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['var15_min']])
                        self.var15_max_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['var15_max']])
                        self.var15_prec_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['var15_prec']])


                        self.res1_formula_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['res1_formula']])
                        self.res1_min_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['res1_min']])
                        self.res1_max_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['res1_max']])
                        self.res1_prec_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['res1_prec']])

                        self.res2_formula_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['res2_formula']])
                        self.res2_min_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['res2_min']])
                        self.res2_max_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['res2_max']])
                        self.res2_prec_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['res2_prec']])

                        self.res3_formula_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['res3_formula']])
                        self.res3_min_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['res3_min']])
                        self.res3_max_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['res3_max']])
                        self.res3_prec_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['res3_prec']])

                        self.res4_formula_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['res4_formula']])
                        self.res4_min_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['res4_min']])
                        self.res4_max_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['res4_max']])
                        self.res4_prec_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['res4_prec']])

                        self.res5_formula_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['res5_formula']])
                        self.res5_min_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['res5_min']])
                        self.res5_max_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['res5_max']])
                        self.res5_prec_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['res5_prec']])

                        self.res6_formula_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['res6_formula']])
                        self.res6_min_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['res6_min']])
                        self.res6_max_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['res6_max']])
                        self.res6_prec_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['res6_prec']])

                        self.res7_formula_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['res7_formula']])
                        self.res7_min_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['res7_min']])
                        self.res7_max_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['res7_max']])
                        self.res7_prec_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['res7_prec']])

                        self.res8_formula_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['res8_formula']])
                        self.res8_min_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['res8_min']])
                        self.res8_max_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['res8_max']])
                        self.res8_prec_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['res8_prec']])

                        self.res9_formula_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['res9_formula']])
                        self.res9_min_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['res9_min']])
                        self.res9_max_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['res9_max']])
                        self.res9_prec_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['res9_prec']])

                        self.res10_formula_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['res10_formula']])
                        self.res10_min_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['res10_min']])
                        self.res10_max_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['res10_max']])
                        self.res10_prec_entry.insert(0, ff_db_record[self.ff_db_entry_to_index_dict['res10_prec']])

                        #print("INSERTED")

                        # Formel ausrechnen, wenn eine im Eingabefeld vorhanden ist
                        if self.res1_formula_entry.get() != "":
                            Formelfrage.ff_calculate_value_range_from_formula_in_GUI(self, self.res1_formula_entry.get(), self.var_res_combined_min_entries_list, self.var_res_combined_max_entries_list, self.var_prec_entry_list,  self.res1_min_entry, self.res1_max_entry, self.res1_prec_entry, self.res_min_entry_list, self.res_max_entry_list, self.ff_var_calculate_value_range_for_all_db_entries_check.get())
                        if self.res2_formula_entry.get() != "":
                            Formelfrage.ff_calculate_value_range_from_formula_in_GUI(self, self.res2_formula_entry.get(), self.var_res_combined_min_entries_list, self.var_res_combined_max_entries_list, self.var_prec_entry_list,  self.res2_min_entry, self.res2_max_entry, self.res2_prec_entry, self.res_min_entry_list, self.res_max_entry_list, self.ff_var_calculate_value_range_for_all_db_entries_check.get())
                        if self.res3_formula_entry.get() != "":
                            Formelfrage.ff_calculate_value_range_from_formula_in_GUI(self, self.res3_formula_entry.get(), self.var_res_combined_min_entries_list, self.var_res_combined_max_entries_list, self.var_prec_entry_list,  self.res3_min_entry, self.res3_max_entry, self.res3_prec_entry, self.res_min_entry_list, self.res_max_entry_list, self.ff_var_calculate_value_range_for_all_db_entries_check.get())
                        if self.res4_formula_entry.get() != "":
                            Formelfrage.ff_calculate_value_range_from_formula_in_GUI(self, self.res4_formula_entry.get(), self.var_res_combined_min_entries_list, self.var_res_combined_max_entries_list, self.var_prec_entry_list,  self.res4_min_entry, self.res4_max_entry, self.res4_prec_entry, self.res_min_entry_list, self.res_max_entry_list, self.ff_var_calculate_value_range_for_all_db_entries_check.get())
                        if self.res5_formula_entry.get() != "":
                            Formelfrage.ff_calculate_value_range_from_formula_in_GUI(self, self.res5_formula_entry.get(), self.var_res_combined_min_entries_list, self.var_res_combined_max_entries_list, self.var_prec_entry_list,  self.res5_min_entry, self.res5_max_entry, self.res5_prec_entry, self.res_min_entry_list, self.res_max_entry_list, self.ff_var_calculate_value_range_for_all_db_entries_check.get())
                        if self.res6_formula_entry.get() != "":
                            Formelfrage.ff_calculate_value_range_from_formula_in_GUI(self, self.res6_formula_entry.get(), self.var_res_combined_min_entries_list, self.var_res_combined_max_entries_list, self.var_prec_entry_list,  self.res6_min_entry, self.res6_max_entry, self.res6_prec_entry, self.res_min_entry_list, self.res_max_entry_list, self.ff_var_calculate_value_range_for_all_db_entries_check.get())
                        if self.res7_formula_entry.get() != "":
                            Formelfrage.ff_calculate_value_range_from_formula_in_GUI(self, self.res7_formula_entry.get(), self.var_res_combined_min_entries_list, self.var_res_combined_max_entries_list, self.var_prec_entry_list,  self.res7_min_entry, self.res7_max_entry, self.res7_prec_entry, self.res_min_entry_list, self.res_max_entry_list, self.ff_var_calculate_value_range_for_all_db_entries_check.get())
                        if self.res8_formula_entry.get() != "":
                            Formelfrage.ff_calculate_value_range_from_formula_in_GUI(self, self.res8_formula_entry.get(), self.var_res_combined_min_entries_list, self.var_res_combined_max_entries_list, self.var_prec_entry_list,  self.res8_min_entry, self.res8_max_entry, self.res8_prec_entry, self.res_min_entry_list, self.res_max_entry_list, self.ff_var_calculate_value_range_for_all_db_entries_check.get())
                        if self.res9_formula_entry.get() != "":
                            Formelfrage.ff_calculate_value_range_from_formula_in_GUI(self, self.res9_formula_entry.get(), self.var_res_combined_min_entries_list, self.var_res_combined_max_entries_list, self.var_prec_entry_list,  self.res9_min_entry, self.res9_max_entry, self.res9_prec_entry, self.res_min_entry_list, self.res_max_entry_list, self.ff_var_calculate_value_range_for_all_db_entries_check.get())
                        if self.res10_formula_entry.get() != "":
                            Formelfrage.ff_calculate_value_range_from_formula_in_GUI(self, self.res10_formula_entry.get(), self.var_res_combined_min_entries_list, self.var_res_combined_max_entries_list, self.var_prec_entry_list,  self.res10_min_entry, self.res10_max_entry, self.res10_prec_entry, self.res_min_entry_list, self.res_max_entry_list, self.ff_var_calculate_value_range_for_all_db_entries_check.get())

                        if self.ff_var_calculate_value_range_for_all_db_entries_check.get() == 1:
                            # Verbindung mit der Datenbank
                            conn = sqlite3.connect(self.database_formelfrage_path)
                            c = conn.cursor()

                            # sql_update_query = "UPDATE " + self.ff_database_table + " SET res1_min=?, res1_max=? WHERE id=?",( res_min_entry, res_max_entry, record_id)

                            for t in range(0, 10):
                                c.execute("UPDATE " + self.ff_database_table + " SET res" + str(t+1) + "_min=?, res" + str(t+1) + "_max=? WHERE oid=?", (self.var_res_combined_min_entries_list[t+15].get(), self.var_res_combined_max_entries_list[t+15].get(), self.ff_test_entry_splitted[i]))

                            conn.commit()
                            conn.close()



    def ff_calculate_value_range_replace_formula_numpy(self, formula, var_res_combined_min_entries_list, var_res_combined_max_entries_list, res_min_entries_list, res_max_entries_list):

        self.formula = formula
        self.formula_var_replaced = formula.replace('$', '_')
        self.formula_var_replaced = self.formula_var_replaced.replace('^', '**')


        self.np_variables_translator_dict = {"pi": "np.pi",
                                   ",": ".",
                                   "^": "**",
                                   "e": "*10**",

                                   "sin": "np.sin",
                                   "cos": "np.cos",
                                   "tan": "np.tan",
                                   "arcsin": "np.arcsin",
                                   "arccos": "np.arccos",
                                   "arctan": "np.arctan",

                                   "sinh": "np.sinh",
                                   "cosh": "np.cosh",
                                   "tanh": "np.tanh",
                                   "arcsinh": "np.arcsinh",
                                   "arccosh": "np.arccosh",
                                   "arctanh": "np.arctanh",

                                   "sqrt": "np.sqrt",
                                   "abs": "np.abs",
                                   "ln": "np.ln",
                                   "log": "np.log",

                                   "_v1": " row['a'] ",
                                   "_v2": " row['b'] ",
                                   "_v3": " row['c'] ",
                                   "_v4": " row['d'] ",
                                   "_v5": " row['e'] ",
                                   "_v6": " row['f'] ",
                                   "_v7": " row['g'] ",
                                   "_v8": " row['h'] ",
                                   "_v9": " row['i'] ",
                                   "_v10": " row['j'] ",
                                   "_v11": " row['k'] ",
                                   "_v12": " row['l'] ",
                                   "_v13": " row['m'] ",
                                   "_v14": " row['n'] ",
                                   "_v15": " row['o'] "}

        self.np_results_translator_dict = {

                                   "_r1": " row['p'] ",
                                   "_r2": " row['q'] ",
                                   "_r3": " row['r'] ",
                                   "_r4": " row['s'] ",
                                   "_r5": " row['t'] ",
                                   "_r6": " row['u'] ",
                                   "_r7": " row['v'] ",
                                   "_r8": " row['w'] ",
                                   "_r9": " row['x'] ",
                                   "_r10": " row['y'] "}

        print("----------------------")
        #print("Übernehme Formel aus Eingabefeld:")
        print("---> ", self.formula, end="", flush=True)
        #print("Prüfe auf Grenzen")


        def replace_var(match):
            return self.np_variables_translator_dict[match.group(0)]

        def replace_res(match):
            return self.np_results_translator_dict[match.group(0)]



        self.formula_var_replaced = re.sub('|'.join(r'\b%s\b' % re.escape(s) for s in self.np_variables_translator_dict),replace_var, self.formula_var_replaced)


        #for key in self.np_variables_translator_dict.keys():
        #    self.formula_var_replaced = self.formula_var_replaced.replace(key, self.np_variables_translator_dict[key])

        self.formula_res_replaced = re.sub('|'.join(r'\b%s\b' % re.escape(s) for s in self.np_results_translator_dict),replace_res, self.formula_var_replaced)


        print(" --- ", "NUMPY: ", self.formula_res_replaced)

        #for key in self.np_results_translator_dict.keys():
        #    self.formula_res_replaced = self.formula_res_replaced.replace(key, self.np_results_translator_dict[key])



        for i in range(len(var_res_combined_min_entries_list)):
            if "$v" + (str(i+1)) in formula and var_res_combined_min_entries_list[i].get() != "" and var_res_combined_max_entries_list[i].get() != "":
                self.formula = self.formula_var_replaced


                for j in range(len(res_min_entries_list)):
                    if "$r" + (str(j+1)) in formula:
                        if res_min_entries_list[j].get() != "" and res_max_entries_list[j].get() != "":

                            #print("Grenzen verfügbar! --> Ersetze alle Symbole mit numpy-symoblik")

                            self.formula = self.formula_res_replaced

                        else:
                            self.formula = "NaN"


            if "$r" + (str(i+1)) in formula and var_res_combined_min_entries_list[i].get() != "" and var_res_combined_max_entries_list[i].get() != "":
                self.formula = self.formula_res_replaced


        return self.formula


    def ff_calculate_value_range_from_formula_in_GUI(self, formula, var_res_combined_min_entries_list, var_res_combined_max_entries_list, var_prec_entries_list,  res_min_entry, res_max_entry, res_prec_entry, res_min_entries_list, res_max_entries_list, calculate_value_range_for_pool_check):


        def value_range_lower_upper_bounds(var_res_combined_min_entries_list, var_res_combined_max_entries_list, var_lower_bound_list, var_upper_bound_list):

                for u in range(len(var_res_combined_min_entries_list)):
                    if var_res_combined_min_entries_list[u] != "":
                        if bool(re.search(r'\d', var_res_combined_min_entries_list[u].get())) == True and bool(re.search(r'\d', var_res_combined_max_entries_list[u].get())) == True:
                            try:
                                var_lower_bound_list[u], var_upper_bound_list[u] = int(var_res_combined_min_entries_list[u].get()), int(var_res_combined_max_entries_list[u].get())
                            except ValueError:
                                var_lower_bound_list[u], var_upper_bound_list[u] = float(var_res_combined_min_entries_list[u].get()), float(var_res_combined_max_entries_list[u].get())
                        else:
                            var_lower_bound_list[u], var_upper_bound_list[u] = 0, 0

        def min_max(col):
            return pd.Series(index=['min', 'max'], data=[col.min(), col.max()])


        # Alle Formeln berechnen die KEIN $r enthalten (nur variablen)


        self.var1_lower, self.var1_upper = 0, 0
        self.var2_lower, self.var2_upper = 0, 0
        self.var3_lower, self.var3_upper = 0, 0
        self.var4_lower, self.var4_upper = 0, 0
        self.var5_lower, self.var5_upper = 0, 0
        self.var6_lower, self.var6_upper = 0, 0
        self.var7_lower, self.var7_upper = 0, 0
        self.var8_lower, self.var8_upper = 0, 0
        self.var9_lower, self.var9_upper = 0, 0
        self.var10_lower, self.var10_upper = 0, 0
        self.var11_lower, self.var11_upper = 0, 0
        self.var12_lower, self.var12_upper = 0, 0
        self.var13_lower, self.var13_upper = 0, 0
        self.var14_lower, self.var14_upper = 0, 0
        self.var15_lower, self.var15_upper = 0, 0

        self.res1_lower, self.res1_upper = 0, 0
        self.res2_lower, self.res2_upper = 0, 0
        self.res3_lower, self.res3_upper = 0, 0
        self.res4_lower, self.res4_upper = 0, 0
        self.res5_lower, self.res5_upper = 0, 0
        self.res6_lower, self.res6_upper = 0, 0
        self.res7_lower, self.res7_upper = 0, 0
        self.res8_lower, self.res8_upper = 0, 0
        self.res9_lower, self.res9_upper = 0, 0
        self.res10_lower, self.res10_upper = 0, 0



        self.new_list = []
        self.new_list2 = []
        self.set_nr_of_var_index = []

        self.var_prec_entry_list_values = []

        self.lower_list = [self.var1_lower, self.var2_lower, self.var3_lower, self.var4_lower, self.var5_lower,
                           self.var6_lower, self.var7_lower, self.var8_lower, self.var9_lower, self.var10_lower,
                           self.var11_lower, self.var12_lower, self.var13_lower, self.var14_lower, self.var15_lower,
                           self.res1_lower, self.res2_lower, self.res3_lower, self.res4_lower, self.res5_lower,
                           self.res6_lower, self.res7_lower, self.res8_lower, self.res9_lower, self.res10_lower]

        self.upper_list = [self.var1_upper, self.var2_upper, self.var3_upper, self.var4_upper, self.var5_upper,
                           self.var6_upper, self.var7_upper, self.var8_upper, self.var9_upper, self.var10_upper,
                           self.var11_upper, self.var12_upper, self.var13_upper, self.var14_upper, self.var15_upper,
                           self.res1_upper, self.res2_upper, self.res3_upper, self.res4_upper, self.res5_upper,
                           self.res6_upper, self.res7_upper, self.res8_upper, self.res9_upper, self.res10_upper]

        self.new_dict = {"row['a']": 'a',
                         "row['b']": 'b',
                         "row['c']": 'c',
                         "row['d']": 'd',
                         "row['e']": 'e',
                         "row['f']": 'f',
                         "row['g']": 'g',
                         "row['h']": 'h',
                         "row['i']": 'i',
                         "row['j']": 'j',
                         "row['k']": 'k',
                         "row['l']": 'l',
                         "row['m']": 'm',
                         "row['n']": 'n',
                         "row['o']": 'o',
                         "row['p']": 'p',
                         "row['q']": 'q',
                         "row['r']": 'r',
                         "row['s']": 's',
                         "row['t']": 't',
                         "row['u']": 'u',
                         "row['v']": 'v',
                         "row['w']": 'w',
                         "row['x']": 'x',
                         "row['y']": 'y' }
        
        self.list_index_dict = {'a': 0,
                                'b': 1,
                                'c': 2,
                                'd': 3,
                                'e': 4,
                                'f': 5,
                                'g': 6,
                                'h': 7,
                                'i': 8,
                                'j': 9,
                                'k': 10,
                                'l': 11,
                                'm': 12,
                                'n': 13,
                                'o': 14,
                                'p': 15,
                                'q': 16,
                                'r': 17,
                                's': 18,
                                't': 19,
                                'u': 20,
                                'v': 21,
                                'w': 22,
                                'x': 23,
                                'y': 24,
                                }

        values = []

        # Number of values per range
        N = 5

        # ersetzt formel durch numpy expressions: z.B. 2^5 -> 2**5, $v1*2+$v3 -> row[a] *2+ row[c]
        self.formula_1_numpy_expression = Formelfrage.ff_calculate_value_range_replace_formula_numpy(self, formula, var_res_combined_min_entries_list, var_res_combined_max_entries_list, res_min_entries_list, res_max_entries_list)


        if self.formula_1_numpy_expression != None and self.formula_1_numpy_expression != "NaN":

            # neue formel wird nach leerzeichen gesplittet um einzelne 'row[a]' durch 'a' zu ersetzen
            self.new_list = self.formula_1_numpy_expression.split(' ')




            self.exp_as_func = eval('lambda row: ' + self.formula_1_numpy_expression)

            # self.exp_as_func is not iterable, therefore it is assigned to function[]
            functions = [self.exp_as_func]

            value_range_lower_upper_bounds(var_res_combined_min_entries_list, var_res_combined_max_entries_list, self.lower_list, self.upper_list)



            # ersetzen: 'row[a]' -> 'a' als neue Liste
            for i in range(len(self.new_list)):
                if "row" in self.new_list[i]:
                    if self.new_dict[self.new_list[i]] not in self.new_list2:
                        self.new_list2.append(self.new_dict[self.new_list[i]])

            self.set_nr_of_var_index = sorted(self.new_list2)

            self.max_index_nr = self.list_index_dict[self.set_nr_of_var_index[-1]] + 1


            # Berechnung der Formel. "linspace" erstellt "N" Werte zwischen zwei Grenzen -> linspace(0,10,N) N=11 --> 0,1,2,3,4,5,6,7,8,9,10
            for p in range(len(self.set_nr_of_var_index)):
                values.append(np.linspace(self.lower_list[self.list_index_dict[self.set_nr_of_var_index[p]]], self.upper_list[self.list_index_dict[self.set_nr_of_var_index[p]]], N))


            df = pd.DataFrame(cartesian_product(values), index=self.set_nr_of_var_index).T



            if res_prec_entry.get() != "":
                self.var_prec_highest_value = res_prec_entry.get()
            else:
                for i in range(len(var_prec_entries_list)):
                    self.var_prec_entry_list_values.append(var_prec_entries_list[i].get())

                self.var_prec_highest_value = max(self.var_prec_entry_list_values)





            #pd.options.display.float_format = '{:,.3f}'.format


            for i, f in enumerate(functions):
                df[f'f_{i + 1}'] = df.apply(f, axis=1)


            df1 = df.apply(pd.to_numeric, errors='coerce')

            #print(df1)
            #print()
            print(" --- ", "min: ", df1.apply(min_max).iloc[0]['f_1'], " max: ",df1.apply(min_max).iloc[1]['f_1'])
            #print(df1.apply(min_max).iloc[0]['f_1'])
            #print(df1.apply(min_max).iloc[1]['f_1'])
            #print("////////////////////////")


            self.res_min_calc_value = df1.apply(min_max).iloc[0]['f_1']
            self.res_max_calc_value = df1.apply(min_max).iloc[1]['f_1']




            #"{:.2f}".format(a_float)
            res_min_entry.delete(0, END)
            res_min_entry.insert(END, str("{:.2f}".format(self.res_min_calc_value)))
            res_max_entry.delete(0, END)
            res_max_entry.insert(END, str(self.res_max_calc_value))





            # Prüfen ob $r.. in Formeln enthalten
            for i in range(len(self.res_formula_entry_list)):
                for j in range(1,10):
                    if "$r" + str(j) in str(self.res_formula_entry_list[i].get()):
                        print("$r" + str(j) + " found!", self.res_formula_entry_list[i].get())

                        if self.res_min_entry_list[j-1].get() != "" and self.res_max_entry_list[j-1].get() != "":
                            print("---", self.res_min_entry_list[j-1].get(), self.res_max_entry_list[j-1].get())




#############  DATENBANK FUNKTIONEN
    def ff_save_id_to_db(self, ff_database_table, column_names_string):

        self.ff_database_table = ff_database_table
        self.column_names_string = column_names_string

        conn = sqlite3.connect(self.database_formelfrage_path)
        c =conn.cursor()


        # format of duration P0Y0M0DT0H30M0S
        self.ff_test_time = "P0Y0M0DT" + self.ff_proc_hours_box.get() + "H" + self.ff_proc_minutes_box.get() + "M" + self.ff_proc_seconds_box.get() + "S"


        # Bild 1
        if self.ff_description_img_name_1 != "" and self.ff_description_img_name_1 != "EMPTY":
            # read image data in byte format
            with open(self.ff_description_img_path_1, 'rb') as image_file_1:
                self.ff_description_img_data_1 = image_file_1.read()


        else:
            self.ff_description_img_name_1 = ""
            self.ff_description_img_path_1 = ""
            self.ff_description_img_data_1 = ""


        # Bild 2
        if self.ff_description_img_name_2 != "" and self.ff_description_img_name_2 != "EMPTY":
            # read image data in byte format
            with open(self.ff_description_img_path_2, 'rb') as image_file_2:
                self.ff_description_img_data_2 = image_file_2.read()


        else:
            self.ff_description_img_name_2 = ""
            self.ff_description_img_path_2 = ""
            self.ff_description_img_data_2 = ""


        # Bild 3
        if self.ff_description_img_name_3 != "" and self.ff_description_img_name_3 != "EMPTY":

            # read image data in byte format
            with open(self.ff_description_img_path_3, 'rb') as image_file_3:
                self.ff_description_img_data_3 = image_file_3.read()


        else:
            self.ff_description_img_name_3 = ""
            self.ff_description_img_path_3 = ""
            self.ff_description_img_data_3 = ""


        ########### Prüfen ob Fragen-TItel oder Fragen-ID bereits in DB vorhanden ####
        c.execute("SELECT *, oid FROM " + self.ff_database_table)
        db_records = c.fetchall()
        self.db_records_fragen_titel_list = []
        self.db_records_fragen_id_list = []
        self.temp_list = []
        self.temp2_list = []
        self.temp_string = ""
        for db_record in db_records:
            self.db_records_fragen_titel_list.append(db_record[self.ff_db_entry_to_index_dict['question_title']])
            self.temp_list = db_record[self.ff_db_entry_to_index_dict['question_title']].split(' ')
            self.db_records_fragen_id_list.append(self.temp_list[0])

        print("\n")

        if self.ff_question_title_entry.get() in self.db_records_fragen_titel_list:
            print(" -----> ACHTUNG! Fragentitel: \"" + str(self.ff_question_title_entry.get()) + "\" befindet sich bereits in der Datenbank")

        self.temp2_list = self.ff_question_title_entry.get().split(' ')
        self.temp_string = self.temp2_list[0]

        if self.temp_string in self.db_records_fragen_id_list:
            print(" -----> ACHTUNG! Fragen-ID: \"" + str(self.temp_string) + "\" befindet sich bereits in der Datenbank")

        print("\n")

        #############

        # Insert into Table
        c.execute(
            "INSERT INTO " + self.ff_database_table + " VALUES (" + self.ff_db_column_names_string + ")",
            {
                'question_difficulty': self.ff_question_difficulty_entry.get(),
                'question_category': self.ff_question_category_entry.get(),
                'question_type': self.ff_question_type_entry.get(),

                'question_title': self.ff_question_title_entry.get(),
                'question_description_title': self.ff_question_description_title_entry.get(),

                # The first part, "1.0" means that the input should be read from line one, character zero (ie: the very first character).
                # END is an imported constant which is set to the string "end". The END part means to read until the end of the text box is reached.
                # The only issue with this is that it actually adds a newline to our input. "
                # "So, in order to fix it we should change END to end-1c(Thanks Bryan Oakley) The -1c deletes 1 character, while -2c would mean delete two characters, and so on."
                'question_description_main': self.ff_question_description_main_entry.get("1.0", 'end-1c'),

                'res1_formula': self.res1_formula_entry.get(),
                'res2_formula': self.res2_formula_entry.get(),
                'res3_formula': self.res3_formula_entry.get(),
                'res4_formula': self.res4_formula_entry.get(),
                'res5_formula': self.res5_formula_entry.get(),
                'res6_formula': self.res6_formula_entry.get(),
                'res7_formula': self.res7_formula_entry.get(),
                'res8_formula': self.res8_formula_entry.get(),
                'res9_formula': self.res9_formula_entry.get(),
                'res10_formula': self.res10_formula_entry.get(),

                'var1_name': self.var1_name_entry.get(),
                'var1_min': self.var1_min_entry.get(),
                'var1_max': self.var1_max_entry.get(),
                'var1_prec': self.var1_prec_entry.get(),
                'var1_divby': self.var1_divby_entry.get(),
                'var1_unit': "",

                'var2_name': self.var2_name_entry.get(),
                'var2_min': self.var2_min_entry.get(),
                'var2_max': self.var2_max_entry.get(),
                'var2_prec': self.var2_prec_entry.get(),
                'var2_divby': self.var2_divby_entry.get(),
                'var2_unit': "",

                'var3_name': self.var3_name_entry.get(),
                'var3_min': self.var3_min_entry.get(),
                'var3_max': self.var3_max_entry.get(),
                'var3_prec': self.var3_prec_entry.get(),
                'var3_divby': self.var3_divby_entry.get(),
                'var3_unit': "",

                'var4_name': self.var4_name_entry.get(),
                'var4_min': self.var4_min_entry.get(),
                'var4_max': self.var4_max_entry.get(),
                'var4_prec': self.var4_prec_entry.get(),
                'var4_divby': self.var4_divby_entry.get(),
                'var4_unit': "",

                'var5_name': self.var5_name_entry.get(),
                'var5_min': self.var5_min_entry.get(),
                'var5_max': self.var5_max_entry.get(),
                'var5_prec': self.var5_prec_entry.get(),
                'var5_divby': self.var5_divby_entry.get(),
                'var5_unit': "",

                'var6_name': self.var6_name_entry.get(),
                'var6_min': self.var6_min_entry.get(),
                'var6_max': self.var6_max_entry.get(),
                'var6_prec': self.var6_prec_entry.get(),
                'var6_divby': self.var6_divby_entry.get(),
                'var6_unit': "",

                'var7_name': self.var7_name_entry.get(),
                'var7_min': self.var7_min_entry.get(),
                'var7_max': self.var7_max_entry.get(),
                'var7_prec': self.var7_prec_entry.get(),
                'var7_divby': self.var7_divby_entry.get(),
                'var7_unit': "",

                'var8_name': self.var8_name_entry.get(),
                'var8_min': self.var8_min_entry.get(),
                'var8_max': self.var8_max_entry.get(),
                'var8_prec': self.var8_prec_entry.get(),
                'var8_divby': self.var8_divby_entry.get(),
                'var8_unit': "",

                'var9_name': self.var9_name_entry.get(),
                'var9_min': self.var9_min_entry.get(),
                'var9_max': self.var9_max_entry.get(),
                'var9_prec': self.var9_prec_entry.get(),
                'var9_divby': self.var9_divby_entry.get(),
                'var9_unit': "",

                'var10_name': self.var10_name_entry.get(),
                'var10_min': self.var10_min_entry.get(),
                'var10_max': self.var10_max_entry.get(),
                'var10_prec': self.var10_prec_entry.get(),
                'var10_divby': self.var10_divby_entry.get(),
                'var10_unit': "",

                'var11_name': self.var11_name_entry.get(),
                'var11_min': self.var11_min_entry.get(),
                'var11_max': self.var11_max_entry.get(),
                'var11_prec': self.var11_prec_entry.get(),
                'var11_divby': self.var11_divby_entry.get(),
                'var11_unit': "",

                'var12_name': self.var12_name_entry.get(),
                'var12_min': self.var12_min_entry.get(),
                'var12_max': self.var12_max_entry.get(),
                'var12_prec': self.var12_prec_entry.get(),
                'var12_divby': self.var12_divby_entry.get(),
                'var12_unit': "",

                'var13_name': self.var13_name_entry.get(),
                'var13_min': self.var13_min_entry.get(),
                'var13_max': self.var13_max_entry.get(),
                'var13_prec': self.var13_prec_entry.get(),
                'var13_divby': self.var13_divby_entry.get(),
                'var13_unit': "",

                'var14_name': self.var14_name_entry.get(),
                'var14_min': self.var14_min_entry.get(),
                'var14_max': self.var14_max_entry.get(),
                'var14_prec': self.var14_prec_entry.get(),
                'var14_divby': self.var14_divby_entry.get(),
                'var14_unit': "",

                'var15_name': self.var15_name_entry.get(),
                'var15_min': self.var15_min_entry.get(),
                'var15_max': self.var15_max_entry.get(),
                'var15_prec': self.var15_prec_entry.get(),
                'var15_divby': self.var15_divby_entry.get(),
                'var15_unit': "",


                'res1_name': self.res1_name_entry.get(),
                'res1_min': self.res1_min_entry.get(),
                'res1_max': self.res1_max_entry.get(),
                'res1_prec': self.res1_prec_entry.get(),
                'res1_tol': self.res1_tol_entry.get(),
                'res1_points': self.res1_points_entry.get(),
                'res1_unit': "",

                'res2_name': self.res2_name_entry.get(),
                'res2_min': self.res2_min_entry.get(),
                'res2_max': self.res2_max_entry.get(),
                'res2_prec': self.res2_prec_entry.get(),
                'res2_tol': self.res2_tol_entry.get(),
                'res2_points': self.res2_points_entry.get(),
                'res2_unit': "",

                'res3_name': self.res3_name_entry.get(),
                'res3_min': self.res3_min_entry.get(),
                'res3_max': self.res3_max_entry.get(),
                'res3_prec': self.res3_prec_entry.get(),
                'res3_tol': self.res3_tol_entry.get(),
                'res3_points': self.res3_points_entry.get(),
                'res3_unit': "",

                'res4_name': self.res4_name_entry.get(),
                'res4_min': self.res4_min_entry.get(),
                'res4_max': self.res4_max_entry.get(),
                'res4_prec': self.res4_prec_entry.get(),
                'res4_tol': self.res4_tol_entry.get(),
                'res4_points': self.res4_points_entry.get(),
                'res4_unit': "",

                'res5_name': self.res5_name_entry.get(),
                'res5_min': self.res5_min_entry.get(),
                'res5_max': self.res5_max_entry.get(),
                'res5_prec': self.res5_prec_entry.get(),
                'res5_tol': self.res5_tol_entry.get(),
                'res5_points': self.res5_points_entry.get(),
                'res5_unit': "",

                'res6_name': self.res6_name_entry.get(),
                'res6_min': self.res6_min_entry.get(),
                'res6_max': self.res6_max_entry.get(),
                'res6_prec': self.res6_prec_entry.get(),
                'res6_tol': self.res6_tol_entry.get(),
                'res6_points': self.res6_points_entry.get(),
                'res6_unit': "",

                'res7_name': self.res7_name_entry.get(),
                'res7_min': self.res7_min_entry.get(),
                'res7_max': self.res7_max_entry.get(),
                'res7_prec': self.res7_prec_entry.get(),
                'res7_tol': self.res7_tol_entry.get(),
                'res7_points': self.res7_points_entry.get(),
                'res7_unit': "",

                'res8_name': self.res8_name_entry.get(),
                'res8_min': self.res8_min_entry.get(),
                'res8_max': self.res8_max_entry.get(),
                'res8_prec': self.res8_prec_entry.get(),
                'res8_tol': self.res8_tol_entry.get(),
                'res8_points': self.res8_points_entry.get(),
                'res8_unit': "",

                'res9_name': self.res9_name_entry.get(),
                'res9_min': self.res9_min_entry.get(),
                'res9_max': self.res9_max_entry.get(),
                'res9_prec': self.res9_prec_entry.get(),
                'res9_tol': self.res9_tol_entry.get(),
                'res9_points': self.res9_points_entry.get(),
                'res9_unit': "",

                'res10_name': self.res10_name_entry.get(),
                'res10_min': self.res10_min_entry.get(),
                'res10_max': self.res10_max_entry.get(),
                'res10_prec': self.res10_prec_entry.get(),
                'res10_tol': self.res10_tol_entry.get(),
                'res10_points': self.res10_points_entry.get(),
                'res10_unit': "",

                'description_img_name_1': self.ff_description_img_name_1,
                'description_img_data_1': self.ff_description_img_data_1,
                'description_img_path_1': self.ff_description_img_path_1,

                'description_img_name_2': self.ff_description_img_name_2,
                'description_img_data_2': self.ff_description_img_data_2,
                'description_img_path_2': self.ff_description_img_path_2,

                'description_img_name_3': self.ff_description_img_name_3,
                'description_img_data_3': self.ff_description_img_data_3,
                'description_img_path_3': self.ff_description_img_path_3,

                'test_time': self.ff_test_time,
                'var_number': self.ff_numbers_of_answers_box.get(),
                'res_number': self.ff_numbers_of_results_box.get(),
                'question_pool_tag': self.ff_question_pool_tag_entry.get(),
                'question_author': self.ff_question_author_entry.get()
            })


        conn.commit()
        conn.close()

        print("Neuer Eintrag in die Formelfrage-Datenbank --> Fragentitel: " + str(self.ff_question_title_entry.get()))

    def ff_load_id_from_db(self, entry_to_index_dict):
        self.ff_db_entry_to_index_dict = entry_to_index_dict
        conn = sqlite3.connect(self.database_formelfrage_path)
        c = conn.cursor()
        record_id = self.ff_load_box.get()

        self.ff_hidden_edit_box_entry.delete(0, END)
        self.ff_hidden_edit_box_entry.insert(0, self.ff_load_box.get())

        c.execute("SELECT * FROM %s WHERE oid = %s " % (self.ff_database_table, str(record_id)))
        ff_db_records = c.fetchall()


        Formelfrage.ff_clear_GUI(self)


        for ff_db_record in ff_db_records:
            self.ff_question_difficulty_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['question_difficulty']] )
            self.ff_question_category_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['question_category']])

            self.ff_question_type_entry.delete(0, END)
            self.ff_question_type_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['question_type']])

            self.ff_question_title_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['question_title']])
            self.ff_question_description_title_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['question_description_title']])
            self.ff_question_description_main_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['question_description_main']])

            self.res1_formula_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res1_formula']])
            self.res2_formula_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res2_formula']])
            self.res3_formula_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res3_formula']])
            self.res4_formula_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res4_formula']])
            self.res5_formula_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res5_formula']])
            self.res6_formula_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res6_formula']])
            self.res7_formula_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res7_formula']])
            self.res8_formula_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res8_formula']])
            self.res9_formula_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res9_formula']])
            self.res10_formula_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res10_formula']])

            self.var1_name_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var1_name']])
            self.var1_min_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var1_min']])
            self.var1_max_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var1_max']])
            self.var1_prec_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var1_prec']])
            self.var1_divby_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var1_divby']])


            self.var2_name_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var2_name']])
            self.var2_min_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var2_min']])
            self.var2_max_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var2_max']])
            self.var2_prec_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var2_prec']])
            self.var2_divby_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var2_divby']])


            self.var3_name_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var3_name']])
            self.var3_min_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var3_min']])
            self.var3_max_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var3_max']])
            self.var3_prec_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var3_prec']])
            self.var3_divby_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var3_divby']])


            self.var4_name_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var4_name']])
            self.var4_min_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var4_min']])
            self.var4_max_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var4_max']])
            self.var4_prec_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var4_prec']])
            self.var4_divby_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var4_divby']])


            self.var5_name_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var5_name']])
            self.var5_min_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var5_min']])
            self.var5_max_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var5_max']])
            self.var5_prec_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var5_prec']])
            self.var5_divby_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var5_divby']])


            self.var6_name_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var6_name']])
            self.var6_min_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var6_min']])
            self.var6_max_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var6_max']])
            self.var6_prec_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var6_prec']])
            self.var6_divby_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var6_divby']])


            self.var7_name_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var7_name']])
            self.var7_min_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var7_min']])
            self.var7_max_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var7_max']])
            self.var7_prec_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var7_prec']])
            self.var7_divby_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var7_divby']])


            self.var8_name_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var8_name']])
            self.var8_min_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var8_min']])
            self.var8_max_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var8_max']])
            self.var8_prec_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var8_prec']])
            self.var8_divby_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var8_divby']])


            self.var9_name_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var9_name']])
            self.var9_min_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var9_min']])
            self.var9_max_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var9_max']])
            self.var9_prec_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var9_prec']])
            self.var9_divby_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var9_divby']])


            self.var10_name_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var10_name']])
            self.var10_min_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var10_min']])
            self.var10_max_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var10_max']])
            self.var10_prec_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var10_prec']])
            self.var10_divby_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var10_divby']])

            self.var11_name_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var11_name']])
            self.var11_min_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var11_min']])
            self.var11_max_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var11_max']])
            self.var11_prec_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var11_prec']])
            self.var11_divby_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var11_divby']])

            self.var12_name_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var12_name']])
            self.var12_min_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var12_min']])
            self.var12_max_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var12_max']])
            self.var12_prec_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var12_prec']])
            self.var12_divby_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var12_divby']])

            self.var13_name_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var13_name']])
            self.var13_min_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var13_min']])
            self.var13_max_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var13_max']])
            self.var13_prec_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var13_prec']])
            self.var13_divby_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var13_divby']])

            self.var14_name_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var14_name']])
            self.var14_min_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var14_min']])
            self.var14_max_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var14_max']])
            self.var14_prec_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var14_prec']])
            self.var14_divby_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var14_divby']])

            self.var15_name_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var15_name']])
            self.var15_min_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var15_min']])
            self.var15_max_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var15_max']])
            self.var15_prec_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var15_prec']])
            self.var15_divby_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var15_divby']])


            self.res1_name_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res1_name']])
            self.res1_min_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res1_min']])
            self.res1_max_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res1_max']])
            self.res1_prec_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res1_prec']])
            self.res1_tol_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res1_tol']])
            self.res1_points_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res1_points']])


            self.res2_name_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res2_name']])
            self.res2_min_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res2_min']])
            self.res2_max_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res2_max']])
            self.res2_prec_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res2_prec']])
            self.res2_tol_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res2_tol']])
            self.res2_points_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res2_points']])


            self.res3_name_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res3_name']])
            self.res3_min_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res3_min']])
            self.res3_max_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res3_max']])
            self.res3_prec_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res3_prec']])
            self.res3_tol_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res3_tol']])
            self.res3_points_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res3_points']])


            self.res4_name_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res4_name']])
            self.res4_min_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res4_min']])
            self.res4_max_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res4_max']])
            self.res4_prec_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res4_prec']])
            self.res4_tol_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res4_tol']])
            self.res4_points_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res4_points']])


            self.res5_name_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res5_name']])
            self.res5_min_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res5_min']])
            self.res5_max_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res5_max']])
            self.res5_prec_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res5_prec']])
            self.res5_tol_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res5_tol']])
            self.res5_points_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res5_points']])


            self.res6_name_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res6_name']])
            self.res6_min_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res6_min']])
            self.res6_max_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res6_max']])
            self.res6_prec_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res6_prec']])
            self.res6_tol_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res6_tol']])
            self.res6_points_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res6_points']])


            self.res7_name_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res7_name']])
            self.res7_min_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res7_min']])
            self.res7_max_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res7_max']])
            self.res7_prec_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res7_prec']])
            self.res7_tol_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res7_tol']])
            self.res7_points_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res7_points']])


            self.res8_name_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res8_name']])
            self.res8_min_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res8_min']])
            self.res8_max_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res8_max']])
            self.res8_prec_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res8_prec']])
            self.res8_tol_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res8_tol']])
            self.res8_points_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res8_points']])


            self.res9_name_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res9_name']])
            self.res9_min_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res9_min']])
            self.res9_max_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res9_max']])
            self.res9_prec_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res9_prec']])
            self.res9_tol_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res9_tol']])
            self.res9_points_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res9_points']])


            self.res10_name_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res10_name']])
            self.res10_min_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res10_min']])
            self.res10_max_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res10_max']])
            self.res10_prec_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res10_prec']])
            self.res10_tol_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res10_tol']])
            self.res10_points_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res10_points']])

            self.ff_description_img_name_1 = ff_db_record[self.ff_db_entry_to_index_dict['description_img_name_1']]
            self.ff_description_img_data_1 = ff_db_record[self.ff_db_entry_to_index_dict['description_img_data_1']]
            self.ff_description_img_path_1 = ff_db_record[self.ff_db_entry_to_index_dict['description_img_path_1']]

            self.ff_description_img_name_2 = ff_db_record[self.ff_db_entry_to_index_dict['description_img_name_2']]
            self.ff_description_img_data_2 = ff_db_record[self.ff_db_entry_to_index_dict['description_img_data_2']]
            self.ff_description_img_path_2 = ff_db_record[self.ff_db_entry_to_index_dict['description_img_path_2']]

            self.ff_description_img_name_3 = ff_db_record[self.ff_db_entry_to_index_dict['description_img_name_3']]
            self.ff_description_img_data_3 = ff_db_record[self.ff_db_entry_to_index_dict['description_img_data_3']]
            self.ff_description_img_path_3 = ff_db_record[self.ff_db_entry_to_index_dict['description_img_path_3']]

            self.ff_question_pool_tag_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['question_pool_tag']])

        conn.commit()
        conn.close()


        if self.ff_var_highlight_question_text.get() == 1:
            print("Frage wird MIT Text-Formatierung geladen. --> Fragen-ID: " + str(self.ff_load_box.get()))
            test_generator_modul_taxonomie_und_textformatierung.Textformatierung.reallocate_text(self, self.ff_question_description_main_entry)

        else:
            print("Frage wird OHNE Text-Formatierung geladen. --> Fragen-ID: " + str(self.ff_load_box.get()))

    def ff_edit_id_from_db(self):

        # Verbindung mit der Datenbank
        conn = sqlite3.connect(self.database_formelfrage_path)
        c = conn.cursor()

        # ID der Frage aus dem Eingabefeld "ID editieren" auslesen
        # Eingabefeld ist für den User nicht sichtbar
        record_id = self.ff_hidden_edit_box_entry.get()

        # Format von Testdauer in der XML Datei:  P0Y0M0DT0H30M0S
        self.ff_test_time = "P0Y0M0DT" + self.ff_proc_hours_box.get() + "H" + self.ff_proc_minutes_box.get() + "M" + self.ff_proc_seconds_box.get() + "S"

        # Ist ein Bild-Name vorhanden, dann das Bild über den Pfad einlesen
        # Sonst auf "" setzen
        # Bilder werden als byte eingelesen "rb" = read byte

        # Fragen-Text Bild 1
        if self.ff_description_img_name_1 != "" and self.ff_description_img_name_1 != "EMPTY":
            with open(os.path.join(self.project_root_path, self.ff_description_img_path_1), 'rb') as description_image_file_1:
                self.ff_description_img_data_1 = description_image_file_1.read()

        else:
            self.ff_description_img_name_1 = ""
            self.ff_description_img_data_1 = ""
            self.ff_description_img_path_1 = ""

        # Fragen-Text Bild 2
        if self.ff_description_img_name_2 != "" and self.ff_description_img_name_2 != "EMPTY":
            with open( self.ff_description_img_path_2, 'rb') as description_image_file_2:
                self.ff_description_img_data_2 = description_image_file_2.read()

        else:
            self.ff_description_img_name_2 = ""
            self.ff_description_img_data_2 = ""
            self.ff_description_img_path_2 = ""

        # Fragen-Text Bild 3
        if self.ff_description_img_name_3 != "" and self.ff_description_img_name_3 != "EMPTY":
            with open( self.ff_description_img_path_3, 'rb') as description_image_file_3:
                self.ff_description_img_data_3 = description_image_file_3.read()

        else:
            self.ff_description_img_name_3 = ""
            self.ff_description_img_data_3 = ""
            self.ff_description_img_path_3 = ""



        self.edit_list = []
        for i in range(len(self.ff_db_column_names_list)):
            self.edit_list.append(self.ff_db_column_names_list[i] + " = :" + self.ff_db_column_names_list[i])
        self.db_column_names_string_for_edit = ','.join(self.edit_list)
        print("''''''''''''''", self.db_column_names_string_for_edit)


        c.execute("UPDATE " + self.ff_database_table + " SET " + self.db_column_names_string_for_edit + " WHERE oid = :oid",
                {'question_difficulty': self.ff_question_difficulty_entry.get(),
                 'question_category': self.ff_question_category_entry.get(),
                 'question_type': self.ff_question_type_entry.get(),

                 'question_title': self.ff_question_title_entry.get(),
                 'question_description_title': self.ff_question_description_title_entry.get(),
                 'question_description_main': self.ff_question_description_main_entry.get("1.0", 'end-1c'),

                 'res1_formula': self.res1_formula_entry.get(),
                 'res2_formula': self.res2_formula_entry.get(),
                 'res3_formula': self.res3_formula_entry.get(),
                 'res4_formula': self.res4_formula_entry.get(),
                 'res5_formula': self.res5_formula_entry.get(),
                 'res6_formula': self.res6_formula_entry.get(),
                 'res7_formula': self.res7_formula_entry.get(),
                 'res8_formula': self.res8_formula_entry.get(),
                 'res9_formula': self.res9_formula_entry.get(),
                 'res10_formula': self.res10_formula_entry.get(),

                 'var1_name': self.var1_name_entry.get(),
                 'var1_min': self.var1_min_entry.get(),
                 'var1_max': self.var1_max_entry.get(),
                 'var1_prec': self.var1_prec_entry.get(),
                 'var1_divby': self.var1_divby_entry.get(),
                 'var1_unit': "",

                 'var2_name': self.var2_name_entry.get(),
                 'var2_min': self.var2_min_entry.get(),
                 'var2_max': self.var2_max_entry.get(),
                 'var2_prec': self.var2_prec_entry.get(),
                 'var2_divby': self.var2_divby_entry.get(),
                 'var2_unit': "",

                 'var3_name': self.var3_name_entry.get(),
                 'var3_min': self.var3_min_entry.get(),
                 'var3_max': self.var3_max_entry.get(),
                 'var3_prec': self.var3_prec_entry.get(),
                 'var3_divby': self.var3_divby_entry.get(),
                 'var3_unit': "",

                 'var4_name': self.var4_name_entry.get(),
                 'var4_min': self.var4_min_entry.get(),
                 'var4_max': self.var4_max_entry.get(),
                 'var4_prec': self.var4_prec_entry.get(),
                 'var4_divby': self.var4_divby_entry.get(),
                 'var4_unit': "",

                 'var5_name': self.var5_name_entry.get(),
                 'var5_min': self.var5_min_entry.get(),
                 'var5_max': self.var5_max_entry.get(),
                 'var5_prec': self.var5_prec_entry.get(),
                 'var5_divby': self.var5_divby_entry.get(),
                 'var5_unit': "",

                 'var6_name': self.var6_name_entry.get(),
                 'var6_min': self.var6_min_entry.get(),
                 'var6_max': self.var6_max_entry.get(),
                 'var6_prec': self.var6_prec_entry.get(),
                 'var6_divby': self.var6_divby_entry.get(),
                 'var6_unit': "",

                 'var7_name': self.var7_name_entry.get(),
                 'var7_min': self.var7_min_entry.get(),
                 'var7_max': self.var7_max_entry.get(),
                 'var7_prec': self.var7_prec_entry.get(),
                 'var7_divby': self.var7_divby_entry.get(),
                 'var7_unit': "",

                 'var8_name': self.var8_name_entry.get(),
                 'var8_min': self.var8_min_entry.get(),
                 'var8_max': self.var8_max_entry.get(),
                 'var8_prec': self.var8_prec_entry.get(),
                 'var8_divby': self.var8_divby_entry.get(),
                 'var8_unit': "",

                 'var9_name': self.var9_name_entry.get(),
                 'var9_min': self.var9_min_entry.get(),
                 'var9_max': self.var9_max_entry.get(),
                 'var9_prec': self.var9_prec_entry.get(),
                 'var9_divby': self.var9_divby_entry.get(),
                 'var9_unit': "",

                 'var10_name': self.var10_name_entry.get(),
                 'var10_min': self.var10_min_entry.get(),
                 'var10_max': self.var10_max_entry.get(),
                 'var10_prec': self.var10_prec_entry.get(),
                 'var10_divby': self.var10_divby_entry.get(),
                 'var10_unit': "",

                 'var11_name': self.var11_name_entry.get(),
                 'var11_min': self.var11_min_entry.get(),
                 'var11_max': self.var11_max_entry.get(),
                 'var11_prec': self.var11_prec_entry.get(),
                 'var11_divby': self.var11_divby_entry.get(),
                 'var11_unit': "",

                 'var12_name': self.var12_name_entry.get(),
                 'var12_min': self.var12_min_entry.get(),
                 'var12_max': self.var12_max_entry.get(),
                 'var12_prec': self.var12_prec_entry.get(),
                 'var12_divby': self.var12_divby_entry.get(),
                 'var12_unit': "",

                 'var13_name': self.var13_name_entry.get(),
                 'var13_min': self.var13_min_entry.get(),
                 'var13_max': self.var13_max_entry.get(),
                 'var13_prec': self.var13_prec_entry.get(),
                 'var13_divby': self.var13_divby_entry.get(),
                 'var13_unit': "",

                 'var14_name': self.var14_name_entry.get(),
                 'var14_min': self.var14_min_entry.get(),
                 'var14_max': self.var14_max_entry.get(),
                 'var14_prec': self.var14_prec_entry.get(),
                 'var14_divby': self.var14_divby_entry.get(),
                 'var14_unit': "",

                 'var15_name': self.var15_name_entry.get(),
                 'var15_min': self.var15_min_entry.get(),
                 'var15_max': self.var15_max_entry.get(),
                 'var15_prec': self.var15_prec_entry.get(),
                 'var15_divby': self.var15_divby_entry.get(),
                 'var15_unit': "",



                 'res1_name': self.res1_name_entry.get(),
                 'res1_min': self.res1_min_entry.get(),
                 'res1_max': self.res1_max_entry.get(),
                 'res1_prec': self.res1_prec_entry.get(),
                 'res1_tol': self.res1_tol_entry.get(),
                 'res1_points': self.res1_points_entry.get(),
                 'res1_unit': "",

                 'res2_name': self.res2_name_entry.get(),
                 'res2_min': self.res2_min_entry.get(),
                 'res2_max': self.res2_max_entry.get(),
                 'res2_prec': self.res2_prec_entry.get(),
                 'res2_tol': self.res2_tol_entry.get(),
                 'res2_points': self.res2_points_entry.get(),
                 'res2_unit': "",

                 'res3_name': self.res3_name_entry.get(),
                 'res3_min': self.res3_min_entry.get(),
                 'res3_max': self.res3_max_entry.get(),
                 'res3_prec': self.res3_prec_entry.get(),
                 'res3_tol': self.res3_tol_entry.get(),
                 'res3_points': self.res3_points_entry.get(),
                 'res3_unit': "",

                 'res4_name': self.res4_name_entry.get(),
                 'res4_min': self.res4_min_entry.get(),
                 'res4_max': self.res4_max_entry.get(),
                 'res4_prec': self.res4_prec_entry.get(),
                 'res4_tol': self.res4_tol_entry.get(),
                 'res4_points': self.res4_points_entry.get(),
                 'res4_unit': "",

                 'res5_name': self.res5_name_entry.get(),
                 'res5_min': self.res5_min_entry.get(),
                 'res5_max': self.res5_max_entry.get(),
                 'res5_prec': self.res5_prec_entry.get(),
                 'res5_tol': self.res5_tol_entry.get(),
                 'res5_points': self.res5_points_entry.get(),
                 'res5_unit': "",

                 'res6_name': self.res6_name_entry.get(),
                 'res6_min': self.res6_min_entry.get(),
                 'res6_max': self.res6_max_entry.get(),
                 'res6_prec': self.res6_prec_entry.get(),
                 'res6_tol': self.res6_tol_entry.get(),
                 'res6_points': self.res6_points_entry.get(),
                 'res6_unit': "",

                 'res7_name': self.res7_name_entry.get(),
                 'res7_min': self.res7_min_entry.get(),
                 'res7_max': self.res7_max_entry.get(),
                 'res7_prec': self.res7_prec_entry.get(),
                 'res7_tol': self.res7_tol_entry.get(),
                 'res7_points': self.res7_points_entry.get(),
                 'res7_unit': "",

                 'res8_name': self.res8_name_entry.get(),
                 'res8_min': self.res8_min_entry.get(),
                 'res8_max': self.res8_max_entry.get(),
                 'res8_prec': self.res8_prec_entry.get(),
                 'res8_tol': self.res8_tol_entry.get(),
                 'res8_points': self.res8_points_entry.get(),
                 'res8_unit': "",

                 'res9_name': self.res9_name_entry.get(),
                 'res9_min': self.res9_min_entry.get(),
                 'res9_max': self.res9_max_entry.get(),
                 'res9_prec': self.res9_prec_entry.get(),
                 'res9_tol': self.res9_tol_entry.get(),
                 'res9_points': self.res9_points_entry.get(),
                 'res9_unit': "",

                 'res10_name': self.res10_name_entry.get(),
                 'res10_min': self.res10_min_entry.get(),
                 'res10_max': self.res10_max_entry.get(),
                 'res10_prec': self.res10_prec_entry.get(),
                 'res10_tol': self.res10_tol_entry.get(),
                 'res10_points': self.res10_points_entry.get(),
                 'res10_unit': "",

                 'description_img_name_1': self.ff_description_img_name_1,
                 'description_img_data_1': self.ff_description_img_data_1,
                 'description_img_path_1': self.ff_description_img_path_1,

                 'description_img_name_2': self.ff_description_img_name_2,
                 'description_img_data_2': self.ff_description_img_data_2,
                 'description_img_path_2': self.ff_description_img_path_2,

                 'description_img_name_3': self.ff_description_img_name_3,
                 'description_img_data_3': self.ff_description_img_data_3,
                 'description_img_path_3': self.ff_description_img_path_3,

                 'test_time': self.ff_test_time,
                 'var_number': "",
                 'res_number': "",
                 'question_pool_tag': self.ff_question_pool_tag_entry.get(),
                 'question_author': self.ff_question_author_entry.get(),
                 'oid': record_id
                 })

        conn.commit()
        conn.close()

        print("Frage mit ID: '" + record_id + "' editiert")

    def ff_delete_id_from_db(self):

        self.ff_delete_box_id = ""
        self.ff_delete_box_id = self.ff_delete_box.get()

        test_generator_modul_datenbanken_erstellen.Delete_Entry_from_Database.__init__(self, self.ff_delete_box_id, self.ff_question_type_name, self.ff_var_delete_all.get(), self.project_root_path, self.ff_db_entry_to_index_dict, self.database_formelfrage_path, self.ff_database, self.ff_database_table, "Formelfrage_DB_export_file.xlsx", "Formelfrage - Database")

    # Wird für Wertebreich berechnen verwendet
    # Bei mehreren Fragen hintereinander, müssen die Entry-Felder leer sein
    def ff_clear_var_res_entries(self):
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

        self.var11_name_entry.delete(0, END)
        self.var11_min_entry.delete(0, END)
        self.var11_max_entry.delete(0, END)
        self.var11_prec_entry.delete(0, END)
        self.var11_divby_entry.delete(0, END)

        self.var12_name_entry.delete(0, END)
        self.var12_min_entry.delete(0, END)
        self.var12_max_entry.delete(0, END)
        self.var12_prec_entry.delete(0, END)
        self.var12_divby_entry.delete(0, END)

        self.var13_name_entry.delete(0, END)
        self.var13_min_entry.delete(0, END)
        self.var13_max_entry.delete(0, END)
        self.var13_prec_entry.delete(0, END)
        self.var13_divby_entry.delete(0, END)

        self.var14_name_entry.delete(0, END)
        self.var14_min_entry.delete(0, END)
        self.var14_max_entry.delete(0, END)
        self.var14_prec_entry.delete(0, END)
        self.var14_divby_entry.delete(0, END)

        self.var15_name_entry.delete(0, END)
        self.var15_min_entry.delete(0, END)
        self.var15_max_entry.delete(0, END)
        self.var15_prec_entry.delete(0, END)
        self.var15_divby_entry.delete(0, END)

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

    def ff_clear_GUI(self):
        self.ff_question_difficulty_entry.delete(0, END)
        self.ff_question_category_entry.delete(0, END)
        #self.ff_question_type_entry.delete(0, END)

        self.ff_question_title_entry.delete(0, END)
        self.ff_question_description_title_entry.delete(0, END)
        self.ff_question_description_main_entry.delete('1.0', 'end-1c')

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

        self.var11_name_entry.delete(0, END)
        self.var11_min_entry.delete(0, END)
        self.var11_max_entry.delete(0, END)
        self.var11_prec_entry.delete(0, END)
        self.var11_divby_entry.delete(0, END)

        self.var12_name_entry.delete(0, END)
        self.var12_min_entry.delete(0, END)
        self.var12_max_entry.delete(0, END)
        self.var12_prec_entry.delete(0, END)
        self.var12_divby_entry.delete(0, END)

        self.var13_name_entry.delete(0, END)
        self.var13_min_entry.delete(0, END)
        self.var13_max_entry.delete(0, END)
        self.var13_prec_entry.delete(0, END)
        self.var13_divby_entry.delete(0, END)

        self.var14_name_entry.delete(0, END)
        self.var14_min_entry.delete(0, END)
        self.var14_max_entry.delete(0, END)
        self.var14_prec_entry.delete(0, END)
        self.var14_divby_entry.delete(0, END)

        self.var15_name_entry.delete(0, END)
        self.var15_min_entry.delete(0, END)
        self.var15_max_entry.delete(0, END)
        self.var15_prec_entry.delete(0, END)
        self.var15_divby_entry.delete(0, END)

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

        self.ff_question_pool_tag_entry.delete(0, END)

class Create_Formelfrage_Questions(Formelfrage):

    # INIT
    # ff_question_structure
    # ff_question_variable_structure
    # ff_question_results_structure

    def __init__(self, db_entry_to_index_dict, ids_in_entry_box, question_type, pool_img_dir, ilias_id_pool_qpl_dir, xml_read_qti_template_path, xml_qti_output_file_path, xml_qpl_output_file_path, max_id_pool_qti_xml, max_id, taxonomy_file_question_pool):

        # Gibt die ANzahl der Pools an
        # Üblicherweise wird nur 1 Pool erzeugt. Nur bei "Taxonomie getrennt" Erstellung, werden mehrere Pools erzeugt
        #self.number_of_pools = 1

        self.ff_db_entry_to_index_dict = db_entry_to_index_dict
        self.ff_test_entry_splitted = ids_in_entry_box.split(",")
        self.qti_file_path_output = xml_qti_output_file_path
        self.formelfrage_pool_qpl_file_path_output = xml_qpl_output_file_path

        self.ff_mytree = ET.parse(xml_read_qti_template_path)
        self.ff_myroot = self.ff_mytree.getroot()



        self.ff_question_type_test_or_pool = question_type
        self.formelfrage_pool_img_file_path = pool_img_dir           # Wird nur bei Erstellung eines Fragen-Pool verwendet. Ordnername wird erst bei Laufzeit erstellt)

        self.all_entries_from_db_list = []
        self.number_of_entrys = []
        self.ff_collection_of_question_titles = []



        self.question_pool_id_list = []
        self.question_title_list = []

        self.ff_number_of_questions_generated = 1


        self.ilias_id_pool_qpl_dir = ilias_id_pool_qpl_dir
        self.ff_file_max_id = max_id
        self.taxonomy_file_question_pool = taxonomy_file_question_pool
        self.ilias_id_pool_qti_xml = max_id_pool_qti_xml


        print("\n")


        if self.ff_question_type_test_or_pool == "question_test":
            print("FORMELFRAGE: ILIAS-TEST WIRD ERSTELLT...  ID: " + str(ids_in_entry_box))

        else:
            print("FORMELFRAGE: ILIAS-POOL WIRD ERSTELLT...  ID: " + str(ids_in_entry_box))


        # Mit FF_Datenbank verknüpfen
        connect_ff_db = sqlite3.connect(self.database_formelfrage_path)
        cursor = connect_ff_db.cursor()


        # Prüfen ob alle Einträge generiert werden sollen (checkbox gesetzt)
        if self.ff_var_create_question_pool_all_check.get() == 1 and self.ff_var_create_multiple_question_pools_from_tax_check.get() == 0:
            conn = sqlite3.connect(self.database_formelfrage_path)
            c = conn.cursor()
            c.execute("SELECT *, oid FROM %s"  % self.ff_database_table)

            ff_db_records = c.fetchall()

            for ff_db_record in ff_db_records:
                self.all_entries_from_db_list.append(int(ff_db_record[len(ff_db_record) - 1]))

            self.string_temp = ','.join(map(str, self.all_entries_from_db_list))
            self.ff_test_entry_splitted = self.string_temp.split(",")

            # Eintrag mit ID "1" entspricht der Vorlage und soll nicht mit erstellt werden
            #self.ff_test_entry_splitted.pop(0)

            #print(self.ff_test_entry_splitted)






            #print("Number of Pools: " + str(len(self.list_of_lists)))
            #self.number_of_pools = len(self.list_of_lists)


        # Sämtliche Datenbank Einträge auslesen mit der entsprechenden "oid" (Datenbank ID)
        # Datenbank ID wird automatisch bei einem neuen Eintrag erstellt (fortlaufend) und kann nicht beeinflusst werden
        cursor.execute("SELECT *, oid FROM %s"  % self.ff_database_table)
        ff_db_records = cursor.fetchall()
        """
        for pool_number in range(self.number_of_pools):

            self.string2_temp = ','.join(map(str, self.list_of_lists[pool_number]))
            self.ff_test_entry_splitted = self.string2_temp.split(",")
            print("%%%%%%")
            print(self.ff_test_entry_splitted)

        """

        for i in range(len(self.ff_test_entry_splitted)):
            for ff_db_record in ff_db_records:
                if str(ff_db_record[len(ff_db_record) - 1]) == self.ff_test_entry_splitted[i]:
                    for t in range(len(ff_db_record)):
                        if ff_db_record[self.ff_db_entry_to_index_dict['question_type']].lower() == self.ff_question_type_name.lower():
                            self.ff_question_difficulty                                                = ff_db_record[self.ff_db_entry_to_index_dict['question_difficulty']]
                            self.ff_question_category                                                  = ff_db_record[self.ff_db_entry_to_index_dict['question_category']]
                            self.ff_question_type                                                      = ff_db_record[self.ff_db_entry_to_index_dict['question_type']]
                            self.ff_question_title                                                     = ff_db_record[self.ff_db_entry_to_index_dict['question_title']].replace('&', "&amp;")
                            self.ff_question_description_title                                         = ff_db_record[self.ff_db_entry_to_index_dict['question_description_title']].replace('&', "&amp;")
                            self.ff_question_description_main                                          = ff_db_record[self.ff_db_entry_to_index_dict['question_description_main']]
                            self.ff_res1_formula                                                       = ff_db_record[self.ff_db_entry_to_index_dict['res1_formula']]
                            self.ff_res2_formula                                                       = ff_db_record[self.ff_db_entry_to_index_dict['res2_formula']]
                            self.ff_res3_formula                                                       = ff_db_record[self.ff_db_entry_to_index_dict['res3_formula']]
                            self.ff_res4_formula                                                       = ff_db_record[self.ff_db_entry_to_index_dict['res4_formula']]
                            self.ff_res5_formula                                                       = ff_db_record[self.ff_db_entry_to_index_dict['res5_formula']]
                            self.ff_res6_formula                                                       = ff_db_record[self.ff_db_entry_to_index_dict['res6_formula']]
                            self.ff_res7_formula                                                       = ff_db_record[self.ff_db_entry_to_index_dict['res7_formula']]
                            self.ff_res8_formula                                                       = ff_db_record[self.ff_db_entry_to_index_dict['res8_formula']]
                            self.ff_res9_formula                                                       = ff_db_record[self.ff_db_entry_to_index_dict['res9_formula']]
                            self.ff_res10_formula                                                      = ff_db_record[self.ff_db_entry_to_index_dict['res10_formula']]

                            self.ff_var1_name                                                          = ff_db_record[self.ff_db_entry_to_index_dict['var1_name']]
                            self.ff_var1_min                                                           = ff_db_record[self.ff_db_entry_to_index_dict['var1_min']]
                            self.ff_var1_max                                                           = ff_db_record[self.ff_db_entry_to_index_dict['var1_max']]
                            self.ff_var1_prec                                                          = ff_db_record[self.ff_db_entry_to_index_dict['var1_prec']]
                            self.ff_var1_divby                                                         = ff_db_record[self.ff_db_entry_to_index_dict['var1_divby']]
                            self.ff_var1_unit                                                          = ff_db_record[self.ff_db_entry_to_index_dict['var1_unit']]

                            self.ff_var2_name                                                          = ff_db_record[self.ff_db_entry_to_index_dict['var2_name']]
                            self.ff_var2_min                                                           = ff_db_record[self.ff_db_entry_to_index_dict['var2_min']]
                            self.ff_var2_max                                                           = ff_db_record[self.ff_db_entry_to_index_dict['var2_max']]
                            self.ff_var2_prec                                                          = ff_db_record[self.ff_db_entry_to_index_dict['var2_prec']]
                            self.ff_var2_divby                                                         = ff_db_record[self.ff_db_entry_to_index_dict['var2_divby']]
                            self.ff_var2_unit                                                          = ff_db_record[self.ff_db_entry_to_index_dict['var2_unit']]

                            self.ff_var3_name                                                          = ff_db_record[self.ff_db_entry_to_index_dict['var3_name']]
                            self.ff_var3_min                                                           = ff_db_record[self.ff_db_entry_to_index_dict['var3_min']]
                            self.ff_var3_max                                                           = ff_db_record[self.ff_db_entry_to_index_dict['var3_max']]
                            self.ff_var3_prec                                                          = ff_db_record[self.ff_db_entry_to_index_dict['var3_prec']]
                            self.ff_var3_divby                                                         = ff_db_record[self.ff_db_entry_to_index_dict['var3_divby']]
                            self.ff_var3_unit                                                          = ff_db_record[self.ff_db_entry_to_index_dict['var3_unit']]

                            self.ff_var4_name                                                          = ff_db_record[self.ff_db_entry_to_index_dict['var4_name']]
                            self.ff_var4_min                                                           = ff_db_record[self.ff_db_entry_to_index_dict['var4_min']]
                            self.ff_var4_max                                                           = ff_db_record[self.ff_db_entry_to_index_dict['var4_max']]
                            self.ff_var4_prec                                                          = ff_db_record[self.ff_db_entry_to_index_dict['var4_prec']]
                            self.ff_var4_divby                                                         = ff_db_record[self.ff_db_entry_to_index_dict['var4_divby']]
                            self.ff_var4_unit                                                          = ff_db_record[self.ff_db_entry_to_index_dict['var4_unit']]

                            self.ff_var5_name                                                          = ff_db_record[self.ff_db_entry_to_index_dict['var5_name']]
                            self.ff_var5_min                                                           = ff_db_record[self.ff_db_entry_to_index_dict['var5_min']]
                            self.ff_var5_max                                                           = ff_db_record[self.ff_db_entry_to_index_dict['var5_max']]
                            self.ff_var5_prec                                                          = ff_db_record[self.ff_db_entry_to_index_dict['var5_prec']]
                            self.ff_var5_divby                                                         = ff_db_record[self.ff_db_entry_to_index_dict['var5_divby']]
                            self.ff_var5_unit                                                          = ff_db_record[self.ff_db_entry_to_index_dict['var5_unit']]

                            self.ff_var6_name                                                          = ff_db_record[self.ff_db_entry_to_index_dict['var6_name']]
                            self.ff_var6_min                                                           = ff_db_record[self.ff_db_entry_to_index_dict['var6_min']]
                            self.ff_var6_max                                                           = ff_db_record[self.ff_db_entry_to_index_dict['var6_max']]
                            self.ff_var6_prec                                                          = ff_db_record[self.ff_db_entry_to_index_dict['var6_prec']]
                            self.ff_var6_divby                                                         = ff_db_record[self.ff_db_entry_to_index_dict['var6_divby']]
                            self.ff_var6_unit                                                          = ff_db_record[self.ff_db_entry_to_index_dict['var6_unit']]

                            self.ff_var7_name                                                          = ff_db_record[self.ff_db_entry_to_index_dict['var7_name']]
                            self.ff_var7_min                                                           = ff_db_record[self.ff_db_entry_to_index_dict['var7_min']]
                            self.ff_var7_max                                                           = ff_db_record[self.ff_db_entry_to_index_dict['var7_max']]
                            self.ff_var7_prec                                                          = ff_db_record[self.ff_db_entry_to_index_dict['var7_prec']]
                            self.ff_var7_divby                                                         = ff_db_record[self.ff_db_entry_to_index_dict['var7_divby']]
                            self.ff_var7_unit                                                          = ff_db_record[self.ff_db_entry_to_index_dict['var7_unit']]

                            self.ff_var8_name                                                          = ff_db_record[self.ff_db_entry_to_index_dict['var8_name']]
                            self.ff_var8_min                                                           = ff_db_record[self.ff_db_entry_to_index_dict['var8_min']]
                            self.ff_var8_max                                                           = ff_db_record[self.ff_db_entry_to_index_dict['var8_max']]
                            self.ff_var8_prec                                                          = ff_db_record[self.ff_db_entry_to_index_dict['var8_prec']]
                            self.ff_var8_divby                                                         = ff_db_record[self.ff_db_entry_to_index_dict['var8_divby']]
                            self.ff_var8_unit                                                          = ff_db_record[self.ff_db_entry_to_index_dict['var8_unit']]

                            self.ff_var9_name                                                          = ff_db_record[self.ff_db_entry_to_index_dict['var9_name']]
                            self.ff_var9_min                                                           = ff_db_record[self.ff_db_entry_to_index_dict['var9_min']]
                            self.ff_var9_max                                                           = ff_db_record[self.ff_db_entry_to_index_dict['var9_max']]
                            self.ff_var9_prec                                                          = ff_db_record[self.ff_db_entry_to_index_dict['var9_prec']]
                            self.ff_var9_divby                                                         = ff_db_record[self.ff_db_entry_to_index_dict['var9_divby']]
                            self.ff_var9_unit                                                          = ff_db_record[self.ff_db_entry_to_index_dict['var9_unit']]

                            self.ff_var10_name                                                         = ff_db_record[self.ff_db_entry_to_index_dict['var10_name']]
                            self.ff_var10_min                                                          = ff_db_record[self.ff_db_entry_to_index_dict['var10_min']]
                            self.ff_var10_max                                                          = ff_db_record[self.ff_db_entry_to_index_dict['var10_max']]
                            self.ff_var10_prec                                                         = ff_db_record[self.ff_db_entry_to_index_dict['var10_prec']]
                            self.ff_var10_divby                                                        = ff_db_record[self.ff_db_entry_to_index_dict['var10_divby']]
                            self.ff_var10_unit                                                         = ff_db_record[self.ff_db_entry_to_index_dict['var10_unit']]

                            self.ff_var11_name                                                         = ff_db_record[self.ff_db_entry_to_index_dict['var11_name']]
                            self.ff_var11_min                                                          = ff_db_record[self.ff_db_entry_to_index_dict['var11_min']]
                            self.ff_var11_max                                                          = ff_db_record[self.ff_db_entry_to_index_dict['var11_max']]
                            self.ff_var11_prec                                                         = ff_db_record[self.ff_db_entry_to_index_dict['var11_prec']]
                            self.ff_var11_divby                                                        = ff_db_record[self.ff_db_entry_to_index_dict['var11_divby']]
                            self.ff_var11_unit                                                         = ff_db_record[self.ff_db_entry_to_index_dict['var11_unit']]

                            self.ff_var12_name                                                         = ff_db_record[self.ff_db_entry_to_index_dict['var12_name']]
                            self.ff_var12_min                                                          = ff_db_record[self.ff_db_entry_to_index_dict['var12_min']]
                            self.ff_var12_max                                                          = ff_db_record[self.ff_db_entry_to_index_dict['var12_max']]
                            self.ff_var12_prec                                                         = ff_db_record[self.ff_db_entry_to_index_dict['var12_prec']]
                            self.ff_var12_divby                                                        = ff_db_record[self.ff_db_entry_to_index_dict['var12_divby']]
                            self.ff_var12_unit                                                         = ff_db_record[self.ff_db_entry_to_index_dict['var12_unit']]

                            self.ff_var13_name                                                         = ff_db_record[self.ff_db_entry_to_index_dict['var13_name']]
                            self.ff_var13_min                                                          = ff_db_record[self.ff_db_entry_to_index_dict['var13_min']]
                            self.ff_var13_max                                                          = ff_db_record[self.ff_db_entry_to_index_dict['var13_max']]
                            self.ff_var13_prec                                                         = ff_db_record[self.ff_db_entry_to_index_dict['var13_prec']]
                            self.ff_var13_divby                                                        = ff_db_record[self.ff_db_entry_to_index_dict['var13_divby']]
                            self.ff_var13_unit                                                         = ff_db_record[self.ff_db_entry_to_index_dict['var13_unit']]

                            self.ff_var14_name                                                         = ff_db_record[self.ff_db_entry_to_index_dict['var14_name']]
                            self.ff_var14_min                                                          = ff_db_record[self.ff_db_entry_to_index_dict['var14_min']]
                            self.ff_var14_max                                                          = ff_db_record[self.ff_db_entry_to_index_dict['var14_max']]
                            self.ff_var14_prec                                                         = ff_db_record[self.ff_db_entry_to_index_dict['var14_prec']]
                            self.ff_var14_divby                                                        = ff_db_record[self.ff_db_entry_to_index_dict['var14_divby']]
                            self.ff_var14_unit                                                         = ff_db_record[self.ff_db_entry_to_index_dict['var14_unit']]

                            self.ff_var15_name                                                         = ff_db_record[self.ff_db_entry_to_index_dict['var15_name']]
                            self.ff_var15_min                                                          = ff_db_record[self.ff_db_entry_to_index_dict['var15_min']]
                            self.ff_var15_max                                                          = ff_db_record[self.ff_db_entry_to_index_dict['var15_max']]
                            self.ff_var15_prec                                                         = ff_db_record[self.ff_db_entry_to_index_dict['var15_prec']]
                            self.ff_var15_divby                                                        = ff_db_record[self.ff_db_entry_to_index_dict['var15_divby']]
                            self.ff_var15_unit                                                         = ff_db_record[self.ff_db_entry_to_index_dict['var15_unit']]

                            self.ff_res1_name                                                          = ff_db_record[self.ff_db_entry_to_index_dict['res1_name']]
                            self.ff_res1_min                                                           = ff_db_record[self.ff_db_entry_to_index_dict['res1_min']]
                            self.ff_res1_max                                                           = ff_db_record[self.ff_db_entry_to_index_dict['res1_max']]
                            self.ff_res1_prec                                                          = ff_db_record[self.ff_db_entry_to_index_dict['res1_prec']]
                            self.ff_res1_tol                                                           = ff_db_record[self.ff_db_entry_to_index_dict['res1_tol']]
                            self.ff_res1_points                                                        = ff_db_record[self.ff_db_entry_to_index_dict['res1_points']]
                            self.ff_res1_unit                                                          = ff_db_record[self.ff_db_entry_to_index_dict['res1_unit']]

                            self.ff_res2_name                                                          = ff_db_record[self.ff_db_entry_to_index_dict['res2_name']]
                            self.ff_res2_min                                                           = ff_db_record[self.ff_db_entry_to_index_dict['res2_min']]
                            self.ff_res2_max                                                           = ff_db_record[self.ff_db_entry_to_index_dict['res2_max']]
                            self.ff_res2_prec                                                          = ff_db_record[self.ff_db_entry_to_index_dict['res2_prec']]
                            self.ff_res2_tol                                                           = ff_db_record[self.ff_db_entry_to_index_dict['res2_tol']]
                            self.ff_res2_points                                                        = ff_db_record[self.ff_db_entry_to_index_dict['res2_points']]
                            self.ff_res2_unit                                                          = ff_db_record[self.ff_db_entry_to_index_dict['res2_unit']]

                            self.ff_res3_name                                                          = ff_db_record[self.ff_db_entry_to_index_dict['res3_name']]
                            self.ff_res3_min                                                           = ff_db_record[self.ff_db_entry_to_index_dict['res3_min']]
                            self.ff_res3_max                                                           = ff_db_record[self.ff_db_entry_to_index_dict['res3_max']]
                            self.ff_res3_prec                                                          = ff_db_record[self.ff_db_entry_to_index_dict['res3_prec']]
                            self.ff_res3_tol                                                           = ff_db_record[self.ff_db_entry_to_index_dict['res3_tol']]
                            self.ff_res3_points                                                        = ff_db_record[self.ff_db_entry_to_index_dict['res3_points']]
                            self.ff_res3_unit                                                          = ff_db_record[self.ff_db_entry_to_index_dict['res3_unit']]

                            self.ff_res4_name                                                          = ff_db_record[self.ff_db_entry_to_index_dict['res4_name']]
                            self.ff_res4_min                                                           = ff_db_record[self.ff_db_entry_to_index_dict['res4_min']]
                            self.ff_res4_max                                                           = ff_db_record[self.ff_db_entry_to_index_dict['res4_max']]
                            self.ff_res4_prec                                                          = ff_db_record[self.ff_db_entry_to_index_dict['res4_prec']]
                            self.ff_res4_tol                                                           = ff_db_record[self.ff_db_entry_to_index_dict['res4_tol']]
                            self.ff_res4_points                                                        = ff_db_record[self.ff_db_entry_to_index_dict['res4_points']]
                            self.ff_res4_unit                                                          = ff_db_record[self.ff_db_entry_to_index_dict['res4_unit']]

                            self.ff_res5_name                                                          = ff_db_record[self.ff_db_entry_to_index_dict['res5_name']]
                            self.ff_res5_min                                                           = ff_db_record[self.ff_db_entry_to_index_dict['res5_min']]
                            self.ff_res5_max                                                           = ff_db_record[self.ff_db_entry_to_index_dict['res5_max']]
                            self.ff_res5_prec                                                          = ff_db_record[self.ff_db_entry_to_index_dict['res5_prec']]
                            self.ff_res5_tol                                                           = ff_db_record[self.ff_db_entry_to_index_dict['res5_tol']]
                            self.ff_res5_points                                                        = ff_db_record[self.ff_db_entry_to_index_dict['res5_points']]
                            self.ff_res5_unit                                                          = ff_db_record[self.ff_db_entry_to_index_dict['res5_unit']]

                            self.ff_res6_name                                                          = ff_db_record[self.ff_db_entry_to_index_dict['res6_name']]
                            self.ff_res6_min                                                           = ff_db_record[self.ff_db_entry_to_index_dict['res6_min']]
                            self.ff_res6_max                                                           = ff_db_record[self.ff_db_entry_to_index_dict['res6_max']]
                            self.ff_res6_prec                                                          = ff_db_record[self.ff_db_entry_to_index_dict['res6_prec']]
                            self.ff_res6_tol                                                           = ff_db_record[self.ff_db_entry_to_index_dict['res6_tol']]
                            self.ff_res6_points                                                        = ff_db_record[self.ff_db_entry_to_index_dict['res6_points']]
                            self.ff_res6_unit                                                          = ff_db_record[self.ff_db_entry_to_index_dict['res6_unit']]

                            self.ff_res7_name                                                          = ff_db_record[self.ff_db_entry_to_index_dict['res7_name']]
                            self.ff_res7_min                                                           = ff_db_record[self.ff_db_entry_to_index_dict['res7_min']]
                            self.ff_res7_max                                                           = ff_db_record[self.ff_db_entry_to_index_dict['res7_max']]
                            self.ff_res7_prec                                                          = ff_db_record[self.ff_db_entry_to_index_dict['res7_prec']]
                            self.ff_res7_tol                                                           = ff_db_record[self.ff_db_entry_to_index_dict['res7_tol']]
                            self.ff_res7_points                                                        = ff_db_record[self.ff_db_entry_to_index_dict['res7_points']]
                            self.ff_res7_unit                                                          = ff_db_record[self.ff_db_entry_to_index_dict['res7_unit']]

                            self.ff_es8_name                                                           = ff_db_record[self.ff_db_entry_to_index_dict['res8_name']]
                            self.ff_res8_min                                                           = ff_db_record[self.ff_db_entry_to_index_dict['res8_min']]
                            self.ff_res8_max                                                           = ff_db_record[self.ff_db_entry_to_index_dict['res8_max']]
                            self.ff_res8_prec                                                          = ff_db_record[self.ff_db_entry_to_index_dict['res8_prec']]
                            self.ff_res8_tol                                                           = ff_db_record[self.ff_db_entry_to_index_dict['res8_tol']]
                            self.ff_res8_points                                                        = ff_db_record[self.ff_db_entry_to_index_dict['res8_points']]
                            self.ff_res8_unit                                                          = ff_db_record[self.ff_db_entry_to_index_dict['res8_unit']]

                            self.ff_res9_name                                                          = ff_db_record[self.ff_db_entry_to_index_dict['res9_name']]
                            self.ff_res9_min                                                           = ff_db_record[self.ff_db_entry_to_index_dict['res9_min']]
                            self.ff_res9_max                                                           = ff_db_record[self.ff_db_entry_to_index_dict['res9_max']]
                            self.ff_res9_prec                                                          = ff_db_record[self.ff_db_entry_to_index_dict['res9_prec']]
                            self.ff_res9_tol                                                           = ff_db_record[self.ff_db_entry_to_index_dict['res9_tol']]
                            self.ff_res9_points                                                        = ff_db_record[self.ff_db_entry_to_index_dict['res9_points']]
                            self.ff_res9_unit                                                          = ff_db_record[self.ff_db_entry_to_index_dict['res9_unit']]

                            self.ff_res10_name                                                         = ff_db_record[self.ff_db_entry_to_index_dict['res10_name']]
                            self.ff_res10_min                                                          = ff_db_record[self.ff_db_entry_to_index_dict['res10_min']]
                            self.ff_res10_max                                                          = ff_db_record[self.ff_db_entry_to_index_dict['res10_max']]
                            self.ff_res10_prec                                                         = ff_db_record[self.ff_db_entry_to_index_dict['res10_prec']]
                            self.ff_res10_tol                                                          = ff_db_record[self.ff_db_entry_to_index_dict['res10_tol']]
                            self.ff_res10_points                                                       = ff_db_record[self.ff_db_entry_to_index_dict['res10_points']]
                            self.ff_res10_unit                                                         = ff_db_record[self.ff_db_entry_to_index_dict['res10_unit']]

                            self.ff_description_img_name_1	                                           = ff_db_record[self.ff_db_entry_to_index_dict['description_img_name_1']]
                            self.ff_description_img_data_1	                                           = ff_db_record[self.ff_db_entry_to_index_dict['description_img_data_1']]
                            self.ff_description_img_path_1	                                           = ff_db_record[self.ff_db_entry_to_index_dict['description_img_path_1']]
                            self.ff_description_img_name_2	                                           = ff_db_record[self.ff_db_entry_to_index_dict['description_img_name_2']]
                            self.ff_description_img_data_2	                                           = ff_db_record[self.ff_db_entry_to_index_dict['description_img_data_2']]
                            self.ff_description_img_path_2	                                           = ff_db_record[self.ff_db_entry_to_index_dict['description_img_path_2']]
                            self.ff_description_img_name_3	                                           = ff_db_record[self.ff_db_entry_to_index_dict['description_img_name_3']]
                            self.ff_description_img_data_3	                                           = ff_db_record[self.ff_db_entry_to_index_dict['description_img_data_3']]
                            self.ff_description_img_path_3	                                           = ff_db_record[self.ff_db_entry_to_index_dict['description_img_path_3']]

                            self.ff_test_time	                                                       = ff_db_record[self.ff_db_entry_to_index_dict['test_time']]
                            self.ff_var_number	                                                       = ff_db_record[self.ff_db_entry_to_index_dict['var_number']]
                            self.ff_res_number	                                                       = ff_db_record[self.ff_db_entry_to_index_dict['res_number']]
                            self.ff_question_pool_tag                                                  = ff_db_record[self.ff_db_entry_to_index_dict['question_pool_tag']]
                            self.ff_question_author                                                    = ff_db_record[self.ff_db_entry_to_index_dict['question_author']].replace('&', "&amp;")



            Create_Formelfrage_Questions.ff_question_structure(self, i)

    def ff_question_structure(self, id_nr):
        """Diese Funktion wandelt die SQL-Einträge in die .xml um, welche anschließend in ILIAS eingespielt werden kann"""



        # VARIABLEN
        self.ff_response_counter = 0    #wird verwendet zu zählen, wieviele Anworten pro Frage verwendet werden. Bei einer neuer Antwort -> +1

        self.ff_question_description_main = test_generator_modul_taxonomie_und_textformatierung.Textformatierung.format_description_text_in_xml(self, self.ff_var_use_latex_on_text_check.get(), self.ff_question_description_main)


        # Verbindung zur FF-Datenank
        ff_connect = sqlite3.connect(self.database_formelfrage_path)
        ff_cursor = ff_connect.cursor()

        # Alle Einträge auslesen
        ff_cursor.execute("SELECT *, oid FROM %s" % self.ff_database_table)
        ff_db_records = ff_cursor.fetchall()



        for ff_db_record in ff_db_records:

            # Hier werden die Fragen anhand der ID's erstellt
            if str(ff_db_record[len(ff_db_record)-1]) == self.ff_test_entry_splitted[id_nr]:


                # Bilder für die Beschreibung speichern
                test_generator_modul_ilias_test_struktur.Additional_Funtions.add_dir_for_images(self, self.ff_description_img_name_1, self.ff_description_img_data_1, id_nr, self.ff_question_type_test_or_pool, self.formelfrage_test_img_file_path, self.formelfrage_pool_img_file_path)
                test_generator_modul_ilias_test_struktur.Additional_Funtions.add_dir_for_images(self, self.ff_description_img_name_2, self.ff_description_img_data_2, id_nr, self.ff_question_type_test_or_pool, self.formelfrage_test_img_file_path, self.formelfrage_pool_img_file_path)
                test_generator_modul_ilias_test_struktur.Additional_Funtions.add_dir_for_images(self, self.ff_description_img_name_3, self.ff_description_img_data_3, id_nr, self.ff_question_type_test_or_pool, self.formelfrage_test_img_file_path, self.formelfrage_pool_img_file_path)


                # Aufbau für  Fragenstruktur "TEST"
                if self.ff_question_type_test_or_pool == "question_test":
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

                    # Zusatz für Taxonomie Einstellungen

                    test_generator_modul_ilias_test_struktur.Additional_Funtions.set_taxonomy_for_question(self,
                                                                                                           id_nr,
                                                                                                           self.number_of_entrys,
                                                                                                           item,
                                                                                                           self.formelfrage_pool_qpl_file_path_template,
                                                                                                           self.formelfrage_pool_qpl_file_path_output
                                                                                                           )



                # Struktur für den Formelfragen - Variableen/Lösungen Teil
                # Muss für jede Frage neu angelegt/hinzugefügt werden
                qticomment = ET.SubElement(item, 'qticomment')
                duration = ET.SubElement(item, 'duration')
                itemmetadata = ET.SubElement(item, 'itemmetadata')
                presentation = ET.SubElement(item, 'presentation')

                flow = ET.SubElement(presentation, 'flow')
                question_description_material = ET.SubElement(flow, 'material')
                question_description_mattext = ET.SubElement(question_description_material, 'mattext')
                qtimetadata = ET.SubElement(itemmetadata, 'qtimetadata')


                ### ------------------------------------------------------- XML Einträge mit Werten füllen
                 # Fragen-Titel -- "item title" in xml
                item.set('title', self.ff_question_title)

                # Fragen-Titel Beschreibung
                qticomment.text = self.ff_question_description_title

                # Testdauer -- "duration" in xml
                # wird keine Testzeit eingetragen, wird 1h vorausgewählt
                duration.text = self.ff_test_time
                if duration.text == "":
                    duration.text = "P0Y0M0DT1H0M0S"

                # -----------------------------------------------------------------------ILIAS VERSION
                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "ILIAS_VERSION"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
                fieldentry.text = "5.4.10 2020-03-04"
                # -----------------------------------------------------------------------QUESTIONTYPE
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
                fieldentry.text = self.ff_question_author
                # -----------------------------------------------------------------------POINTS
                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "points"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
                fieldentry.text = str(self.ff_res1_points)

                # Fragentitel einsetzen -- "presentation label" in xml
                presentation.set('label', self.ff_question_title)

                # Fragen-Text (Format) einsetzen -- "mattext_texttype" in xml -- Gibt das Format des Textes an
                question_description_mattext.set('texttype', "text/html")

                # Fragen-Text (Text) einsetzen   -- "mattext_texttype" in xml -- Gibt die eigentliche Fragen-Beschreibung an
                # Wenn Bild enthalten ist, dann in Fragenbeschreibung einbetten
                question_description_mattext.text = test_generator_modul_ilias_test_struktur.Additional_Funtions.add_picture_to_description_main(
                                                    self, self.ff_description_img_name_1, self.ff_description_img_data_1,
                                                    self.ff_description_img_name_2, self.ff_description_img_data_2,
                                                    self.ff_description_img_name_3, self.ff_description_img_data_3,
                                                    self.ff_question_description_main, question_description_mattext, question_description_material, id_nr)




                # ----------------------------------------------------------------------- Variable
                Create_Formelfrage_Questions.ff_question_variables_structure(self, qtimetadata, "$v1", self.ff_var1_min, self.ff_var1_max, self.ff_var1_prec, self.ff_var1_divby, self.ff_var1_unit)
                Create_Formelfrage_Questions.ff_question_variables_structure(self, qtimetadata, "$v2", self.ff_var2_min, self.ff_var2_max, self.ff_var2_prec, self.ff_var2_divby, self.ff_var2_unit)
                Create_Formelfrage_Questions.ff_question_variables_structure(self, qtimetadata, "$v3", self.ff_var3_min, self.ff_var3_max, self.ff_var3_prec, self.ff_var3_divby, self.ff_var3_unit)
                Create_Formelfrage_Questions.ff_question_variables_structure(self, qtimetadata, "$v4", self.ff_var4_min, self.ff_var4_max, self.ff_var4_prec, self.ff_var4_divby, self.ff_var4_unit)
                Create_Formelfrage_Questions.ff_question_variables_structure(self, qtimetadata, "$v5", self.ff_var5_min, self.ff_var5_max, self.ff_var5_prec, self.ff_var5_divby, self.ff_var5_unit)
                Create_Formelfrage_Questions.ff_question_variables_structure(self, qtimetadata, "$v6", self.ff_var6_min, self.ff_var6_max, self.ff_var6_prec, self.ff_var6_divby, self.ff_var6_unit)
                Create_Formelfrage_Questions.ff_question_variables_structure(self, qtimetadata, "$v7", self.ff_var7_min, self.ff_var7_max, self.ff_var7_prec, self.ff_var7_divby, self.ff_var7_unit)
                Create_Formelfrage_Questions.ff_question_variables_structure(self, qtimetadata, "$v8", self.ff_var8_min, self.ff_var8_max, self.ff_var8_prec, self.ff_var8_divby, self.ff_var8_unit)
                Create_Formelfrage_Questions.ff_question_variables_structure(self, qtimetadata, "$v9", self.ff_var9_min, self.ff_var9_max, self.ff_var9_prec, self.ff_var9_divby, self.ff_var9_unit)
                Create_Formelfrage_Questions.ff_question_variables_structure(self, qtimetadata, "$v10", self.ff_var10_min, self.ff_var10_max, self.ff_var10_prec, self.ff_var10_divby, self.ff_var10_unit)
                Create_Formelfrage_Questions.ff_question_variables_structure(self, qtimetadata, "$v11", self.ff_var11_min, self.ff_var11_max, self.ff_var11_prec, self.ff_var11_divby, self.ff_var11_unit)
                Create_Formelfrage_Questions.ff_question_variables_structure(self, qtimetadata, "$v12", self.ff_var12_min, self.ff_var12_max, self.ff_var12_prec, self.ff_var12_divby, self.ff_var12_unit)
                Create_Formelfrage_Questions.ff_question_variables_structure(self, qtimetadata, "$v13", self.ff_var13_min, self.ff_var13_max, self.ff_var13_prec, self.ff_var13_divby, self.ff_var13_unit)
                Create_Formelfrage_Questions.ff_question_variables_structure(self, qtimetadata, "$v14", self.ff_var14_min, self.ff_var14_max, self.ff_var14_prec, self.ff_var14_divby, self.ff_var14_unit)
                Create_Formelfrage_Questions.ff_question_variables_structure(self, qtimetadata, "$v15", self.ff_var15_min, self.ff_var15_max, self.ff_var15_prec, self.ff_var15_divby, self.ff_var15_unit)



                # ----------------------------------------------------------------------- Solution
                Create_Formelfrage_Questions.ff_question_results_structure(self, qtimetadata, "$r1", self.ff_res1_formula, self.ff_res1_min, self.ff_res1_max, self.ff_res1_prec, self.ff_res1_tol, self.ff_res1_points, self.ff_res1_unit)
                Create_Formelfrage_Questions.ff_question_results_structure(self, qtimetadata, "$r2", self.ff_res2_formula, self.ff_res2_min, self.ff_res2_max, self.ff_res2_prec, self.ff_res2_tol, self.ff_res2_points, self.ff_res2_unit)
                Create_Formelfrage_Questions.ff_question_results_structure(self, qtimetadata, "$r3", self.ff_res3_formula, self.ff_res3_min, self.ff_res3_max, self.ff_res3_prec, self.ff_res3_tol, self.ff_res3_points, self.ff_res3_unit)
                Create_Formelfrage_Questions.ff_question_results_structure(self, qtimetadata, "$r4", self.ff_res4_formula, self.ff_res4_min, self.ff_res4_max, self.ff_res4_prec, self.ff_res4_tol, self.ff_res4_points, self.ff_res4_unit)
                Create_Formelfrage_Questions.ff_question_results_structure(self, qtimetadata, "$r5", self.ff_res5_formula, self.ff_res5_min, self.ff_res5_max, self.ff_res5_prec, self.ff_res5_tol, self.ff_res5_points, self.ff_res5_unit)
                Create_Formelfrage_Questions.ff_question_results_structure(self, qtimetadata, "$r6", self.ff_res6_formula, self.ff_res6_min, self.ff_res6_max, self.ff_res6_prec, self.ff_res6_tol, self.ff_res6_points, self.ff_res6_unit)
                Create_Formelfrage_Questions.ff_question_results_structure(self, qtimetadata, "$r7", self.ff_res7_formula, self.ff_res7_min, self.ff_res7_max, self.ff_res7_prec, self.ff_res7_tol, self.ff_res7_points, self.ff_res7_unit)
                Create_Formelfrage_Questions.ff_question_results_structure(self, qtimetadata, "$r8", self.ff_res8_formula, self.ff_res8_min, self.ff_res8_max, self.ff_res8_prec, self.ff_res8_tol, self.ff_res8_points, self.ff_res8_unit)
                Create_Formelfrage_Questions.ff_question_results_structure(self, qtimetadata, "$r9", self.ff_res9_formula, self.ff_res9_min, self.ff_res9_max, self.ff_res9_prec, self.ff_res9_tol, self.ff_res9_points, self.ff_res9_unit)
                Create_Formelfrage_Questions.ff_question_results_structure(self, qtimetadata, "$r10", self.ff_res10_formula, self.ff_res10_min, self.ff_res10_max, self.ff_res10_prec, self.ff_res10_tol, self.ff_res10_points, self.ff_res10_unit)








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



                # Wenn es sich um einen ILIAS-Test handelt, beinhaltet die XML eine Struktur mit mehreren "Zweigen"
                # Der letzte "Zweig" --> "len(self.ff_myroot[0]) - 1" (beschreibt das letze Fach) beinhaltet die eigentlichen Fragen
                if self.ff_question_type_test_or_pool == "question_test":
                    self.ff_myroot[0][len(self.ff_myroot[0]) - 1].append(item)

                # Wenn es sich um einen ILIAS-Pool handelt, beinhaltet die XML keine Struktur
                # Die Frage kann einfach angehangen werden
                else:
                    self.ff_myroot.append(item)

                self.ff_mytree.write(self.qti_file_path_output)

                print(str(self.ff_number_of_questions_generated) + ".) Formelfrage Frage erstellt! ---> Titel: " + str(self.ff_question_title))
                self.ff_number_of_questions_generated += 1
                self.ff_collection_of_question_titles.append(self.ff_question_title)

        ff_connect.commit()
        ff_connect.close()

        if self.ff_question_type_test_or_pool == "question_pool":
            ######  Anpassung der Datei "qpl". Akualisierung des Dateinamens
            self.qpl_file = os.path.normpath(os.path.join(self.formelfrage_files_path,"ff_ilias_pool_abgabe", self.ilias_id_pool_qpl_dir, self.ilias_id_pool_qti_xml))

            self.mytree = ET.parse(self.qpl_file)
            self.myroot = self.mytree.getroot()

            for ident_id in self.myroot.iter('Identifier'):
                ident_id.set('Entry', "il_0_qpl_" + str(self.ff_file_max_id+1))
            self.mytree.write(self.qpl_file)

    def ff_question_variables_structure(self, xml_qtimetadata,  ff_var_name, ff_var_min, ff_var_max, ff_var_prec, ff_var_divby, ff_var_unit):

        # <------------ INIT ----------->
        self.ff_var_name = ff_var_name
        self.ff_var_min = str(ff_var_min)
        self.ff_var_max = str(ff_var_max)
        self.ff_var_prec = str(ff_var_prec)
        self.ff_var_divby = str(ff_var_divby)
        self.ff_var_divby_length = len(str(self.ff_var_divby))
        self.ff_var_unit = ff_var_unit
        self.ff_var_unit_length = len(str(self.ff_var_unit))

        # <------------ FORMELFRAGE VARIABLEN STRUKTUR (in XML) ----------->
        qtimetadatafield = ET.SubElement(xml_qtimetadata, 'qtimetadatafield')
        fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
        fieldlabel.text = ff_var_name
        fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')

        # Mit Einheiten:
        if self.ff_var_unit != "":
            fieldentry.text = "a:6:{" \
                              "s:9:\"precision\";i:" + self.ff_var_prec + ";" \
                              "s:12:\"intprecision\";s:" + str(self.ff_var_divby_length) + ":\"" + self.ff_var_divby + "\";" \
                              "s:8:\"rangemin\";d:" + self.ff_var_min + ";" \
                              "s:8:\"rangemax\";d:" + self.ff_var_max + ";" \
                              "s:4:\"unit\";s:" + str(self.ff_var_unit_length) + ":\"" + self.ff_var_unit + "\";" \
                              "s:9:\"unitvalue\";s:" + str(len(Formelfrage.unit_table(self, self.ff_var_unit))) + ":\"" + Formelfrage.unit_table(self, self.ff_var_unit) + "\";" \
                              "}"
        # Ohne Einheiten:
        else:
            fieldentry.text = "a:6:{" \
                              "s:9:\"precision\";i:" + self.ff_var_prec + ";" \
                              "s:12:\"intprecision\";s:" + str(self.ff_var_divby_length) + ":\"" + self.ff_var_divby + "\";" \
                              "s:8:\"rangemin\";d:" + self.ff_var_min + ";" \
                              "s:8:\"rangemax\";d:" + self.ff_var_max + ";" \
                              "s:4:\"unit\";s:0:\"\";" \
                              "s:9:\"unitvalue\";s:0:\"\";" \
                              "}"

    def ff_question_results_structure(self, xml_qtimetadata, ff_res_name, ff_res_formula, ff_res_min, ff_res_max, ff_res_prec, ff_res_tol, ff_res_points, ff_res_unit):

        def replace_words_in_formula(formula):

            self.replace_words_dict = {
                "$V": "$v",
                "$R": "$r",
                "=": " ",
                "SIN": "sin",
                "SINH": "sinh",
                "ARCSIN": "arcsin",
                "ASIN": "asin",
                "ARCSINH": "arcsinh",
                "ASINH": "asinh",
                "COS": "cos",
                "COSH": "cosh",
                "ARCCOS": "arccos",
                "ACOS": "acos",
                "ARCCOSH": "arccosh",
                "ACOSH": "acosh",
                "TAN": "tan",
                "TANH": "tanh",
                "ARCTAN": "arctan",
                "ATAN": "atan",
                "ARCTANH": "arctanh",
                "ATANH": "atanh",
                "SQRT": "sqrt",
                "Wurzel": "sqrt",
                "wurzel": "sqrt",
                "ABS": "abs",
                "LN": "ln",
                "LOG": "log"
            }

            formula = ' '.join([self.replace_words_dict.get(i,i) for i in formula.split()])

            return formula

        # <------------ INIT ----------->
        self.ff_res_name = ff_res_name
        self.ff_res_formula = ff_res_formula
        self.ff_res_formula_length = len(str(self.ff_res_formula))
        self.ff_res_min = str(ff_res_min)
        self.ff_res_min_length = len(str(self.ff_res_min))
        self.ff_res_max = str(ff_res_max)
        self.ff_res_max_length = len(str(self.ff_res_max))
        self.ff_res_prec = str(ff_res_prec)
        self.ff_res_tol = str(ff_res_tol)
        self.ff_res_tol_length = len(str(self.ff_res_tol))


        self.ff_res_points = str(ff_res_points)
        self.ff_res_points_length = len(self.ff_res_points)
        self.ff_res_unit = ff_res_unit
        self.ff_res_unit_length = len(str(self.ff_res_unit))


        # ILIAS kann nicht mit "$Vx" statt "$vx" oder "$Rx" statt "$rx"  umgehen (kleines statt großes "V" für Variablen)
        # In der Ergebnisgleichung darf kein "=" verwendet werden! Es erscheint keine Fehlermeldung, jedoch werden die Ergebnisse
        # aus der ILIAS-Berechnung immer auf "0" gesetzt
        self.ff_res_formula = replace_words_in_formula(self.ff_res_formula)




        # <------------ FORMELFRAGE ERGEBNIS STRUKTUR (in XML)  ----------->
        # Hier wird die Struktur des Ergebnis-Teils (z.B. $r1) in XML geschrieben
        # Wenn der Ergebnisteil mit Einheiten verwendet wird, müssen entsprechend Daten in "resultunits" eingetragen werden
        # s for string length: "9" -> precision = "9" characters
        # rangemin: "s" for read string-like type --> "10*1000"

        qtimetadatafield = ET.SubElement(xml_qtimetadata, 'qtimetadatafield')
        fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
        fieldlabel.text = self.ff_res_name
        fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')


        # Mit Einheiten:
        if self.ff_res_unit != "":
            fieldentry.text = "a:10:{" \
                              "s:9:\"precision\";i:" + self.ff_res_prec + ";" \
                              "s:9:\"tolerance\";s:" + self.ff_res_tol_length + ":\"" + self.ff_res_tol + "\";" \
                              "s:8:\"rangemin\";s:" + self.ff_res_min_length + ":\"" + self.ff_res_min + "\";" \
                              "s:8:\"rangemax\";s:" + self.ff_res_max_length + ":\"" + self.ff_res_max + "\";" \
                              "s:6:\"points\";s:1:\"" + self.ff_res_points + "\";" \
                              "s:7:\"formula\";s:" + self.ff_res_formula_length + ":\"" + self.ff_res_formula + "\";" \
                              "s:6:\"rating\";s:0:\"\";" \
                              "s:4:\"unit\";s:" + str(self.ff_res_unit_length) + ":\"" + self.ff_res_unit + "\";" \
                              "s:9:\"unitvalue\";s:" + str(len(Formelfrage.unit_table(self, self.ff_res_unit))) + ":\"" + Formelfrage.unit_table(self, self.ff_res_unit) + "\";" \
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

        # Ohne Einheiten:
        else:
            fieldentry.text = "a:10:{" \
                              "s:9:\"precision\";i:" + self.ff_res_prec + ";" \
                              "s:9:\"tolerance\";s:" + str(self.ff_res_tol_length) + ":\"" + self.ff_res_tol + "\";" \
                              "s:8:\"rangemin\";s:" + str(self.ff_res_min_length) + ":\"" + self.ff_res_min + "\";" \
                              "s:8:\"rangemax\";s:" + str(self.ff_res_max_length) + ":\"" + self.ff_res_max + "\";" \
                              "s:6:\"points\";s:" + str(self.ff_res_points_length) + ":\"" + self.ff_res_points + "\";" \
                              "s:7:\"formula\";s:" + str(self.ff_res_formula_length) + ":\"" + self.ff_res_formula + "\";" \
                              "s:6:\"rating\";s:0:\"\";" \
                              "s:4:\"unit\";s:0:\"\";" \
                              "s:9:\"unitvalue\";s:0:\"\";" \
                              "s:11:\"resultunits\";a:0:{}" \
                              "}"



# <------------ FORMELFRAGE-TEST ERSTELLEN ----------->
class Create_Formelfrage_Test(Formelfrage):

    def __init__(self, entry_to_index_dict):
        self.ff_db_entry_to_index_dict = entry_to_index_dict

        test_generator_modul_ilias_test_struktur.Create_ILIAS_Test.__init__(self,
                                                                            self.ff_db_entry_to_index_dict,
                                                                            self.formelfrage_test_tst_file_path_template,
                                                                            self.formelfrage_test_tst_file_path_output,
                                                                            self.formelfrage_test_qti_file_path_template,
                                                                            self.formelfrage_test_qti_file_path_output,
                                                                            self.ff_ilias_test_title_entry.get(),
                                                                            self.create_formelfrage_test_entry.get(),
                                                                            self.ff_question_type_entry.get(),
                                                                            )

        if self.ff_var_create_test_settings_check.get() == 1:
            test_generator_modul_test_einstellungen.Test_Einstellungen_GUI.create_settings(self, self.test_settings_database_path, self.test_settings_database_table, self.ff_selected_profile_for_test_settings_box.get())



        self.excel_id_list =[]
        self.excel_temp_list = []
        for t in range(len(self.ff_collection_of_question_titles)):
            self.excel_temp_list = self.ff_collection_of_question_titles[t].split(' ')
            self.excel_id_list.append(self.excel_temp_list[0])



        self.id_dublicates_counter = Counter(self.excel_id_list)
        self.id_dublicates_results = [k for k, v in self.id_dublicates_counter.items() if v > 1]

        self.titels_dublicates_counter = Counter(self.ff_collection_of_question_titles)
        self.titles_dublicates_results = [k for k, v in self.titels_dublicates_counter.items() if v > 1]

        dublicate_id_warning = ""
        dublicate_title_warning = ""

        if len(self.id_dublicates_results) >= 1 or len(self.titles_dublicates_results) >= 1:
            dublicate_id_warning = "ACHTUNG!\nErstellter Fragentest enthält doppelte Fragen:" + "\n"

        if len(self.id_dublicates_results) >= 1:
            dublicate_id_warning += "\n\n" + "Fragen-ID" + "\n"
            for i in range(len(self.id_dublicates_results)):
                dublicate_id_warning +=  "---> " + str(self.id_dublicates_results[i]) + "\n"

        if len(self.titles_dublicates_results) >= 1:
            dublicate_title_warning = "Fragen-Titel" + "\n"
            for i in range(len(self.titles_dublicates_results)):
                dublicate_title_warning += "---> " + str(self.titles_dublicates_results[i]) + "\n"


        messagebox.showinfo("Fragentest erstellen", "Fragentest wurde erstellt!" + "\n\n" + dublicate_id_warning + "\n\n" + dublicate_title_warning)



# <------------ FORMELFRAGE-POOL ERSTELLEN ----------->
class Create_Formelfrage_Pool(Formelfrage):

    def __init__(self, entry_to_index_dict, var_create_all_questions, var_create_multiple_question_pools_from_tax):
        self.ff_entry_to_index_dict = entry_to_index_dict
        self.ff_var_create_question_pool_all = var_create_all_questions
        self.var_create_multiple_question_pools_from_tax = var_create_multiple_question_pools_from_tax
        self.ff_pool_entry = self.create_formelfrage_pool_entry.get()
        self.taxonomy_collection_no_dublicates = []

        self.pool_number_list = []
        self.taxonomy_number_list = []
        self.directory_number_list = []
        self.oid_number_list_temp = []
        self.oid_number_list = []



        # Wertebereich berechnen für Fragenpool Einträge
        #if var_calculate_value_range_for_pool_ids == 1:
        #    print("Wertebereich für Pool-IDs berechnen")
        #    Formelfrage.ff_calculate_value_range_function_in_GUI(self, self.ff_pool_entry)

        # "Normalerweise" wird nur ein Fragenpool erstellt
        # Wenn mehrere Fragenpools "nach Taxonomie getrennt" erstellt werden sollen, wird "self.number_of_pool"
        # auf die Anzahl der Taxonomien gesetzt
        self.number_of_pools = 1



        # Wenn "nach Taxonomie getrennte Fragenpools" == 1:
        if self.ff_var_create_multiple_question_pools_from_tax_check.get() == 1:

            self.tax_entries_from_db_list = []
            self.oid_entries_from_db_list = []
            self.tax_and_oid_entries_from_db_list = []
            self.tax_and_oid_entries_from_db_list_sorted = []
            self.ids_with_same_tax_list = []
            self.list_of_lists = []




            # Verbindung mit Datenbank
            conn = sqlite3.connect(self.database_formelfrage_path)
            c = conn.cursor()
            c.execute("SELECT *, oid FROM %s" % self.ff_database_table)
            ff_db_records = c.fetchall()

            # Alle Einträge aus der DB nehmen
            if self.ff_var_create_question_pool_all == 1:
                for ff_db_record in ff_db_records:
                    self.oid_entries_from_db_list.append(int(ff_db_record[len(ff_db_record) - 1]))
                    self.tax_entries_from_db_list.append(ff_db_record[self.ff_db_entry_to_index_dict['question_pool_tag']])

                #self.oid_entries_from_db_list.pop(0)
                #self.tax_entries_from_db_list.pop(0)



            # ID's aus dem Eingabefeld nehmen
            else:

                self.ff_pool_entry_list = []
                self.ff_pool_entry_list = self.ff_pool_entry.split(',')

                for ff_db_record in ff_db_records:
                    if str(ff_db_record[len(ff_db_record) - 1]) in self.ff_pool_entry_list:
                        self.oid_entries_from_db_list.append(int(ff_db_record[len(ff_db_record) - 1]))
                        self.tax_entries_from_db_list.append(ff_db_record[self.ff_db_entry_to_index_dict['question_pool_tag']])



            # Listen zusammenfügen
            for i in range(len(self.oid_entries_from_db_list)):
                self.tax_and_oid_entries_from_db_list.append([self.oid_entries_from_db_list[i], self.tax_entries_from_db_list[i]])


            #print(self.oid_entries_from_db_list)
            #print(self.tax_entries_from_db_list)

            # Liste muss sortiert sein (Alphabetisch)  itemgetter(1) nimmt den Wert aus Fach 1 aus den Listen in der Liste
            # Bsp. Format von "self.tax_and_oid_entries_from_db_list" = [[2, '1'], [3, '2'], [4, '2'], [5, '3'], [6, '3']]
            # hier: '1', '2', '2', '3', '3'
            self.tax_and_oid_entries_from_db_list_sorted = sorted(self.tax_and_oid_entries_from_db_list, key=itemgetter(1))




            # Taxonomie der Fragen (ohne doppelte Einträge)
            self.taxonomy_collection_no_dublicates = list(dict.fromkeys(self.tax_entries_from_db_list))


            new_list = []

            # 1. Feld auslesen (Tax_id)
            # Bsp. Format von "self.tax_and_oid_entries_from_db_list" = [[2, '1'], [3, '2'], [4, '2'], [5, '3'], [6, '3']]
            # Taxonomien sind hier als '1', '2','3' deklariert
            # Tax_id im Bsp. self.id_temp = '1'
            self.id_temp = self.tax_and_oid_entries_from_db_list_sorted[0][1]
            #new_list.append(self.tax_and_oid_entries_from_db_list[0][0])

            for k in range(len(self.tax_and_oid_entries_from_db_list_sorted)):

                if self.tax_and_oid_entries_from_db_list_sorted[k][1] == self.id_temp:
                    new_list.append(self.tax_and_oid_entries_from_db_list_sorted[k][0])

                else:

                    self.list_of_lists.append(new_list)
                    new_list = []
                    new_list.append(self.tax_and_oid_entries_from_db_list_sorted[k][0])
                    self.id_temp = self.tax_and_oid_entries_from_db_list_sorted[k][1]




            # new_list wird nur der list_of_lists hinzugefügt wenn die Taxonomien unterschiedlich sind
            # Da die letzten Taxonomien gleich sein können, muss nochmal manuell der Befehl gestartet werden
            self.list_of_lists.append(new_list)

            self.number_of_pools = len(self.list_of_lists)



        # Die __init__ wird bei einem Knopfdruck auf "ILIAS-Fragenpool erstellen" ausgeführt
        # Es werden XML-Dateien und Ordner mit einer aufsteigenden ID erstellt.
        for pool_number in range(self.number_of_pools):


            if self.var_create_multiple_question_pools_from_tax == 1:



                self.string_entry = ','.join(map(str, self.list_of_lists[pool_number]))
                self.ff_pool_entry = self.string_entry


            self.ilias_id_pool_img_dir, self.ilias_id_pool_qpl_dir, self.pool_qti_file_path_output, self.pool_qpl_file_path_output, self.ilias_id_pool_qti_xml, self.file_max_id, self.taxonomy_file_question_pool = test_generator_modul_ilias_test_struktur.Create_ILIAS_Pool.__init__(
                                                                                                                                                                                                                    self, self.project_root_path, self.formelfrage_files_path_pool_output,
                                                                                                                                                                                                                            self.formelfrage_files_path_pool_output, self.formelfrage_pool_qti_file_path_template,
                                                                                                                                                                                                                            self.ff_ilias_test_title_entry.get(), self.ff_pool_entry, self.ff_question_type_name,
                                                                                                                                                                                                                            self.database_formelfrage_path, self.ff_database_table, self.ff_db_entry_to_index_dict,
                                                                                                                                                                                                                            self.ff_var_create_question_pool_all)



            # Bestimmt den Pfad zum spezifischen erstellten Formelfrage-Pool Ordner
            # z.B.: ...ILIAS-Formelfrage\ff_ilias_pool_abgabe\1596569820__0__qpl_1115713
            self.ff_specific_pool_dir_path = os.path.join(self.formelfrage_files_path_pool_output, self.ilias_id_pool_qpl_dir)


            # Variablen für Bildschirmausgabe sammeln
            self.pool_number_list.append(pool_number)
            self.directory_number_list.append(self.ilias_id_pool_qpl_dir)
            self.oid_number_list_temp = self.ff_pool_entry.split(',')
            self.oid_number_list.append(len(self.oid_number_list_temp))

            # Formelfrage Fragen erstellen
            Create_Formelfrage_Questions.__init__(self,
                                                   self.ff_db_entry_to_index_dict,
                                                   self.ff_pool_entry,
                                                   "question_pool",
                                                   self.ilias_id_pool_img_dir,
                                                   self.ilias_id_pool_qpl_dir,
                                                   self.formelfrage_pool_qti_file_path_template,
                                                   self.pool_qti_file_path_output,
                                                   self.pool_qpl_file_path_output,
                                                   self.ilias_id_pool_qti_xml,
                                                   self.file_max_id,
                                                   self.taxonomy_file_question_pool)


            # In der erstellten XML Datei muss "&amp;" gegen "&" getauscht werden
            test_generator_modul_ilias_test_struktur.Additional_Funtions.replace_character_in_xml_file(self, self.pool_qti_file_path_output)

            # Taxonomien werden für erstellte Pools nicht verwendet
            if self.ff_var_remove_pool_tags_for_tax_check.get() == 0:
                # Hier wird die Taxonomie des Fragenpools bearbeitet / konfiguriert
                test_generator_modul_taxonomie_und_textformatierung.Taxonomie.create_taxonomy_for_pool(self,
                                                                                                       self.ff_pool_entry,
                                                                                                       self.ff_var_create_question_pool_all,
                                                                                                       self.database_formelfrage_path,
                                                                                                       "formelfrage_table",
                                                                                                       self.ff_entry_to_index_dict,
                                                                                                       self.taxonomy_file_question_pool,
                                                                                                       self.pool_qti_file_path_output,
                                                                                                       pool_number,
                                                                                                       self.number_of_pools
                                                                                                       )

            # Abgeschlossener Fragenpool abgelegt

            print("______________________________________________________________________")
            print("FRAGENPOOL ABGESCHLOSSEN")
            print(" ---> Erstellt im Ordner \"" + "ff_ilias_pool_abgabe\\" + self.ilias_id_pool_qpl_dir)


            self.zip_output_path = os.path.join(self.ff_specific_pool_dir_path, self.ilias_id_pool_qpl_dir)
            self.zip_output_path2 = os.path.join(self.ff_specific_pool_dir_path, "test")

            # Zip Ordner erstellen
            def zip(src, dst):
                zf = zipfile.ZipFile("%s.zip" % (dst), "w", zipfile.ZIP_DEFLATED)
                abs_src = os.path.abspath(src)
                for dirname, subdirs, files in os.walk(src):
                    for filename in files:
                        absname = os.path.abspath(os.path.join(dirname, filename))
                        arcname = absname[len(abs_src)-len(self.ilias_id_pool_qpl_dir):]
                        #print('zipping %s as %s' % (os.path.join(dirname, filename), arcname))
                        zf.write(absname, arcname)
                zf.close()

            zip(os.path.join(self.formelfrage_files_path_pool_output, self.ilias_id_pool_qpl_dir), os.path.join(self.formelfrage_files_path_pool_output, self.ilias_id_pool_qpl_dir))

        string_collection = ""

        if self.var_create_multiple_question_pools_from_tax == 1:
            for i in range(len(self.pool_number_list)):
                string_collection += "Fragenpool: " + str(self.pool_number_list[i]+1) + "/" + str(len(self.pool_number_list)) + "\n" + \
                                     "Abgelegt im Ordner: " + str(self.directory_number_list[i]) + "\n" + \
                                     "Taxonomie: " + str(self.taxonomy_collection_no_dublicates[i]) + "\n" + \
                                     "Anzahl der Fragen: " + str(self.oid_number_list[i]) + " \n" + \
                                     "_____________________________________________________________" + "\n" + \
                                     "\n"


        self.excel_id_list =[]
        self.excel_temp_list = []
        for t in range(len(self.ff_collection_of_question_titles)):
            self.excel_temp_list = self.ff_collection_of_question_titles[t].split(' ')
            self.excel_id_list.append(self.excel_temp_list[0])



        self.id_dublicates_counter = Counter(self.excel_id_list)
        self.id_dublicates_results = [k for k, v in self.id_dublicates_counter.items() if v > 1]

        self.titels_dublicates_counter = Counter(self.ff_collection_of_question_titles)
        self.titles_dublicates_results = [k for k, v in self.titels_dublicates_counter.items() if v > 1]

        dublicate_id_warning = ""
        dublicate_title_warning = ""

        if len(self.id_dublicates_results) >= 1 or len(self.titles_dublicates_results) >= 1:
            dublicate_id_warning = "ACHTUNG!\nErstellter Fragenpool enthält doppelte Fragen:" + "\n"

        if len(self.id_dublicates_results) >= 1:
            dublicate_id_warning += "\n\n" + "Fragen-ID" + "\n"
            for i in range(len(self.id_dublicates_results)):
                dublicate_id_warning +=  "---> " + str(self.id_dublicates_results[i]) + "\n"

        if len(self.titles_dublicates_results) >= 1:
            dublicate_title_warning = "Fragen-Titel" + "\n"
            for i in range(len(self.titles_dublicates_results)):
                dublicate_title_warning += "---> " + str(self.titles_dublicates_results[i]) + "\n"


        messagebox.showinfo("Fragenpool erstellen", "Fragenpool wurde erstellt!" + "\n\n" + dublicate_id_warning + "\n\n" + dublicate_title_warning + "\n\n"+ string_collection)
