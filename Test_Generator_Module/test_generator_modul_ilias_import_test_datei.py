from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
from tkinter import ttk
import sqlite3                              #verwendet für mySQL Datenbank
import xml.etree.ElementTree as ET
import os
import pathlib
import base64

class Import_ILIAS_Datei_in_DB:

    def __init__(self, project_root_path):

        # Pfade für Datenbanken
        self.project_root_path = project_root_path
        self.database_formelfrage_path = os.path.normpath(os.path.join(self.project_root_path, "Test_Generator_Datenbanken", "ilias_formelfrage_db.db"))
        self.database_singlechoice_path = os.path.normpath(os.path.join(self.project_root_path,"Test_Generator_Datenbanken", "ilias_singlechoice_db.db"))
        self.database_multiplechoice_path = os.path.normpath(os.path.join(self.project_root_path,"Test_Generator_Datenbanken", "ilias_multiplechoice_db.db"))
        self.database_zuordnungsfrage_path = os.path.normpath(os.path.join(self.project_root_path,"Test_Generator_Datenbanken", "ilias_zuordnungsfrage_db.db"))




        self.ilias_question_type = []

        self.ilias_question_title = []
        self.ilias_question_description_title = []
        self.ilias_question_description_main = []

        # SINGLE CHOICE
        self.ilias_response_text = []
        self.ilias_response_pts = []
        self.ilias_response_img_label = []
        self.ilias_response_img_string_base64_encoded = []
        self.ilias_response_img_path = []
        self.ilias_picture_preview_pixel = []
        ##########

        # MULTIPLE CHOICE
        self.mc_ilias_response_text = []
        self.mc_ilias_response_pts = []
        self.mc_ilias_response_img_label = []
        self.mc_ilias_response_img_string_base64_encoded = []
        self.mc_ilias_response_img_path = []
        self.mc_ilias_picture_preview_pixel = []
        ##########

        # Es werden bis zu drei Bilder im Fragen-Text aufgenommen
        self.ilias_test_question_description_image_name_1 = []
        self.ilias_test_question_description_image_data_1 = []
        self.ilias_test_question_description_image_uri_1 = []
        self.ilias_test_question_description_image_name_2 = []
        self.ilias_test_question_description_image_data_2 = []
        self.ilias_test_question_description_image_uri_2 = []
        self.ilias_test_question_description_image_name_3 = []
        self.ilias_test_question_description_image_data_3 = []
        self.ilias_test_question_description_image_uri_3 = []

        self.ilias_test_duration = []
        self.ilias_question_author = []

        self.description_singlechoice_del_index = []
        self.description_multiplechoice_del_index = []
        self.description_matchedquestion_del_index = []

        self.all_sc_questions_points = []

        self.mattext_text_all_mc_answers = []
        self.all_mc_questions_points = []
        self.mc_questions_correct_points = []
        self.mc_questions_false_points = []


        self.mattext_text_all_mq_answers = []
        self.mattext_text_all_mq_answers_collection = []
        self.mattText_text_all_mq_answers = []

        self.sc_answer_list_nr = ""
        self.mc_answer_list_nr = ""
        self.mq_answer_list_nr = ""

        self.mq_answer_matchings = []
        self.mq_number_of_answers_per_question = []
        self.mq_number_of_answers_per_question_temp = []
        self.mq_answer_matchings_points = []
        self.mq_answer_matching_per_question = []

        self.mq_response_img_label = []
        self.mq_response_img_data = []
        self.mq_response_img_path = []
        self.mq_matching_ids = []
        self.mq_matching_ids_points = []
        self.mq_len_list = []


        self.number_of_answers_per_question_sc = []
        self.number_of_answers_per_question_mc = []
        self.number_of_answers_per_question_mq = []

        self.ilias_question_title_sc = []
        self.ilias_question_author_sc = []
        self.ilias_question_type_ff_question_index = []
        self.ilias_question_type_sc_question_index = []
        self.ilias_question_type_mc_question_index = []
        self.ilias_question_type_mq_question_index = []



        ### Hier wird die ausgewählte XML nach möglichen Fragen-Typen durchsucht und entsprechende flag gesetzt

        self.formelfrage_flag = 0
        self.singlechoice_flag = 0
        self.multiplechoice_flag = 0
        self.matchingquestion_flag = 0

        self.formelfrage_number_of_questions = 0
        self.singlechoice_number_of_questions = 0
        self.multiplechoice_number_of_questions = 0
        self.matchingquestion_number_of_questions = 0



        # Auswahl der Datei die bearbeitet werden soll
        filename = filedialog.askdirectory(initialdir=pathlib.Path().absolute(), title="Select a File")
        self.select_test_import_file = filename

        # Ordner-Name splitten um automatisiert die enthaltene qti.xml Datei einlesen zu können
        self.ilias_folder_name = self.select_test_import_file.rsplit('/', 1)[-1]
        self.ilias_folder_name_split1 = self.ilias_folder_name[:15]
        self.ilias_folder_name_split2 = self.ilias_folder_name.rsplit('_', 1)[-1]
        self.ilias_test_qti_file = os.path.normpath(os.path.join(self.select_test_import_file, self.ilias_folder_name_split1 + "qti_" + self.ilias_folder_name_split2 + ".xml"))



        # XML Datei einlesen -> Root Verzeichnis bestimmen
        self.mytree = ET.parse(self.ilias_test_qti_file)
        self.myroot = self.mytree.getroot()

        # Alle Fragentypen aus der XML Datei aufnehmen
        for qtimetadatafield in self.myroot.iter('qtimetadatafield'):
            if qtimetadatafield.find('fieldlabel').text == "QUESTIONTYPE":
                self.ilias_question_type.append(qtimetadatafield.find('fieldentry').text)




#################### ALLE FRAGEN-INDEXE DEN FRAGENTYPEN ZUORDNEN

        for i in range(len(self.ilias_question_type)):
            if self.ilias_question_type[i] == "assFormulaQuestion":
                self.ilias_question_type_ff_question_index.append(str(i))
                self.formelfrage_flag = 1
                self.formelfrage_number_of_questions += 1

            elif self.ilias_question_type[i] == "SINGLE CHOICE QUESTION":
                self.ilias_question_type_sc_question_index.append(str(i))
                self.singlechoice_flag = 1
                self.singlechoice_number_of_questions += 1

            elif self.ilias_question_type[i] == "MULTIPLE CHOICE QUESTION":
                self.ilias_question_type_mc_question_index.append(str(i))
                self.multiplechoice_flag = 1
                self.multiplechoice_number_of_questions += 1

            elif self.ilias_question_type[i] == "MATCHING QUESTION":
                self.ilias_question_type_mq_question_index.append(str(i))
                self.matchingquestion_flag = 1
                self.matchingquestion_number_of_questions += 1

            else:
                print("Keine Fragen gefunden")



        print("Anzahl Formelfrage: " + str(self.formelfrage_number_of_questions))
        print("Anzahl SingleChoice: " + str(self.singlechoice_number_of_questions))
        print("Anzahl MultipleChoice: " + str(self.multiplechoice_number_of_questions))
        print("Anzahl Zuordnungsfrage: " + str(self.matchingquestion_number_of_questions))


################# FRAGEN-BESCHREIBUNG (FRAGEN-TEXT) SAMMELN

        # Fragen-Beschreibung, aller Fragen, sammeln
        for flow in self.myroot.iter('flow'):
            for material in flow.iter('material'):
                if "" in material.find('mattext').text:


                    # Wenn in dem Fragentext "img" enthalten ist, gibt es immer auch ein Bild zu der Frage
                    if "il_0_mob_" in material.find('mattext').text:
                        self.ilias_question_description_main.append(material.find('mattext').text)

                        #Bildname hinzufügen
                        if material.find('matimage').attrib.get('label'):
                            self.ilias_test_question_description_image_name_1.append(material.find('matimage').attrib.get('label'))


                        # Bild Pfad hinzufügen
                        if material.find('matimage').attrib.get('uri'):
                            self.ilias_test_question_description_image_uri_1.append(material.find('matimage').attrib.get('uri'))

                    else:
                        self.ilias_question_description_main.append(material.find('mattext').text)
                        self.ilias_test_question_description_image_name_1.append("EMPTY")
                        self.ilias_test_question_description_image_uri_1.append("EMPTY")
                        self.ilias_test_question_description_image_name_2.append("EMPTY")
                        self.ilias_test_question_description_image_uri_2.append("EMPTY")
                        self.ilias_test_question_description_image_name_3.append("EMPTY")
                        self.ilias_test_question_description_image_uri_3.append("EMPTY")







################# FRAGEN HAUPTATTRIBUTE AUSLESEN
        # Zu den Hauputattributen gehören z.B. "Fragen-Titel", "Fragen-Beschreibung", "Autor" etc.


        # Fragen-Titel auslesen
        for item in self.myroot.iter('item'):
            self.ilias_question_title.append(item.get('title'))

        # Fragen-Einleitungstext auslesen
        # Wenn der Eintrag nicht existiert, dann Eintrag erstellen und "" einfügen
        for qticomment in self.myroot.iter('qticomment'):
            if qticomment.text == None:
                qticomment.text = ""

        for item in self.myroot.iter('item'):
            if "" in item.find('qticomment').text:
                self.ilias_question_description_title.append(item.find('qticomment').text)


        # Test-Dauer auslesen (wenn Eintrag existiert
        for item in self.myroot.iter('item'):
            if "" in item.find('duration').text:
                self.ilias_test_duration.append(item.find('duration').text)

        # Fragen-Autor auslesen
        for qtimetadatafield in self.myroot.iter('qtimetadatafield'):
            if qtimetadatafield.find('fieldlabel').text == "AUTHOR":
                self.ilias_question_author.append(qtimetadatafield.find('fieldentry').text)


########### FRAGEN AUSLESEN JE NACH FRAGEN-TYP

        # Fragen auslesen: Single Choice
        if self.singlechoice_flag == 1:
            Import_ILIAS_Datei_in_DB.read_singlechoice_questions(self)

        # Fragen auslesen: Formelfrage
        if self.formelfrage_flag == 1:
            Import_ILIAS_Datei_in_DB.read_formelfrage_questions(self)

        # Fragen auslesen: Multiple Choice
        if self.multiplechoice_flag == 1:
            Import_ILIAS_Datei_in_DB.read_multiplechoice_questions(self)

        # Fragen auslesen: Matching Question
        if self.matchingquestion_flag == 1:
            Import_ILIAS_Datei_in_DB.read_matching_questions(self)


################ FRAGEN_BESCHREIBUNG (FRAGEN-TEXT) FILTERN
        # Single Choice Antworten entfernen
        for i in range(len(self.ilias_question_description_main)):
            for j in range(len(self.ilias_response_text)):
                if self.ilias_question_description_main[i] == self.ilias_response_text[j]:
                    self.description_singlechoice_del_index.append(i)


        # Remove any dublicates, dict's können keine Elemente mehrfach besitzen. Daher werden alle doppelten Einträge entfernt
        # Doppelte Einträge entstehen wenn die Antwort bzw. die Beschreibung genau gleich lautet
        # Z.B. Zeigerdiagramm, Zeigerdiagramm
        self.description_singlechoice_del_index = list(dict.fromkeys(self.description_singlechoice_del_index))


        for i in range(len(self.description_singlechoice_del_index)):
            if len(self.description_singlechoice_del_index) > 0:
                self.ilias_question_description_main.pop(self.description_singlechoice_del_index[i]-i)
                self.ilias_test_question_description_image_name_1.pop(self.description_singlechoice_del_index[i]-i)
                self.ilias_test_question_description_image_uri_1.pop(self.description_singlechoice_del_index[i]-i)


        # Multiple Choice Antworten entfernen
        for i in range(len(self.ilias_question_description_main)):
            for j in range(len(self.mattext_text_all_mc_answers)):
                if self.ilias_question_description_main[i] == self.mattext_text_all_mc_answers[j]:
                    self.description_multiplechoice_del_index.append(i)

        for i in range(len(self.description_multiplechoice_del_index)):
            if len(self.description_multiplechoice_del_index) > 0:
                self.ilias_question_description_main.pop(self.description_multiplechoice_del_index[i]-i)
                self.ilias_test_question_description_image_name_1.pop(self.description_multiplechoice_del_index[i]-i)
                self.ilias_test_question_description_image_uri_1.pop(self.description_multiplechoice_del_index[i]-i)



        # Matched Questions Antworten entfernen
        for i in range(len(self.ilias_question_description_main)):
            for j in range(len(self.mattText_text_all_mq_answers)):
                if self.ilias_question_description_main[i] == self.mattText_text_all_mq_answers[j]:
                    self.description_matchedquestion_del_index.append(i)



        # Remove any dublicates, dict's können keine Elemente mehrfach besitzen. Daher werden alle doppelten Einträge entfernt
        # Doppelte Einträge entstehen wenn die Antwort bzw. die Beschreibung genau gleich lautet
        # Z.B. Zeigerdiagramm, Zeigerdiagramm
        self.description_matchedquestion_del_index = list(dict.fromkeys(self.description_matchedquestion_del_index))


        for i in range(len(self.description_matchedquestion_del_index)):
            if len(self.description_matchedquestion_del_index) > 0:
                self.ilias_question_description_main.pop(self.description_matchedquestion_del_index[i]-i)
                self.ilias_test_question_description_image_name_1.pop(self.description_matchedquestion_del_index[i]-i)
                self.ilias_test_question_description_image_uri_1.pop(self.description_matchedquestion_del_index[i]-i)




########### FRAGEN IN DATENBANK SCHREIBEN
        # Schreiben
        if self.singlechoice_flag == 1:
            Import_ILIAS_Datei_in_DB.write_data_to_database_sc(self)
        if self.formelfrage_flag == 1:
            Import_ILIAS_Datei_in_DB.write_data_to_database_ff(self)
        if self.multiplechoice_flag == 1:
            Import_ILIAS_Datei_in_DB.write_data_to_database_mc(self)
        if self.matchingquestion_flag == 1:
            Import_ILIAS_Datei_in_DB.write_data_to_database_mq(self)

####### Single Choice Fragen
    def read_singlechoice_questions(self):


        # SINGLE CHOICE Punkte für Antworten
        for respcondition in self.myroot.iter('respcondition'):
            for varequal in respcondition.iter('varequal'):
                if varequal.attrib.get('respident') == "MCSR":
                    for setvar in respcondition.iter('setvar'):
                        self.ilias_response_pts.append(setvar.text)

        # SINGLE CHOICE Antworten und Bilder
        for response_lid in self.myroot.iter('response_lid'):
            if response_lid.attrib.get('ident') == "MCSR":  # SR -> Single Choice
                for render_choice in response_lid.iter('render_choice'):
                    for response_label in render_choice.iter('response_label'):
                        for material in response_label.iter('material'):
                            if material.find('matimage') == None:
                                self.ilias_response_img_label.append("EMPTY")
                                self.ilias_response_img_string_base64_encoded.append("EMPTY")

                            else:
                                self.ilias_response_img_label.append(material.find('matimage').attrib.get('label'))
                                self.ilias_response_img_string_base64_encoded.append(material.find('matimage').text)


                            for mattext in material.iter('mattext'):
                                self.ilias_response_text.append(mattext.text)



        self.count=[]





#####################################   Anzahl der Antworten pro SC-Frage
         # Durch diese Iteration und Abfrage nach MCSR (=Single Choice), werden alle Antworten der SC-Fragen aufgelistet
        for response_lid in self.myroot.iter('response_lid'):
            if response_lid.attrib.get('ident') == 'MCSR':
                for render_choice in response_lid.iter('render_choice'):
                    # Zu Beginn jedes Anwort-Blocks wird ein "$" geschrieben, um hinterher zu splitten
                    self.sc_answer_list_nr += "$"
                    for response_label in render_choice.iter('response_label'):
                        self.sc_answer_list_nr += str(response_label.attrib.get('ident'))

        self.ilias_test_question_type_collection_sc_answers = self.sc_answer_list_nr.split("$")
        self.ilias_test_question_type_collection_sc_answers.pop(0)  # Durch split() enthält erstes Feld keine Daten

        for i in range(len(self.ilias_test_question_type_collection_sc_answers)):
            self.number_of_answers_per_question_sc.append(str( int(max(self.ilias_test_question_type_collection_sc_answers[i]))+1))




#################################### Punkte für Fragen


#####################################   Haupt-Fragentext aufzählen


        self.ilias_number_of_response_variables = 10
        self.ilias_response_text_1, self.ilias_response_pts_1, self.ilias_response_img_label_1, self.ilias_response_img_string_base64_encoded_1 = [], [], [], []
        self.ilias_response_text_2, self.ilias_response_pts_2, self.ilias_response_img_label_2, self.ilias_response_img_string_base64_encoded_2 = [], [], [], []
        self.ilias_response_text_3, self.ilias_response_pts_3, self.ilias_response_img_label_3, self.ilias_response_img_string_base64_encoded_3 = [], [], [], []
        self.ilias_response_text_4, self.ilias_response_pts_4, self.ilias_response_img_label_4, self.ilias_response_img_string_base64_encoded_4 = [], [], [], []
        self.ilias_response_text_5, self.ilias_response_pts_5, self.ilias_response_img_label_5, self.ilias_response_img_string_base64_encoded_5 = [], [], [], []
        self.ilias_response_text_6, self.ilias_response_pts_6, self.ilias_response_img_label_6, self.ilias_response_img_string_base64_encoded_6 = [], [], [], []
        self.ilias_response_text_7, self.ilias_response_pts_7, self.ilias_response_img_label_7, self.ilias_response_img_string_base64_encoded_7 = [], [], [], []
        self.ilias_response_text_8, self.ilias_response_pts_8, self.ilias_response_img_label_8, self.ilias_response_img_string_base64_encoded_8 = [], [], [], []
        self.ilias_response_text_9, self.ilias_response_pts_9, self.ilias_response_img_label_9, self.ilias_response_img_string_base64_encoded_9 = [], [], [], []
        self.ilias_response_text_10, self.ilias_response_pts_10, self.ilias_response_img_label_10, self.ilias_response_img_string_base64_encoded_10 = [], [], [], []




        t = 0
        for i in range(len(self.ilias_test_question_type_collection_sc_answers)):
            if i == 1:
                t = int(max(self.ilias_test_question_type_collection_sc_answers[0])) + 1

            if "0" in self.ilias_test_question_type_collection_sc_answers[i]:
                self.ilias_response_text_1.append(self.ilias_response_text[t])
                self.ilias_response_pts_1.append(self.ilias_response_pts[t])
                self.ilias_response_img_label_1.append(self.ilias_response_img_label[t])
                self.ilias_response_img_string_base64_encoded_1.append(self.ilias_response_img_string_base64_encoded[t])
            else:
                self.ilias_response_text_1.append(" ")
                self.ilias_response_pts_1.append(" ")
                self.ilias_response_img_label_1.append("EMPTY")
                self.ilias_response_img_string_base64_encoded_1.append("EMPTY")

            if "1" in self.ilias_test_question_type_collection_sc_answers[i]:
                self.ilias_response_text_2.append(self.ilias_response_text[t + 1])
                self.ilias_response_pts_2.append(self.ilias_response_pts[t + 1])
                self.ilias_response_img_label_2.append(self.ilias_response_img_label[t + 1])
                self.ilias_response_img_string_base64_encoded_2.append(self.ilias_response_img_string_base64_encoded[t])
            else:
                self.ilias_response_text_2.append(" ")
                self.ilias_response_pts_2.append(" ")
                self.ilias_response_img_label_2.append("EMPTY")
                self.ilias_response_img_string_base64_encoded_2.append("EMPTY")

            if "2" in self.ilias_test_question_type_collection_sc_answers[i]:
                self.ilias_response_text_3.append(self.ilias_response_text[t + 2])
                self.ilias_response_pts_3.append(self.ilias_response_pts[t + 2])
                self.ilias_response_img_label_3.append(self.ilias_response_img_label[t + 2])
                self.ilias_response_img_string_base64_encoded_3.append(self.ilias_response_img_string_base64_encoded[t])
            else:
                self.ilias_response_text_3.append(" ")
                self.ilias_response_pts_3.append(" ")
                self.ilias_response_img_label_3.append("EMPTY")
                self.ilias_response_img_string_base64_encoded_3.append("EMPTY")

            if "3" in self.ilias_test_question_type_collection_sc_answers[i]:
                self.ilias_response_text_4.append(self.ilias_response_text[t + 3])
                self.ilias_response_pts_4.append(self.ilias_response_pts[t + 3])
                self.ilias_response_img_label_4.append(self.ilias_response_img_label[t + 3])
                self.ilias_response_img_string_base64_encoded_4.append(self.ilias_response_img_string_base64_encoded[t])
            else:
                self.ilias_response_text_4.append(" ")
                self.ilias_response_pts_4.append(" ")
                self.ilias_response_img_label_4.append("EMPTY")
                self.ilias_response_img_string_base64_encoded_4.append("EMPTY")

            if "4" in self.ilias_test_question_type_collection_sc_answers[i]:
                self.ilias_response_text_5.append(self.ilias_response_text[t + 4])
                self.ilias_response_pts_5.append(self.ilias_response_pts[t + 4])
                self.ilias_response_img_label_5.append(self.ilias_response_img_label[t + 4])
                self.ilias_response_img_string_base64_encoded_5.append(self.ilias_response_img_string_base64_encoded[t])
            else:
                self.ilias_response_text_5.append(" ")
                self.ilias_response_pts_5.append(" ")
                self.ilias_response_img_label_5.append("EMPTY")
                self.ilias_response_img_string_base64_encoded_5.append("EMPTY")

            if "5" in self.ilias_test_question_type_collection_sc_answers[i]:
                self.ilias_response_text_6.append(self.ilias_response_text[t + 5])
                self.ilias_response_pts_6.append(self.ilias_response_pts[t + 5])
                self.ilias_response_img_label_6.append(self.ilias_response_img_label[t + 5])
                self.ilias_response_img_string_base64_encoded_6.append(self.ilias_response_img_string_base64_encoded[t])
            else:
                self.ilias_response_text_6.append(" ")
                self.ilias_response_pts_6.append(" ")
                self.ilias_response_img_label_6.append("EMPTY")
                self.ilias_response_img_string_base64_encoded_6.append("EMPTY")

            if "6" in self.ilias_test_question_type_collection_sc_answers[i]:
                self.ilias_response_text_7.append(self.ilias_response_text[t + 6])
                self.ilias_response_pts_7.append(self.ilias_response_pts[t + 6])
                self.ilias_response_img_label_7.append(self.ilias_response_img_label[t + 6])
                self.ilias_response_img_string_base64_encoded_7.append(self.ilias_response_img_string_base64_encoded[t])
            else:
                self.ilias_response_text_7.append(" ")
                self.ilias_response_pts_7.append(" ")
                self.ilias_response_img_label_7.append("EMPTY")
                self.ilias_response_img_string_base64_encoded_7.append("EMPTY")

            if "7" in self.ilias_test_question_type_collection_sc_answers[i]:
                self.ilias_response_text_8.append(self.ilias_response_text[t + 7])
                self.ilias_response_pts_8.append(self.ilias_response_pts[t + 7])
                self.ilias_response_img_label_8.append(self.ilias_response_img_label[t + 7])
                self.ilias_response_img_string_base64_encoded_8.append(self.ilias_response_img_string_base64_encoded[t])
            else:
                self.ilias_response_text_8.append(" ")
                self.ilias_response_pts_8.append(" ")
                self.ilias_response_img_label_8.append("EMPTY")
                self.ilias_response_img_string_base64_encoded_8.append("EMPTY")

            if "8" in self.ilias_test_question_type_collection_sc_answers[i]:
                self.ilias_response_text_9.append(self.ilias_response_text[t + 8])
                self.ilias_response_pts_9.append(self.ilias_response_pts[t + 8])
                self.ilias_response_img_label_9.append(self.ilias_response_img_label[t + 8])
                self.ilias_response_img_string_base64_encoded_9.append(self.ilias_response_img_string_base64_encoded[t])
            else:
                self.ilias_response_text_9.append(" ")
                self.ilias_response_pts_9.append(" ")
                self.ilias_response_img_label_9.append("EMPTY")
                self.ilias_response_img_string_base64_encoded_9.append("EMPTY")

            if "9" in self.ilias_test_question_type_collection_sc_answers[i]:
                self.ilias_response_text_10.append(self.ilias_response_text[t + 9])
                self.ilias_response_pts_10.append(self.ilias_response_pts[t + 9])
                self.ilias_response_img_label_10.append(self.ilias_response_img_label[t + 9])
                self.ilias_response_img_string_base64_encoded_10.append(self.ilias_response_img_string_base64_encoded[t])
            else:
                self.ilias_response_text_10.append(" ")
                self.ilias_response_pts_10.append(" ")
                self.ilias_response_img_label_10.append("EMPTY")
                self.ilias_response_img_string_base64_encoded_10.append("EMPTY")

            t += int(max(self.ilias_test_question_type_collection_sc_answers[i])) + 1

    def write_data_to_database_sc(self):

        print("_______________________________________________")

        # Create a database or connect to one
        connect = sqlite3.connect(self.database_singlechoice_path)

        # Create cursor
        cursor = connect.cursor()

        for i in range(len( self.ilias_question_type_sc_question_index)):

            # Bilder der Reihe nach einlesen
            if self.ilias_test_question_description_image_uri_1[i] != "EMPTY":

                with open(os.path.normpath(os.path.join(self.select_test_import_file, self.ilias_test_question_description_image_uri_1[i])), 'rb') as image_file:
                    self.ilias_test_question_description_image_data_1.append(image_file.read())

            else:
                self.ilias_test_question_description_image_data_1.append("EMPTY")


            # Create table
            cursor.execute(
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
                    'question_difficulty': "",
                    'question_category': "",
                    'question_type': "Singlechoice",

                    'question_title': self.ilias_question_title[int(self.ilias_question_type_sc_question_index[i])],
                    'question_description_title': self.ilias_question_description_title[int(self.ilias_question_type_sc_question_index[i])],
                    'question_description_main': self.ilias_question_description_main[int(self.ilias_question_type_sc_question_index[i])],

                    'response_1_text': self.ilias_response_text_1[i],
                    'response_1_pts': self.ilias_response_pts_1[i],
                    'response_1_img_label': self.ilias_response_img_label_1[i],
                    'response_1_img_string_base64_encoded': self.ilias_response_img_string_base64_encoded_1[i],
                    'response_1_img_path': "",

                    'response_2_text': self.ilias_response_text_2[i],
                    'response_2_pts': self.ilias_response_pts_2[i],
                    'response_2_img_label': self.ilias_response_img_label_2[i],
                    'response_2_img_string_base64_encoded': self.ilias_response_img_string_base64_encoded_2[i],
                    'response_2_img_path': "",

                    'response_3_text':  self.ilias_response_text_3[i],
                    'response_3_pts': self.ilias_response_pts_3[i],
                    'response_3_img_label': self.ilias_response_img_label_3[i],
                    'response_3_img_string_base64_encoded': self.ilias_response_img_string_base64_encoded_3[i],
                    'response_3_img_path': "",

                    'response_4_text': self.ilias_response_text_4[i],
                    'response_4_pts': self.ilias_response_pts_4[i],
                    'response_4_img_label': self.ilias_response_img_label_4[i],
                    'response_4_img_string_base64_encoded': self.ilias_response_img_string_base64_encoded_4[i],
                    'response_4_img_path': "",

                    'response_5_text': self.ilias_response_text_5[i],
                    'response_5_pts': self.ilias_response_pts_5[i],
                    'response_5_img_label': self.ilias_response_img_label_5[i],
                    'response_5_img_string_base64_encoded': self.ilias_response_img_string_base64_encoded_5[i],
                    'response_5_img_path': "",

                    'response_6_text': self.ilias_response_text_6[i],
                    'response_6_pts': self.ilias_response_pts_6[i],
                    'response_6_img_label': self.ilias_response_img_label_6[i],
                    'response_6_img_string_base64_encoded': self.ilias_response_img_string_base64_encoded_6[i],
                    'response_6_img_path': "",

                    'response_7_text': self.ilias_response_text_7[i],
                    'response_7_pts': self.ilias_response_pts_7[i],
                    'response_7_img_label': self.ilias_response_img_label_7[i],
                    'response_7_img_string_base64_encoded': self.ilias_response_img_string_base64_encoded_7[i],
                    'response_7_img_path': "",

                    'response_8_text': self.ilias_response_text_8[i],
                    'response_8_pts': self.ilias_response_pts_8[i],
                    'response_8_img_label': self.ilias_response_img_label_8[i],
                    'response_8_img_string_base64_encoded': self.ilias_response_img_string_base64_encoded_8[i],
                    'response_8_img_path': "",

                    'response_9_text': self.ilias_response_text_9[i],
                    'response_9_pts': self.ilias_response_pts_9[i],
                    'response_9_img_label': self.ilias_response_img_label_9[i],
                    'response_9_img_string_base64_encoded': self.ilias_response_img_string_base64_encoded_9[i],
                    'response_9_img_path': "",

                    'response_10_text': self.ilias_response_text_10[i],
                    'response_10_pts': self.ilias_response_pts_10[i],
                    'response_10_img_label': self.ilias_response_img_label_10[i],
                    'response_10_img_string_base64_encoded': self.ilias_response_img_string_base64_encoded_10[i],
                    'response_10_img_path': "",

                    'picture_preview_pixel': "",

                    'description_img_name_1': self.ilias_test_question_description_image_name_1[i],
                    'description_img_data_1': self.ilias_test_question_description_image_data_1[i],
                    'description_img_path_1': self.ilias_test_question_description_image_uri_1[i],

                    'description_img_name_2': "",
                    'description_img_data_2': "",
                    'description_img_path_2': "",

                    'description_img_name_3': "",
                    'description_img_data_3': "",
                    'description_img_path_3': "",

                    'test_time': self.ilias_test_duration[int(self.ilias_question_type_sc_question_index[i])],

                    'var_number': "",
                    'question_pool_tag': "",
                    'question_author': self.ilias_question_author[int(self.ilias_question_type_sc_question_index[i])]
                }
            )
            print(str(i+1) + ": SingleChoice: " + str(self.ilias_question_title[int(self.ilias_question_type_sc_question_index[i])]) + " in DB gespeichert")




        # Commit Changes
        connect.commit()

        # Close Connection
        connect.close()

####### Formelfragen
    def read_formelfrage_questions(self):

###########################################   INIT VARIABLES ###########################
        self.ilias_test_question_points = []

        ### Variable - Variablen - INIT
        self.ilias_test_variable1, self.ilias_test_variable1_prec, self.ilias_test_variable1_divby, self.ilias_test_variable1_min, self.ilias_test_variable1_max = [], [], [], [], []
        self.ilias_test_variable2, self.ilias_test_variable2_prec, self.ilias_test_variable2_divby, self.ilias_test_variable2_min, self.ilias_test_variable2_max = [], [], [], [], []
        self.ilias_test_variable3, self.ilias_test_variable3_prec, self.ilias_test_variable3_divby, self.ilias_test_variable3_min, self.ilias_test_variable3_max = [], [], [], [], []
        self.ilias_test_variable4, self.ilias_test_variable4_prec, self.ilias_test_variable4_divby, self.ilias_test_variable4_min, self.ilias_test_variable4_max = [], [], [], [], []
        self.ilias_test_variable5, self.ilias_test_variable5_prec, self.ilias_test_variable5_divby, self.ilias_test_variable5_min, self.ilias_test_variable5_max = [], [], [], [], []
        self.ilias_test_variable6, self.ilias_test_variable6_prec, self.ilias_test_variable6_divby, self.ilias_test_variable6_min, self.ilias_test_variable6_max = [], [], [], [], []
        self.ilias_test_variable7, self.ilias_test_variable7_prec, self.ilias_test_variable7_divby, self.ilias_test_variable7_min, self.ilias_test_variable7_max = [], [], [], [], []
        self.ilias_test_variable8, self.ilias_test_variable8_prec, self.ilias_test_variable8_divby, self.ilias_test_variable8_min, self.ilias_test_variable8_max = [], [], [], [], []
        self.ilias_test_variable9, self.ilias_test_variable9_prec, self.ilias_test_variable9_divby, self.ilias_test_variable9_min, self.ilias_test_variable9_max = [], [], [], [], []
        self.ilias_test_variable10, self.ilias_test_variable10_prec, self.ilias_test_variable10_divby, self.ilias_test_variable10_min, self.ilias_test_variable10_max = [], [], [], [], []

        self.ilias_test_variable1_prec_temp, self.ilias_test_variable1_divby_temp, self.ilias_test_variable1_min_temp, self.ilias_test_variable1_max_temp = [], [], [], []
        self.ilias_test_variable2_prec_temp, self.ilias_test_variable2_divby_temp, self.ilias_test_variable2_min_temp, self.ilias_test_variable2_max_temp = [], [], [], []
        self.ilias_test_variable3_prec_temp, self.ilias_test_variable3_divby_temp, self.ilias_test_variable3_min_temp, self.ilias_test_variable3_max_temp = [], [], [], []
        self.ilias_test_variable4_prec_temp, self.ilias_test_variable4_divby_temp, self.ilias_test_variable4_min_temp, self.ilias_test_variable4_max_temp = [], [], [], []
        self.ilias_test_variable5_prec_temp, self.ilias_test_variable5_divby_temp, self.ilias_test_variable5_min_temp, self.ilias_test_variable5_max_temp = [], [], [], []
        self.ilias_test_variable6_prec_temp, self.ilias_test_variable6_divby_temp, self.ilias_test_variable6_min_temp, self.ilias_test_variable6_max_temp = [], [], [], []
        self.ilias_test_variable7_prec_temp, self.ilias_test_variable7_divby_temp, self.ilias_test_variable7_min_temp, self.ilias_test_variable7_max_temp = [], [], [], []
        self.ilias_test_variable8_prec_temp, self.ilias_test_variable8_divby_temp, self.ilias_test_variable8_min_temp, self.ilias_test_variable8_max_temp = [], [], [], []
        self.ilias_test_variable9_prec_temp, self.ilias_test_variable9_divby_temp, self.ilias_test_variable9_min_temp, self.ilias_test_variable9_max_temp = [], [], [], []
        self.ilias_test_variable10_prec_temp, self.ilias_test_variable10_divby_temp, self.ilias_test_variable10_min_temp, self.ilias_test_variable10_max_temp = [], [], [], []

        self.ilias_test_variable1_settings, self.ilias_test_variable1_settings_temp = [], []
        self.ilias_test_variable2_settings, self.ilias_test_variable2_settings_temp = [], []
        self.ilias_test_variable3_settings, self.ilias_test_variable3_settings_temp = [], []
        self.ilias_test_variable4_settings, self.ilias_test_variable4_settings_temp = [], []
        self.ilias_test_variable5_settings, self.ilias_test_variable5_settings_temp = [], []
        self.ilias_test_variable6_settings, self.ilias_test_variable6_settings_temp = [], []
        self.ilias_test_variable7_settings, self.ilias_test_variable7_settings_temp = [], []
        self.ilias_test_variable8_settings, self.ilias_test_variable8_settings_temp = [], []
        self.ilias_test_variable9_settings, self.ilias_test_variable9_settings_temp = [], []
        self.ilias_test_variable10_settings, self.ilias_test_variable10_settings_temp = [], []

        ### Ergebnisse - Variablen - INIT
        self.ilias_test_result1, self.ilias_test_result1_prec, self.ilias_test_result1_tol, self.ilias_test_result1_min, self.ilias_test_result1_max, self.ilias_test_result1_pts, self.ilias_test_result1_formula = [], [], [], [], [], [], []
        self.ilias_test_result2, self.ilias_test_result2_prec, self.ilias_test_result2_tol, self.ilias_test_result2_min, self.ilias_test_result2_max, self.ilias_test_result2_pts, self.ilias_test_result2_formula = [], [], [], [], [], [], []
        self.ilias_test_result3, self.ilias_test_result3_prec, self.ilias_test_result3_tol, self.ilias_test_result3_min, self.ilias_test_result3_max, self.ilias_test_result3_pts, self.ilias_test_result3_formula = [], [], [], [], [], [], []
        self.ilias_test_result4, self.ilias_test_result4_prec, self.ilias_test_result4_tol, self.ilias_test_result4_min, self.ilias_test_result4_max, self.ilias_test_result4_pts, self.ilias_test_result4_formula = [], [], [], [], [], [], []
        self.ilias_test_result5, self.ilias_test_result5_prec, self.ilias_test_result5_tol, self.ilias_test_result5_min, self.ilias_test_result5_max, self.ilias_test_result5_pts, self.ilias_test_result5_formula = [], [], [], [], [], [], []
        self.ilias_test_result6, self.ilias_test_result6_prec, self.ilias_test_result6_tol, self.ilias_test_result6_min, self.ilias_test_result6_max, self.ilias_test_result6_pts, self.ilias_test_result6_formula = [], [], [], [], [], [], []
        self.ilias_test_result7, self.ilias_test_result7_prec, self.ilias_test_result7_tol, self.ilias_test_result7_min, self.ilias_test_result7_max, self.ilias_test_result7_pts, self.ilias_test_result7_formula = [], [], [], [], [], [], []
        self.ilias_test_result8, self.ilias_test_result8_prec, self.ilias_test_result8_tol, self.ilias_test_result8_min, self.ilias_test_result8_max, self.ilias_test_result8_pts, self.ilias_test_result8_formula = [], [], [], [], [], [], []
        self.ilias_test_result9, self.ilias_test_result9_prec, self.ilias_test_result9_tol, self.ilias_test_result9_min, self.ilias_test_result9_max, self.ilias_test_result9_pts, self.ilias_test_result9_formula = [], [], [], [], [], [], []
        self.ilias_test_result10, self.ilias_test_result10_prec, self.ilias_test_result10_tol, self.ilias_test_result10_min, self.ilias_test_result10_max, self.ilias_test_result10_pts, self.ilias_test_result10_formula = [], [], [], [], [], [], []

        self.ilias_test_result1_temp, self.ilias_test_result1_prec_temp, self.ilias_test_result1_tol_temp, self.ilias_test_result1_min_temp, self.ilias_test_result1_max_temp, self.ilias_test_result1_pts_temp, self.ilias_test_result1_formula_temp = [], [], [], [], [], [], []
        self.ilias_test_result2_temp, self.ilias_test_result2_prec_temp, self.ilias_test_result2_tol_temp, self.ilias_test_result2_min_temp, self.ilias_test_result2_max_temp, self.ilias_test_result2_pts_temp, self.ilias_test_result2_formula_temp = [], [], [], [], [], [], []
        self.ilias_test_result3_temp, self.ilias_test_result3_prec_temp, self.ilias_test_result3_tol_temp, self.ilias_test_result3_min_temp, self.ilias_test_result3_max_temp, self.ilias_test_result3_pts_temp, self.ilias_test_result3_formula_temp = [], [], [], [], [], [], []
        self.ilias_test_result4_temp, self.ilias_test_result4_prec_temp, self.ilias_test_result4_tol_temp, self.ilias_test_result4_min_temp, self.ilias_test_result4_max_temp, self.ilias_test_result4_pts_temp, self.ilias_test_result4_formula_temp = [], [], [], [], [], [], []
        self.ilias_test_result5_temp, self.ilias_test_result5_prec_temp, self.ilias_test_result5_tol_temp, self.ilias_test_result5_min_temp, self.ilias_test_result5_max_temp, self.ilias_test_result5_pts_temp, self.ilias_test_result5_formula_temp = [], [], [], [], [], [], []
        self.ilias_test_result6_temp, self.ilias_test_result6_prec_temp, self.ilias_test_result6_tol_temp, self.ilias_test_result6_min_temp, self.ilias_test_result6_max_temp, self.ilias_test_result6_pts_temp, self.ilias_test_result6_formula_temp = [], [], [], [], [], [], []
        self.ilias_test_result7_temp, self.ilias_test_result7_prec_temp, self.ilias_test_result7_tol_temp, self.ilias_test_result7_min_temp, self.ilias_test_result7_max_temp, self.ilias_test_result7_pts_temp, self.ilias_test_result7_formula_temp = [], [], [], [], [], [], []
        self.ilias_test_result8_temp, self.ilias_test_result8_prec_temp, self.ilias_test_result8_tol_temp, self.ilias_test_result8_min_temp, self.ilias_test_result8_max_temp, self.ilias_test_result8_pts_temp, self.ilias_test_result8_formula_temp = [], [], [], [], [], [], []
        self.ilias_test_result9_temp, self.ilias_test_result9_prec_temp, self.ilias_test_result9_tol_temp, self.ilias_test_result9_min_temp, self.ilias_test_result9_max_temp, self.ilias_test_result9_pts_temp, self.ilias_test_result9_formula_temp = [], [], [], [], [], [], []
        self.ilias_test_result10_temp, self.ilias_test_result10_prec_temp, self.ilias_test_result10_tol_temp, self.ilias_test_result10_min_temp, self.ilias_test_result10_max_temp, self.ilias_test_result10_pts_temp, self.ilias_test_result10_formula_temp = [], [], [], [], [], [], []


        self.ilias_test_result1_settings, self.ilias_test_result1_settings_temp = [], []
        self.ilias_test_result2_settings, self.ilias_test_result2_settings_temp = [], []
        self.ilias_test_result3_settings, self.ilias_test_result3_settings_temp = [], []
        self.ilias_test_result4_settings, self.ilias_test_result4_settings_temp = [], []
        self.ilias_test_result5_settings, self.ilias_test_result5_settings_temp = [], []
        self.ilias_test_result6_settings, self.ilias_test_result6_settings_temp = [], []
        self.ilias_test_result7_settings, self.ilias_test_result7_settings_temp = [], []
        self.ilias_test_result8_settings, self.ilias_test_result8_settings_temp = [], []
        self.ilias_test_result9_settings, self.ilias_test_result9_settings_temp = [], []
        self.ilias_test_result10_settings, self.ilias_test_result10_settings_temp = [], []




        self.ilias_question_type_ff_question_index = []

        self.variables_collection_string = ""
        self.result_collection_string = ""
        self.variables_collection_list = []
        self.result_collection_list = []

################################ VARIABLEN FÜLLEN AUS XML DATEI #########################
        for qtimetadatafield in self.myroot.iter('qtimetadatafield'):

            # "$" Zeichen werden eingefügt wenn eine neue Frage gefunden wird ("assFormuaQuestion")
            # Später wird der String an den "$" getrennt um die Variablen pro Frage anzuzeigen
            if qtimetadatafield.find('fieldentry').text == "assFormulaQuestion":
                self.variables_collection_string += '$'
                self.result_collection_string += '$'

            #if qtimetadatafield.find('fieldlabel').text == "QUESTIONTYPE":
            #    self.ilias_question_type.append(qtimetadatafield.find('fieldentry').text)

            if qtimetadatafield.find('fieldlabel').text == "points":
                self.ilias_test_question_points.append(qtimetadatafield.find('fieldentry').text)

            if qtimetadatafield.find('fieldlabel').text == "$v1":
                self.ilias_test_variable1.append(qtimetadatafield.find('fieldentry').text)
                self.variables_collection_string += 'v1'

            if qtimetadatafield.find('fieldlabel').text == "$v2":
                self.ilias_test_variable2.append(qtimetadatafield.find('fieldentry').text)
                self.variables_collection_string += 'v2'

            if qtimetadatafield.find('fieldlabel').text == "$v3":
                self.ilias_test_variable3.append(qtimetadatafield.find('fieldentry').text)
                self.variables_collection_string += 'v3'

            if qtimetadatafield.find('fieldlabel').text == "$v4":
                self.ilias_test_variable4.append(qtimetadatafield.find('fieldentry').text)
                self.variables_collection_string += 'v4'

            if qtimetadatafield.find('fieldlabel').text == "$v5":
                self.ilias_test_variable5.append(qtimetadatafield.find('fieldentry').text)
                self.variables_collection_string += 'v5'

            if qtimetadatafield.find('fieldlabel').text == "$v6":
                self.ilias_test_variable6.append(qtimetadatafield.find('fieldentry').text)
                self.variables_collection_string += 'v6'

            if qtimetadatafield.find('fieldlabel').text == "$v7":
                self.ilias_test_variable7.append(qtimetadatafield.find('fieldentry').text)
                self.variables_collection_string += 'v7'

            if qtimetadatafield.find('fieldlabel').text == "$v8":
                self.ilias_test_variable8.append(qtimetadatafield.find('fieldentry').text)
                self.variables_collection_string += 'v8'

            if qtimetadatafield.find('fieldlabel').text == "$v9":
                self.ilias_test_variable9.append(qtimetadatafield.find('fieldentry').text)
                self.variables_collection_string += 'v9'

            if qtimetadatafield.find('fieldlabel').text == "$v10":
                self.ilias_test_variable10.append(qtimetadatafield.find('fieldentry').text)
                self.variables_collection_string += 'v10'

            if qtimetadatafield.find('fieldlabel').text == "$r1":
                self.ilias_test_result1.append(qtimetadatafield.find('fieldentry').text)
                self.result_collection_string += 'r1'

            if qtimetadatafield.find('fieldlabel').text == "$r2":
                self.ilias_test_result2.append(qtimetadatafield.find('fieldentry').text)
                self.result_collection_string += 'r2'

            if qtimetadatafield.find('fieldlabel').text == "$r3":
                self.ilias_test_result3.append(qtimetadatafield.find('fieldentry').text)
                self.result_collection_string += 'r3'

            if qtimetadatafield.find('fieldlabel').text == "$r4":
                self.ilias_test_result4.append(qtimetadatafield.find('fieldentry').text)
                self.result_collection_string += 'r4'

            if qtimetadatafield.find('fieldlabel').text == "$r5":
                self.ilias_test_result5.append(qtimetadatafield.find('fieldentry').text)
                self.result_collection_string += 'r5'

            if qtimetadatafield.find('fieldlabel').text == "$r6":
                self.ilias_test_result6.append(qtimetadatafield.find('fieldentry').text)
                self.result_collection_string += 'r6'

            if qtimetadatafield.find('fieldlabel').text == "$r7":
                self.ilias_test_result7.append(qtimetadatafield.find('fieldentry').text)
                self.result_collection_string += 'r7'

            if qtimetadatafield.find('fieldlabel').text == "$r8":
                self.ilias_test_result8.append(qtimetadatafield.find('fieldentry').text)
                self.result_collection_string += 'r8'

            if qtimetadatafield.find('fieldlabel').text == "$r9":
                self.ilias_test_result9.append(qtimetadatafield.find('fieldentry').text)
                self.result_collection_string += 'r9'

            if qtimetadatafield.find('fieldlabel').text == "$r10":
                self.ilias_test_result10.append(qtimetadatafield.find('fieldentry').text)
                self.result_collection_string += 'r10'

        #### XML durchsuchen und Fragentyp (FF,SC,MC,MQ) nach "Formelfrage" durchsuchen
        #### assFormulaQuestion ist vom ilias codiert für "Formelfrage"
        for i in range(len(self.ilias_question_type)):
            if self.ilias_question_type[i] == "assFormulaQuestion":
                self.ilias_question_type_ff_question_index.append(str(i))



        # Liste Variable 1 - Werte auftrennen nach ";"
        # Der Eintrag für die "Settings" einer Variablen in der XML Datei sieht wie folgt aus:
        # <fieldentry>a:6:{s:9:"precision";i:1;s:12:"intprecision";  s:1:"1";s:8:"rangemin";  d:1;s:8:"rangemax";  d:10;s:4:"unit";  s:0:"";s:9:"unitvalue";s:0:"";  }</fieldentry>




        for i in range(len(self.ilias_test_variable1)):
            self.ilias_test_variable1_settings += self.ilias_test_variable1[i].split(";")

        for i in range(len(self.ilias_test_variable2)):
            self.ilias_test_variable2_settings += self.ilias_test_variable2[i].split(";")

        for i in range(len(self.ilias_test_variable3)):
            self.ilias_test_variable3_settings += self.ilias_test_variable3[i].split(";")

        for i in range(len(self.ilias_test_variable4)):
            self.ilias_test_variable4_settings += self.ilias_test_variable4[i].split(";")

        for i in range(len(self.ilias_test_variable5)):
            self.ilias_test_variable5_settings += self.ilias_test_variable5[i].split(";")

        for i in range(len(self.ilias_test_variable6)):
            self.ilias_test_variable6_settings += self.ilias_test_variable6[i].split(";")

        for i in range(len(self.ilias_test_variable7)):
            self.ilias_test_variable7_settings += self.ilias_test_variable7[i].split(";")

        for i in range(len(self.ilias_test_variable8)):
            self.ilias_test_variable8_settings += self.ilias_test_variable8[i].split(";")

        for i in range(len(self.ilias_test_variable9)):
            self.ilias_test_variable9_settings += self.ilias_test_variable9[i].split(";")

        for i in range(len(self.ilias_test_variable10)):
            self.ilias_test_variable10_settings += self.ilias_test_variable10[i].split(";")



        for i in range(len(self.ilias_test_result1)):
            self.ilias_test_result1_settings += self.ilias_test_result1[i].split(";")

        for i in range(len(self.ilias_test_result2)):
            self.ilias_test_result2_settings += self.ilias_test_result2[i].split(";")

        for i in range(len(self.ilias_test_result3)):
            self.ilias_test_result3_settings += self.ilias_test_result3[i].split(";")

        for i in range(len(self.ilias_test_result4)):
            self.ilias_test_result4_settings += self.ilias_test_result4[i].split(";")

        for i in range(len(self.ilias_test_result5)):
            self.ilias_test_result5_settings += self.ilias_test_result5[i].split(";")

        for i in range(len(self.ilias_test_result6)):
            self.ilias_test_result6_settings += self.ilias_test_result6[i].split(";")

        for i in range(len(self.ilias_test_result7)):
            self.ilias_test_result7_settings += self.ilias_test_result7[i].split(";")

        for i in range(len(self.ilias_test_result8)):
            self.ilias_test_result8_settings += self.ilias_test_result8[i].split(";")

        for i in range(len(self.ilias_test_result9)):
            self.ilias_test_result9_settings += self.ilias_test_result9[i].split(";")

        for i in range(len(self.ilias_test_result10)):
            self.ilias_test_result10_settings += self.ilias_test_result10[i].split(";")




        # Lösche Fach 12 und danach jedes 13te Feld
        # Diese Felder enthalten keine Informationen. Der String schließt mit "unitvalue";s:0:"";} ab und die gelöschten Felder
        # enthalten den "Wert zwischen ; und } und sind unbrauchbar.
        del self.ilias_test_variable1_settings[12::13]
        del self.ilias_test_variable2_settings[12::13]
        del self.ilias_test_variable3_settings[12::13]
        del self.ilias_test_variable4_settings[12::13]
        del self.ilias_test_variable5_settings[12::13]
        del self.ilias_test_variable6_settings[12::13]
        del self.ilias_test_variable7_settings[12::13]
        del self.ilias_test_variable8_settings[12::13]
        del self.ilias_test_variable9_settings[12::13]
        del self.ilias_test_variable10_settings[12::13]


        # Erstes Feld löschen, dann enthält jedes 2. Fach der eigentliche Wert für die jeweilige Einstellung z.B. Präzision
        if len(self.ilias_test_variable1_settings) > 0:
            self.ilias_test_variable1_settings.pop(0)

        if len(self.ilias_test_variable2_settings) > 0:
            self.ilias_test_variable2_settings.pop(0)

        if len(self.ilias_test_variable3_settings) > 0:
            self.ilias_test_variable3_settings.pop(0)

        if len(self.ilias_test_variable4_settings) > 0:
            self.ilias_test_variable4_settings.pop(0)

        if len(self.ilias_test_variable5_settings) > 0:
            self.ilias_test_variable5_settings.pop(0)

        if len(self.ilias_test_variable6_settings) > 0:
            self.ilias_test_variable6_settings.pop(0)

        if len(self.ilias_test_variable7_settings) > 0:
            self.ilias_test_variable7_settings.pop(0)

        if len(self.ilias_test_variable8_settings) > 0:
            self.ilias_test_variable8_settings.pop(0)

        if len(self.ilias_test_variable9_settings) > 0:
            self.ilias_test_variable9_settings.pop(0)

        if len(self.ilias_test_variable10_settings) > 0:
            self.ilias_test_variable10_settings.pop(0)

        # jedes 2. Fach enthält den eigentlichen Wert für die jeweilige Einstellung z.B. Präzision
        # die
        self.ilias_test_variable1_settings_temp = self.ilias_test_variable1_settings[::2]
        self.ilias_test_variable2_settings_temp = self.ilias_test_variable2_settings[::2]
        self.ilias_test_variable3_settings_temp = self.ilias_test_variable3_settings[::2]
        self.ilias_test_variable4_settings_temp = self.ilias_test_variable4_settings[::2]
        self.ilias_test_variable5_settings_temp = self.ilias_test_variable5_settings[::2]
        self.ilias_test_variable6_settings_temp = self.ilias_test_variable6_settings[::2]
        self.ilias_test_variable7_settings_temp = self.ilias_test_variable7_settings[::2]
        self.ilias_test_variable8_settings_temp = self.ilias_test_variable8_settings[::2]
        self.ilias_test_variable9_settings_temp = self.ilias_test_variable9_settings[::2]
        self.ilias_test_variable10_settings_temp = self.ilias_test_variable10_settings[::2]


        self.variables_collection_list = self.variables_collection_string.split('$')
        self.variables_collection_list.pop(0)
        self.result_collection_list = self.result_collection_string.split('$')
        self.result_collection_list.pop(0)

        self.var1_count = 0
        self.var2_count = 0
        self.var3_count = 0
        self.var4_count = 0
        self.var5_count = 0
        self.var6_count = 0
        self.var7_count = 0
        self.var8_count = 0
        self.var9_count = 0
        self.var10_count = 0

        self.ilias_test_variable1_prec, self.ilias_test_variable1_divby, self.ilias_test_variable1_min,  self.ilias_test_variable1_max, self.var1_count = Import_ILIAS_Datei_in_DB.append_data_to_var_of_ff_question_type(self, self.var1_count, self.ilias_test_variable1_settings_temp, "v1")
        self.ilias_test_variable2_prec, self.ilias_test_variable2_divby, self.ilias_test_variable2_min,  self.ilias_test_variable2_max, self.var2_count = Import_ILIAS_Datei_in_DB.append_data_to_var_of_ff_question_type(self, self.var2_count, self.ilias_test_variable2_settings_temp, "v2")
        self.ilias_test_variable3_prec, self.ilias_test_variable3_divby, self.ilias_test_variable3_min,  self.ilias_test_variable3_max, self.var3_count = Import_ILIAS_Datei_in_DB.append_data_to_var_of_ff_question_type(self, self.var3_count, self.ilias_test_variable3_settings_temp, "v3")
        self.ilias_test_variable4_prec, self.ilias_test_variable4_divby, self.ilias_test_variable4_min,  self.ilias_test_variable4_max, self.var4_count = Import_ILIAS_Datei_in_DB.append_data_to_var_of_ff_question_type(self, self.var4_count, self.ilias_test_variable4_settings_temp, "v4")
        self.ilias_test_variable5_prec, self.ilias_test_variable5_divby, self.ilias_test_variable5_min,  self.ilias_test_variable5_max, self.var5_count = Import_ILIAS_Datei_in_DB.append_data_to_var_of_ff_question_type(self, self.var5_count, self.ilias_test_variable5_settings_temp, "v5")
        self.ilias_test_variable6_prec, self.ilias_test_variable6_divby, self.ilias_test_variable6_min,  self.ilias_test_variable6_max, self.var6_count = Import_ILIAS_Datei_in_DB.append_data_to_var_of_ff_question_type(self, self.var6_count, self.ilias_test_variable6_settings_temp, "v6")
        self.ilias_test_variable7_prec, self.ilias_test_variable7_divby, self.ilias_test_variable7_min,  self.ilias_test_variable7_max, self.var7_count = Import_ILIAS_Datei_in_DB.append_data_to_var_of_ff_question_type(self, self.var7_count, self.ilias_test_variable7_settings_temp, "v7")
        self.ilias_test_variable8_prec, self.ilias_test_variable8_divby, self.ilias_test_variable8_min,  self.ilias_test_variable8_max, self.var8_count = Import_ILIAS_Datei_in_DB.append_data_to_var_of_ff_question_type(self, self.var8_count, self.ilias_test_variable8_settings_temp, "v8")
        self.ilias_test_variable9_prec, self.ilias_test_variable9_divby, self.ilias_test_variable9_min,  self.ilias_test_variable9_max, self.var9_count = Import_ILIAS_Datei_in_DB.append_data_to_var_of_ff_question_type(self, self.var9_count, self.ilias_test_variable9_settings_temp, "v9")
        self.ilias_test_variable10_prec, self.ilias_test_variable10_divby, self.ilias_test_variable10_min,  self.ilias_test_variable10_max, self.var10_count = Import_ILIAS_Datei_in_DB.append_data_to_var_of_ff_question_type(self, self.var10_count, self.ilias_test_variable10_settings_temp, "v10")



        # Ergebnis String auslesen



        if len(self.ilias_test_result1_settings) > 0:
            self.ilias_test_result1_settings.pop(0)

        if len(self.ilias_test_result2_settings) > 0:
            self.ilias_test_result2_settings.pop(0)

        if len(self.ilias_test_result3_settings) > 0:
            self.ilias_test_result3_settings.pop(0)

        if len(self.ilias_test_result4_settings) > 0:
            self.ilias_test_result4_settings.pop(0)

        if len(self.ilias_test_result5_settings) > 0:
            self.ilias_test_result5_settings.pop(0)

        if len(self.ilias_test_result6_settings) > 0:
            self.ilias_test_result6_settings.pop(0)

        if len(self.ilias_test_result7_settings) > 0:
            self.ilias_test_result7_settings.pop(0)

        if len(self.ilias_test_result8_settings) > 0:
            self.ilias_test_result8_settings.pop(0)

        if len(self.ilias_test_result9_settings) > 0:
            self.ilias_test_result9_settings.pop(0)

        if len(self.ilias_test_result10_settings) > 0:
            self.ilias_test_result10_settings.pop(0)


        self.ilias_test_result1_settings_temp = self.ilias_test_result1_settings[::2]
        self.ilias_test_result2_settings_temp = self.ilias_test_result2_settings[::2]
        self.ilias_test_result3_settings_temp = self.ilias_test_result3_settings[::2]
        self.ilias_test_result4_settings_temp = self.ilias_test_result4_settings[::2]
        self.ilias_test_result5_settings_temp = self.ilias_test_result5_settings[::2]
        self.ilias_test_result6_settings_temp = self.ilias_test_result6_settings[::2]
        self.ilias_test_result7_settings_temp = self.ilias_test_result7_settings[::2]
        self.ilias_test_result8_settings_temp = self.ilias_test_result8_settings[::2]
        self.ilias_test_result9_settings_temp = self.ilias_test_result9_settings[::2]



        for i in range(len(self.ilias_test_result1_settings_temp)):
            self.ilias_test_result1_settings_temp[i] = self.ilias_test_result1_settings_temp[i].replace('"', '')

        for i in range(len(self.ilias_test_result2_settings_temp)):
            self.ilias_test_result2_settings_temp[i] = self.ilias_test_result2_settings_temp[i].replace('"', '')

        for i in range(len(self.ilias_test_result3_settings_temp)):
            self.ilias_test_result3_settings_temp[i] = self.ilias_test_result3_settings_temp[i].replace('"', '')

        for i in range(len(self.ilias_test_result4_settings_temp)):
            self.ilias_test_result4_settings_temp[i] = self.ilias_test_result4_settings_temp[i].replace('"', '')

        for i in range(len(self.ilias_test_result5_settings_temp)):
            self.ilias_test_result5_settings_temp[i] = self.ilias_test_result5_settings_temp[i].replace('"', '')

        for i in range(len(self.ilias_test_result6_settings_temp)):
            self.ilias_test_result6_settings_temp[i] = self.ilias_test_result6_settings_temp[i].replace('"', '')

        for i in range(len(self.ilias_test_result7_settings_temp)):
            self.ilias_test_result7_settings_temp[i] = self.ilias_test_result7_settings_temp[i].replace('"', '')

        for i in range(len(self.ilias_test_result8_settings_temp)):
            self.ilias_test_result8_settings_temp[i] = self.ilias_test_result8_settings_temp[i].replace('"', '')

        for i in range(len(self.ilias_test_result9_settings_temp)):
            self.ilias_test_result9_settings_temp[i] = self.ilias_test_result9_settings_temp[i].replace('"', '')

        for i in range(len(self.ilias_test_result10_settings_temp)):
            self.ilias_test_result10_settings_temp[i] = self.ilias_test_result10_settings_temp[i].replace('"', '')


        self.res1_count = 0
        self.res2_count = 0
        self.res3_count = 0
        self.res4_count = 0
        self.res5_count = 0
        self.res6_count = 0
        self.res7_count = 0
        self.res8_count = 0
        self.res9_count = 0
        self.res10_count = 0

        self.ilias_test_result1_prec, self.ilias_test_result1_tol, self.ilias_test_result1_min,  self.ilias_test_result1_max, self.ilias_test_result1_pts, self.ilias_test_result1_formula, self.res1_count = Import_ILIAS_Datei_in_DB.append_data_to_res_of_ff_question_type(self, self.res1_count, self.ilias_test_result1_settings_temp, "r1")
        self.ilias_test_result2_prec, self.ilias_test_result2_tol, self.ilias_test_result2_min,  self.ilias_test_result2_max, self.ilias_test_result2_pts, self.ilias_test_result2_formula, self.res2_count = Import_ILIAS_Datei_in_DB.append_data_to_res_of_ff_question_type(self, self.res2_count, self.ilias_test_result2_settings_temp, "r2")
        self.ilias_test_result3_prec, self.ilias_test_result3_tol, self.ilias_test_result3_min,  self.ilias_test_result3_max, self.ilias_test_result3_pts, self.ilias_test_result3_formula, self.res3_count = Import_ILIAS_Datei_in_DB.append_data_to_res_of_ff_question_type(self, self.res3_count, self.ilias_test_result3_settings_temp, "r3")
        self.ilias_test_result4_prec, self.ilias_test_result4_tol, self.ilias_test_result4_min,  self.ilias_test_result4_max, self.ilias_test_result4_pts, self.ilias_test_result4_formula, self.res4_count = Import_ILIAS_Datei_in_DB.append_data_to_res_of_ff_question_type(self, self.res4_count, self.ilias_test_result4_settings_temp, "r4")
        self.ilias_test_result5_prec, self.ilias_test_result5_tol, self.ilias_test_result5_min,  self.ilias_test_result5_max, self.ilias_test_result5_pts, self.ilias_test_result5_formula, self.res5_count = Import_ILIAS_Datei_in_DB.append_data_to_res_of_ff_question_type(self, self.res5_count, self.ilias_test_result5_settings_temp, "r5")
        self.ilias_test_result6_prec, self.ilias_test_result6_tol, self.ilias_test_result6_min,  self.ilias_test_result6_max, self.ilias_test_result6_pts, self.ilias_test_result6_formula, self.res6_count = Import_ILIAS_Datei_in_DB.append_data_to_res_of_ff_question_type(self, self.res6_count, self.ilias_test_result6_settings_temp, "r6")
        self.ilias_test_result7_prec, self.ilias_test_result7_tol, self.ilias_test_result7_min,  self.ilias_test_result7_max, self.ilias_test_result7_pts, self.ilias_test_result7_formula, self.res7_count = Import_ILIAS_Datei_in_DB.append_data_to_res_of_ff_question_type(self, self.res7_count, self.ilias_test_result7_settings_temp, "r7")
        self.ilias_test_result8_prec, self.ilias_test_result8_tol, self.ilias_test_result8_min,  self.ilias_test_result8_max, self.ilias_test_result8_pts, self.ilias_test_result8_formula, self.res8_count = Import_ILIAS_Datei_in_DB.append_data_to_res_of_ff_question_type(self, self.res8_count, self.ilias_test_result8_settings_temp, "r8")
        self.ilias_test_result9_prec, self.ilias_test_result9_tol, self.ilias_test_result9_min,  self.ilias_test_result9_max, self.ilias_test_result9_pts, self.ilias_test_result9_formula, self.res9_count = Import_ILIAS_Datei_in_DB.append_data_to_res_of_ff_question_type(self, self.res9_count, self.ilias_test_result9_settings_temp, "r9")
        self.ilias_test_result10_prec, self.ilias_test_result10_tol, self.ilias_test_result10_min,  self.ilias_test_result10_max, self.ilias_test_result10_pts, self.ilias_test_result10_formula, self.res10_count = Import_ILIAS_Datei_in_DB.append_data_to_res_of_ff_question_type(self, self.res10_count, self.ilias_test_result10_settings_temp, "r10")






        self.ilias_question_description_main = Import_ILIAS_Datei_in_DB.split_description_main_from_img(self, self.ilias_question_description_main)

    def append_data_to_var_of_ff_question_type(self, var_count, var_settings_temp, var_id ):
        self.var_prec, self.var_prec_temp = [], []
        self.var_min, self.var_min_temp = [], []
        self.var_max, self.var_max_temp = [], []
        self.var_divby, self.var_divby_temp = [], []
        self.var_formula, self.var_formula_temp = [], []

        self.var_settings_temp = var_settings_temp
        self.var_id = var_id
        self.var_count = var_count


        for i in range(0, len(self.var_settings_temp), 6):
            self.var_prec_temp.append(self.var_settings_temp[i].rsplit(':', 1)[-1])
            self.var_divby_temp.append(self.var_settings_temp[i + 1][5:][:-1])
            self.var_min_temp.append(self.var_settings_temp[i + 2].rsplit(':', 1)[-1])
            self.var_max_temp.append(self.var_settings_temp[i + 3].rsplit(':', 1)[-1])

        for i in range(len(self.variables_collection_list)):
            if self.var_id in self.variables_collection_list[i]:
                self.var_prec.append(self.var_prec_temp[self.var_count])
                self.var_divby.append(self.var_divby_temp[self.var_count])
                self.var_min.append(self.var_min_temp[self.var_count])
                self.var_max.append(self.var_max_temp[self.var_count])
                self.var_count = self.var_count + 1

            else:
                self.var_prec.append(" ")
                self.var_divby.append(" ")
                self.var_min.append(" ")
                self.var_max.append(" ")

        return self.var_prec, self.var_divby, self.var_min, self.var_max, self.var_count

    def append_data_to_res_of_ff_question_type(self, res_count, res_settings_temp, res_id):




        self.res_prec, self.res_prec_temp = [], []
        self.res_tol, self.res_tol_temp = [], []
        self.res_min, self.res_min_temp = [], []
        self.res_max, self.res_max_temp = [], []
        self.res_pts, self.res_pts_temp = [], []
        self.res_formula, self.res_formula_temp = [], []

        self.res_settings_temp = res_settings_temp
        self.res_id = res_id
        self.res_count = res_count


        for i in range(0, len(self.res_settings_temp), 10):
            self.res_prec_temp.append(self.res_settings_temp[i].rsplit(':', 1)[-1])
            self.res_tol_temp.append(self.res_settings_temp[i + 1].rsplit(':', 1)[-1])
            self.res_min_temp.append(self.res_settings_temp[i + 2].rsplit(':', 1)[-1])
            self.res_max_temp.append(self.res_settings_temp[i + 3].rsplit(':', 1)[-1])
            self.res_pts_temp.append(self.res_settings_temp[i + 4].rsplit(':', 1)[-1])
            self.res_formula_temp.append(self.res_settings_temp[i + 5].rsplit(':', 1)[-1])

        for i in range(len(self.result_collection_list)):
            if self.res_id in self.result_collection_list[i]:
                self.res_prec.append(self.res_prec_temp[self.res_count])
                self.res_tol.append(self.res_tol_temp[self.res_count])
                self.res_min.append(self.res_min_temp[self.res_count])
                self.res_max.append(self.res_max_temp[self.res_count])
                self.res_pts.append(self.res_pts_temp[self.res_count])
                self.res_formula.append(self.res_formula_temp[self.res_count])
                self.res_count = self.res_count + 1

            else:
                self.res_prec.append(" ")
                self.res_tol.append(" ")
                self.res_min.append(" ")
                self.res_max.append(" ")
                self.res_pts.append(" ")
                self.res_formula.append(" ")


        return self.res_prec, self.res_tol, self.res_min, self.res_max, self.res_pts, self.res_formula, self.res_count

    def write_data_to_database_ff(self):

        print("_______________________________________________")

        # Create a database or connect to one
        connect = sqlite3.connect(self.database_formelfrage_path)

        # Create cursor
        cursor = connect.cursor()

        for i in range(len(self.ilias_question_type_ff_question_index)):

            # Bilder der Reihe nach einlesen
            if self.ilias_test_question_description_image_uri_1[i] != "EMPTY":

                with open(os.path.normpath(os.path.join(self.select_test_import_file, self.ilias_test_question_description_image_uri_1[i])), 'rb') as image_file:
                    self.ilias_test_question_description_image_data_1.append(image_file.read())

            else:
                self.ilias_test_question_description_image_data_1.append("EMPTY")


            # Create table
            cursor.execute(
                    "INSERT INTO formelfrage_table VALUES ("
                    ":question_difficulty, :question_category, :question_type, "
                    ":question_title, :question_description_title, :question_description_main, "
                    ":res1_formula, :res2_formula, :res3_formula,  "
                    ":res4_formula, :res5_formula, :res6_formula,  "
                    ":res7_formula, :res8_formula, :res9_formula, :res10_formula, "
                    ":var1_name, :var1_min, :var1_max, :var1_prec, :var1_divby, :var1_unit, "
                    ":var2_name, :var2_min, :var2_max, :var2_prec, :var2_divby, :var2_unit, "
                    ":var3_name, :var3_min, :var3_max, :var3_prec, :var3_divby, :var3_unit, "
                    ":var4_name, :var4_min, :var4_max, :var4_prec, :var4_divby, :var4_unit, "
                    ":var5_name, :var5_min, :var5_max, :var5_prec, :var5_divby, :var5_unit, "
                    ":var6_name, :var6_min, :var6_max, :var6_prec, :var6_divby, :var6_unit, "
                    ":var7_name, :var7_min, :var7_max, :var7_prec, :var7_divby, :var7_unit, "
                    ":var8_name, :var8_min, :var8_max, :var8_prec, :var8_divby, :var8_unit, "
                    ":var9_name, :var9_min, :var9_max, :var9_prec, :var9_divby, :var9_unit, "
                    ":var10_name, :var10_min, :var10_max, :var10_prec, :var10_divby, :var10_unit, "
                    ":var11_name, :var11_min, :var11_max, :var11_prec, :var11_divby, :var11_unit, "
                    ":var12_name, :var12_min, :var12_max, :var12_prec, :var12_divby, :var12_unit, "
                    ":var13_name, :var13_min, :var13_max, :var13_prec, :var13_divby, :var13_unit, "
                    ":var14_name, :var14_min, :var14_max, :var14_prec, :var14_divby, :var14_unit, "
                    ":var15_name, :var15_min, :var15_max, :var15_prec, :var15_divby, :var15_unit, "
                    ":res1_name, :res1_min, :res1_max, :res1_prec, :res1_tol, :res1_points, :res1_unit, "
                    ":res2_name, :res2_min, :res2_max, :res2_prec, :res2_tol, :res2_points, :res2_unit, "
                    ":res3_name, :res3_min, :res3_max, :res3_prec, :res3_tol, :res3_points, :res3_unit,"
                    ":res4_name, :res4_min, :res4_max, :res4_prec, :res4_tol, :res4_points, :res4_unit, "
                    ":res5_name, :res5_min, :res5_max, :res5_prec, :res5_tol, :res5_points, :res5_unit, "
                    ":res6_name, :res6_min, :res6_max, :res6_prec, :res6_tol, :res6_points, :res6_unit, "
                    ":res7_name, :res7_min, :res7_max, :res7_prec, :res7_tol, :res7_points, :res7_unit, "
                    ":res8_name, :res8_min, :res8_max, :res8_prec, :res8_tol, :res8_points, :res8_unit, "
                    ":res9_name, :res9_min, :res9_max, :res9_prec, :res9_tol, :res9_points, :res9_unit, "
                    ":res10_name, :res10_min, :res10_max, :res10_prec, :res10_tol, :res10_points, :res10_unit, "
                    ":description_img_name_1, :description_img_data_1, :description_img_path_1, "
                    ":description_img_name_2, :description_img_data_2, :description_img_path_2, "
                    ":description_img_name_3, :description_img_data_3, :description_img_path_3, "
                    ":test_time, :var_number, :res_number, :question_pool_tag, :question_author)",
                    {
                        'question_difficulty': "",
                        'question_category':  "",
                        'question_type': "Formelfrage",

                        'question_title': self.ilias_question_title[int(self.ilias_question_type_ff_question_index[i])],
                        'question_description_title': self.ilias_question_description_title[int(self.ilias_question_type_ff_question_index[i])],
                        'question_description_main': self.ilias_question_description_main[int(self.ilias_question_type_ff_question_index[i])],

                        'res1_formula': self.ilias_test_result1_formula[i],
                        'res2_formula': self.ilias_test_result2_formula[i],
                        'res3_formula': self.ilias_test_result3_formula[i],
                        'res4_formula': self.ilias_test_result4_formula[i],
                        'res5_formula': self.ilias_test_result5_formula[i],
                        'res6_formula': self.ilias_test_result6_formula[i],
                        'res7_formula': self.ilias_test_result7_formula[i],
                        'res8_formula': self.ilias_test_result8_formula[i],
                        'res9_formula': self.ilias_test_result9_formula[i],
                        'res10_formula': self.ilias_test_result10_formula[i],

                        'var1_name':  "",
                        'var1_min': self.ilias_test_variable1_min[i],
                        'var1_max': self.ilias_test_variable1_max[i],
                        'var1_prec': self.ilias_test_variable1_prec[i],
                        'var1_divby': self.ilias_test_variable1_divby[i],
                        'var1_unit': "",

                        'var2_name':  "",
                        'var2_min': self.ilias_test_variable2_min[i],
                        'var2_max': self.ilias_test_variable2_max[i],
                        'var2_prec': self.ilias_test_variable2_prec[i],
                        'var2_divby': self.ilias_test_variable2_divby[i],
                        'var2_unit':  "",

                        'var3_name':  "",
                        'var3_min': self.ilias_test_variable3_min[i],
                        'var3_max': self.ilias_test_variable3_max[i],
                        'var3_prec': self.ilias_test_variable3_prec[i],
                        'var3_divby': self.ilias_test_variable3_divby[i],
                        'var3_unit':  "",

                        'var4_name':  "",
                        'var4_min': self.ilias_test_variable4_min[i],
                        'var4_max': self.ilias_test_variable4_max[i],
                        'var4_prec': self.ilias_test_variable4_prec[i],
                        'var4_divby': self.ilias_test_variable4_divby[i],
                        'var4_unit':  "",

                        'var5_name':  "",
                        'var5_min': self.ilias_test_variable5_min[i],
                        'var5_max': self.ilias_test_variable5_max[i],
                        'var5_prec': self.ilias_test_variable5_prec[i],
                        'var5_divby': self.ilias_test_variable5_divby[i],
                        'var5_unit': "",

                        'var6_name':  "",
                        'var6_min': self.ilias_test_variable6_min[i],
                        'var6_max': self.ilias_test_variable6_max[i],
                        'var6_prec': self.ilias_test_variable6_prec[i],
                        'var6_divby': self.ilias_test_variable6_divby[i],
                        'var6_unit':  "",

                        'var7_name':  "",
                        'var7_min': self.ilias_test_variable7_min[i],
                        'var7_max': self.ilias_test_variable7_max[i],
                        'var7_prec': self.ilias_test_variable7_prec[i],
                        'var7_divby': self.ilias_test_variable7_divby[i],
                        'var7_unit':  "",

                        'var8_name':  "",
                        'var8_min': self.ilias_test_variable8_min[i],
                        'var8_max': self.ilias_test_variable8_max[i],
                        'var8_prec': self.ilias_test_variable8_prec[i],
                        'var8_divby': self.ilias_test_variable8_divby[i],
                        'var8_unit':  "",

                        'var9_name':  "",
                        'var9_min': self.ilias_test_variable9_min[i],
                        'var9_max': self.ilias_test_variable9_max[i],
                        'var9_prec': self.ilias_test_variable9_prec[i],
                        'var9_divby': self.ilias_test_variable9_divby[i],
                        'var9_unit':  "",

                        'var10_name':  "",
                        'var10_min': self.ilias_test_variable10_min[i],
                        'var10_max': self.ilias_test_variable10_max[i],
                        'var10_prec': self.ilias_test_variable10_prec[i],
                        'var10_divby': self.ilias_test_variable10_divby[i],
                        'var10_unit':  "",

                        'var11_name': "",
                        'var11_min': "",
                        'var11_max': "",
                        'var11_prec': "",
                        'var11_divby': "",
                        'var11_unit': "",

                        'var12_name': "",
                        'var12_min': "",
                        'var12_max': "",
                        'var12_prec': "",
                        'var12_divby': "",
                        'var12_unit': "",

                        'var13_name': "",
                        'var13_min': "",
                        'var13_max': "",
                        'var13_prec': "",
                        'var13_divby': "",
                        'var13_unit': "",

                        'var14_name': "",
                        'var14_min': "",
                        'var14_max': "",
                        'var14_prec': "",
                        'var14_divby': "",
                        'var14_unit': "",

                        'var15_name': "",
                        'var15_min': "",
                        'var15_max': "",
                        'var15_prec': "",
                        'var15_divby': "",
                        'var15_unit': "",

                        'res1_name':  "",
                        'res1_min': self.ilias_test_result1_min[i],
                        'res1_max': self.ilias_test_result1_max[i],
                        'res1_prec': self.ilias_test_result1_prec[i],
                        'res1_tol': self.ilias_test_result1_tol[i],
                        'res1_points': self.ilias_test_result1_pts[i],
                        'res1_unit': "",

                        'res2_name':  "",
                        'res2_min': self.ilias_test_result2_min[i],
                        'res2_max': self.ilias_test_result2_max[i],
                        'res2_prec': self.ilias_test_result2_prec[i],
                        'res2_tol': self.ilias_test_result2_tol[i],
                        'res2_points': self.ilias_test_result2_pts[i],
                        'res2_unit':  "",

                        'res3_name':  "",
                        'res3_min': self.ilias_test_result3_min[i],
                        'res3_max': self.ilias_test_result3_max[i],
                        'res3_prec': self.ilias_test_result3_prec[i],
                        'res3_tol': self.ilias_test_result3_tol[i],
                        'res3_points': self.ilias_test_result3_pts[i],
                        'res3_unit':  "",

                        'res4_name':  "",
                        'res4_min': self.ilias_test_result4_min[i],
                        'res4_max': self.ilias_test_result4_max[i],
                        'res4_prec': self.ilias_test_result4_prec[i],
                        'res4_tol': self.ilias_test_result4_tol[i],
                        'res4_points': self.ilias_test_result4_pts[i],
                        'res4_unit':  "",

                        'res5_name':  "",
                        'res5_min': self.ilias_test_result5_min[i],
                        'res5_max': self.ilias_test_result5_max[i],
                        'res5_prec': self.ilias_test_result5_prec[i],
                        'res5_tol': self.ilias_test_result5_tol[i],
                        'res5_points': self.ilias_test_result5_pts[i],
                        'res5_unit':  "",

                        'res6_name':  "",
                        'res6_min': self.ilias_test_result6_min[i],
                        'res6_max': self.ilias_test_result6_max[i],
                        'res6_prec': self.ilias_test_result6_prec[i],
                        'res6_tol': self.ilias_test_result6_tol[i],
                        'res6_points': self.ilias_test_result6_pts[i],
                        'res6_unit':  "",

                        'res7_name':  "",
                        'res7_min': self.ilias_test_result7_min[i],
                        'res7_max': self.ilias_test_result7_max[i],
                        'res7_prec': self.ilias_test_result7_prec[i],
                        'res7_tol': self.ilias_test_result7_tol[i],
                        'res7_points': self.ilias_test_result7_pts[i],
                        'res7_unit':  "",

                        'res8_name':  "",
                        'res8_min': self.ilias_test_result8_min[i],
                        'res8_max': self.ilias_test_result8_max[i],
                        'res8_prec': self.ilias_test_result8_prec[i],
                        'res8_tol': self.ilias_test_result8_tol[i],
                        'res8_points': self.ilias_test_result8_pts[i],
                        'res8_unit':  "",

                        'res9_name':  "",
                        'res9_min': self.ilias_test_result9_min[i],
                        'res9_max': self.ilias_test_result9_max[i],
                        'res9_prec': self.ilias_test_result9_prec[i],
                        'res9_tol': self.ilias_test_result9_tol[i],
                        'res9_points': self.ilias_test_result9_pts[i],
                        'res9_unit':  "",

                        'res10_name':  "",
                        'res10_min': self.ilias_test_result10_min[i],
                        'res10_max': self.ilias_test_result10_max[i],
                        'res10_prec': self.ilias_test_result10_prec[i],
                        'res10_tol': self.ilias_test_result10_tol[i],
                        'res10_points': self.ilias_test_result10_pts[i],
                        'res10_unit':  "",

                        'description_img_name_1': self.ilias_test_question_description_image_name_1[i],
                        'description_img_data_1': self.ilias_test_question_description_image_data_1[i],
                        'description_img_path_1': self.ilias_test_question_description_image_uri_1[i],

                        'description_img_name_2': "",
                        'description_img_data_2': "",
                        'description_img_path_2': "",

                        'description_img_name_3': "",
                        'description_img_data_3': "",
                        'description_img_path_3': "",

                        'test_time':  self.ilias_test_duration[int(self.ilias_question_type_ff_question_index[i])],

                        'var_number':  "",
                        'res_number':  "",
                        'question_pool_tag':  "",
                        'question_author': self.ilias_question_author[int(self.ilias_question_type_ff_question_index[i])]
                    }
            )
            print(str(i+1) + ": Formelfrage: " + str(self.ilias_question_title[int(self.ilias_question_type_ff_question_index[i])]) + " in DB gespeichert")

        # Commit Changes
        connect.commit()

        # Close Connection
        connect.close()

####### Multiple Choice Fragen
    def read_multiplechoice_questions(self):

        # MULTIPLE CHOICE Antworten
        for response_lid in self.myroot.iter('response_lid'):
            if response_lid.attrib.get('ident') == "MCMR":    #MR -> Multiple Choice
                for render_choice in response_lid.iter('render_choice'):
                    for response_label in render_choice.iter('response_label'):
                        for material in response_label.iter('material'):
                            if material.find('matimage') == None:
                                self.mc_ilias_response_img_label.append("EMPTY")
                                self.mc_ilias_response_img_string_base64_encoded.append("EMPTY")

                            else:
                                self.mc_ilias_response_img_label.append(material.find('matimage').attrib.get('label'))
                                self.mc_ilias_response_img_string_base64_encoded.append(material.find('matimage').text)



                            for mattext in material.iter('mattext'):
                                self.mattext_text_all_mc_answers.append(mattext.text)
                                self.mc_ilias_response_text.append(mattext.text)


#####################################   Anzahl der Antworten pro MC-Frage
        # Durch diese Iteration und Abfrage nach MCMR (=Multiple Choice), werden alle Antworten der MC-Fragen aufgelistet
        for response_lid in self.myroot.iter('response_lid'):
            if response_lid.attrib.get('ident') == 'MCMR':
                for render_choice in response_lid.iter('render_choice'):
                    # Zu Beginn jedes Anwort-Blocks wird ein "$" geschrieben, um hinterher zu splitten
                    self.mc_answer_list_nr += "$"
                    for response_label in render_choice.iter('response_label'):
                        self.mc_answer_list_nr += str(response_label.attrib.get('ident'))

        self.ilias_test_question_type_collection_mc_answers = self.mc_answer_list_nr.split("$")
        self.ilias_test_question_type_collection_mc_answers.pop(0)  # Durch split() enthält erstes Feld keine Daten



        for respcondition in self.myroot.iter('respcondition'):
            for varequal in respcondition.iter('varequal'):
                if varequal.attrib.get('respident') == "MCMR":
                    for setvar in respcondition.iter('setvar'):
                        self.all_mc_questions_points.append(setvar.text)

        # Jedes zweite ELement übernehmen [::2] mit Start beim 1. Fach (nicht das 0. Fach)
        self.mc_questions_false_points = self.all_mc_questions_points[1::2]
        self.mc_questions_correct_points = self.all_mc_questions_points[::2]


        self.mc_ilias_number_of_response_variables = 10
        self.mc_ilias_response_text_1, self.mc_ilias_response_pts_correct_answer_1, self.mc_ilias_response_pts_false_answer_1, self.mc_ilias_response_img_label_1, self.mc_ilias_response_img_string_base64_encoded_1 = [], [], [], [], []
        self.mc_ilias_response_text_2, self.mc_ilias_response_pts_correct_answer_2, self.mc_ilias_response_pts_false_answer_2, self.mc_ilias_response_img_label_2, self.mc_ilias_response_img_string_base64_encoded_2 = [], [], [], [], []
        self.mc_ilias_response_text_3, self.mc_ilias_response_pts_correct_answer_3, self.mc_ilias_response_pts_false_answer_3, self.mc_ilias_response_img_label_3, self.mc_ilias_response_img_string_base64_encoded_3 = [], [], [], [], []
        self.mc_ilias_response_text_4, self.mc_ilias_response_pts_correct_answer_4, self.mc_ilias_response_pts_false_answer_4, self.mc_ilias_response_img_label_4, self.mc_ilias_response_img_string_base64_encoded_4 = [], [], [], [], []
        self.mc_ilias_response_text_5, self.mc_ilias_response_pts_correct_answer_5, self.mc_ilias_response_pts_false_answer_5, self.mc_ilias_response_img_label_5, self.mc_ilias_response_img_string_base64_encoded_5 = [], [], [], [], []
        self.mc_ilias_response_text_6, self.mc_ilias_response_pts_correct_answer_6, self.mc_ilias_response_pts_false_answer_6, self.mc_ilias_response_img_label_6, self.mc_ilias_response_img_string_base64_encoded_6 = [], [], [], [], []
        self.mc_ilias_response_text_7, self.mc_ilias_response_pts_correct_answer_7, self.mc_ilias_response_pts_false_answer_7, self.mc_ilias_response_img_label_7, self.mc_ilias_response_img_string_base64_encoded_7 = [], [], [], [], []
        self.mc_ilias_response_text_8, self.mc_ilias_response_pts_correct_answer_8, self.mc_ilias_response_pts_false_answer_8, self.mc_ilias_response_img_label_8, self.mc_ilias_response_img_string_base64_encoded_8 = [], [], [], [], []
        self.mc_ilias_response_text_9, self.mc_ilias_response_pts_correct_answer_9, self.mc_ilias_response_pts_false_answer_9, self.mc_ilias_response_img_label_9, self.mc_ilias_response_img_string_base64_encoded_9 = [], [], [], [], []
        self.mc_ilias_response_text_10, self.mc_ilias_response_pts_correct_answer_10, self.mc_ilias_response_pts_false_answer_10, self.mc_ilias_response_img_label_10, self.mc_ilias_response_img_string_base64_encoded_10 = [], [], [], [], []


        t = 0
        for i in range(len(self.ilias_test_question_type_collection_mc_answers)):
            if i == 1:
                t = int(max(self.ilias_test_question_type_collection_mc_answers[0])) + 1

            if "0" in self.ilias_test_question_type_collection_mc_answers[i]:
                self.mc_ilias_response_text_1.append(self.mc_ilias_response_text[t])
                self.mc_ilias_response_pts_correct_answer_1.append(self.mc_questions_correct_points[t])
                self.mc_ilias_response_pts_false_answer_1.append(self.mc_questions_false_points[t])
                self.mc_ilias_response_img_label_1.append(self.mc_ilias_response_img_label[t])
                self.mc_ilias_response_img_string_base64_encoded_1.append(self.mc_ilias_response_img_string_base64_encoded[t])
            else:
                self.mc_ilias_response_text_1.append(" ")
                self.mc_ilias_response_pts_correct_answer_1.append(" ")
                self.mc_ilias_response_pts_false_answer_1.append(" ")
                self.mc_ilias_response_img_label_1.append("EMPTY")
                self.mc_ilias_response_img_string_base64_encoded_1.append("EMPTY")

            if "1" in self.ilias_test_question_type_collection_mc_answers[i]:
                self.mc_ilias_response_text_2.append(self.mc_ilias_response_text[t + 1])
                self.mc_ilias_response_pts_correct_answer_2.append(self.mc_questions_correct_points[t+1])
                self.mc_ilias_response_pts_false_answer_2.append(self.mc_questions_false_points[t + 1])
                self.mc_ilias_response_img_label_2.append(self.mc_ilias_response_img_label[t + 1])
                self.mc_ilias_response_img_string_base64_encoded_2.append(self.mc_ilias_response_img_string_base64_encoded[t])
            else:
                self.mc_ilias_response_text_2.append(" ")
                self.mc_ilias_response_pts_correct_answer_2.append(" ")
                self.mc_ilias_response_pts_false_answer_2.append(" ")
                self.mc_ilias_response_img_label_2.append("EMPTY")
                self.mc_ilias_response_img_string_base64_encoded_2.append("EMPTY")

            if "2" in self.ilias_test_question_type_collection_mc_answers[i]:
                self.mc_ilias_response_text_3.append(self.mc_ilias_response_text[t + 2])
                self.mc_ilias_response_pts_correct_answer_3.append(self.mc_questions_correct_points[t+2])
                self.mc_ilias_response_pts_false_answer_3.append(self.mc_questions_false_points[t + 2])
                self.mc_ilias_response_img_label_3.append(self.mc_ilias_response_img_label[t + 2])
                self.mc_ilias_response_img_string_base64_encoded_3.append(self.mc_ilias_response_img_string_base64_encoded[t])
            else:
                self.mc_ilias_response_text_3.append(" ")
                self.mc_ilias_response_pts_correct_answer_3.append(" ")
                self.mc_ilias_response_pts_false_answer_3.append(" ")
                self.mc_ilias_response_img_label_3.append("EMPTY")
                self.mc_ilias_response_img_string_base64_encoded_3.append("EMPTY")

            if "3" in self.ilias_test_question_type_collection_mc_answers[i]:
                self.mc_ilias_response_text_4.append(self.mc_ilias_response_text[t + 3])
                self.mc_ilias_response_pts_correct_answer_4.append(self.mc_questions_correct_points[t+4])
                self.mc_ilias_response_pts_false_answer_4.append(self.mc_questions_false_points[t + 3])
                self.mc_ilias_response_img_label_4.append(self.mc_ilias_response_img_label[t + 3])
                self.mc_ilias_response_img_string_base64_encoded_4.append(self.mc_ilias_response_img_string_base64_encoded[t])
            else:
                self.mc_ilias_response_text_4.append(" ")
                self.mc_ilias_response_pts_correct_answer_4.append(" ")
                self.mc_ilias_response_pts_false_answer_4.append(" ")
                self.mc_ilias_response_img_label_4.append("EMPTY")
                self.mc_ilias_response_img_string_base64_encoded_4.append("EMPTY")

            if "4" in self.ilias_test_question_type_collection_mc_answers[i]:
                self.mc_ilias_response_text_5.append(self.mc_ilias_response_text[t + 4])
                self.mc_ilias_response_pts_correct_answer_5.append(self.mc_questions_correct_points[t+4])
                self.mc_ilias_response_pts_false_answer_5.append(self.mc_questions_false_points[t + 4])
                self.mc_ilias_response_img_label_5.append(self.mc_ilias_response_img_label[t + 4])
                self.mc_ilias_response_img_string_base64_encoded_5.append(self.mc_ilias_response_img_string_base64_encoded[t])
            else:
                self.mc_ilias_response_text_5.append(" ")
                self.mc_ilias_response_pts_correct_answer_5.append(" ")
                self.mc_ilias_response_pts_false_answer_5.append(" ")
                self.mc_ilias_response_img_label_5.append("EMPTY")
                self.mc_ilias_response_img_string_base64_encoded_5.append("EMPTY")

            if "5" in self.ilias_test_question_type_collection_mc_answers[i]:
                self.mc_ilias_response_text_6.append(self.mc_ilias_response_text[t + 5])
                self.mc_ilias_response_pts_correct_answer_6.append(self.mc_questions_correct_points[t+5])
                self.mc_ilias_response_pts_false_answer_6.append(self.mc_questions_false_points[t + 5])
                self.mc_ilias_response_img_label_6.append(self.mc_ilias_response_img_label[t + 5])
                self.mc_ilias_response_img_string_base64_encoded_6.append(self.mc_ilias_response_img_string_base64_encoded[t])
            else:
                self.mc_ilias_response_text_6.append(" ")
                self.mc_ilias_response_pts_correct_answer_6.append(" ")
                self.mc_ilias_response_pts_false_answer_6.append(" ")
                self.mc_ilias_response_img_label_6.append("EMPTY")
                self.mc_ilias_response_img_string_base64_encoded_6.append("EMPTY")

            if "6" in self.ilias_test_question_type_collection_mc_answers[i]:
                self.mc_ilias_response_text_7.append(self.mc_ilias_response_text[t + 6])
                self.mc_ilias_response_pts_correct_answer_7.append(self.mc_questions_correct_points[t+6])
                self.mc_ilias_response_pts_false_answer_7.append(self.mc_questions_false_points[t + 6])
                self.mc_ilias_response_img_label_7.append(self.mc_ilias_response_img_label[t + 6])
                self.mc_ilias_response_img_string_base64_encoded_7.append(self.mc_ilias_response_img_string_base64_encoded[t])
            else:
                self.mc_ilias_response_text_7.append(" ")
                self.mc_ilias_response_pts_correct_answer_7.append(" ")
                self.mc_ilias_response_pts_false_answer_7.append(" ")
                self.mc_ilias_response_img_label_7.append("EMPTY")
                self.mc_ilias_response_img_string_base64_encoded_7.append("EMPTY")

            if "7" in self.ilias_test_question_type_collection_mc_answers[i]:
                self.mc_ilias_response_text_8.append(self.mc_ilias_response_text[t + 7])
                self.mc_ilias_response_pts_correct_answer_8.append(self.mc_questions_correct_points[t+7])
                self.mc_ilias_response_pts_false_answer_8.append(self.mc_questions_false_points[t + 7])
                self.mc_ilias_response_img_label_8.append(self.mc_ilias_response_img_label[t + 7])
                self.mc_ilias_response_img_string_base64_encoded_8.append(self.mc_ilias_response_img_string_base64_encoded[t])
            else:
                self.mc_ilias_response_text_8.append(" ")
                self.mc_ilias_response_pts_correct_answer_8.append(" ")
                self.mc_ilias_response_pts_false_answer_8.append(" ")
                self.mc_ilias_response_img_label_8.append("EMPTY")
                self.mc_ilias_response_img_string_base64_encoded_8.append("EMPTY")

            if "8" in self.ilias_test_question_type_collection_mc_answers[i]:
                self.mc_ilias_response_text_9.append(self.mc_ilias_response_text[t + 8])
                self.mc_ilias_response_pts_correct_answer_9.append(self.mc_questions_correct_points[t+8])
                self.mc_ilias_response_pts_false_answer_9.append(self.mc_questions_false_points[t + 8])
                self.mc_ilias_response_img_label_9.append(self.mc_ilias_response_img_label[t + 8])
                self.mc_ilias_response_img_string_base64_encoded_9.append(self.mc_ilias_response_img_string_base64_encoded[t])
            else:
                self.mc_ilias_response_text_9.append(" ")
                self.mc_ilias_response_pts_correct_answer_9.append(" ")
                self.mc_ilias_response_pts_false_answer_9.append(" ")
                self.mc_ilias_response_img_label_9.append("EMPTY")
                self.mc_ilias_response_img_string_base64_encoded_9.append("EMPTY")

            if "9" in self.ilias_test_question_type_collection_mc_answers[i]:
                self.mc_ilias_response_text_10.append(self.mc_ilias_response_text[t + 9])
                self.mc_ilias_response_pts_correct_answer_10.append(self.mc_questions_correct_points[t+9])
                self.mc_ilias_response_pts_false_answer_10.append(self.mc_questions_false_points[t + 9])
                self.mc_ilias_response_img_label_10.append(self.mc_ilias_response_img_label[t + 9])
                self.mc_ilias_response_img_string_base64_encoded_10.append(self.mc_ilias_response_img_string_base64_encoded[t])
            else:
                self.mc_ilias_response_text_10.append(" ")
                self.mc_ilias_response_pts_correct_answer_10.append(" ")
                self.mc_ilias_response_pts_false_answer_10.append(" ")
                self.mc_ilias_response_img_label_10.append("EMPTY")
                self.mc_ilias_response_img_string_base64_encoded_10.append("EMPTY")

            t += int(max(self.ilias_test_question_type_collection_mc_answers[i])) + 1



    def write_data_to_database_mc(self):

        print("_______________________________________________")

        # Create a database or connect to one
        connect = sqlite3.connect(self.database_multiplechoice_path)

        # Create cursor
        cursor = connect.cursor()


        for i in range(len( self.ilias_question_type_mc_question_index)):

            # Bilder der Reihe nach einlesen
            if self.ilias_test_question_description_image_uri_1[i] != "EMPTY":

                with open(os.path.normpath(os.path.join(self.select_test_import_file, self.ilias_test_question_description_image_uri_1[i])), 'rb') as image_file:
                    self.ilias_test_question_description_image_data_1.append(image_file.read())

            else:
                self.ilias_test_question_description_image_data_1.append("EMPTY")


            # Create table
            cursor.execute(
                "INSERT INTO multiplechoice_table VALUES ("
                ":question_difficulty, :question_category, :question_type, "
                ":question_title, :question_description_title, :question_description_main, "
                ":response_1_text, :response_1_pts_correct_answer, :response_1_pts_false_answer, :response_1_img_label, :response_1_img_string_base64_encoded, :response_1_img_path,"
                ":response_2_text, :response_2_pts_correct_answer, :response_2_pts_false_answer, :response_2_img_label, :response_2_img_string_base64_encoded, :response_2_img_path,"
                ":response_3_text, :response_3_pts_correct_answer, :response_3_pts_false_answer, :response_3_img_label, :response_3_img_string_base64_encoded, :response_3_img_path,"
                ":response_4_text, :response_4_pts_correct_answer, :response_4_pts_false_answer, :response_4_img_label, :response_4_img_string_base64_encoded, :response_4_img_path,"
                ":response_5_text, :response_5_pts_correct_answer, :response_5_pts_false_answer, :response_5_img_label, :response_5_img_string_base64_encoded, :response_5_img_path,"
                ":response_6_text, :response_6_pts_correct_answer, :response_6_pts_false_answer, :response_6_img_label, :response_6_img_string_base64_encoded, :response_6_img_path,"
                ":response_7_text, :response_7_pts_correct_answer, :response_7_pts_false_answer, :response_7_img_label, :response_7_img_string_base64_encoded, :response_7_img_path,"
                ":response_8_text, :response_8_pts_correct_answer, :response_8_pts_false_answer, :response_8_img_label, :response_8_img_string_base64_encoded, :response_8_img_path,"
                ":response_9_text, :response_9_pts_correct_answer, :response_9_pts_false_answer, :response_9_img_label, :response_9_img_string_base64_encoded, :response_9_img_path,"
                ":response_10_text, :response_10_pts_correct_answer, :response_10_pts_false_answer, :response_10_img_label, :response_10_img_string_base64_encoded, :response_10_img_path,"
                ":picture_preview_pixel, "
                ":description_img_name_1, :description_img_data_1, :description_img_path_1, "
                ":description_img_name_2, :description_img_data_2, :description_img_path_2, "
                ":description_img_name_3, :description_img_data_3, :description_img_path_3, "
                ":test_time, :var_number, :question_pool_tag, :question_author)",
                {
                    'question_difficulty': " ",
                    'question_category': " ",
                    'question_type': "Multiplechoice",

                    'question_title': self.ilias_question_title[int(self.ilias_question_type_mc_question_index[i])],
                    'question_description_title': self.ilias_question_description_title[int(self.ilias_question_type_mc_question_index[i])],
                    'question_description_main': self.ilias_question_description_main[int(self.ilias_question_type_mc_question_index[i])],


                    'response_1_text': self.mc_ilias_response_text_1[i],
                    'response_1_pts_correct_answer': self.mc_ilias_response_pts_correct_answer_1[i],
                    'response_1_pts_false_answer': self.mc_ilias_response_pts_false_answer_1[i],
                    'response_1_img_label': self.mc_ilias_response_img_label_1[i],
                    'response_1_img_string_base64_encoded': self.mc_ilias_response_img_string_base64_encoded_1[i],
                    'response_1_img_path': "",

                    'response_2_text': self.mc_ilias_response_text_2[i],
                    'response_2_pts_correct_answer': self.mc_ilias_response_pts_correct_answer_2[i],
                    'response_2_pts_false_answer': self.mc_ilias_response_pts_false_answer_2[i],
                    'response_2_img_label': self.mc_ilias_response_img_label_2[i],
                    'response_2_img_string_base64_encoded': self.mc_ilias_response_img_string_base64_encoded_2[i],
                    'response_2_img_path': "",

                    'response_3_text':  self.mc_ilias_response_text_3[i],
                    'response_3_pts_correct_answer': self.mc_ilias_response_pts_correct_answer_3[i],
                    'response_3_pts_false_answer': self.mc_ilias_response_pts_false_answer_3[i],
                    'response_3_img_label': self.mc_ilias_response_img_label_3[i],
                    'response_3_img_string_base64_encoded': self.mc_ilias_response_img_string_base64_encoded_3[i],
                    'response_3_img_path': "",

                    'response_4_text': self.mc_ilias_response_text_4[i],
                    'response_4_pts_correct_answer': self.mc_ilias_response_pts_correct_answer_4[i],
                    'response_4_pts_false_answer': self.mc_ilias_response_pts_false_answer_4[i],
                    'response_4_img_label': self.mc_ilias_response_img_label_4[i],
                    'response_4_img_string_base64_encoded': self.mc_ilias_response_img_string_base64_encoded_4[i],
                    'response_4_img_path': "",

                    'response_5_text': self.mc_ilias_response_text_5[i],
                    'response_5_pts_correct_answer': self.mc_ilias_response_pts_correct_answer_5[i],
                    'response_5_pts_false_answer': self.mc_ilias_response_pts_false_answer_5[i],
                    'response_5_img_label': self.mc_ilias_response_img_label_5[i],
                    'response_5_img_string_base64_encoded': self.mc_ilias_response_img_string_base64_encoded_5[i],
                    'response_5_img_path': "",

                    'response_6_text': self.mc_ilias_response_text_6[i],
                    'response_6_pts_correct_answer': self.mc_ilias_response_pts_correct_answer_6[i],
                    'response_6_pts_false_answer': self.mc_ilias_response_pts_false_answer_6[i],
                    'response_6_img_label': self.mc_ilias_response_img_label_6[i],
                    'response_6_img_string_base64_encoded': self.mc_ilias_response_img_string_base64_encoded_6[i],
                    'response_6_img_path': "",

                    'response_7_text': self.mc_ilias_response_text_7[i],
                    'response_7_pts_correct_answer': self.mc_ilias_response_pts_correct_answer_7[i],
                    'response_7_pts_false_answer': self.mc_ilias_response_pts_false_answer_7[i],
                    'response_7_img_label': self.mc_ilias_response_img_label_7[i],
                    'response_7_img_string_base64_encoded': self.mc_ilias_response_img_string_base64_encoded_7[i],
                    'response_7_img_path': "",

                    'response_8_text': self.mc_ilias_response_text_8[i],
                    'response_8_pts_correct_answer': self.mc_ilias_response_pts_correct_answer_8[i],
                    'response_8_pts_false_answer': self.mc_ilias_response_pts_false_answer_8[i],
                    'response_8_img_label': self.mc_ilias_response_img_label_8[i],
                    'response_8_img_string_base64_encoded': self.mc_ilias_response_img_string_base64_encoded_8[i],
                    'response_8_img_path': "",

                    'response_9_text': self.mc_ilias_response_text_9[i],
                    'response_9_pts_correct_answer': self.mc_ilias_response_pts_correct_answer_9[i],
                    'response_9_pts_false_answer': self.mc_ilias_response_pts_false_answer_9[i],
                    'response_9_img_label': self.mc_ilias_response_img_label_9[i],
                    'response_9_img_string_base64_encoded': self.mc_ilias_response_img_string_base64_encoded_9[i],
                    'response_9_img_path': "",

                    'response_10_text': self.mc_ilias_response_text_10[i],
                    'response_10_pts_correct_answer': self.mc_ilias_response_pts_correct_answer_10[i],
                    'response_10_pts_false_answer': self.mc_ilias_response_pts_false_answer_10[i],
                    'response_10_img_label': self.mc_ilias_response_img_label_10[i],
                    'response_10_img_string_base64_encoded': self.mc_ilias_response_img_string_base64_encoded_10[i],
                    'response_10_img_path': "",

                    'picture_preview_pixel': "",

                    'description_img_name_1': self.ilias_test_question_description_image_name_1[i],
                    'description_img_data_1': self.ilias_test_question_description_image_data_1[i],
                    'description_img_path_1': self.ilias_test_question_description_image_uri_1[i],

                    'description_img_name_2': "",
                    'description_img_data_2': "",
                    'description_img_path_2': "",

                    'description_img_name_3': "",
                    'description_img_data_3': "",
                    'description_img_path_3': "",

                    'test_time': self.ilias_test_duration[int(self.ilias_question_type_mc_question_index[i])],

                    'var_number': "",
                    'question_pool_tag': "",
                    'question_author': self.ilias_question_author[int(self.ilias_question_type_mc_question_index[i])]

                }
            )
            print(str(i+1) + ": MultipleChoice: " + str(self.ilias_question_title[int(self.ilias_question_type_mc_question_index[i])]) + " in DB gespeichert")
        # Commit Changes
        connect.commit()

        # Close Connection
        connect.close()

####### Matching Question Fragen
    def read_matching_questions(self):

        # MATCHING QUESTIONS Antworten
        # Es werden alle möglichen Antworten (ident_nr) aus der .xml für die MQ-Fragen aufgelistet
        for response_grp in self.myroot.iter('response_grp'):
            if response_grp.attrib.get('ident') == "MQ":      #MQ -> Matching Question
                self.mattext_text_all_mq_answers.append("$")
                for render_choice in response_grp.iter('render_choice'):
                    for response_label in render_choice.iter('response_label'):
                        self.mattext_text_all_mq_answers.append(response_label.attrib.get('ident'))
                        self.mattext_text_all_mq_answers_collection.append(response_label.attrib.get('ident'))
                        # Eine Antwort (ident_nr) wird immer einer "match_group" zugewiesen
                        #self.mq_match_group.append(response_label.attrib.get('match_group'))


        for response_grp in self.myroot.iter('response_grp'):
            if response_grp.attrib.get('ident') == "MQ":    #MQ -> Matching Question
                for render_choice in response_grp.iter('render_choice'):
                    for response_label in render_choice.iter('response_label'):
                        for material in response_label.iter('material'):
                            for mattext in material.iter('mattext'):
                                self.mattText_text_all_mq_answers.append(mattext.text)



        # MATCHING QUESTIONS Bild-Namen
        for response_grp in self.myroot.iter('response_grp'):
            if response_grp.attrib.get('ident') == "MQ":    #MQ -> Matching Question
                for render_choice in response_grp.iter('render_choice'):
                    for response_label in render_choice.iter('response_label'):
                        for material in response_label.iter('material'):
                            for matimage in material.iter('matimage'):
                                self.mq_response_img_label.append(matimage.attrib.get('label'))
                                self.mq_response_img_data.append(matimage.text)


        for item in self.myroot.iter('item'):
            for resprocessing in item.iter('resprocessing'):
                for respcondition in resprocessing.iter('respcondition'):
                    for conditionvar in respcondition.iter('conditionvar'):
                        for varsubset in conditionvar.iter('varsubset'):
                            if varsubset.attrib.get('respident') == "MQ":
                                self.mq_matching_ids.append(varsubset.text)


            self.mq_len_list.append(len(self.mq_matching_ids))

        self.mq_len_list = list(dict.fromkeys(self.mq_len_list))
        for j in range(len(self.mq_len_list)):
            if j > 0:
                self.mq_len_list[j] = self.mq_len_list[j] - self.mq_len_list[j-1]


        # MATCHING QUESTIONS Punkte für Antworten
        for respcondition in self.myroot.iter('respcondition'):
            for conditionvar in respcondition.iter('conditionvar'):
                for varsubset in conditionvar.iter('varsubset'):
                    if varsubset.attrib.get('respident') == "MQ":
                        for setvar in respcondition.iter('setvar'):
                            self.mq_matching_ids_points.append(setvar.text)



        # Erstes Fach enthält ein "$" und wird nicht benötigt
        if len(self.mattext_text_all_mq_answers) > 0:
            self.mattext_text_all_mq_answers.pop(0)

        self.index_counter = 0
        for i in range(len(self.mattext_text_all_mq_answers)):
            if self.mattext_text_all_mq_answers[i] == "$":
                self.mq_number_of_answers_per_question.append(i-self.index_counter)
                self.index_counter = self.index_counter + 1



        # Die Anzahl der Werte nach dem letzten "$" einfügen. "-1" weil noch ein "$" enhalten ist
        self.mq_number_of_answers_per_question.append(len(self.mattext_text_all_mq_answers)- len(self.mq_number_of_answers_per_question))



        # Letztes Fach der Liste wird, vorletztes Fach abgezogen.
        #self.mq_number_of_answers_per_question[len(self.mq_number_of_answers_per_question)-1] = self.mq_number_of_answers_per_question[len(self.mq_number_of_answers_per_question)-1] - self.mq_number_of_answers_per_question[len(self.mq_number_of_answers_per_question)-2]

        for i in range(len(self.mq_number_of_answers_per_question)):
            if i >= 1:
                self.mq_number_of_answers_per_question_temp.append(self.mq_number_of_answers_per_question[i] - self.mq_number_of_answers_per_question[i-1])
            else:
                self.mq_number_of_answers_per_question_temp.append(self.mq_number_of_answers_per_question[i])

        self.mq_number_of_answers_per_question = self.mq_number_of_answers_per_question_temp



        ##

        self.mq_len_list.pop(0)
        len_temp = 0
        for j in range(len(self.mq_number_of_answers_per_question)):
            for k in range(self.mq_number_of_answers_per_question[j]):
                if k >= self.mq_len_list[j]:
                    self.mq_matching_ids.insert(k+len_temp, " ")
                    self.mq_matching_ids_points.insert(k+len_temp, " ")
            len_temp += self.mq_number_of_answers_per_question[j]





        for varsubset in self.myroot.iter('varsubset'):
            if varsubset.attrib.get('respident') == "MQ":
                self.mq_answer_matchings.append(varsubset.text)

        # Punkte können nicht spezifisch ausgelesen werden für MQ
        # Jedoch können die einzelnen Lösungen ausgelesen werden und entsprechend für jede Lösung fix "1" Pkt. vergeben
        for i in range(len(self.mq_answer_matchings)):
            self.mq_answer_matchings_points.append("1")

        for i in range(len(self.mq_number_of_answers_per_question)):
            self.mq_answer_matching_per_question.append(int(self.mq_number_of_answers_per_question[i]/2))

        for i in range(len(self.mq_number_of_answers_per_question)):
            self.mq_answer_list_nr += "$"
            for j in range(int(self.mq_number_of_answers_per_question[i])):
                self.mq_answer_list_nr += str(j)


        self.ilias_test_question_type_collection_mq_answers = self.mq_answer_list_nr.split("$")
        self.ilias_test_question_type_collection_mq_answers.pop(0)  # Durch split() enthält erstes Feld keine Daten


        self.mq_ilias_response_text_1, self.mq_ilias_response_img_label_1, self.mq_ilias_response_img_string_base64_encoded_1 = [],[], []
        self.mq_ilias_response_text_2, self.mq_ilias_response_img_label_2, self.mq_ilias_response_img_string_base64_encoded_2 = [],[], []
        self.mq_ilias_response_text_3, self.mq_ilias_response_img_label_3, self.mq_ilias_response_img_string_base64_encoded_3 = [],[], []
        self.mq_ilias_response_text_4, self.mq_ilias_response_img_label_4, self.mq_ilias_response_img_string_base64_encoded_4 = [],[], []
        self.mq_ilias_response_text_5, self.mq_ilias_response_img_label_5, self.mq_ilias_response_img_string_base64_encoded_5 = [],[], []
        self.mq_ilias_response_text_6, self.mq_ilias_response_img_label_6, self.mq_ilias_response_img_string_base64_encoded_6 = [],[], []
        self.mq_ilias_response_text_7, self.mq_ilias_response_img_label_7, self.mq_ilias_response_img_string_base64_encoded_7 = [],[], []
        self.mq_ilias_response_text_8, self.mq_ilias_response_img_label_8, self.mq_ilias_response_img_string_base64_encoded_8 = [],[], []
        self.mq_ilias_response_text_9, self.mq_ilias_response_img_label_9, self.mq_ilias_response_img_string_base64_encoded_9 = [],[], []
        self.mq_ilias_response_text_10, self.mq_ilias_response_img_label_10, self.mq_ilias_response_img_string_base64_encoded_10 = [],[], []

        self.mq_matching_id_1, self.mq_matching_id_points_1 = [], []
        self.mq_matching_id_2, self.mq_matching_id_points_2 = [], []
        self.mq_matching_id_3, self.mq_matching_id_points_3 = [], []
        self.mq_matching_id_4, self.mq_matching_id_points_4 = [], []
        self.mq_matching_id_5, self.mq_matching_id_points_5 = [], []
        self.mq_matching_id_6, self.mq_matching_id_points_6 = [], []
        self.mq_matching_id_7, self.mq_matching_id_points_7 = [], []
        self.mq_matching_id_8, self.mq_matching_id_points_8 = [], []
        self.mq_matching_id_9, self.mq_matching_id_points_9 = [], []
        self.mq_matching_id_10, self.mq_matching_id_points_10 = [], []

        t = 0
        for i in range(len(self.ilias_test_question_type_collection_mq_answers)):
            if i == 1:
                t = int(max(self.ilias_test_question_type_collection_mq_answers[0])) + 1

            if "0" in self.ilias_test_question_type_collection_mq_answers[i]:
                self.mq_ilias_response_text_1.append(self.mattText_text_all_mq_answers[t])
                self.mq_ilias_response_img_label_1.append(self.mq_response_img_label[t])
                self.mq_ilias_response_img_string_base64_encoded_1.append(self.mq_response_img_data[t])
                self.mq_matching_id_1.append(self.mq_matching_ids[t])
                self.mq_matching_id_points_1.append(self.mq_matching_ids_points[t])
            else:
                self.mq_ilias_response_text_1.append(" ")
                self.mq_ilias_response_img_label_1.append(" ")
                self.mq_ilias_response_img_string_base64_encoded_1.append(" ")
                self.mq_matching_id_1.append(" ")
                self.mq_matching_id_points_1.append(" ")

            if "1" in self.ilias_test_question_type_collection_mq_answers[i]:
                self.mq_ilias_response_text_2.append(self.mattText_text_all_mq_answers[t + 1])
                self.mq_ilias_response_img_label_2.append(self.mq_response_img_label[t + 1])
                self.mq_ilias_response_img_string_base64_encoded_2.append(self.mq_response_img_data[t + 1])
                self.mq_matching_id_2.append(self.mq_matching_ids[t + 1])
                self.mq_matching_id_points_2.append(self.mq_matching_ids_points[t + 1])
            else:
                self.mq_ilias_response_text_2.append(" ")
                self.mq_ilias_response_img_label_2.append(" ")
                self.mq_ilias_response_img_string_base64_encoded_2.append(" ")
                self.mq_matching_id_2.append(" ")
                self.mq_matching_id_points_2.append(" ")

            if "2" in self.ilias_test_question_type_collection_mq_answers[i]:
                self.mq_ilias_response_text_3.append(self.mattText_text_all_mq_answers[t + 2])
                self.mq_ilias_response_img_label_3.append(self.mq_response_img_label[t + 2])
                self.mq_ilias_response_img_string_base64_encoded_3.append(self.mq_response_img_data[t + 2])
                self.mq_matching_id_3.append(self.mq_matching_ids[t + 2])
                self.mq_matching_id_points_3.append(self.mq_matching_ids_points[t + 2])
            else:
                self.mq_ilias_response_text_3.append(" ")
                self.mq_ilias_response_img_label_3.append(" ")
                self.mq_ilias_response_img_string_base64_encoded_3.append(" ")
                self.mq_matching_id_3.append(" ")
                self.mq_matching_id_points_3.append(" ")

            if "3" in self.ilias_test_question_type_collection_mq_answers[i]:
                self.mq_ilias_response_text_4.append(self.mattText_text_all_mq_answers[t + 3])
                self.mq_ilias_response_img_label_4.append(self.mq_response_img_label[t + 3])
                self.mq_ilias_response_img_string_base64_encoded_4.append(self.mq_response_img_data[t + 3])
                self.mq_matching_id_4.append(self.mq_matching_ids[t + 3])
                self.mq_matching_id_points_4.append(self.mq_matching_ids_points[t + 3])
            else:
                self.mq_ilias_response_text_4.append(" ")
                self.mq_ilias_response_img_label_4.append(" ")
                self.mq_ilias_response_img_string_base64_encoded_4.append(" ")
                self.mq_matching_id_4.append(" ")
                self.mq_matching_id_points_4.append(" ")

            if "4" in self.ilias_test_question_type_collection_mq_answers[i]:
                self.mq_ilias_response_text_5.append(self.mattText_text_all_mq_answers[t + 4])
                self.mq_ilias_response_img_label_5.append(self.mq_response_img_label[t + 4])
                self.mq_ilias_response_img_string_base64_encoded_5.append(self.mq_response_img_data[t + 4])
                self.mq_matching_id_5.append(self.mq_matching_ids[t + 4])
                self.mq_matching_id_points_5.append(self.mq_matching_ids_points[t + 4])
            else:
                self.mq_ilias_response_text_5.append(" ")
                self.mq_ilias_response_img_label_5.append(" ")
                self.mq_ilias_response_img_string_base64_encoded_5.append(" ")
                self.mq_matching_id_5.append(" ")
                self.mq_matching_id_points_5.append(" ")

            if "5" in self.ilias_test_question_type_collection_mq_answers[i]:
                self.mq_ilias_response_text_6.append(self.mattText_text_all_mq_answers[t + 5])
                self.mq_ilias_response_img_label_6.append(self.mq_response_img_label[t + 5])
                self.mq_ilias_response_img_string_base64_encoded_6.append(self.mq_response_img_data[t + 5])
                self.mq_matching_id_6.append(self.mq_matching_ids[t + 5])
                self.mq_matching_id_points_6.append(self.mq_matching_ids_points[t + 5])
            else:
                self.mq_ilias_response_text_6.append(" ")
                self.mq_ilias_response_img_label_6.append(" ")
                self.mq_ilias_response_img_string_base64_encoded_6.append(" ")
                self.mq_matching_id_6.append(" ")
                self.mq_matching_id_points_6.append(" ")

            if "6" in self.ilias_test_question_type_collection_mq_answers[i]:
                self.mq_ilias_response_text_7.append(self.mattText_text_all_mq_answers[t + 6])
                self.mq_ilias_response_img_label_7.append(self.mq_response_img_label[t + 6])
                self.mq_ilias_response_img_string_base64_encoded_7.append(self.mq_response_img_data[t + 6])
                self.mq_matching_id_7.append(self.mq_matching_ids[t + 6])
                self.mq_matching_id_points_7.append(self.mq_matching_ids_points[t + 6])
            else:
                self.mq_ilias_response_text_7.append(" ")
                self.mq_ilias_response_img_label_7.append(" ")
                self.mq_ilias_response_img_string_base64_encoded_7.append(" ")
                self.mq_matching_id_7.append(" ")
                self.mq_matching_id_points_7.append(" ")

            if "7" in self.ilias_test_question_type_collection_mq_answers[i]:
                self.mq_ilias_response_text_8.append(self.mattText_text_all_mq_answers[t + 7])
                self.mq_ilias_response_img_label_8.append(self.mq_response_img_label[t + 7])
                self.mq_ilias_response_img_string_base64_encoded_8.append(self.mq_response_img_data[t + 7])
                self.mq_matching_id_8.append(self.mq_matching_ids[t + 7])
                self.mq_matching_id_points_8.append(self.mq_matching_ids_points[t + 7])
            else:
                self.mq_ilias_response_text_8.append(" ")
                self.mq_ilias_response_img_label_8.append(" ")
                self.mq_ilias_response_img_string_base64_encoded_8.append(" ")
                self.mq_matching_id_8.append(" ")
                self.mq_matching_id_points_8.append(" ")

            if "8" in self.ilias_test_question_type_collection_mq_answers[i]:
                self.mq_ilias_response_text_9.append(self.mattText_text_all_mq_answers[t + 8])
                self.mq_ilias_response_img_label_9.append(self.mq_response_img_label[t + 8])
                self.mq_ilias_response_img_string_base64_encoded_9.append(self.mq_response_img_data[t + 8])
                self.mq_matching_id_9.append(self.mq_matching_ids[t + 8])
                self.mq_matching_id_points_9.append(self.mq_matching_ids_points[t + 8])
            else:
                self.mq_ilias_response_text_9.append(" ")
                self.mq_ilias_response_img_label_9.append(" ")
                self.mq_ilias_response_img_string_base64_encoded_9.append(" ")
                self.mq_matching_id_9.append(" ")
                self.mq_matching_id_points_9.append(" ")

            if "9" in self.ilias_test_question_type_collection_mq_answers[i]:
                self.mq_ilias_response_text_10.append(self.mattText_text_all_mq_answers[t + 9])
                self.mq_ilias_response_img_label_10.append(self.mq_response_img_label[t + 9])
                self.mq_ilias_response_img_string_base64_encoded_10.append(self.mq_response_img_data[t + 9])
                self.mq_matching_id_10.append(self.mq_matching_ids[t + 9])
                self.mq_matching_id_points_10.append(self.mq_matching_ids_points[t + 9])
            else:
                self.mq_ilias_response_text_10.append(" ")
                self.mq_ilias_response_img_label_10.append(" ")
                self.mq_ilias_response_img_string_base64_encoded_10.append(" ")
                self.mq_matching_id_10.append(" ")
                self.mq_matching_id_points_10.append(" ")

            t += int(max(self.ilias_test_question_type_collection_mq_answers[i])) + 1

    def write_data_to_database_mq(self):

        print("_______________________________________________")
        # Create a database or connect to one
        connect = sqlite3.connect(self.database_zuordnungsfrage_path)

        # Create cursor
        cursor = connect.cursor()

        for i in range(len( self.ilias_question_type_mq_question_index)):

            # Bilder der Reihe nach einlesen
            if self.ilias_test_question_description_image_uri_1[i] != "EMPTY":

                with open(os.path.normpath(os.path.join(self.select_test_import_file, self.ilias_test_question_description_image_uri_1[i])), 'rb') as image_file:
                    self.ilias_test_question_description_image_data_1.append(image_file.read())

            else:
                self.ilias_test_question_description_image_data_1.append("EMPTY")

            # Create table
            cursor.execute(
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
                    'question_difficulty': " ",
                    'question_category': " ",
                    'question_type': "Zuordnungsfrage",

                    'question_title': self.ilias_question_title[int(self.ilias_question_type_mq_question_index[i])],
                    'question_description_title': self.ilias_question_description_title[int(self.ilias_question_type_mq_question_index[i])],
                    'question_description_main': self.ilias_question_description_main[int(self.ilias_question_type_mq_question_index[i])],
                    'mix_answers': "mix_answers",
                    'assignment_mode': "assignment_mode",

                    'definitions_response_1_text': self.mq_ilias_response_text_1[i],
                    'definitions_response_2_text': self.mq_ilias_response_text_2[i],
                    'definitions_response_3_text': self.mq_ilias_response_text_3[i],
                    'definitions_response_4_text': self.mq_ilias_response_text_4[i],
                    'definitions_response_5_text': self.mq_ilias_response_text_5[i],
                    'definitions_response_6_text': self.mq_ilias_response_text_6[i],
                    'definitions_response_7_text': self.mq_ilias_response_text_7[i],
                    'definitions_response_8_text': self.mq_ilias_response_text_8[i],
                    'definitions_response_9_text': self.mq_ilias_response_text_9[i],
                    'definitions_response_10_text': self.mq_ilias_response_text_10[i],
                    'definitions_response_1_img_label': self.mq_ilias_response_img_label_1[i],
                    'definitions_response_2_img_label': self.mq_ilias_response_img_label_2[i],
                    'definitions_response_3_img_label': self.mq_ilias_response_img_label_3[i],
                    'definitions_response_4_img_label': self.mq_ilias_response_img_label_4[i],
                    'definitions_response_5_img_label': self.mq_ilias_response_img_label_5[i],
                    'definitions_response_6_img_label': self.mq_ilias_response_img_label_6[i],
                    'definitions_response_7_img_label': self.mq_ilias_response_img_label_7[i],
                    'definitions_response_8_img_label': self.mq_ilias_response_img_label_8[i],
                    'definitions_response_9_img_label': self.mq_ilias_response_img_label_9[i],
                    'definitions_response_10_img_label': self.mq_ilias_response_img_label_10[i],
                    'definitions_response_1_img_path': "",
                    'definitions_response_2_img_path': "",
                    'definitions_response_3_img_path': "",
                    'definitions_response_4_img_path': "",
                    'definitions_response_5_img_path': "",
                    'definitions_response_6_img_path': "",
                    'definitions_response_7_img_path': "",
                    'definitions_response_8_img_path': "",
                    'definitions_response_9_img_path': "",
                    'definitions_response_10_img_path': "",
                    'definitions_response_1_img_string_base64_encoded': self.mq_ilias_response_img_string_base64_encoded_1[i],
                    'definitions_response_2_img_string_base64_encoded': self.mq_ilias_response_img_string_base64_encoded_2[i],
                    'definitions_response_3_img_string_base64_encoded': self.mq_ilias_response_img_string_base64_encoded_3[i],
                    'definitions_response_4_img_string_base64_encoded': self.mq_ilias_response_img_string_base64_encoded_4[i],
                    'definitions_response_5_img_string_base64_encoded': self.mq_ilias_response_img_string_base64_encoded_5[i],
                    'definitions_response_6_img_string_base64_encoded': self.mq_ilias_response_img_string_base64_encoded_6[i],
                    'definitions_response_7_img_string_base64_encoded': self.mq_ilias_response_img_string_base64_encoded_7[i],
                    'definitions_response_8_img_string_base64_encoded': self.mq_ilias_response_img_string_base64_encoded_8[i],
                    'definitions_response_9_img_string_base64_encoded': self.mq_ilias_response_img_string_base64_encoded_9[i],
                    'definitions_response_10_img_string_base64_encoded': self.mq_ilias_response_img_string_base64_encoded_10[i],

                    'terms_response_1_text': "",
                    'terms_response_2_text': "",
                    'terms_response_3_text': "",
                    'terms_response_4_text': "",
                    'terms_response_5_text': "",
                    'terms_response_6_text': "",
                    'terms_response_7_text': "",
                    'terms_response_8_text': "",
                    'terms_response_9_text': "",
                    'terms_response_10_text': "",
                    'terms_response_1_img_label': " ",
                    'terms_response_2_img_label': "",
                    'terms_response_3_img_label': "",
                    'terms_response_4_img_label': "",
                    'terms_response_5_img_label': "",
                    'terms_response_6_img_label': "",
                    'terms_response_7_img_label': "",
                    'terms_response_8_img_label': "",
                    'terms_response_9_img_label': "",
                    'terms_response_10_img_label': "",
                    'terms_response_1_img_path': "",
                    'terms_response_2_img_path': "",
                    'terms_response_3_img_path': "",
                    'terms_response_4_img_path': "",
                    'terms_response_5_img_path': "",
                    'terms_response_6_img_path': "",
                    'terms_response_7_img_path': "",
                    'terms_response_8_img_path': "",
                    'terms_response_9_img_path': "",
                    'terms_response_10_img_path': "",
                    'terms_response_1_img_string_base64_encoded': "",
                    'terms_response_2_img_string_base64_encoded': "",
                    'terms_response_3_img_string_base64_encoded': "",
                    'terms_response_4_img_string_base64_encoded': "",
                    'terms_response_5_img_string_base64_encoded': "",
                    'terms_response_6_img_string_base64_encoded': "",
                    'terms_response_7_img_string_base64_encoded': "",
                    'terms_response_8_img_string_base64_encoded': "",
                    'terms_response_9_img_string_base64_encoded': "",
                    'terms_response_10_img_string_base64_encoded': "",

                    'assignment_pairs_definition_1': self.mq_matching_id_1[i],
                    'assignment_pairs_definition_2': self.mq_matching_id_2[i],
                    'assignment_pairs_definition_3': self.mq_matching_id_3[i],
                    'assignment_pairs_definition_4': self.mq_matching_id_4[i],
                    'assignment_pairs_definition_5': self.mq_matching_id_5[i],
                    'assignment_pairs_definition_6': self.mq_matching_id_6[i],
                    'assignment_pairs_definition_7': self.mq_matching_id_7[i],
                    'assignment_pairs_definition_8': self.mq_matching_id_8[i],
                    'assignment_pairs_definition_9': self.mq_matching_id_9[i],
                    'assignment_pairs_definition_10': self.mq_matching_id_10[i],
                    'assignment_pairs_term_1': "",
                    'assignment_pairs_term_2': "",
                    'assignment_pairs_term_3': "",
                    'assignment_pairs_term_4': "",
                    'assignment_pairs_term_5': "",
                    'assignment_pairs_term_6': "",
                    'assignment_pairs_term_7': "",
                    'assignment_pairs_term_8': "",
                    'assignment_pairs_term_9': "",
                    'assignment_pairs_term_10': "",
                    'assignment_pairs_1_pts': self.mq_matching_id_points_1[i],
                    'assignment_pairs_2_pts': self.mq_matching_id_points_2[i],
                    'assignment_pairs_3_pts': self.mq_matching_id_points_3[i],
                    'assignment_pairs_4_pts': self.mq_matching_id_points_4[i],
                    'assignment_pairs_5_pts': self.mq_matching_id_points_5[i],
                    'assignment_pairs_6_pts': self.mq_matching_id_points_6[i],
                    'assignment_pairs_7_pts': self.mq_matching_id_points_7[i],
                    'assignment_pairs_8_pts': self.mq_matching_id_points_8[i],
                    'assignment_pairs_9_pts': self.mq_matching_id_points_9[i],
                    'assignment_pairs_10_pts': self.mq_matching_id_points_10[i],

                    'picture_preview_pixel': "",


                    'description_img_name_1': self.ilias_test_question_description_image_name_1[i],
                    'description_img_data_1': self.ilias_test_question_description_image_data_1[i],
                    'description_img_path_1': self.ilias_test_question_description_image_uri_1[i],

                    'description_img_name_2': "",
                    'description_img_data_2': "",
                    'description_img_path_2': "",

                    'description_img_name_3': "",
                    'description_img_data_3': "",
                    'description_img_path_3': "",

                    'test_time': self.ilias_test_duration[int(self.ilias_question_type_mq_question_index[i])],
                    'var_number': "",
                    'res_number': "",
                    'question_pool_tag': "",
                    'question_author': self.ilias_question_author[int(self.ilias_question_type_mq_question_index[i])]
                }
            )
            print(str(i+1) + ": Zuordnungsfrage: " + str(self.ilias_question_title[int(self.ilias_question_type_mq_question_index[i])]) + " in DB gespeichert")

        # Commit Changes
        connect.commit()

        # Close Connection
        connect.close()

####### Sonstige Funktionen
    def split_description_main_from_img(self, ilias_test_question_description):

        self.ilias_test_question_description = ilias_test_question_description

        self.test_list1 = []
        self.test_list1_l_join = []

        for i in range(len(self.ilias_test_question_description)):


            # Text aus Fach übernehmen
            self.test_neu1 = self.ilias_test_question_description[i]

            #Text auftrennen nach Beschreibung und IMG
            self.test_list1 = self.test_neu1.split('</p>')

            # IMG teil löschen
            for i in range(len(self.test_list1)):
                if "img" in self.test_list1[i]:
                    self.test_list1.pop(i)
                    break



            self.test_list1_l_join.append('</p>'.join(self.test_list1))


        for i in range(len(self.test_list1_l_join)):
            self.test_list1_l_join[i] = self.test_list1_l_join[i].replace('<p>', "")
            self.test_list1_l_join[i] = self.test_list1_l_join[i].replace('</p>', "")

        return self.test_list1_l_join


