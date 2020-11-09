




from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
from tkinter import ttk
import sqlite3                              #verwendet für mySQL Datenbank
import xml.etree.ElementTree as ET
import os
import pathlib
import base64




class Import_ilias_test_file:

    def __init__(self):



        filename = filedialog.askdirectory(initialdir=pathlib.Path().absolute(), title="Select a File")
        self.select_test_import_file = filename


        self.ilias_folder_name = self.select_test_import_file .rsplit('/', 1)[-1]
        self.ilias_folder_name_split1 = self.ilias_folder_name[:15]
        self.ilias_folder_name_split2 = self.ilias_folder_name.rsplit('_', 1)[-1]
        self.ilias_test_qti_file = os.path.normpath(os.path.join(self.select_test_import_file, self.ilias_folder_name_split1 + "qti_" + self.ilias_folder_name_split2 + ".xml"))


        self.ilias_test_title = []
        self.ilias_test_question_description_title = []
        self.ilias_test_question_description = []


        self.ilias_test_question_description_image_name = []
        self.ilias_test_question_description_image_data = []
        self.ilias_test_question_description_image_uri = []

        self.ilias_test_duration = []
        self.ilias_test_question_points = []

        self.ilias_test_variable1_prec, self.ilias_test_variable1_divby, self.ilias_test_variable1_min, self.ilias_test_variable1_max = [], [], [], []
        self.ilias_test_variable2_prec, self.ilias_test_variable2_divby, self.ilias_test_variable2_min, self.ilias_test_variable2_max = [], [], [], []
        self.ilias_test_variable3_prec, self.ilias_test_variable3_divby, self.ilias_test_variable3_min, self.ilias_test_variable3_max = [], [], [], []
        self.ilias_test_variable4_prec, self.ilias_test_variable4_divby, self.ilias_test_variable4_min, self.ilias_test_variable4_max = [], [], [], []
        self.ilias_test_variable5_prec, self.ilias_test_variable5_divby, self.ilias_test_variable5_min, self.ilias_test_variable5_max = [], [], [], []
        self.ilias_test_variable6_prec, self.ilias_test_variable6_divby, self.ilias_test_variable6_min, self.ilias_test_variable6_max = [], [], [], []
        self.ilias_test_variable7_prec, self.ilias_test_variable7_divby, self.ilias_test_variable7_min, self.ilias_test_variable7_max = [], [], [], []
        self.ilias_test_variable8_prec, self.ilias_test_variable8_divby, self.ilias_test_variable8_min, self.ilias_test_variable8_max = [], [], [], []
        self.ilias_test_variable9_prec, self.ilias_test_variable9_divby, self.ilias_test_variable9_min, self.ilias_test_variable9_max = [], [], [], []
        self.ilias_test_variable10_prec, self.ilias_test_variable10_divby, self.ilias_test_variable10_min, self.ilias_test_variable10_max = [], [], [], []

        self.ilias_test_variable1_prec_2nd, self.ilias_test_variable1_divby_2nd, self.ilias_test_variable1_min_2nd, self.ilias_test_variable1_max_2nd = [], [], [], []
        self.ilias_test_variable2_prec_2nd, self.ilias_test_variable2_divby_2nd, self.ilias_test_variable2_min_2nd, self.ilias_test_variable2_max_2nd = [], [], [], []
        self.ilias_test_variable3_prec_2nd, self.ilias_test_variable3_divby_2nd, self.ilias_test_variable3_min_2nd, self.ilias_test_variable3_max_2nd = [], [], [], []
        self.ilias_test_variable4_prec_2nd, self.ilias_test_variable4_divby_2nd, self.ilias_test_variable4_min_2nd, self.ilias_test_variable4_max_2nd = [], [], [], []
        self.ilias_test_variable5_prec_2nd, self.ilias_test_variable5_divby_2nd, self.ilias_test_variable5_min_2nd, self.ilias_test_variable5_max_2nd = [], [], [], []
        self.ilias_test_variable6_prec_2nd, self.ilias_test_variable6_divby_2nd, self.ilias_test_variable6_min_2nd, self.ilias_test_variable6_max_2nd = [], [], [], []
        self.ilias_test_variable7_prec_2nd, self.ilias_test_variable7_divby_2nd, self.ilias_test_variable7_min_2nd, self.ilias_test_variable7_max_2nd = [], [], [], []
        self.ilias_test_variable8_prec_2nd, self.ilias_test_variable8_divby_2nd, self.ilias_test_variable8_min_2nd, self.ilias_test_variable8_max_2nd = [], [], [], []
        self.ilias_test_variable9_prec_2nd, self.ilias_test_variable9_divby_2nd, self.ilias_test_variable9_min_2nd, self.ilias_test_variable9_max_2nd = [], [], [], []
        self.ilias_test_variable10_prec_2nd, self.ilias_test_variable10_divby_2nd, self.ilias_test_variable10_min_2nd, self.ilias_test_variable10_max_2nd = [], [], [], []

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



        # Werte für die Variable 1 in der Reihenfolge: "Präzision", "divby", "range_min", "range_max",
        self.ilias_test_variable1 = []
        self.ilias_test_variable2 = []
        self.ilias_test_variable3 = []
        self.ilias_test_variable4 = []
        self.ilias_test_variable5 = []
        self.ilias_test_variable6 = []
        self.ilias_test_variable7 = []
        self.ilias_test_variable8 = []
        self.ilias_test_variable9 = []
        self.ilias_test_variable10 = []
        self.ilias_test_question_type = []
        self.ilias_test_question_type_assFormulaQuestion = []
        self.ilias_test_question_type_assFormulaQuestion_index = []
        self.ilias_test_question_type_not_FormulaQuestion = []
        self.ilias_test_question_type_not_FormulaQuestion_index = []
        self.ilias_test_question_type_single_sc_answers = []
        self.ilias_test_question_type_collection_sc_answers = []
        self.ilias_test_question_type_collection_mc_answers = []
        self.ilias_test_question_type_collection_mq_answers = []
        self.ilias_test_question_type_ff_question_index = []
        self.ilias_test_question_type_sc_question_index = []
        self.ilias_test_question_type_mc_question_index = []
        self.ilias_test_question_type_mq_question_index = []
        self.ilias_test_question_type_all_in_one_index = []





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

        self.ilias_test_result1_2nd, self.ilias_test_result1_prec_2nd, self.ilias_test_result1_tol_2nd, self.ilias_test_result1_min_2nd, self.ilias_test_result1_max_2nd, self.ilias_test_result1_pts_2nd, self.ilias_test_result1_formula_2nd = [], [], [], [], [], [], []
        self.ilias_test_result2_2nd, self.ilias_test_result2_prec_2nd, self.ilias_test_result2_tol_2nd, self.ilias_test_result2_min_2nd, self.ilias_test_result2_max_2nd, self.ilias_test_result2_pts_2nd, self.ilias_test_result2_formula_2nd = [], [], [], [], [], [], []
        self.ilias_test_result3_2nd, self.ilias_test_result3_prec_2nd, self.ilias_test_result3_tol_2nd, self.ilias_test_result3_min_2nd, self.ilias_test_result3_max_2nd, self.ilias_test_result3_pts_2nd, self.ilias_test_result3_formula_2nd = [], [], [], [], [], [], []
        self.ilias_test_result4_2nd, self.ilias_test_result4_prec_2nd, self.ilias_test_result4_tol_2nd, self.ilias_test_result4_min_2nd, self.ilias_test_result4_max_2nd, self.ilias_test_result4_pts_2nd, self.ilias_test_result4_formula_2nd = [], [], [], [], [], [], []
        self.ilias_test_result5_2nd, self.ilias_test_result5_prec_2nd, self.ilias_test_result5_tol_2nd, self.ilias_test_result5_min_2nd, self.ilias_test_result5_max_2nd, self.ilias_test_result5_pts_2nd, self.ilias_test_result5_formula_2nd = [], [], [], [], [], [], []
        self.ilias_test_result6_2nd, self.ilias_test_result6_prec_2nd, self.ilias_test_result6_tol_2nd, self.ilias_test_result6_min_2nd, self.ilias_test_result6_max_2nd, self.ilias_test_result6_pts_2nd, self.ilias_test_result6_formula_2nd = [], [], [], [], [], [], []
        self.ilias_test_result7_2nd, self.ilias_test_result7_prec_2nd, self.ilias_test_result7_tol_2nd, self.ilias_test_result7_min_2nd, self.ilias_test_result7_max_2nd, self.ilias_test_result7_pts_2nd, self.ilias_test_result7_formula_2nd = [], [], [], [], [], [], []
        self.ilias_test_result8_2nd, self.ilias_test_result8_prec_2nd, self.ilias_test_result8_tol_2nd, self.ilias_test_result8_min_2nd, self.ilias_test_result8_max_2nd, self.ilias_test_result8_pts_2nd, self.ilias_test_result8_formula_2nd = [], [], [], [], [], [], []
        self.ilias_test_result9_2nd, self.ilias_test_result9_prec_2nd, self.ilias_test_result9_tol_2nd, self.ilias_test_result9_min_2nd, self.ilias_test_result9_max_2nd, self.ilias_test_result9_pts_2nd, self.ilias_test_result9_formula_2nd = [], [], [], [], [], [], []
        self.ilias_test_result10_2nd, self.ilias_test_result10_prec_2nd, self.ilias_test_result10_tol_2nd, self.ilias_test_result10_min_2nd, self.ilias_test_result10_max_2nd, self.ilias_test_result10_pts_2nd, self.ilias_test_result10_formula_2nd = [], [], [], [], [], [], []

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





        # XML Datei zum bearbeiten einlesen
        self.mytree = ET.parse(self.ilias_test_qti_file)
        self.myroot = self.mytree.getroot()



        for item in self.myroot.iter('item'):
            #print(item.get('title'))
            self.ilias_test_title.append(item.get('title'))


        for comment in self.myroot.iter('qticomment'):
            if comment.text == None:
                comment.text = ""

        for item in self.myroot.iter('item'):
            if "" in item.find('qticomment').text:
                self.ilias_test_question_description_title.append(item.find('qticomment').text)


        for item in self.myroot.iter('item'):
            if "" in item.find('duration').text:
                self.ilias_test_duration.append(item.find('duration').text)


        for qtimetadatafield in self.myroot.iter('qtimetadatafield'):

            if qtimetadatafield.find('fieldlabel').text == "QUESTIONTYPE":
                self.ilias_test_question_type.append(qtimetadatafield.find('fieldentry').text)



            if qtimetadatafield.find('fieldlabel').text == "points":
                self.ilias_test_question_points.append(qtimetadatafield.find('fieldentry').text)

            if qtimetadatafield.find('fieldlabel').text == "$v1":
                self.ilias_test_variable1.append(qtimetadatafield.find('fieldentry').text)

            if qtimetadatafield.find('fieldlabel').text == "$v2":
                self.ilias_test_variable2.append(qtimetadatafield.find('fieldentry').text)

            if qtimetadatafield.find('fieldlabel').text == "$v3":
                self.ilias_test_variable3.append(qtimetadatafield.find('fieldentry').text)

            if qtimetadatafield.find('fieldlabel').text == "$v4":
                self.ilias_test_variable4.append(qtimetadatafield.find('fieldentry').text)

            if qtimetadatafield.find('fieldlabel').text == "$v5":
                self.ilias_test_variable5.append(qtimetadatafield.find('fieldentry').text)

            if qtimetadatafield.find('fieldlabel').text == "$v6":
                self.ilias_test_variable6.append(qtimetadatafield.find('fieldentry').text)

            if qtimetadatafield.find('fieldlabel').text == "$v7":
                self.ilias_test_variable7.append(qtimetadatafield.find('fieldentry').text)

            if qtimetadatafield.find('fieldlabel').text == "$v8":
                self.ilias_test_variable8.append(qtimetadatafield.find('fieldentry').text)

            if qtimetadatafield.find('fieldlabel').text == "$v9":
                self.ilias_test_variable9.append(qtimetadatafield.find('fieldentry').text)

            if qtimetadatafield.find('fieldlabel').text == "$v10":
                self.ilias_test_variable10.append(qtimetadatafield.find('fieldentry').text)

            if qtimetadatafield.find('fieldlabel').text == "$r1":
                self.ilias_test_result1.append(qtimetadatafield.find('fieldentry').text)

            if qtimetadatafield.find('fieldlabel').text == "$r2":
                self.ilias_test_result2.append(qtimetadatafield.find('fieldentry').text)

            if qtimetadatafield.find('fieldlabel').text == "$r3":
                self.ilias_test_result3.append(qtimetadatafield.find('fieldentry').text)

            if qtimetadatafield.find('fieldlabel').text == "$r4":
                self.ilias_test_result4.append(qtimetadatafield.find('fieldentry').text)

            if qtimetadatafield.find('fieldlabel').text == "$r5":
                self.ilias_test_result5.append(qtimetadatafield.find('fieldentry').text)

            if qtimetadatafield.find('fieldlabel').text == "$r6":
                self.ilias_test_result6.append(qtimetadatafield.find('fieldentry').text)

            if qtimetadatafield.find('fieldlabel').text == "$r7":
                self.ilias_test_result7.append(qtimetadatafield.find('fieldentry').text)

            if qtimetadatafield.find('fieldlabel').text == "$r8":
                self.ilias_test_result8.append(qtimetadatafield.find('fieldentry').text)

            if qtimetadatafield.find('fieldlabel').text == "$r9":
                self.ilias_test_result9.append(qtimetadatafield.find('fieldentry').text)

            if qtimetadatafield.find('fieldlabel').text == "$r10":
                self.ilias_test_result10.append(qtimetadatafield.find('fieldentry').text)



        #for mattext in self.myroot.iter('mattext'):
        #    self.ilias_test_question_description.append(mattext.text)






        for i in range(len(self.ilias_test_question_type)):
            if self.ilias_test_question_type[i] != "assFormulaQuestion":
                #print("index of NOT formula type question: " + str(i))
                self.ilias_test_question_type_not_FormulaQuestion_index.append(str(i))
                self.ilias_test_question_type_not_FormulaQuestion.append(self.ilias_test_title[i])


        for i in range(len(self.ilias_test_question_type)):
            if self.ilias_test_question_type[i] == "assFormulaQuestion":
                #print("index of formula type question: " + str(i))
                self.ilias_test_question_type_assFormulaQuestion_index.append(str(i))

        #for i in range(len(self.ilias_test_question_type_assFormulaQuestion_index)):
        #    print(self.ilias_test_title[int(self.ilias_test_question_type_assFormulaQuestion_index[i])])


        # SingleChoice Index suchen und speichern
        for i in range(len(self.ilias_test_question_type)):
            if self.ilias_test_question_type[i] == "assFormulaQuestion":
                self.ilias_test_question_type_ff_question_index.append(str(i))
            if self.ilias_test_question_type[i] == "SINGLE CHOICE QUESTION":
                self.ilias_test_question_type_sc_question_index.append(str(i))
            if self.ilias_test_question_type[i] == "MULTIPLE CHOICE QUESTION":
                self.ilias_test_question_type_mc_question_index.append(str(i))
            if self.ilias_test_question_type[i] == "MATCHING QUESTION":
                self.ilias_test_question_type_mq_question_index.append(str(i))
        print("&&&&&&")
        print("Formelfrage: " + str(len(self.ilias_test_question_type_ff_question_index)) + ", with index nr: " + str(self.ilias_test_question_type_ff_question_index))
        print("SingleChoice: " + str(len(self.ilias_test_question_type_sc_question_index)) + ", with  index nr: " + str(self.ilias_test_question_type_sc_question_index))
        print("MultipleChoice: " + str(len(self.ilias_test_question_type_mc_question_index)) + ", with  index nr: " + str(self.ilias_test_question_type_mc_question_index))
        print("Matching Question: " + str(len(self.ilias_test_question_type_mq_question_index)) + ", with  index nr: " + str(self.ilias_test_question_type_mq_question_index))


        print("###############")

        # for item in self.myroot.iter('item'):
        #     for presentation in item.iter('presentation'):
        #         for i in range(len(self.ilias_test_question_type_assFormulaQuestion_index)):
        #             if presentation.attrib.get('label') == self.ilias_test_title[int(self.ilias_test_question_type_assFormulaQuestion_index[i])]:
        #                 print("found!" + str(i) + "  " + str(presentation.attrib.get('label')))

        print()
        print("###############")

        self.formelfrage_flag = 0
        self.singlechoice_flag = 0
        self.multiplechoice_flag = 0
        self.matchingquestion_flag = 0


        for i in range(len(self.ilias_test_question_type)):
            if self.ilias_test_question_type[i] == "assFormulaQuestion":
                self.ilias_test_question_type[i] = "Formelfrage"
                self.formelfrage_flag = 1
            elif self.ilias_test_question_type[i] == "SINGLE CHOICE QUESTION":
                self.ilias_test_question_type[i] = "Single Choice"
                self.singlechoice_flag = 1
            elif self.ilias_test_question_type[i] == "MULTIPLE CHOICE QUESTION":
                self.ilias_test_question_type[i] = "Multiple Choice"
                self.multiplechoice_flag = 1
            elif self.ilias_test_question_type[i] == "MATCHING QUESTION":
                self.ilias_test_question_type[i] = "Matching"
                self.matchingquestion_flag = 1
            else:
                print("No Questions found")

        for flow in self.myroot.iter('flow'):
            for material in flow.iter('material'):
                if "" in material.find('mattext').text:

                    # Wenn in dem Fragentext "img" enthalten ist, gibt es immer auch ein Bild zu der Frage
                    if "il_0_mob_" in material.find('mattext').text:
                        self.ilias_test_question_description.append(material.find('mattext').text)

                        #Bildname hinzufügen
                        if material.find('matimage').attrib.get('label'):
                            self.ilias_test_question_description_image_name.append(material.find('matimage').attrib.get('label'))
                        # Bild Pfad hinzufügen
                        if material.find('matimage').attrib.get('uri'):
                            self.ilias_test_question_description_image_uri.append(material.find('matimage').attrib.get('uri'))
                    else:
                        self.ilias_test_question_description.append(material.find('mattext').text)
                        self.ilias_test_question_description_image_name.append("EMPTY")
                        self.ilias_test_question_description_image_uri.append("EMPTY")

        #for i in range(len(self.ilias_test_question_description)):
            #print(str(i) + " " + str(self.ilias_test_question_description[i]))

        print()

        #for i in range(len(self.ilias_test_title)):
        #     print(str(i) + " " + str(self.ilias_test_title[i]) + " --- " + str(self.ilias_test_question_type[i]))



        #for flow in self.myroot.iter('flow'):
         #   for response_lid in flow.iter('response_lid'):
          #      for render_choice in response_lid.iter('render_choice'):
           #         print(render_choice.find('response_label').attrib.get('ident'))
        print("####")

        prev_count = 0
        count = 0
        sc_answer_list_nr = ""
        mc_answer_list_nr = ""
        mq_answer_list_nr = ""
        self.mattext_text_all_sc_answers = []
        self.number_of_answers_per_question_sc = []
        self.all_sc_questions_points = []

        self.mattext_text_all_mc_answers = []
        self.all_mc_questions_points = []
        self.mc_questions_true_points = []
        self.mc_questions_false_points = []

        self.mattext_text_all_mq_answers = []
        self.mattext_text_all_mq_answers_collection = []
        self.response_label_mq_answers = []

        self.mattText_text_all_mq_answers = []

        self.mq_answer_matchings = []
        self.mq_answer_matching_per_question = []
        self.mq_answer_matchings_points = []
        self.mq_number_of_answers_per_question = []
        self.mq_number_of_answers_per_question_temp = []
        self.mq_images_label = []
        self.mq_images_data_string = []


        # Durch diese Iteration und Abfrage nach MCSR (=Single Choice), werden alle Antworten der SC-Fragen aufgelistet
        for response_lid in self.myroot.iter('response_lid'):
            if response_lid.attrib.get('ident') == 'MCSR':
                for render_choice in response_lid.iter('render_choice'):
                    # Zu Beginn jedes Anwort-Blocks wird ein "$" geschrieben, um hinterher zu splitten
                    sc_answer_list_nr += "$"
                    for response_label in render_choice.iter('response_label'):
                        sc_answer_list_nr += str(response_label.attrib.get('ident'))

        # Durch diese Iteration und Abfrage nach MCMR (=Multiple Choice), werden alle Antworten der MC-Fragen aufgelistet
        for response_lid in self.myroot.iter('response_lid'):
            if response_lid.attrib.get('ident') == 'MCMR':
                for render_choice in response_lid.iter('render_choice'):
                    # Zu Beginn jedes Anwort-Blocks wird ein "$" geschrieben, um hinterher zu splitten
                    mc_answer_list_nr += "$"
                    for response_label in render_choice.iter('response_label'):
                        mc_answer_list_nr += str(response_label.attrib.get('ident'))




        print("_______________")
        #print(mc_answer_list_nr)

        self.ilias_test_question_type_collection_sc_answers = sc_answer_list_nr.split("$")
        self.ilias_test_question_type_collection_sc_answers.pop(0)  # Durch split() enthält erstes Feld keine Daten

        for i in range(len(self.ilias_test_question_type_collection_sc_answers)):
            #print("Anzahl Antworten für SC-Frage " + str(i) + ": " +  str( int(max(self.ilias_test_question_type_collection_sc_answers[i]))+1))
            self.number_of_answers_per_question_sc.append(str( int(max(self.ilias_test_question_type_collection_sc_answers[i]))+1))


        self.ilias_test_question_type_collection_mc_answers = mc_answer_list_nr.split("$")
        self.ilias_test_question_type_collection_mc_answers.pop(0)  # Durch split() enthält erstes Feld keine Daten


        #for flow in self.myroot.iter('flow'):
        #    for material in flow.iter('material'):
        #        for mattext in material.iter('mattext'):
        #            self.mattext_text2.append(mattext.text)

        for response_lid in self.myroot.iter('response_lid'):
            if response_lid.attrib.get('ident') == "MCSR":   #SR -> Single Choice
                for render_choice in response_lid.iter('render_choice'):
                    for response_label in render_choice.iter('response_label'):
                        for material in response_label.iter('material'):
                            for mattext in material.iter('mattext'):
                                self.mattext_text_all_sc_answers.append(mattext.text)

            if response_lid.attrib.get('ident') == "MCMR":    #MR -> Multiple Choice
                for render_choice in response_lid.iter('render_choice'):
                    for response_label in render_choice.iter('response_label'):
                        for material in response_label.iter('material'):
                            for mattext in material.iter('mattext'):
                                self.mattext_text_all_mc_answers.append(mattext.text)

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


        # Erstes Fach enthält ein "$" und wird nicht benötigt
        if len(self.mattext_text_all_mq_answers) > 0:
            self.mattext_text_all_mq_answers.pop(0)

        self.index_counter = 0
        for i in range(len(self.mattext_text_all_mq_answers)):
            if self.mattext_text_all_mq_answers[i] == "$":
                print("found new question at index: " + str(i))
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
            mq_answer_list_nr += "$"
            for j in range(int(self.mq_number_of_answers_per_question[i])):
                mq_answer_list_nr += str(j)


        self.ilias_test_question_type_collection_mq_answers = mq_answer_list_nr.split("$")
        self.ilias_test_question_type_collection_mq_answers.pop(0)  # Durch split() enthält erstes Feld keine Daten


        ### Matching Question beinhalten Bilder, welche zugeordnet werden müssen
        ### Diese Bilder sind in base64 veschlüsselt in der .xml Datei enthalten
        ### Auslesen der base64 decodierten Bilder:

        for matimage in self.myroot.iter('matimage'):
            if matimage.attrib.get('embedded') == "base64":
                self.mq_images_label.append(matimage.attrib.get('label'))
                #self.mq_images_data_string.append(base64.b64decode(matimage.text))
                self.mq_images_data_string.append(matimage.text)


        #for t in range(len(self.mq_images_label)):
        #    with open("Export_Bilder\\" + str(self.mq_images_label[t]), "wb") as picture:
        #        picture.write(self.mq_images_data[t])



        print("NEW TEST")
        print(mq_answer_list_nr)
        print(self.ilias_test_question_type_collection_mq_answers)


        print("NEW TEST END")



        print(len(self.mattext_text_all_mq_answers))


        print("??????")
        print(self.mattext_text_all_mq_answers)
        print(self.mq_answer_matchings)
        print(self.mq_answer_matchings_points)
        print(self.mq_number_of_answers_per_question)
        print(self.mq_answer_matching_per_question)






        #print("ALL SC ANSWERS")
        #for i in range(len(self.mattext_text_all_sc_answers)):
            #print(str(i) + " SC: ---> " + str(self.mattext_text_all_sc_answers[i]))






        #print("\n")
        #print("ALL MC ANSWERS")
        #for i in range(len(self.mattext_text_all_mc_answers)):
        #    print(str(i) + " MC: ---> " + str(self.mattext_text_all_mc_answers[i]))

        #print("\n")
        #print("ALL MQ ANSWERS")
        #for i in range(len(self.mattext_text_all_mq_answers)):
        #    print(str(i) + " MQ: ---> " + str(self.mattext_text_all_mq_answers[i]))
        #for i in range(len(self.mattext_text2)):
         #   print(str(i) + "  " + str(self.mattext_text2[i]))

        print("\n")
        #print("ALL DESCRIPTIONS")
        self.description_singlechoice_del_index = []
        self.description_multiplechoice_del_index = []
        self.description_matchedquestion_del_index = []


        #for i in range(len(self.ilias_test_question_description)):
        #    print(str(i) + " Description: ---> " + str(self.ilias_test_question_description[i]))

        # Single Choice Antworten entfernen
        for i in range(len(self.ilias_test_question_description)):
            for j in range(len(self.mattext_text_all_sc_answers)):
                if self.ilias_test_question_description[i] == self.mattext_text_all_sc_answers[j]:
                    self.description_singlechoice_del_index.append(i)

        for i in range(len(self.description_singlechoice_del_index)):
            if len(self.description_singlechoice_del_index) > 0:
                self.ilias_test_question_description.pop(self.description_singlechoice_del_index[i]-i)


        # Multiple Choice Antworten entfernen
        for i in range(len(self.ilias_test_question_description)):
            for j in range(len(self.mattext_text_all_mc_answers)):
                if self.ilias_test_question_description[i] == self.mattext_text_all_mc_answers[j]:
                    self.description_multiplechoice_del_index.append(i)

        for i in range(len(self.description_multiplechoice_del_index)):
            if len(self.description_multiplechoice_del_index) > 0:
                self.ilias_test_question_description.pop(self.description_multiplechoice_del_index[i]-i)



        # Matched Questions Antworten entfernen
        for i in range(len(self.ilias_test_question_description)):
            for j in range(len(self.mattText_text_all_mq_answers)):
                if self.ilias_test_question_description[i] == self.mattText_text_all_mq_answers[j]:
                    self.description_matchedquestion_del_index.append(i)



        # Remove any dublicates, dict's können keine Elemente mehrfach besitzen. Daher werden alle doppelten Einträge entfernt
        # Doppelte Einträge entstehen wenn die Antwort bzw. die Beschreibung genau gleich lautet
        # Z.B. Zeigerdiagramm, Zeigerdiagramm
        self.description_matchedquestion_del_index = list(dict.fromkeys(self.description_matchedquestion_del_index))


        for i in range(len(self.description_matchedquestion_del_index)):
            if len(self.description_matchedquestion_del_index) > 0:
                self.ilias_test_question_description.pop(self.description_matchedquestion_del_index[i]-i)


        print("###################################")










        print("####")











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




        #print("Anzahl der Fragen: " + str(len(self.ilias_test_title)))
        #print("Anzahl der Beschreibungen: " + str(len(self.ilias_test_question_description_title)))
        #print("Anzahl der Zeiten " + str(len(self.ilias_test_duration)))
        #print("Anzahl der Punkte " + str(len(self.ilias_test_question_points)))
        #print("Anzahl der Variablen1 " + str(len(self.ilias_test_variable1)))
        #print(self.ilias_test_variable1)


        self.ilias_test_variable1_settings = []
        self.ilias_test_variable1_settings_2nd = []
        self.ilias_test_variable2_settings = []
        self.ilias_test_variable2_settings_2nd = []
        self.ilias_test_variable3_settings = []
        self.ilias_test_variable3_settings_2nd = []
        self.ilias_test_variable4_settings = []
        self.ilias_test_variable4_settings_2nd = []
        self.ilias_test_variable5_settings = []
        self.ilias_test_variable5_settings_2nd = []
        self.ilias_test_variable6_settings = []
        self.ilias_test_variable6_settings_2nd = []
        self.ilias_test_variable7_settings = []
        self.ilias_test_variable7_settings_2nd = []
        self.ilias_test_variable8_settings = []
        self.ilias_test_variable8_settings_2nd = []
        self.ilias_test_variable9_settings = []
        self.ilias_test_variable9_settings_2nd = []
        self.ilias_test_variable10_settings = []
        self.ilias_test_variable10_settings_2nd = []

        self.ilias_test_result1_settings = []
        self.ilias_test_result1_settings_2nd = []
        self.ilias_test_result2_settings = []
        self.ilias_test_result2_settings_2nd = []
        self.ilias_test_result3_settings = []
        self.ilias_test_result3_settings_2nd = []
        self.ilias_test_result4_settings = []
        self.ilias_test_result4_settings_2nd = []
        self.ilias_test_result5_settings = []
        self.ilias_test_result5_settings_2nd = []
        self.ilias_test_result6_settings = []
        self.ilias_test_result6_settings_2nd = []
        self.ilias_test_result7_settings = []
        self.ilias_test_result7_settings_2nd = []
        self.ilias_test_result8_settings = []
        self.ilias_test_result8_settings_2nd = []
        self.ilias_test_result9_settings = []
        self.ilias_test_result9_settings_2nd = []
        self.ilias_test_result10_settings = []
        self.ilias_test_result10_settings_2nd = []



        # Liste Variable 1 - Werte auftrennen nach ";"
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




        self.ilias_test_variable1_settings_2nd = self.ilias_test_variable1_settings[::2]
        self.ilias_test_variable2_settings_2nd = self.ilias_test_variable2_settings[::2]
        self.ilias_test_variable3_settings_2nd = self.ilias_test_variable3_settings[::2]
        self.ilias_test_variable4_settings_2nd = self.ilias_test_variable4_settings[::2]
        self.ilias_test_variable5_settings_2nd = self.ilias_test_variable5_settings[::2]
        self.ilias_test_variable6_settings_2nd = self.ilias_test_variable6_settings[::2]
        self.ilias_test_variable7_settings_2nd = self.ilias_test_variable7_settings[::2]
        self.ilias_test_variable8_settings_2nd = self.ilias_test_variable8_settings[::2]
        self.ilias_test_variable9_settings_2nd = self.ilias_test_variable9_settings[::2]
        self.ilias_test_variable10_settings_2nd = self.ilias_test_variable10_settings[::2]







        self.variables_collection = ""
        self.result_collection = ""

        # "$" Zeichen werden eingefügt wenn eine neue Frage gefunden wird ("assFormuaQuestion")
        # Später wird der String an den "$" getrennt um die Variablen pro Frage anzuzeigen
        for qtimetadatafield in self.myroot.iter('qtimetadatafield'):
            if qtimetadatafield.find('fieldentry').text == "assFormulaQuestion":
                self.variables_collection += '$'
                self.result_collection += '$'


            if qtimetadatafield.find('fieldlabel').text == "$v1":
                #print("$v1 -- check")
                self.variables_collection += 'v1'

            if qtimetadatafield.find('fieldlabel').text == "$v2":
                #print("$v2 -- check")
                self.variables_collection += 'v2'

            if qtimetadatafield.find('fieldlabel').text == "$v3":
                #print("$v3 -- check")
                self.variables_collection += 'v3'

            if qtimetadatafield.find('fieldlabel').text == "$v4":
                #print("$v4 -- check")
                self.variables_collection += 'v4'

            if qtimetadatafield.find('fieldlabel').text == "$v5":
                #print("$v5 -- check")
                self.variables_collection += 'v5'

            if qtimetadatafield.find('fieldlabel').text == "$v6":
                #print("$v6 -- check")
                self.variables_collection += 'v6'

            if qtimetadatafield.find('fieldlabel').text == "$v7":
                #print("$v7 -- check")
                self.variables_collection += 'v7'

            if qtimetadatafield.find('fieldlabel').text == "$v8":
                #print("$v8 -- check")
                self.variables_collection += 'v8'

            if qtimetadatafield.find('fieldlabel').text == "$v9":
                #print("$v9 -- check")
                self.variables_collection += 'v9'

            if qtimetadatafield.find('fieldlabel').text == "$v10":
                #print("$v10 -- check")
                self.variables_collection += 'v10'

            if qtimetadatafield.find('fieldlabel').text == "$r1":
                #print("$v10 -- check")
                self.result_collection += 'r1'
            if qtimetadatafield.find('fieldlabel').text == "$r2":
                #print("$v10 -- check")
                self.result_collection += 'r2'
            if qtimetadatafield.find('fieldlabel').text == "$r3":
                #print("$v10 -- check")
                self.result_collection += 'r3'
            if qtimetadatafield.find('fieldlabel').text == "$r4":
                #print("$v10 -- check")
                self.result_collection += 'r4'
            if qtimetadatafield.find('fieldlabel').text == "$r5":
                #print("$v10 -- check")
                self.result_collection += 'r5'
            if qtimetadatafield.find('fieldlabel').text == "$r6":
                #print("$v10 -- check")
                self.result_collection += 'r6'
            if qtimetadatafield.find('fieldlabel').text == "$r7":
                #print("$v10 -- check")
                self.result_collection += 'r7'
            if qtimetadatafield.find('fieldlabel').text == "$r8":
                #print("$v10 -- check")
                self.result_collection += 'r8'
            if qtimetadatafield.find('fieldlabel').text == "$r9":
                #print("$v10 -- check")
                self.result_collection += 'r9'
            if qtimetadatafield.find('fieldlabel').text == "$r10":
                #print("$v10 -- check")
                self.result_collection += 'r10'


        #print("SHOW ALL COLLECTIONS")
        #print(self.variables_collection)
        #print(self.result_collection)



        self.vari_collection = []
        self.res_collection = []
        self.vari_collection = self.variables_collection.split('$')
        self.vari_collection.pop(0)
        self.res_collection = self.result_collection.split('$')
        self.res_collection.pop(0)


        self.var1_count = 0
        for i in range(0, len(self.ilias_test_variable1_settings_2nd), 6):
            self.ilias_test_variable1_prec_2nd.append(self.ilias_test_variable1_settings_2nd[i].rsplit(':', 1)[-1])
            self.ilias_test_variable1_divby_2nd.append(self.ilias_test_variable1_settings_2nd[i + 1][5:][:-1])
            self.ilias_test_variable1_min_2nd.append(self.ilias_test_variable1_settings_2nd[i + 2].rsplit(':', 1)[-1])
            self.ilias_test_variable1_max_2nd.append(self.ilias_test_variable1_settings_2nd[i + 3].rsplit(':', 1)[-1])

        for i in range(len(self.vari_collection)):
            if "v1" in self.vari_collection[i]:
                self.ilias_test_variable1_prec.append(self.ilias_test_variable1_prec_2nd[self.var1_count])
                self.ilias_test_variable1_divby.append(self.ilias_test_variable1_divby_2nd[self.var1_count])
                self.ilias_test_variable1_min.append(self.ilias_test_variable1_min_2nd[self.var1_count])
                self.ilias_test_variable1_max.append(self.ilias_test_variable1_max_2nd[self.var1_count])
                self.var1_count = self.var1_count + 1

            else:
                self.ilias_test_variable1_prec.append(" ")
                self.ilias_test_variable1_divby.append(" ")
                self.ilias_test_variable1_min.append(" ")
                self.ilias_test_variable1_max.append(" ")

        self.var2_count = 0
        for i in range(0, len(self.ilias_test_variable2_settings_2nd), 6):
            self.ilias_test_variable2_prec_2nd.append(self.ilias_test_variable2_settings_2nd[i].rsplit(':', 1)[-1])
            self.ilias_test_variable2_divby_2nd.append(self.ilias_test_variable2_settings_2nd[i + 1][5:][:-1])
            self.ilias_test_variable2_min_2nd.append(self.ilias_test_variable2_settings_2nd[i + 2].rsplit(':', 1)[-1])
            self.ilias_test_variable2_max_2nd.append(self.ilias_test_variable2_settings_2nd[i + 3].rsplit(':', 1)[-1])

        for i in range(len(self.vari_collection)):
            if "v2" in self.vari_collection[i]:
                self.ilias_test_variable2_prec.append(self.ilias_test_variable2_prec_2nd[self.var2_count])
                self.ilias_test_variable2_divby.append(self.ilias_test_variable2_divby_2nd[self.var2_count])
                self.ilias_test_variable2_min.append(self.ilias_test_variable2_min_2nd[self.var2_count])
                self.ilias_test_variable2_max.append(self.ilias_test_variable2_max_2nd[self.var2_count])
                self.var2_count = self.var2_count + 1

            else:
                self.ilias_test_variable2_prec.append(" ")
                self.ilias_test_variable2_divby.append(" ")
                self.ilias_test_variable2_min.append(" ")
                self.ilias_test_variable2_max.append(" ")

        self.var3_count = 0
        for i in range(0, len(self.ilias_test_variable3_settings_2nd), 6):
            self.ilias_test_variable3_prec_2nd.append(self.ilias_test_variable3_settings_2nd[i].rsplit(':', 1)[-1])
            self.ilias_test_variable3_divby_2nd.append(self.ilias_test_variable3_settings_2nd[i + 1][5:][:-1])
            self.ilias_test_variable3_min_2nd.append(self.ilias_test_variable3_settings_2nd[i + 2].rsplit(':', 1)[-1])
            self.ilias_test_variable3_max_2nd.append(self.ilias_test_variable3_settings_2nd[i + 3].rsplit(':', 1)[-1])

        for i in range(len(self.vari_collection)):
            if "v3" in self.vari_collection[i]:
                self.ilias_test_variable3_prec.append(self.ilias_test_variable3_prec_2nd[self.var3_count])
                self.ilias_test_variable3_divby.append(self.ilias_test_variable3_divby_2nd[self.var3_count])
                self.ilias_test_variable3_min.append(self.ilias_test_variable3_min_2nd[self.var3_count])
                self.ilias_test_variable3_max.append(self.ilias_test_variable3_max_2nd[self.var3_count])
                self.var3_count = self.var3_count + 1

            else:
                self.ilias_test_variable3_prec.append(" ")
                self.ilias_test_variable3_divby.append(" ")
                self.ilias_test_variable3_min.append(" ")
                self.ilias_test_variable3_max.append(" ")

        self.var4_count = 0
        for i in range(0, len(self.ilias_test_variable4_settings_2nd), 6):
            self.ilias_test_variable4_prec_2nd.append(self.ilias_test_variable4_settings_2nd[i].rsplit(':', 1)[-1])
            self.ilias_test_variable4_divby_2nd.append(self.ilias_test_variable4_settings_2nd[i + 1][5:][:-1])
            self.ilias_test_variable4_min_2nd.append(self.ilias_test_variable4_settings_2nd[i + 2].rsplit(':', 1)[-1])
            self.ilias_test_variable4_max_2nd.append(self.ilias_test_variable4_settings_2nd[i + 3].rsplit(':', 1)[-1])

        for i in range(len(self.vari_collection)):
            if "v4" in self.vari_collection[i]:
                self.ilias_test_variable4_prec.append(self.ilias_test_variable4_prec_2nd[self.var4_count])
                self.ilias_test_variable4_divby.append(self.ilias_test_variable4_divby_2nd[self.var4_count])
                self.ilias_test_variable4_min.append(self.ilias_test_variable4_min_2nd[self.var4_count])
                self.ilias_test_variable4_max.append(self.ilias_test_variable4_max_2nd[self.var4_count])
                self.var4_count = self.var4_count + 1

            else:
                self.ilias_test_variable4_prec.append(" ")
                self.ilias_test_variable4_divby.append(" ")
                self.ilias_test_variable4_min.append(" ")
                self.ilias_test_variable4_max.append(" ")


        self.var5_count = 0
        for i in range(0, len(self.ilias_test_variable5_settings_2nd), 6):
            self.ilias_test_variable5_prec_2nd.append(self.ilias_test_variable5_settings_2nd[i].rsplit(':', 1)[-1])
            self.ilias_test_variable5_divby_2nd.append(self.ilias_test_variable5_settings_2nd[i + 1][5:][:-1])
            self.ilias_test_variable5_min_2nd.append(self.ilias_test_variable5_settings_2nd[i + 2].rsplit(':', 1)[-1])
            self.ilias_test_variable5_max_2nd.append(self.ilias_test_variable5_settings_2nd[i + 3].rsplit(':', 1)[-1])

        for i in range(len(self.vari_collection)):
            if "v5" in self.vari_collection[i]:
                self.ilias_test_variable5_prec.append(self.ilias_test_variable5_prec_2nd[self.var5_count])
                self.ilias_test_variable5_divby.append(self.ilias_test_variable5_divby_2nd[self.var5_count])
                self.ilias_test_variable5_min.append(self.ilias_test_variable5_min_2nd[self.var5_count])
                self.ilias_test_variable5_max.append(self.ilias_test_variable5_max_2nd[self.var5_count])
                self.var5_count = self.var5_count + 1

            else:
                self.ilias_test_variable5_prec.append(" ")
                self.ilias_test_variable5_divby.append(" ")
                self.ilias_test_variable5_min.append(" ")
                self.ilias_test_variable5_max.append(" ")


        self.var6_count = 0
        for i in range(0, len(self.ilias_test_variable6_settings_2nd), 6):
                self.ilias_test_variable6_prec_2nd.append(self.ilias_test_variable6_settings_2nd[i].rsplit(':', 1)[-1])
                self.ilias_test_variable6_divby_2nd.append(self.ilias_test_variable6_settings_2nd[i + 1][5:][:-1])
                self.ilias_test_variable6_min_2nd.append(self.ilias_test_variable6_settings_2nd[i + 2].rsplit(':', 1)[-1])
                self.ilias_test_variable6_max_2nd.append(self.ilias_test_variable6_settings_2nd[i + 3].rsplit(':', 1)[-1])

        for i in range(len(self.vari_collection)):
            if "v6" in self.vari_collection[i]:
                self.ilias_test_variable6_prec.append(self.ilias_test_variable6_prec_2nd[self.var6_count])
                self.ilias_test_variable6_divby.append(self.ilias_test_variable6_divby_2nd[self.var6_count])
                self.ilias_test_variable6_min.append(self.ilias_test_variable6_min_2nd[self.var6_count])
                self.ilias_test_variable6_max.append(self.ilias_test_variable6_max_2nd[self.var6_count])
                self.var6_count = self.var6_count + 1

            else:
                self.ilias_test_variable6_prec.append(" ")
                self.ilias_test_variable6_divby.append(" ")
                self.ilias_test_variable6_min.append(" ")
                self.ilias_test_variable6_max.append(" ")


        self.var7_count = 0
        for i in range(0, len(self.ilias_test_variable7_settings_2nd), 6):
                self.ilias_test_variable7_prec_2nd.append(self.ilias_test_variable7_settings_2nd[i].rsplit(':', 1)[-1])
                self.ilias_test_variable7_divby_2nd.append(self.ilias_test_variable7_settings_2nd[i + 1][5:][:-1])
                self.ilias_test_variable7_min_2nd.append(self.ilias_test_variable7_settings_2nd[i + 2].rsplit(':', 1)[-1])
                self.ilias_test_variable7_max_2nd.append(self.ilias_test_variable7_settings_2nd[i + 3].rsplit(':', 1)[-1])

        for i in range(len(self.vari_collection)):
            if "v7" in self.vari_collection[i]:
                self.ilias_test_variable7_prec.append(self.ilias_test_variable7_prec_2nd[self.var7_count])
                self.ilias_test_variable7_divby.append(self.ilias_test_variable7_divby_2nd[self.var7_count])
                self.ilias_test_variable7_min.append(self.ilias_test_variable7_min_2nd[self.var7_count])
                self.ilias_test_variable7_max.append(self.ilias_test_variable7_max_2nd[self.var7_count])
                self.var7_count = self.var7_count + 1

            else:
                self.ilias_test_variable7_prec.append(" ")
                self.ilias_test_variable7_divby.append(" ")
                self.ilias_test_variable7_min.append(" ")
                self.ilias_test_variable7_max.append(" ")


        self.var8_count = 0
        for i in range(0, len(self.ilias_test_variable8_settings_2nd), 6):
                self.ilias_test_variable8_prec_2nd.append(self.ilias_test_variable8_settings_2nd[i].rsplit(':', 1)[-1])
                self.ilias_test_variable8_divby_2nd.append(self.ilias_test_variable8_settings_2nd[i + 1][5:][:-1])
                self.ilias_test_variable8_min_2nd.append(self.ilias_test_variable8_settings_2nd[i + 2].rsplit(':', 1)[-1])
                self.ilias_test_variable8_max_2nd.append(self.ilias_test_variable8_settings_2nd[i + 3].rsplit(':', 1)[-1])

        for i in range(len(self.vari_collection)):
            if "v8" in self.vari_collection[i]:
                self.ilias_test_variable8_prec.append(self.ilias_test_variable8_prec_2nd[self.var8_count])
                self.ilias_test_variable8_divby.append(self.ilias_test_variable8_divby_2nd[self.var8_count])
                self.ilias_test_variable8_min.append(self.ilias_test_variable8_min_2nd[self.var8_count])
                self.ilias_test_variable8_max.append(self.ilias_test_variable8_max_2nd[self.var8_count])
                self.var8_count = self.var8_count + 1

            else:
                self.ilias_test_variable8_prec.append(" ")
                self.ilias_test_variable8_divby.append(" ")
                self.ilias_test_variable8_min.append(" ")
                self.ilias_test_variable8_max.append(" ")


        self.var9_count = 0
        for i in range(0, len(self.ilias_test_variable9_settings_2nd), 6):
            self.ilias_test_variable9_prec_2nd.append(self.ilias_test_variable9_settings_2nd[i].rsplit(':', 1)[-1])
            self.ilias_test_variable9_divby_2nd.append(self.ilias_test_variable9_settings_2nd[i + 1][5:][:-1])
            self.ilias_test_variable9_min_2nd.append(self.ilias_test_variable9_settings_2nd[i + 2].rsplit(':', 1)[-1])
            self.ilias_test_variable9_max_2nd.append(self.ilias_test_variable9_settings_2nd[i + 3].rsplit(':', 1)[-1])

        for i in range(len(self.vari_collection)):
            if "v9" in self.vari_collection[i]:
                self.ilias_test_variable9_prec.append(self.ilias_test_variable9_prec_2nd[self.var9_count])
                self.ilias_test_variable9_divby.append(self.ilias_test_variable9_divby_2nd[self.var9_count])
                self.ilias_test_variable9_min.append(self.ilias_test_variable9_min_2nd[self.var9_count])
                self.ilias_test_variable9_max.append(self.ilias_test_variable9_max_2nd[self.var9_count])
                self.var9_count = self.var9_count + 1

            else:
                self.ilias_test_variable9_prec.append(" ")
                self.ilias_test_variable9_divby.append(" ")
                self.ilias_test_variable9_min.append(" ")
                self.ilias_test_variable9_max.append(" ")


        self.var10_count = 0
        for i in range(0, len(self.ilias_test_variable10_settings_2nd), 6):
            self.ilias_test_variable10_prec_2nd.append(self.ilias_test_variable10_settings_2nd[i].rsplit(':', 1)[-1])
            self.ilias_test_variable10_divby_2nd.append(self.ilias_test_variable10_settings_2nd[i + 1][5:][:-1])
            self.ilias_test_variable10_min_2nd.append(self.ilias_test_variable10_settings_2nd[i + 2].rsplit(':', 1)[-1])
            self.ilias_test_variable10_max_2nd.append(self.ilias_test_variable10_settings_2nd[i + 3].rsplit(':', 1)[-1])

        for i in range(len(self.vari_collection)):
            if "v10" in self.vari_collection[i]:
                self.ilias_test_variable10_prec.append(self.ilias_test_variable10_prec_2nd[self.var10_count])
                self.ilias_test_variable10_divby.append(self.ilias_test_variable10_divby_2nd[self.var10_count])
                self.ilias_test_variable10_min.append(self.ilias_test_variable10_min_2nd[self.var10_count])
                self.ilias_test_variable10_max.append(self.ilias_test_variable10_max_2nd[self.var10_count])
                self.var10_count = self.var10_count + 1

            else:
                self.ilias_test_variable10_prec.append(" ")
                self.ilias_test_variable10_divby.append(" ")
                self.ilias_test_variable10_min.append(" ")
                self.ilias_test_variable10_max.append(" ")


















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


        self.ilias_test_result1_settings_2nd = self.ilias_test_result1_settings[::2]
        self.ilias_test_result2_settings_2nd = self.ilias_test_result2_settings[::2]
        self.ilias_test_result3_settings_2nd = self.ilias_test_result3_settings[::2]
        self.ilias_test_result4_settings_2nd = self.ilias_test_result4_settings[::2]
        self.ilias_test_result5_settings_2nd = self.ilias_test_result5_settings[::2]
        self.ilias_test_result6_settings_2nd = self.ilias_test_result6_settings[::2]
        self.ilias_test_result7_settings_2nd = self.ilias_test_result7_settings[::2]
        self.ilias_test_result8_settings_2nd = self.ilias_test_result8_settings[::2]
        self.ilias_test_result9_settings_2nd = self.ilias_test_result9_settings[::2]



        for i in range(len(self.ilias_test_result1_settings_2nd)):
            self.ilias_test_result1_settings_2nd[i] = self.ilias_test_result1_settings_2nd[i].replace('"', '')

        for i in range(len(self.ilias_test_result2_settings_2nd)):
            self.ilias_test_result2_settings_2nd[i] = self.ilias_test_result2_settings_2nd[i].replace('"', '')

        for i in range(len(self.ilias_test_result3_settings_2nd)):
            self.ilias_test_result3_settings_2nd[i] = self.ilias_test_result3_settings_2nd[i].replace('"', '')

        for i in range(len(self.ilias_test_result4_settings_2nd)):
            self.ilias_test_result4_settings_2nd[i] = self.ilias_test_result4_settings_2nd[i].replace('"', '')

        for i in range(len(self.ilias_test_result5_settings_2nd)):
            self.ilias_test_result5_settings_2nd[i] = self.ilias_test_result5_settings_2nd[i].replace('"', '')

        for i in range(len(self.ilias_test_result6_settings_2nd)):
            self.ilias_test_result6_settings_2nd[i] = self.ilias_test_result6_settings_2nd[i].replace('"', '')

        for i in range(len(self.ilias_test_result7_settings_2nd)):
            self.ilias_test_result7_settings_2nd[i] = self.ilias_test_result7_settings_2nd[i].replace('"', '')

        for i in range(len(self.ilias_test_result8_settings_2nd)):
            self.ilias_test_result8_settings_2nd[i] = self.ilias_test_result8_settings_2nd[i].replace('"', '')

        for i in range(len(self.ilias_test_result9_settings_2nd)):
            self.ilias_test_result9_settings_2nd[i] = self.ilias_test_result9_settings_2nd[i].replace('"', '')

        for i in range(len(self.ilias_test_result10_settings_2nd)):
            self.ilias_test_result10_settings_2nd[i] = self.ilias_test_result10_settings_2nd[i].replace('"', '')


        self.res1_count = 0
        for i in range(0, len(self.ilias_test_result1_settings_2nd), 10):
            self.ilias_test_result1_prec_2nd.append(self.ilias_test_result1_settings_2nd[i].rsplit(':', 1)[-1])
            self.ilias_test_result1_tol_2nd.append(self.ilias_test_result1_settings_2nd[i+1].rsplit(':', 1)[-1])
            self.ilias_test_result1_min_2nd.append(self.ilias_test_result1_settings_2nd[i+2].rsplit(':', 1)[-1])
            self.ilias_test_result1_max_2nd.append(self.ilias_test_result1_settings_2nd[i+3].rsplit(':', 1)[-1])
            self.ilias_test_result1_pts_2nd.append(self.ilias_test_result1_settings_2nd[i+4].rsplit(':', 1)[-1])
            self.ilias_test_result1_formula_2nd.append(self.ilias_test_result1_settings_2nd[i+5].rsplit(':', 1)[-1])

        for i in range(len(self.res_collection)):
            if "r1" in self.res_collection[i]:
                self.ilias_test_result1_prec.append(self.ilias_test_result1_prec_2nd[self.res1_count])
                self.ilias_test_result1_tol.append(self.ilias_test_result1_tol_2nd[self.res1_count])
                self.ilias_test_result1_min.append(self.ilias_test_result1_min_2nd[self.res1_count])
                self.ilias_test_result1_max.append(self.ilias_test_result1_max_2nd[self.res1_count])
                self.ilias_test_result1_pts.append(self.ilias_test_result1_pts_2nd[self.res1_count])
                self.ilias_test_result1_formula.append(self.ilias_test_result1_formula_2nd[self.res1_count])
                self.res1_count = self.res1_count + 1

            else:
                self.ilias_test_result1_prec.append(" ")
                self.ilias_test_result1_tol.append(" ")
                self.ilias_test_result1_min.append(" ")
                self.ilias_test_result1_max.append(" ")
                self.ilias_test_result1_pts.append(" ")
                self.ilias_test_result1_formula.append(" ")


        self.res2_count = 0
        for i in range(0, len(self.ilias_test_result2_settings_2nd), 10):
            self.ilias_test_result2_prec_2nd.append(self.ilias_test_result2_settings_2nd[i].rsplit(':', 1)[-1])
            self.ilias_test_result2_tol_2nd.append(self.ilias_test_result2_settings_2nd[i+1].rsplit(':', 1)[-1])
            self.ilias_test_result2_min_2nd.append(self.ilias_test_result2_settings_2nd[i+2].rsplit(':', 1)[-1])
            self.ilias_test_result2_max_2nd.append(self.ilias_test_result2_settings_2nd[i+3].rsplit(':', 1)[-1])
            self.ilias_test_result2_pts_2nd.append(self.ilias_test_result2_settings_2nd[i+4].rsplit(':', 1)[-1])
            self.ilias_test_result2_formula_2nd.append(self.ilias_test_result2_settings_2nd[i+5].rsplit(':', 1)[-1])

        for i in range(len(self.res_collection)):
            if "r2" in self.res_collection[i]:
                self.ilias_test_result2_prec.append(self.ilias_test_result2_prec_2nd[self.res2_count])
                self.ilias_test_result2_tol.append(self.ilias_test_result2_tol_2nd[self.res2_count])
                self.ilias_test_result2_min.append(self.ilias_test_result2_min_2nd[self.res2_count])
                self.ilias_test_result2_max.append(self.ilias_test_result2_max_2nd[self.res2_count])
                self.ilias_test_result2_pts.append(self.ilias_test_result2_pts_2nd[self.res2_count])
                self.ilias_test_result2_formula.append(self.ilias_test_result2_formula_2nd[self.res2_count])
                self.res2_count = self.res2_count + 1

            else:
                self.ilias_test_result2_prec.append(" ")
                self.ilias_test_result2_tol.append(" ")
                self.ilias_test_result2_min.append(" ")
                self.ilias_test_result2_max.append(" ")
                self.ilias_test_result2_pts.append(" ")
                self.ilias_test_result2_formula.append(" ")


        self.res3_count = 0
        for i in range(0, len(self.ilias_test_result3_settings_2nd), 10):
            self.ilias_test_result3_prec_2nd.append(self.ilias_test_result3_settings_2nd[i].rsplit(':', 1)[-1])
            self.ilias_test_result3_tol_2nd.append(self.ilias_test_result3_settings_2nd[i+1].rsplit(':', 1)[-1])
            self.ilias_test_result3_min_2nd.append(self.ilias_test_result3_settings_2nd[i+2].rsplit(':', 1)[-1])
            self.ilias_test_result3_max_2nd.append(self.ilias_test_result3_settings_2nd[i+3].rsplit(':', 1)[-1])
            self.ilias_test_result3_pts_2nd.append(self.ilias_test_result3_settings_2nd[i+4].rsplit(':', 1)[-1])
            self.ilias_test_result3_formula_2nd.append(self.ilias_test_result3_settings_2nd[i+5].rsplit(':', 1)[-1])

        for i in range(len(self.res_collection)):
            if "r3" in self.res_collection[i]:
                self.ilias_test_result3_prec.append(self.ilias_test_result3_prec_2nd[self.res3_count])
                self.ilias_test_result3_tol.append(self.ilias_test_result3_tol_2nd[self.res3_count])
                self.ilias_test_result3_min.append(self.ilias_test_result3_min_2nd[self.res3_count])
                self.ilias_test_result3_max.append(self.ilias_test_result3_max_2nd[self.res3_count])
                self.ilias_test_result3_pts.append(self.ilias_test_result3_pts_2nd[self.res3_count])
                self.ilias_test_result3_formula.append(self.ilias_test_result3_formula_2nd[self.res3_count])
                self.res3_count = self.res3_count + 1

            else:
                self.ilias_test_result3_prec.append(" ")
                self.ilias_test_result3_tol.append(" ")
                self.ilias_test_result3_min.append(" ")
                self.ilias_test_result3_max.append(" ")
                self.ilias_test_result3_pts.append(" ")
                self.ilias_test_result3_formula.append(" ")



        self.res4_count = 0
        for i in range(0, len(self.ilias_test_result4_settings_2nd), 10):
            self.ilias_test_result4_prec_2nd.append(self.ilias_test_result4_settings_2nd[i].rsplit(':', 1)[-1])
            self.ilias_test_result4_tol_2nd.append(self.ilias_test_result4_settings_2nd[i+1].rsplit(':', 1)[-1])
            self.ilias_test_result4_min_2nd.append(self.ilias_test_result4_settings_2nd[i+2].rsplit(':', 1)[-1])
            self.ilias_test_result4_max_2nd.append(self.ilias_test_result4_settings_2nd[i+3].rsplit(':', 1)[-1])
            self.ilias_test_result4_pts_2nd.append(self.ilias_test_result4_settings_2nd[i+4].rsplit(':', 1)[-1])
            self.ilias_test_result4_formula_2nd.append(self.ilias_test_result4_settings_2nd[i+5].rsplit(':', 1)[-1])

        for i in range(len(self.res_collection)):
            if "r4" in self.res_collection[i]:
                self.ilias_test_result4_prec.append(self.ilias_test_result4_prec_2nd[self.res4_count])
                self.ilias_test_result4_tol.append(self.ilias_test_result4_tol_2nd[self.res4_count])
                self.ilias_test_result4_min.append(self.ilias_test_result4_min_2nd[self.res4_count])
                self.ilias_test_result4_max.append(self.ilias_test_result4_max_2nd[self.res4_count])
                self.ilias_test_result4_pts.append(self.ilias_test_result4_pts_2nd[self.res4_count])
                self.ilias_test_result4_formula.append(self.ilias_test_result4_formula_2nd[self.res4_count])
                self.res4_count = self.res4_count + 1

            else:
                self.ilias_test_result4_prec.append(" ")
                self.ilias_test_result4_tol.append(" ")
                self.ilias_test_result4_min.append(" ")
                self.ilias_test_result4_max.append(" ")
                self.ilias_test_result4_pts.append(" ")
                self.ilias_test_result4_formula.append(" ")

        self.res5_count = 0
        for i in range(0, len(self.ilias_test_result5_settings_2nd), 10):
            self.ilias_test_result5_prec_2nd.append(self.ilias_test_result5_settings_2nd[i].rsplit(':', 1)[-1])
            self.ilias_test_result5_tol_2nd.append(self.ilias_test_result5_settings_2nd[i + 1].rsplit(':', 1)[-1])
            self.ilias_test_result5_min_2nd.append(self.ilias_test_result5_settings_2nd[i + 2].rsplit(':', 1)[-1])
            self.ilias_test_result5_max_2nd.append(self.ilias_test_result5_settings_2nd[i + 3].rsplit(':', 1)[-1])
            self.ilias_test_result5_pts_2nd.append(self.ilias_test_result5_settings_2nd[i + 4].rsplit(':', 1)[-1])
            self.ilias_test_result5_formula_2nd.append(self.ilias_test_result5_settings_2nd[i + 5].rsplit(':', 1)[-1])

        for i in range(len(self.res_collection)):
            if "r5" in self.res_collection[i]:
                self.ilias_test_result5_prec.append(self.ilias_test_result5_prec_2nd[self.res5_count])
                self.ilias_test_result5_tol.append(self.ilias_test_result5_tol_2nd[self.res5_count])
                self.ilias_test_result5_min.append(self.ilias_test_result5_min_2nd[self.res5_count])
                self.ilias_test_result5_max.append(self.ilias_test_result5_max_2nd[self.res5_count])
                self.ilias_test_result5_pts.append(self.ilias_test_result5_pts_2nd[self.res5_count])
                self.ilias_test_result5_formula.append(self.ilias_test_result5_formula_2nd[self.res5_count])
                self.res5_count = self.res5_count + 1

            else:
                self.ilias_test_result5_prec.append(" ")
                self.ilias_test_result5_tol.append(" ")
                self.ilias_test_result5_min.append(" ")
                self.ilias_test_result5_max.append(" ")
                self.ilias_test_result5_pts.append(" ")
                self.ilias_test_result5_formula.append(" ")



        self.res6_count = 0
        for i in range(0, len(self.ilias_test_result6_settings_2nd), 10):
            self.ilias_test_result6_prec_2nd.append(self.ilias_test_result6_settings_2nd[i].rsplit(':', 1)[-1])
            self.ilias_test_result6_tol_2nd.append(self.ilias_test_result6_settings_2nd[i + 1].rsplit(':', 1)[-1])
            self.ilias_test_result6_min_2nd.append(self.ilias_test_result6_settings_2nd[i + 2].rsplit(':', 1)[-1])
            self.ilias_test_result6_max_2nd.append(self.ilias_test_result6_settings_2nd[i + 3].rsplit(':', 1)[-1])
            self.ilias_test_result6_pts_2nd.append(self.ilias_test_result6_settings_2nd[i + 4].rsplit(':', 1)[-1])
            self.ilias_test_result6_formula_2nd.append(self.ilias_test_result6_settings_2nd[i + 5].rsplit(':', 1)[-1])

        for i in range(len(self.res_collection)):
            if "r6" in self.res_collection[i]:
                self.ilias_test_result6_prec.append(self.ilias_test_result6_prec_2nd[self.res6_count])
                self.ilias_test_result6_tol.append(self.ilias_test_result6_tol_2nd[self.res6_count])
                self.ilias_test_result6_min.append(self.ilias_test_result6_min_2nd[self.res6_count])
                self.ilias_test_result6_max.append(self.ilias_test_result6_max_2nd[self.res6_count])
                self.ilias_test_result6_pts.append(self.ilias_test_result6_pts_2nd[self.res6_count])
                self.ilias_test_result6_formula.append(self.ilias_test_result6_formula_2nd[self.res6_count])
                self.res6_count = self.res6_count + 1

            else:
                self.ilias_test_result6_prec.append(" ")
                self.ilias_test_result6_tol.append(" ")
                self.ilias_test_result6_min.append(" ")
                self.ilias_test_result6_max.append(" ")
                self.ilias_test_result6_pts.append(" ")
                self.ilias_test_result6_formula.append(" ")


        self.res7_count = 0
        for i in range(0, len(self.ilias_test_result7_settings_2nd), 10):
            self.ilias_test_result7_prec_2nd.append(self.ilias_test_result7_settings_2nd[i].rsplit(':', 1)[-1])
            self.ilias_test_result7_tol_2nd.append(self.ilias_test_result7_settings_2nd[i + 1].rsplit(':', 1)[-1])
            self.ilias_test_result7_min_2nd.append(self.ilias_test_result7_settings_2nd[i + 2].rsplit(':', 1)[-1])
            self.ilias_test_result7_max_2nd.append(self.ilias_test_result7_settings_2nd[i + 3].rsplit(':', 1)[-1])
            self.ilias_test_result7_pts_2nd.append(self.ilias_test_result7_settings_2nd[i + 4].rsplit(':', 1)[-1])
            self.ilias_test_result7_formula_2nd.append(self.ilias_test_result7_settings_2nd[i + 5].rsplit(':', 1)[-1])

        for i in range(len(self.res_collection)):
            if "r7" in self.res_collection[i]:
                self.ilias_test_result7_prec.append(self.ilias_test_result7_prec_2nd[self.res7_count])
                self.ilias_test_result7_tol.append(self.ilias_test_result7_tol_2nd[self.res7_count])
                self.ilias_test_result7_min.append(self.ilias_test_result7_min_2nd[self.res7_count])
                self.ilias_test_result7_max.append(self.ilias_test_result7_max_2nd[self.res7_count])
                self.ilias_test_result7_pts.append(self.ilias_test_result7_pts_2nd[self.res7_count])
                self.ilias_test_result7_formula.append(self.ilias_test_result7_formula_2nd[self.res7_count])
                self.res7_count = self.res7_count + 1

            else:
                self.ilias_test_result7_prec.append(" ")
                self.ilias_test_result7_tol.append(" ")
                self.ilias_test_result7_min.append(" ")
                self.ilias_test_result7_max.append(" ")
                self.ilias_test_result7_pts.append(" ")
                self.ilias_test_result7_formula.append(" ")


        self.res8_count = 0
        for i in range(0, len(self.ilias_test_result8_settings_2nd), 10):
            self.ilias_test_result8_prec_2nd.append(self.ilias_test_result8_settings_2nd[i].rsplit(':', 1)[-1])
            self.ilias_test_result8_tol_2nd.append(self.ilias_test_result8_settings_2nd[i + 1].rsplit(':', 1)[-1])
            self.ilias_test_result8_min_2nd.append(self.ilias_test_result8_settings_2nd[i + 2].rsplit(':', 1)[-1])
            self.ilias_test_result8_max_2nd.append(self.ilias_test_result8_settings_2nd[i + 3].rsplit(':', 1)[-1])
            self.ilias_test_result8_pts_2nd.append(self.ilias_test_result8_settings_2nd[i + 4].rsplit(':', 1)[-1])
            self.ilias_test_result8_formula_2nd.append(self.ilias_test_result8_settings_2nd[i + 5].rsplit(':', 1)[-1])

        for i in range(len(self.res_collection)):
            if "r8" in self.res_collection[i]:
                self.ilias_test_result8_prec.append(self.ilias_test_result8_prec_2nd[self.res8_count])
                self.ilias_test_result8_tol.append(self.ilias_test_result8_tol_2nd[self.res8_count])
                self.ilias_test_result8_min.append(self.ilias_test_result8_min_2nd[self.res8_count])
                self.ilias_test_result8_max.append(self.ilias_test_result8_max_2nd[self.res8_count])
                self.ilias_test_result8_pts.append(self.ilias_test_result8_pts_2nd[self.res8_count])
                self.ilias_test_result8_formula.append(self.ilias_test_result8_formula_2nd[self.res8_count])
                self.res8_count = self.res8_count + 1

            else:
                self.ilias_test_result8_prec.append(" ")
                self.ilias_test_result8_tol.append(" ")
                self.ilias_test_result8_min.append(" ")
                self.ilias_test_result8_max.append(" ")
                self.ilias_test_result8_pts.append(" ")
                self.ilias_test_result8_formula.append(" ")


        self.res9_count = 0
        for i in range(0, len(self.ilias_test_result9_settings_2nd), 10):
            self.ilias_test_result9_prec_2nd.append(self.ilias_test_result9_settings_2nd[i].rsplit(':', 1)[-1])
            self.ilias_test_result9_tol_2nd.append(self.ilias_test_result9_settings_2nd[i + 1].rsplit(':', 1)[-1])
            self.ilias_test_result9_min_2nd.append(self.ilias_test_result9_settings_2nd[i + 2].rsplit(':', 1)[-1])
            self.ilias_test_result9_max_2nd.append(self.ilias_test_result9_settings_2nd[i + 3].rsplit(':', 1)[-1])
            self.ilias_test_result9_pts_2nd.append(self.ilias_test_result9_settings_2nd[i + 4].rsplit(':', 1)[-1])
            self.ilias_test_result9_formula_2nd.append(self.ilias_test_result9_settings_2nd[i + 5].rsplit(':', 1)[-1])

        for i in range(len(self.res_collection)):
            if "r9" in self.res_collection[i]:
                self.ilias_test_result9_prec.append(self.ilias_test_result9_prec_2nd[self.res9_count])
                self.ilias_test_result9_tol.append(self.ilias_test_result9_tol_2nd[self.res9_count])
                self.ilias_test_result9_min.append(self.ilias_test_result9_min_2nd[self.res9_count])
                self.ilias_test_result9_max.append(self.ilias_test_result9_max_2nd[self.res9_count])
                self.ilias_test_result9_pts.append(self.ilias_test_result9_pts_2nd[self.res9_count])
                self.ilias_test_result9_formula.append(self.ilias_test_result9_formula_2nd[self.res9_count])
                self.res9_count = self.res9_count + 1

            else:
                self.ilias_test_result9_prec.append(" ")
                self.ilias_test_result9_tol.append(" ")
                self.ilias_test_result9_min.append(" ")
                self.ilias_test_result9_max.append(" ")
                self.ilias_test_result9_pts.append(" ")
                self.ilias_test_result9_formula.append(" ")


        self.res10_count = 0
        for i in range(0, len(self.ilias_test_result10_settings_2nd), 10):
            self.ilias_test_result10_prec_2nd.append(self.ilias_test_result10_settings_2nd[i].rsplit(':', 1)[-1])
            self.ilias_test_result10_tol_2nd.append(self.ilias_test_result10_settings_2nd[i + 1].rsplit(':', 1)[-1])
            self.ilias_test_result10_min_2nd.append(self.ilias_test_result10_settings_2nd[i + 2].rsplit(':', 1)[-1])
            self.ilias_test_result10_max_2nd.append(self.ilias_test_result10_settings_2nd[i + 3].rsplit(':', 1)[-1])
            self.ilias_test_result10_pts_2nd.append(self.ilias_test_result10_settings_2nd[i + 4].rsplit(':', 1)[-1])
            self.ilias_test_result10_formula_2nd.append(self.ilias_test_result10_settings_2nd[i + 5].rsplit(':', 1)[-1])

        for i in range(len(self.res_collection)):
            if "r10" in self.res_collection[i]:
                self.ilias_test_result10_prec.append(self.ilias_test_result10_prec_2nd[self.res10_count])
                self.ilias_test_result10_tol.append(self.ilias_test_result10_tol_2nd[self.res10_count])
                self.ilias_test_result10_min.append(self.ilias_test_result10_min_2nd[self.res10_count])
                self.ilias_test_result10_max.append(self.ilias_test_result10_max_2nd[self.res10_count])
                self.ilias_test_result10_pts.append(self.ilias_test_result10_pts_2nd[self.res10_count])
                self.ilias_test_result10_formula.append(self.ilias_test_result10_formula_2nd[self.res10_count])
                self.res10_count = self.res10_count + 1

            else:
                self.ilias_test_result10_prec.append(" ")
                self.ilias_test_result10_tol.append(" ")
                self.ilias_test_result10_min.append(" ")
                self.ilias_test_result10_max.append(" ")
                self.ilias_test_result10_pts.append(" ")
                self.ilias_test_result10_formula.append(" ")



        for respcondition in self.myroot.iter('respcondition'):
            for varequal in respcondition.iter('varequal'):
                if varequal.attrib.get('respident') == "MCSR":
                    for setvar in respcondition.iter('setvar'):
                        #print(varequal.attrib, varequal.text, setvar.text)

                        self.all_sc_questions_points.append(setvar.text)



        for respcondition in self.myroot.iter('respcondition'):
            for varequal in respcondition.iter('varequal'):
                if varequal.attrib.get('respident') == "MCMR":
                    for setvar in respcondition.iter('setvar'):
                        #print(varequal.attrib, varequal.text, setvar.text)

                        self.all_mc_questions_points.append(setvar.text)

        # Jedes zweite ELement übernehmen [::2] mit Start beim 1. Fach (nicht das 0. Fach)
        self.mc_questions_false_points = self.all_mc_questions_points[1::2]
        self.mc_questions_true_points = self.all_mc_questions_points[::2]
        #print(self.all_mc_questions_points)
        #print(self.mc_questions_false_points)




        ######### Einfügen der Single-Choice Fragen #############################
        # Wenn in den Fragentiteln eine SingleChoice Question erkannt wird, dann sc_flag = 1

        if self.singlechoice_flag == 1:
            t =  int(max(self.ilias_test_question_type_collection_sc_answers[0])) + 1

            for i in range(len(self.ilias_test_question_type_collection_sc_answers)):
                if i == 0:
                    if "0" in self.ilias_test_question_type_collection_sc_answers[i]:
                        self.ilias_test_variable1_min.append(self.mattext_text_all_sc_answers[i])
                        self.ilias_test_variable1_prec.append(" ")
                        self.ilias_test_variable1_divby.append(" ")
                        self.ilias_test_variable1_max.append(" ")

                        self.ilias_test_result1_min.append(self.all_sc_questions_points[i])
                        self.ilias_test_result1_max.append(" ")
                        self.ilias_test_result1_prec.append(" ")
                        self.ilias_test_result1_tol.append(" ")
                        self.ilias_test_result1_pts.append(" ")
                        self.ilias_test_result1_formula.append(" ")
                    else:
                        self.ilias_test_variable1_min.append(" ")
                        self.ilias_test_variable1_prec.append(" ")
                        self.ilias_test_variable1_divby.append(" ")
                        self.ilias_test_variable1_max.append(" ")

                        self.ilias_test_result1_min.append(" ")
                        self.ilias_test_result1_max.append(" ")
                        self.ilias_test_result1_prec.append(" ")
                        self.ilias_test_result1_tol.append(" ")
                        self.ilias_test_result1_pts.append(" ")
                        self.ilias_test_result1_formula.append(" ")

                    if "1" in self.ilias_test_question_type_collection_sc_answers[i]:
                        self.ilias_test_variable2_min.append(self.mattext_text_all_sc_answers[i+1])
                        self.ilias_test_variable2_prec.append(" ")
                        self.ilias_test_variable2_divby.append(" ")
                        self.ilias_test_variable2_max.append(" ")

                        self.ilias_test_result2_min.append(self.all_sc_questions_points[i+1])
                        self.ilias_test_result2_max.append(" ")
                        self.ilias_test_result2_prec.append(" ")
                        self.ilias_test_result2_tol.append(" ")
                        self.ilias_test_result2_pts.append(" ")
                        self.ilias_test_result2_formula.append(" ")
                    else:
                        self.ilias_test_variable2_min.append(" ")
                        self.ilias_test_variable2_prec.append(" ")
                        self.ilias_test_variable2_divby.append(" ")
                        self.ilias_test_variable2_max.append(" ")

                        self.ilias_test_result2_min.append(" ")
                        self.ilias_test_result2_max.append(" ")
                        self.ilias_test_result2_prec.append(" ")
                        self.ilias_test_result2_tol.append(" ")
                        self.ilias_test_result2_pts.append(" ")
                        self.ilias_test_result2_formula.append(" ")

                    if "2" in self.ilias_test_question_type_collection_sc_answers[i]:
                        self.ilias_test_variable3_min.append(self.mattext_text_all_sc_answers[i+2])
                        self.ilias_test_variable3_prec.append(" ")
                        self.ilias_test_variable3_divby.append(" ")
                        self.ilias_test_variable3_max.append(" ")

                        self.ilias_test_result3_min.append(self.all_sc_questions_points[i+2])
                        self.ilias_test_result3_max.append(" ")
                        self.ilias_test_result3_prec.append(" ")
                        self.ilias_test_result3_tol.append(" ")
                        self.ilias_test_result3_pts.append(" ")
                        self.ilias_test_result3_formula.append(" ")
                    else:
                        self.ilias_test_variable3_min.append(" ")
                        self.ilias_test_variable3_prec.append(" ")
                        self.ilias_test_variable3_divby.append(" ")
                        self.ilias_test_variable3_max.append(" ")

                        self.ilias_test_result3_min.append(" ")
                        self.ilias_test_result3_max.append(" ")
                        self.ilias_test_result3_prec.append(" ")
                        self.ilias_test_result3_tol.append(" ")
                        self.ilias_test_result3_pts.append(" ")
                        self.ilias_test_result3_formula.append(" ")

                    if "3" in self.ilias_test_question_type_collection_sc_answers[i]:
                        self.ilias_test_variable4_min.append(self.mattext_text_all_sc_answers[i+3])
                        self.ilias_test_variable4_prec.append(" ")
                        self.ilias_test_variable4_divby.append(" ")
                        self.ilias_test_variable4_max.append(" ")

                        self.ilias_test_result4_min.append(self.all_sc_questions_points[i+3])
                        self.ilias_test_result4_max.append(" ")
                        self.ilias_test_result4_prec.append(" ")
                        self.ilias_test_result4_tol.append(" ")
                        self.ilias_test_result4_pts.append(" ")
                        self.ilias_test_result4_formula.append(" ")
                    else:
                        self.ilias_test_variable4_min.append(" ")
                        self.ilias_test_variable4_prec.append(" ")
                        self.ilias_test_variable4_divby.append(" ")
                        self.ilias_test_variable4_max.append(" ")

                        self.ilias_test_result4_min.append(" ")
                        self.ilias_test_result4_max.append(" ")
                        self.ilias_test_result4_prec.append(" ")
                        self.ilias_test_result4_tol.append(" ")
                        self.ilias_test_result4_pts.append(" ")
                        self.ilias_test_result4_formula.append(" ")

                    if "4" in self.ilias_test_question_type_collection_sc_answers[i]:
                        self.ilias_test_variable5_min.append(self.mattext_text_all_sc_answers[i+4])
                        self.ilias_test_variable5_prec.append(" ")
                        self.ilias_test_variable5_divby.append(" ")
                        self.ilias_test_variable5_max.append(" ")

                        self.ilias_test_result5_min.append(self.all_sc_questions_points[i+4])
                        self.ilias_test_result5_max.append(" ")
                        self.ilias_test_result5_prec.append(" ")
                        self.ilias_test_result5_tol.append(" ")
                        self.ilias_test_result5_pts.append(" ")
                        self.ilias_test_result5_formula.append(" ")
                    else:
                        self.ilias_test_variable5_min.append(" ")
                        self.ilias_test_variable5_prec.append(" ")
                        self.ilias_test_variable5_divby.append(" ")
                        self.ilias_test_variable5_max.append(" ")

                        self.ilias_test_result5_min.append(" ")
                        self.ilias_test_result5_max.append(" ")
                        self.ilias_test_result5_prec.append(" ")
                        self.ilias_test_result5_tol.append(" ")
                        self.ilias_test_result5_pts.append(" ")
                        self.ilias_test_result5_formula.append(" ")

                    if "5" in self.ilias_test_question_type_collection_sc_answers[i]:
                        self.ilias_test_variable6_min.append(self.mattext_text_all_sc_answers[i+5])
                        self.ilias_test_variable6_prec.append(" ")
                        self.ilias_test_variable6_divby.append(" ")
                        self.ilias_test_variable6_max.append(" ")

                        self.ilias_test_result6_min.append(self.all_sc_questions_points[i+5])
                        self.ilias_test_result6_max.append(" ")
                        self.ilias_test_result6_prec.append(" ")
                        self.ilias_test_result6_tol.append(" ")
                        self.ilias_test_result6_pts.append(" ")
                        self.ilias_test_result6_formula.append(" ")
                    else:
                        self.ilias_test_variable6_min.append(" ")
                        self.ilias_test_variable6_prec.append(" ")
                        self.ilias_test_variable6_divby.append(" ")
                        self.ilias_test_variable6_max.append(" ")

                        self.ilias_test_result6_min.append(" ")
                        self.ilias_test_result6_max.append(" ")
                        self.ilias_test_result6_prec.append(" ")
                        self.ilias_test_result6_tol.append(" ")
                        self.ilias_test_result6_pts.append(" ")
                        self.ilias_test_result6_formula.append(" ")

                    if "6" in self.ilias_test_question_type_collection_sc_answers[i]:
                        self.ilias_test_variable7_min.append(self.mattext_text_all_sc_answers[i+6])
                        self.ilias_test_variable7_prec.append(" ")
                        self.ilias_test_variable7_divby.append(" ")
                        self.ilias_test_variable7_max.append(" ")

                        self.ilias_test_result7_min.append(self.all_sc_questions_points[i+6])
                        self.ilias_test_result7_max.append(" ")
                        self.ilias_test_result7_prec.append(" ")
                        self.ilias_test_result7_tol.append(" ")
                        self.ilias_test_result7_pts.append(" ")
                        self.ilias_test_result7_formula.append(" ")
                    else:
                        self.ilias_test_variable7_min.append(" ")
                        self.ilias_test_variable7_prec.append(" ")
                        self.ilias_test_variable7_divby.append(" ")
                        self.ilias_test_variable7_max.append(" ")

                        self.ilias_test_result7_min.append(" ")
                        self.ilias_test_result7_max.append(" ")
                        self.ilias_test_result7_prec.append(" ")
                        self.ilias_test_result7_tol.append(" ")
                        self.ilias_test_result7_pts.append(" ")
                        self.ilias_test_result7_formula.append(" ")

                    if "7" in self.ilias_test_question_type_collection_sc_answers[i]:
                        self.ilias_test_variable8_min.append(self.mattext_text_all_sc_answers[i+7])
                        self.ilias_test_variable8_prec.append(" ")
                        self.ilias_test_variable8_divby.append(" ")
                        self.ilias_test_variable8_max.append(" ")

                        self.ilias_test_result8_min.append(self.all_sc_questions_points[i+7])
                        self.ilias_test_result8_max.append(" ")
                        self.ilias_test_result8_prec.append(" ")
                        self.ilias_test_result8_tol.append(" ")
                        self.ilias_test_result8_pts.append(" ")
                        self.ilias_test_result8_formula.append(" ")
                    else:
                        self.ilias_test_variable8_min.append(" ")
                        self.ilias_test_variable8_prec.append(" ")
                        self.ilias_test_variable8_divby.append(" ")
                        self.ilias_test_variable8_max.append(" ")

                        self.ilias_test_result8_min.append(" ")
                        self.ilias_test_result8_max.append(" ")
                        self.ilias_test_result8_prec.append(" ")
                        self.ilias_test_result8_tol.append(" ")
                        self.ilias_test_result8_pts.append(" ")
                        self.ilias_test_result8_formula.append(" ")

                    if "8" in self.ilias_test_question_type_collection_sc_answers[i]:
                        self.ilias_test_variable9_min.append(self.mattext_text_all_sc_answers[i+8])
                        self.ilias_test_variable9_prec.append(" ")
                        self.ilias_test_variable9_divby.append(" ")
                        self.ilias_test_variable9_max.append(" ")

                        self.ilias_test_result9_min.append(self.all_sc_questions_points[i+8])
                        self.ilias_test_result9_max.append(" ")
                        self.ilias_test_result9_prec.append(" ")
                        self.ilias_test_result9_tol.append(" ")
                        self.ilias_test_result9_pts.append(" ")
                        self.ilias_test_result9_formula.append(" ")
                    else:
                        self.ilias_test_variable9_min.append(" ")
                        self.ilias_test_variable9_prec.append(" ")
                        self.ilias_test_variable9_divby.append(" ")
                        self.ilias_test_variable9_max.append(" ")

                        self.ilias_test_result9_min.append(" ")
                        self.ilias_test_result9_max.append(" ")
                        self.ilias_test_result9_prec.append(" ")
                        self.ilias_test_result9_tol.append(" ")
                        self.ilias_test_result9_pts.append(" ")
                        self.ilias_test_result9_formula.append(" ")

                    if "9" in self.ilias_test_question_type_collection_sc_answers[i]:
                        self.ilias_test_variable10_min.append(self.mattext_text_all_sc_answers[i+9])
                        self.ilias_test_variable10_prec.append(" ")
                        self.ilias_test_variable10_divby.append(" ")
                        self.ilias_test_variable10_max.append(" ")

                        self.ilias_test_result10_min.append(self.all_sc_questions_points[i+9])
                        self.ilias_test_result10_max.append(" ")
                        self.ilias_test_result10_prec.append(" ")
                        self.ilias_test_result10_tol.append(" ")
                        self.ilias_test_result10_pts.append(" ")
                        self.ilias_test_result10_formula.append(" ")
                    else:
                        self.ilias_test_variable10_min.append(" ")
                        self.ilias_test_variable10_prec.append(" ")
                        self.ilias_test_variable10_divby.append(" ")
                        self.ilias_test_variable10_max.append(" ")

                        self.ilias_test_result10_min.append(" ")
                        self.ilias_test_result10_max.append(" ")
                        self.ilias_test_result10_prec.append(" ")
                        self.ilias_test_result10_tol.append(" ")
                        self.ilias_test_result10_pts.append(" ")
                        self.ilias_test_result10_formula.append(" ")


                else:
                    if "0" in self.ilias_test_question_type_collection_sc_answers[i]:
                        self.ilias_test_variable1_min.append(self.mattext_text_all_sc_answers[t])
                        self.ilias_test_variable1_prec.append(" ")
                        self.ilias_test_variable1_divby.append(" ")
                        self.ilias_test_variable1_max.append(" ")

                        self.ilias_test_result1_min.append(self.all_sc_questions_points[t])
                        self.ilias_test_result1_max.append(" ")
                        self.ilias_test_result1_prec.append(" ")
                        self.ilias_test_result1_tol.append(" ")
                        self.ilias_test_result1_pts.append(" ")
                        self.ilias_test_result1_formula.append(" ")
                    else:
                        self.ilias_test_variable1_min.append(" ")
                        self.ilias_test_variable1_prec.append(" ")
                        self.ilias_test_variable1_divby.append(" ")
                        self.ilias_test_variable1_max.append(" ")

                        self.ilias_test_result1_min.append(" ")
                        self.ilias_test_result1_max.append(" ")
                        self.ilias_test_result1_prec.append(" ")
                        self.ilias_test_result1_tol.append(" ")
                        self.ilias_test_result1_pts.append(" ")
                        self.ilias_test_result1_formula.append(" ")

                    if "1" in self.ilias_test_question_type_collection_sc_answers[i]:
                        self.ilias_test_variable2_min.append(self.mattext_text_all_sc_answers[t+1])
                        self.ilias_test_variable2_prec.append(" ")
                        self.ilias_test_variable2_divby.append(" ")
                        self.ilias_test_variable2_max.append(" ")

                        self.ilias_test_result2_min.append(self.all_sc_questions_points[t+1])
                        self.ilias_test_result2_max.append(" ")
                        self.ilias_test_result2_prec.append(" ")
                        self.ilias_test_result2_tol.append(" ")
                        self.ilias_test_result2_pts.append(" ")
                        self.ilias_test_result2_formula.append(" ")
                    else:
                        self.ilias_test_variable2_min.append(" ")
                        self.ilias_test_variable2_prec.append(" ")
                        self.ilias_test_variable2_divby.append(" ")
                        self.ilias_test_variable2_max.append(" ")

                        self.ilias_test_result2_min.append(" ")
                        self.ilias_test_result2_max.append(" ")
                        self.ilias_test_result2_prec.append(" ")
                        self.ilias_test_result2_tol.append(" ")
                        self.ilias_test_result2_pts.append(" ")
                        self.ilias_test_result2_formula.append(" ")

                    if "2" in self.ilias_test_question_type_collection_sc_answers[i]:
                        self.ilias_test_variable3_min.append(self.mattext_text_all_sc_answers[t+2])
                        self.ilias_test_variable3_prec.append(" ")
                        self.ilias_test_variable3_divby.append(" ")
                        self.ilias_test_variable3_max.append(" ")

                        self.ilias_test_result3_min.append(self.all_sc_questions_points[t+2])
                        self.ilias_test_result3_max.append(" ")
                        self.ilias_test_result3_prec.append(" ")
                        self.ilias_test_result3_tol.append(" ")
                        self.ilias_test_result3_pts.append(" ")
                        self.ilias_test_result3_formula.append(" ")
                    else:
                        self.ilias_test_variable3_min.append(" ")
                        self.ilias_test_variable3_prec.append(" ")
                        self.ilias_test_variable3_divby.append(" ")
                        self.ilias_test_variable3_max.append(" ")

                        self.ilias_test_result3_min.append(" ")
                        self.ilias_test_result3_max.append(" ")
                        self.ilias_test_result3_prec.append(" ")
                        self.ilias_test_result3_tol.append(" ")
                        self.ilias_test_result3_pts.append(" ")
                        self.ilias_test_result3_formula.append(" ")

                    if "3" in self.ilias_test_question_type_collection_sc_answers[i]:
                        self.ilias_test_variable4_min.append(self.mattext_text_all_sc_answers[t+3])
                        self.ilias_test_variable4_prec.append(" ")
                        self.ilias_test_variable4_divby.append(" ")
                        self.ilias_test_variable4_max.append(" ")

                        self.ilias_test_result4_min.append(self.all_sc_questions_points[t+3])
                        self.ilias_test_result4_max.append(" ")
                        self.ilias_test_result4_prec.append(" ")
                        self.ilias_test_result4_tol.append(" ")
                        self.ilias_test_result4_pts.append(" ")
                        self.ilias_test_result4_formula.append(" ")
                    else:
                        self.ilias_test_variable4_min.append(" ")
                        self.ilias_test_variable4_prec.append(" ")
                        self.ilias_test_variable4_divby.append(" ")
                        self.ilias_test_variable4_max.append(" ")

                        self.ilias_test_result4_min.append(" ")
                        self.ilias_test_result4_max.append(" ")
                        self.ilias_test_result4_prec.append(" ")
                        self.ilias_test_result4_tol.append(" ")
                        self.ilias_test_result4_pts.append(" ")
                        self.ilias_test_result4_formula.append(" ")

                    if "4" in self.ilias_test_question_type_collection_sc_answers[i]:
                        self.ilias_test_variable5_min.append(self.mattext_text_all_sc_answers[t+4])
                        self.ilias_test_variable5_prec.append(" ")
                        self.ilias_test_variable5_divby.append(" ")
                        self.ilias_test_variable5_max.append(" ")

                        self.ilias_test_result5_min.append(self.all_sc_questions_points[t+4])
                        self.ilias_test_result5_max.append(" ")
                        self.ilias_test_result5_prec.append(" ")
                        self.ilias_test_result5_tol.append(" ")
                        self.ilias_test_result5_pts.append(" ")
                        self.ilias_test_result5_formula.append(" ")
                    else:
                        self.ilias_test_variable5_min.append(" ")
                        self.ilias_test_variable5_prec.append(" ")
                        self.ilias_test_variable5_divby.append(" ")
                        self.ilias_test_variable5_max.append(" ")

                        self.ilias_test_result5_min.append(" ")
                        self.ilias_test_result5_max.append(" ")
                        self.ilias_test_result5_prec.append(" ")
                        self.ilias_test_result5_tol.append(" ")
                        self.ilias_test_result5_pts.append(" ")
                        self.ilias_test_result5_formula.append(" ")

                    if "5" in self.ilias_test_question_type_collection_sc_answers[i]:
                        self.ilias_test_variable6_min.append(self.mattext_text_all_sc_answers[t+5])
                        self.ilias_test_variable6_prec.append(" ")
                        self.ilias_test_variable6_divby.append(" ")
                        self.ilias_test_variable6_max.append(" ")

                        self.ilias_test_result6_min.append(self.all_sc_questions_points[t+5])
                        self.ilias_test_result6_max.append(" ")
                        self.ilias_test_result6_prec.append(" ")
                        self.ilias_test_result6_tol.append(" ")
                        self.ilias_test_result6_pts.append(" ")
                        self.ilias_test_result6_formula.append(" ")
                    else:
                        self.ilias_test_variable6_min.append(" ")
                        self.ilias_test_variable6_prec.append(" ")
                        self.ilias_test_variable6_divby.append(" ")
                        self.ilias_test_variable6_max.append(" ")

                        self.ilias_test_result6_min.append(" ")
                        self.ilias_test_result6_max.append(" ")
                        self.ilias_test_result6_prec.append(" ")
                        self.ilias_test_result6_tol.append(" ")
                        self.ilias_test_result6_pts.append(" ")
                        self.ilias_test_result6_formula.append(" ")

                    if "6" in self.ilias_test_question_type_collection_sc_answers[i]:
                        self.ilias_test_variable7_min.append(self.mattext_text_all_sc_answers[t+6])
                        self.ilias_test_variable7_prec.append(" ")
                        self.ilias_test_variable7_divby.append(" ")
                        self.ilias_test_variable7_max.append(" ")

                        self.ilias_test_result7_min.append(self.all_sc_questions_points[t+6])
                        self.ilias_test_result7_max.append(" ")
                        self.ilias_test_result7_prec.append(" ")
                        self.ilias_test_result7_tol.append(" ")
                        self.ilias_test_result7_pts.append(" ")
                        self.ilias_test_result7_formula.append(" ")
                    else:
                        self.ilias_test_variable7_min.append(" ")
                        self.ilias_test_variable7_prec.append(" ")
                        self.ilias_test_variable7_divby.append(" ")
                        self.ilias_test_variable7_max.append(" ")

                        self.ilias_test_result7_min.append(" ")
                        self.ilias_test_result7_max.append(" ")
                        self.ilias_test_result7_prec.append(" ")
                        self.ilias_test_result7_tol.append(" ")
                        self.ilias_test_result7_pts.append(" ")
                        self.ilias_test_result7_formula.append(" ")

                    if "7" in self.ilias_test_question_type_collection_sc_answers[i]:
                        self.ilias_test_variable8_min.append(self.mattext_text_all_sc_answers[t+7])
                        self.ilias_test_variable8_prec.append(" ")
                        self.ilias_test_variable8_divby.append(" ")
                        self.ilias_test_variable8_max.append(" ")

                        self.ilias_test_result8_min.append(self.all_sc_questions_points[t+7])
                        self.ilias_test_result8_max.append(" ")
                        self.ilias_test_result8_prec.append(" ")
                        self.ilias_test_result8_tol.append(" ")
                        self.ilias_test_result8_pts.append(" ")
                        self.ilias_test_result8_formula.append(" ")
                    else:
                        self.ilias_test_variable8_min.append(" ")
                        self.ilias_test_variable8_prec.append(" ")
                        self.ilias_test_variable8_divby.append(" ")
                        self.ilias_test_variable8_max.append(" ")

                        self.ilias_test_result8_min.append(" ")
                        self.ilias_test_result8_max.append(" ")
                        self.ilias_test_result8_prec.append(" ")
                        self.ilias_test_result8_tol.append(" ")
                        self.ilias_test_result8_pts.append(" ")
                        self.ilias_test_result8_formula.append(" ")

                    if "8" in self.ilias_test_question_type_collection_sc_answers[i]:
                        self.ilias_test_variable9_min.append(self.mattext_text_all_sc_answers[t+8])
                        self.ilias_test_variable9_prec.append(" ")
                        self.ilias_test_variable9_divby.append(" ")
                        self.ilias_test_variable9_max.append(" ")

                        self.ilias_test_result9_min.append(self.all_sc_questions_points[t+8])
                        self.ilias_test_result9_max.append(" ")
                        self.ilias_test_result9_prec.append(" ")
                        self.ilias_test_result9_tol.append(" ")
                        self.ilias_test_result9_pts.append(" ")
                        self.ilias_test_result9_formula.append(" ")
                    else:
                        self.ilias_test_variable9_min.append(" ")
                        self.ilias_test_variable9_prec.append(" ")
                        self.ilias_test_variable9_divby.append(" ")
                        self.ilias_test_variable9_max.append(" ")

                        self.ilias_test_result9_min.append(" ")
                        self.ilias_test_result9_max.append(" ")
                        self.ilias_test_result9_prec.append(" ")
                        self.ilias_test_result9_tol.append(" ")
                        self.ilias_test_result9_pts.append(" ")
                        self.ilias_test_result9_formula.append(" ")

                    if "9" in self.ilias_test_question_type_collection_sc_answers[i]:
                        self.ilias_test_variable10_min.append(self.mattext_text_all_sc_answers[t+9])
                        self.ilias_test_variable10_prec.append(" ")
                        self.ilias_test_variable10_divby.append(" ")
                        self.ilias_test_variable10_max.append(" ")

                        self.ilias_test_result10_min.append(self.all_sc_questions_points[t+9])
                        self.ilias_test_result10_max.append(" ")
                        self.ilias_test_result10_prec.append(" ")
                        self.ilias_test_result10_tol.append(" ")
                        self.ilias_test_result10_pts.append(" ")
                        self.ilias_test_result10_formula.append(" ")
                    else:
                        self.ilias_test_variable10_min.append(" ")
                        self.ilias_test_variable10_prec.append(" ")
                        self.ilias_test_variable10_divby.append(" ")
                        self.ilias_test_variable10_max.append(" ")

                        self.ilias_test_result10_min.append(" ")
                        self.ilias_test_result10_max.append(" ")
                        self.ilias_test_result10_prec.append(" ")
                        self.ilias_test_result10_tol.append(" ")
                        self.ilias_test_result10_pts.append(" ")
                        self.ilias_test_result10_formula.append(" ")

                    t += int(max(self.ilias_test_question_type_collection_sc_answers[i])) + 1



        ######### Einfügen der Multiple-Choice Fragen #############################
        # Wenn in den Fragentiteln eine MultipleChoice Question erkannt wird, dann mc_flag = 1
        if self.multiplechoice_flag == 1:
            t = int(max(self.ilias_test_question_type_collection_mc_answers[0])) + 1
            for i in range(len(self.ilias_test_question_type_collection_mc_answers)):
                if i == 0:
                    if "0" in self.ilias_test_question_type_collection_mc_answers[i]:
                        self.ilias_test_variable1_min.append(self.mattext_text_all_mc_answers[i])
                        self.ilias_test_variable1_prec.append(" ")
                        self.ilias_test_variable1_divby.append(" ")
                        self.ilias_test_variable1_max.append(" ")

                        self.ilias_test_result1_min.append(self.mc_questions_false_points[i])
                        self.ilias_test_result1_max.append(self.mc_questions_true_points[i])
                        self.ilias_test_result1_prec.append(" ")
                        self.ilias_test_result1_tol.append(" ")
                        self.ilias_test_result1_pts.append(" ")
                        self.ilias_test_result1_formula.append(" ")
                    else:
                        self.ilias_test_variable1_min.append(" ")
                        self.ilias_test_variable1_prec.append(" ")
                        self.ilias_test_variable1_divby.append(" ")
                        self.ilias_test_variable1_max.append(" ")

                        self.ilias_test_result1_min.append(" ")
                        self.ilias_test_result1_max.append(" ")
                        self.ilias_test_result1_prec.append(" ")
                        self.ilias_test_result1_tol.append(" ")
                        self.ilias_test_result1_pts.append(" ")
                        self.ilias_test_result1_formula.append(" ")

                    if "1" in self.ilias_test_question_type_collection_mc_answers[i]:
                        self.ilias_test_variable2_min.append(self.mattext_text_all_mc_answers[i+1])
                        self.ilias_test_variable2_prec.append(" ")
                        self.ilias_test_variable2_divby.append(" ")
                        self.ilias_test_variable2_max.append(" ")

                        self.ilias_test_result2_min.append(self.mc_questions_false_points[i+1])
                        self.ilias_test_result2_max.append(self.mc_questions_true_points[i+1])
                        self.ilias_test_result2_prec.append(" ")
                        self.ilias_test_result2_tol.append(" ")
                        self.ilias_test_result2_pts.append(" ")
                        self.ilias_test_result2_formula.append(" ")
                    else:
                        self.ilias_test_variable2_min.append(" ")
                        self.ilias_test_variable2_prec.append(" ")
                        self.ilias_test_variable2_divby.append(" ")
                        self.ilias_test_variable2_max.append(" ")

                        self.ilias_test_result2_min.append(" ")
                        self.ilias_test_result2_max.append(" ")
                        self.ilias_test_result2_prec.append(" ")
                        self.ilias_test_result2_tol.append(" ")
                        self.ilias_test_result2_pts.append(" ")
                        self.ilias_test_result2_formula.append(" ")

                    if "2" in self.ilias_test_question_type_collection_mc_answers[i]:
                        self.ilias_test_variable3_min.append(self.mattext_text_all_mc_answers[i+2])
                        self.ilias_test_variable3_prec.append(" ")
                        self.ilias_test_variable3_divby.append(" ")
                        self.ilias_test_variable3_max.append(" ")

                        self.ilias_test_result3_min.append(self.mc_questions_false_points[i+2])
                        self.ilias_test_result3_max.append(self.mc_questions_true_points[i+2])
                        self.ilias_test_result3_prec.append(" ")
                        self.ilias_test_result3_tol.append(" ")
                        self.ilias_test_result3_pts.append(" ")
                        self.ilias_test_result3_formula.append(" ")
                    else:
                        self.ilias_test_variable3_min.append(" ")
                        self.ilias_test_variable3_prec.append(" ")
                        self.ilias_test_variable3_divby.append(" ")
                        self.ilias_test_variable3_max.append(" ")

                        self.ilias_test_result3_min.append(" ")
                        self.ilias_test_result3_max.append(" ")
                        self.ilias_test_result3_prec.append(" ")
                        self.ilias_test_result3_tol.append(" ")
                        self.ilias_test_result3_pts.append(" ")
                        self.ilias_test_result3_formula.append(" ")


                    if "3" in self.ilias_test_question_type_collection_mc_answers[i]:
                        self.ilias_test_variable4_min.append(self.mattext_text_all_mc_answers[i+3])
                        self.ilias_test_variable4_prec.append(" ")
                        self.ilias_test_variable4_divby.append(" ")
                        self.ilias_test_variable4_max.append(" ")

                        self.ilias_test_result4_min.append(self.mc_questions_false_points[i+3])
                        self.ilias_test_result4_max.append(self.mc_questions_true_points[i+3])
                        self.ilias_test_result4_prec.append(" ")
                        self.ilias_test_result4_tol.append(" ")
                        self.ilias_test_result4_pts.append(" ")
                        self.ilias_test_result4_formula.append(" ")
                    else:
                        self.ilias_test_variable4_min.append(" ")
                        self.ilias_test_variable4_prec.append(" ")
                        self.ilias_test_variable4_divby.append(" ")
                        self.ilias_test_variable4_max.append(" ")

                        self.ilias_test_result4_min.append(" ")
                        self.ilias_test_result4_max.append(" ")
                        self.ilias_test_result4_prec.append(" ")
                        self.ilias_test_result4_tol.append(" ")
                        self.ilias_test_result4_pts.append(" ")
                        self.ilias_test_result4_formula.append(" ")

                    if "4" in self.ilias_test_question_type_collection_mc_answers[i]:
                        self.ilias_test_variable5_min.append(self.mattext_text_all_mc_answers[i+4])
                        self.ilias_test_variable5_prec.append(" ")
                        self.ilias_test_variable5_divby.append(" ")
                        self.ilias_test_variable5_max.append(" ")

                        self.ilias_test_result5_min.append(self.mc_questions_false_points[i+4])
                        self.ilias_test_result5_max.append(self.mc_questions_true_points[i+4])
                        self.ilias_test_result5_prec.append(" ")
                        self.ilias_test_result5_tol.append(" ")
                        self.ilias_test_result5_pts.append(" ")
                        self.ilias_test_result5_formula.append(" ")
                    else:
                        self.ilias_test_variable5_min.append(" ")
                        self.ilias_test_variable5_prec.append(" ")
                        self.ilias_test_variable5_divby.append(" ")
                        self.ilias_test_variable5_max.append(" ")

                        self.ilias_test_result5_min.append(" ")
                        self.ilias_test_result5_max.append(" ")
                        self.ilias_test_result5_prec.append(" ")
                        self.ilias_test_result5_tol.append(" ")
                        self.ilias_test_result5_pts.append(" ")
                        self.ilias_test_result5_formula.append(" ")

                    if "5" in self.ilias_test_question_type_collection_mc_answers[i]:
                        self.ilias_test_variable6_min.append(self.mattext_text_all_mc_answers[i+5])
                        self.ilias_test_variable6_prec.append(" ")
                        self.ilias_test_variable6_divby.append(" ")
                        self.ilias_test_variable6_max.append(" ")

                        self.ilias_test_result6_min.append(self.mc_questions_false_points[i+5])
                        self.ilias_test_result6_max.append(self.mc_questions_false_points[i+5])
                        self.ilias_test_result6_prec.append(" ")
                        self.ilias_test_result6_tol.append(" ")
                        self.ilias_test_result6_pts.append(" ")
                        self.ilias_test_result6_formula.append(" ")
                    else:
                        self.ilias_test_variable6_min.append(" ")
                        self.ilias_test_variable6_prec.append(" ")
                        self.ilias_test_variable6_divby.append(" ")
                        self.ilias_test_variable6_max.append(" ")

                        self.ilias_test_result6_min.append(" ")
                        self.ilias_test_result6_max.append(" ")
                        self.ilias_test_result6_prec.append(" ")
                        self.ilias_test_result6_tol.append(" ")
                        self.ilias_test_result6_pts.append(" ")
                        self.ilias_test_result6_formula.append(" ")

                    if "6" in self.ilias_test_question_type_collection_mc_answers[i]:
                        self.ilias_test_variable7_min.append(self.mattext_text_all_mc_answers[i+6])
                        self.ilias_test_variable7_prec.append(" ")
                        self.ilias_test_variable7_divby.append(" ")
                        self.ilias_test_variable7_max.append(" ")

                        self.ilias_test_result7_min.append(self.mc_questions_false_points[i+6])
                        self.ilias_test_result7_max.append(self.mc_questions_true_points[i+6])
                        self.ilias_test_result7_prec.append(" ")
                        self.ilias_test_result7_tol.append(" ")
                        self.ilias_test_result7_pts.append(" ")
                        self.ilias_test_result7_formula.append(" ")
                    else:
                        self.ilias_test_variable7_min.append(" ")
                        self.ilias_test_variable7_prec.append(" ")
                        self.ilias_test_variable7_divby.append(" ")
                        self.ilias_test_variable7_max.append(" ")

                        self.ilias_test_result7_min.append(" ")
                        self.ilias_test_result7_max.append(" ")
                        self.ilias_test_result7_prec.append(" ")
                        self.ilias_test_result7_tol.append(" ")
                        self.ilias_test_result7_pts.append(" ")
                        self.ilias_test_result7_formula.append(" ")

                    if "7" in self.ilias_test_question_type_collection_mc_answers[i]:
                        self.ilias_test_variable8_min.append(self.mattext_text_all_mc_answers[i+7])
                        self.ilias_test_variable8_prec.append(" ")
                        self.ilias_test_variable8_divby.append(" ")
                        self.ilias_test_variable8_max.append(" ")

                        self.ilias_test_result8_min.append(self.mc_questions_false_points[i+7])
                        self.ilias_test_result8_max.append(self.mc_questions_true_points[i+7])
                        self.ilias_test_result8_prec.append(" ")
                        self.ilias_test_result8_tol.append(" ")
                        self.ilias_test_result8_pts.append(" ")
                        self.ilias_test_result8_formula.append(" ")
                    else:
                        self.ilias_test_variable8_min.append(" ")
                        self.ilias_test_variable8_prec.append(" ")
                        self.ilias_test_variable8_divby.append(" ")
                        self.ilias_test_variable8_max.append(" ")

                        self.ilias_test_result8_min.append(" ")
                        self.ilias_test_result8_max.append(" ")
                        self.ilias_test_result8_prec.append(" ")
                        self.ilias_test_result8_tol.append(" ")
                        self.ilias_test_result8_pts.append(" ")
                        self.ilias_test_result8_formula.append(" ")

                    if "8" in self.ilias_test_question_type_collection_mc_answers[i]:
                        self.ilias_test_variable9_min.append(self.mattext_text_all_mc_answers[i+8])
                        self.ilias_test_variable9_prec.append(" ")
                        self.ilias_test_variable9_divby.append(" ")
                        self.ilias_test_variable9_max.append(" ")

                        self.ilias_test_result9_min.append(self.mc_questions_false_points[i+8])
                        self.ilias_test_result9_max.append(self.mc_questions_true_points[i+8])
                        self.ilias_test_result9_prec.append(" ")
                        self.ilias_test_result9_tol.append(" ")
                        self.ilias_test_result9_pts.append(" ")
                        self.ilias_test_result9_formula.append(" ")
                    else:
                        self.ilias_test_variable9_min.append(" ")
                        self.ilias_test_variable9_prec.append(" ")
                        self.ilias_test_variable9_divby.append(" ")
                        self.ilias_test_variable9_max.append(" ")

                        self.ilias_test_result9_min.append(" ")
                        self.ilias_test_result9_max.append(" ")
                        self.ilias_test_result9_prec.append(" ")
                        self.ilias_test_result9_tol.append(" ")
                        self.ilias_test_result9_pts.append(" ")
                        self.ilias_test_result9_formula.append(" ")

                    if "9" in self.ilias_test_question_type_collection_mc_answers[i]:
                        self.ilias_test_variable10_min.append(self.mattext_text_all_mc_answers[i+9])
                        self.ilias_test_variable10_prec.append(" ")
                        self.ilias_test_variable10_divby.append(" ")
                        self.ilias_test_variable10_max.append(" ")

                        self.ilias_test_result10_min.append(self.mc_questions_false_points[i+9])
                        self.ilias_test_result10_max.append(self.mc_questions_true_points[i+9])
                        self.ilias_test_result10_prec.append(" ")
                        self.ilias_test_result10_tol.append(" ")
                        self.ilias_test_result10_pts.append(" ")
                        self.ilias_test_result10_formula.append(" ")
                    else:
                        self.ilias_test_variable10_min.append(" ")
                        self.ilias_test_variable10_prec.append(" ")
                        self.ilias_test_variable10_divby.append(" ")
                        self.ilias_test_variable10_max.append(" ")

                        self.ilias_test_result10_min.append(" ")
                        self.ilias_test_result10_max.append(" ")
                        self.ilias_test_result10_prec.append(" ")
                        self.ilias_test_result10_tol.append(" ")
                        self.ilias_test_result10_pts.append(" ")
                        self.ilias_test_result10_formula.append(" ")

                else:
                    if "0" in self.ilias_test_question_type_collection_mc_answers[i]:
                        self.ilias_test_variable1_min.append(self.mattext_text_all_mc_answers[t])
                        self.ilias_test_variable1_prec.append(" ")
                        self.ilias_test_variable1_divby.append(" ")
                        self.ilias_test_variable1_max.append(" ")

                        self.ilias_test_result1_min.append(self.mc_questions_false_points[t])
                        self.ilias_test_result1_max.append(self.mc_questions_true_points[t])
                        self.ilias_test_result1_prec.append(" ")
                        self.ilias_test_result1_tol.append(" ")
                        self.ilias_test_result1_pts.append(" ")
                        self.ilias_test_result1_formula.append(" ")
                    else:
                        self.ilias_test_variable1_min.append(" ")
                        self.ilias_test_variable1_prec.append(" ")
                        self.ilias_test_variable1_divby.append(" ")
                        self.ilias_test_variable1_max.append(" ")

                        self.ilias_test_result1_min.append(" ")
                        self.ilias_test_result1_max.append(" ")
                        self.ilias_test_result1_prec.append(" ")
                        self.ilias_test_result1_tol.append(" ")
                        self.ilias_test_result1_pts.append(" ")
                        self.ilias_test_result1_formula.append(" ")

                    if "1" in self.ilias_test_question_type_collection_mc_answers[i]:
                        self.ilias_test_variable2_min.append(self.mattext_text_all_mc_answers[t + 1])
                        self.ilias_test_variable2_prec.append(" ")
                        self.ilias_test_variable2_divby.append(" ")
                        self.ilias_test_variable2_max.append(" ")

                        self.ilias_test_result2_min.append(self.mc_questions_false_points[t + 1])
                        self.ilias_test_result2_max.append(self.mc_questions_true_points[t + 1])
                        self.ilias_test_result2_prec.append(" ")
                        self.ilias_test_result2_tol.append(" ")
                        self.ilias_test_result2_pts.append(" ")
                        self.ilias_test_result2_formula.append(" ")
                    else:
                        self.ilias_test_variable2_min.append(" ")
                        self.ilias_test_variable2_prec.append(" ")
                        self.ilias_test_variable2_divby.append(" ")
                        self.ilias_test_variable2_max.append(" ")

                        self.ilias_test_result2_min.append(" ")
                        self.ilias_test_result2_max.append(" ")
                        self.ilias_test_result2_prec.append(" ")
                        self.ilias_test_result2_tol.append(" ")
                        self.ilias_test_result2_pts.append(" ")
                        self.ilias_test_result2_formula.append(" ")

                    if "2" in self.ilias_test_question_type_collection_mc_answers[i]:
                        self.ilias_test_variable3_min.append(self.mattext_text_all_mc_answers[t + 2])
                        self.ilias_test_variable3_prec.append(" ")
                        self.ilias_test_variable3_divby.append(" ")
                        self.ilias_test_variable3_max.append(" ")

                        self.ilias_test_result3_min.append(self.mc_questions_false_points[t + 2])
                        self.ilias_test_result3_max.append(self.mc_questions_true_points[t + 2])
                        self.ilias_test_result3_prec.append(" ")
                        self.ilias_test_result3_tol.append(" ")
                        self.ilias_test_result3_pts.append(" ")
                        self.ilias_test_result3_formula.append(" ")
                    else:
                        self.ilias_test_variable3_min.append(" ")
                        self.ilias_test_variable3_prec.append(" ")
                        self.ilias_test_variable3_divby.append(" ")
                        self.ilias_test_variable3_max.append(" ")

                        self.ilias_test_result3_min.append(" ")
                        self.ilias_test_result3_max.append(" ")
                        self.ilias_test_result3_prec.append(" ")
                        self.ilias_test_result3_tol.append(" ")
                        self.ilias_test_result3_pts.append(" ")
                        self.ilias_test_result3_formula.append(" ")

                    if "3" in self.ilias_test_question_type_collection_mc_answers[i]:
                        self.ilias_test_variable4_min.append(self.mattext_text_all_mc_answers[t + 3])
                        self.ilias_test_variable4_prec.append(" ")
                        self.ilias_test_variable4_divby.append(" ")
                        self.ilias_test_variable4_max.append(" ")

                        self.ilias_test_result4_min.append(self.mc_questions_false_points[t + 3])
                        self.ilias_test_result4_max.append(self.mc_questions_true_points[t + 3])
                        self.ilias_test_result4_prec.append(" ")
                        self.ilias_test_result4_tol.append(" ")
                        self.ilias_test_result4_pts.append(" ")
                        self.ilias_test_result4_formula.append(" ")
                    else:
                        self.ilias_test_variable4_min.append(" ")
                        self.ilias_test_variable4_prec.append(" ")
                        self.ilias_test_variable4_divby.append(" ")
                        self.ilias_test_variable4_max.append(" ")

                        self.ilias_test_result4_min.append(" ")
                        self.ilias_test_result4_max.append(" ")
                        self.ilias_test_result4_prec.append(" ")
                        self.ilias_test_result4_tol.append(" ")
                        self.ilias_test_result4_pts.append(" ")
                        self.ilias_test_result4_formula.append(" ")

                    if "4" in self.ilias_test_question_type_collection_mc_answers[i]:
                        self.ilias_test_variable5_min.append(self.mattext_text_all_mc_answers[t + 4])
                        self.ilias_test_variable5_prec.append(" ")
                        self.ilias_test_variable5_divby.append(" ")
                        self.ilias_test_variable5_max.append(" ")

                        self.ilias_test_result5_min.append(self.mc_questions_false_points[t + 4])
                        self.ilias_test_result5_max.append(self.mc_questions_true_points[t + 4])
                        self.ilias_test_result5_prec.append(" ")
                        self.ilias_test_result5_tol.append(" ")
                        self.ilias_test_result5_pts.append(" ")
                        self.ilias_test_result5_formula.append(" ")
                    else:
                        self.ilias_test_variable5_min.append(" ")
                        self.ilias_test_variable5_prec.append(" ")
                        self.ilias_test_variable5_divby.append(" ")
                        self.ilias_test_variable5_max.append(" ")

                        self.ilias_test_result5_min.append(" ")
                        self.ilias_test_result5_max.append(" ")
                        self.ilias_test_result5_prec.append(" ")
                        self.ilias_test_result5_tol.append(" ")
                        self.ilias_test_result5_pts.append(" ")
                        self.ilias_test_result5_formula.append(" ")

                    if "5" in self.ilias_test_question_type_collection_mc_answers[i]:
                        self.ilias_test_variable6_min.append(self.mattext_text_all_mc_answers[t + 5])
                        self.ilias_test_variable6_prec.append(" ")
                        self.ilias_test_variable6_divby.append(" ")
                        self.ilias_test_variable6_max.append(" ")

                        self.ilias_test_result6_min.append(self.mc_questions_false_points[t + 5])
                        self.ilias_test_result6_max.append(self.mc_questions_true_points[t + 5])
                        self.ilias_test_result6_prec.append(" ")
                        self.ilias_test_result6_tol.append(" ")
                        self.ilias_test_result6_pts.append(" ")
                        self.ilias_test_result6_formula.append(" ")
                    else:
                        self.ilias_test_variable6_min.append(" ")
                        self.ilias_test_variable6_prec.append(" ")
                        self.ilias_test_variable6_divby.append(" ")
                        self.ilias_test_variable6_max.append(" ")

                        self.ilias_test_result6_min.append(" ")
                        self.ilias_test_result6_max.append(" ")
                        self.ilias_test_result6_prec.append(" ")
                        self.ilias_test_result6_tol.append(" ")
                        self.ilias_test_result6_pts.append(" ")
                        self.ilias_test_result6_formula.append(" ")

                    if "6" in self.ilias_test_question_type_collection_mc_answers[i]:
                        self.ilias_test_variable7_min.append(self.mattext_text_all_mc_answers[t + 6])
                        self.ilias_test_variable7_prec.append(" ")
                        self.ilias_test_variable7_divby.append(" ")
                        self.ilias_test_variable7_max.append(" ")

                        self.ilias_test_result7_min.append(self.mc_questions_false_points[t + 6])
                        self.ilias_test_result7_max.append(self.mc_questions_true_points[t + 6])
                        self.ilias_test_result7_prec.append(" ")
                        self.ilias_test_result7_tol.append(" ")
                        self.ilias_test_result7_pts.append(" ")
                        self.ilias_test_result7_formula.append(" ")
                    else:
                        self.ilias_test_variable7_min.append(" ")
                        self.ilias_test_variable7_prec.append(" ")
                        self.ilias_test_variable7_divby.append(" ")
                        self.ilias_test_variable7_max.append(" ")

                        self.ilias_test_result7_min.append(" ")
                        self.ilias_test_result7_max.append(" ")
                        self.ilias_test_result7_prec.append(" ")
                        self.ilias_test_result7_tol.append(" ")
                        self.ilias_test_result7_pts.append(" ")
                        self.ilias_test_result7_formula.append(" ")

                    if "7" in self.ilias_test_question_type_collection_mc_answers[i]:
                        self.ilias_test_variable8_min.append(self.mattext_text_all_mc_answers[t+7])
                        self.ilias_test_variable8_prec.append(" ")
                        self.ilias_test_variable8_divby.append(" ")
                        self.ilias_test_variable8_max.append(" ")

                        self.ilias_test_result8_min.append(self.mc_questions_false_points[t+7])
                        self.ilias_test_result8_max.append(self.mc_questions_true_points[t+7])
                        self.ilias_test_result8_prec.append(" ")
                        self.ilias_test_result8_tol.append(" ")
                        self.ilias_test_result8_pts.append(" ")
                        self.ilias_test_result8_formula.append(" ")
                    else:
                        self.ilias_test_variable8_min.append(" ")
                        self.ilias_test_variable8_prec.append(" ")
                        self.ilias_test_variable8_divby.append(" ")
                        self.ilias_test_variable8_max.append(" ")

                        self.ilias_test_result8_min.append(" ")
                        self.ilias_test_result8_max.append(" ")
                        self.ilias_test_result8_prec.append(" ")
                        self.ilias_test_result8_tol.append(" ")
                        self.ilias_test_result8_pts.append(" ")
                        self.ilias_test_result8_formula.append(" ")

                    if "8" in self.ilias_test_question_type_collection_mc_answers[i]:
                        self.ilias_test_variable9_min.append(self.mattext_text_all_mc_answers[t+8])
                        self.ilias_test_variable9_prec.append(" ")
                        self.ilias_test_variable9_divby.append(" ")
                        self.ilias_test_variable9_max.append(" ")

                        self.ilias_test_result9_min.append(self.mc_questions_false_points[t+8])
                        self.ilias_test_result9_max.append(self.mc_questions_true_points[t+8])
                        self.ilias_test_result9_prec.append(" ")
                        self.ilias_test_result9_tol.append(" ")
                        self.ilias_test_result9_pts.append(" ")
                        self.ilias_test_result9_formula.append(" ")
                    else:
                        self.ilias_test_variable9_min.append(" ")
                        self.ilias_test_variable9_prec.append(" ")
                        self.ilias_test_variable9_divby.append(" ")
                        self.ilias_test_variable9_max.append(" ")

                        self.ilias_test_result9_min.append(" ")
                        self.ilias_test_result9_max.append(" ")
                        self.ilias_test_result9_prec.append(" ")
                        self.ilias_test_result9_tol.append(" ")
                        self.ilias_test_result9_pts.append(" ")
                        self.ilias_test_result9_formula.append(" ")

                    if "9" in self.ilias_test_question_type_collection_mc_answers[i]:
                        self.ilias_test_variable10_min.append(self.mattext_text_all_mc_answers[t+9])
                        self.ilias_test_variable10_prec.append(" ")
                        self.ilias_test_variable10_divby.append(" ")
                        self.ilias_test_variable10_max.append(" ")

                        self.ilias_test_result10_min.append(self.mc_questions_false_points[t+9])
                        self.ilias_test_result10_max.append(self.mc_questions_true_points[t+9])
                        self.ilias_test_result10_prec.append(" ")
                        self.ilias_test_result10_tol.append(" ")
                        self.ilias_test_result10_pts.append(" ")
                        self.ilias_test_result10_formula.append(" ")
                    else:
                        self.ilias_test_variable10_min.append(" ")
                        self.ilias_test_variable10_prec.append(" ")
                        self.ilias_test_variable10_divby.append(" ")
                        self.ilias_test_variable10_max.append(" ")

                        self.ilias_test_result10_min.append(" ")
                        self.ilias_test_result10_max.append(" ")
                        self.ilias_test_result10_prec.append(" ")
                        self.ilias_test_result10_tol.append(" ")
                        self.ilias_test_result10_pts.append(" ")
                        self.ilias_test_result10_formula.append(" ")


                    t += int(max(self.ilias_test_question_type_collection_mc_answers[i])) + 1

        print("äääääääääää")
        print(len(self.mattext_text_all_mq_answers_collection))
        print(self.mattext_text_all_mq_answers_collection)
        print(len(self.ilias_test_question_type_collection_mq_answers))
        print(self.ilias_test_question_type_collection_mq_answers)

        print("äääääääääää")

        ######### Einfügen der MATCHING Fragen #############################
        # Wenn in den Fragentiteln eine Matching Question erkannt wird, dann mq_flag = 1
        if self.matchingquestion_flag == 1:
            t = int(max(self.ilias_test_question_type_collection_mq_answers[0])) + 1
            #print("===================")
            #print(self.ilias_test_question_type_collection_sc_answers)
            for i in range(len(self.ilias_test_question_type_collection_mq_answers)):
                #print(self.mattext_text_all_mq_answers_collection[i+5])
                if i == 0:
                    if "0" in self.ilias_test_question_type_collection_mq_answers[i]:
                        self.ilias_test_variable1_min.append(self.mq_images_label[i])
                        self.ilias_test_variable1_prec.append(self.mq_images_data_string[i])
                        self.ilias_test_variable1_divby.append(" ")
                        self.ilias_test_variable1_max.append(self.mattext_text_all_mq_answers_collection[i])

                        self.ilias_test_result1_min.append(" ")
                        self.ilias_test_result1_max.append(" ")
                        self.ilias_test_result1_prec.append(" ")
                        self.ilias_test_result1_tol.append(" ")
                        self.ilias_test_result1_pts.append(" ")
                        self.ilias_test_result1_formula.append(" ")
                    else:
                        self.ilias_test_variable1_min.append(" ")
                        self.ilias_test_variable1_prec.append(" ")
                        self.ilias_test_variable1_divby.append(" ")
                        self.ilias_test_variable1_max.append(" ")

                        self.ilias_test_result1_min.append(" ")
                        self.ilias_test_result1_max.append(" ")
                        self.ilias_test_result1_prec.append(" ")
                        self.ilias_test_result1_tol.append(" ")
                        self.ilias_test_result1_pts.append(" ")
                        self.ilias_test_result1_formula.append(" ")


                    if "1" in self.ilias_test_question_type_collection_mq_answers[i]:
                        print("in 1")
                        self.ilias_test_variable2_min.append(self.mq_images_label[i])
                        self.ilias_test_variable2_prec.append(self.mq_images_data_string[i])
                        self.ilias_test_variable2_divby.append(" ")
                        self.ilias_test_variable2_max.append(self.mattext_text_all_mq_answers_collection[i])

                        self.ilias_test_result2_min.append(" ")
                        self.ilias_test_result2_max.append(" ")
                        self.ilias_test_result2_prec.append(" ")
                        self.ilias_test_result2_tol.append(" ")
                        self.ilias_test_result2_pts.append(" ")
                        self.ilias_test_result2_formula.append(" ")
                    else:
                        self.ilias_test_variable2_min.append(" ")
                        self.ilias_test_variable2_prec.append(" ")
                        self.ilias_test_variable2_divby.append(" ")
                        self.ilias_test_variable2_max.append(" ")

                        self.ilias_test_result2_min.append(" ")
                        self.ilias_test_result2_max.append(" ")
                        self.ilias_test_result2_prec.append(" ")
                        self.ilias_test_result2_tol.append(" ")
                        self.ilias_test_result2_pts.append(" ")
                        self.ilias_test_result2_formula.append(" ")

                    if "2" in self.ilias_test_question_type_collection_mq_answers[i]:
                        print("in 2")
                        self.ilias_test_variable3_min.append(self.mq_images_label[i])
                        self.ilias_test_variable3_prec.append(self.mq_images_data_string[i])
                        self.ilias_test_variable3_divby.append(" ")
                        self.ilias_test_variable3_max.append(self.mattext_text_all_mq_answers_collection[i])

                        self.ilias_test_result3_min.append(" ")
                        self.ilias_test_result3_max.append(" ")
                        self.ilias_test_result3_prec.append(" ")
                        self.ilias_test_result3_tol.append(" ")
                        self.ilias_test_result3_pts.append(" ")
                        self.ilias_test_result3_formula.append(" ")
                    else:
                        self.ilias_test_variable3_min.append(" ")
                        self.ilias_test_variable3_prec.append(" ")
                        self.ilias_test_variable3_divby.append(" ")
                        self.ilias_test_variable3_max.append(" ")

                        self.ilias_test_result3_min.append(" ")
                        self.ilias_test_result3_max.append(" ")
                        self.ilias_test_result3_prec.append(" ")
                        self.ilias_test_result3_tol.append(" ")
                        self.ilias_test_result3_pts.append(" ")
                        self.ilias_test_result3_formula.append(" ")

                    if "3" in self.ilias_test_question_type_collection_mq_answers[i]:
                        print("in 3")
                        self.ilias_test_variable4_min.append(self.mq_images_label[i])
                        self.ilias_test_variable4_prec.append(self.mq_images_data_string[i])
                        self.ilias_test_variable4_divby.append(" ")
                        self.ilias_test_variable4_max.append(self.mattext_text_all_mq_answers_collection[i])

                        self.ilias_test_result4_min.append(" ")
                        self.ilias_test_result4_max.append(" ")
                        self.ilias_test_result4_prec.append(" ")
                        self.ilias_test_result4_tol.append(" ")
                        self.ilias_test_result4_pts.append(" ")
                        self.ilias_test_result4_formula.append(" ")
                    else:
                        self.ilias_test_variable4_min.append(" ")
                        self.ilias_test_variable4_prec.append(" ")
                        self.ilias_test_variable4_divby.append(" ")
                        self.ilias_test_variable4_max.append(" ")

                        self.ilias_test_result4_min.append(" ")
                        self.ilias_test_result4_max.append(" ")
                        self.ilias_test_result4_prec.append(" ")
                        self.ilias_test_result4_tol.append(" ")
                        self.ilias_test_result4_pts.append(" ")
                        self.ilias_test_result4_formula.append(" ")

                    if "4" in self.ilias_test_question_type_collection_mq_answers[i]:
                        self.ilias_test_variable5_min.append(self.mq_images_label[i])
                        self.ilias_test_variable5_prec.append(self.mq_images_data_string[i])
                        self.ilias_test_variable5_divby.append(" ")
                        self.ilias_test_variable5_max.append(self.mattext_text_all_mq_answers_collection[i])

                        self.ilias_test_result5_min.append(" ")
                        self.ilias_test_result5_max.append(" ")
                        self.ilias_test_result5_prec.append(" ")
                        self.ilias_test_result5_tol.append(" ")
                        self.ilias_test_result5_pts.append(" ")
                        self.ilias_test_result5_formula.append(" ")
                    else:
                        self.ilias_test_variable5_min.append(" ")
                        self.ilias_test_variable5_prec.append(" ")
                        self.ilias_test_variable5_divby.append(" ")
                        self.ilias_test_variable5_max.append(" ")

                        self.ilias_test_result5_min.append(" ")
                        self.ilias_test_result5_max.append(" ")
                        self.ilias_test_result5_prec.append(" ")
                        self.ilias_test_result5_tol.append(" ")
                        self.ilias_test_result5_pts.append(" ")
                        self.ilias_test_result5_formula.append(" ")

                    if "5" in self.ilias_test_question_type_collection_mq_answers[i]:
                        self.ilias_test_variable6_min.append(self.mq_images_label[i])
                        self.ilias_test_variable6_prec.append(self.mq_images_data_string[i])
                        self.ilias_test_variable6_divby.append(" ")
                        self.ilias_test_variable6_max.append(self.mattext_text_all_mq_answers_collection[i])

                        self.ilias_test_result6_min.append(" ")
                        self.ilias_test_result6_max.append(" ")
                        self.ilias_test_result6_prec.append(" ")
                        self.ilias_test_result6_tol.append(" ")
                        self.ilias_test_result6_pts.append(" ")
                        self.ilias_test_result6_formula.append(" ")
                    else:
                        self.ilias_test_variable6_min.append(" ")
                        self.ilias_test_variable6_prec.append(" ")
                        self.ilias_test_variable6_divby.append(" ")
                        self.ilias_test_variable6_max.append(" ")

                        self.ilias_test_result6_min.append(" ")
                        self.ilias_test_result6_max.append(" ")
                        self.ilias_test_result6_prec.append(" ")
                        self.ilias_test_result6_tol.append(" ")
                        self.ilias_test_result6_pts.append(" ")
                        self.ilias_test_result6_formula.append(" ")

                    if "6" in self.ilias_test_question_type_collection_mq_answers[i]:
                        self.ilias_test_variable7_min.append(self.mq_images_label[i])
                        self.ilias_test_variable7_prec.append(self.mq_images_data_string[i])
                        self.ilias_test_variable7_divby.append(" ")
                        self.ilias_test_variable7_max.append(self.mattext_text_all_mq_answers_collection[i])

                        self.ilias_test_result7_min.append(" ")
                        self.ilias_test_result7_max.append(" ")
                        self.ilias_test_result7_prec.append(" ")
                        self.ilias_test_result7_tol.append(" ")
                        self.ilias_test_result7_pts.append(" ")
                        self.ilias_test_result7_formula.append(" ")
                    else:
                        self.ilias_test_variable7_min.append(" ")
                        self.ilias_test_variable7_prec.append(" ")
                        self.ilias_test_variable7_divby.append(" ")
                        self.ilias_test_variable7_max.append(" ")

                        self.ilias_test_result7_min.append(" ")
                        self.ilias_test_result7_max.append(" ")
                        self.ilias_test_result7_prec.append(" ")
                        self.ilias_test_result7_tol.append(" ")
                        self.ilias_test_result7_pts.append(" ")
                        self.ilias_test_result7_formula.append(" ")

                    if "7" in self.ilias_test_question_type_collection_mq_answers[i]:
                        self.ilias_test_variable8_min.append(self.mq_images_label[i])
                        self.ilias_test_variable8_prec.append(self.mq_images_data_string[i])
                        self.ilias_test_variable8_divby.append(" ")
                        self.ilias_test_variable8_max.append(self.mattext_text_all_mq_answers_collection[i])

                        self.ilias_test_result8_min.append(" ")
                        self.ilias_test_result8_max.append(" ")
                        self.ilias_test_result8_prec.append(" ")
                        self.ilias_test_result8_tol.append(" ")
                        self.ilias_test_result8_pts.append(" ")
                        self.ilias_test_result8_formula.append(" ")
                    else:
                        self.ilias_test_variable8_min.append(" ")
                        self.ilias_test_variable8_prec.append(" ")
                        self.ilias_test_variable8_divby.append(" ")
                        self.ilias_test_variable8_max.append(" ")

                        self.ilias_test_result8_min.append(" ")
                        self.ilias_test_result8_max.append(" ")
                        self.ilias_test_result8_prec.append(" ")
                        self.ilias_test_result8_tol.append(" ")
                        self.ilias_test_result8_pts.append(" ")
                        self.ilias_test_result8_formula.append(" ")

                    if "8" in self.ilias_test_question_type_collection_mq_answers[i]:
                        self.ilias_test_variable9_min.append(self.mq_images_label[i])
                        self.ilias_test_variable9_prec.append(self.mq_images_data_string[i])
                        self.ilias_test_variable9_divby.append(" ")
                        self.ilias_test_variable9_max.append(self.mattext_text_all_mq_answers_collection[i])

                        self.ilias_test_result9_min.append(" ")
                        self.ilias_test_result9_max.append(" ")
                        self.ilias_test_result9_prec.append(" ")
                        self.ilias_test_result9_tol.append(" ")
                        self.ilias_test_result9_pts.append(" ")
                        self.ilias_test_result9_formula.append(" ")
                    else:
                        self.ilias_test_variable9_min.append(" ")
                        self.ilias_test_variable9_prec.append(" ")
                        self.ilias_test_variable9_divby.append(" ")
                        self.ilias_test_variable9_max.append(" ")

                        self.ilias_test_result9_min.append(" ")
                        self.ilias_test_result9_max.append(" ")
                        self.ilias_test_result9_prec.append(" ")
                        self.ilias_test_result9_tol.append(" ")
                        self.ilias_test_result9_pts.append(" ")
                        self.ilias_test_result9_formula.append(" ")

                    if "9" in self.ilias_test_question_type_collection_mq_answers[i]:
                        self.ilias_test_variable10_min.append(self.mq_images_label[i])
                        self.ilias_test_variable10_prec.append(self.mq_images_data_string[i])
                        self.ilias_test_variable10_divby.append(" ")
                        self.ilias_test_variable10_max.append(self.mattext_text_all_mq_answers_collection[i])

                        self.ilias_test_result10_min.append(" ")
                        self.ilias_test_result10_max.append(" ")
                        self.ilias_test_result10_prec.append(" ")
                        self.ilias_test_result10_tol.append(" ")
                        self.ilias_test_result10_pts.append(" ")
                        self.ilias_test_result10_formula.append(" ")
                    else:
                        self.ilias_test_variable10_min.append(" ")
                        self.ilias_test_variable10_prec.append(" ")
                        self.ilias_test_variable10_divby.append(" ")
                        self.ilias_test_variable10_max.append(" ")

                        self.ilias_test_result10_min.append(" ")
                        self.ilias_test_result10_max.append(" ")
                        self.ilias_test_result10_prec.append(" ")
                        self.ilias_test_result10_tol.append(" ")
                        self.ilias_test_result10_pts.append(" ")
                        self.ilias_test_result10_formula.append(" ")



                else:
                    if "0" in self.ilias_test_question_type_collection_mq_answers[i]:
                        self.ilias_test_variable1_min.append(self.mq_images_label[t])
                        self.ilias_test_variable1_prec.append(self.mq_images_data_string[t])
                        self.ilias_test_variable1_divby.append(" ")
                        self.ilias_test_variable1_max.append(self.mattext_text_all_mq_answers_collection[t])

                        self.ilias_test_result1_min.append(" ")
                        self.ilias_test_result1_max.append(" ")
                        self.ilias_test_result1_prec.append(" ")
                        self.ilias_test_result1_tol.append(" ")
                        self.ilias_test_result1_pts.append(" ")
                        self.ilias_test_result1_formula.append(" ")
                    else:
                        self.ilias_test_variable1_min.append(" ")
                        self.ilias_test_variable1_prec.append(" ")
                        self.ilias_test_variable1_divby.append(" ")
                        self.ilias_test_variable1_max.append(" ")

                        self.ilias_test_result1_min.append(" ")
                        self.ilias_test_result1_max.append(" ")
                        self.ilias_test_result1_prec.append(" ")
                        self.ilias_test_result1_tol.append(" ")
                        self.ilias_test_result1_pts.append(" ")
                        self.ilias_test_result1_formula.append(" ")

                    if "1" in self.ilias_test_question_type_collection_mq_answers[i]:
                        self.ilias_test_variable2_min.append(self.mq_images_label[t + 1])
                        self.ilias_test_variable2_prec.append(self.mq_images_data_string[t + 1])
                        self.ilias_test_variable2_divby.append(" ")
                        self.ilias_test_variable2_max.append(self.mattext_text_all_mq_answers_collection[t + 1])

                        self.ilias_test_result2_min.append(" ")
                        self.ilias_test_result2_max.append(" ")
                        self.ilias_test_result2_prec.append(" ")
                        self.ilias_test_result2_tol.append(" ")
                        self.ilias_test_result2_pts.append(" ")
                        self.ilias_test_result2_formula.append(" ")
                    else:
                        self.ilias_test_variable2_min.append(" ")
                        self.ilias_test_variable2_prec.append(" ")
                        self.ilias_test_variable2_divby.append(" ")
                        self.ilias_test_variable2_max.append(" ")

                        self.ilias_test_result2_min.append(" ")
                        self.ilias_test_result2_max.append(" ")
                        self.ilias_test_result2_prec.append(" ")
                        self.ilias_test_result2_tol.append(" ")
                        self.ilias_test_result2_pts.append(" ")
                        self.ilias_test_result2_formula.append(" ")

                    if "2" in self.ilias_test_question_type_collection_mq_answers[i]:
                        self.ilias_test_variable3_min.append(self.mq_images_label[t + 2])
                        self.ilias_test_variable3_prec.append(self.mq_images_data_string[t + 2])
                        self.ilias_test_variable3_divby.append(" ")
                        self.ilias_test_variable3_max.append(self.mattext_text_all_mq_answers_collection[t + 2])

                        self.ilias_test_result3_min.append(" ")
                        self.ilias_test_result3_max.append(" ")
                        self.ilias_test_result3_prec.append(" ")
                        self.ilias_test_result3_tol.append(" ")
                        self.ilias_test_result3_pts.append(" ")
                        self.ilias_test_result3_formula.append(" ")
                    else:
                        self.ilias_test_variable3_min.append(" ")
                        self.ilias_test_variable3_prec.append(" ")
                        self.ilias_test_variable3_divby.append(" ")
                        self.ilias_test_variable3_max.append(" ")

                        self.ilias_test_result3_min.append(" ")
                        self.ilias_test_result3_max.append(" ")
                        self.ilias_test_result3_prec.append(" ")
                        self.ilias_test_result3_tol.append(" ")
                        self.ilias_test_result3_pts.append(" ")
                        self.ilias_test_result3_formula.append(" ")

                    if "3" in self.ilias_test_question_type_collection_mq_answers[i]:
                        self.ilias_test_variable4_min.append(self.mq_images_label[t + 3])
                        self.ilias_test_variable4_prec.append(self.mq_images_data_string[t + 3])
                        self.ilias_test_variable4_divby.append(" ")
                        self.ilias_test_variable4_max.append(self.mattext_text_all_mq_answers_collection[t + 3])

                        self.ilias_test_result4_min.append(" ")
                        self.ilias_test_result4_max.append(" ")
                        self.ilias_test_result4_prec.append(" ")
                        self.ilias_test_result4_tol.append(" ")
                        self.ilias_test_result4_pts.append(" ")
                        self.ilias_test_result4_formula.append(" ")
                    else:
                        self.ilias_test_variable4_min.append(" ")
                        self.ilias_test_variable4_prec.append(" ")
                        self.ilias_test_variable4_divby.append(" ")
                        self.ilias_test_variable4_max.append(" ")

                        self.ilias_test_result4_min.append(" ")
                        self.ilias_test_result4_max.append(" ")
                        self.ilias_test_result4_prec.append(" ")
                        self.ilias_test_result4_tol.append(" ")
                        self.ilias_test_result4_pts.append(" ")
                        self.ilias_test_result4_formula.append(" ")

                    if "4" in self.ilias_test_question_type_collection_mq_answers[i]:
                        self.ilias_test_variable5_min.append(self.mq_images_label[t + 4])
                        self.ilias_test_variable5_prec.append(self.mq_images_data_string[t + 4])
                        self.ilias_test_variable5_divby.append(" ")
                        self.ilias_test_variable5_max.append(self.mattext_text_all_mq_answers_collection[t + 4])

                        self.ilias_test_result5_min.append(" ")
                        self.ilias_test_result5_max.append(" ")
                        self.ilias_test_result5_prec.append(" ")
                        self.ilias_test_result5_tol.append(" ")
                        self.ilias_test_result5_pts.append(" ")
                        self.ilias_test_result5_formula.append(" ")
                    else:
                        self.ilias_test_variable5_min.append(" ")
                        self.ilias_test_variable5_prec.append(" ")
                        self.ilias_test_variable5_divby.append(" ")
                        self.ilias_test_variable5_max.append(" ")

                        self.ilias_test_result5_min.append(" ")
                        self.ilias_test_result5_max.append(" ")
                        self.ilias_test_result5_prec.append(" ")
                        self.ilias_test_result5_tol.append(" ")
                        self.ilias_test_result5_pts.append(" ")
                        self.ilias_test_result5_formula.append(" ")

                    if "5" in self.ilias_test_question_type_collection_mq_answers[i]:
                        self.ilias_test_variable6_min.append(self.mq_images_label[t + 5])
                        self.ilias_test_variable6_prec.append(self.mq_images_data_string[t + 5])
                        self.ilias_test_variable6_divby.append(" ")
                        self.ilias_test_variable6_max.append(self.mattext_text_all_mq_answers_collection[t + 5])

                        self.ilias_test_result6_min.append(" ")
                        self.ilias_test_result6_max.append(" ")
                        self.ilias_test_result6_prec.append(" ")
                        self.ilias_test_result6_tol.append(" ")
                        self.ilias_test_result6_pts.append(" ")
                        self.ilias_test_result6_formula.append(" ")
                    else:
                        self.ilias_test_variable6_min.append(" ")
                        self.ilias_test_variable6_prec.append(" ")
                        self.ilias_test_variable6_divby.append(" ")
                        self.ilias_test_variable6_max.append(" ")

                        self.ilias_test_result6_min.append(" ")
                        self.ilias_test_result6_max.append(" ")
                        self.ilias_test_result6_prec.append(" ")
                        self.ilias_test_result6_tol.append(" ")
                        self.ilias_test_result6_pts.append(" ")
                        self.ilias_test_result6_formula.append(" ")

                    if "6" in self.ilias_test_question_type_collection_mq_answers[i]:
                        self.ilias_test_variable7_min.append(self.mq_images_label[t + 6])
                        self.ilias_test_variable7_prec.append(self.mq_images_data_string[t + 6])
                        self.ilias_test_variable7_divby.append(" ")
                        self.ilias_test_variable7_max.append(self.mattext_text_all_mq_answers_collection[t + 6])

                        self.ilias_test_result7_min.append(" ")
                        self.ilias_test_result7_max.append(" ")
                        self.ilias_test_result7_prec.append(" ")
                        self.ilias_test_result7_tol.append(" ")
                        self.ilias_test_result7_pts.append(" ")
                        self.ilias_test_result7_formula.append(" ")
                    else:
                        self.ilias_test_variable7_min.append(" ")
                        self.ilias_test_variable7_prec.append(" ")
                        self.ilias_test_variable7_divby.append(" ")
                        self.ilias_test_variable7_max.append(" ")

                        self.ilias_test_result7_min.append(" ")
                        self.ilias_test_result7_max.append(" ")
                        self.ilias_test_result7_prec.append(" ")
                        self.ilias_test_result7_tol.append(" ")
                        self.ilias_test_result7_pts.append(" ")
                        self.ilias_test_result7_formula.append(" ")

                    if "7" in self.ilias_test_question_type_collection_mq_answers[i]:
                        self.ilias_test_variable8_min.append(self.mq_images_label[t + 7])
                        self.ilias_test_variable8_prec.append(self.mq_images_data_string[t + 7])
                        self.ilias_test_variable8_divby.append(" ")
                        self.ilias_test_variable8_max.append(self.mattext_text_all_mq_answers_collection[t + 7])

                        self.ilias_test_result8_min.append(" ")
                        self.ilias_test_result8_max.append(" ")
                        self.ilias_test_result8_prec.append(" ")
                        self.ilias_test_result8_tol.append(" ")
                        self.ilias_test_result8_pts.append(" ")
                        self.ilias_test_result8_formula.append(" ")
                    else:
                        self.ilias_test_variable8_min.append(" ")
                        self.ilias_test_variable8_prec.append(" ")
                        self.ilias_test_variable8_divby.append(" ")
                        self.ilias_test_variable8_max.append(" ")

                        self.ilias_test_result8_min.append(" ")
                        self.ilias_test_result8_max.append(" ")
                        self.ilias_test_result8_prec.append(" ")
                        self.ilias_test_result8_tol.append(" ")
                        self.ilias_test_result8_pts.append(" ")
                        self.ilias_test_result8_formula.append(" ")



                    if "8" in self.ilias_test_question_type_collection_mq_answers[i]:
                        self.ilias_test_variable9_min.append(self.mq_images_label[t + 8])
                        self.ilias_test_variable9_prec.append(self.mq_images_data_string[t + 8])
                        self.ilias_test_variable9_divby.append(" ")
                        self.ilias_test_variable9_max.append(self.mattext_text_all_mq_answers_collection[t + 8])

                        self.ilias_test_result9_min.append(" ")
                        self.ilias_test_result9_max.append(" ")
                        self.ilias_test_result9_prec.append(" ")
                        self.ilias_test_result9_tol.append(" ")
                        self.ilias_test_result9_pts.append(" ")
                        self.ilias_test_result9_formula.append(" ")
                    else:
                        self.ilias_test_variable9_min.append(" ")
                        self.ilias_test_variable9_prec.append(" ")
                        self.ilias_test_variable9_divby.append(" ")
                        self.ilias_test_variable9_max.append(" ")

                        self.ilias_test_result9_min.append(" ")
                        self.ilias_test_result9_max.append(" ")
                        self.ilias_test_result9_prec.append(" ")
                        self.ilias_test_result9_tol.append(" ")
                        self.ilias_test_result9_pts.append(" ")
                        self.ilias_test_result9_formula.append(" ")



                    if "9" in self.ilias_test_question_type_collection_mq_answers[i]:
                        self.ilias_test_variable10_min.append(self.mq_images_label[t + 9])
                        self.ilias_test_variable10_prec.append(self.mq_images_data_string[t + 9])
                        self.ilias_test_variable10_divby.append(" ")
                        self.ilias_test_variable10_max.append(self.mattext_text_all_mq_answers_collection[t + 9])

                        self.ilias_test_result10_min.append(" ")
                        self.ilias_test_result10_max.append(" ")
                        self.ilias_test_result10_prec.append(" ")
                        self.ilias_test_result10_tol.append(" ")
                        self.ilias_test_result10_pts.append(" ")
                        self.ilias_test_result10_formula.append(" ")
                    else:
                        self.ilias_test_variable10_min.append(" ")
                        self.ilias_test_variable10_prec.append(" ")
                        self.ilias_test_variable10_divby.append(" ")
                        self.ilias_test_variable10_max.append(" ")

                        self.ilias_test_result10_min.append(" ")
                        self.ilias_test_result10_max.append(" ")
                        self.ilias_test_result10_prec.append(" ")
                        self.ilias_test_result10_tol.append(" ")
                        self.ilias_test_result10_pts.append(" ")
                        self.ilias_test_result10_formula.append(" ")



                    t += int(max(self.ilias_test_question_type_collection_mq_answers[i])) + 1
        """
        print("77777777777777777777777777777777777")
        print(len(self.ilias_test_variable1_prec), len(self.ilias_test_variable1_divby), len(self.ilias_test_variable1_min), len(self.ilias_test_variable1_max))
        print(len(self.ilias_test_variable2_prec), len(self.ilias_test_variable2_divby), len(self.ilias_test_variable2_min), len(self.ilias_test_variable2_max))
        print(len(self.ilias_test_variable3_prec), len(self.ilias_test_variable3_divby), len(self.ilias_test_variable3_min), len(self.ilias_test_variable3_max))
        print(len(self.ilias_test_variable4_prec), len(self.ilias_test_variable4_divby), len(self.ilias_test_variable4_min), len(self.ilias_test_variable4_max))
        print(len(self.ilias_test_variable5_prec), len(self.ilias_test_variable5_divby), len(self.ilias_test_variable5_min), len(self.ilias_test_variable5_max))
        print(len(self.ilias_test_variable6_prec), len(self.ilias_test_variable6_divby), len(self.ilias_test_variable6_min), len(self.ilias_test_variable6_max))
        print(len(self.ilias_test_variable7_prec), len(self.ilias_test_variable7_divby), len(self.ilias_test_variable7_min), len(self.ilias_test_variable7_max))
        print(len(self.ilias_test_variable8_prec), len(self.ilias_test_variable8_divby), len(self.ilias_test_variable8_min), len(self.ilias_test_variable8_max))
        print(len(self.ilias_test_variable9_prec), len(self.ilias_test_variable9_divby), len(self.ilias_test_variable9_min), len(self.ilias_test_variable9_max))
        print(len(self.ilias_test_variable10_prec), len(self.ilias_test_variable10_divby), len(self.ilias_test_variable10_min), len(self.ilias_test_variable10_max))
        """


         # Listen auffüllen. Liste "Fragentitel" enthält die max. Anzahl an Fragen
        for i in range(len(self.ilias_test_variable1_min), len(self.ilias_test_title)):
            self.ilias_test_variable1_prec.append(" ")
            self.ilias_test_variable1_divby.append(" ")
            self.ilias_test_variable1_min.append(" ")
            self.ilias_test_variable1_max.append(" ")


        for i in range(len(self.ilias_test_variable2_min), len(self.ilias_test_title)):
            self.ilias_test_variable2_prec.append(" ")
            self.ilias_test_variable2_divby.append(" ")
            self.ilias_test_variable2_min.append(" ")
            self.ilias_test_variable2_max.append(" ")

        for i in range(len(self.ilias_test_variable3_min), len(self.ilias_test_title)):
            self.ilias_test_variable3_prec.append(" ")
            self.ilias_test_variable3_divby.append(" ")
            self.ilias_test_variable3_min.append(" ")
            self.ilias_test_variable3_max.append(" ")

        for i in range(len(self.ilias_test_variable4_min), len(self.ilias_test_title)):
            self.ilias_test_variable4_prec.append(" ")
            self.ilias_test_variable4_divby.append(" ")
            self.ilias_test_variable4_min.append(" ")
            self.ilias_test_variable4_max.append(" ")


        for i in range(len(self.ilias_test_variable5_min), len(self.ilias_test_title)):
            self.ilias_test_variable5_prec.append(" ")
            self.ilias_test_variable5_divby.append(" ")
            self.ilias_test_variable5_min.append(" ")
            self.ilias_test_variable5_max.append(" ")

        for i in range(len(self.ilias_test_variable6_min), len(self.ilias_test_title)):
            self.ilias_test_variable6_prec.append(" ")
            self.ilias_test_variable6_divby.append(" ")
            self.ilias_test_variable6_min.append(" ")
            self.ilias_test_variable6_max.append(" ")

        for i in range(len(self.ilias_test_variable7_min), len(self.ilias_test_title)):
            self.ilias_test_variable7_prec.append(" ")
            self.ilias_test_variable7_divby.append(" ")
            self.ilias_test_variable7_min.append(" ")
            self.ilias_test_variable7_max.append(" ")

        for i in range(len(self.ilias_test_variable8_min), len(self.ilias_test_title)):
            self.ilias_test_variable8_prec.append(" ")
            self.ilias_test_variable8_divby.append(" ")
            self.ilias_test_variable8_min.append(" ")
            self.ilias_test_variable8_max.append(" ")

        for i in range(len(self.ilias_test_variable9_min), len(self.ilias_test_title)):
            self.ilias_test_variable9_prec.append(" ")
            self.ilias_test_variable9_divby.append(" ")
            self.ilias_test_variable9_min.append(" ")
            self.ilias_test_variable9_max.append(" ")

        for i in range(len(self.ilias_test_variable10_min), len(self.ilias_test_title)):
            self.ilias_test_variable10_prec.append(" ")
            self.ilias_test_variable10_divby.append(" ")
            self.ilias_test_variable10_min.append(" ")
            self.ilias_test_variable10_max.append(" ")





        ### Ergebnis Listen auffüllen

        for i in range(len(self.ilias_test_result1_min), len(self.ilias_test_title)):
            self.ilias_test_result1_min.append(" ")
            self.ilias_test_result1_max.append(" ")
            self.ilias_test_result1_prec.append(" ")
            self.ilias_test_result1_tol.append(" ")
            self.ilias_test_result1_pts.append(" ")
            self.ilias_test_result1_formula.append(" ")

        for i in range(len(self.ilias_test_result2_min), len(self.ilias_test_title)):
            self.ilias_test_result2_min.append(" ")
            self.ilias_test_result2_max.append(" ")
            self.ilias_test_result2_prec.append(" ")
            self.ilias_test_result2_tol.append(" ")
            self.ilias_test_result2_pts.append(" ")
            self.ilias_test_result2_formula.append(" ")

        for i in range(len(self.ilias_test_result3_min), len(self.ilias_test_title)):
            self.ilias_test_result3_min.append(" ")
            self.ilias_test_result3_max.append(" ")
            self.ilias_test_result3_prec.append(" ")
            self.ilias_test_result3_tol.append(" ")
            self.ilias_test_result3_pts.append(" ")
            self.ilias_test_result3_formula.append(" ")


        for i in range(len(self.ilias_test_result4_min), len(self.ilias_test_title)):
            self.ilias_test_result4_min.append(" ")
            self.ilias_test_result4_max.append(" ")
            self.ilias_test_result4_prec.append(" ")
            self.ilias_test_result4_tol.append(" ")
            self.ilias_test_result4_pts.append(" ")
            self.ilias_test_result4_formula.append(" ")

        for i in range(len(self.ilias_test_result5_min), len(self.ilias_test_title)):
            self.ilias_test_result5_min.append(" ")
            self.ilias_test_result5_max.append(" ")
            self.ilias_test_result5_prec.append(" ")
            self.ilias_test_result5_tol.append(" ")
            self.ilias_test_result5_pts.append(" ")
            self.ilias_test_result5_formula.append(" ")

        for i in range(len(self.ilias_test_result6_min), len(self.ilias_test_title)):
            self.ilias_test_result6_min.append(" ")
            self.ilias_test_result6_max.append(" ")
            self.ilias_test_result6_prec.append(" ")
            self.ilias_test_result6_tol.append(" ")
            self.ilias_test_result6_pts.append(" ")
            self.ilias_test_result6_formula.append(" ")

        for i in range(len(self.ilias_test_result7_min), len(self.ilias_test_title)):
            self.ilias_test_result7_min.append(" ")
            self.ilias_test_result7_max.append(" ")
            self.ilias_test_result7_prec.append(" ")
            self.ilias_test_result7_tol.append(" ")
            self.ilias_test_result7_pts.append(" ")
            self.ilias_test_result7_formula.append(" ")

        for i in range(len(self.ilias_test_result8_min), len(self.ilias_test_title)):
            self.ilias_test_result8_min.append(" ")
            self.ilias_test_result8_max.append(" ")
            self.ilias_test_result8_prec.append(" ")
            self.ilias_test_result8_tol.append(" ")
            self.ilias_test_result8_pts.append(" ")
            self.ilias_test_result8_formula.append(" ")

        for i in range(len(self.ilias_test_result9_min), len(self.ilias_test_title)):
            self.ilias_test_result9_min.append(" ")
            self.ilias_test_result9_max.append(" ")
            self.ilias_test_result9_prec.append(" ")
            self.ilias_test_result9_tol.append(" ")
            self.ilias_test_result9_pts.append(" ")
            self.ilias_test_result9_formula.append(" ")

        for i in range(len(self.ilias_test_result10_min), len(self.ilias_test_title)):
            self.ilias_test_result10_min.append(" ")
            self.ilias_test_result10_max.append(" ")
            self.ilias_test_result10_prec.append(" ")
            self.ilias_test_result10_tol.append(" ")
            self.ilias_test_result10_pts.append(" ")
            self.ilias_test_result10_formula.append(" ")

        """
        print("aufgefüllt")
        print(len(self.ilias_test_variable1_prec), len(self.ilias_test_variable1_divby), len(self.ilias_test_variable1_min), len(self.ilias_test_variable1_max))
        print(len(self.ilias_test_variable2_prec), len(self.ilias_test_variable2_divby), len(self.ilias_test_variable2_min), len(self.ilias_test_variable2_max))
        print(len(self.ilias_test_variable3_prec), len(self.ilias_test_variable3_divby), len(self.ilias_test_variable3_min), len(self.ilias_test_variable3_max))
        print(len(self.ilias_test_variable4_prec), len(self.ilias_test_variable4_divby), len(self.ilias_test_variable4_min), len(self.ilias_test_variable4_max))
        print(len(self.ilias_test_variable5_prec), len(self.ilias_test_variable5_divby), len(self.ilias_test_variable5_min), len(self.ilias_test_variable5_max))
        print(len(self.ilias_test_variable6_prec), len(self.ilias_test_variable6_divby), len(self.ilias_test_variable6_min), len(self.ilias_test_variable6_max))
        print(len(self.ilias_test_variable7_prec), len(self.ilias_test_variable7_divby), len(self.ilias_test_variable7_min), len(self.ilias_test_variable7_max))
        print(len(self.ilias_test_variable8_prec), len(self.ilias_test_variable8_divby), len(self.ilias_test_variable8_min), len(self.ilias_test_variable8_max))
        print(len(self.ilias_test_variable9_prec), len(self.ilias_test_variable9_divby), len(self.ilias_test_variable9_min), len(self.ilias_test_variable9_max))
        print(len(self.ilias_test_variable10_prec), len(self.ilias_test_variable10_divby), len(self.ilias_test_variable10_min), len(self.ilias_test_variable10_max))
        """

        # Inhalt der Formeln prüfen


        #for i in range(len(self.ilias_test_result1_formula)):
        #    print(str(i+2) + " ----- " + str(self.ilias_test_result1_formula[i]) + " ,  " + str(self.ilias_test_result2_formula[i])+ " ,  " +  str(self.ilias_test_result3_formula[i])+ " ,  " +  str(self.ilias_test_result4_formula[i])+ " ,  " +  str(self.ilias_test_result5_formula[i]))

        #print("1: " + str(self.ilias_test_result1_formula))
        #print("2: " + str(self.ilias_test_result2_formula))
        #print("3: " + str(self.ilias_test_result3_formula))
        #print("4: " + str(self.ilias_test_result4_formula))
        #print("5: " + str(self.ilias_test_result5_formula))
        #print("6: " + str(self.ilias_test_result6_formula))
        #print("7: " + str(self.ilias_test_result7_formula))
        #print("8: " + str(self.ilias_test_result8_formula))
        #print("9: " + str(self.ilias_test_result9_formula))
        #print("10: " + str(self.ilias_test_result10_formula))









        print("========  Move elements in right order  ===========")
        print("Durchsuche in der Reihenfolge: Formelfragen, SingleChoice, MultipleChoice, MatchingQuestion")


        ### Index der Fragen wird in der Reihenfolge FF, SC, MC, MQ in eine Liste zusammengefasst
        for i in range(len(self.ilias_test_question_type_ff_question_index)):
            self.ilias_test_question_type_all_in_one_index.append(self.ilias_test_question_type_ff_question_index[i])
        for i in range(len(self.ilias_test_question_type_sc_question_index)):
            self.ilias_test_question_type_all_in_one_index.append(self.ilias_test_question_type_sc_question_index[i])
        for i in range(len(self.ilias_test_question_type_mc_question_index)):
            self.ilias_test_question_type_all_in_one_index.append(self.ilias_test_question_type_mc_question_index[i])
        for i in range(len(self.ilias_test_question_type_mq_question_index)):
            self.ilias_test_question_type_all_in_one_index.append(self.ilias_test_question_type_mq_question_index[i])



        #self.ilias_test_variable1_min_temp = []


        self.count_vari = 0


        print("444444444444444")
        print(self.ilias_test_variable1_min)
        print(self.ilias_test_variable2_min)
        print(self.ilias_test_variable3_min)
        print(self.ilias_test_variable4_min)
        print(self.ilias_test_variable5_min)
        print(self.ilias_test_variable6_min)
        print(self.ilias_test_variable7_min)
        print(self.ilias_test_variable8_min)
        print(self.ilias_test_variable9_min)
        print(self.ilias_test_variable10_min)

        while self.count_vari < len(self.ilias_test_question_type_all_in_one_index):
            for i in range(len(self.ilias_test_question_type_all_in_one_index)):
                if self.ilias_test_question_type_all_in_one_index[i] == str(self.count_vari):

                    self.ilias_test_variable1_prec_temp.append(self.ilias_test_variable1_prec[i])
                    self.ilias_test_variable1_divby_temp.append(self.ilias_test_variable1_divby[i])
                    self.ilias_test_variable1_min_temp.append(self.ilias_test_variable1_min[i])
                    self.ilias_test_variable1_max_temp.append(self.ilias_test_variable1_max[i])

                    self.ilias_test_variable2_prec_temp.append(self.ilias_test_variable2_prec[i])
                    self.ilias_test_variable2_divby_temp.append(self.ilias_test_variable2_divby[i])
                    self.ilias_test_variable2_min_temp.append(self.ilias_test_variable2_min[i])
                    self.ilias_test_variable2_max_temp.append(self.ilias_test_variable2_max[i])

                    self.ilias_test_variable3_prec_temp.append(self.ilias_test_variable3_prec[i])
                    self.ilias_test_variable3_divby_temp.append(self.ilias_test_variable3_divby[i])
                    self.ilias_test_variable3_min_temp.append(self.ilias_test_variable3_min[i])
                    self.ilias_test_variable3_max_temp.append(self.ilias_test_variable3_max[i])

                    self.ilias_test_variable4_prec_temp.append(self.ilias_test_variable4_prec[i])
                    self.ilias_test_variable4_divby_temp.append(self.ilias_test_variable4_divby[i])
                    self.ilias_test_variable4_min_temp.append(self.ilias_test_variable4_min[i])
                    self.ilias_test_variable4_max_temp.append(self.ilias_test_variable4_max[i])

                    self.ilias_test_variable5_prec_temp.append(self.ilias_test_variable5_prec[i])
                    self.ilias_test_variable5_divby_temp.append(self.ilias_test_variable5_divby[i])
                    self.ilias_test_variable5_min_temp.append(self.ilias_test_variable5_min[i])
                    self.ilias_test_variable5_max_temp.append(self.ilias_test_variable5_max[i])

                    self.ilias_test_variable6_prec_temp.append(self.ilias_test_variable6_prec[i])
                    self.ilias_test_variable6_divby_temp.append(self.ilias_test_variable6_divby[i])
                    self.ilias_test_variable6_min_temp.append(self.ilias_test_variable6_min[i])
                    self.ilias_test_variable6_max_temp.append(self.ilias_test_variable6_max[i])

                    self.ilias_test_variable7_prec_temp.append(self.ilias_test_variable7_prec[i])
                    self.ilias_test_variable7_divby_temp.append(self.ilias_test_variable7_divby[i])
                    self.ilias_test_variable7_min_temp.append(self.ilias_test_variable7_min[i])
                    self.ilias_test_variable7_max_temp.append(self.ilias_test_variable7_max[i])

                    self.ilias_test_variable8_prec_temp.append(self.ilias_test_variable8_prec[i])
                    self.ilias_test_variable8_divby_temp.append(self.ilias_test_variable8_divby[i])
                    self.ilias_test_variable8_min_temp.append(self.ilias_test_variable8_min[i])
                    self.ilias_test_variable8_max_temp.append(self.ilias_test_variable8_max[i])

                    self.ilias_test_variable9_prec_temp.append(self.ilias_test_variable9_prec[i])
                    self.ilias_test_variable9_divby_temp.append(self.ilias_test_variable9_divby[i])
                    self.ilias_test_variable9_min_temp.append(self.ilias_test_variable9_min[i])
                    self.ilias_test_variable9_max_temp.append(self.ilias_test_variable9_max[i])

                    self.ilias_test_variable10_prec_temp.append(self.ilias_test_variable10_prec[i])
                    self.ilias_test_variable10_divby_temp.append(self.ilias_test_variable10_divby[i])
                    self.ilias_test_variable10_min_temp.append(self.ilias_test_variable10_min[i])
                    self.ilias_test_variable10_max_temp.append(self.ilias_test_variable10_max[i])


                    self.ilias_test_result1_prec_temp.append(self.ilias_test_result1_prec[i])
                    self.ilias_test_result1_tol_temp.append(self.ilias_test_result1_tol[i])
                    self.ilias_test_result1_min_temp.append(self.ilias_test_result1_min[i])
                    self.ilias_test_result1_max_temp.append(self.ilias_test_result1_max[i])
                    self.ilias_test_result1_pts_temp.append(self.ilias_test_result1_pts[i])
                    self.ilias_test_result1_formula_temp.append(self.ilias_test_result1_formula[i])
                    self.ilias_test_result2_prec_temp.append(self.ilias_test_result2_prec[i])
                    self.ilias_test_result2_tol_temp.append(self.ilias_test_result2_tol[i])
                    self.ilias_test_result2_min_temp.append(self.ilias_test_result2_min[i])
                    self.ilias_test_result2_max_temp.append(self.ilias_test_result2_max[i])
                    self.ilias_test_result2_pts_temp.append(self.ilias_test_result2_pts[i])
                    self.ilias_test_result2_formula_temp.append(self.ilias_test_result2_formula[i])
                    self.ilias_test_result3_prec_temp.append(self.ilias_test_result3_prec[i])
                    self.ilias_test_result3_tol_temp.append(self.ilias_test_result3_tol[i])
                    self.ilias_test_result3_min_temp.append(self.ilias_test_result3_min[i])
                    self.ilias_test_result3_max_temp.append(self.ilias_test_result3_max[i])
                    self.ilias_test_result3_pts_temp.append(self.ilias_test_result3_pts[i])
                    self.ilias_test_result3_formula_temp.append(self.ilias_test_result3_formula[i])
                    self.ilias_test_result4_prec_temp.append(self.ilias_test_result4_prec[i])
                    self.ilias_test_result4_tol_temp.append(self.ilias_test_result4_tol[i])
                    self.ilias_test_result4_min_temp.append(self.ilias_test_result4_min[i])
                    self.ilias_test_result4_max_temp.append(self.ilias_test_result4_max[i])
                    self.ilias_test_result4_pts_temp.append(self.ilias_test_result4_pts[i])
                    self.ilias_test_result4_formula_temp.append(self.ilias_test_result4_formula[i])
                    self.ilias_test_result5_prec_temp.append(self.ilias_test_result5_prec[i])
                    self.ilias_test_result5_tol_temp.append(self.ilias_test_result5_tol[i])
                    self.ilias_test_result5_min_temp.append(self.ilias_test_result5_min[i])
                    self.ilias_test_result5_max_temp.append(self.ilias_test_result5_max[i])
                    self.ilias_test_result5_pts_temp.append(self.ilias_test_result5_pts[i])
                    self.ilias_test_result5_formula_temp.append(self.ilias_test_result5_formula[i])
                    self.ilias_test_result6_prec_temp.append(self.ilias_test_result6_prec[i])
                    self.ilias_test_result6_tol_temp.append(self.ilias_test_result6_tol[i])
                    self.ilias_test_result6_min_temp.append(self.ilias_test_result6_min[i])
                    self.ilias_test_result6_max_temp.append(self.ilias_test_result6_max[i])
                    self.ilias_test_result6_pts_temp.append(self.ilias_test_result6_pts[i])
                    self.ilias_test_result6_formula_temp.append(self.ilias_test_result6_formula[i])
                    self.ilias_test_result7_prec_temp.append(self.ilias_test_result7_prec[i])
                    self.ilias_test_result7_tol_temp.append(self.ilias_test_result7_tol[i])
                    self.ilias_test_result7_min_temp.append(self.ilias_test_result7_min[i])
                    self.ilias_test_result7_max_temp.append(self.ilias_test_result7_max[i])
                    self.ilias_test_result7_pts_temp.append(self.ilias_test_result7_pts[i])
                    self.ilias_test_result7_formula_temp.append(self.ilias_test_result7_formula[i])
                    self.ilias_test_result8_prec_temp.append(self.ilias_test_result8_prec[i])
                    self.ilias_test_result8_tol_temp.append(self.ilias_test_result8_tol[i])
                    self.ilias_test_result8_min_temp.append(self.ilias_test_result8_min[i])
                    self.ilias_test_result8_max_temp.append(self.ilias_test_result8_max[i])
                    self.ilias_test_result8_pts_temp.append(self.ilias_test_result8_pts[i])
                    self.ilias_test_result8_formula_temp.append(self.ilias_test_result8_formula[i])
                    self.ilias_test_result9_prec_temp.append(self.ilias_test_result9_prec[i])
                    self.ilias_test_result9_tol_temp.append(self.ilias_test_result9_tol[i])
                    self.ilias_test_result9_min_temp.append(self.ilias_test_result9_min[i])
                    self.ilias_test_result9_max_temp.append(self.ilias_test_result9_max[i])
                    self.ilias_test_result9_pts_temp.append(self.ilias_test_result9_pts[i])
                    self.ilias_test_result9_formula_temp.append(self.ilias_test_result9_formula[i])
                    self.ilias_test_result10_prec_temp.append(self.ilias_test_result10_prec[i])
                    self.ilias_test_result10_tol_temp.append(self.ilias_test_result10_tol[i])
                    self.ilias_test_result10_min_temp.append(self.ilias_test_result10_min[i])
                    self.ilias_test_result10_max_temp.append(self.ilias_test_result10_max[i])
                    self.ilias_test_result10_pts_temp.append(self.ilias_test_result10_pts[i])
                    self.ilias_test_result10_formula_temp.append(self.ilias_test_result10_formula[i])



                    self.count_vari = self.count_vari + 1






        for i in range(len(self.ilias_test_variable1_min_temp)):
            #self.ilias_test_variable1_min[i] = self.ilias_test_variable1_min_temp[i]

            self.ilias_test_variable1_prec[i], self.ilias_test_variable1_divby[i], self.ilias_test_variable1_min[i], self.ilias_test_variable1_max[i] = self.ilias_test_variable1_prec_temp[i], self.ilias_test_variable1_divby_temp[i], self.ilias_test_variable1_min_temp[i], self.ilias_test_variable1_max_temp[i]
            self.ilias_test_variable2_prec[i], self.ilias_test_variable2_divby[i], self.ilias_test_variable2_min[i], self.ilias_test_variable2_max[i] = self.ilias_test_variable2_prec_temp[i], self.ilias_test_variable2_divby_temp[i], self.ilias_test_variable2_min_temp[i], self.ilias_test_variable2_max_temp[i]
            self.ilias_test_variable3_prec[i], self.ilias_test_variable3_divby[i], self.ilias_test_variable3_min[i], self.ilias_test_variable3_max[i] = self.ilias_test_variable3_prec_temp[i], self.ilias_test_variable3_divby_temp[i], self.ilias_test_variable3_min_temp[i], self.ilias_test_variable3_max_temp[i]
            self.ilias_test_variable4_prec[i], self.ilias_test_variable4_divby[i], self.ilias_test_variable4_min[i], self.ilias_test_variable4_max[i] = self.ilias_test_variable4_prec_temp[i], self.ilias_test_variable4_divby_temp[i], self.ilias_test_variable4_min_temp[i], self.ilias_test_variable4_max_temp[i]
            self.ilias_test_variable5_prec[i], self.ilias_test_variable5_divby[i], self.ilias_test_variable5_min[i], self.ilias_test_variable5_max[i] = self.ilias_test_variable5_prec_temp[i], self.ilias_test_variable5_divby_temp[i], self.ilias_test_variable5_min_temp[i], self.ilias_test_variable5_max_temp[i]
            self.ilias_test_variable6_prec[i], self.ilias_test_variable6_divby[i], self.ilias_test_variable6_min[i], self.ilias_test_variable6_max[i] = self.ilias_test_variable6_prec_temp[i], self.ilias_test_variable6_divby_temp[i], self.ilias_test_variable6_min_temp[i], self.ilias_test_variable6_max_temp[i]
            self.ilias_test_variable7_prec[i], self.ilias_test_variable7_divby[i], self.ilias_test_variable7_min[i], self.ilias_test_variable7_max[i] = self.ilias_test_variable7_prec_temp[i], self.ilias_test_variable7_divby_temp[i], self.ilias_test_variable7_min_temp[i], self.ilias_test_variable7_max_temp[i]
            self.ilias_test_variable8_prec[i], self.ilias_test_variable8_divby[i], self.ilias_test_variable8_min[i], self.ilias_test_variable8_max[i] = self.ilias_test_variable8_prec_temp[i], self.ilias_test_variable8_divby_temp[i], self.ilias_test_variable8_min_temp[i], self.ilias_test_variable8_max_temp[i]
            self.ilias_test_variable9_prec[i], self.ilias_test_variable9_divby[i], self.ilias_test_variable9_min[i], self.ilias_test_variable9_max[i] = self.ilias_test_variable9_prec_temp[i], self.ilias_test_variable9_divby_temp[i], self.ilias_test_variable9_min_temp[i], self.ilias_test_variable9_max_temp[i]
            self.ilias_test_variable10_prec[i], self.ilias_test_variable10_divby[i], self.ilias_test_variable10_min[i], self.ilias_test_variable10_max[i] = self.ilias_test_variable10_prec_temp[i], self.ilias_test_variable10_divby_temp[i], self.ilias_test_variable10_min_temp[i], self.ilias_test_variable10_max_temp[i]

            self.ilias_test_result1_prec[i], self.ilias_test_result1_tol[i], self.ilias_test_result1_min[i], self.ilias_test_result1_max[i], self.ilias_test_result1_pts[i], self.ilias_test_result1_formula[i] = self.ilias_test_result1_prec_temp[i], self.ilias_test_result1_tol_temp[i], self.ilias_test_result1_min_temp[i], self.ilias_test_result1_max_temp[i], self.ilias_test_result1_pts_temp[i], self.ilias_test_result1_formula_temp[i]
            self.ilias_test_result2_prec[i], self.ilias_test_result2_tol[i], self.ilias_test_result2_min[i], self.ilias_test_result2_max[i], self.ilias_test_result2_pts[i], self.ilias_test_result2_formula[i] = self.ilias_test_result2_prec_temp[i], self.ilias_test_result2_tol_temp[i], self.ilias_test_result2_min_temp[i], self.ilias_test_result2_max_temp[i], self.ilias_test_result2_pts_temp[i], self.ilias_test_result2_formula_temp[i]
            self.ilias_test_result3_prec[i], self.ilias_test_result3_tol[i], self.ilias_test_result3_min[i], self.ilias_test_result3_max[i], self.ilias_test_result3_pts[i], self.ilias_test_result3_formula[i] = self.ilias_test_result3_prec_temp[i], self.ilias_test_result3_tol_temp[i], self.ilias_test_result3_min_temp[i], self.ilias_test_result3_max_temp[i], self.ilias_test_result3_pts_temp[i], self.ilias_test_result3_formula_temp[i]
            self.ilias_test_result4_prec[i], self.ilias_test_result4_tol[i], self.ilias_test_result4_min[i], self.ilias_test_result4_max[i], self.ilias_test_result4_pts[i], self.ilias_test_result4_formula[i] = self.ilias_test_result4_prec_temp[i], self.ilias_test_result4_tol_temp[i], self.ilias_test_result4_min_temp[i], self.ilias_test_result4_max_temp[i], self.ilias_test_result4_pts_temp[i], self.ilias_test_result4_formula_temp[i]
            self.ilias_test_result5_prec[i], self.ilias_test_result5_tol[i], self.ilias_test_result5_min[i], self.ilias_test_result5_max[i], self.ilias_test_result5_pts[i], self.ilias_test_result5_formula[i] = self.ilias_test_result5_prec_temp[i], self.ilias_test_result5_tol_temp[i], self.ilias_test_result5_min_temp[i], self.ilias_test_result5_max_temp[i], self.ilias_test_result5_pts_temp[i], self.ilias_test_result5_formula_temp[i]
            self.ilias_test_result6_prec[i], self.ilias_test_result6_tol[i], self.ilias_test_result6_min[i], self.ilias_test_result6_max[i], self.ilias_test_result6_pts[i], self.ilias_test_result6_formula[i] = self.ilias_test_result6_prec_temp[i], self.ilias_test_result6_tol_temp[i], self.ilias_test_result6_min_temp[i], self.ilias_test_result6_max_temp[i], self.ilias_test_result6_pts_temp[i], self.ilias_test_result6_formula_temp[i]
            self.ilias_test_result7_prec[i], self.ilias_test_result7_tol[i], self.ilias_test_result7_min[i], self.ilias_test_result7_max[i], self.ilias_test_result7_pts[i], self.ilias_test_result7_formula[i] = self.ilias_test_result7_prec_temp[i], self.ilias_test_result7_tol_temp[i], self.ilias_test_result7_min_temp[i], self.ilias_test_result7_max_temp[i], self.ilias_test_result7_pts_temp[i], self.ilias_test_result7_formula_temp[i]
            self.ilias_test_result8_prec[i], self.ilias_test_result8_tol[i], self.ilias_test_result8_min[i], self.ilias_test_result8_max[i], self.ilias_test_result8_pts[i], self.ilias_test_result8_formula[i] = self.ilias_test_result8_prec_temp[i], self.ilias_test_result8_tol_temp[i], self.ilias_test_result8_min_temp[i], self.ilias_test_result8_max_temp[i], self.ilias_test_result8_pts_temp[i], self.ilias_test_result8_formula_temp[i]
            self.ilias_test_result9_prec[i], self.ilias_test_result9_tol[i], self.ilias_test_result9_min[i], self.ilias_test_result9_max[i], self.ilias_test_result9_pts[i], self.ilias_test_result9_formula[i] = self.ilias_test_result9_prec_temp[i], self.ilias_test_result9_tol_temp[i], self.ilias_test_result9_min_temp[i], self.ilias_test_result9_max_temp[i], self.ilias_test_result9_pts_temp[i], self.ilias_test_result9_formula_temp[i]
            self.ilias_test_result10_prec[i], self.ilias_test_result10_tol[i], self.ilias_test_result10_min[i], self.ilias_test_result10_max[i], self.ilias_test_result10_pts[i], self.ilias_test_result10_formula[i] = self.ilias_test_result10_prec_temp[i], self.ilias_test_result10_tol_temp[i], self.ilias_test_result10_min_temp[i], self.ilias_test_result10_max_temp[i], self.ilias_test_result10_pts_temp[i], self.ilias_test_result10_formula_temp[i]












        print("////////////////////////////////////////")
        print(self.ilias_test_variable1_min)
        print(self.ilias_test_variable2_min)
        print(self.ilias_test_variable3_min)
        print(self.ilias_test_variable4_min)
        print(self.ilias_test_variable5_min)
        print(self.ilias_test_variable6_min)
        print(self.ilias_test_variable7_min)
        print(self.ilias_test_variable8_min)
        print(self.ilias_test_variable9_min)
        print(self.ilias_test_variable10_min)







        # Daten in die SQL-Datenbank einfügen
        conn = sqlite3.connect('ilias_questions_db.db')
        c = conn.cursor()
        conn.commit()






        for i in range(len(self.ilias_test_title)):

            # Bilder der Reihe nach einlesen
            if self.ilias_test_question_description_image_uri[i] != "EMPTY":

                with open(os.path.normpath(os.path.join(self.select_test_import_file, self.ilias_test_question_description_image_uri[i])), 'rb') as image_file:
                    self.ilias_test_question_description_image_data.append(image_file.read())

            else:
                self.ilias_test_question_description_image_data.append("EMPTY")




            c.execute(
                    "INSERT INTO my_table VALUES ("
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
                    ":img_name, :img_data, :test_time, :var_number, :res_number, :question_pool_tag)",
                    {
                        'question_difficulty': "",
                        'question_category':  "",
                        'question_type': self.ilias_test_question_type[i],
                        'question_title': self.ilias_test_title[i],
                        'question_description_title': self.ilias_test_question_description_title[i],
                        'question_description_main': self.test_list1_l_join[i],

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

                        'img_name': self.ilias_test_question_description_image_name[i],
                        'img_data': self.ilias_test_question_description_image_data[i],

                        'test_time': self.ilias_test_duration[i],
                        'var_number':  "",
                        'res_number':  "",
                        'question_pool_tag':  ""
                    }
                )
        conn.commit()
        conn.close()

        print("Test importiert!")


