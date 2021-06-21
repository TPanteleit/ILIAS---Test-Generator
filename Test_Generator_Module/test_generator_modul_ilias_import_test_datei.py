from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
from tkinter import ttk
import sqlite3                              #verwendet für mySQL Datenbank
import xml.etree.ElementTree as ET
import os
import pathlib
import base64
from PyQt5.QtWidgets import QMainWindow, QApplication, QLineEdit, QMessageBox, QFileDialog, QTimeEdit, QTableWidgetItem
from PyQt5 import QtCore, QtGui, QtWidgets
import shutil
from distutils.dir_util import copy_tree

class Import_ILIAS_Datei_in_DB:
    def __init__(self, project_root_path):
        # self.project_root_path = os.path.normpath(r"C:\Users\Genesis\Desktop\ilias Generator - Projekt\Silvan\1623652533__0__tst_2341643")

        self.ilias_test_qti_file = "1602067473__0__qti_30598_wilde_mischung.xml"

        # Todo pyqt5 - tkinter filedialog
        self.import_ilias_test_or_pool_file = filedialog.askdirectory(initialdir=pathlib.Path().absolute(), title="Select a File")

        
        # Pfade für Datenbanken
        self.project_root_path = project_root_path
        self.database_formelfrage_path = os.path.normpath(os.path.join(self.project_root_path, "Test_Generator_Datenbanken", "ilias_formelfrage_db.db"))
        self.database_singlechoice_path = os.path.normpath(os.path.join(self.project_root_path,"Test_Generator_Datenbanken", "ilias_singlechoice_db.db"))
        self.database_multiplechoice_path = os.path.normpath(os.path.join(self.project_root_path,"Test_Generator_Datenbanken", "ilias_multiplechoice_db.db"))
        self.database_zuordnungsfrage_path = os.path.normpath(os.path.join(self.project_root_path,"Test_Generator_Datenbanken", "ilias_zuordnungsfrage_db.db"))



        # Ordner-Name splitten um automatisiert die enthaltene qti.xml Datei einlesen zu können
        self.import_ilias_test_or_pool_file_folder_name = self.import_ilias_test_or_pool_file.rsplit('/', 1)[-1]
        self.import_ilias_test_or_pool_file_folder_name_split1 = self.import_ilias_test_or_pool_file_folder_name[:15]
        self.import_ilias_test_or_pool_file_folder_name_split2 = self.import_ilias_test_or_pool_file_folder_name.rsplit('_', 1)[-1]
        self.import_ilias_test_or_pool_file_qti_file = os.path.normpath(os.path.join(self.import_ilias_test_or_pool_file,
                                                                                     self.import_ilias_test_or_pool_file_folder_name_split1 + "qti_" + self.import_ilias_test_or_pool_file_folder_name_split2 + ".xml"))



        #XML Datei einlesen -> Root Verzeichnis bestimmen
        self.mytree = ET.parse(self.import_ilias_test_or_pool_file_qti_file)
        self.myroot = self.mytree.getroot()

        ff_nr = 0
        sc_nr = 0
        mc_nr = 0
        mq_nr = 0
        number_of_type_questions = self.mytree.findall(".//fieldentry")

        self.max_number_of_responses = 10
        self.mc_max_number_of_responses = 10
        self.mq_max_number_of_responses = 10
        self.ff_max_number_of_variables = 15
        self.ff_max_number_of_results = 10


        for i in range(len(number_of_type_questions)):
            if number_of_type_questions[i].text == "assFormulaQuestion":
                ff_nr += 1
            elif number_of_type_questions[i].text == "SINGLE CHOICE QUESTION":
                sc_nr += 1
            elif number_of_type_questions[i].text == "MULTIPLE CHOICE QUESTION":
                mc_nr += 1
            elif number_of_type_questions[i].text == "MATCHING QUESTION":
                mq_nr += 1

        print("FF-Anzahl: ", ff_nr)
        print("SC-Anzahl: ", sc_nr)
        print("MC-Anzahl: ", mc_nr)
        print("MQ-Anzahl: ", mq_nr)

        items = self.mytree.findall(".//item")

        # Hier werden alle Fragen aus der QTI behandelt
        for t in range(len(items)):

            # Alle Fragen-Attribute auslesen
            # Hier kann der Typ der Frage über ein DICT ausgelesen werden
            qtimetadatafield_list = items[t].findall(".//qtimetadatafield")

            # INIT
            self.field_label_list = []
            self.field_entry_list = []
            self.question_attributes_dict = []






            # XML fieldlabel und fieldentry auslesen
            # hier stehen die Grundinformation der Frage drin z.B.
            #   <fieldlabel>QUESTIONTYPE</fieldlabel>
            #   <fieldentry>SINGLE CHOICE QUESTION</fieldentry>
            for i in range(len(qtimetadatafield_list)):
                 self.field_label_list.append(qtimetadatafield_list[i].find('fieldlabel').text)
                 self.field_entry_list.append(qtimetadatafield_list[i].find('fieldentry').text)

            # Erstellung DICT
            self.question_attributes_dict = dict(zip(self.field_label_list, self.field_entry_list))





            # Fragen-Titel
            self.question_title = items[t].attrib.get('title')

             # Fragen-Titel Beschreibung
            self.question_description_title = items[t].find('qticomment').text
            if self.question_description_title is None:
                self.question_description_title = ""

            # Zeit für die Bearbeitung der Frage
            self.question_duration = items[t].find('duration').text
            if self.question_duration is None:
                self.question_duration = ""

            # Autor
            if self.question_attributes_dict.get("AUTHOR") is not None:
                self.question_author = self.question_attributes_dict["AUTHOR"]
            else:
                self.question_author = ""


            # Punkte
            if self.question_attributes_dict.get("points") is not None:
                self.points = self.question_attributes_dict["points"]
            else:
                self.points = ""


            # Vorschaubild (in Pixel)
            if self.question_attributes_dict.get("thumb_size") is not None:
                self.picture_preview_pixel = self.question_attributes_dict["thumb_size"]
            else:
                self.picture_preview_pixel = ""



            # Antworten einzeilig/mehrzeilig
            if self.question_attributes_dict.get("singleline") is not None:
                self.singleline = self.question_attributes_dict["singleline"]
            else:
                self.singleline = ""



            # shuffle
            if self.question_attributes_dict.get("shuffle") is not None:
                self.shuffle = self.question_attributes_dict["shuffle"]
            else:
                self.shuffle = ""


            # thumb_geometry
            if self.question_attributes_dict.get("thumb_geometry") is not None:
                self.thumb_geometry = self.question_attributes_dict["thumb_geometry"]
            else:
                self.thumb_geometry = ""


            # matching_mode
            if self.question_attributes_dict.get("matching_mode") is not None:
                self.matching_mode = self.question_attributes_dict["matching_mode"]
            else:
                self.matching_mode = ""




            # QTI Text-Tag "FLOW" auslesen
            # behinhaltet im XML Format den Fragen-Text und die Fragen-Antworten
            flow_material_mattext_list = items[t].findall(".//flow")

            if self.question_attributes_dict["QUESTIONTYPE"] == "assFormulaQuestion":

                # INIT
                self.ff_question_description_main = ""
                self.ff_question_description_img_list = []
                self.ff_question_description_img_label_list = []
                self.ff_question_description_img_uri_list = []

                self.ff_number_of_variables_list = []
                self.ff_number_of_results_list = []


                # Fragen-Text Text & Bild
                self.ff_question_description_main, self.ff_question_description_img_list, self.ff_question_description_img_label_list, self.ff_question_description_img_uri_list = Import_ILIAS_Datei_in_DB.read_description_main_text_and_img_from_qti(self, flow_material_mattext_list)



                # Im "self.question_attributes_dict" wurde alle "fieldlabel" und "fielentry" Einträge ausgelesen
                # Bei dem Fragentyp "Formelfrage" beinhaltet es neben den "allgemeinen" Daten (wie Fragentyp oder Autor) auch die Variablen und Ergebnisse
                # Das Ziel ist aus dem Dict eine Liste zu erstellen und nach den Einträgen für Variablen und Ergebnissen zu suchen
                # Variable sind in der Form "$v1" und Ergebniss "$r1"
                self.list_of_dict_keys_list = list(self.question_attributes_dict.keys())

                # Immer wenn eine Variable gefunden wird, in eine Liste anhängen
                # Anschließend kann über "max()" die Anzahl der Variablen/Ergebnisse in der Aufgabe ermittelt werden
                for i in range(len(self.list_of_dict_keys_list)):
                    if "$v" in self.list_of_dict_keys_list[i]:
                        self.ff_number_of_variables_list.append(self.list_of_dict_keys_list[i])

                    elif "$r" in self.list_of_dict_keys_list[i]:
                        self.ff_number_of_results_list.append(self.list_of_dict_keys_list[i])





                ########### VARAIBLES
                self.variables_settings_list = []
                self.ff_variables_settings_list = []

                for i in range(len(self.ff_number_of_variables_list)):
                    self.variables_settings_list.append(self.question_attributes_dict[self.ff_number_of_variables_list[i]])



                for i in range(len(self.variables_settings_list)):
                    new_list_temp = []
                    test_list_temp = self.variables_settings_list[i].split(";")
                    test_list_temp = test_list_temp[1::2]



                    for j in range(len(test_list_temp)):
                        test_list_2_index = test_list_temp[j].rfind(':')
                        test_list_2 = test_list_temp[j][test_list_2_index+1:]

                        new_list_temp.append(test_list_2)
                    self.ff_variables_settings_list.append(new_list_temp)



                for i in range(len(self.ff_variables_settings_list)):
                    for j in range(len(self.ff_variables_settings_list[i])):
                        self.ff_variables_settings_list[i][j] = self.ff_variables_settings_list[i][j].replace('"','')


                ############ RESULTS
                self.results_settings_list = []
                self.ff_results_settings_list = []



                for i in range(len(self.ff_number_of_results_list)):
                    self.results_settings_list.append(self.question_attributes_dict[self.ff_number_of_results_list[i]])



                # todo [1::2] ist für results anders!
                for i in range(len(self.results_settings_list)):
                    new_list_temp = []
                    test_list_temp = self.results_settings_list[i].split(";")


                    test_list_temp = test_list_temp[1::2]



                    for j in range(len(test_list_temp)):
                        test_list_2_index = test_list_temp[j].rfind(':')
                        test_list_2 = test_list_temp[j][test_list_2_index + 1:]

                        new_list_temp.append(test_list_2)
                    self.ff_results_settings_list.append(new_list_temp)



                for i in range(len(self.ff_results_settings_list)):
                    for j in range(len(self.ff_results_settings_list[i])):
                        self.ff_results_settings_list[i][j] = self.ff_results_settings_list[i][j].replace('"','')



                self.ff_question_attributes_list = [self.question_duration, self.question_title,
                                                    self.question_description_title, self.question_description_main,
                                                    self.thumb_geometry, self.shuffle, self.matching_mode,
                                                    self.question_author]

                # In Datenbdank einlesen
                Import_ILIAS_Datei_in_DB.insert_into_ff_db(self, self.ff_question_attributes_list, self.ff_question_description_img_uri_list, self.ff_variables_settings_list, self.ff_results_settings_list, self.ff_max_number_of_variables, self.ff_max_number_of_results)

                # Bilder aus Fragen-Text kopieren
                Import_ILIAS_Datei_in_DB.copy_description_main_img_to_dir(self)


            # SINGLECHOICE FRAGEN
            elif self.question_attributes_dict["QUESTIONTYPE"] == "SINGLE CHOICE QUESTION":

                self.sc_question_description_main = ""
                self.sc_question_description_img_list = []
                self.sc_question_description_img_label_list = []
                self.sc_question_description_img_uri_list = []

                self.sc_response_text_list = []
                self.sc_response_img_label_list = []
                self.sc_response_img_base64_data_list = []
                self.sc_response_pts_list = []





                # Fragen-Text Text & Bild
                self.sc_question_description_main, self.sc_question_description_img_list, self.sc_question_description_img_label_list, self.sc_question_description_img_uri_list = Import_ILIAS_Datei_in_DB.read_description_main_text_and_img_from_qti(self, flow_material_mattext_list)

                # Fragen-Antworten Text & Bild
                for i in range(len(flow_material_mattext_list)):
                    for material in flow_material_mattext_list[i]:
                        if material.tag == "response_lid":
                            for renderChoice in material:

                                # Antworten Darstellung mischen
                                self.sc_mix_answers = renderChoice.attrib.get('shuffle')
                                if self.sc_mix_answers == "Yes":
                                    self.sc_mix_answers = "1"
                                else:
                                    self.sc_mix_answers = "0"

                                for responseLabel in renderChoice:
                                    for material in responseLabel:

                                        # Prüfen ob Antwort-Text vorhanden ist
                                        if material.find("mattext") != None:
                                            self.sc_response_text_list.append(material.find("mattext").text)
                                        else:
                                            self.sc_response_text_list.append("NONE")

                                        # Prüfen ob Antwort-Bild vorhanden ist
                                        if material.find("matimage") != None:
                                            self.sc_response_img_label_list.append(material.find("matimage").attrib.get('label'))
                                            self.sc_response_img_base64_data_list.append(material.find("matimage").text)
                                        else:
                                            self.sc_response_img_label_list.append("NONE")
                                            self.sc_response_img_base64_data_list.append("NONE")




                # Fragen-Punkte auslesen
                setvar_list = items[t].findall(".//setvar")
                for i in range(len(setvar_list)):
                    self.sc_response_pts_list.append(setvar_list[i].text)



                self.question_attributes_list = [ self.question_duration, self.question_title, self.question_description_title, self.question_description_main,
                                                  self.picture_preview_pixel, self.question_author]

                # In Datenbdank einlesen
                Import_ILIAS_Datei_in_DB.insert_into_sc_db(self, self.question_attributes_list, self.sc_question_description_img_uri_list, self.sc_response_text_list, self.sc_response_img_label_list, self.sc_response_img_base64_data_list, self.sc_response_pts_list, self.max_number_of_responses)

                # Bilder aus Fragen-Text kopieren
                Import_ILIAS_Datei_in_DB.copy_description_main_img_to_dir(self)

                # Antwort Bilder (base64 encoded) in "Bilder" Ordner kopieren
                Import_ILIAS_Datei_in_DB.copy_response_text_img_to_dir(self, "SC", self.import_ilias_test_or_pool_file_folder_name, self.sc_response_img_label_list, self.sc_response_img_base64_data_list)

            elif self.question_attributes_dict["QUESTIONTYPE"] == "MULTIPLE CHOICE QUESTION":


                # INIT
                self.mc_question_description_main = ""
                self.mc_question_description_img_list = []
                self.mc_question_description_img_label_list = []
                self.mc_question_description_img_uri_list = []

                self.mc_response_text_list = []
                self.mc_response_img_label_list = []
                self.mc_response_img_base64_data_list = []
                self.mc_response_pts_list = []

                # Fragen-Text Text & Bild
                self.mc_question_description_main, self.mc_question_description_img_list, self.mc_question_description_img_label_list, self.mc_question_description_img_uri_list = Import_ILIAS_Datei_in_DB.read_description_main_text_and_img_from_qti(self, flow_material_mattext_list)

                # Fragen-Antworten Text & Bild
                for i in range(len(flow_material_mattext_list)):
                    for material in flow_material_mattext_list[i]:
                        if material.tag == "response_lid":
                            for renderChoice in material:
                                # Gemischte Antworten
                                self.mc_mix_answers = renderChoice.attrib.get('shuffle')
                                if self.mc_mix_answers == "Yes":
                                    self.mc_mix_answers = "1"
                                else:
                                    self.mc_mix_answers = "0"

                                for responseLabel in renderChoice:
                                    for material in responseLabel:

                                        # Prüfen ob Antwort-Text vorhanden ist
                                        if material.find("mattext") != None:
                                            self.mc_response_text_list.append(material.find("mattext").text)
                                        else:
                                            self.mc_response_text_list.append("NONE")

                                        # Prüfen ob Antwort-Bild vorhanden ist
                                        if material.find("matimage") != None:
                                            self.mc_response_img_label_list.append(material.find("matimage").attrib.get('label'))
                                            self.mc_response_img_base64_data_list.append(material.find("matimage").text)
                                        else:
                                            self.mc_response_img_label_list.append("NONE")
                                            self.mc_response_img_base64_data_list.append("NONE")


                # Fragen-Punkte auslesen
                setvar_list = items[t].findall(".//setvar")
                for i in range(len(setvar_list)):
                    self.mc_response_pts_list.append(setvar_list[i].text)

                self.mc_response_correct_pts_list = []
                self.mc_response_false_pts_list = []

                # Jedes "gerade" Element in der "response_pts_list" beinhaltet die Punkte für eine "ausgewählt" Antwort
                self.mc_response_correct_pts_list = self.mc_response_pts_list[::2]

                # Jedes "ungerade" Element in der "response_pts_list" beinhaltet die Punkte für eine "nicht ausgewählt" Antwort
                # [1::2] = Start bei Listen-Eintrag "1" und dann jedes zweite Element
                self.mc_response_false_pts_list = self.mc_response_pts_list[1::2]


                self.mc_question_attributes_list = [self.question_duration, self.question_title, self.question_description_title, self.question_description_main,
                                                    self.picture_preview_pixel, self.question_author]





                # In Datenbdank einlesen
                Import_ILIAS_Datei_in_DB.insert_into_mc_db(self, self.mc_question_attributes_list, self.mc_question_description_img_uri_list, self.mc_response_text_list, self.mc_response_img_label_list, self.mc_response_img_base64_data_list, self.mc_response_correct_pts_list, self.mc_response_false_pts_list, self.mc_max_number_of_responses)

                # Bilder aus Fragen-Text kopieren
                Import_ILIAS_Datei_in_DB.copy_description_main_img_to_dir(self)


                # Antwort Bilder (base64 encoded) in "Bilder" Ordner kopieren
                Import_ILIAS_Datei_in_DB.copy_response_text_img_to_dir(self, "MC", self.import_ilias_test_or_pool_file_folder_name, self.mc_response_img_label_list, self.mc_response_img_base64_data_list)

            elif self.question_attributes_dict["QUESTIONTYPE"] == "MATCHING QUESTION":

                self.mq_question_description_main = ""
                self.mq_question_description_img_list = []
                self.mq_question_description_img_label_list = []
                self.mq_question_description_img_uri_list = []

                self.response_label_ident_list = []
                self.response_matimage_label_list = []

                self.mq_definition_response_text_list = []
                self.mq_definition_response_img_label_list = []
                self.mq_definition_response_img_base64_data_list = []

                self.mq_term_response_text_list = []
                self.mq_term_response_img_label_list = []
                self.mq_term_response_img_base64_data_list = []

                self.mq_assignment_pairs_list = []
                self.mq_assignment_pairs_definition_list = []
                self.mq_assignment_pairs_term_list = []
                self.mq_assignment_pairs_pts_list = []





                # Fragen-Text Text & Bild
                self.mq_question_description_main, self.mq_question_description_img_list, self.mq_question_description_img_label_list, self.mq_question_description_img_uri_list = Import_ILIAS_Datei_in_DB.read_description_main_text_and_img_from_qti(self, flow_material_mattext_list)

                # Fragen-Antworten Text & Bild
                for i in range(len(flow_material_mattext_list)):
                    for material in flow_material_mattext_list[i]:
                        if material.tag == "response_grp":
                            for renderChoice in material:

                                # Antworten Darstellung mischen
                                self.mq_mix_answers = renderChoice.attrib.get('shuffle')
                                if self.mq_mix_answers == "Yes":
                                    self.mq_mix_answers = "1"
                                else:
                                    self.mq_mix_answers = "0"

                                for responseLabel in renderChoice:



                                    # Wenn das Attribut "match_group" in der XML nicht vorhanden ist, handelt es sich auf einen "Definition" Eintrag
                                    if responseLabel.attrib.get('match_group') is not None:

                                        for material in responseLabel:

                                            # Prüfen ob Antwort-Text vorhanden ist
                                            if material.find("mattext") != None:
                                                self.mq_definition_response_text_list.append(material.find("mattext").text)
                                            else:
                                                self.mq_definition_response_text_list.append("NONE")

                                            # Prüfen ob Antwort-Bild vorhanden ist
                                            if material.find("matimage") != None:
                                                self.mq_definition_response_img_label_list.append(material.find("matimage").attrib.get('label'))
                                                self.mq_definition_response_img_base64_data_list.append(material.find("matimage").text)
                                            else:
                                                self.mq_definition_response_img_label_list.append("NONE")
                                                self.mq_definition_response_img_base64_data_list.append("NONE")

                                    # Sonst handelt es sich um einen "Term" Eintrag
                                    else:
                                        for material in responseLabel:
                                            # Prüfen ob Antwort-Text vorhanden ist
                                            if material.find("mattext") != None:
                                                self.mq_term_response_text_list.append(material.find("mattext").text)
                                            else:
                                                self.mq_term_response_text_list.append("NONE")

                                            # Prüfen ob Antwort-Bild vorhanden ist
                                            if material.find("matimage") != None:
                                                self.mq_term_response_img_label_list.append(material.find("matimage").attrib.get('label'))
                                                self.mq_term_response_img_base64_data_list.append(material.find("matimage").text)
                                            else:
                                                self.mq_term_response_img_label_list.append("NONE")
                                                self.mq_term_response_img_base64_data_list.append("NONE")



                response_label_list = items[t].findall(".//response_label")
                for i in range(len(response_label_list)):
                    self.response_label_ident_list.append(response_label_list[i].attrib.get('ident'))
                    for child in response_label_list[i]:
                        for matimage in child:
                            if matimage.tag == "matimage":
                                self.response_matimage_label_list.append(matimage.attrib.get('label'))






                self.response_ident_to_img_label_dict = dict(zip(self.response_label_ident_list, self.response_matimage_label_list))



                # Fragen-Punkte auslesen
                setvar_list = items[t].findall(".//setvar")
                for i in range(len(setvar_list)):
                    self.mq_assignment_pairs_pts_list.append(setvar_list[i].text)

                # Assignment Pairs auslesen

                var_subset_list = items[t].findall(".//varsubset")
                for i in range(len(var_subset_list)):
                    self.mq_assignment_pairs_list.append(var_subset_list[i].text)





                for i in range(len(self.mq_assignment_pairs_list)):
                    temp_list = self.mq_assignment_pairs_list[i].split(',')

                    self.mq_assignment_pairs_term_list.append(temp_list[0])
                    self.mq_assignment_pairs_definition_list.append(temp_list[1])



                self.mq_question_attributes_list = [self.question_duration, self.question_title, self.question_description_title, self.question_description_main,
                                                    self.thumb_geometry, self.shuffle, self.matching_mode,self.question_author]





                # In Datenbdank einlesen
                Import_ILIAS_Datei_in_DB.insert_into_mq_db(self, self.mq_question_attributes_list, self.mq_question_description_img_uri_list,
                                       self.mq_definition_response_text_list, self.mq_definition_response_img_label_list, self.mq_definition_response_img_base64_data_list,
                                       self.mq_term_response_text_list, self.mq_term_response_img_label_list, self.mq_term_response_img_base64_data_list,
                                       self.mq_assignment_pairs_definition_list, self.mq_assignment_pairs_term_list, self.mq_assignment_pairs_pts_list,
                                       self.mq_max_number_of_responses)

                # Bilder aus Fragen-Text kopieren
                Import_ILIAS_Datei_in_DB.copy_description_main_img_to_dir(self)


                # Antwort Bilder (base64 encoded) in "Bilder" Ordner kopieren
                Import_ILIAS_Datei_in_DB.copy_response_text_img_to_dir(self, "MQ", self.import_ilias_test_or_pool_file_folder_name, self.mq_definition_response_img_label_list, self.mq_definition_response_img_base64_data_list)
                Import_ILIAS_Datei_in_DB.copy_response_text_img_to_dir(self, "MQ", self.import_ilias_test_or_pool_file_folder_name, self.mq_term_response_img_label_list, self.mq_term_response_img_base64_data_list)



        print("Import abgeschlossen -->", self.import_ilias_test_or_pool_file_folder_name)


    def read_description_main_text_and_img_from_qti(self, flow_material_mattext_list):

        self.question_description_img_list = []
        self.question_description_img_label_list = []
        self.question_description_img_uri_list = []

        self.question_description_main = ""



        # Fragen-Text
        for i in range(len(flow_material_mattext_list)):
            for material in flow_material_mattext_list[i]:
                if material.tag == "material":
                    if material.find("mattext") != None:
                        self.question_description_main = material.find("mattext").text

                    self.question_description_img_list = material.findall(".//matimage")

                    for j in range(len(self.question_description_img_list)):
                        self.question_description_img_label_list.append(self.question_description_img_list[j].attrib.get('label'))
                        self.question_description_img_uri_list.append(os.path.basename(self.question_description_img_list[j].attrib.get('uri')))

        self.question_description_main_temp = self.question_description_main.split('</p>')

        self.img_in_description_main_index_list = []
        for i in range(len(self.question_description_main_temp)):
            if "img" in self.question_description_main_temp[i]:
                self.img_in_description_main_index_list.append(i)

        self.sorted_img_in_description_main_index_list = sorted(self.img_in_description_main_index_list, reverse=True)

        for i in range(len(self.sorted_img_in_description_main_index_list)):
            self.question_description_main_temp.pop(self.sorted_img_in_description_main_index_list[i])




        self.question_description_main_temp_new = []

        self.question_description_main_temp_new.append('</p>'.join(self.question_description_main_temp))

        self.question_description_main_temp_new = self.question_description_main_temp_new[0].replace('<span class="latex">', '')
        self.question_description_main_temp_new = self.question_description_main_temp_new.replace('</span>', '')
        self.question_description_main_temp_new = self.question_description_main_temp_new.replace('&gt;', '>')
        self.question_description_main_temp_new = self.question_description_main_temp_new.replace('&lt;', '<')
        self.question_description_main_temp_new = self.question_description_main_temp_new.replace('<p>', '')
        self.question_description_main_temp_new = self.question_description_main_temp_new.replace('</p>', '')
        self.question_description_main_temp_new = self.question_description_main_temp_new.replace('<li>', '')
        self.question_description_main_temp_new = self.question_description_main_temp_new.replace('/li>', '')
        self.question_description_main_temp_new = self.question_description_main_temp_new.replace('<em>', '')
        self.question_description_main_temp_new = self.question_description_main_temp_new.replace('</em>', '')
        self.question_description_main_temp_new = self.question_description_main_temp_new.replace('<ol>', '')
        self.question_description_main_temp_new = self.question_description_main_temp_new.replace('</ol>', '')


        return self.question_description_main, self.question_description_img_list, self.question_description_img_label_list, self.question_description_img_uri_list

    def copy_description_main_img_to_dir(self):
        # Bilder für Fragen-Text in "Bilder" Ordner kopieren

        self.copy_from_dir = os.path.join(self.import_ilias_test_or_pool_file, "objects")
        self.copy_to_question_description_img_dir   = os.path.join(pathlib.Path().absolute(), "Bilder", "Bilder_von_Import_" + self.import_ilias_test_or_pool_file_folder_name, "Fragen_Text_Bilder")

        copy_tree(self.copy_from_dir, self.copy_to_question_description_img_dir)

    def copy_response_text_img_to_dir(self, question_type, import_ilias_test_or_pool_file_folder_name, response_img_label_list, response_img_base64_data_list):

        self.question_type_dir = question_type
        self.import_ilias_test_or_pool_file_folder_name = import_ilias_test_or_pool_file_folder_name
        self.response_img_label_list = response_img_label_list.copy()
        self.response_img_base64_data_list = response_img_base64_data_list.copy()


        self.copy_to_question_response_img_dir_path = os.path.join(pathlib.Path().absolute(), "Bilder", "Bilder_von_Import_" + self.import_ilias_test_or_pool_file_folder_name, "Fragen_Antworten_Bilder", self.question_type_dir)
        print(self.copy_to_question_response_img_dir_path)
        # Create directory
        try:
            # Create target Directory
            os.makedirs(self.copy_to_question_response_img_dir_path)
        except FileExistsError:
            pass


        # Bilder für Fragen-Antworten aus String(base64 erstellen)
        # self.sc_response_img_base64_data_list

        for i in range(len(self.response_img_base64_data_list)):
            if self.response_img_label_list[i] != "NONE":
                imgdata = base64.b64decode(self.response_img_base64_data_list[i])
                filename = self.response_img_label_list[i]

                with open(os.path.join(self.copy_to_question_response_img_dir_path, filename), 'wb') as img:
                    img.write(imgdata)



    def insert_into_ff_db(self, question_attributes_list, description_img_path_list, variables_settings_list, results_settings_list, max_number_of_variables, max_number_of_results ):
        self.ff_responses_string_temp = ""

        self.ff_question_attributes_to_db_list = question_attributes_list.copy()
        self.ff_description_img_path_to_db_list = description_img_path_list.copy()
        self.ff_max_number_of_variables = max_number_of_variables
        self.ff_max_number_of_results = max_number_of_results

        self.ff_variables_settings_to_db_list = variables_settings_list.copy()
        self.ff_results_settings_to_db_list = results_settings_list.copy()

        self.ff_description_img_path_to_db_list = description_img_path_list.copy()


        # Listen ohne Einträge mit "" auffüllen, damit keine "NULL" Einträge in der DB exestieren
        for i in range(3 - len(self.ff_description_img_path_to_db_list)):
            self.ff_description_img_path_to_db_list.append("")



        # variablen settings auffüllen
        for i in range(self.ff_max_number_of_variables - len(self.ff_variables_settings_list)):
            var_temp_list = ["", "", "", "", "", ""]
            self.ff_variables_settings_to_db_list.append(var_temp_list)

       # Ergebnisse settings auffüllen
        for i in range(self.ff_max_number_of_results - len(self.ff_results_settings_list)):
            res_temp_list = ["", "", "", "", "", "", "", "", "", ""]
            self.ff_results_settings_to_db_list.append(res_temp_list)


        # todo 2x question_type? in mc mq sc?

        self.ff_question_attributes_beginning_1 = "question_type, question_title, question_description_title, question_description_main, "
        self.ff_question_attributes_beginning_2 = ":question_type, :question_title, :question_description_title, :question_description_main, "

        self.ff_question_attributes_ending_1 = "description_img_path_1, description_img_path_2, description_img_path_3, test_time, question_author, question_difficulty, question_category, question_pool_tag "
        self.ff_question_attributes_ending_2 = ":description_img_path_1, :description_img_path_2, :description_img_path_3, :test_time, :question_author, :question_difficulty, :question_category, :question_pool_tag "

        # Verbindung mit der Datenbank herstellen
        conn = sqlite3.connect(self.database_formelfrage_path)
        cursor = conn.cursor()


        cursor.execute("INSERT INTO formelfrage_table "
                       "(" + self.ff_question_attributes_beginning_1 + self.ff_question_attributes_ending_1 + ")"
                       "VALUES"
                       "(" + self.ff_question_attributes_beginning_2 + self.ff_question_attributes_ending_2 + ")",
                       {"question_title":                   self.ff_question_attributes_to_db_list[1],
                        "question_description_title":       self.ff_question_attributes_to_db_list[2],
                        "question_description_main":        self.ff_question_attributes_to_db_list[3],
                        "description_img_path_1":  self.ff_description_img_path_to_db_list[0],
                        "description_img_path_2":  self.ff_description_img_path_to_db_list[1],
                        "description_img_path_3":  self.ff_description_img_path_to_db_list[2],
                        "test_time":                        self.ff_question_attributes_to_db_list[0],
                        "question_author":                  self.ff_question_attributes_to_db_list[7],
                        "question_difficulty":          "",
                        "question_type":                "formelfrage",
                        "question_category":            "",
                        "question_pool_tag":            ""          #todo need taxonomy?
                        })
        self.ff_max_oid = Import_ILIAS_Datei_in_DB.find_max_oid_in_table(self, conn, "formelfrage_table")

        for i in range(self.ff_max_number_of_variables):

            self.ff_variables_string_temp = "var" + str(i+1) + "_name = :var" + str(i+1) + "_name, " \
                                            "var" + str(i+1) + "_min = :var" + str(i+1) + "_min, " \
                                            "var" + str(i+1) + "_max = :var" + str(i+1) + "_max, " \
                                            "var" + str(i+1) + "_prec = :var" + str(i+1) + "_prec, " \
                                            "var" + str(i+1) + "_divby = :var" + str(i+1) + "_divby, " \
                                            "var" + str(i+1) + "_unit = :var" + str(i+1) + "_unit "



            cursor.execute(" UPDATE formelfrage_table SET " + self.ff_variables_string_temp + " WHERE oid = :oid",
                                    {"var" + str(i+1) + '_name': "",
                                     'var' + str(i+1) + '_min': self.ff_variables_settings_to_db_list[i][2],
                                     'var' + str(i+1) + '_max': self.ff_variables_settings_to_db_list[i][3],
                                     'var' + str(i+1) + '_prec': self.ff_variables_settings_to_db_list[i][0],
                                     'var' + str(i+1) + '_divby': self.ff_variables_settings_to_db_list[i][1],
                                     'var' + str(i+1) + '_unit': "",
                                     'oid': self.ff_max_oid
                                     })


        for i in range(self.ff_max_number_of_results):
            self.ff_results_string_temp = "res" + str(i+1) + "_name = :res" + str(i+1) + "_name, " \
                                          "res" + str(i+1) + "_min = :res" + str(i+1) + "_min, " \
                                          "res" + str(i+1) + "_max = :res" + str(i+1) + "_max, " \
                                          "res" + str(i+1) + "_prec = :res" + str(i+1) + "_prec, " \
                                          "res" + str(i+1) + "_tol = :res" + str(i+1) + "_tol, " \
                                          "res" + str(i+1) + "_points = :res" + str(i+1) + "_points, " \
                                          "res" + str(i+1) + "_formula = :res" + str(i+1) + "_formula," \
                                          "res" + str(i+1) + "_unit = :res" + str(i+1) + "_unit"


            cursor.execute(" UPDATE formelfrage_table SET " + self.ff_results_string_temp + " WHERE oid = :oid",
                                    {'res' + str(i+1) + '_name': "",
                                     'res' + str(i+1) + '_min': self.ff_results_settings_to_db_list[i][2],
                                     'res' + str(i+1) + '_max': self.ff_results_settings_to_db_list[i][3],
                                     'res' + str(i+1) + '_prec': self.ff_results_settings_to_db_list[i][0],
                                     'res' + str(i+1) + '_tol': self.ff_results_settings_to_db_list[i][1],
                                     'res' + str(i+1) + '_points': self.ff_results_settings_to_db_list[i][4],
                                     'res' + str(i+1) + '_formula': self.ff_results_settings_to_db_list[i][5],
                                     'res' + str(i+1) + '_unit': "",
                                     'oid': self.ff_max_oid
                                     })

        conn.commit()
        conn.close()

        print("FF - inserted")

    def insert_into_sc_db(self, question_attributes_list, description_img_path_list,
                          response_text_list, response_img_label_list, response_img_base64_data_list,
                          response_pts_list, max_number_of_responses ):

        # copy() wird verwendet um die eigentliche Liste nicht zu veränder, sondern eine Kopie zu erstellen
        self.response_text_list = response_text_list.copy()
        self.response_img_label_list = response_img_label_list.copy()
        self.response_img_base64_data_list = response_img_base64_data_list.copy()
        self.response_pts_list = response_pts_list.copy()
        self.max_number_of_responses = max_number_of_responses

        self.description_img_path_list = description_img_path_list.copy()

        # Listen ohne Einträge mit "" auffüllen, damit keine "NULL" Einträge in der DB exestieren
        for i in range(3 - len(self.description_img_path_list)):
            self.description_img_path_list.append("")


        for i in range(self.max_number_of_responses - len(self.response_text_list)):
            self.response_text_list.append("")
            self.response_img_label_list.append("")
            self.response_img_base64_data_list.append("")
            self.response_pts_list.append("")




        self.responses_string_temp = ""

        self.question_attributes_beginning_1 = "question_type, question_title, question_description_title, question_description_main, "
        self.question_attributes_beginning_2 = ":question_type, :question_title, :question_description_title, :question_description_main, "



        self.question_attributes_ending_1 = "picture_preview_pixel,  description_img_path_1, description_img_path_2, description_img_path_3, test_time, question_author, question_difficulty, question_type, question_category, question_pool_tag "
        self.question_attributes_ending_2 = ":picture_preview_pixel,  :description_img_path_1, :description_img_path_2, :description_img_path_3, :test_time, :question_author, :question_difficulty, :question_type, :question_category, :question_pool_tag "

        # Verbindung mit der Datenbank herstellen
        conn = sqlite3.connect(self.database_singlechoice_path)
        cursor = conn.cursor()


        cursor.execute("INSERT INTO singlechoice_table "
                       "(" + self.question_attributes_beginning_1 + self.question_attributes_ending_1 + ")"
                       "VALUES"
                       "(" + self.question_attributes_beginning_2 + self.question_attributes_ending_2 + ")",
                       {"question_title":              question_attributes_list[1],
                        "question_description_title":   question_attributes_list[2],
                        "question_description_main":    question_attributes_list[3],
                        "picture_preview_pixel":        question_attributes_list[4],
                        "description_img_path_1": self.description_img_path_list[0],
                        "description_img_path_2": self.description_img_path_list[1],
                        "description_img_path_3": self.description_img_path_list[2],
                        "test_time":                    question_attributes_list[0],
                        "question_author":              question_attributes_list[5],
                        "question_difficulty":          "",
                        "question_type":                "singlechoice",
                        "question_category":            "",
                        "question_pool_tag":            ""          #todo need taxonomy?
                        })


        self.max_oid = Import_ILIAS_Datei_in_DB.find_max_oid_in_table(self, conn, "singlechoice_table")

        for i in range(self.max_number_of_responses):

            self.responses_string_temp = "response_" + str(i+1) + "_text = :response_" + str(i+1) + "_text, " \
                                          "response_" + str(i+1) + "_pts = :response_" + str(i+1) + "_pts, " \
                                          "response_" + str(i+1) + "_img_path = :response_" + str(i+1) + "_img_path "


            cursor.execute(" UPDATE singlechoice_table SET " + self.responses_string_temp + " WHERE oid =:oid",
                                    {"response_" + str(i+1) + "_text": self.response_text_list[i],
                                     "response_" + str(i+1) + "_pts": self.response_pts_list[i],
                                     "response_" + str(i+1) + "_img_path": self.response_img_label_list[i],
                                     'oid': self.max_oid
                                     })

        conn.commit()
        conn.close()

        print("SC - inserted")

    def insert_into_mc_db(self, question_attributes_list, description_img_path_list,
                          response_text_list, response_img_label_list, response_img_base64_data_list,
                          mc_response_correct_pts_list, mc_response_false_pts_list, max_number_of_responses):

        # copy() wird verwendet um die eigentliche Liste nicht zu veränder, sondern eine Kopie zu erstellen
        self.mc_question_attributes_to_db_list = question_attributes_list.copy()

        self.mc_response_text_to_db_list = response_text_list.copy()
        self.mc_response_img_label_to_db_list = response_img_label_list.copy()
        self.mc_response_img_base64_data_to_db_list = response_img_base64_data_list.copy()
        self.mc_response_correct_pts_to_db_list = mc_response_correct_pts_list.copy()
        self.mc_response_false_pts_to_db_list = mc_response_false_pts_list.copy()
        self.mc_max_number_of_responses = max_number_of_responses

        self.mc_description_img_path_to_db_list = description_img_path_list.copy()

        # Listen ohne Einträge mit "" auffüllen, damit keine "NULL" Einträge in der DB exestieren
        for i in range(3 - len(self.mc_description_img_path_to_db_list)):
            self.mc_description_img_path_to_db_list.append("")


        for i in range(self.mc_max_number_of_responses - len(self.mc_response_text_to_db_list)):
            self.mc_response_text_to_db_list.append("")
            self.mc_response_img_label_to_db_list.append("")
            self.mc_response_img_base64_data_to_db_list.append("")
            self.mc_response_correct_pts_to_db_list.append("")
            self.mc_response_false_pts_to_db_list.append("")



        self.mc_responses_string_temp = ""

        self.mc_question_attributes_beginning_1 = "question_type, question_title, question_description_title, question_description_main, "
        self.mc_question_attributes_beginning_2 = ":question_type, :question_title, :question_description_title, :question_description_main, "



        self.mc_question_attributes_ending_1 = "picture_preview_pixel, description_img_path_1, description_img_path_2, description_img_path_3, test_time, question_author, question_difficulty, question_type, question_category, question_pool_tag "
        self.mc_question_attributes_ending_2 = ":picture_preview_pixel, :description_img_path_1, :description_img_path_2, :description_img_path_3, :test_time, :question_author, :question_difficulty, :question_type, :question_category, :question_pool_tag "

        # Verbindung mit der Datenbank herstellen
        conn = sqlite3.connect(self.database_multiplechoice_path)
        cursor = conn.cursor()


        cursor.execute("INSERT INTO multiplechoice_table "
                       "(" + self.mc_question_attributes_beginning_1 + self.mc_question_attributes_ending_1 + ")"
                       "VALUES"
                       "(" + self.mc_question_attributes_beginning_2 + self.mc_question_attributes_ending_2 + ")",
                       {"question_title":                   self.mc_question_attributes_to_db_list[1],
                        "question_description_title":       self.mc_question_attributes_to_db_list[2],
                        "question_description_main":        self.mc_question_attributes_to_db_list[3],
                        "picture_preview_pixel":            self.mc_question_attributes_to_db_list[4],
                        "description_img_path_1":  self.mc_description_img_path_to_db_list[0],
                        "description_img_path_2":  self.mc_description_img_path_to_db_list[1],
                        "description_img_path_3":  self.mc_description_img_path_to_db_list[2],
                        "test_time":                        self.mc_question_attributes_to_db_list[0],
                        "question_author":                  self.mc_question_attributes_to_db_list[5],
                        "question_difficulty":          "",
                        "question_type":                "multiplechoice",
                        "question_category":            "",
                        "question_pool_tag":            ""          #todo need taxonomy?
                        })


        self.mc_max_oid = Import_ILIAS_Datei_in_DB.find_max_oid_in_table(self, conn, "multiplechoice_table")

        for i in range(self.mc_max_number_of_responses):


            self.mc_responses_string_temp = "response_" + str(i+1) + "_text = :response_" + str(i+1) + "_text, " \
                                            "response_" + str(i+1) + "_pts_correct_answer = :response_" + str(i+1) + "_pts_correct_answer, " \
                                            "response_" + str(i+1) + "_pts_false_answer = :response_" + str(i+1) + "_pts_false_answer, " \
                                            "response_" + str(i+1) + "_img_path = :response_" + str(i+1) + "_img_path "


            cursor.execute(" UPDATE multiplechoice_table SET " + self.mc_responses_string_temp + " WHERE oid =:oid",
                                    {"response_" + str(i+1) + "_text": self.mc_response_text_to_db_list[i],
                                     "response_" + str(i+1) + "_pts_correct_answer": self.mc_response_correct_pts_to_db_list[i],
                                     "response_" + str(i+1) + "_pts_false_answer": self.mc_response_false_pts_to_db_list[i],
                                     "response_" + str(i+1) + "_img_path": self.mc_response_img_label_to_db_list[i],
                                     'oid': self.mc_max_oid
                                     })

        conn.commit()
        conn.close()

        print("MC - inserted")

    def insert_into_mq_db(self, question_attributes_list, description_img_path_list,
                          response_definition_text_list, response_definition_img_label_list, response_definition_img_base64_data_list,
                          response_term_text_list, response_term_img_label_list, response_term_img_base64_data_list,
                          mq_assignment_pairs_definition_list, mq_assignment_pairs_term_list,  mq_assignment_pairs_pts_list,
                          max_number_of_responses):


        # copy() wird verwendet um die eigentliche Liste nicht zu veränder, sondern eine Kopie zu erstellen
        self.mq_question_attributes_to_db_list = question_attributes_list.copy()

        self.mq_definition_response_text_to_db_list = response_definition_text_list.copy()
        self.mq_definition_response_img_label_to_db_list = response_definition_img_label_list.copy()
        self.mq_definition_response_img_base64_data_to_db_list = response_definition_img_base64_data_list.copy()

        self.mq_term_response_text_to_db_list = response_term_text_list.copy()
        self.mq_term_response_img_label_to_db_list = response_term_img_label_list.copy()
        self.mq_term_response_img_base64_data_to_db_list = response_term_img_base64_data_list.copy()

        self.mq_assignment_pairs_definition_to_db_list = mq_assignment_pairs_definition_list.copy()
        self.mq_assignment_pairs_term_to_db_list = mq_assignment_pairs_term_list.copy()
        self.mq_assignment_pairs_pts_to_db_list = mq_assignment_pairs_pts_list.copy()

        self.mq_max_number_of_responses = max_number_of_responses

        self.mq_description_img_path_to_db_list = description_img_path_list.copy()

        # Listen ohne Einträge mit "" auffüllen, damit keine "NULL" Einträge in der DB exestieren
        for i in range(3 - len(self.mq_description_img_path_to_db_list)):
            self.mq_description_img_path_to_db_list.append("")


        for i in range(self.mq_max_number_of_responses - len(self.mq_definition_response_text_to_db_list)):
            self.mq_definition_response_text_to_db_list.append("")
            self.mq_definition_response_img_label_to_db_list.append("")
            self.mq_definition_response_img_base64_data_to_db_list.append("")

            self.mq_term_response_text_to_db_list.append("")
            self.mq_term_response_img_label_to_db_list.append("")
            self.mq_term_response_img_base64_data_to_db_list.append("")

            self.mq_assignment_pairs_definition_to_db_list.append("")
            self.mq_assignment_pairs_term_to_db_list.append("")
            self.mq_assignment_pairs_pts_to_db_list.append("")


        self.mq_responses_string_temp = ""

        self.mq_question_attributes_beginning_1 = "question_type, question_title, question_description_title, question_description_main, "
        self.mq_question_attributes_beginning_2 = ":question_type, :question_title, :question_description_title, :question_description_main, "



        self.mq_question_attributes_ending_1 = "picture_preview_pixel, mix_answers, assignment_mode, description_img_path_1, description_img_path_2, description_img_path_3, test_time, question_author, question_difficulty, question_type, question_category, question_pool_tag "
        self.mq_question_attributes_ending_2 = ":picture_preview_pixel, :mix_answers, :assignment_mode, :description_img_path_1, :description_img_path_2, :description_img_path_3, :test_time, :question_author, :question_difficulty, :question_type, :question_category, :question_pool_tag "

        # Verbindung mit der Datenbank herstellen
        conn = sqlite3.connect(self.database_zuordnungsfrage_path)
        cursor = conn.cursor()


        cursor.execute("INSERT INTO zuordnungsfrage_table "
                       "(" + self.mq_question_attributes_beginning_1 + self.mq_question_attributes_ending_1 + ")"
                       "VALUES"
                       "(" + self.mq_question_attributes_beginning_2 + self.mq_question_attributes_ending_2 + ")",
                       {"question_title":                   self.mq_question_attributes_to_db_list[1],
                        "question_description_title":       self.mq_question_attributes_to_db_list[2],
                        "question_description_main":        self.mq_question_attributes_to_db_list[3],
                        "picture_preview_pixel":            self.mq_question_attributes_to_db_list[4],
                        "mix_answers":                      self.mq_question_attributes_to_db_list[5],
                        "assignment_mode":                      self.mq_question_attributes_to_db_list[6],
                        "description_img_path_1":  self.mq_description_img_path_to_db_list[0],
                        "description_img_path_2":  self.mq_description_img_path_to_db_list[1],
                        "description_img_path_3":  self.mq_description_img_path_to_db_list[2],
                        "test_time":                        self.mq_question_attributes_to_db_list[0],
                        "question_author":                  self.mq_question_attributes_to_db_list[7],
                        "question_difficulty":          "",
                        "question_type":                "zuordnungsfrage",
                        "question_category":            "",
                        "question_pool_tag":            ""          #todo need taxonomy?
                        })

        self.mq_max_oid = Import_ILIAS_Datei_in_DB.find_max_oid_in_table(self, conn, "zuordnungsfrage_table")

        for i in range(self.mq_max_number_of_responses):
            self.mq_responses_string_temp = "definitions_response_" + str(i+1) + "_text = :definitions_response_" + str(i+1) + "_text, " \
                                          "definitions_response_" + str(i+1) + "_img_path = :definitions_response_" + str(i+1) + "_img_path, " \
                                          "terms_response_" + str(i+1) + "_text = :terms_response_" + str(i+1) + "_text, " \
                                          "terms_response_" + str(i+1) + "_img_path = :terms_response_" + str(i+1) + "_img_path, " \
                                          "assignment_pairs_definition_" + str(i+1) + " = :assignment_pairs_definition_" + str(i+1) + ", " \
                                          "assignment_pairs_term_" + str(i+1) + " = :assignment_pairs_term_" + str(i+1) + ", " \
                                          "assignment_pairs_" + str(i+1) + "_pts = :assignment_pairs_" + str(i+1) + "_pts "

            cursor.execute("UPDATE zuordnungsfrage_table" + " SET " + self.mq_responses_string_temp + " WHERE oid = :oid",
                            {"definitions_response_" + str(i+1) + "_text": self.mq_definition_response_text_to_db_list[i],
                             "definitions_response_" + str(i+1) + "_img_path": self.mq_definition_response_img_label_to_db_list[i],
                             "terms_response_" + str(i+1) + "_text": self.mq_term_response_text_to_db_list[i],
                             "terms_response_" + str(i+1) + "_img_path": self.mq_term_response_img_label_to_db_list[i],
                             "assignment_pairs_definition_" + str(i+1): self.mq_assignment_pairs_definition_to_db_list[i],
                             "assignment_pairs_term_" + str(i+1): self.mq_assignment_pairs_term_to_db_list[i],
                             "assignment_pairs_" + str(i+1) + "_pts": self.mq_assignment_pairs_pts_to_db_list[i],
                             "oid": self.mq_max_oid
                             })

        conn.commit()
        conn.close()

        print("MQ - inserted")
    def find_max_oid_in_table(self, database_connection, database_table):

        self.oid = 0
        self.oid_list = []
        self.database_connection = database_connection
        self.database_table = database_table

        cursor = self.database_connection.cursor()

        # Alle Einträge aus der DB durchsuchen (mit oid Eintrag)
        # oid ist eine individuelle ID für jede Frage in einer Datenbank
        # Der Eintrag ist üblicherweise ausgeblendet und wird mit "SELECT *, oid.." aktiv dargestellt
        cursor.execute("SELECT *, oid FROM " + str(self.database_table))
        self.db_records = cursor.fetchall()


        # Die oid von allen enthaltenen Fragen sammeln. [-1] greift auf das letzte Fach zu
        # Das letzte Fach ist IMMER der oid Eintrag
        for db_record in self.db_records:
            self.oid_list.append(db_record[-1])

        # Aus den gesammelten Einträgen wird der höchste Wert genommen
        self.oid = max(self.oid_list)

        return self.oid
