
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
from Test_Generator_Module import test_generator_modul_taxonomie_und_textformatierung
from Test_Generator_Module import test_generator_modul_ilias_test_struktur
from Test_Generator_Module import test_generator_modul_ilias_import_test_datei

class SingleChoice:
    def __init__(self, app, singlechoice_tab, project_root_path):
        self.singlechoice_tab = singlechoice_tab

############## SET QUESTION_TYPE SPECIFIC NAMES FOR DATABASE AND WORBOOK/SHEET
        # Name des Fragentyps
        self.sc_question_type_name = "singlechoice"

        # Name für Datenbank und Tabelle
        self.sc_database = "ilias_singlechoice_db.db"
        self.sc_database_table = "singlechoice_table"

        # Name für Tabellenkalulations-Datei und Tabelle
        self.sc_xlsx_workbook_name = "SingleChoice_DB_export_file"
        self.sc_xlsx_worksheet_name = "SingleChoice - Database"

############## SET IMAGE VARIABLES

        # Die Variablen müssen am Anfang des Programms gesetzt werden, um diese an andere Funktionen weitergeben zu können
        self.sc_description_img_name_1 = ""
        self.sc_description_img_data_1 = ""
        self.sc_description_img_path_1 = ""

        self.sc_description_img_name_2 = ""
        self.sc_description_img_data_2 = ""
        self.sc_description_img_path_2 = ""

        self.sc_description_img_name_3 = ""
        self.sc_description_img_data_3 = ""
        self.sc_description_img_path_3 = ""


############## DEFINE SINGLECHOICE PATHS

        # Pfad des Projekts und des SC-Moduls
        self.project_root_path = project_root_path
        self.singlechoice_files_path = os.path.normpath(os.path.join(self.project_root_path, "ILIAS-SingleChoice"))
        self.singlechoice_files_path_pool_output = os.path.normpath(os.path.join(self.singlechoice_files_path, "sc_ilias_pool_abgabe"))

        # Pfad für die Datenbank
        self.database_singlechoice_path = os.path.normpath(os.path.join(self.project_root_path, "Test_Generator_Datenbanken", "ilias_singlechoice_db.db"))

        # Pfad für ILIAS-Test Vorlage
        self.singlechoice_test_qti_file_path_template = os.path.normpath(os.path.join(self.singlechoice_files_path, "sc_test_qti_und_tst_dateien_vorlage", "ilias_test_vorlage__qti__.xml"))
        self.singlechoice_test_tst_file_path_template = os.path.normpath(os.path.join(self.singlechoice_files_path, "sc_test_qti_und_tst_dateien_vorlage", "ilias_test_vorlage__tst__.xml"))


        # Pfad für ILIAS-Test Dateien (zum hochladen in ILIAS)
        self.singlechoice_test_qti_file_path_output = os.path.normpath(os.path.join(self.singlechoice_files_path,"sc_ilias_test_abgabe", "1604407426__0__tst_2040314", "1604407426__0__qti_2040314.xml"))
        self.singlechoice_test_tst_file_path_output = os.path.normpath(os.path.join(self.singlechoice_files_path,"sc_ilias_test_abgabe", "1604407426__0__tst_2040314", "1604407426__0__tst_2040314.xml"))
        self.singlechoice_test_img_file_path = os.path.normpath(os.path.join(self.singlechoice_files_path,"sc_ilias_test_abgabe", "1604407426__0__tst_2040314", "objects"))


        # Pfad für ILIAS-Pool Vorlage
        self.singlechoice_pool_qti_file_path_template = os.path.normpath(os.path.join(self.singlechoice_files_path, "sc_pool_qti_und_qpl_dateien_vorlage", "ilias_pool_vorlage__qti__.xml"))
        self.singlechoice_pool_qpl_file_path_template = os.path.normpath(os.path.join(self.singlechoice_files_path, "sc_pool_qti_und_qpl_dateien_vorlage", "ilias_pool_vorlage__qpl__.xml"))


        # Pfad für ILIAS-Pool Dateien (zum hochladen in ILIAS)
        # Die Pfade für die qti.xml und qpl.xml werden erst zur Laufzeit bestimmt.
        # Die Deklaration ist daher unter "class Create_SingleChoice_Pool"
        self.singlechoice_pool_directory_output = os.path.normpath(os.path.join(self.singlechoice_files_path,"sc_ilias_pool_abgabe"))


        # Pfad zur Ablage von Bildern
        self.sc_image_directory = "Bilder"

###################### "DATENBANK ENTRIES UND INDEX DICT  ###################

        # Dictionary aus zwei Listen erstellen
        self.sc_db_find_entries = []
        self.sc_db_find_indexes = []
        self.sc_db_column_names_list = []
        self.sc_collection_of_question_titles = []

        connect = sqlite3.connect(self.database_singlechoice_path)
        cursor = connect.execute('select * from ' + self.sc_database_table)
        self.sc_db_column_names_list = list(map(lambda x: x[0], cursor.description))
        self.db_column_names_string = ', :'.join(self.sc_db_column_names_list)
        self.db_column_names_string = ":" + self.db_column_names_string

        for i in range(len(self.sc_db_column_names_list)):
            self.sc_db_find_indexes.append(i)

        """
        # Durch list(map(lambdax: x[0])) werden die Spaltennamen aus der DB ausgelesen
        cursor = conn.execute('select * from ' + self.sc_database_table)
        db_column_names_list = list(map(lambda x: x[0], cursor.description))
        db_column_names_string  = ', :'.join(db_column_names_list)
        db_column_names_string  = ":" + db_column_names_string
        """

        self.sc_db_entry_to_index_dict = dict(zip((self.sc_db_column_names_list), (self.sc_db_find_indexes)))

        connect.commit()
        connect.close()


############## FRAMES

        self.sc_frame_ilias_test_title = LabelFrame(self.singlechoice_tab, text="Testname & Autor", padx=5, pady=5)
        self.sc_frame_ilias_test_title.grid(row=0, column=0, padx=10, pady=10, sticky="NW")

        self.sc_frame = LabelFrame(self.singlechoice_tab, text="Singlechoice", padx=5, pady=5)
        self.sc_frame.grid(row=1, column=0, padx=10, pady=10, sticky="NW")

        self.sc_frame_question_attributes = LabelFrame(self.singlechoice_tab, text="Fragen Attribute", padx=5, pady=5)
        self.sc_frame_question_attributes.grid(row=2, column=0, padx=155, pady=10, sticky="NE")

        self.sc_frame_database = LabelFrame(self.singlechoice_tab, text="Singlechoice-Datenbank", padx=5, pady=5)
        self.sc_frame_database.grid(row=2, column=0, padx=10, pady=10, sticky="NW")

        self.sc_frame_create_singlechoice_test = LabelFrame(self.singlechoice_tab, text="SC-Test erstellen", padx=5, pady=5)
        self.sc_frame_create_singlechoice_test.grid(row=2, column=0, padx=250, pady=120, sticky="NE")


        self.sc_frame_taxonomy_settings = LabelFrame(self.singlechoice_tab, text="Taxonomie Einstellungen", padx=5, pady=5)
        self.sc_frame_taxonomy_settings.grid(row=0, column=1, padx=10, pady=10, sticky="NW")

        self.sc_frame_question_description_functions = LabelFrame(self.singlechoice_tab, text="Fragentext Funktionen", padx=5, pady=5)
        self.sc_frame_question_description_functions.grid(row=1, column=1, padx=10, pady=10, sticky="NW")

        self.sc_frame_excel_import_export = LabelFrame(self.singlechoice_tab, text="Excel Import/Export", padx=5, pady=5)
        self.sc_frame_excel_import_export.grid(row=2, column=1, padx=10, pady=10, sticky="NW")

        self.sc_frame_question_permutation = LabelFrame(self.singlechoice_tab, text="Fragen - Permutation", padx=5, pady=5)
        self.sc_frame_question_permutation.grid(row=2, column=1,padx=10, pady=120,   sticky="NW")


        self.sc_frame_description_picture = LabelFrame(self.singlechoice_tab, text="Fragen-Text Bild", padx=5, pady=5)
        self.sc_frame_description_picture.grid(row=1, column=2, padx=10, pady=10, sticky="NW")


 ###################### "Testname & Autor" - FRAME   -------- LABELS / ENTRYS / BUTTONS  ################
 
        self.sc_ilias_test_title_label = Label(self.sc_frame_ilias_test_title, text="Name des Tests")
        self.sc_ilias_test_title_label.grid(row=0, column=0, sticky=W)

        self.sc_ilias_test_title_entry = Entry(self.sc_frame_ilias_test_title, width=60)
        self.sc_ilias_test_title_entry.grid(row=0, column=1, sticky=W, padx=30)

        self.sc_ilias_test_autor_label = Label(self.sc_frame_ilias_test_title, text="Autor")
        self.sc_ilias_test_autor_label.grid(row=1, column=0, sticky=W)

        self.sc_ilias_test_autor_entry = Entry(self.sc_frame_ilias_test_title, width=60)
        self.sc_ilias_test_autor_entry.grid(row=1, column=1, sticky=W, padx=30)

###################### "Fragen-Text Bild" - FRAME   -------- LABELS / ENTRYS / BUTTONS  ################

        # Hinzufügen Bild 1
        self.sc_var_use_image_1 = IntVar()
        self.sc_check_use_image_1_in_description = Checkbutton(self.sc_frame_question_description_functions, text="Bild 1 hochladen?", variable=self.sc_var_use_image_1, onvalue=1, offvalue=0)
        self.sc_check_use_image_1_in_description.deselect()
        self.sc_check_use_image_1_in_description.grid(row=5, column=0, sticky=W, padx=90, pady=(10, 0))

        # Hinzufügen Bild 2
        self.sc_var_use_image_2 = IntVar()
        self.sc_check_use_image_2_in_description = Checkbutton(self.sc_frame_question_description_functions, text="Bild 2 hochladen?", variable=self.sc_var_use_image_2, onvalue=1, offvalue=0)
        self.sc_check_use_image_2_in_description.deselect()
        self.sc_check_use_image_2_in_description.grid(row=6, column=0, sticky=W, padx=90)

        # Hinzufügen Bild 3
        self.sc_var_use_image_3 = IntVar()
        self.sc_check_use_image_3_in_description = Checkbutton(self.sc_frame_question_description_functions, text="Bild 3 hochladen?", variable=self.sc_var_use_image_3, onvalue=1, offvalue=0)
        self.sc_check_use_image_3_in_description.deselect()
        self.sc_check_use_image_3_in_description.grid(row=7, column=0, sticky=W, padx=90)

        # Buttons - Bild hinzufügen & Bild löschen
        self.sc_add_img_to_description_btn = Button(self.sc_frame_question_description_functions, text="Bild hinzufügen", command=lambda: sc_add_image_to_description_and_create_labels())
        self.sc_add_img_to_description_btn.grid(row=8, column=0, sticky=W, padx = 10, pady=(20,0))



        def sc_add_image_to_description_and_create_labels():
            # Erstelle Labels
            self.sc_question_description_img_1_filename_label = Label(self.sc_frame_description_picture, text=self.sc_description_img_name_1)
            self.sc_question_description_img_2_filename_label = Label(self.sc_frame_description_picture, text=self.sc_description_img_name_2)
            self.sc_question_description_img_3_filename_label = Label(self.sc_frame_description_picture, text=self.sc_description_img_name_3)

            self.sc_description_img_name_1, self.sc_description_img_name_2, self.sc_description_img_name_3, self.sc_description_img_path_1, self.sc_description_img_path_2, self.sc_description_img_path_3, self.sc_question_description_img_1_filename_label, self.sc_question_description_img_2_filename_label, self.sc_question_description_img_3_filename_label = test_generator_modul_ilias_test_struktur.Additional_Funtions.add_image_to_description(
                    self,
                    self.sc_var_use_image_1.get(),
                    self.sc_var_use_image_2.get(),
                    self.sc_var_use_image_3.get(),
                    self.sc_frame_description_picture,
                    self.sc_description_img_name_1,
                    self.sc_description_img_name_2,
                    self.sc_description_img_name_3,
                    self.sc_description_img_path_1,
                    self.sc_description_img_path_2,
                    self.sc_description_img_path_3,
                    )


        self.sc_remove_img_from_description_btn = Button(self.sc_frame_question_description_functions, text="Bild entfernen", command=lambda: sc_add_image_to_description_and_delete_labels())
        self.sc_remove_img_from_description_btn.grid(row=8, column=0, sticky=W, padx=120, pady=(20,0))

        def sc_add_image_to_description_and_delete_labels():
            self.sc_description_img_name_1, self.sc_description_img_name_2, self.sc_description_img_name_3 = test_generator_modul_ilias_test_struktur.Additional_Funtions.delete_image_from_description(
                 self,
                 self.sc_var_use_image_1.get(),
                 self.sc_var_use_image_2.get(),
                 self.sc_var_use_image_3.get(),
                 self.sc_question_description_img_1_filename_label,
                 self.sc_question_description_img_2_filename_label,
                 self.sc_question_description_img_3_filename_label,
                 self.sc_description_img_name_1,
                 self.sc_description_img_name_2,
                 self.sc_description_img_name_3,
            )

###################### "Taxonomie Einstellungen" - FRAME   -------- LABELS / ENTRYS / BUTTONS  ################
        self.sc_taxonomy_settings_btn = Button(self.sc_frame_taxonomy_settings, text="Taxonomie-Einstellungen",command=lambda: test_generator_modul_taxonomie_und_textformatierung.Taxonomie.__init__(self))
        self.sc_taxonomy_settings_btn.grid(row=3, column=0, columnspan = 2, padx=10, sticky="W")

###################### "Fragentext Funktionen" - FRAME   -------- LABELS / ENTRYS / BUTTONS  ###################
        self.add_latex_term_btn = Button(self.sc_frame_question_description_functions, text="Text \"Latex\"", command=lambda: test_generator_modul_taxonomie_und_textformatierung.Textformatierung.text_latex(self, self.sc_question_description_main_entry))
        self.add_latex_term_btn.grid(row=1, column=0, padx=10, sticky="W")

        self.set_text_sub_btn = Button(self.sc_frame_question_description_functions, text="Text \"Tiefgestellt\"", command=lambda: test_generator_modul_taxonomie_und_textformatierung.Textformatierung.text_sub(self, self.sc_question_description_main_entry))
        self.set_text_sub_btn .grid(row=2, column=0, padx=10, pady=(10, 0), sticky="W")

        self.set_text_sup_btn = Button(self.sc_frame_question_description_functions, text="Text \"Hochgestellt\"", command=lambda: test_generator_modul_taxonomie_und_textformatierung.Textformatierung.text_sup(self, self.sc_question_description_main_entry))
        self.set_text_sup_btn.grid(row=3, column=0, padx=10, sticky="W")

        self.set_text_italic_btn = Button(self.sc_frame_question_description_functions, text="Text \"Kursiv\"", command=lambda: test_generator_modul_taxonomie_und_textformatierung.Textformatierung.text_italic(self, self.sc_question_description_main_entry))
        self.set_text_italic_btn.grid(row=4, column=0, padx=10, sticky="W")

        self.set_postion_for_picture_1_btn = Button(self.sc_frame_question_description_functions, text="Pos. Bild 1", command=lambda: test_generator_modul_taxonomie_und_textformatierung.Textformatierung.set_position_for_picture_1(self, self.sc_question_description_main_entry))
        self.set_postion_for_picture_1_btn.grid(row=5, column=0, padx=10, pady=(10, 0), sticky="W")

        self.set_postion_for_picture_2_btn = Button(self.sc_frame_question_description_functions, text="Pos. Bild 2", command=lambda: test_generator_modul_taxonomie_und_textformatierung.Textformatierung.set_position_for_picture_2(self, self.sc_question_description_main_entry))
        self.set_postion_for_picture_2_btn.grid(row=6, column=0, padx=10,  sticky="W")

        self.set_postion_for_picture_3_btn = Button(self.sc_frame_question_description_functions, text="Pos. Bild 3", command=lambda: test_generator_modul_taxonomie_und_textformatierung.Textformatierung.set_position_for_picture_3(self, self.sc_question_description_main_entry))
        self.set_postion_for_picture_3_btn.grid(row=7, column=0, padx=10,  sticky="W")



###################### "Fragen Attribute" - FRAME   -------- LABELS / ENTRYS / BUTTONS  ###################

        self.sc_question_difficulty_label = Label(self.sc_frame_question_attributes, text="Schwierigkeit")
        self.sc_question_difficulty_label.grid(row=0, column=0, pady=5, padx=5, sticky=W)

        self.sc_question_difficulty_entry = Entry(self.sc_frame_question_attributes, width=15)
        self.sc_question_difficulty_entry.grid(row=0, column=1, pady=5, padx=5, sticky=W)

        self.sc_question_category_label = Label(self.sc_frame_question_attributes, text="Fragenkategorie")
        self.sc_question_category_label.grid(row=1, column=0, pady=5, padx=5, sticky=W)

        self.sc_question_category_entry = Entry(self.sc_frame_question_attributes, width=15)
        self.sc_question_category_entry.grid(row=1, column=1, pady=5, padx=5, sticky=W)

        self.sc_question_type_label = Label(self.sc_frame_question_attributes, text="Fragen-Typ")
        self.sc_question_type_label.grid(row=0, column=2, pady=5, padx=5, sticky=W)

        self.sc_question_type_entry = Entry(self.sc_frame_question_attributes, width=15)
        self.sc_question_type_entry.grid(row=0, column=3, pady=5, padx=5, sticky=W)
        self.sc_question_type_entry.insert(0, "Singlechoice")

        self.sc_question_pool_tag_label = Label(self.sc_frame_question_attributes, text="Pool-Tag")
        self.sc_question_pool_tag_label.grid(row=1, column=2, pady=5, padx=5, sticky=W)

        self.sc_question_pool_tag_entry = Entry(self.sc_frame_question_attributes, width=15)
        self.sc_question_pool_tag_entry.grid(row=1, column=3, pady=5, padx=5, sticky=W)






 ###################### "Single Choice" - FRAME   -------- LABELS / ENTRYS / BUTTONS  ###################

        self.sc_question_author_label = Label(self.sc_frame, text="Fragen-Autor")
        self.sc_question_author_label.grid(row=0, column=0, sticky=W, padx=10, pady=(10, 0))
        self.sc_question_author_entry = Entry(self.sc_frame, width=30)
        self.sc_question_author_entry.grid(row=0, column=1, pady=(10, 0), sticky=W)

        self.sc_question_title_label = Label(self.sc_frame, text="Fragen-Titel")
        self.sc_question_title_label.grid(row=1, column=0, sticky=W, padx=10, pady=(10, 0))
        self.sc_question_title_entry = Entry(self.sc_frame, width=60)
        self.sc_question_title_entry.grid(row=1, column=1, pady=(10, 0), sticky=W)

        self.sc_question_description_title_label = Label(self.sc_frame, text="Fragen-Beschreibung")
        self.sc_question_description_title_label.grid(row=2, column=0, sticky=W, padx=10)
        self.sc_question_description_title_entry = Entry(self.sc_frame, width=60)
        self.sc_question_description_title_entry.grid(row=2, column=1, sticky=W)

        self.sc_question_textfield_label = Label(self.sc_frame, text="Fragen-Text")
        self.sc_question_textfield_label.grid(row=3, column=0, sticky=W, padx=10)

        self.sc_bar = Scrollbar(self.sc_frame)
        self.sc_question_description_main_entry = Text(self.sc_frame, height=6, width=80, font=('Helvetica', 9))
        self.sc_bar.grid(row=3, column=2, sticky=W)
        self.sc_question_description_main_entry.grid(row=3, column=1, pady=10, sticky=W)
        self.sc_bar.config(command=self.sc_question_description_main_entry.yview)
        self.sc_question_description_main_entry.config(yscrollcommand=self.sc_bar.set)

        self.sc_processing_time_label = Label(self.sc_frame, text="Bearbeitungsdauer")
        self.sc_processing_time_label.grid(row=4, column=0, sticky=W, pady=(5, 0), padx=10)

        self.sc_processing_time_label = Label(self.sc_frame, text="Std:")
        self.sc_processing_time_label.grid(row=4, column=1, sticky=W, pady=(5, 0))
        self.sc_processing_time_label = Label(self.sc_frame, text="Min:")
        self.sc_processing_time_label.grid(row=4, column=1, sticky=W, padx=70, pady=(5, 0))
        self.sc_processing_time_label = Label(self.sc_frame, text="Sek:")
        self.sc_processing_time_label.grid(row=4, column=1, sticky=W, padx=145, pady=(5, 0))

        self.sc_picture_preview_pixel_label = Label(self.sc_frame, text="Bild-Vorschaugröße (in Pixel)")
        self.sc_picture_preview_pixel_label.grid(row=4, column=1, sticky=E, padx=70)

        self.sc_picture_preview_pixel_entry = Entry(self.sc_frame, width=10)
        self.sc_picture_preview_pixel_entry.grid(row=4, column=1, sticky=E,  padx=0)
        self.sc_picture_preview_pixel_entry.insert(END, "300")

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

        self.sc_proc_hours_box.current(23)
        self.sc_proc_minutes_box.current(0)
        self.sc_proc_seconds_box.current(0)

        def sc_selected_hours(event):
            self.selected_hours = self.sc_proc_hours_box.get()
            print(self.selected_hours)

        def sc_selected_minutes(event):
            self.selected_minutes = self.sc_proc_minutes_box.get()
            print(self.selected_minutes)

        def sc_selected_seconds(event):
            self.selected_seconds = self.sc_proc_seconds_box.get()
            print(self.selected_seconds)

        self.sc_proc_hours_box.bind("<<ComboboxSelected>>", sc_selected_hours)
        self.sc_proc_hours_box.bind("<<ComboboxSelected>>", sc_selected_minutes)
        self.sc_proc_hours_box.bind("<<ComboboxSelected>>", sc_selected_seconds)

        self.sc_proc_hours_box.grid(row=4, column=1, sticky=W, padx=25, pady=(5, 0))
        self.sc_proc_minutes_box.grid(row=4, column=1, sticky=W, padx=100, pady=(5, 0))
        self.sc_proc_seconds_box.grid(row=4, column=1, sticky=W, padx=170, pady=(5, 0))

        self.sc_mix_questions_label = Label(self.sc_frame, text="Fragen mischen")
        self.sc_mix_questions_label.grid(row=5, column=0, sticky=W, padx=10, pady=(5, 0))

        self.sc_var_mix_questions = StringVar()
        self.sc_check_mix_questions = Checkbutton(self.sc_frame, text="", variable=self.sc_var_mix_questions,
                                                  onvalue="Yes", offvalue="No")
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
                sc_var8_remove()
                sc_var9_remove()
                sc_var10_remove()


            elif self.sc_numbers_of_answers_box.get() == '2':
                sc_var2_show()
                sc_var3_remove()
                sc_var4_remove()
                sc_var5_remove()
                sc_var6_remove()
                sc_var7_remove()
                sc_var8_remove()
                sc_var9_remove()
                sc_var10_remove()

            elif self.sc_numbers_of_answers_box.get() == '3':
                sc_var2_show()
                sc_var3_show()
                sc_var4_remove()
                sc_var5_remove()
                sc_var6_remove()
                sc_var7_remove()
                sc_var8_remove()
                sc_var9_remove()
                sc_var10_remove()

            elif self.sc_numbers_of_answers_box.get() == '4':
                sc_var2_show()
                sc_var3_show()
                sc_var4_show()
                sc_var5_remove()
                sc_var6_remove()
                sc_var7_remove()
                sc_var8_remove()
                sc_var9_remove()
                sc_var10_remove()

            elif self.sc_numbers_of_answers_box.get() == '5':
                sc_var2_show()
                sc_var3_show()
                sc_var4_show()
                sc_var5_show()
                sc_var6_remove()
                sc_var7_remove()
                sc_var8_remove()
                sc_var9_remove()
                sc_var10_remove()

            elif self.sc_numbers_of_answers_box.get() == '6':
                sc_var2_show()
                sc_var3_show()
                sc_var4_show()
                sc_var5_show()
                sc_var6_show()
                sc_var7_remove()
                sc_var8_remove()
                sc_var9_remove()
                sc_var10_remove()

            elif self.sc_numbers_of_answers_box.get() == '7':
                sc_var2_show()
                sc_var3_show()
                sc_var4_show()
                sc_var5_show()
                sc_var6_show()
                sc_var7_show()
                sc_var8_remove()
                sc_var9_remove()
                sc_var10_remove()

            elif self.sc_numbers_of_answers_box.get() == '8':
                sc_var2_show()
                sc_var3_show()
                sc_var4_show()
                sc_var5_show()
                sc_var6_show()
                sc_var7_show()
                sc_var8_show()
                sc_var9_remove()
                sc_var10_remove()

            elif self.sc_numbers_of_answers_box.get() == '9':
                sc_var2_show()
                sc_var3_show()
                sc_var4_show()
                sc_var5_show()
                sc_var6_show()
                sc_var7_show()
                sc_var8_show()
                sc_var9_show()
                sc_var10_remove()

            elif self.sc_numbers_of_answers_box.get() == '10':
                sc_var2_show()
                sc_var3_show()
                sc_var4_show()
                sc_var5_show()
                sc_var6_show()
                sc_var7_show()
                sc_var8_show()
                sc_var9_show()
                sc_var10_show()

        self.sc_numbers_of_answers_box_label = Label(self.sc_frame, text="Anzahl der Antworten")
        self.sc_numbers_of_answers_box_label.grid(row=8, column=0, sticky=W, padx=10, pady=(5, 0))
        self.sc_numbers_of_answers_value = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
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
        

        ######  VARIABLES
        self.sc_var1_img_data = ""
        self.sc_var2_img_data = ""
        self.sc_var3_img_data = ""
        self.sc_var3_img_data = ""
        self.sc_var4_img_data = ""
        self.sc_var5_img_data = ""
        self.sc_var6_img_data = ""
        self.sc_var7_img_data = ""
        self.sc_var8_img_data = ""
        self.sc_var9_img_data = ""
        self.sc_var10_img_data = ""

        self.sc_var1_img_data_encoded64_string = ""
        self.sc_var2_img_data_encoded64_string = ""
        self.sc_var3_img_data_encoded64_string = ""
        self.sc_var4_img_data_encoded64_string = ""
        self.sc_var5_img_data_encoded64_string = ""
        self.sc_var6_img_data_encoded64_string = ""
        self.sc_var7_img_data_encoded64_string = ""
        self.sc_var8_img_data_encoded64_string = ""
        self.sc_var9_img_data_encoded64_string = ""
        self.sc_var10_img_data_encoded64_string = ""

        self.sc_var1_img_data_encoded64_string = "Encoded1-Test"

        # Antwort-Text
        self.sc_var1_answer_entry = Entry(self.sc_frame, width=45)
        self.sc_var2_answer_entry = Entry(self.sc_frame, width=45)
        self.sc_var3_answer_entry = Entry(self.sc_frame, width=45)
        self.sc_var4_answer_entry = Entry(self.sc_frame, width=45)
        self.sc_var5_answer_entry = Entry(self.sc_frame, width=45)
        self.sc_var6_answer_entry = Entry(self.sc_frame, width=45)
        self.sc_var7_answer_entry = Entry(self.sc_frame, width=45)
        self.sc_var8_answer_entry = Entry(self.sc_frame, width=45)
        self.sc_var9_answer_entry = Entry(self.sc_frame, width=45)
        self.sc_var10_answer_entry = Entry(self.sc_frame, width=45)

        # Punkte
        self.sc_var1_points_entry = Entry(self.sc_frame, width=8)
        self.sc_var2_points_entry = Entry(self.sc_frame, width=8)
        self.sc_var3_points_entry = Entry(self.sc_frame, width=8)
        self.sc_var4_points_entry = Entry(self.sc_frame, width=8)
        self.sc_var5_points_entry = Entry(self.sc_frame, width=8)
        self.sc_var6_points_entry = Entry(self.sc_frame, width=8)
        self.sc_var7_points_entry = Entry(self.sc_frame, width=8)
        self.sc_var8_points_entry = Entry(self.sc_frame, width=8)
        self.sc_var9_points_entry = Entry(self.sc_frame, width=8)
        self.sc_var10_points_entry = Entry(self.sc_frame, width=8)
##################
        

        self.sc_var1_img_data_entry = Entry(self.sc_frame, width=8)
        self.sc_var2_img_data_entry = Entry(self.sc_frame, width=8)
        self.sc_var3_img_data_entry = Entry(self.sc_frame, width=8)
        self.sc_var4_img_data_entry = Entry(self.sc_frame, width=8)
        self.sc_var5_img_data_entry = Entry(self.sc_frame, width=8)
        self.sc_var6_img_data_entry = Entry(self.sc_frame, width=8)
        self.sc_var7_img_data_entry = Entry(self.sc_frame, width=8)
        self.sc_var8_img_data_entry = Entry(self.sc_frame, width=8)
        self.sc_var9_img_data_entry = Entry(self.sc_frame, width=8)
        self.sc_var10_img_data_entry = Entry(self.sc_frame, width=8)




        self.sc_var1_img_path_entry = Entry(self.sc_frame, width=8)
        self.sc_var2_img_path_entry = Entry(self.sc_frame, width=8)
        self.sc_var3_img_path_entry = Entry(self.sc_frame, width=8)
        self.sc_var4_img_path_entry = Entry(self.sc_frame, width=8)
        self.sc_var5_img_path_entry = Entry(self.sc_frame, width=8)
        self.sc_var6_img_path_entry = Entry(self.sc_frame, width=8)
        self.sc_var7_img_path_entry = Entry(self.sc_frame, width=8)
        self.sc_var8_img_path_entry = Entry(self.sc_frame, width=8)
        self.sc_var9_img_path_entry = Entry(self.sc_frame, width=8)
        self.sc_var10_img_path_entry = Entry(self.sc_frame, width=8)


 





################





        # ------------------------------- VARIABLES BUTTONS - SELECT IMAGE --------------------------------------------
        self.sc_var1_select_img_btn = Button(self.sc_frame, text="Datei wählen", command=lambda: SingleChoice.sc_add_image_to_answer(self, self.sc_var1_img_label_entry, self.sc_var1_img_data_entry, self.sc_var1_img_path_entry))
        self.sc_var2_select_img_btn = Button(self.sc_frame, text="Datei wählen", command=lambda: SingleChoice.sc_add_image_to_answer(self, self.sc_var2_img_label_entry, self.sc_var2_img_data_entry, self.sc_var2_img_path_entry))
        self.sc_var3_select_img_btn = Button(self.sc_frame, text="Datei wählen", command=lambda: SingleChoice.sc_add_image_to_answer(self, self.sc_var3_img_label_entry, self.sc_var3_img_data_entry, self.sc_var3_img_path_entry))
        self.sc_var4_select_img_btn = Button(self.sc_frame, text="Datei wählen", command=lambda: SingleChoice.sc_add_image_to_answer(self, self.sc_var4_img_label_entry, self.sc_var4_img_data_entry, self.sc_var4_img_path_entry))
        self.sc_var5_select_img_btn = Button(self.sc_frame, text="Datei wählen", command=lambda: SingleChoice.sc_add_image_to_answer(self, self.sc_var5_img_label_entry, self.sc_var5_img_data_entry, self.sc_var5_img_path_entry))
        self.sc_var6_select_img_btn = Button(self.sc_frame, text="Datei wählen", command=lambda: SingleChoice.sc_add_image_to_answer(self, self.sc_var6_img_label_entry, self.sc_var6_img_data_entry, self.sc_var6_img_path_entry))
        self.sc_var7_select_img_btn = Button(self.sc_frame, text="Datei wählen", command=lambda: SingleChoice.sc_add_image_to_answer(self, self.sc_var7_img_label_entry, self.sc_var7_img_data_entry, self.sc_var7_img_path_entry))
        self.sc_var8_select_img_btn = Button(self.sc_frame, text="Datei wählen", command=lambda: SingleChoice.sc_add_image_to_answer(self, self.sc_var8_img_label_entry, self.sc_var8_img_data_entry, self.sc_var8_img_path_entry))
        self.sc_var9_select_img_btn = Button(self.sc_frame, text="Datei wählen", command=lambda: SingleChoice.sc_add_image_to_answer(self, self.sc_var9_img_label_entry, self.sc_var9_img_data_entry, self.sc_var9_img_path_entry))
        self.sc_var10_select_img_btn = Button(self.sc_frame, text="Datei wählen", command=lambda: SingleChoice.sc_add_image_to_answer(self, self.sc_var10_img_label_entry, self.sc_var10_img_data_entry, self.sc_var10_img_path_entry))





###################### "SingleChoice-Datenbank" - FRAME   -------- LABELS / ENTRYS / BUTTONS  ###################




        self.sc_database_show_db_singlechoice_btn = Button(self.sc_frame_database, text="SC - Datenbank anzeigen", command=lambda: test_generator_modul_datenbanken_anzeigen.MainGUI.__init__(self, self.database_singlechoice_path, "singlechoice_table"))
        self.sc_database_show_db_singlechoice_btn.grid(row=0, column=0, sticky=W, pady=5)

        self.sc_database_save_id_to_db_singlechoice_btn = Button(self.sc_frame_database, text="Speichern unter neuer ID", command=lambda: SingleChoice.sc_save_id_to_db(self))
        self.sc_database_save_id_to_db_singlechoice_btn.grid(row=1, column=0, sticky=W, pady=5)

        self.sc_database_delete_id_from_db_btn = Button(self.sc_frame_database, text="ID Löschen", command=lambda: SingleChoice.sc_delete_id_from_db(self))
        self.sc_database_delete_id_from_db_btn.grid(row=6, column=0, sticky=W, pady=5)
        self.sc_delete_box = Entry(self.sc_frame_database, width=10)
        self.sc_delete_box.grid(row=6, column=0, padx=80, sticky=W)

        self.sc_database_new_question_btn = Button(self.sc_frame_database, text="GUI Einträge leeren", command=lambda: SingleChoice.sc_clear_GUI(self))
        self.sc_database_new_question_btn.grid(row=8, column=0, sticky=W, pady=5)

        self.sc_database_edit_btn = Button(self.sc_frame_database, text="Aktuellen Eintrag editieren", command=lambda: SingleChoice.sc_edit_id_from_db(self))
        self.sc_database_edit_btn.grid(row=3, column=0, sticky=W, pady=5)


        self.sc_database_load_id_btn = Button(self.sc_frame_database, text="ID Laden", command=lambda: SingleChoice.sc_load_id_from_db(self, self.sc_db_entry_to_index_dict))
        self.sc_database_load_id_btn.grid(row=4, column=0, sticky=W, pady=(15,0))
        self.sc_load_box = Entry(self.sc_frame_database, width=10)
        self.sc_load_box.grid(row=4, column=0, sticky=W, padx=80, pady=(15,0))


        # Checkbox - "Fragentext mit Highlighting?"
        self.sc_highlight_question_text_label = Label(self.sc_frame_database, text="Fragentext mit Highlighting?")
        self.sc_highlight_question_text_label.grid(row=5, column=0, pady=5, padx=5)

        self.sc_var_highlight_question_text = IntVar()
        self.sc_check_highlight_question_text = Checkbutton(self.sc_frame_database, text="", variable=self.sc_var_highlight_question_text, onvalue=1, offvalue=0)
        self.sc_check_highlight_question_text.deselect()
        self.sc_check_highlight_question_text.grid(row=5, column=0, sticky=E)


        # Checkbox - "Alle DB Einträge löschen?"
        self.sc_delete_all_label = Label(self.sc_frame_database, text="Alle DB Einträge löschen?")
        self.sc_delete_all_label.grid(row=7, column=0, pady=5, padx=5)

        self.sc_var_delete_all = IntVar()
        self.sc_check_delete_all = Checkbutton(self.sc_frame_database, text="", variable=self.sc_var_delete_all, onvalue=1, offvalue=0)
        self.sc_check_delete_all.deselect()
        self.sc_check_delete_all.grid(row=7, column=0, sticky=E)

###################### "Excel Import/Export" - FRAME   -------- LABELS / ENTRYS / BUTTONS  ###################

        #excel_import_btn
        self.sc_excel_import_to_db_singlechoice_btn = Button(self.sc_frame_excel_import_export, text="Excel-Datei importieren", command=lambda: test_generator_modul_datenbanken_erstellen.Import_Export_Database.excel_import_to_db(self, self.sc_question_type_name, self.sc_db_entry_to_index_dict))
        self.sc_excel_import_to_db_singlechoice_btn.grid(row=0, column=1, sticky=W, pady=5, padx=10)

        # excel_export_btn
        self.sc_excel_export_to_xlsx_singlechoice_btn = Button(self.sc_frame_excel_import_export, text="Datenbank exportieren",command=lambda: test_generator_modul_datenbanken_erstellen.Import_Export_Database.excel_export_to_xlsx(self, self.project_root_path, self.sc_db_entry_to_index_dict, self.database_singlechoice_path, self.sc_database, self.sc_database_table, self.sc_xlsx_workbook_name, self.sc_xlsx_worksheet_name))
        self.sc_excel_export_to_xlsx_singlechoice_btn.grid(row=1, column=1, sticky=W, pady=5, padx=10)

        # ILIAS_testfile_import
        self.sc_import_ilias_testfile_btn = Button(self.sc_frame_excel_import_export, text="ILIAS-Datei importieren",command=lambda: test_generator_modul_ilias_import_test_datei.Import_ILIAS_Datei_in_DB.__init__(self, self.project_root_path))
        self.sc_import_ilias_testfile_btn.grid(row=2, column=1, sticky=W, pady=(20,0), padx=10)

        ##ilias test import_btn
        #self.ilias_test_import_btn = Button(self.sc_frame_excel_import_export, text="ILIAS-Test importieren",command=lambda: Database.ilias_test_to_sql_import(self))
        #self.ilias_test_import_btn.grid(row=2, column=1, sticky=W, pady=5, padx=10)


# ------------------------------- VARIABLES  - TEXT & ENTRY --------------------------------------------

        self.sc_var1_img_label_entry = Entry(self.sc_frame, width=30)
        self.sc_var2_img_label_entry = Entry(self.sc_frame, width=30)
        self.sc_var3_img_label_entry = Entry(self.sc_frame, width=30)
        self.sc_var4_img_label_entry = Entry(self.sc_frame, width=30)
        self.sc_var5_img_label_entry = Entry(self.sc_frame, width=30)
        self.sc_var6_img_label_entry = Entry(self.sc_frame, width=30)
        self.sc_var7_img_label_entry = Entry(self.sc_frame, width=30)
        self.sc_var8_img_label_entry = Entry(self.sc_frame, width=30)
        self.sc_var9_img_label_entry = Entry(self.sc_frame, width=30)
        self.sc_var10_img_label_entry = Entry(self.sc_frame, width=30)



        self.sc_answer1_label = Label(self.sc_frame, text="Antwort-Text 1")
        self.sc_answer2_label = Label(self.sc_frame, text="Antwort-Text 2")
        self.sc_answer3_label = Label(self.sc_frame, text="Antwort-Text 3")
        self.sc_answer4_label = Label(self.sc_frame, text="Antwort-Text 4")
        self.sc_answer5_label = Label(self.sc_frame, text="Antwort-Text 5")
        self.sc_answer6_label = Label(self.sc_frame, text="Antwort-Text 6")
        self.sc_answer7_label = Label(self.sc_frame, text="Antwort-Text 7")
        self.sc_answer8_label = Label(self.sc_frame, text="Antwort-Text 8")
        self.sc_answer9_label = Label(self.sc_frame, text="Antwort-Text 9")
        self.sc_answer10_label = Label(self.sc_frame, text="Antwort-Text 10")

        self.sc_answer1_label.grid(row=10, column=0, sticky=W, padx=30)
        self.sc_var1_answer_entry.grid(row=10, column=1, sticky=W)
        self.sc_var1_img_label_entry.grid(row=10, column=1, sticky=E, padx=0)
        self.sc_var1_points_entry.grid(row=10, column=2)
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

        def sc_var8_show():
            self.sc_answer8_label.grid(row=17, column=0, sticky=W, padx=30)
            self.sc_var8_answer_entry.grid(row=17, column=1, sticky=W)
            self.sc_var8_img_label_entry.grid(row=17, column=1, sticky=E, padx=0)
            self.sc_var8_points_entry.grid(row=17, column=2, sticky=W, padx=20)
            self.sc_var8_select_img_btn.grid(row=17, column=1, sticky=E, padx=200)

        def sc_var9_show():
            self.sc_answer9_label.grid(row=18, column=0, sticky=W, padx=30)
            self.sc_var9_answer_entry.grid(row=18, column=1, sticky=W)
            self.sc_var9_img_label_entry.grid(row=18, column=1, sticky=E, padx=0)
            self.sc_var9_points_entry.grid(row=18, column=2, sticky=W, padx=20)
            self.sc_var9_select_img_btn.grid(row=18, column=1, sticky=E, padx=200)

        def sc_var10_show():
            self.sc_answer10_label.grid(row=19, column=0, sticky=W, padx=30)
            self.sc_var10_answer_entry.grid(row=19, column=1, sticky=W)
            self.sc_var10_img_label_entry.grid(row=19, column=1, sticky=E, padx=0)
            self.sc_var10_points_entry.grid(row=19, column=2, sticky=W, padx=20)
            self.sc_var10_select_img_btn.grid(row=19, column=1, sticky=E, padx=200)



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

        def sc_var8_remove():
            self.sc_answer8_label.grid_remove()
            self.sc_var8_answer_entry.grid_remove()
            self.sc_var8_img_label_entry.grid_remove()
            self.sc_var8_points_entry.grid_remove()
            self.sc_var8_select_img_btn.grid_remove()

        def sc_var9_remove():
            self.sc_answer9_label.grid_remove()
            self.sc_var9_answer_entry.grid_remove()
            self.sc_var9_img_label_entry.grid_remove()
            self.sc_var9_points_entry.grid_remove()
            self.sc_var9_select_img_btn.grid_remove()

        def sc_var10_remove():
            self.sc_answer10_label.grid_remove()
            self.sc_var10_answer_entry.grid_remove()
            self.sc_var10_img_label_entry.grid_remove()
            self.sc_var10_points_entry.grid_remove()
            self.sc_var10_select_img_btn.grid_remove()










 ###################### "SC-Test erstellen" - FRAME   -------- LABELS / ENTRYS / BUTTONS  ###################

        # self.create_singlechoice_test_btn = Button(self.sc_frame_create_singlechoice_test, text="SC-Test erstellen", command=lambda:  Create_SingleChoice_Test.__init__(self, self.sc_db_entry_to_index_dict))
        # self.create_singlechoice_test_btn.grid(row=2, column=0, sticky=W)
        # self.create_singlechoice_test_entry = Entry(self.sc_frame_create_singlechoice_test, width=15)
        # self.create_singlechoice_test_entry.grid(row=2, column=1, sticky=W, padx=20)
        #
        # self.create_singlechoice_pool_btn = Button(self.sc_frame_create_singlechoice_test, text="SC-Pool erstellen", command=lambda: Create_SingleChoice_Pool.__init__(self, self.sc_db_entry_to_index_dict))
        # self.create_singlechoice_pool_btn.grid(row=3, column=0, sticky=W, pady=10)
        # self.create_singlechoice_pool_entry = Entry(self.sc_frame_create_singlechoice_test, width=15)
        # self.create_singlechoice_pool_entry.grid(row=3, column=1, sticky=W, padx=20, pady=10)

        # Button "SingleChoice-Test erstellen"
        self.create_singlechoice_test_btn = Button(self.sc_frame_create_singlechoice_test, text="SC-Test erstellen", command=lambda: Create_SingleChoice_Test.__init__(self, self.sc_db_entry_to_index_dict))
        self.create_singlechoice_test_btn.grid(row=0, column=0, sticky=W)
        self.create_singlechoice_test_entry = Entry(self.sc_frame_create_singlechoice_test, width=15)
        self.create_singlechoice_test_entry.grid(row=0, column=1, sticky=W, padx=0)

        # Checkbox "Test-Einstellungen übernehmen?"
        self.create_test_settings_label = Label(self.sc_frame_create_singlechoice_test, text="Test-Einstellungen übernehmen?")
        self.create_test_settings_label.grid(row=1, column=0, pady=5, padx=5, sticky=W)
        self.var_test_settings = IntVar()
        self.check_test_settings = Checkbutton(self.sc_frame_create_singlechoice_test, text="", variable=self.var_test_settings, onvalue=1, offvalue=0)
        self.check_test_settings.deselect()
        self.check_test_settings.grid(row=1, column=1, sticky=W)

        # Checkbox "Latex für Fragentext nutzen?"
        self.sc_use_latex_on_text_label = Label(self.sc_frame_create_singlechoice_test, text="Latex für Fragentext nutzen?")
        self.sc_use_latex_on_text_label.grid(row=2, column=0, sticky=W, padx=5)
        self.sc_var_use_latex_on_text_check = IntVar()
        self.sc_use_latex_on_text_check = Checkbutton(self.sc_frame_create_singlechoice_test, text="", variable=self.sc_var_use_latex_on_text_check, onvalue=1, offvalue=0)
        self.sc_use_latex_on_text_check.deselect()
        self.sc_use_latex_on_text_check.grid(row=2, column=1, sticky=W)




        # Checkbox "Alle Einträge aus der DB erzeugen?"
        self.sc_create_question_pool_all_label = Label(self.sc_frame_create_singlechoice_test, text="Alle Einträge aus der DB erzeugen?")
        self.sc_create_question_pool_all_label.grid(row=4, column=0, pady=(10,0), padx=5, sticky=W)
        self.sc_var_create_question_pool_all_check = IntVar()
        self.sc_create_question_pool_all = Checkbutton(self.sc_frame_create_singlechoice_test, text="", variable=self.sc_var_create_question_pool_all_check, onvalue=1, offvalue=0)
        #self.sc_var_create_question_pool_all_check.set(0)
        self.sc_create_question_pool_all.grid(row=4, column=1, sticky=W, pady=(10,0))



        # Button "SingleChoice-Fragenpool erstellen"
        self.create_singlechoice_pool_btn = Button(self.sc_frame_create_singlechoice_test, text="SC-Pool erstellen", command=lambda: Create_SingleChoice_Pool.__init__(self, self.sc_db_entry_to_index_dict, self.sc_var_create_question_pool_all_check.get()))
        self.create_singlechoice_pool_btn.grid(row=3, column=0, sticky=W, pady=(30,0))
        self.create_singlechoice_pool_entry = Entry(self.sc_frame_create_singlechoice_test, width=15)
        self.create_singlechoice_pool_entry.grid(row=3, column=1, sticky=W, padx=0, pady=(30,0))







    # Funktion dient zur Auswahl von Bildern für einzelne Antwortmöglichkeiten

    def sc_add_image_to_answer(self, picture_label_entry, picture_data_entry, picture_path_entry):

         ### Dateipfad auswählen
         self.sc_picture_path = filedialog.askopenfilename(initialdir=os.path.join(pathlib.Path().absolute(), self.sc_image_directory), title="Select a File")

         # "rindex" sucht nach einem bestimmten Zeichen in einem String, beginnend von rechts
         self.sc_picture_name = self.sc_picture_path[self.sc_picture_path.rindex('/')+1:]        # Nach dem "/" befindet sich der Dateiname
         self.sc_image_format = self.sc_picture_path[self.sc_picture_path.rindex('.'):]          # Nach dem "." befindet sich das Dateiformat z.B. .jpg

         ### Bild-Namen in entsprechendes, geleertes, Eingabefeld übertragen
         picture_label_entry.delete(0, END)
         picture_label_entry.insert(0, str(self.sc_picture_name))

         ### Bild-Daten in base64 speichern. Die XML Datei enthält die Bilder der Antworten in base64 encoded
         # "encoded64_string_raw enthält die Daten als String in der Form b'String'
         # Um die Daten in der richtigen Form zu erhalten (nur den String ohne b''), wird die Funktion .decode('utf-8') verwendet
         # Dieser String kann in der .xml Datei verwendet werden um im Ilias ein Bild zu erzeugen

         if picture_label_entry.get() != "" or picture_label_entry.get() != " ":
             with open(self.sc_picture_path, "rb") as image_file:
                 encoded64_string_raw = base64.b64encode(image_file.read())
                 picture_data_entry.delete(0, END)
                 picture_data_entry.insert(END, encoded64_string_raw.decode('utf-8'))

                 # Der Ordner für Bilder-Dateien wird unter "self.image_directory" bestimmt. (Bsp. "Bilder")
                 # Bei der Auswahl von Bildern über die GUI wird der komplette Pfad aufgenommen (Bsp. C:\user\Bilder\test.png)
                 # Der String wird nach dem Eintrag "self.image_directory" durchsucht und gibt den Index im String zurück (Bsp: 8)
                 # Dann wird von diesem index (8) beginnend, der restliche String-Teil aufgenommen (Bsp: Bilder\test.png)
                 # Der ":" sorgt dafür das nur ein Teil vom String gelesen wird (Index_Start:Index_ende (wenn für "Index_ende" nichts eingetragen wird, wird alles übernommen
                 # Es kann hier auch z.B. Index_start:-1 eingetragen werden, dann wird alles bis auf das letzte Zeichen übernommen Bsp: Bilder\test.pn)
                 self.sc_image_dir_index_for_path = self.sc_picture_path.rfind(self.sc_image_directory)
                 self.sc_picture_path_img = os.path.normpath(self.sc_picture_path[int(self.sc_image_dir_index_for_path):])

                 picture_path_entry.delete(0, END)
                 picture_path_entry.insert(END, self.sc_picture_path_img)





    def sc_save_id_to_db(self):
        conn = sqlite3.connect(self.database_singlechoice_path)
        c = conn.cursor()

        # format of duration P0Y0M0DT0H30M0S
        self.sc_test_time = "P0Y0M0DT" + self.sc_proc_hours_box.get() + "H" + self.sc_proc_minutes_box.get() + "M" + self.sc_proc_seconds_box.get() + "S"


        # Bild 1
        if self.sc_description_img_name_1 != "" or self.sc_description_img_name_1 != "EMPTY":
            # read image data in byte format
            with open(self.sc_description_img_path_1, 'rb') as image_file_1:
                self.sc_description_img_data_1 = image_file_1.read()

        else:
            self.sc_description_img_name_1= ""
            self.sc_description_img_path_1 = ""
            self.sc_description_img_data_1 = ""


        # Bild 2
        if self.sc_description_img_name_2 != "" or self.sc_description_img_name_2 != "EMPTY":
            # read image data in byte format
            with open(self.sc_description_img_path_2, 'rb') as image_file_2:
                self.sc_description_img_data_2 = image_file_2.read()

        else:
            self.sc_description_img_name_2 = ""
            self.sc_description_img_path_2 = ""
            self.sc_description_img_data_2 = ""


        # Bild 3
        if self.sc_description_img_name_3 != "" or self.sc_description_img_name_3 != "EMPTY":

            # read image data in byte format
            with open(self.sc_description_img_path_3, 'rb') as image_file_3:
                self.sc_description_img_data_3 = image_file_3.read()

        else:
            self.sc_description_img_name_3 = ""
            self.sc_description_img_path_3 = ""
            self.sc_description_img_data_3 = ""



        def sc_bind_value_for_empty_answer_image(picture_label_entry, picture_data_entry, picture_path_entry):
            if picture_label_entry.get() == "":
                picture_label_entry.insert(0, "")
                picture_data_entry.insert(0, "")
                picture_path_entry.insert(0, "")

        sc_bind_value_for_empty_answer_image(self.sc_var1_img_label_entry, self.sc_var1_img_data_entry, self.sc_var1_img_path_entry)
        sc_bind_value_for_empty_answer_image(self.sc_var2_img_label_entry, self.sc_var2_img_data_entry, self.sc_var2_img_path_entry)
        sc_bind_value_for_empty_answer_image(self.sc_var3_img_label_entry, self.sc_var3_img_data_entry, self.sc_var3_img_path_entry)
        sc_bind_value_for_empty_answer_image(self.sc_var4_img_label_entry, self.sc_var4_img_data_entry, self.sc_var4_img_path_entry)
        sc_bind_value_for_empty_answer_image(self.sc_var5_img_label_entry, self.sc_var5_img_data_entry, self.sc_var5_img_path_entry)
        sc_bind_value_for_empty_answer_image(self.sc_var6_img_label_entry, self.sc_var6_img_data_entry, self.sc_var6_img_path_entry)
        sc_bind_value_for_empty_answer_image(self.sc_var7_img_label_entry, self.sc_var7_img_data_entry, self.sc_var7_img_path_entry)
        sc_bind_value_for_empty_answer_image(self.sc_var8_img_label_entry, self.sc_var8_img_data_entry, self.sc_var8_img_path_entry)
        sc_bind_value_for_empty_answer_image(self.sc_var9_img_label_entry, self.sc_var9_img_data_entry, self.sc_var9_img_path_entry)
        sc_bind_value_for_empty_answer_image(self.sc_var10_img_label_entry, self.sc_var10_img_data_entry, self.sc_var10_img_path_entry)


        # Insert into Table
        # Reihenfolge muss mit der Datenbank übereinstimmen
        c.execute(
            "INSERT INTO singlechoice_table VALUES ("
            ":question_difficulty, :question_category, :question_type, "
            ":question_title, :question_description_title, :question_description_main, "
            ":response_1_text, :response_1_pts, :response_1_img_label, :response_1_img_string_base64_encoded, :response_1_img_path,"
            ":response_2_text, :response_2_pts, :response_2_img_label, :response_2_img_string_base64_encoded, :response_2_img_path,"
            ":response_3_text, :response_3_pts, :response_3_img_label, :response_3_img_string_base64_encoded, :response_3_img_path,"
            ":response_4_text, :response_4_pts, :response_4_img_label, :response_4_img_string_base64_encoded, :response_4_img_path,"
            ":response_5_text, :response_5_pts, :response_5_img_label, :response_5_img_string_base64_encoded, :response_5_img_path,"
            ":response_6_text, :response_6_pts, :response_6_img_label, :response_6_img_string_base64_encoded, :response_6_img_path,"
            ":response_7_text, :response_7_pts, :response_7_img_label, :response_7_img_string_base64_encoded, :response_7_img_path,"
            ":response_8_text, :response_8_pts, :response_8_img_label, :response_8_img_string_base64_encoded, :response_8_img_path,"
            ":response_9_text, :response_9_pts, :response_9_img_label, :response_9_img_string_base64_encoded, :response_9_img_path,"
            ":response_10_text, :response_10_pts, :response_10_img_label, :response_10_img_string_base64_encoded, :response_10_img_path,"
            ":picture_preview_pixel, "
            ":description_img_name_1, :description_img_data_1, :description_img_path_1, "
            ":description_img_name_2, :description_img_data_2, :description_img_path_2, "
            ":description_img_name_3, :description_img_data_3, :description_img_path_3, "
            ":test_time, :var_number, :question_pool_tag, :question_author)",
            {
                'question_difficulty': self.sc_question_difficulty_entry.get(),
                'question_category': self.sc_question_category_entry.get(),
                'question_type': self.sc_question_type_entry.get(),
                'question_title': self.sc_question_title_entry.get(),
                'question_description_title': self.sc_question_description_title_entry.get(),

                # The first part, "1.0" means that the input should be read from line one, character zero (ie: the very first character).
                # END is an imported constant which is set to the string "end". The END part means to read until the end of the text box is reached.
                # The only issue with this is that it actually adds a newline to our input. "
                # "So, in order to fix it we should change END to end-1c(Thanks Bryan Oakley) The -1c deletes 1 character, while -2c would mean delete two characters, and so on."
                'question_description_main': self.sc_question_description_main_entry.get("1.0", 'end-1c'),

                # Antwort-Text  in Datenbank-Fach: var_name
                'response_1_text': self.sc_var1_answer_entry.get(),
                'response_1_pts': self.sc_var1_points_entry.get(),
                'response_1_img_label':  self.sc_var1_img_label_entry.get(),
                'response_1_img_string_base64_encoded':  self.sc_var1_img_data_entry.get(),
                'response_1_img_path': self.sc_var1_img_path_entry.get(),

                'response_2_text': self.sc_var2_answer_entry.get(),
                'response_2_pts': self.sc_var2_points_entry.get(),
                'response_2_img_label': self.sc_var2_img_label_entry.get(),
                'response_2_img_string_base64_encoded':  self.sc_var2_img_data_entry.get(),
                'response_2_img_path': self.sc_var2_img_path_entry.get(),

                'response_3_text': self.sc_var3_answer_entry.get(),
                'response_3_pts': self.sc_var3_points_entry.get(),
                'response_3_img_label': self.sc_var3_img_label_entry.get(),
                'response_3_img_string_base64_encoded':  self.sc_var3_img_data_entry.get(),
                'response_3_img_path': self.sc_var3_img_path_entry.get(),

                'response_4_text': self.sc_var4_answer_entry.get(),
                'response_4_pts': self.sc_var4_points_entry.get(),
                'response_4_img_label': self.sc_var4_img_label_entry.get(),
                'response_4_img_string_base64_encoded':  self.sc_var4_img_data_entry.get(),
                'response_4_img_path': self.sc_var4_img_path_entry.get(),

                'response_5_text': self.sc_var5_answer_entry.get(),
                'response_5_pts': self.sc_var5_points_entry.get(),
                'response_5_img_label': self.sc_var5_img_label_entry.get(),
                'response_5_img_string_base64_encoded':  self.sc_var5_img_data_entry.get(),
                'response_5_img_path': self.sc_var5_img_path_entry.get(),

                'response_6_text': self.sc_var6_answer_entry.get(),
                'response_6_pts': self.sc_var6_points_entry.get(),
                'response_6_img_label': self.sc_var6_img_label_entry.get(),
                'response_6_img_string_base64_encoded':  self.sc_var6_img_data_entry.get(),
                'response_6_img_path': self.sc_var6_img_path_entry.get(),

                'response_7_text': self.sc_var7_answer_entry.get(),
                'response_7_pts': self.sc_var7_points_entry.get(),
                'response_7_img_label': self.sc_var7_img_label_entry.get(),
                'response_7_img_string_base64_encoded':  self.sc_var7_img_data_entry.get(),
                'response_7_img_path': self.sc_var7_img_path_entry.get(),

                'response_8_text': self.sc_var8_answer_entry.get(),
                'response_8_pts': self.sc_var8_points_entry.get(),
                'response_8_img_label': self.sc_var8_img_label_entry.get(),
                'response_8_img_string_base64_encoded':  self.sc_var8_img_data_entry.get(),
                'response_8_img_path': self.sc_var8_img_path_entry.get(),

                'response_9_text': self.sc_var9_answer_entry.get(),
                'response_9_pts': self.sc_var9_points_entry.get(),
                'response_9_img_label': self.sc_var9_img_label_entry.get(),
                'response_9_img_string_base64_encoded':  self.sc_var9_img_data_entry.get(),
                'response_9_img_path': self.sc_var9_img_path_entry.get(),

                'response_10_text': self.sc_var10_answer_entry.get(),
                'response_10_pts': self.sc_var10_points_entry.get(),
                'response_10_img_label': self.sc_var10_img_label_entry.get(),
                'response_10_img_string_base64_encoded':  self.sc_var10_img_data_entry.get(),
                'response_10_img_path': self.sc_var10_img_path_entry.get(),

                'picture_preview_pixel': self.sc_picture_preview_pixel_entry.get(),

                'description_img_name_1': self.sc_description_img_name_1,
                'description_img_data_1': self.sc_description_img_data_1,
                'description_img_path_1': self.sc_description_img_path_1,

                'description_img_name_2': self.sc_description_img_name_2,
                'description_img_data_2': self.sc_description_img_data_2,
                'description_img_path_2': self.sc_description_img_path_2,

                'description_img_name_3': self.sc_description_img_name_3,
                'description_img_data_3': self.sc_description_img_data_3,
                'description_img_path_3': self.sc_description_img_path_3,

                'test_time': self.sc_test_time,

                'var_number': "",
                'question_pool_tag': self.sc_question_pool_tag_entry.get(),
                'question_author': self.sc_question_author_entry.get()

            }
        )
        conn.commit()
        conn.close()

        print("Neuer Eintrag in die SingleChoice-Datenbank --> Fragentitel: " + str(self.sc_question_title_entry.get()))


    def sc_load_id_from_db(self, entry_to_index_dict):
        self.sc_db_entry_to_index_dict = entry_to_index_dict
        conn = sqlite3.connect(self.database_singlechoice_path)
        c = conn.cursor()
        record_id = self.sc_load_box.get()
        c.execute("SELECT * FROM singlechoice_table WHERE oid =" + record_id)
        sc_db_records = c.fetchall()

        SingleChoice.sc_clear_GUI(self)


        for sc_db_record in sc_db_records:

            self.sc_question_difficulty_entry.insert(END,  sc_db_record[self.sc_db_entry_to_index_dict['question_difficulty']] )
            self.sc_question_category_entry.insert(END,  sc_db_record[self.sc_db_entry_to_index_dict['question_category']] )
            self.sc_question_type_entry.insert(END,  sc_db_record[self.sc_db_entry_to_index_dict['question_type']] )

            self.sc_question_title_entry.insert(END,  sc_db_record[self.sc_db_entry_to_index_dict['question_title']] )
            self.sc_question_description_title_entry.insert(END,  sc_db_record[self.sc_db_entry_to_index_dict['question_description_title']] )
            self.sc_question_description_main_entry.insert(END, sc_db_record[self.sc_db_entry_to_index_dict['question_description_main']] )

            self.sc_var1_answer_entry.insert(END, sc_db_record[self.sc_db_entry_to_index_dict['response_1_text']] )
            self.sc_var2_answer_entry.insert(END, sc_db_record[self.sc_db_entry_to_index_dict['response_2_text']] )
            self.sc_var3_answer_entry.insert(END, sc_db_record[self.sc_db_entry_to_index_dict['response_3_text']] )
            self.sc_var4_answer_entry.insert(END, sc_db_record[self.sc_db_entry_to_index_dict['response_4_text']] )
            self.sc_var5_answer_entry.insert(END, sc_db_record[self.sc_db_entry_to_index_dict['response_5_text']] )
            self.sc_var6_answer_entry.insert(END, sc_db_record[self.sc_db_entry_to_index_dict['response_6_text']] )
            self.sc_var7_answer_entry.insert(END, sc_db_record[self.sc_db_entry_to_index_dict['response_7_text']] )
            self.sc_var8_answer_entry.insert(END, sc_db_record[self.sc_db_entry_to_index_dict['response_8_text']] )
            self.sc_var9_answer_entry.insert(END, sc_db_record[self.sc_db_entry_to_index_dict['response_9_text']] )
            self.sc_var10_answer_entry.insert(END, sc_db_record[self.sc_db_entry_to_index_dict['response_10_text']])

            self.sc_var1_img_label_entry.insert(END, sc_db_record[self.sc_db_entry_to_index_dict['response_1_img_label']])
            self.sc_var2_img_label_entry.insert(END, sc_db_record[self.sc_db_entry_to_index_dict['response_2_img_label']])
            self.sc_var3_img_label_entry.insert(END, sc_db_record[self.sc_db_entry_to_index_dict['response_3_img_label']])
            self.sc_var4_img_label_entry.insert(END, sc_db_record[self.sc_db_entry_to_index_dict['response_4_img_label']])
            self.sc_var5_img_label_entry.insert(END, sc_db_record[self.sc_db_entry_to_index_dict['response_5_img_label']])
            self.sc_var6_img_label_entry.insert(END, sc_db_record[self.sc_db_entry_to_index_dict['response_6_img_label']])
            self.sc_var7_img_label_entry.insert(END, sc_db_record[self.sc_db_entry_to_index_dict['response_7_img_label']])
            self.sc_var8_img_label_entry.insert(END, sc_db_record[self.sc_db_entry_to_index_dict['response_8_img_label']])
            self.sc_var9_img_label_entry.insert(END, sc_db_record[self.sc_db_entry_to_index_dict['response_9_img_label']])
            self.sc_var10_img_label_entry.insert(END, sc_db_record[self.sc_db_entry_to_index_dict['response_10_img_label']])

            self.sc_var1_img_data_entry.insert(END, sc_db_record[self.sc_db_entry_to_index_dict['response_1_img_string_base64_encoded']])
            self.sc_var2_img_data_entry.insert(END, sc_db_record[self.sc_db_entry_to_index_dict['response_2_img_string_base64_encoded']])
            self.sc_var3_img_data_entry.insert(END, sc_db_record[self.sc_db_entry_to_index_dict['response_3_img_string_base64_encoded']])
            self.sc_var4_img_data_entry.insert(END, sc_db_record[self.sc_db_entry_to_index_dict['response_4_img_string_base64_encoded']])
            self.sc_var5_img_data_entry.insert(END, sc_db_record[self.sc_db_entry_to_index_dict['response_5_img_string_base64_encoded']])
            self.sc_var6_img_data_entry.insert(END, sc_db_record[self.sc_db_entry_to_index_dict['response_6_img_string_base64_encoded']])
            self.sc_var7_img_data_entry.insert(END, sc_db_record[self.sc_db_entry_to_index_dict['response_7_img_string_base64_encoded']])
            self.sc_var8_img_data_entry.insert(END, sc_db_record[self.sc_db_entry_to_index_dict['response_8_img_string_base64_encoded']])
            self.sc_var9_img_data_entry.insert(END, sc_db_record[self.sc_db_entry_to_index_dict['response_9_img_string_base64_encoded']])
            self.sc_var10_img_data_entry.insert(END, sc_db_record[self.sc_db_entry_to_index_dict['response_10_img_string_base64_encoded']])

            self.sc_var1_img_path_entry.insert(END, sc_db_record[self.sc_db_entry_to_index_dict['response_1_img_path']])
            self.sc_var2_img_path_entry.insert(END, sc_db_record[self.sc_db_entry_to_index_dict['response_2_img_path']])
            self.sc_var3_img_path_entry.insert(END, sc_db_record[self.sc_db_entry_to_index_dict['response_3_img_path']])
            self.sc_var4_img_path_entry.insert(END, sc_db_record[self.sc_db_entry_to_index_dict['response_4_img_path']])
            self.sc_var5_img_path_entry.insert(END, sc_db_record[self.sc_db_entry_to_index_dict['response_5_img_path']])
            self.sc_var6_img_path_entry.insert(END, sc_db_record[self.sc_db_entry_to_index_dict['response_6_img_path']])
            self.sc_var7_img_path_entry.insert(END, sc_db_record[self.sc_db_entry_to_index_dict['response_7_img_path']])
            self.sc_var8_img_path_entry.insert(END, sc_db_record[self.sc_db_entry_to_index_dict['response_8_img_path']])
            self.sc_var9_img_path_entry.insert(END, sc_db_record[self.sc_db_entry_to_index_dict['response_9_img_path']])
            self.sc_var10_img_path_entry.insert(END, sc_db_record[self.sc_db_entry_to_index_dict['response_10_img_path']])

            self.sc_var1_points_entry.insert(END, sc_db_record[self.sc_db_entry_to_index_dict['response_1_pts']])
            self.sc_var2_points_entry.insert(END, sc_db_record[self.sc_db_entry_to_index_dict['response_2_pts']])
            self.sc_var3_points_entry.insert(END, sc_db_record[self.sc_db_entry_to_index_dict['response_3_pts']])
            self.sc_var4_points_entry.insert(END, sc_db_record[self.sc_db_entry_to_index_dict['response_4_pts']])
            self.sc_var5_points_entry.insert(END, sc_db_record[self.sc_db_entry_to_index_dict['response_5_pts']])
            self.sc_var6_points_entry.insert(END, sc_db_record[self.sc_db_entry_to_index_dict['response_6_pts']])
            self.sc_var7_points_entry.insert(END, sc_db_record[self.sc_db_entry_to_index_dict['response_7_pts']])
            self.sc_var8_points_entry.insert(END, sc_db_record[self.sc_db_entry_to_index_dict['response_8_pts']])
            self.sc_var9_points_entry.insert(END, sc_db_record[self.sc_db_entry_to_index_dict['response_9_pts']])
            self.sc_var10_points_entry.insert(END, sc_db_record[self.sc_db_entry_to_index_dict['response_10_pts']])

            self.sc_description_img_name_1 = sc_db_record[self.sc_db_entry_to_index_dict['description_img_name_1']]
            self.sc_description_img_data_1 = sc_db_record[self.sc_db_entry_to_index_dict['description_img_data_1']]
            self.sc_description_img_path_1 = sc_db_record[self.sc_db_entry_to_index_dict['description_img_path_1']]

            self.sc_description_img_name_2 = sc_db_record[self.sc_db_entry_to_index_dict['description_img_name_2']]
            self.sc_description_img_data_2 = sc_db_record[self.sc_db_entry_to_index_dict['description_img_data_2']]
            self.sc_description_img_path_2 = sc_db_record[self.sc_db_entry_to_index_dict['description_img_path_2']]

            self.sc_description_img_name_3 = sc_db_record[self.sc_db_entry_to_index_dict['description_img_name_3']]
            self.sc_description_img_data_3 = sc_db_record[self.sc_db_entry_to_index_dict['description_img_data_3']]
            self.sc_description_img_path_3 = sc_db_record[self.sc_db_entry_to_index_dict['description_img_path_3']]



        conn.commit()
        conn.close()




    def sc_edit_id_from_db(self):
        
        # Verbindung mit der Datenbank
        conn = sqlite3.connect(self.database_singlechoice_path)
        c = conn.cursor()

        # ID der Frage aus dem Eingabefeld "ID Laden" auslesen
        record_id = self.sc_load_box.get()

        # Format von Testdauer in der XML Datei:  P0Y0M0DT0H30M0S
        self.sc_test_time = "P0Y0M0DT" + self.sc_proc_hours_box.get() + "H" + self.sc_proc_minutes_box.get() + "M" + self.sc_proc_seconds_box.get() + "S"

        # Ist ein Bild-Name vorhanden, dann das Bild über den Pfad einlesen
        # Sonst auf "EMPTY" setzen
        # Bilder werden als byte eingelesen "rb" = read byte

        # Fragen-Text Bild 1
        if self.sc_description_img_name_1 != "" or self.sc_description_img_name_1 != "EMPTY":
            with open( self.sc_description_img_path_1, 'rb') as description_image_file_1:
                self.sc_description_img_data_1 = description_image_file_1.read()
        
        else:
            self.sc_description_img_name_1 = ""
            self.sc_description_img_data_1 = ""
            self.sc_description_img_path_1 = ""
            
        # Fragen-Text Bild 2
        if self.sc_description_img_name_2 != "" or self.sc_description_img_name_2 != "EMPTY":
            with open( self.sc_description_img_path_2, 'rb') as description_image_file_2:
                self.sc_description_img_data_2 = description_image_file_2.read()
        
        else:
            self.sc_description_img_name_2 = ""
            self.sc_description_img_data_2 = ""
            self.sc_description_img_path_2 = ""
        
        # Fragen-Text Bild 3
        if self.sc_description_img_name_3 != "" or self.sc_description_img_name_3 != "EMPTY":
            with open( self.sc_description_img_path_3, 'rb') as description_image_file_3:
                self.sc_description_img_data_3 = description_image_file_3.read()
        
        else:
            self.sc_description_img_name_3 = ""
            self.sc_description_img_data_3 = ""
            self.sc_description_img_path_3 = ""


        c.execute("""UPDATE singlechoice_table SET
                    question_difficulty = :question_difficulty,
                    question_category = :question_category,
                    question_type = :question_type,

                    question_title = :question_title,
                    question_description_title = :question_description_title,
                    question_description_main = :question_description_main,
                    
                    'response_1_text'= :response_1_text,
                'response_1_pts'= :response_1_pts,
                'response_1_img_label'= :response_1_img_label,
                'response_1_img_string_base64_encoded'= :response_1_img_string_base64_encoded,
                'response_1_img_path' = :response_1_img_path,

                'response_2_text'= :response_2_text,
                'response_2_pts'= :response_2_pts,
                'response_2_img_label'= :response_2_img_label,
                'response_2_img_string_base64_encoded'= :response_2_img_string_base64_encoded,
                'response_2_img_path'= :response_2_img_path,

                'response_3_text'= : response_3_text,
                'response_3_pts'= :response_3_pts,
                'response_3_img_label'= :response_3_img_label,
                'response_3_img_string_base64_encoded'= :response_3_img_string_base64_encoded,
                'response_3_img_path'= :response_3_img_path,

                'response_4_text'= :response_4_text,
                'response_4_pts'= :response_4_pts,
                'response_4_img_label'= :response_4_img_label,
                'response_4_img_string_base64_encoded'= :response_4_img_string_base64_encoded,
                'response_4_img_path'= :response_4_img_path,

                'response_5_text'= :response_5_text,
                'response_5_pts'= :response_5_pts,
                'response_5_img_label'= :response_5_img_label,
                'response_5_img_string_base64_encoded'= :response_5_img_string_base64_encoded,
                'response_5_img_path'= :response_5_img_path,

                'response_6_text'= :response_6_text,
                'response_6_pts'= :response_6_pts,
                'response_6_img_label'= :response_6_img_label,
                'response_6_img_string_base64_encoded'= :response_6_img_string_base64_encoded,
                'response_6_img_path'= :response_6_img_path,

                'response_7_text'= :response_7_text,
                'response_7_pts'= :response_7_pts,
                'response_7_img_label'= :response_7_img_label,
                'response_7_img_string_base64_encoded'= :response_7_img_string_base64_encoded,
                'response_7_img_path'= :response_7_img_path,

                'response_8_text'= :response_8_text,
                'response_8_pts'= :response_8_pts,
                'response_8_img_label'= :response_8_img_label,
                'response_8_img_string_base64_encoded'= :response_8_img_string_base64_encoded,
                'response_8_img_path'= :response_8_img_path,

                'response_9_text'= :response_9_text,
                'response_9_pts'= :response_9_pts,
                'response_9_img_label'= :response_9_img_label,
                'response_9_img_string_base64_encoded'= :response_9_img_string_base64_encoded,
                'response_9_img_path'= :response_9_img_path,

                'response_10_text'= :response_10_text,
                'response_10_pts'= :response_10_pts,
                'response_10_img_label'= :response_10_img_label,
                'response_10_img_string_base64_encoded'= :response_10_img_string_base64_encoded,
                'response_10_img_path'= :response_10_img_path,

                'picture_preview_pixel'= :'picture_preview_pixel',

                'description_img_name_1'= :description_img_name_1,
                'description_img_data_1'= :description_img_data_1,
                'description_img_path_1'= :description_img_path_1,

                'description_img_name_2'= :description_img_name_2,
                'description_img_data_2'= :description_img_data_2,
                'description_img_path_2'= :description_img_path_2,

                'description_img_name_3'= :description_img_name_3,
                'description_img_data_3'= :description_img_data_3,
                'description_img_path_3'= :description_img_path_3,

                'test_time'= :test_time,

                'var_number'= :var_number,
                'question_pool_tag'= :question_pool_tag,
                'question_author'= :question_author
                
                WHERE oid = :oid""",
                {'question_difficulty': self.sc_question_difficulty_entry.get(),
                 'question_category': self.sc_question_category_entry.get(),
                 'question_type': self.sc_question_type_entry.get(),

                 'question_title': self.sc_question_title_entry.get(),
                 'question_description_title': self.sc_question_description_title_entry.get(),
                 'question_description_main': self.sc_question_description_main_entry.get("1.0", 'end-1c'),

                 'response_1_text': self.sc_var1_answer_entry.get(),
                 'response_1_pts': self.sc_var1_points_entry.get(),
                 'response_1_img_label': self.sc_var1_img_label_entry.get(),
                 'response_1_img_string_base64_encoded': self.sc_var1_img_data_entry.get(),
                 'response_1_img_path': self.sc_var1_img_path_entry.get(),

                 'response_2_text': self.sc_var2_answer_entry.get(),
                 'response_2_pts': self.sc_var2_points_entry.get(),
                 'response_2_img_label': self.sc_var2_img_label_entry.get(),
                 'response_2_img_string_base64_encoded': self.sc_var2_img_data_entry.get(),
                 'response_2_img_path': self.sc_var2_img_path_entry.get(),

                 'response_3_text': self.sc_var3_answer_entry.get(),
                 'response_3_pts': self.sc_var3_points_entry.get(),
                 'response_3_img_label': self.sc_var3_img_label_entry.get(),
                 'response_3_img_string_base64_encoded': self.sc_var3_img_data_entry.get(),
                 'response_3_img_path': self.sc_var3_img_path_entry.get(),

                 'response_4_text': self.sc_var4_answer_entry.get(),
                 'response_4_pts': self.sc_var4_points_entry.get(),
                 'response_4_img_label': self.sc_var4_img_label_entry.get(),
                 'response_4_img_string_base64_encoded': self.sc_var4_img_data_entry.get(),
                 'response_4_img_path': self.sc_var4_img_path_entry.get(),

                 'response_5_text': self.sc_var5_answer_entry.get(),
                 'response_5_pts': self.sc_var5_points_entry.get(),
                 'response_5_img_label': self.sc_var5_img_label_entry.get(),
                 'response_5_img_string_base64_encoded': self.sc_var5_img_data_entry.get(),
                 'response_5_img_path': self.sc_var5_img_path_entry.get(),

                 'response_6_text': self.sc_var6_answer_entry.get(),
                 'response_6_pts': self.sc_var6_points_entry.get(),
                 'response_6_img_label': self.sc_var6_img_label_entry.get(),
                 'response_6_img_string_base64_encoded': self.sc_var6_img_data_entry.get(),
                 'response_6_img_path': self.sc_var6_img_path_entry.get(),

                 'response_7_text': self.sc_var7_answer_entry.get(),
                 'response_7_pts': self.sc_var7_points_entry.get(),
                 'response_7_img_label': self.sc_var7_img_label_entry.get(),
                 'response_7_img_string_base64_encoded': self.sc_var7_img_data_entry.get(),
                 'response_7_img_path': self.sc_var7_img_path_entry.get(),

                 'response_8_text': self.sc_var8_answer_entry.get(),
                 'response_8_pts': self.sc_var8_points_entry.get(),
                 'response_8_img_label': self.sc_var8_img_label_entry.get(),
                 'response_8_img_string_base64_encoded': self.sc_var8_img_data_entry.get(),
                 'response_8_img_path': self.sc_var8_img_path_entry.get(),

                 'response_9_text': self.sc_var9_answer_entry.get(),
                 'response_9_pts': self.sc_var9_points_entry.get(),
                 'response_9_img_label': self.sc_var9_img_label_entry.get(),
                 'response_9_img_string_base64_encoded': self.sc_var9_img_data_entry.get(),
                 'response_9_img_path': self.sc_var9_img_path_entry.get(),

                 'response_10_text': self.sc_var10_answer_entry.get(),
                 'response_10_pts': self.sc_var10_points_entry.get(),
                 'response_10_img_label': self.sc_var10_img_label_entry.get(),
                 'response_10_img_string_base64_encoded': self.sc_var10_img_data_entry.get(),
                 'response_10_img_path': self.sc_var10_img_path_entry.get(),

                 'picture_preview_pixel': self.sc_picture_preview_pixel_entry.get(),

                 
                 
                 'description_img_name_1': self.sc_description_img_name_1,
                 'description_img_data_1': self.sc_description_img_data_1,
                 'description_img_path_1': self.sc_description_img_path_1,

                 'description_img_name_2': self.sc_description_img_name_2,
                 'description_img_data_2': self.sc_description_img_data_2,
                 'description_img_path_2': self.sc_description_img_path_2,

                 'description_img_name_3': self.sc_description_img_name_3,
                 'description_img_data_3': self.sc_description_img_data_3,
                 'description_img_path_3': self.sc_description_img_path_3,

                 'test_time': self.sc_test_time,
                 'question_pool_tag': self.sc_question_pool_tag_entry.get(),
                 'question_author': self.sc_question_author_entry.get(),
                 'oid': record_id
                 })
                 
    def sc_delete_id_from_db(self):

        self.sc_delete_box_id = ""
        self.sc_delete_box_id = self.sc_delete_box.get()

        test_generator_modul_datenbanken_erstellen.Delete_Entry_from_Database.__init__(self, self.sc_delete_box_id, self.sc_question_type_name, self.sc_var_delete_all.get(), self.project_root_path, self.sc_db_entry_to_index_dict, self.database_singlechoice_path, "singlechoice_db.db", "singlechoice_table", "SingleChoice_DB_export_file.xlsx", "Singlechoice - Database")

        self.sc_delete_box.delete(0, END)



    def sc_clear_GUI(self):
        self.sc_question_difficulty_entry.delete(0, END)
        self.sc_question_category_entry.delete(0, END)
        self.sc_question_type_entry.delete(0, END)

        self.sc_question_title_entry.delete(0, END)
        self.sc_question_description_title_entry.delete(0, END)
        self.sc_question_description_main_entry.delete('1.0', 'end-1c')

        self.sc_var1_answer_entry.delete(0, END)
        self.sc_var2_answer_entry.delete(0, END)
        self.sc_var3_answer_entry.delete(0, END)
        self.sc_var4_answer_entry.delete(0, END)
        self.sc_var5_answer_entry.delete(0, END)
        self.sc_var6_answer_entry.delete(0, END)
        self.sc_var7_answer_entry.delete(0, END)
        self.sc_var8_answer_entry.delete(0, END)
        self.sc_var9_answer_entry.delete(0, END)
        self.sc_var10_answer_entry.delete(0, END)

        self.sc_var1_img_label_entry.delete(0, END)
        self.sc_var2_img_label_entry.delete(0, END)
        self.sc_var3_img_label_entry.delete(0, END)
        self.sc_var4_img_label_entry.delete(0, END)
        self.sc_var5_img_label_entry.delete(0, END)
        self.sc_var6_img_label_entry.delete(0, END)
        self.sc_var7_img_label_entry.delete(0, END)
        self.sc_var8_img_label_entry.delete(0, END)
        self.sc_var9_img_label_entry.delete(0, END)
        self.sc_var10_img_label_entry.delete(0, END)

        self.sc_var1_points_entry.delete(0, END)
        self.sc_var2_points_entry.delete(0, END)
        self.sc_var3_points_entry.delete(0, END)
        self.sc_var4_points_entry.delete(0, END)
        self.sc_var5_points_entry.delete(0, END)
        self.sc_var6_points_entry.delete(0, END)
        self.sc_var7_points_entry.delete(0, END)
        self.sc_var8_points_entry.delete(0, END)
        self.sc_var9_points_entry.delete(0, END)
        self.sc_var10_points_entry.delete(0, END)



class Create_SingleChoice_Questions(SingleChoice):
    def __init__(self, db_entry_to_index_dict, ids_in_entry_box, question_type_test_or_pool, pool_img_dir, ilias_id_pool_qpl_dir, xml_read_qti_template_path, xml_qti_output_file_path, xml_qpl_output_file_path, max_id_pool_qti_xml, max_id, taxonomy_file_question_pool):

        self.sc_db_entry_to_index_dict = db_entry_to_index_dict
        self.sc_test_entry_splitted = ids_in_entry_box.split(",")
        self.qti_file_path_output = xml_qti_output_file_path
        self.singlechoice_pool_qpl_file_path_output = xml_qpl_output_file_path
        self.sc_mytree = ET.parse(xml_read_qti_template_path)
        self.sc_myroot = self.sc_mytree.getroot()
        self.sc_question_type_test_or_pool = question_type_test_or_pool
        self.singlechoice_pool_img_file_path = pool_img_dir           # Wird nur bei Erstellung eines Fragen-Pool verwendet. Ordnername wird erst bei Laufzeit erstellt)
        
        self.all_entries_from_db_list = []
        self.number_of_entrys = []

        self.sc_question_pool_id_list = []
        self.sc_question_title_list = []

        self.sc_ilias_id_pool_qpl_dir = ilias_id_pool_qpl_dir
        self.sc_file_max_id = max_id
        self.sc_taxonomy_file_question_pool = taxonomy_file_question_pool
        self.sc_ilias_id_pool_qti_xml = max_id_pool_qti_xml

        self.sc_number_of_questions_generated = 1

        
        print("\n")


        if self.sc_question_type_test_or_pool == "question_test":
            print("SINGLECHOICE: ILIAS-TEST WIRD ERSTELLT...  ID: " + str(ids_in_entry_box))

        else:
            print("SINGLECHOICE: ILIAS-POOL WIRD ERSTELLT...  ID: " + str(ids_in_entry_box))



        # Mit SC_Datenbank verknüpfen
        connect_sc_db = sqlite3.connect(self.database_singlechoice_path)
        cursor = connect_sc_db.cursor()

        # Prüfen ob alle Einträge generiert werden sollen (checkbox gesetzt)
        if self.sc_var_create_question_pool_all_check.get() == 1:
            conn = sqlite3.connect(self.database_singlechoice_path)
            c = conn.cursor()
            c.execute("SELECT *, oid FROM singlechoice_table")

            sc_db_records = c.fetchall()

            for sc_db_record in sc_db_records:
                self.all_entries_from_db_list.append(int(sc_db_record[len(sc_db_record) - 1]))

            self.string_temp = ','.join(map(str, self.all_entries_from_db_list))
            self.sc_test_entry_splitted = self.string_temp.split(",")

            # Eintrag mit ID "1" entspricht der Vorlage und soll nicht mit erstellt werden
            self.sc_test_entry_splitted.pop(0)

        # Sämtliche Datenbank Einträge auslesen mit der entsprechenden "oid" (Datenbank ID)
        # Datenbank ID wird automatisch bei einem neuen Eintrag erstellt (fortlaufend) und kann nicht beeinflusst werden
        cursor.execute("SELECT *, oid FROM singlechoice_table")
        sc_db_records = cursor.fetchall()


        for i in range(len(self.sc_test_entry_splitted)):
            for sc_db_record in sc_db_records:
                if str(sc_db_record[len(sc_db_record) - 1]) == self.sc_test_entry_splitted[i]:
                    for t in range(len(sc_db_record)):
                        if sc_db_record[self.sc_db_entry_to_index_dict['question_type']].lower() == self.sc_question_type_name.lower():

                            # an "sc_db_record[self.sc_db_entry_to_index_dict['question_description_main']]"
                            # darf kein extra "replace('&', "&amp;")",
                            # da bei der Bearbeitung der Frage noch die "&" replaced werden.

                            self.sc_question_difficulty                     = sc_db_record[self.sc_db_entry_to_index_dict['question_difficulty']]
                            self.sc_question_category                       = sc_db_record[self.sc_db_entry_to_index_dict['question_category']]
                            self.sc_question_type                           = sc_db_record[self.sc_db_entry_to_index_dict['question_type']]
                            self.sc_question_title                          = sc_db_record[self.sc_db_entry_to_index_dict['question_title']].replace('&', "&amp;")
                            self.sc_question_description_title              = sc_db_record[self.sc_db_entry_to_index_dict['question_description_title']].replace('&', "&amp;")
                            self.sc_question_description_main               = sc_db_record[self.sc_db_entry_to_index_dict['question_description_main']]
                           
                            self.sc_response_1_text                         = sc_db_record[self.sc_db_entry_to_index_dict['response_1_text']].replace('&', "&amp;")
                            self.sc_response_1_pts	                        = sc_db_record[self.sc_db_entry_to_index_dict['response_1_pts']]
                            self.sc_response_1_img_label	                = sc_db_record[self.sc_db_entry_to_index_dict['response_1_img_label']].replace('&', "&amp;")
                            self.sc_response_1_img_string_base64_encoded	= sc_db_record[self.sc_db_entry_to_index_dict['response_1_img_string_base64_encoded']]
                            self.sc_response_1_img_path                 	= sc_db_record[self.sc_db_entry_to_index_dict['response_1_img_path']]
                            
                            self.sc_response_2_text	                        = sc_db_record[self.sc_db_entry_to_index_dict['response_2_text']].replace('&', "&amp;")
                            self.sc_response_2_pts	                        = sc_db_record[self.sc_db_entry_to_index_dict['response_2_pts']]
                            self.sc_response_2_img_label	                = sc_db_record[self.sc_db_entry_to_index_dict['response_2_img_label']].replace('&', "&amp;")
                            self.sc_response_2_img_string_base64_encoded	= sc_db_record[self.sc_db_entry_to_index_dict['response_2_img_string_base64_encoded']]
                            self.sc_response_2_img_path                 	= sc_db_record[self.sc_db_entry_to_index_dict['response_2_img_path']]
                            
                            self.sc_response_3_text	                        = sc_db_record[self.sc_db_entry_to_index_dict['response_3_text']].replace('&', "&amp;")
                            self.sc_response_3_pts	                        = sc_db_record[self.sc_db_entry_to_index_dict['response_3_pts']]
                            self.sc_response_3_img_label	                = sc_db_record[self.sc_db_entry_to_index_dict['response_3_img_label']].replace('&', "&amp;")
                            self.sc_response_3_img_string_base64_encoded	= sc_db_record[self.sc_db_entry_to_index_dict['response_3_img_string_base64_encoded']]
                            self.sc_response_3_img_path                 	= sc_db_record[self.sc_db_entry_to_index_dict['response_3_img_path']]
                            
                            self.sc_response_4_text	                        = sc_db_record[self.sc_db_entry_to_index_dict['response_4_text']].replace('&', "&amp;")
                            self.sc_response_4_pts	                        = sc_db_record[self.sc_db_entry_to_index_dict['response_4_pts']]
                            self.sc_response_4_img_label	                = sc_db_record[self.sc_db_entry_to_index_dict['response_4_img_label']].replace('&', "&amp;")
                            self.sc_response_4_img_string_base64_encoded	= sc_db_record[self.sc_db_entry_to_index_dict['response_4_img_string_base64_encoded']]
                            self.sc_response_4_img_path                 	= sc_db_record[self.sc_db_entry_to_index_dict['response_4_img_path']]
                            
                            self.sc_response_5_text	                        = sc_db_record[self.sc_db_entry_to_index_dict['response_5_text']].replace('&', "&amp;")
                            self.sc_response_5_pts	                        = sc_db_record[self.sc_db_entry_to_index_dict['response_5_pts']]
                            self.sc_response_5_img_label	                = sc_db_record[self.sc_db_entry_to_index_dict['response_5_img_label']].replace('&', "&amp;")
                            self.sc_response_5_img_string_base64_encoded	= sc_db_record[self.sc_db_entry_to_index_dict['response_5_img_string_base64_encoded']]
                            self.sc_response_5_img_path                 	= sc_db_record[self.sc_db_entry_to_index_dict['response_5_img_path']]
                            
                            self.sc_response_6_text	                        = sc_db_record[self.sc_db_entry_to_index_dict['response_6_text']].replace('&', "&amp;")
                            self.sc_response_6_pts	                        = sc_db_record[self.sc_db_entry_to_index_dict['response_6_pts']]
                            self.sc_response_6_img_label	                = sc_db_record[self.sc_db_entry_to_index_dict['response_6_img_label']].replace('&', "&amp;")
                            self.sc_response_6_img_string_base64_encoded	= sc_db_record[self.sc_db_entry_to_index_dict['response_6_img_string_base64_encoded']]
                            self.sc_response_6_img_path                 	= sc_db_record[self.sc_db_entry_to_index_dict['response_6_img_path']]
                            
                            self.sc_response_7_text	                        = sc_db_record[self.sc_db_entry_to_index_dict['response_7_text']].replace('&', "&amp;")
                            self.sc_response_7_pts	                        = sc_db_record[self.sc_db_entry_to_index_dict['response_7_pts']]
                            self.sc_response_7_img_label	                = sc_db_record[self.sc_db_entry_to_index_dict['response_7_img_label']].replace('&', "&amp;")
                            self.sc_response_7_img_string_base64_encoded	= sc_db_record[self.sc_db_entry_to_index_dict['response_7_img_string_base64_encoded']]
                            self.sc_response_7_img_path                 	= sc_db_record[self.sc_db_entry_to_index_dict['response_7_img_path']]
                            
                            self.sc_response_8_text	                        = sc_db_record[self.sc_db_entry_to_index_dict['response_8_text']].replace('&', "&amp;")
                            self.sc_response_8_pts	                        = sc_db_record[self.sc_db_entry_to_index_dict['response_8_pts']]
                            self.sc_response_8_img_label	                = sc_db_record[self.sc_db_entry_to_index_dict['response_8_img_label']].replace('&', "&amp;")
                            self.sc_response_8_img_string_base64_encoded	= sc_db_record[self.sc_db_entry_to_index_dict['response_8_img_string_base64_encoded']]
                            self.sc_response_8_img_path                 	= sc_db_record[self.sc_db_entry_to_index_dict['response_8_img_path']]
                            
                            self.sc_response_9_text	                        = sc_db_record[self.sc_db_entry_to_index_dict['response_9_text']].replace('&', "&amp;")
                            self.sc_response_9_pts	                        = sc_db_record[self.sc_db_entry_to_index_dict['response_9_pts']]
                            self.sc_response_9_img_label	                = sc_db_record[self.sc_db_entry_to_index_dict['response_9_img_label']].replace('&', "&amp;")
                            self.sc_response_9_img_string_base64_encoded	= sc_db_record[self.sc_db_entry_to_index_dict['response_9_img_string_base64_encoded']]
                            self.sc_response_9_img_path                 	= sc_db_record[self.sc_db_entry_to_index_dict['response_9_img_path']]
                            
                            self.sc_response_10_text	                    = sc_db_record[self.sc_db_entry_to_index_dict['response_10_text']].replace('&', "&amp;")
                            self.sc_response_10_pts	                        = sc_db_record[self.sc_db_entry_to_index_dict['response_10_pts']]
                            self.sc_response_10_img_label	                = sc_db_record[self.sc_db_entry_to_index_dict['response_10_img_label']].replace('&', "&amp;")
                            self.sc_response_10_img_string_base64_encoded	= sc_db_record[self.sc_db_entry_to_index_dict['response_10_img_string_base64_encoded']]
                            self.sc_response_10_img_path                 	= sc_db_record[self.sc_db_entry_to_index_dict['response_10_img_path']]
                            
                            self.sc_picture_preview_pixel                   = sc_db_record[self.sc_db_entry_to_index_dict['picture_preview_pixel']]
                            
                            self.sc_description_img_name_1	                = sc_db_record[self.sc_db_entry_to_index_dict['description_img_name_1']]
                            self.sc_description_img_data_1	                = sc_db_record[self.sc_db_entry_to_index_dict['description_img_data_1']]
                            self.sc_description_img_path_1	                = sc_db_record[self.sc_db_entry_to_index_dict['description_img_path_1']]
                            self.sc_description_img_name_2	                = sc_db_record[self.sc_db_entry_to_index_dict['description_img_name_2']]
                            self.sc_description_img_data_2	                = sc_db_record[self.sc_db_entry_to_index_dict['description_img_data_2']]
                            self.sc_description_img_path_2	                = sc_db_record[self.sc_db_entry_to_index_dict['description_img_path_2']]
                            self.sc_description_img_name_3	                = sc_db_record[self.sc_db_entry_to_index_dict['description_img_name_3']]
                            self.sc_description_img_data_3	                = sc_db_record[self.sc_db_entry_to_index_dict['description_img_data_3']]
                            self.sc_description_img_path_3	                = sc_db_record[self.sc_db_entry_to_index_dict['description_img_path_3']]
                           
                            self.sc_test_time	                            = sc_db_record[self.sc_db_entry_to_index_dict['test_time']]
                            self.sc_var_number	                            = sc_db_record[self.sc_db_entry_to_index_dict['var_number']]
                            self.sc_question_pool_tag                       = sc_db_record[self.sc_db_entry_to_index_dict['question_pool_tag']]
                            self.sc_question_author                         = sc_db_record[self.sc_db_entry_to_index_dict['question_author']].replace('&', "&amp;")


            Create_SingleChoice_Questions.sc_question_structure(self, i)


    def sc_question_structure(self, id_nr):
        """Diese Funktion wandelt die SQL-Einträge in die .xml um, welche anschließend in ILIAS eingespielt werden kann"""


        # VARIABLEN
        self.sc_response_counter = 0    #wird verwendet zu zählen, wieviele Anworten pro Frage verwendet werden. Bei einer neuer Antwort -> +1

        self.sc_question_description_main = test_generator_modul_taxonomie_und_textformatierung.Textformatierung.format_description_text_in_xml(self, self.sc_var_use_latex_on_text_check.get(), self.sc_question_description_main)



        # Verbindung zur SC-Datenank
        sc_connect = sqlite3.connect(self.database_singlechoice_path)
        sc_cursor = sc_connect.cursor()

        # Alle Einträge auslesen
        sc_cursor.execute("SELECT *, oid FROM singlechoice_table")
        sc_db_records = sc_cursor.fetchall()



        for sc_db_record in sc_db_records:

            # Hier werden die Fragen anhand der ID's erstellt
            if str(sc_db_record[len(sc_db_record)-1]) == self.sc_test_entry_splitted[id_nr]:

                test_generator_modul_ilias_test_struktur.Additional_Funtions.add_dir_for_images(self, self.sc_description_img_name_1, self.sc_description_img_data_1, id_nr, self.sc_question_type_test_or_pool, self.singlechoice_test_img_file_path, self.singlechoice_pool_img_file_path)
                test_generator_modul_ilias_test_struktur.Additional_Funtions.add_dir_for_images(self, self.sc_description_img_name_2, self.sc_description_img_data_2, id_nr, self.sc_question_type_test_or_pool, self.singlechoice_test_img_file_path, self.singlechoice_pool_img_file_path)
                test_generator_modul_ilias_test_struktur.Additional_Funtions.add_dir_for_images(self, self.sc_description_img_name_3, self.sc_description_img_data_3, id_nr, self.sc_question_type_test_or_pool, self.singlechoice_test_img_file_path, self.singlechoice_pool_img_file_path)
                        

                    


                # Aufbau für  Fragenstruktur "TEST"
                if self.sc_question_type_test_or_pool == "question_test":
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
                                                                                                           self.singlechoice_pool_qpl_file_path_template,
                                                                                                           self.singlechoice_pool_qpl_file_path_output)

                # Struktur für den SingleChoice - Fragen/Antworten Teil  -- HEADER
                # Muss für jede Frage neu angelegt/hinzugefügt werden
                qticomment = ET.SubElement(item, 'qticomment')
                duration = ET.SubElement(item, 'duration')
                itemmetadata = ET.SubElement(item, 'itemmetadata')
                presentation = ET.SubElement(item, 'presentation')
                resprocessing = ET.SubElement(item, 'resprocessing')

                # Struktur für den SingleChoice - Fragen/Antworten Teil  -- MAIN
                # Muss für jede Frage neu angelegt/hinzugefügt werden
                flow = ET.SubElement(presentation, 'flow')
                question_description_material = ET.SubElement(flow, 'material')
                question_description_mattext = ET.SubElement(question_description_material, 'mattext')
                response_lid = ET.SubElement(flow, 'response_lid')
                render_choice = ET.SubElement(response_lid, 'render_choice')


                qtimetadata = ET.SubElement(itemmetadata, 'qtimetadata')
                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')

                ### ------------------------------------------------------- XML Einträge mit Werten füllen

                # Fragen-Titel -- "item title" in xml
                item.set('title', self.sc_question_title)

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
                fieldentry.text = self.sc_question_author
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
                fieldentry.text = str(self.sc_picture_preview_pixel)
                # -----------------------------------------------------------------------FEEDBACK_SETTING
                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "feedback_setting"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
                fieldentry.text = "1"
                # -----------------------------------------------------------------------SINGLELINE
                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "singleline"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
                fieldentry.text = "1"

                # Fragentitel einsetzen -- "presentation label" in xml
                presentation.set('label', self.sc_question_title)

                # Fragen-Text (Format) einsetzen -- "mattext_texttype" in xml -- Gibt das Format des Textes an
                question_description_mattext.set('texttype', "text/html")


                # Fragen-Text (Text) einsetzen   -- "mattext_texttype" in xml -- Gibt die eigentliche Fragen-Beschreibung an
                # Wenn Bild enthalten ist, dann in Fragenbeschreibung einbetten
                question_description_mattext.text = test_generator_modul_ilias_test_struktur.Additional_Funtions.add_picture_to_description_main(
                                                                self, self.sc_description_img_name_1, self.sc_description_img_data_1,
                                                                self.sc_description_img_name_2, self.sc_description_img_data_2,
                                                                self.sc_description_img_name_3, self.sc_description_img_data_3,
                                                                self.sc_question_description_main, question_description_mattext, question_description_material, id_nr)






                # "MCSR --> Singlechoice Identifier für xml datei
                response_lid.set('ident', "MCSR")
                response_lid.set('rcardinality', "Single")
                render_choice.set('shuffle', self.sc_var_mix_questions.get())



                # Antworten erstellen
                Create_SingleChoice_Questions.sc_question_answer_structure(self, self.sc_response_1_text, self.sc_response_1_pts, self.sc_response_1_img_path, self.sc_response_1_img_string_base64_encoded, render_choice, resprocessing, item, "0")
                Create_SingleChoice_Questions.sc_question_answer_structure(self, self.sc_response_2_text, self.sc_response_2_pts, self.sc_response_2_img_path, self.sc_response_2_img_string_base64_encoded, render_choice, resprocessing, item, "1")
                Create_SingleChoice_Questions.sc_question_answer_structure(self, self.sc_response_3_text, self.sc_response_3_pts, self.sc_response_3_img_path, self.sc_response_3_img_string_base64_encoded, render_choice, resprocessing, item, "2")
                Create_SingleChoice_Questions.sc_question_answer_structure(self, self.sc_response_4_text, self.sc_response_4_pts, self.sc_response_4_img_path, self.sc_response_4_img_string_base64_encoded, render_choice, resprocessing, item, "3")
                Create_SingleChoice_Questions.sc_question_answer_structure(self, self.sc_response_5_text, self.sc_response_5_pts, self.sc_response_5_img_path, self.sc_response_5_img_string_base64_encoded, render_choice, resprocessing, item, "4")
                Create_SingleChoice_Questions.sc_question_answer_structure(self, self.sc_response_6_text, self.sc_response_6_pts, self.sc_response_6_img_path, self.sc_response_6_img_string_base64_encoded, render_choice, resprocessing, item, "5")
                Create_SingleChoice_Questions.sc_question_answer_structure(self, self.sc_response_7_text, self.sc_response_7_pts, self.sc_response_7_img_path, self.sc_response_7_img_string_base64_encoded, render_choice, resprocessing, item, "6")
                Create_SingleChoice_Questions.sc_question_answer_structure(self, self.sc_response_8_text, self.sc_response_8_pts, self.sc_response_8_img_path, self.sc_response_8_img_string_base64_encoded, render_choice, resprocessing, item, "7")
                Create_SingleChoice_Questions.sc_question_answer_structure(self, self.sc_response_9_text, self.sc_response_9_pts, self.sc_response_9_img_path, self.sc_response_9_img_string_base64_encoded, render_choice, resprocessing, item, "8")
                Create_SingleChoice_Questions.sc_question_answer_structure(self, self.sc_response_10_text, self.sc_response_10_pts, self.sc_response_10_img_path, self.sc_response_10_img_string_base64_encoded, render_choice, resprocessing, item, "9")







                # Wenn es sich um einen ILIAS-Test handelt, beinhaltet die XML eine Struktur mit mehreren "Zweigen"
                # Der letzte "Zweig" --> "len(self.sc_myroot[0]) - 1" (beschreibt das letze Fach) beinhaltet die eigentlichen Fragen
                if self.sc_question_type_test_or_pool == "question_test":
                    self.sc_myroot[0][len(self.sc_myroot[0]) - 1].append(item)

                # Wenn es sich um einen ILIAS-Pool handelt, beinhaltet die XML keine Struktur
                # Die Frage kann einfach angehangen werden
                else:
                    self.sc_myroot.append(item)

                self.sc_mytree.write(self.qti_file_path_output)
                print(str(self.sc_number_of_questions_generated) + ".) SingleChoice Frage erstellt! ---> Titel: " + str(self.sc_question_title))
                self.sc_number_of_questions_generated += 1

        sc_connect.commit()
        sc_connect.close()

        if self.sc_question_type_test_or_pool == "question_pool":
            ######  Anpassung der Datei "qpl". Akualisierung des Dateinamens
            self.qpl_file = os.path.normpath(os.path.join(self.singlechoice_files_path,"sc_ilias_pool_abgabe", self.sc_ilias_id_pool_qpl_dir, self.sc_ilias_id_pool_qti_xml))

            self.mytree = ET.parse(self.qpl_file)
            self.myroot = self.mytree.getroot()

            for ident_id in self.myroot.iter('Identifier'):
                ident_id.set('Entry', "il_0_qpl_" + str(self.sc_file_max_id+1))
            self.mytree.write(self.qpl_file)
        
    ####################### QUESTION_ANSWER STRUCTURE #############################
    def sc_question_answer_structure(self, sc_response_var_text, sc_response_var_pts, sc_response_var_img_path, sc_response_var_img_string_base64_encoded, xml_render_choice, xml_resprocessing, xml_item, sc_response_counter):

        if sc_response_var_text != "":
            response_label = ET.SubElement(xml_render_choice, 'response_label')
            question_answer_material = ET.SubElement(response_label, 'material')
            question_answer_mattext = ET.SubElement(question_answer_material, 'mattext')
            response_label.set('ident', str(sc_response_counter))
            question_answer_mattext.set('texttype', "text/plain")
            question_answer_mattext.text = sc_response_var_text

            #with open(sc_response_var_img_path, "rb") as image_file:
            #    encoded64_string_raw = base64.b64encode(image_file.read())
            #    sc_response_var_img_string_base64_encoded2 = encoded64_string_raw.decode('utf-8')

            #    print("============")

            #    print(sc_response_var_img_path)
            #    print("============")
            if sc_response_var_img_string_base64_encoded != "":
                question_answer_matimage = ET.SubElement(question_answer_material, 'matimage')

                if str(sc_response_var_img_path.rpartition('.')[-1]) == "jpg" or str(sc_response_var_img_path.rpartition('.')[-1]) == "jpeg":
                    question_answer_matimage.set('imagtype', "image/jpeg")
                elif str(sc_response_var_img_path.rpartition('.')[-1]) == "png":
                    question_answer_matimage.set('imagtype', "image/png")
                elif str(sc_response_var_img_path.rpartition('.')[-1]) == "gif":
                    question_answer_matimage.set('imagtype', "image/gif")
                else:
                    print("Bildformat ist nicht jpg/jpeg/png/gif und wird von ILIAS nicht unterstützt!")

                question_answer_matimage.set('label', sc_response_var_img_path.rpartition('/')[-1])
                question_answer_matimage.set('embedded', "base64")
                question_answer_matimage.text = str(sc_response_var_img_string_base64_encoded)

            # --------------------------------------------------------PUNKTE FÜR ANTWORT

            respcondition = ET.SubElement(xml_resprocessing, 'respcondition')
            respcondition.set('continue', "Yes")

            conditionvar = ET.SubElement(respcondition, 'conditionvar')
            varequal = ET.SubElement(conditionvar, 'varequal')
            varequal.set('respident', "MCSR")  # MCSR --> SingleChoice Ident
            varequal.text = str(sc_response_counter)  # ID der Antwort inkrementiert für jede Antwort

            setvar = ET.SubElement(respcondition, 'setvar')
            setvar.set('action', "Add")
            setvar.text = str(sc_response_var_pts)  # Punktevergabe für die Antwort
            displayfeedback = ET.SubElement(respcondition, 'displayfeedback')
            displayfeedback.set('feedbacktype', "Response")
            displayfeedback.set('linkrefid', "response_" + str(sc_response_counter))
            # --------------------------------------------------------ZUSATZ FÜR ANTWORT

            itemfeedback = ET.SubElement(xml_item, 'itemfeedback')
            itemfeedback_flow_mat = ET.SubElement(itemfeedback, 'flow_mat')
            itemfeedback_material = ET.SubElement(itemfeedback_flow_mat, 'material')
            itemfeedback_mattext = ET.SubElement(itemfeedback_material, 'mattext')

            itemfeedback.set('ident', "response_" + str(sc_response_counter))
            itemfeedback.set('view', "All")
            itemfeedback_mattext.set('texttype', "text/plain")

    ###############################################################################

class Create_SingleChoice_Test(SingleChoice):
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

        self.sc_db_entry_to_index_dict = entry_to_index_dict

        test_generator_modul_ilias_test_struktur.Create_ILIAS_Test.__init__(self,
                                                                            self.sc_db_entry_to_index_dict,
                                                                            self.singlechoice_test_tst_file_path_template,
                                                                            self.singlechoice_test_tst_file_path_output,
                                                                            self.singlechoice_test_qti_file_path_template,
                                                                            self.singlechoice_test_qti_file_path_output,
                                                                            self.sc_ilias_test_title_entry.get(),
                                                                            self.create_singlechoice_test_entry.get(),
                                                                            self.sc_question_type_entry.get(),
                                                                            )




class Create_SingleChoice_Pool(SingleChoice):
    def __init__(self, entry_to_index_dict, var_create_all_questions):

        self.entry_to_index_dict = entry_to_index_dict
        self.sc_var_create_question_pool_all = var_create_all_questions

        # Die __init__ wird bei einem Knopfdruck auf "ILIAS-Fragenpool erstellen" ausgeführt
        # Es werden XML-Dateien und Ordner mit einer aufsteigenden ID erstellt.
        test_generator_modul_ilias_test_struktur.Create_ILIAS_Pool.__init__(self,
                                                                            self.project_root_path,
                                                                            self.singlechoice_pool_directory_output,
                                                                            self.singlechoice_files_path_pool_output,
                                                                            self.singlechoice_pool_qti_file_path_template,
                                                                            self.sc_ilias_test_title_entry.get(),
                                                                            self.create_singlechoice_pool_entry.get(),
                                                                            self.sc_question_type_name,
                                                                            self.database_singlechoice_path,
                                                                            self.sc_database_table,
                                                                            self.sc_db_entry_to_index_dict,
                                                                            self.sc_var_create_question_pool_all
                                                                            )






