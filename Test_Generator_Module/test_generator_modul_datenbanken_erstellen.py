import sqlite3
import os
import xlsxwriter                       # import/export von excel Dateien
import pandas as pd
from tkinter import filedialog
import pathlib
import collections.abc as byteobj
import base64
from datetime import datetime

class CreateDatabases:

    def __init__(self, project_root_path):
        self.project_root_path = project_root_path

        self.database_formelfrage_path = os.path.normpath(os.path.join(self.project_root_path, "Test_Generator_Datenbanken", "ilias_formelfrage_db.db"))
        self.database_singlechoice_path = os.path.normpath(os.path.join(self.project_root_path, "Test_Generator_Datenbanken", "ilias_singlechoice_db.db"))
        self.database_multiplechoice_path = os.path.normpath(os.path.join(self.project_root_path, "Test_Generator_Datenbanken", "ilias_multiplechoice_db.db"))
        self.database_zuordnungsfrage_path = os.path.normpath(os.path.join(self.project_root_path, "Test_Generator_Datenbanken", "ilias_zuordnungsfrage_db.db"))


        self.database_formelfrage_permutation_path = os.path.normpath(os.path.join(self.project_root_path,"Test_Generator_Datenbanken", "ilias_formelfrage_permutation_db.db"))
        self.database_test_settings_profiles_path = os.path.normpath(os.path.join(self.project_root_path, "Test_Generator_Datenbanken", "test_settings_profiles_db.db"))

        # Prüfen ob die Datenbank vorhanden ist
        self.database_formelfrage_exists = os.path.exists(self.database_formelfrage_path)
        self.database_formelfrage_permutation_exists = os.path.exists(self.database_formelfrage_permutation_path)
        self.database_singlechoice_exists = os.path.exists(self.database_singlechoice_path)
        self.database_multiplechoice_exists = os.path.exists(self.database_multiplechoice_path)
        self.database_zuordnungsfrage_exists = os.path.exists(self.database_zuordnungsfrage_path)

        self.database_test_settings_profiles_exists = os.path.exists(self.database_test_settings_profiles_path)

        print("##    Datenbank -> Formelfrage:                        " + str(self.database_formelfrage_exists))
        print("##    Datenbank -> SingleChoice:                       " + str(self.database_singlechoice_exists))
        print("##    Datenbank -> MultipleChoice:                     " + str(self.database_multiplechoice_exists))
        print("##    Datenbank -> Zuordnungsfrage:                    " + str(self.database_zuordnungsfrage_exists))
        print("##    Datenbank -> Formelfrage_Permutation:            " + str(self.database_formelfrage_permutation_exists))
        print("##    Datenbank -> Test-Einstellungen_Profile:         " + str(self.database_test_settings_profiles_exists))
        print("\n")

####### Neue -- FORMELFRAGE --  Datenbank erstellen und befüllen #########

    def create_database_formelfrage(self):
        if self.database_formelfrage_exists != True:


            # Create a database or connect to one
            conn = sqlite3.connect(self.database_formelfrage_path)

            # Create cursor
            c = conn.cursor()

            # Create table
            c.execute("""CREATE TABLE IF NOT EXISTS formelfrage_table (
                    question_difficulty text,
                    question_category text,
                    question_type text,
                    question_title text,
                    question_description_title text,
                    question_description_main text,
                    res1_formula text,
                    res2_formula text,
                    res3_formula text,
                    res4_formula text,
                    res5_formula text,
                    res6_formula text,
                    res7_formula text,
                    res8_formula text,
                    res9_formula text,
                    res10_formula text,
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
                    var8_name text,
                    var8_min int,
                    var8_max int,
                    var8_prec int,
                    var8_divby int,
                    var8_unit text,
                    var9_name text,
                    var9_min int,
                    var9_max int,
                    var9_prec int,
                    var9_divby int,
                    var9_unit text,
                    var10_name text,
                    var10_min int,
                    var10_max int,
                    var10_prec int,
                    var10_divby int,
                    var10_unit text,
                    var11_name text,
                    var11_min int,
                    var11_max int,
                    var11_prec int,
                    var11_divby int,
                    var11_unit text,
                    var12_name text,
                    var12_min int,
                    var12_max int,
                    var12_prec int,
                    var12_divby int,
                    var12_unit text,
                    var13_name text,
                    var13_min int,
                    var13_max int,
                    var13_prec int,
                    var13_divby int,
                    var13_unit text,
                    var14_name text,
                    var14_min int,
                    var14_max int,
                    var14_prec int,
                    var14_divby int,
                    var14_unit text,
                    var15_name text,
                    var15_min int,
                    var15_max int,
                    var15_prec int,
                    var15_divby int,
                    var15_unit text,
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
                    res4_name text,
                    res4_min int,
                    res4_max int,
                    res4_prec int,
                    res4_tol int,
                    res4_points int,
                    res4_unit text,
                    res5_name text,
                    res5_min int,
                    res5_max int,
                    res5_prec int,
                    res5_tol int,
                    res5_points int,
                    res5_unit text,
                    res6_name text,
                    res6_min int,
                    res6_max int,
                    res6_prec int,
                    res6_tol int,
                    res6_points int,
                    res6_unit text,
                    res7_name text,
                    res7_min int,
                    res7_max int,
                    res7_prec int,
                    res7_tol int,
                    res7_points int,
                    res7_unit text,
                    res8_name text,
                    res8_min int,
                    res8_max int,
                    res8_prec int,
                    res8_tol int,
                    res8_points int,
                    res8_unit text,
                    res9_name text,
                    res9_min int,
                    res9_max int,
                    res9_prec int,
                    res9_tol int,
                    res9_points int,
                    res9_unit text,
                    res10_name text,
                    res10_min int,
                    res10_max int,
                    res10_prec int,
                    res10_tol int,
                    res10_points int,
                    res10_unit text,
                    
                    description_img_name_1 text,
                    description_img_data_1 blop,
                    description_img_path_1 text,
                    
                    description_img_name_2 text,
                    description_img_data_2 blop,
                    description_img_path_2 text,
                    
                    description_img_name_3 text,
                    description_img_data_3 blop,
                    description_img_path_3 text,
                    
                    test_time text,
                    var_number int,
                    res_number int,
                    question_pool_tag text,
                    question_author text
                    )""")


            # Commit Changes
            conn.commit()

            # Close Connection
            conn.close()


            print("Neue Formelfrage Datenbank erstellt! Wird mit Vorlage_Werten befüllt..")

            CreateDatabases.insert_template_to_database_formelfrage(self)

    def insert_template_to_database_formelfrage(self):
        # Create a database or connect to one
        connect = sqlite3.connect(self.database_formelfrage_path)

        # Create cursor
        cursor = connect.cursor()

        # Insert into Table
        cursor.execute(
            "INSERT INTO formelfrage_table VALUES ("
            ":question_difficulty, :question_category, :question_type, "
            ":question_title, :question_description_title, :question_description_main, "
            ":res1_formula, :res2_formula, :res3_formula,  "
            ":res4_formula, :res5_formula, :res6_formula,  "
            ":res7_formula, :res8_formula, :res9_formula, :res10_formula,  "
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
            ":res3_name, :res3_min, :res3_max, :res3_prec, :res3_tol, :res3_points, :res3_unit, "
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
                'question_difficulty': "question_difficulty",
                'question_category': "question_category",
                'question_type': "question_type",

                'question_title': "question_title",
                'question_description_title': "question_description_title",
                'question_description_main': "question_description_main",

                'res1_formula': "res1_formula",
                'res2_formula': "res2_formula",
                'res3_formula': "res3_formula",
                'res4_formula': "res4_formula",
                'res5_formula': "res5_formula",
                'res6_formula': "res6_formula",
                'res7_formula': "res7_formula",
                'res8_formula': "res8_formula",
                'res9_formula': "res9_formula",
                'res10_formula': "res10_formula",

                'var1_name': "var1_name",
                'var1_min': "var1_min",
                'var1_max': "var1_max",
                'var1_prec': "var1_prec",
                'var1_divby': "var1_divby",
                'var1_unit': "var1_unit",

                'var2_name': "var2_name",
                'var2_min': "var2_min",
                'var2_max': "var2_max",
                'var2_prec': "var2_prec",
                'var2_divby': "var2_divby",
                'var2_unit': "var2_unit",

                'var3_name': "var3_name",
                'var3_min': "var3_min",
                'var3_max': "var3_max",
                'var3_prec': "var3_prec",
                'var3_divby': "var3_divby",
                'var3_unit': "var3_unit",

                'var4_name': "var4_name",
                'var4_min': "var4_min",
                'var4_max': "var4_max",
                'var4_prec': "var4_prec",
                'var4_divby': "var4_divby",
                'var4_unit': "var4_unit",

                'var5_name': "var5_name",
                'var5_min': "var5_min",
                'var5_max': "var5_max",
                'var5_prec': "var5_prec",
                'var5_divby': "var5_divby",
                'var5_unit': "var5_unit",

                'var6_name': "var6_name",
                'var6_min': "var6_min",
                'var6_max': "var6_max",
                'var6_prec': "var6_prec",
                'var6_divby': "var6_divby",
                'var6_unit': "var6_unit",

                'var7_name': "var7_name",
                'var7_min': "var7_min",
                'var7_max': "var7_max",
                'var7_prec': "var7_prec",
                'var7_divby': "var7_divby",
                'var7_unit': "var7_unit",

                'var8_name': "var8_name",
                'var8_min': "var8_min",
                'var8_max': "var8_max",
                'var8_prec': "var8_prec",
                'var8_divby': "var8_divby",
                'var8_unit': "var8_unit",

                'var9_name': "var9_name",
                'var9_min': "var9_min",
                'var9_max': "var9_max",
                'var9_prec': "var9_prec",
                'var9_divby': "var9_divby",
                'var9_unit': "var9_unit",

                'var10_name': "var10_name",
                'var10_min': "var10_min",
                'var10_max': "var10_max",
                'var10_prec': "var10_prec",
                'var10_divby': "var10_divby",
                'var10_unit': "var10_unit",

                'var11_name': "var11_name",
                'var11_min': "var11_min",
                'var11_max': "var11_max",
                'var11_prec': "var11_prec",
                'var11_divby': "var11_divby",
                'var11_unit': "var11_unit",

                'var12_name': "var12_name",
                'var12_min': "var12_min",
                'var12_max': "var12_max",
                'var12_prec': "var12_prec",
                'var12_divby': "var12_divby",
                'var12_unit': "var12_unit",

                'var13_name': "var13_name",
                'var13_min': "var13_min",
                'var13_max': "var13_max",
                'var13_prec': "var13_prec",
                'var13_divby': "var13_divby",
                'var13_unit': "var13_unit",

                'var14_name': "var14_name",
                'var14_min': "var14_min",
                'var14_max': "var14_max",
                'var14_prec': "var14_prec",
                'var14_divby': "var14_divby",
                'var14_unit': "var14_unit",

                'var15_name': "var15_name",
                'var15_min': "var15_min",
                'var15_max': "var15_max",
                'var15_prec': "var15_prec",
                'var15_divby': "var15_divby",
                'var15_unit': "var15_unit",

                'res1_name': "res1_name",
                'res1_min': "res1_min",
                'res1_max': "res1_max",
                'res1_prec': "res1_prec",
                'res1_tol': "res1_tol",
                'res1_points': "res1_points",
                'res1_unit': "res1_unit",

                'res2_name': "res2_name",
                'res2_min': "res2_min",
                'res2_max': "res2_max",
                'res2_prec': "res2_prec",
                'res2_tol': "res2_tol",
                'res2_points': "res2_points",
                'res2_unit': "res2_unit",

                'res3_name': "res3_name",
                'res3_min': "res3_min",
                'res3_max': "res3_max",
                'res3_prec': "res3_prec",
                'res3_tol': "res3_tol",
                'res3_points': "res3_points",
                'res3_unit': "res3_unit",

                'res4_name': "res4_name",
                'res4_min': "res4_min",
                'res4_max': "res4_max",
                'res4_prec': "res4_prec",
                'res4_tol': "res4_tol",
                'res4_points': "res4_points",
                'res4_unit': "res4_unit",

                'res5_name': "res5_name",
                'res5_min': "res5_min",
                'res5_max': "res5_max",
                'res5_prec': "res5_prec",
                'res5_tol': "res5_tol",
                'res5_points': "res5_points",
                'res5_unit': "res5_unit",

                'res6_name': "res6_name",
                'res6_min': "res6_min",
                'res6_max': "res6_max",
                'res6_prec': "res6_prec",
                'res6_tol': "res6_tol",
                'res6_points': "res6_points",
                'res6_unit': "res6_unit",

                'res7_name': "res7_name",
                'res7_min': "res7_min",
                'res7_max': "res7_max",
                'res7_prec': "res7_prec",
                'res7_tol': "res7_tol",
                'res7_points': "res7_points",
                'res7_unit': "res7_unit",

                'res8_name': "res8_name",
                'res8_min': "res8_min",
                'res8_max': "res8_max",
                'res8_prec': "res8_prec",
                'res8_tol': "res8_tol",
                'res8_points': "res8_points",
                'res8_unit': "res8_unit",

                'res9_name': "res9_name",
                'res9_min': "res9_min",
                'res9_max': "res9_max",
                'res9_prec': "res9_prec",
                'res9_tol': "res9_tol",
                'res9_points': "res9_points",
                'res9_unit': "res9_unit",

                'res10_name': "res10_name",
                'res10_min': "res10_min",
                'res10_max': "res10_max",
                'res10_prec': "res10_prec",
                'res10_tol': "res10_tol",
                'res10_points': "res10_points",
                'res10_unit': "res10_unit",

                'description_img_name_1': "description_img_name_1",
                'description_img_data_1': "description_img_data_1",
                'description_img_path_1': "description_img_path_1",

                'description_img_name_2': "description_img_name_2",
                'description_img_data_2': "description_img_data_2",
                'description_img_path_2': "description_img_path_2",

                'description_img_name_3': "description_img_name_3",
                'description_img_data_3': "description_img_data_3",
                'description_img_path_3': "description_img_path_3",

                'test_time': "test_time",
                'var_number': "var_number",
                'res_number': "res_number",
                'question_pool_tag': "question_pool_tag",
                'question_author': "question_author"
            }
        )


        # Commit Changes
        connect.commit()

        # Close Connection
        connect.close()

        print("Eintrag \"Vorlage\" zur Formelfrage Datenbank hinzugefügt!")

####### Neue -- FORMELFRAGE --  Datenbank erstellen und befüllen #########

    def create_database_formelfrage_permutation(self):
        if self.database_formelfrage_permutation_exists != True:


            # Create a database or connect to one
            conn = sqlite3.connect(self.database_formelfrage_permutation_path)

            # Create cursor
            c = conn.cursor()

            # Create table
            c.execute("""CREATE TABLE IF NOT EXISTS formelfrage_permutation_table (
                    question_difficulty text,
                    question_category text,
                    question_type text,
                    question_title text,
                    question_description_title text,
                    question_description_main text,
                    res1_formula text,
                    res2_formula text,
                    res3_formula text,
                    res4_formula text,
                    res5_formula text,
                    res6_formula text,
                    res7_formula text,
                    res8_formula text,
                    res9_formula text,
                    res10_formula text,
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
                    var8_name text,
                    var8_min int,
                    var8_max int,
                    var8_prec int,
                    var8_divby int,
                    var8_unit text,
                    var9_name text,
                    var9_min int,
                    var9_max int,
                    var9_prec int,
                    var9_divby int,
                    var9_unit text,
                    var10_name text,
                    var10_min int,
                    var10_max int,
                    var10_prec int,
                    var10_divby int,
                    var10_unit text,
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
                    res4_name text,
                    res4_min int,
                    res4_max int,
                    res4_prec int,
                    res4_tol int,
                    res4_points int,
                    res4_unit text,
                    res5_name text,
                    res5_min int,
                    res5_max int,
                    res5_prec int,
                    res5_tol int,
                    res5_points int,
                    res5_unit text,
                    res6_name text,
                    res6_min int,
                    res6_max int,
                    res6_prec int,
                    res6_tol int,
                    res6_points int,
                    res6_unit text,
                    res7_name text,
                    res7_min int,
                    res7_max int,
                    res7_prec int,
                    res7_tol int,
                    res7_points int,
                    res7_unit text,
                    res8_name text,
                    res8_min int,
                    res8_max int,
                    res8_prec int,
                    res8_tol int,
                    res8_points int,
                    res8_unit text,
                    res9_name text,
                    res9_min int,
                    res9_max int,
                    res9_prec int,
                    res9_tol int,
                    res9_points int,
                    res9_unit text,
                    res10_name text,
                    res10_min int,
                    res10_max int,
                    res10_prec int,
                    res10_tol int,
                    res10_points int,
                    res10_unit text,
                    
                    
                    perm_var_symbol_1 text,
                    perm_var_value_1 text,
                    perm_var_symbol_2 text,
                    perm_var_value_2 text,
                    perm_var_symbol_3 text,
                    perm_var_value_3 text,
                    perm_var_symbol_4 text,
                    perm_var_value_4 text,
                    perm_var_symbol_5 text,
                    perm_var_value_5 text,
                    perm_var_symbol_6 text,
                    perm_var_value_6 text,
                    perm_var_symbol_7 text,
                    perm_var_value_7 text,
                    perm_var_symbol_8 text,
                    perm_var_value_8 text,
                    perm_var_symbol_9 text,
                    perm_var_value_9 text,
                    perm_var_symbol_10 text,
                    perm_var_value_10 text,
                    
                    
                    description_img_name_1 text,
                    description_img_data_1 blop,
                    description_img_path_1 text,
                    
                    description_img_name_2 text,
                    description_img_data_2 blop,
                    description_img_path_2 text,
                    
                    description_img_name_3 text,
                    description_img_data_3 blop,
                    description_img_path_3 text,
                    
                    test_time text,
                    var_number int,
                    res_number int,
                    question_pool_tag text,
                    question_author text
                    )""")


            # Commit Changes
            conn.commit()

            # Close Connection
            conn.close()


            print("Neue Formelfrage_Permutation Datenbank erstellt! Wird mit Vorlage_Werten befüllt..")

            CreateDatabases.insert_template_to_database_formelfrage_permutation(self)

    def insert_template_to_database_formelfrage_permutation(self):
        # Create a database or connect to one
        connect = sqlite3.connect(self.database_formelfrage_permutation_path)

        # Create cursor
        cursor = connect.cursor()

        # Insert into Table
        cursor.execute(
            "INSERT INTO formelfrage_permutation_table VALUES ("
            ":question_difficulty, :question_category, :question_type, "
            ":question_title, :question_description_title, :question_description_main, "
            ":res1_formula, :res2_formula, :res3_formula,  "
            ":res4_formula, :res5_formula, :res6_formula,  "
            ":res7_formula, :res8_formula, :res9_formula, :res10_formula,  "
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
            ":res3_name, :res3_min, :res3_max, :res3_prec, :res3_tol, :res3_points, :res3_unit, "
            ":res4_name, :res4_min, :res4_max, :res4_prec, :res4_tol, :res4_points, :res4_unit, "
            ":res5_name, :res5_min, :res5_max, :res5_prec, :res5_tol, :res5_points, :res5_unit, "
            ":res6_name, :res6_min, :res6_max, :res6_prec, :res6_tol, :res6_points, :res6_unit, "
            ":res7_name, :res7_min, :res7_max, :res7_prec, :res7_tol, :res7_points, :res7_unit, "
            ":res8_name, :res8_min, :res8_max, :res8_prec, :res8_tol, :res8_points, :res8_unit, "
            ":res9_name, :res9_min, :res9_max, :res9_prec, :res9_tol, :res9_points, :res9_unit, "
            ":res10_name, :res10_min, :res10_max, :res10_prec, :res10_tol, :res10_points, :res10_unit, "
            
            ":perm_var_symbol_1, :perm_var_value_1,"
            ":perm_var_symbol_2, :perm_var_value_2,"
            ":perm_var_symbol_3, :perm_var_value_3,"
            ":perm_var_symbol_4, :perm_var_value_4,"
            ":perm_var_symbol_5, :perm_var_value_5,"
            ":perm_var_symbol_6, :perm_var_value_6,"
            ":perm_var_symbol_7, :perm_var_value_7,"
            ":perm_var_symbol_8, :perm_var_value_8,"
            ":perm_var_symbol_9, :perm_var_value_9,"
            ":perm_var_symbol_10, :perm_var_value_10,"
            
            ":description_img_name_1, :description_img_data_1, :description_img_path_1, "
            ":description_img_name_2, :description_img_data_2, :description_img_path_2, "
            ":description_img_name_3, :description_img_data_3, :description_img_path_3, "
            ":test_time, :var_number, :res_number, :question_pool_tag, :question_author)",
            {
                'question_difficulty': "question_difficulty",
                'question_category': "question_category",
                'question_type': "question_type",

                'question_title': "question_title",
                'question_description_title': "question_description_title",
                'question_description_main': "question_description_main",

                'res1_formula': "res1_formula",
                'res2_formula': "res2_formula",
                'res3_formula': "res3_formula",
                'res4_formula': "res4_formula",
                'res5_formula': "res5_formula",
                'res6_formula': "res6_formula",
                'res7_formula': "res7_formula",
                'res8_formula': "res8_formula",
                'res9_formula': "res9_formula",
                'res10_formula': "res10_formula",

                'var1_name': "var1_name",
                'var1_min': "var1_min",
                'var1_max': "var1_max",
                'var1_prec': "var1_prec",
                'var1_divby': "var1_divby",
                'var1_unit': "var1_unit",

                'var2_name': "var2_name",
                'var2_min': "var2_min",
                'var2_max': "var2_max",
                'var2_prec': "var2_prec",
                'var2_divby': "var2_divby",
                'var2_unit': "var2_unit",

                'var3_name': "var3_name",
                'var3_min': "var3_min",
                'var3_max': "var3_max",
                'var3_prec': "var3_prec",
                'var3_divby': "var3_divby",
                'var3_unit': "var3_unit",

                'var4_name': "var4_name",
                'var4_min': "var4_min",
                'var4_max': "var4_max",
                'var4_prec': "var4_prec",
                'var4_divby': "var4_divby",
                'var4_unit': "var4_unit",

                'var5_name': "var5_name",
                'var5_min': "var5_min",
                'var5_max': "var5_max",
                'var5_prec': "var5_prec",
                'var5_divby': "var5_divby",
                'var5_unit': "var5_unit",

                'var6_name': "var6_name",
                'var6_min': "var6_min",
                'var6_max': "var6_max",
                'var6_prec': "var6_prec",
                'var6_divby': "var6_divby",
                'var6_unit': "var6_unit",

                'var7_name': "var7_name",
                'var7_min': "var7_min",
                'var7_max': "var7_max",
                'var7_prec': "var7_prec",
                'var7_divby': "var7_divby",
                'var7_unit': "var7_unit",

                'var8_name': "var8_name",
                'var8_min': "var8_min",
                'var8_max': "var8_max",
                'var8_prec': "var8_prec",
                'var8_divby': "var8_divby",
                'var8_unit': "var8_unit",

                'var9_name': "var9_name",
                'var9_min': "var9_min",
                'var9_max': "var9_max",
                'var9_prec': "var9_prec",
                'var9_divby': "var9_divby",
                'var9_unit': "var9_unit",

                'var10_name': "var10_name",
                'var10_min': "var10_min",
                'var10_max': "var10_max",
                'var10_prec': "var10_prec",
                'var10_divby': "var10_divby",
                'var10_unit': "var10_unit",

                'res1_name': "res1_name",
                'res1_min': "res1_min",
                'res1_max': "res1_max",
                'res1_prec': "res1_prec",
                'res1_tol': "res1_tol",
                'res1_points': "res1_points",
                'res1_unit': "res1_unit",

                'res2_name': "res2_name",
                'res2_min': "res2_min",
                'res2_max': "res2_max",
                'res2_prec': "res2_prec",
                'res2_tol': "res2_tol",
                'res2_points': "res2_points",
                'res2_unit': "res2_unit",

                'res3_name': "res3_name",
                'res3_min': "res3_min",
                'res3_max': "res3_max",
                'res3_prec': "res3_prec",
                'res3_tol': "res3_tol",
                'res3_points': "res3_points",
                'res3_unit': "res3_unit",

                'res4_name': "res4_name",
                'res4_min': "res4_min",
                'res4_max': "res4_max",
                'res4_prec': "res4_prec",
                'res4_tol': "res4_tol",
                'res4_points': "res4_points",
                'res4_unit': "res4_unit",

                'res5_name': "res5_name",
                'res5_min': "res5_min",
                'res5_max': "res5_max",
                'res5_prec': "res5_prec",
                'res5_tol': "res5_tol",
                'res5_points': "res5_points",
                'res5_unit': "res5_unit",

                'res6_name': "res6_name",
                'res6_min': "res6_min",
                'res6_max': "res6_max",
                'res6_prec': "res6_prec",
                'res6_tol': "res6_tol",
                'res6_points': "res6_points",
                'res6_unit': "res6_unit",

                'res7_name': "res7_name",
                'res7_min': "res7_min",
                'res7_max': "res7_max",
                'res7_prec': "res7_prec",
                'res7_tol': "res7_tol",
                'res7_points': "res7_points",
                'res7_unit': "res7_unit",

                'res8_name': "res8_name",
                'res8_min': "res8_min",
                'res8_max': "res8_max",
                'res8_prec': "res8_prec",
                'res8_tol': "res8_tol",
                'res8_points': "res8_points",
                'res8_unit': "res8_unit",

                'res9_name': "res9_name",
                'res9_min': "res9_min",
                'res9_max': "res9_max",
                'res9_prec': "res9_prec",
                'res9_tol': "res9_tol",
                'res9_points': "res9_points",
                'res9_unit': "res9_unit",

                'res10_name': "res10_name",
                'res10_min': "res10_min",
                'res10_max': "res10_max",
                'res10_prec': "res10_prec",
                'res10_tol': "res10_tol",
                'res10_points': "res10_points",
                'res10_unit': "res10_unit",


                'perm_var_symbol_1': "perm_var_symbol_1",
                'perm_var_value_1': "perm_var_value_1",

                'perm_var_symbol_2': "perm_var_symbol_2",
                'perm_var_value_2': "perm_var_value_2",

                'perm_var_symbol_3': "perm_var_symbol_3",
                'perm_var_value_3': "perm_var_value_3",

                'perm_var_symbol_4': "perm_var_symbol_4",
                'perm_var_value_4': "perm_var_value_4",

                'perm_var_symbol_5': "perm_var_symbol_5",
                'perm_var_value_5': "perm_var_value_5",

                'perm_var_symbol_6': "perm_var_symbol_6",
                'perm_var_value_6': "perm_var_value_6",

                'perm_var_symbol_7': "perm_var_symbol_7",
                'perm_var_value_7': "perm_var_value_7",

                'perm_var_symbol_8': "perm_var_symbol_8",
                'perm_var_value_8': "perm_var_value_8",

                'perm_var_symbol_9': "perm_var_symbol_9",
                'perm_var_value_9': "perm_var_value_9",

                'perm_var_symbol_10': "perm_var_symbol_10",
                'perm_var_value_10': "perm_var_value_10",

                'description_img_name_1': "description_img_name_1",
                'description_img_data_1': "description_img_data_1",
                'description_img_path_1': "description_img_path_1",

                'description_img_name_2': "description_img_name_2",
                'description_img_data_2': "description_img_data_2",
                'description_img_path_2': "description_img_path_2",

                'description_img_name_3': "description_img_name_3",
                'description_img_data_3': "description_img_data_3",
                'description_img_path_3': "description_img_path_3",

                'test_time': "test_time",
                'var_number': "var_number",
                'res_number': "res_number",
                'question_pool_tag': "question_pool_tag",
                'question_author': "question_author"
            }
        )


        # Commit Changes
        connect.commit()

        # Close Connection
        connect.close()

        print("Eintrag \"Vorlage\" zur Formelfrage_Permutation Datenbank hinzugefügt!")

####### Neue -- SINGLECHOICE --  Datenbank erstellen und befüllen #########

    def create_database_singlechoice(self):
        if self.database_singlechoice_exists != True:

            # Create a database or connect to one
            connect = sqlite3.connect(self.database_singlechoice_path)

            # Create cursor
            cursor = connect.cursor()

            # Create table
            cursor.execute("""CREATE TABLE IF NOT EXISTS singlechoice_table (
                    question_difficulty text,
                    question_category text,
                    question_type text,
                    question_title text,
                    question_description_title text,
                    question_description_main text,
                   
                    response_1_text text,
                    response_1_pts int,
                    response_1_img_label text,
                    response_1_img_string_base64_encoded text,
                    response_1_img_path text,
                    
                    response_2_text text,
                    response_2_pts int,
                    response_2_img_label text,
                    response_2_img_string_base64_encoded text,
                    response_2_img_path text,
                    
                    response_3_text text,
                    response_3_pts int,
                    response_3_img_label text,
                    response_3_img_string_base64_encoded text,
                    response_3_img_path text,
                    
                    response_4_text text,
                    response_4_pts int,
                    response_4_img_label text,
                    response_4_img_string_base64_encoded text,
                    response_4_img_path text,
                    
                    response_5_text text,
                    response_5_pts int,
                    response_5_img_label text,
                    response_5_img_string_base64_encoded text,
                    response_5_img_path text,
                    
                    response_6_text text,
                    response_6_pts int,
                    response_6_img_label text,
                    response_6_img_string_base64_encoded text,
                    response_6_img_path text,
                    
                    response_7_text text,
                    response_7_pts int,
                    response_7_img_label text,
                    response_7_img_string_base64_encoded text,
                    response_7_img_path text,
                    
                    response_8_text text,
                    response_8_pts int,
                    response_8_img_label text,
                    response_8_img_string_base64_encoded text,
                    response_8_img_path text,
                    
                    response_9_text text,
                    response_9_pts int,
                    response_9_img_label text,
                    response_9_img_string_base64_encoded text,
                    response_9_img_path text,
                    
                    response_10_text text,
                    response_10_pts int,
                    response_10_img_label text,
                    response_10_img_string_base64_encoded text,
                    response_10_img_path text,
                    
                    picture_preview_pixel int,
                    
                    description_img_name_1 text,
                    description_img_data_1 blop,
                    description_img_path_1 text,
                    
                    description_img_name_2 text,
                    description_img_data_2 blop,
                    description_img_path_2 text,
                    
                    description_img_name_3 text,
                    description_img_data_3 blop,
                    description_img_path_3 text,
                    
                    test_time text,
                    var_number int,
                    question_pool_tag text,
                    question_author text
                    )""")

            # Commit Changes
            connect.commit()

            # Close Connection
            connect.close()

            print("Neue SingleChoice Datenbank erstellt! Wird mit Vorlage_Werten befüllt..")

            CreateDatabases.insert_template_to_database_singlechoice(self)
    def insert_template_to_database_singlechoice(self):

        # Create a database or connect to one
        connect = sqlite3.connect(self.database_singlechoice_path)

        # Create cursor
        cursor = connect.cursor()

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
                'question_difficulty': "question_difficulty",
                'question_category': "question_category",
                'question_type': "question_type",

                'question_title': "question_title",
                'question_description_title': "question_description_title",
                'question_description_main': "question_description_main",

                'response_1_text': "response_1_text",
                'response_1_pts': "response_1_pts",
                'response_1_img_label': "response_1_img_label",
                'response_1_img_string_base64_encoded': "response_1_img_string_base64_encoded",
                'response_1_img_path' : "response_1_img_path",

                'response_2_text': "response_2_text",
                'response_2_pts': "response_2_pts",
                'response_2_img_label': "response_2_img_label",
                'response_2_img_string_base64_encoded': "response_2_img_string_base64_encoded",
                'response_2_img_path': "response_2_img_path",

                'response_3_text':  "response_3_text",
                'response_3_pts': "response_3_pts",
                'response_3_img_label': "response_3_img_label",
                'response_3_img_string_base64_encoded': "response_3_img_string_base64_encoded",
                'response_3_img_path': "response_3_img_path",

                'response_4_text': "response_4_text",
                'response_4_pts': "response_4_pts",
                'response_4_img_label': "response_4_img_label",
                'response_4_img_string_base64_encoded': "response_4_img_string_base64_encoded",
                'response_4_img_path': "response_4_img_path",

                'response_5_text': "response_5_text",
                'response_5_pts': "response_5_pts",
                'response_5_img_label': "response_5_img_label",
                'response_5_img_string_base64_encoded': "response_5_img_string_base64_encoded",
                'response_5_img_path': "response_5_img_path",

                'response_6_text': "response_6_text",
                'response_6_pts': "response_6_pts",
                'response_6_img_label': "response_6_img_label",
                'response_6_img_string_base64_encoded': "response_6_img_string_base64_encoded",
                'response_6_img_path': "response_6_img_path",

                'response_7_text': "response_7_text",
                'response_7_pts': "response_7_pts",
                'response_7_img_label': "response_7_img_label",
                'response_7_img_string_base64_encoded': "response_7_img_string_base64_encoded",
                'response_7_img_path': "response_7_img_path",

                'response_8_text': "response_8_text",
                'response_8_pts': "response_8_pts",
                'response_8_img_label': "response_8_img_label",
                'response_8_img_string_base64_encoded': "response_8_img_string_base64_encoded",
                'response_8_img_path': "response_8_img_path",

                'response_9_text': "response_9_text",
                'response_9_pts': "response_9_pts",
                'response_9_img_label': "response_9_img_label",
                'response_9_img_string_base64_encoded': "response_9_img_string_base64_encoded",
                'response_9_img_path': "response_9_img_path",

                'response_10_text': "response_10_text",
                'response_10_pts': "response_10_pts",
                'response_10_img_label': "response_10_img_label",
                'response_10_img_string_base64_encoded': "response_10_img_string_base64_encoded",
                'response_10_img_path': "response_10_img_path",

                'picture_preview_pixel': 'picture_preview_pixel',

                'description_img_name_1': "description_img_name_1",
                'description_img_data_1': "description_img_data_1",
                'description_img_path_1': "description_img_path_1",

                'description_img_name_2': "description_img_name_2",
                'description_img_data_2': "description_img_data_2",
                'description_img_path_2': "description_img_path_2",

                'description_img_name_3': "description_img_name_3",
                'description_img_data_3': "description_img_data_3",
                'description_img_path_3': "description_img_path_3",

                'test_time': "test_time",

                'var_number': "var_number",
                'question_pool_tag': "question_pool_tag",
                'question_author': "question_author"
            }
        )

        # Commit Changes
        connect.commit()

        # Close Connection
        connect.close()

        print("Eintrag \"Vorlage\" zur SingleChoice Datenbank hinzugefügt!")
    def insert_ilias_test_data_from_file_to_database_singlechoice(self):

        # Create a database or connect to one
        connect = sqlite3.connect(self.database_singlechoice_path)

        # Create cursor
        cursor = connect.cursor()

        # Create table
        cursor.execute(
            "INSERT INTO singlechoice_table VALUES ("
            ":question_difficulty, :question_category, :question_type, :question_title, :question_description_title, :question_description_main, "
            ":response_1_text,:response_2_text,:response_3_text,:response_4_text,:response_5_text,:response_6_text,:response_7_text,:response_8_text,:response_9_text,:response_10_text, "
            ":response_1_pts, :response_2_pts, :response_3_pts, :response_4_pts, :response_5_pts, :response_6_pts, :response_7_pts, :response_8_pts, :response_9_pts, :response_10_pts, "
            ":response_1_img_label, :response_2_img_label, :response_3_img_label, :response_4_img_label, :response_5_img_label, :response_6_img_label, :response_7_img_label, :response_8_img_label, :response_9_img_label, :response_10_img_label, "
            ":response_1_img_string_base64_encoded, :response_2_img_string_base64_encoded, :response_3_img_string_base64_encoded, :response_4_img_string_base64_encoded, :response_5_img_string_base64_encoded, "
            ":response_6_img_string_base64_encoded, :response_7_img_string_base64_encoded, :response_8_img_string_base64_encoded, :response_9_img_string_base64_encoded, :response_10_img_string_base64_encoded, "
            ":response_1_img_path, :response_2_img_path, :response_3_img_path, :response_4_img_path, :response_5_img_path, "
            ":response_6_img_path, :response_7_img_path, :response_8_img_path, :response_9_img_path, :response_10_img_path, "
            ":picture_preview_pixel, :description_img_name,:description_img_data, :description_img_path, :test_time, :var_number, :question_pool_tag, :question_author)",
            {
                #'question_difficulty': "question_difficulty",
                #'question_category': "question_category",
                'question_type': "question_type",

                'question_title': "question_title",
                'question_description_title': "question_description_title",
                'question_description_main': "question_description_main",

                'response_1_text': "response_1_text",
                'response_1_pts': "response_1_pts",
                'response_1_img_label': "response_1_img_label",
                'response_1_img_string_base64_encoded': "response_1_img_string_base64_encoded",
                'response_1_img_path': "response_1_img_path",

                'response_2_text': "response_2_text",
                'response_2_pts': "response_2_pts",
                'response_2_img_label': "response_2_img_label",
                'response_2_img_string_base64_encoded': "response_2_img_string_base64_encoded",
                'response_2_img_path': "response_2_img_path",

                'response_3_text':  "response_3_text",
                'response_3_pts': "response_3_pts",
                'response_3_img_label': "response_3_img_label",
                'response_3_img_string_base64_encoded': "response_3_img_string_base64_encoded",
                'response_3_img_path': "response_3_img_path",

                'response_4_text': "response_4_text",
                'response_4_pts': "response_4_pts",
                'response_4_img_label': "response_4_img_label",
                'response_4_img_string_base64_encoded': "response_4_img_string_base64_encoded",
                'response_4_img_path': "response_4_img_path",

                'response_5_text': "response_5_text",
                'response_5_pts': "response_5_pts",
                'response_5_img_label': "response_5_img_label",
                'response_5_img_string_base64_encoded': "response_5_img_string_base64_encoded",
                'response_5_img_path': "response_5_img_path",

                'response_6_text': "response_6_text",
                'response_6_pts': "response_6_pts",
                'response_6_img_label': "response_6_img_label",
                'response_6_img_string_base64_encoded': "response_6_img_string_base64_encoded",
                'response_6_img_path': "response_6_img_path",

                'response_7_text': "response_7_text",
                'response_7_pts': "response_7_pts",
                'response_7_img_label': "response_7_img_label",
                'response_7_img_string_base64_encoded': "response_7_img_string_base64_encoded",
                'response_7_img_path': "response_7_img_path",

                'response_8_text': "response_8_text",
                'response_8_pts': "response_8_pts",
                'response_8_img_label': "response_8_img_label",
                'response_8_img_string_base64_encoded': "response_8_img_string_base64_encoded",
                'response_8_img_path': "response_8_img_path",

                'response_9_text': "response_9_text",
                'response_9_pts': "response_9_pts",
                'response_9_img_label': "response_9_img_label",
                'response_9_img_string_base64_encoded': "response_9_img_string_base64_encoded",
                'response_9_img_path': "response_9_img_path",

                'response_10_text': "response_10_text",
                'response_10_pts': "response_10_pts",
                'response_10_img_label': "response_10_img_label",
                'response_10_img_string_base64_encoded': "response_10_img_string_base64_encoded",
                'response_10_img_path': "response_10_img_path",

                'picture_preview_pixel': 'picture_preview_pixel',

                'description_img_name': "description_img_name",
                'description_img_data': "description_img_data",
                'description_img_path': "description_img_path",

                'test_time': "test_time",

                #'var_number': "var_number",
                #'question_pool_tag': "question_pool_tag",
                'question_author': "question_author"
            }
        )

        # Commit Changes
        connect.commit()

        # Close Connection
        connect.close()

####### Neue -- MULTIPLECHOICE --  Datenbank erstellen und befüllen #########

    def create_database_multiplechoice(self):
        if self.database_multiplechoice_exists != True:
                # Create a database or connect to one
                connect = sqlite3.connect(self.database_multiplechoice_path)

                # Create cursor
                cursor = connect.cursor()

                # Create table
                cursor.execute("""CREATE TABLE IF NOT EXISTS multiplechoice_table (
                        question_difficulty text,
                        question_category text,
                        question_type text,
                        question_title text,
                        question_description_title text,
                        question_description_main text,
                        
                        response_1_text text,
                        response_1_pts_correct_answer int,
                        response_1_pts_false_answer int,
                        response_1_img_label text,
                        response_1_img_string_base64_encoded text,
                        response_1_img_path text,
                        
                        response_2_text text,
                        response_2_pts_correct_answer int,
                        response_2_pts_false_answer int,
                        response_2_img_label text,
                        response_2_img_string_base64_encoded text,
                        response_2_img_path text,
                        
                        response_3_text text,
                        response_3_pts_correct_answer int,
                        response_3_pts_false_answer int,
                        response_3_img_label text,
                        response_3_img_string_base64_encoded text,
                        response_3_img_path text,
                        
                        response_4_text text,
                        response_4_pts_correct_answer int,
                        response_4_pts_false_answer int,
                        response_4_img_label text,
                        response_4_img_string_base64_encoded text,
                        response_4_img_path text,
                        
                        response_5_text text,
                        response_5_pts_correct_answer int,
                        response_5_pts_false_answer int,
                        response_5_img_label text,
                        response_5_img_string_base64_encoded text,
                        response_5_img_path text,
                        
                        response_6_text text,
                        response_6_pts_correct_answer int,
                        response_6_pts_false_answer int,
                        response_6_img_label text,
                        response_6_img_string_base64_encoded text,
                        response_6_img_path text,
                        
                        response_7_text text,
                        response_7_pts_correct_answer int,
                        response_7_pts_false_answer int,
                        response_7_img_label text,
                        response_7_img_string_base64_encoded text,
                        response_7_img_path text,
                        
                        response_8_text text,
                        response_8_pts_correct_answer int,
                        response_8_pts_false_answer int,
                        response_8_img_label text,
                        response_8_img_string_base64_encoded text,
                        response_8_img_path text,
                        
                        response_9_text text,
                        response_9_pts_correct_answer int,
                        response_9_pts_false_answer int,
                        response_9_img_label text,
                        response_9_img_string_base64_encoded text,
                        response_9_img_path text,
                        
                        response_10_text text,
                        response_10_pts_correct_answer int,
                        response_10_pts_false_answer int,
                        response_10_img_label text,
                        response_10_img_string_base64_encoded text,
                        response_10_img_path text,
                        
                         
                        picture_preview_pixel int,
                        
                        
                        description_img_name_1 text,
                        description_img_data_1 blop,
                        description_img_path_1 text,
                        
                        description_img_name_2 text,
                        description_img_data_2 blop,
                        description_img_path_2 text,
                        
                        description_img_name_3 text,
                        description_img_data_3 blop,
                        description_img_path_3 text,
                        
                        test_time text,
                        
                        var_number int,
                        question_pool_tag text,
                        question_author text
                        )""")

                # Commit Changes
                connect.commit()

                # Close Connection
                connect.close()

                print("Neue MultipleChoice Datenbank erstellt! Wird mit Vorlage_Werten befüllt..")
                CreateDatabases.insert_template_to_database_multiplechoice(self)

    def insert_template_to_database_multiplechoice(self):

        # Create a database or connect to one
        connect = sqlite3.connect(self.database_multiplechoice_path)

        # Create cursor
        cursor = connect.cursor()

        # Create table
        cursor.execute(
            "INSERT INTO multiplechoice_table VALUES ("
            ":question_difficulty, :question_category, :question_type, :question_title, :question_description_title, :question_description_main, "
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
                'question_difficulty': "question_difficulty",
                'question_category': "question_category",
                'question_type': "question_type",

                'question_title': "question_title",
                'question_description_title': "question_description_title",

                'question_description_main': "question_description_main",
                'response_1_text': "response_1_text",
                'response_1_pts_correct_answer': "response_1_pts_correct_answer",
                'response_1_pts_false_answer': "response_1_pts_false_answer",
                'response_1_img_label': "response_1_img_label",
                'response_1_img_string_base64_encoded': "response_1_img_string_base64_encoded",
                'response_1_img_path': "response_1_img_path",

                'response_2_text': "response_2_text",
                'response_2_pts_correct_answer': "response_2_pts_correct_answer",
                'response_2_pts_false_answer': "response_2_pts_false_answer",
                'response_2_img_label': "response_2_img_label",
                'response_2_img_string_base64_encoded': "response_2_img_string_base64_encoded",
                'response_2_img_path': "response_2_img_path",

                'response_3_text':  "response_3_text",
                'response_3_pts_correct_answer': "response_3_pts_correct_answer",
                'response_3_pts_false_answer': "response_3_pts_false_answer",
                'response_3_img_label': "response_3_img_label",
                'response_3_img_string_base64_encoded': "response_3_img_string_base64_encoded",
                'response_3_img_path': "response_3_img_path",

                'response_4_text': "response_4_text",
                'response_4_pts_correct_answer': "response_4_pts_correct_answer",
                'response_4_pts_false_answer': "response_4_pts_false_answer",
                'response_4_img_label': "response_4_img_label",
                'response_4_img_string_base64_encoded': "response_4_img_string_base64_encoded",
                'response_4_img_path': "response_4_img_path",

                'response_5_text': "response_5_text",
                'response_5_pts_correct_answer': "response_5_pts_correct_answer",
                'response_5_pts_false_answer': "response_5_pts_false_answer",
                'response_5_img_label': "response_5_img_label",
                'response_5_img_string_base64_encoded': "response_5_img_string_base64_encoded",
                'response_5_img_path': "response_5_img_path",

                'response_6_text': "response_6_text",
                'response_6_pts_correct_answer': "response_6_pts_correct_answer",
                'response_6_pts_false_answer': "response_6_pts_false_answer",
                'response_6_img_label': "response_6_img_label",
                'response_6_img_string_base64_encoded': "response_6_img_string_base64_encoded",
                'response_6_img_path': "response_6_img_path",

                'response_7_text': "response_7_text",
                'response_7_pts_correct_answer': "response_7_pts_correct_answer",
                'response_7_pts_false_answer': "response_7_pts_false_answer",
                'response_7_img_label': "response_7_img_label",
                'response_7_img_string_base64_encoded': "response_7_img_string_base64_encoded",
                'response_7_img_path': "response_7_img_path",

                'response_8_text': "response_8_text",
                'response_8_pts_correct_answer': "response_8_pts_correct_answer",
                'response_8_pts_false_answer': "response_8_pts_false_answer",
                'response_8_img_label': "response_8_img_label",
                'response_8_img_string_base64_encoded': "response_8_img_string_base64_encoded",
                'response_8_img_path': "response_8_img_path",

                'response_9_text': "response_9_text",
                'response_9_pts_correct_answer': "response_9_pts_correct_answer",
                'response_9_pts_false_answer': "response_9_pts_false_answer",
                'response_9_img_label': "response_9_img_label",
                'response_9_img_string_base64_encoded': "response_9_img_string_base64_encoded",
                'response_9_img_path': "response_9_img_path",

                'response_10_text': "response_10_text",
                'response_10_pts_correct_answer': "response_10_pts_correct_answer",
                'response_10_pts_false_answer': "response_10_pts_false_answer",
                'response_10_img_label': "response_10_img_label",
                'response_10_img_string_base64_encoded': "response_10_img_string_base64_encoded",
                'response_10_img_path': "response_10_img_path",

                'picture_preview_pixel': 'picture_preview_pixel',

                'description_img_name_1': "description_img_name_1",
                'description_img_data_1': "description_img_data_1",
                'description_img_path_1': "description_img_path_1",

                'description_img_name_2': "description_img_name_2",
                'description_img_data_2': "description_img_data_2",
                'description_img_path_2': "description_img_path_2",

                'description_img_name_3': "description_img_name_3",
                'description_img_data_3': "description_img_data_3",
                'description_img_path_3': "description_img_path_3",

                'test_time': "test_time",

                'var_number': "var_number",
                'question_pool_tag': "question_pool_tag",
                'question_author': "question_author"
            }
        )

        # Commit Changes
        connect.commit()

        # Close Connection
        connect.close()

        print("Eintrag \"Vorlage\" zur MultipleChoice Datenbank hinzugefügt!")


####### Neue -- ZUORDNUNGSFRAGE --  Datenbank erstellen und befüllen #########

    def create_database_zuordnungsfrage(self):
        if self.database_zuordnungsfrage_exists != True:

            # Create a database or connect to one
            connect = sqlite3.connect(self.database_zuordnungsfrage_path)

            # Create cursor
            cursor = connect.cursor()

            # Create table
            cursor.execute("""CREATE TABLE IF NOT EXISTS zuordnungsfrage_table (
                    question_difficulty text,
                    question_category text,
                    question_type text,
                    question_title text,
                    question_description_title text,
                    question_description_main text,
                    mix_answers text,
                    asignment_mode int,
                    
                    definitions_response_1_text text,
                    definitions_response_1_img_label text,
                    definitions_response_1_img_path text,
                    definitions_response_1_img_string_base64_encoded text,
                    
                    definitions_response_2_text text,
                    definitions_response_2_img_label text,
                    definitions_response_2_img_path text,
                    definitions_response_2_img_string_base64_encoded text,
                    
                    definitions_response_3_text text,
                    definitions_response_3_img_label text,
                    definitions_response_3_img_path text,
                    definitions_response_3_img_string_base64_encoded text,
                    
                    definitions_response_4_text text,
                    definitions_response_4_img_label text,
                    definitions_response_4_img_path text,
                    definitions_response_4_img_string_base64_encoded text,
                    
                    definitions_response_5_text text,
                    definitions_response_5_img_label text,
                    definitions_response_5_img_path text,
                    definitions_response_5_img_string_base64_encoded text,
                    
                    definitions_response_6_text text,
                    definitions_response_6_img_label text,
                    definitions_response_6_img_path text,
                    definitions_response_6_img_string_base64_encoded text,
                    
                    definitions_response_7_text text,
                    definitions_response_7_img_label text,
                    definitions_response_7_img_path text,
                    definitions_response_7_img_string_base64_encoded text,
                    
                    definitions_response_8_text text,
                    definitions_response_8_img_label text,
                    definitions_response_8_img_path text,
                    definitions_response_8_img_string_base64_encoded text,
                    
                    definitions_response_9_text text,
                    definitions_response_9_img_label text,
                    definitions_response_9_img_path text,
                    definitions_response_9_img_string_base64_encoded text,
                    
                    definitions_response_10_text text,
                    definitions_response_10_img_label text,
                    definitions_response_10_img_path text,
                    definitions_response_10_img_string_base64_encoded text,
                    
                    
                    
                    terms_response_1_text text,
                    terms_response_1_img_label text,
                    terms_response_1_img_path text,
                    terms_response_1_img_string_base64_encoded text,
                    
                    terms_response_2_text text,
                    terms_response_2_img_label text,
                    terms_response_2_img_path text,
                    terms_response_2_img_string_base64_encoded text,
                    
                    terms_response_3_text text,
                    terms_response_3_img_label text,
                    terms_response_3_img_path text,
                    terms_response_3_img_string_base64_encoded text,
                    
                    terms_response_4_text text,
                    terms_response_4_img_label text,
                    terms_response_4_img_path text,
                    terms_response_4_img_string_base64_encoded text,
                    
                    terms_response_5_text text,
                    terms_response_5_img_label text,
                    terms_response_5_img_path text,
                    terms_response_5_img_string_base64_encoded text,
                    
                    terms_response_6_text text,
                    terms_response_6_img_label text,
                    terms_response_6_img_path text,
                    terms_response_6_img_string_base64_encoded text,
                    
                    terms_response_7_text text,
                    terms_response_7_img_label text,
                    terms_response_7_img_path text,
                    terms_response_7_img_string_base64_encoded text,
                    
                    terms_response_8_text text,
                    terms_response_8_img_label text,
                    terms_response_8_img_path text,
                    terms_response_8_img_string_base64_encoded text,
                    
                    terms_response_9_text text,
                    terms_response_9_img_label text,
                    terms_response_9_img_path text,
                    terms_response_9_img_string_base64_encoded text,
                    
                    terms_response_10_text text,
                    terms_response_10_img_label text,
                    terms_response_10_img_path text,
                    terms_response_10_img_string_base64_encoded text,
                    
                
                    
                    assignment_pairs_definition_1 text,
                    assignment_pairs_term_1 text,
                    assignment_pairs_1_pts int,
                    
                    assignment_pairs_definition_2 text,
                    assignment_pairs_term_2 text,
                    assignment_pairs_2_pts int,
                    
                    assignment_pairs_definition_3 text,
                    assignment_pairs_term_3 text,
                    assignment_pairs_3_pts int,
                    
                    assignment_pairs_definition_4 text,
                    assignment_pairs_term_4 text,
                    assignment_pairs_4_pts int,
                    
                    assignment_pairs_definition_5 text,
                    assignment_pairs_term_5 text,
                    assignment_pairs_5_pts int,
                    
                    assignment_pairs_definition_6 text,
                    assignment_pairs_term_6 text,
                    assignment_pairs_6_pts int,
                    
                    assignment_pairs_definition_7 text,
                    assignment_pairs_term_7 text,
                    assignment_pairs_7_pts int,
                    
                    assignment_pairs_definition_8 text,
                    assignment_pairs_term_8 text,
                    assignment_pairs_8_pts int,
                    
                    assignment_pairs_definition_9 text,
                    assignment_pairs_term_9 text,
                    assignment_pairs_9_pts int,
                    
                    assignment_pairs_definition_10 text,
                    assignment_pairs_term_10 text,
                    assignment_pairs_10_pts int,
                    
                    

               
                    picture_preview_pixel int,
                    
                    description_img_name_1 text,
                    description_img_data_1 blop,
                    description_img_path_1 text,
                    
                    description_img_name_2 text,
                    description_img_data_2 blop,
                    description_img_path_2 text,
                    
                    description_img_name_3 text,
                    description_img_data_3 blop,
                    description_img_path_3 text,
   
                    test_time text,
                    var_number int,
                    res_number int,
                    question_pool_tag text,
                    question_author text
                    )""")

            # Commit Changes
            connect.commit()

            # Close Connection
            connect.close()

            print("Neue Zuordnungsfrage Datenbank erstellt! Wird mit Vorlage_Werten befüllt..")

            CreateDatabases.insert_template_to_database_zuordnungsfrage(self)

    def insert_template_to_database_zuordnungsfrage(self):
        # Create a database or connect to one
        connect = sqlite3.connect(self.database_zuordnungsfrage_path)

        # Create cursor
        cursor = connect.cursor()

        # Insert into Table
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
                'question_difficulty': "question_difficulty",
                'question_category': "question_category",
                'question_type': "question_type",

                'question_title': "question_title",
                'question_description_title': "question_description_title",
                'question_description_main': "question_description_main",
                'mix_answers': "mix_answers",
                'assignment_mode': "assignment_mode",

                'definitions_response_1_text': "definitions_response_1_text",
                'definitions_response_2_text': "definitions_response_2_text",
                'definitions_response_3_text': "definitions_response_3_text",
                'definitions_response_4_text': "definitions_response_4_text",
                'definitions_response_5_text': "definitions_response_5_text",
                'definitions_response_6_text': "definitions_response_6_text",
                'definitions_response_7_text': "definitions_response_7_text",
                'definitions_response_8_text': "definitions_response_8_text",
                'definitions_response_9_text': "definitions_response_9_text",
                'definitions_response_10_text': "definitions_response_10_text",
                'definitions_response_1_img_label': "definitions_response_1_img_label",
                'definitions_response_2_img_label': "definitions_response_2_img_label",
                'definitions_response_3_img_label': "definitions_response_3_img_label",
                'definitions_response_4_img_label': "definitions_response_4_img_label",
                'definitions_response_5_img_label': "definitions_response_5_img_label",
                'definitions_response_6_img_label': "definitions_response_6_img_label",
                'definitions_response_7_img_label': "definitions_response_7_img_label",
                'definitions_response_8_img_label': "definitions_response_8_img_label",
                'definitions_response_9_img_label': "definitions_response_9_img_label",
                'definitions_response_10_img_label': "definitions_response_10_img_label",
                'definitions_response_1_img_path': "definitions_response_1_img_path",
                'definitions_response_2_img_path': "definitions_response_2_img_path",
                'definitions_response_3_img_path': "definitions_response_3_img_path",
                'definitions_response_4_img_path': "definitions_response_4_img_path",
                'definitions_response_5_img_path': "definitions_response_5_img_path",
                'definitions_response_6_img_path': "definitions_response_6_img_path",
                'definitions_response_7_img_path': "definitions_response_7_img_path",
                'definitions_response_8_img_path': "definitions_response_8_img_path",
                'definitions_response_9_img_path': "definitions_response_9_img_path",
                'definitions_response_10_img_path': "definitions_response_10_img_path",
                'definitions_response_1_img_string_base64_encoded': "definitions_response_1_img_string_base64_encoded",
                'definitions_response_2_img_string_base64_encoded': "definitions_response_2_img_string_base64_encoded",
                'definitions_response_3_img_string_base64_encoded': "definitions_response_3_img_string_base64_encoded",
                'definitions_response_4_img_string_base64_encoded': "definitions_response_4_img_string_base64_encoded",
                'definitions_response_5_img_string_base64_encoded': "definitions_response_5_img_string_base64_encoded",
                'definitions_response_6_img_string_base64_encoded': "definitions_response_6_img_string_base64_encoded",
                'definitions_response_7_img_string_base64_encoded': "definitions_response_7_img_string_base64_encoded",
                'definitions_response_8_img_string_base64_encoded': "definitions_response_8_img_string_base64_encoded",
                'definitions_response_9_img_string_base64_encoded': "definitions_response_9_img_string_base64_encoded",
                'definitions_response_10_img_string_base64_encoded': "definitions_response_10_img_string_base64_encoded",

                'terms_response_1_text': "terms_response_1_text" ,
                'terms_response_2_text': "terms_response_2_text",
                'terms_response_3_text': "terms_response_3_text",
                'terms_response_4_text': "terms_response_4_text",
                'terms_response_5_text': "terms_response_5_text",
                'terms_response_6_text': "terms_response_6_text",
                'terms_response_7_text': "terms_response_7_text",
                'terms_response_8_text': "terms_response_8_text",
                'terms_response_9_text': "terms_response_9_text",
                'terms_response_10_text': "terms_response_10_text",
                'terms_response_1_img_label': "terms_response_1_img_label",
                'terms_response_2_img_label': "terms_response_2_img_label",
                'terms_response_3_img_label': "terms_response_3_img_label",
                'terms_response_4_img_label': "terms_response_4_img_label",
                'terms_response_5_img_label': "terms_response_5_img_label",
                'terms_response_6_img_label': "terms_response_6_img_label",
                'terms_response_7_img_label': "terms_response_7_img_label",
                'terms_response_8_img_label': "terms_response_8_img_label",
                'terms_response_9_img_label': "terms_response_9_img_label",
                'terms_response_10_img_label': "terms_response_10_img_label",
                'terms_response_1_img_path': "terms_response_1_img_path",
                'terms_response_2_img_path': "terms_response_2_img_path",
                'terms_response_3_img_path': "terms_response_3_img_path",
                'terms_response_4_img_path': "terms_response_4_img_path",
                'terms_response_5_img_path': "terms_response_5_img_path",
                'terms_response_6_img_path': "terms_response_6_img_path",
                'terms_response_7_img_path': "terms_response_7_img_path",
                'terms_response_8_img_path': "terms_response_8_img_path",
                'terms_response_9_img_path': "terms_response_9_img_path",
                'terms_response_10_img_path': "terms_response_10_img_path",
                'terms_response_1_img_string_base64_encoded': "terms_response_1_img_string_base64_encoded" ,
                'terms_response_2_img_string_base64_encoded': "terms_response_2_img_string_base64_encoded",
                'terms_response_3_img_string_base64_encoded': "terms_response_3_img_string_base64_encoded",
                'terms_response_4_img_string_base64_encoded': "terms_response_4_img_string_base64_encoded",
                'terms_response_5_img_string_base64_encoded': "terms_response_5_img_string_base64_encoded",
                'terms_response_6_img_string_base64_encoded': "terms_response_6_img_string_base64_encoded",
                'terms_response_7_img_string_base64_encoded': "terms_response_7_img_string_base64_encoded",
                'terms_response_8_img_string_base64_encoded': "terms_response_8_img_string_base64_encoded",
                'terms_response_9_img_string_base64_encoded': "terms_response_9_img_string_base64_encoded",
                'terms_response_10_img_string_base64_encoded': "terms_response_10_img_string_base64_encoded",

                'assignment_pairs_definition_1': "assignment_pairs_definition_1",
                'assignment_pairs_definition_2': "assignment_pairs_definition_2",
                'assignment_pairs_definition_3': "assignment_pairs_definition_3",
                'assignment_pairs_definition_4': "assignment_pairs_definition_4",
                'assignment_pairs_definition_5': "assignment_pairs_definition_5",
                'assignment_pairs_definition_6': "assignment_pairs_definition_6",
                'assignment_pairs_definition_7': "assignment_pairs_definition_7",
                'assignment_pairs_definition_8': "assignment_pairs_definition_8",
                'assignment_pairs_definition_9': "assignment_pairs_definition_9",
                'assignment_pairs_definition_10': "assignment_pairs_definition_10",
                'assignment_pairs_term_1': "assignment_pairs_term_1",
                'assignment_pairs_term_2': "assignment_pairs_term_2",
                'assignment_pairs_term_3': "assignment_pairs_term_3",
                'assignment_pairs_term_4': "assignment_pairs_term_4",
                'assignment_pairs_term_5': "assignment_pairs_term_5",
                'assignment_pairs_term_6': "assignment_pairs_term_6",
                'assignment_pairs_term_7': "assignment_pairs_term_7",
                'assignment_pairs_term_8': "assignment_pairs_term_8",
                'assignment_pairs_term_9': "assignment_pairs_term_9",
                'assignment_pairs_term_10': "assignment_pairs_term_10",
                'assignment_pairs_1_pts': "assignment_pairs_1_pts" ,
                'assignment_pairs_2_pts': "assignment_pairs_2_pts" ,
                'assignment_pairs_3_pts': "assignment_pairs_3_pts" ,
                'assignment_pairs_4_pts': "assignment_pairs_4_pts" ,
                'assignment_pairs_5_pts': "assignment_pairs_5_pts" ,
                'assignment_pairs_6_pts': "assignment_pairs_6_pts" ,
                'assignment_pairs_7_pts': "assignment_pairs_7_pts" ,
                'assignment_pairs_8_pts': "assignment_pairs_8_pts" ,
                'assignment_pairs_9_pts': "assignment_pairs_9_pts" ,
                'assignment_pairs_10_pts': "assignment_pairs_10_pts" ,

                'picture_preview_pixel': "picture_preview_pixel" ,


                'description_img_name_1': "description_img_name_1",
                'description_img_data_1': "description_img_data_1",
                'description_img_path_1': "description_img_path_1",

                'description_img_name_2': "description_img_name_2",
                'description_img_data_2': "description_img_data_2",
                'description_img_path_2': "description_img_path_2",

                'description_img_name_3': "description_img_name_3",
                'description_img_data_3': "description_img_data_3",
                'description_img_path_3': "description_img_path_3",

                'test_time': "test_time",
                'var_number': "var_number",
                'res_number': "res_number",
                'question_pool_tag': "question_pool_tag",
                'question_author': "question_author"
            }
        )


        # Commit Changes
        connect.commit()

        # Close Connection
        connect.close()

        print("Eintrag \"Vorlage\" zur Zuordnungsfrage Datenbank hinzugefügt!")


####### Neue -- TEST-EINSTELLUNGEN --  Datenbank erstellen und befüllen #########

    def create_database_test_settings_profiles(self):
        if self.database_test_settings_profiles_exists != True:
            try:
                # Create a database or connect to one
                conn = sqlite3.connect(self.database_test_settings_profiles_path)

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

                print("Test-Einstellungen_Profile Datenbank erstellt!")

            except:
                print("Datenbank \"Test-Einstellungen_Profile\" bereits vorhanden!")


class Import_Export_Database(CreateDatabases):

    def __init__(self):
        print("Database Import/Export Test")


    def excel_import_to_db(self, question_type, db_entry_to_index_dict):


        def img_path_to_base64_encoded_string(response_var_label, response_var_path):

            # Wenn der Bild_Name ".jpg", ".jpeg", ".png", ".gif" enthält
            # dann öffne den Bild_Pfad (rb = read byte) und speichere als base64 encoded String
            if any(x in str(row[self.db_entry_to_index_dict[response_var_label]+1]) for x in self.ilias_image_types):

                # Wird ein Bild als base64.b64encode.. eingelesen startet der Bild_String mit "b'"
                # decode('utf-8') sorgt dafür dass diese zwei character "b'" aus dem String entfernt werden
                # ilias kann einen Image_String der mit "b'" beginnt nicht verwarbeiten
                with open(row[self.db_entry_to_index_dict[response_var_path] + 1], 'rb') as image_file:
                    base64_encoded_string = base64.b64encode(image_file.read())
                    base64_encoded_string = base64_encoded_string.decode('utf-8')

                return base64_encoded_string


        self.question_type = question_type.lower()
        self.db_entry_to_index_dict = db_entry_to_index_dict
        ################################  IMPORT SINGLECHOICE EXCEL FILE TO DB  #################################





        self.xlsx_path = filedialog.askopenfilename(initialdir=pathlib.Path().absolute(), title="Select a File")
        self.xlsx_data = pd.read_excel(self.xlsx_path)

        self.xlsx_file_column_labels = []
        self.sql_values_question_marks = "("
        self.sql_labels_param = ""

        self.ff_description_img_data = ""
        self.sc_description_img_data = ""
        self.mc_description_img_data = ""

        # Datentypen die von ILIAS unterstützt werden
        self.ilias_image_types = [".jpg", ".jpeg", ".png", ".gif"]


        # Dataframe erstellen
        self.dataframe = pd.DataFrame(self.xlsx_data)

        # Über die Excel Spalten iterieren
        for col in self.dataframe.columns:
            self.xlsx_file_column_labels.append(str(col))

        # Dataframe mit neuen Labels belegen
        self.dataframe.columns = self.xlsx_file_column_labels


        # Leere Einträge entfernen
        self.dataframe = self.dataframe.fillna("")



        for i in range(len(self.xlsx_file_column_labels)-1):
            self.sql_values_question_marks += "?,"

            if i == (len(self.xlsx_file_column_labels)-2):
                self.sql_values_question_marks += "?)"

        if self.question_type == "singlechoice" or self.question_type == "single choice":
            # Mit SingleChoice Datenbank verbinden
            conn = sqlite3.connect(self.database_singlechoice_path)
            c = conn.cursor()

            for row in self.dataframe.itertuples():

                # # "+1" ist notwendig weil "row" mit '1' anfängt und das DICT mit '0'
                # if "placeholder" in str(row[self.db_entry_to_index_dict['description_img_data']+1]):
                #     print("image found! -> " + str(row[self.db_entry_to_index_dict['description_img_path']+1]))
                #     # read image data in byte format
                #     with open(row[self.db_entry_to_index_dict['description_img_path']+1], 'rb') as image_file:
                #         self.sc_description_img_data = image_file.read()




                self.response_1_img_string_base64_encoded = img_path_to_base64_encoded_string('response_1_img_label', 'response_1_img_path')
                self.response_2_img_string_base64_encoded = img_path_to_base64_encoded_string('response_2_img_label', 'response_2_img_path')
                self.response_3_img_string_base64_encoded = img_path_to_base64_encoded_string('response_3_img_label', 'response_3_img_path')
                self.response_4_img_string_base64_encoded = img_path_to_base64_encoded_string('response_4_img_label', 'response_4_img_path')
                self.response_5_img_string_base64_encoded = img_path_to_base64_encoded_string('response_5_img_label', 'response_5_img_path')
                self.response_6_img_string_base64_encoded = img_path_to_base64_encoded_string('response_6_img_label', 'response_6_img_path')
                self.response_7_img_string_base64_encoded = img_path_to_base64_encoded_string('response_7_img_label', 'response_7_img_path')
                self.response_8_img_string_base64_encoded = img_path_to_base64_encoded_string('response_8_img_label', 'response_8_img_path')
                self.response_9_img_string_base64_encoded = img_path_to_base64_encoded_string('response_9_img_label', 'response_9_img_path')
                self.response_10_img_string_base64_encoded = img_path_to_base64_encoded_string('response_10_img_label', 'response_10_img_path')


                self.sc_description_img_data_1 = Import_Export_Database.excel_import_placeholder_to_data(self, row, self.db_entry_to_index_dict['description_img_data_1'], self.db_entry_to_index_dict['description_img_path_1'])
                self.sc_description_img_data_2 = Import_Export_Database.excel_import_placeholder_to_data(self, row, self.db_entry_to_index_dict['description_img_data_2'], self.db_entry_to_index_dict['description_img_path_2'])
                self.sc_description_img_data_3 = Import_Export_Database.excel_import_placeholder_to_data(self, row, self.db_entry_to_index_dict['description_img_data_3'], self.db_entry_to_index_dict['description_img_path_3'])


                c.execute("INSERT INTO singlechoice_table VALUES " + self.sql_values_question_marks, (
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

                       self.response_1_img_string_base64_encoded,
                       self.response_2_img_string_base64_encoded,
                       self.response_3_img_string_base64_encoded,
                       self.response_4_img_string_base64_encoded,
                       self.response_5_img_string_base64_encoded,
                       self.response_6_img_string_base64_encoded,
                       self.response_7_img_string_base64_encoded,
                       self.response_8_img_string_base64_encoded,
                       self.response_9_img_string_base64_encoded,
                       self.response_10_img_string_base64_encoded,

                       row.response_1_img_path,
                       row.response_2_img_path,
                       row.response_3_img_path,
                       row.response_4_img_path,
                       row.response_5_img_path,
                       row.response_6_img_path,
                       row.response_7_img_path,
                       row.response_8_img_path,
                       row.response_9_img_path,
                       row.response_10_img_path,

                       row.picture_preview_pixel,

                       row.description_img_name_1,
                       self.sc_description_img_data_1,
                       row.description_img_path_1,

                       row.description_img_name_2,
                       self.sc_description_img_data_2,
                       row.description_img_path_2,

                       row.description_img_name_3,
                       self.sc_description_img_data_3,
                       row.description_img_path_3,

                       row.test_time,
                       row.var_number,
                       row.question_pool_tag,
                       row.question_author
                     ))



            print("Load File: \"" + self.xlsx_path + "\"  ---> in singlechoice_table...done!")
            print("Excel-Einträge: " + str(len(row)))

            conn.commit()

        elif self.question_type == "formelfrage" or self.question_type == "formel frage":

            # Mit Formelfrage Datenbank verbinden
            conn = sqlite3.connect(self.database_formelfrage_path)
            c = conn.cursor()

            self.number_of_excel_entries = 0
            for ff_row in self.dataframe.itertuples():
                self.number_of_excel_entries +=1

                self.ff_description_img_data_1 = Import_Export_Database.excel_import_placeholder_to_data(self, ff_row, self.db_entry_to_index_dict['description_img_data_1'], self.db_entry_to_index_dict['description_img_path_1'])
                self.ff_description_img_data_2 = Import_Export_Database.excel_import_placeholder_to_data(self, ff_row, self.db_entry_to_index_dict['description_img_data_2'], self.db_entry_to_index_dict['description_img_path_2'])
                self.ff_description_img_data_3 = Import_Export_Database.excel_import_placeholder_to_data(self, ff_row, self.db_entry_to_index_dict['description_img_data_3'], self.db_entry_to_index_dict['description_img_path_3'])

                c.execute("INSERT INTO formelfrage_table VALUES " + self.sql_values_question_marks, (
                    ff_row.question_difficulty,
                    ff_row.question_category,
                    ff_row.question_type,
                    ff_row.question_title,
                    ff_row.question_description_title,
                    ff_row.question_description_main,

                    ff_row.res1_formula,
                    ff_row.res2_formula,
                    ff_row.res3_formula,
                    ff_row.res4_formula,
                    ff_row.res5_formula,
                    ff_row.res6_formula,
                    ff_row.res7_formula,
                    ff_row.res8_formula,
                    ff_row.res9_formula,
                    ff_row.res10_formula,

                    ff_row.var1_name,
                    ff_row.var1_min,
                    ff_row.var1_max,
                    ff_row.var1_prec,
                    ff_row.var1_divby,
                    ff_row.var1_unit,

                    ff_row.var2_name,
                    ff_row.var2_min,
                    ff_row.var2_max,
                    ff_row.var2_prec,
                    ff_row.var2_divby,
                    ff_row.var2_unit,

                    ff_row.var3_name,
                    ff_row.var3_min,
                    ff_row.var3_max,
                    ff_row.var3_prec,
                    ff_row.var3_divby,
                    ff_row.var3_unit,

                    ff_row.var4_name,
                    ff_row.var4_min,
                    ff_row.var4_max,
                    ff_row.var4_prec,
                    ff_row.var4_divby,
                    ff_row.var4_unit,

                    ff_row.var5_name,
                    ff_row.var5_min,
                    ff_row.var5_max,
                    ff_row.var5_prec,
                    ff_row.var5_divby,
                    ff_row.var5_unit,

                    ff_row.var6_name,
                    ff_row.var6_min,
                    ff_row.var6_max,
                    ff_row.var6_prec,
                    ff_row.var6_divby,
                    ff_row.var6_unit,

                    ff_row.var7_name,
                    ff_row.var7_min,
                    ff_row.var7_max,
                    ff_row.var7_prec,
                    ff_row.var7_divby,
                    ff_row.var7_unit,

                    ff_row.var8_name,
                    ff_row.var8_min,
                    ff_row.var8_max,
                    ff_row.var8_prec,
                    ff_row.var8_divby,
                    ff_row.var8_unit,

                    ff_row.var9_name,
                    ff_row.var9_min,
                    ff_row.var9_max,
                    ff_row.var9_prec,
                    ff_row.var9_divby,
                    ff_row.var9_unit,

                    ff_row.var10_name,
                    ff_row.var10_min,
                    ff_row.var10_max,
                    ff_row.var10_prec,
                    ff_row.var10_divby,
                    ff_row.var10_unit,

                    ff_row.var11_name,
                    ff_row.var11_min,
                    ff_row.var11_max,
                    ff_row.var11_prec,
                    ff_row.var11_divby,
                    ff_row.var11_unit,

                    ff_row.var12_name,
                    ff_row.var12_min,
                    ff_row.var12_max,
                    ff_row.var12_prec,
                    ff_row.var12_divby,
                    ff_row.var12_unit,

                    ff_row.var13_name,
                    ff_row.var13_min,
                    ff_row.var13_max,
                    ff_row.var13_prec,
                    ff_row.var13_divby,
                    ff_row.var13_unit,

                    ff_row.var14_name,
                    ff_row.var14_min,
                    ff_row.var14_max,
                    ff_row.var14_prec,
                    ff_row.var14_divby,
                    ff_row.var14_unit,

                    ff_row.var15_name,
                    ff_row.var15_min,
                    ff_row.var15_max,
                    ff_row.var15_prec,
                    ff_row.var15_divby,
                    ff_row.var15_unit,


                    ff_row.res1_name,
                    ff_row.res1_min,
                    ff_row.res1_max,
                    ff_row.res1_prec,
                    ff_row.res1_tol,
                    ff_row.res1_points,
                    ff_row.res1_unit,

                    ff_row.res2_name,
                    ff_row.res2_min,
                    ff_row.res2_max,
                    ff_row.res2_prec,
                    ff_row.res2_tol,
                    ff_row.res2_points,
                    ff_row.res2_unit,

                    ff_row.res3_name,
                    ff_row.res3_min,
                    ff_row.res3_max,
                    ff_row.res3_prec,
                    ff_row.res3_tol,
                    ff_row.res3_points,
                    ff_row.res3_unit,

                    ff_row.res4_name,
                    ff_row.res4_min,
                    ff_row.res4_max,
                    ff_row.res4_prec,
                    ff_row.res4_tol,
                    ff_row.res4_points,
                    ff_row.res4_unit,

                    ff_row.res5_name,
                    ff_row.res5_min,
                    ff_row.res5_max,
                    ff_row.res5_prec,
                    ff_row.res5_tol,
                    ff_row.res5_points,
                    ff_row.res5_unit,

                    ff_row.res6_name,
                    ff_row.res6_min,
                    ff_row.res6_max,
                    ff_row.res6_prec,
                    ff_row.res6_tol,
                    ff_row.res6_points,
                    ff_row.res6_unit,

                    ff_row.res7_name,
                    ff_row.res7_min,
                    ff_row.res7_max,
                    ff_row.res7_prec,
                    ff_row.res7_tol,
                    ff_row.res7_points,
                    ff_row.res7_unit,

                    ff_row.res8_name,
                    ff_row.res8_min,
                    ff_row.res8_max,
                    ff_row.res8_prec,
                    ff_row.res8_tol,
                    ff_row.res8_points,
                    ff_row.res8_unit,

                    ff_row.res9_name,
                    ff_row.res9_min,
                    ff_row.res9_max,
                    ff_row.res9_prec,
                    ff_row.res9_tol,
                    ff_row.res9_points,
                    ff_row.res9_unit,

                    ff_row.res10_name,
                    ff_row.res10_min,
                    ff_row.res10_max,
                    ff_row.res10_prec,
                    ff_row.res10_tol,
                    ff_row.res10_points,
                    ff_row.res10_unit,

                    ff_row.description_img_name_1,
                    self.ff_description_img_data_1,
                    ff_row.description_img_path_1,

                    ff_row.description_img_name_2,
                    self.ff_description_img_data_2,
                    ff_row.description_img_path_2,

                    ff_row.description_img_name_3,
                    self.ff_description_img_data_3,
                    ff_row.description_img_path_3,

                    ff_row.test_time,
                    ff_row.var_number,
                    ff_row.res_number,
                    ff_row.question_pool_tag,
                    ff_row.question_author
                ))


                conn.commit()


            print("Load File: \"" + self.xlsx_path + "\" in formelfrage_table...done!")
            print("Excel-Einträge: " + str(self.number_of_excel_entries))

        elif self.question_type == "multiplechoice" or self.question_type == "multiple choice":

            # Mit MultipleChoice Datenbank verbinden
            conn = sqlite3.connect(self.database_multiplechoice_path)
            c = conn.cursor()

            for row in self.dataframe.itertuples():

                # # "+1" ist notwendig weil "row" mit '1' anfängt und das DICT mit '0'
                # if "placeholder" in str(row[self.db_entry_to_index_dict['description_img_data']+1]):
                #     print("image found! -> " + str(row[self.db_entry_to_index_dict['description_img_path']+1]))
                #     # read image data in byte format
                #     with open(row[self.db_entry_to_index_dict['description_img_path']+1], 'rb') as image_file:
                #         self.sc_description_img_data = image_file.read()




                self.response_1_img_string_base64_encoded = img_path_to_base64_encoded_string('response_1_img_label', 'response_1_img_path')
                self.response_2_img_string_base64_encoded = img_path_to_base64_encoded_string('response_2_img_label', 'response_2_img_path')
                self.response_3_img_string_base64_encoded = img_path_to_base64_encoded_string('response_3_img_label', 'response_3_img_path')
                self.response_4_img_string_base64_encoded = img_path_to_base64_encoded_string('response_4_img_label', 'response_4_img_path')
                self.response_5_img_string_base64_encoded = img_path_to_base64_encoded_string('response_5_img_label', 'response_5_img_path')
                self.response_6_img_string_base64_encoded = img_path_to_base64_encoded_string('response_6_img_label', 'response_6_img_path')
                self.response_7_img_string_base64_encoded = img_path_to_base64_encoded_string('response_7_img_label', 'response_7_img_path')
                self.response_8_img_string_base64_encoded = img_path_to_base64_encoded_string('response_8_img_label', 'response_8_img_path')
                self.response_9_img_string_base64_encoded = img_path_to_base64_encoded_string('response_9_img_label', 'response_9_img_path')
                self.response_10_img_string_base64_encoded = img_path_to_base64_encoded_string('response_10_img_label', 'response_10_img_path')


                self.mc_description_img_data_1 = Import_Export_Database.excel_import_placeholder_to_data(self, row, self.db_entry_to_index_dict['description_img_data_1'], self.db_entry_to_index_dict['description_img_path_1'])
                self.mc_description_img_data_2 = Import_Export_Database.excel_import_placeholder_to_data(self, row, self.db_entry_to_index_dict['description_img_data_2'], self.db_entry_to_index_dict['description_img_path_2'])
                self.mc_description_img_data_3 = Import_Export_Database.excel_import_placeholder_to_data(self, row, self.db_entry_to_index_dict['description_img_data_3'], self.db_entry_to_index_dict['description_img_path_3'])


                c.execute("INSERT INTO multiplechoice_table VALUES " + self.sql_values_question_marks, (
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

                   row.response_1_pts_correct_answer,
                   row.response_2_pts_correct_answer,
                   row.response_3_pts_correct_answer,
                   row.response_4_pts_correct_answer,
                   row.response_5_pts_correct_answer,
                   row.response_6_pts_correct_answer,
                   row.response_7_pts_correct_answer,
                   row.response_8_pts_correct_answer,
                   row.response_9_pts_correct_answer,
                   row.response_10_pts_correct_answer,

                   row.response_1_pts_false_answer,
                   row.response_2_pts_false_answer,
                   row.response_3_pts_false_answer,
                   row.response_4_pts_false_answer,
                   row.response_5_pts_false_answer,
                   row.response_6_pts_false_answer,
                   row.response_7_pts_false_answer,
                   row.response_8_pts_false_answer,
                   row.response_9_pts_false_answer,
                   row.response_10_pts_false_answer,

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

                   self.response_1_img_string_base64_encoded,
                   self.response_2_img_string_base64_encoded,
                   self.response_3_img_string_base64_encoded,
                   self.response_4_img_string_base64_encoded,
                   self.response_5_img_string_base64_encoded,
                   self.response_6_img_string_base64_encoded,
                   self.response_7_img_string_base64_encoded,
                   self.response_8_img_string_base64_encoded,
                   self.response_9_img_string_base64_encoded,
                   self.response_10_img_string_base64_encoded,

                   row.response_1_img_path,
                   row.response_2_img_path,
                   row.response_3_img_path,
                   row.response_4_img_path,
                   row.response_5_img_path,
                   row.response_6_img_path,
                   row.response_7_img_path,
                   row.response_8_img_path,
                   row.response_9_img_path,
                   row.response_10_img_path,

                   row.picture_preview_pixel,

                   row.description_img_name_1,
                   self.mc_description_img_data_1,
                   row.description_img_path_1,

                   row.description_img_name_2,
                   self.mc_description_img_data_2,
                   row.description_img_path_2,

                   row.description_img_name_3,
                   self.mc_description_img_data_3,
                   row.description_img_path_3,

                   row.test_time,
                   row.var_number,
                   row.question_pool_tag,
                   row.question_author
                ))

                conn.commit()

                print("Load File: \"" + self.xlsx_path + "\"  ---> in multiplechoice_table...done!")
                print("Excel-Einträge: " + str(len(row)))



        elif self.question_type == "zuordnungsfrage" or self.question_type == "zuordnungs frage":

            # Mit Zuordnungsfrage Datenbank verbinden
            conn = sqlite3.connect(self.database_zuordnungsfrage_path)
            c = conn.cursor()

            for row in self.dataframe.itertuples():

                self.definitions_response_1_img_string_base64_encoded = img_path_to_base64_encoded_string('definitions_response_1_img_label', 'definitions_response_1_img_path')
                self.definitions_response_2_img_string_base64_encoded = img_path_to_base64_encoded_string('definitions_response_2_img_label', 'definitions_response_2_img_path')
                self.definitions_response_3_img_string_base64_encoded = img_path_to_base64_encoded_string('definitions_response_3_img_label', 'definitions_response_3_img_path')
                self.definitions_response_4_img_string_base64_encoded = img_path_to_base64_encoded_string('definitions_response_4_img_label', 'definitions_response_4_img_path')
                self.definitions_response_5_img_string_base64_encoded = img_path_to_base64_encoded_string('definitions_response_5_img_label', 'definitions_response_5_img_path')
                self.definitions_response_6_img_string_base64_encoded = img_path_to_base64_encoded_string('definitions_response_6_img_label', 'definitions_response_6_img_path')
                self.definitions_response_7_img_string_base64_encoded = img_path_to_base64_encoded_string('definitions_response_7_img_label', 'definitions_response_7_img_path')
                self.definitions_response_8_img_string_base64_encoded = img_path_to_base64_encoded_string('definitions_response_8_img_label', 'definitions_response_8_img_path')
                self.definitions_response_9_img_string_base64_encoded = img_path_to_base64_encoded_string('definitions_response_9_img_label', 'definitions_response_9_img_path')
                self.definitions_response_10_img_string_base64_encoded = img_path_to_base64_encoded_string('definitions_response_10_img_label', 'definitions_response_10_img_path')
                
                self.terms_response_1_img_string_base64_encoded = img_path_to_base64_encoded_string('terms_response_1_img_label', 'terms_response_1_img_path')
                self.terms_response_2_img_string_base64_encoded = img_path_to_base64_encoded_string('terms_response_2_img_label', 'terms_response_2_img_path')
                self.terms_response_3_img_string_base64_encoded = img_path_to_base64_encoded_string('terms_response_3_img_label', 'terms_response_3_img_path')
                self.terms_response_4_img_string_base64_encoded = img_path_to_base64_encoded_string('terms_response_4_img_label', 'terms_response_4_img_path')
                self.terms_response_5_img_string_base64_encoded = img_path_to_base64_encoded_string('terms_response_5_img_label', 'terms_response_5_img_path')
                self.terms_response_6_img_string_base64_encoded = img_path_to_base64_encoded_string('terms_response_6_img_label', 'terms_response_6_img_path')
                self.terms_response_7_img_string_base64_encoded = img_path_to_base64_encoded_string('terms_response_7_img_label', 'terms_response_7_img_path')
                self.terms_response_8_img_string_base64_encoded = img_path_to_base64_encoded_string('terms_response_8_img_label', 'terms_response_8_img_path')
                self.terms_response_9_img_string_base64_encoded = img_path_to_base64_encoded_string('terms_response_9_img_label', 'terms_response_9_img_path')
                self.terms_response_10_img_string_base64_encoded = img_path_to_base64_encoded_string('terms_response_10_img_label', 'terms_response_10_img_path')


                self.mq_description_img_data_1 = Import_Export_Database.excel_import_placeholder_to_data(self, row, self.db_entry_to_index_dict['description_img_data_1'], self.db_entry_to_index_dict['description_img_path_1'])
                self.mq_description_img_data_2 = Import_Export_Database.excel_import_placeholder_to_data(self, row, self.db_entry_to_index_dict['description_img_data_2'], self.db_entry_to_index_dict['description_img_path_2'])
                self.mq_description_img_data_3 = Import_Export_Database.excel_import_placeholder_to_data(self, row, self.db_entry_to_index_dict['description_img_data_3'], self.db_entry_to_index_dict['description_img_path_3'])




                c.execute("INSERT INTO multiplechoice_table VALUES " + self.sql_values_question_marks, (
                   row.question_difficulty,
                   row.question_category,
                   row.question_type,
                   row.question_title,
                   row.question_description_title,
                   row.question_description_main,

                   row.mix_answers,
                   row.assignment_mode,

                   row.definitions_response_1_text,
                   row.definitions_response_2_text,
                   row.definitions_response_3_text,
                   row.definitions_response_4_text,
                   row.definitions_response_5_text,
                   row.definitions_response_6_text,
                   row.definitions_response_7_text,
                   row.definitions_response_8_text,
                   row.definitions_response_9_text,
                   row.definitions_response_10_text,
                   row.definitions_response_1_img_label,
                   row.definitions_response_2_img_label,
                   row.definitions_response_3_img_label,
                   row.definitions_response_4_img_label,
                   row.definitions_response_5_img_label,
                   row.definitions_response_6_img_label,
                   row.definitions_response_7_img_label,
                   row.definitions_response_8_img_label,
                   row.definitions_response_9_img_label,
                   row.definitions_response_10_img_label,
                   row.definitions_response_1_img_path,
                   row.definitions_response_2_img_path,
                   row.definitions_response_3_img_path,
                   row.definitions_response_4_img_path,
                   row.definitions_response_5_img_path,
                   row.definitions_response_6_img_path,
                   row.definitions_response_7_img_path,
                   row.definitions_response_8_img_path,
                   row.definitions_response_9_img_path,
                   row.definitions_response_10_img_path,
                   self.definitions_response_1_img_string_base64_encoded,
                   self.definitions_response_2_img_string_base64_encoded,
                   self.definitions_response_3_img_string_base64_encoded,
                   self.definitions_response_4_img_string_base64_encoded,
                   self.definitions_response_5_img_string_base64_encoded,
                   self.definitions_response_6_img_string_base64_encoded,
                   self.definitions_response_7_img_string_base64_encoded,
                   self.definitions_response_8_img_string_base64_encoded,
                   self.definitions_response_9_img_string_base64_encoded,
                   self.definitions_response_10_img_string_base64_encoded,
                   
                   row.terms_response_1_text,
                   row.terms_response_2_text,
                   row.terms_response_3_text,
                   row.terms_response_4_text,
                   row.terms_response_5_text,
                   row.terms_response_6_text,
                   row.terms_response_7_text,
                   row.terms_response_8_text,
                   row.terms_response_9_text,
                   row.terms_response_10_text,
                   row.terms_response_1_img_label,
                   row.terms_response_2_img_label,
                   row.terms_response_3_img_label,
                   row.terms_response_4_img_label,
                   row.terms_response_5_img_label,
                   row.terms_response_6_img_label,
                   row.terms_response_7_img_label,
                   row.terms_response_8_img_label,
                   row.terms_response_9_img_label,
                   row.terms_response_10_img_label,
                   row.terms_response_1_img_path,
                   row.terms_response_2_img_path,
                   row.terms_response_3_img_path,
                   row.terms_response_4_img_path,
                   row.terms_response_5_img_path,
                   row.terms_response_6_img_path,
                   row.terms_response_7_img_path,
                   row.terms_response_8_img_path,
                   row.terms_response_9_img_path,
                   row.terms_response_10_img_path,
                   self.terms_response_1_img_string_base64_encoded,
                   self.terms_response_2_img_string_base64_encoded,
                   self.terms_response_3_img_string_base64_encoded,
                   self.terms_response_4_img_string_base64_encoded,
                   self.terms_response_5_img_string_base64_encoded,
                   self.terms_response_6_img_string_base64_encoded,
                   self.terms_response_7_img_string_base64_encoded,
                   self.terms_response_8_img_string_base64_encoded,
                   self.terms_response_9_img_string_base64_encoded,
                   self.terms_response_10_img_string_base64_encoded,

                   row.assignment_pairs_definition_1,
                   row.assignment_pairs_definition_2,
                   row.assignment_pairs_definition_3,
                   row.assignment_pairs_definition_4,
                   row.assignment_pairs_definition_5,
                   row.assignment_pairs_definition_6,
                   row.assignment_pairs_definition_7,
                   row.assignment_pairs_definition_8,
                   row.assignment_pairs_definition_9,
                   row.assignment_pairs_definition_10,
                   row.assignment_pairs_term_1,
                   row.assignment_pairs_term_2,
                   row.assignment_pairs_term_3,
                   row.assignment_pairs_term_4,
                   row.assignment_pairs_term_5,
                   row.assignment_pairs_term_6,
                   row.assignment_pairs_term_7,
                   row.assignment_pairs_term_8,
                   row.assignment_pairs_term_9,
                   row.assignment_pairs_term_10,
                   row.assignment_pairs_pts_1,
                   row.assignment_pairs_pts_2,
                   row.assignment_pairs_pts_3,
                   row.assignment_pairs_pts_4,
                   row.assignment_pairs_pts_5,
                   row.assignment_pairs_pts_6,
                   row.assignment_pairs_pts_7,
                   row.assignment_pairs_pts_8,
                   row.assignment_pairs_pts_9,
                   row.assignment_pairs_pts_10,

                   row.picture_preview_pixel,

                   row.description_img_name_1,
                   self.mq_description_img_data_1,
                   row.description_img_path_1,

                   row.description_img_name_2,
                   self.mq_description_img_data_2,
                   row.description_img_path_2,

                   row.description_img_name_3,
                   self.mq_description_img_data_3,
                   row.description_img_path_3,

                   row.test_time,
                   row.var_number,
                   row.res_number,
                   row.question_pool_tag,
                   row.question_author
                ))

                conn.commit()

                print("Load File: \"" + self.xlsx_path + "\"  ---> in zuordnungsfrage_table...done!")
                print("Excel-Einträge: " + str(len(row)))


        conn.close()

    def excel_import_placeholder_to_data(self, row, excel_description_img_data_index, excel_description_img_path_index):

        # ".. index + 1" ist notwendig weil "row" den index für die excel-zeilen angibt.
        # row startet allerdings mit index '1', das dictionary startet mit index '0'
        # das dictionary wird verwendet um den gewünschten Eintrag in der Excel-Zeile zu finden und den Index zurückzugeben
        # Dadurch ist es nicht relevant das die Excel-Daten in festen Positionen eingetragen werden


        self.description_img_data = ""
        if "placeholder" in str(row[excel_description_img_data_index + 1]):

            # read image data in byte format
            with open(row[excel_description_img_path_index + 1], 'rb') as image_file:
                self.description_img_data = image_file.read()

        else:
            self.description_img_data = "EMPTY"

        return self.description_img_data


    def excel_export_to_xlsx(self,  project_root_path, db_entry_to_index_dict, database_path, database_name, database_table_name, xlsx_workbook_name, xlsx_worksheet_name):
        self.xlsx_workbook_name = xlsx_workbook_name
        self.database_path = database_path
        self.database_table_name = database_table_name
        self.xlsx_worksheet_name = xlsx_worksheet_name
        self.project_root_path = project_root_path
        self.db_entry_to_index_dict = db_entry_to_index_dict


        # Datenbank-Name lautet z.B.: ilias_singlechoice_db.db
        # durch den Zusatz [:-3] werden die letzten 3 Zeichen gelöscht
        self.database_dir_name = "ilias_" + str(database_name[:-3])
        self.database_dir_name += "_images"



        print("Export Database...")
        print("TABLENAME: " + str(self.xlsx_workbook_name))

        # # Wird benutzt um das Bild aus der DB in Excel skaliert darzustellen
        # image_width = 140.0
        # image_height = 182.0
        #
        # cell_width = 10.0
        # cell_height = 10.0
        #
        # x_scale = cell_width / image_width
        # y_scale = cell_height / image_height
        ##########################################

        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()
        query = 'SELECT * FROM {} LIMIT -1 OFFSET 1'.format(self.database_table_name)
        cursor.execute(query)


        header = [row[0] for row in cursor.description]
        rows = cursor.fetchall()

        # Create an new Excel file and add a worksheet.
        #os.path.normpath(os.path.join(self.project_root_path, 'ILIAS-Fragenpool_qpl_Daten'))
        excel = xlsxwriter.Workbook(os.path.normpath(os.path.join(self.project_root_path, "Datenbank_Export", self.xlsx_workbook_name)))
        excel_sheet = excel.add_worksheet(self.xlsx_worksheet_name)

        # Create style for cells
        header_cell_format = excel.add_format({'bold': True, 'border': True, 'bg_color': 'yellow'})
        body_cell_format = excel.add_format({'border': True})

        row_index = 0
        column_index = 0

        for column_name in header:
            excel_sheet.write(row_index, column_index, column_name, header_cell_format)
            column_index += 1

        row_index += 1
        for row in rows:

            column_index = 0
            self.picture_index = 1
            self.picture_definitions_answer_index = 1
            self.picture_terms_answer_index = 1
            self.sc_picture_answer_index = 1

            for column_data in row:
                # # Prüfen ob der Inhalt vom Typ String / Integer / Float ist
                # # Wenn die Prüfung "falsch" ergibt, handelt es sich um einen Bild-Eintrag






                # prüfen ob Zeilen-Inhalt vom Typ "BLOB" ist (Bild Format in SQL)
                if isinstance(column_data,byteobj.ByteString) == False:
                    excel_sheet.write(row_index, column_index, column_data, body_cell_format)
                    #column_index += 1

                # Wenn kein Typ "BLOB", aber Länge des Strings sehr groß ist (64encoded image string)
                if isinstance(column_data,byteobj.ByteString) == False and len(str(column_data)) > 300 and str(column_data).count(' ') < 10 :

                    # Wenn Fragen-Typ ---> "ZUORDNUNGSFRAGE"
                    if row[self.db_entry_to_index_dict['question_type']].lower() == "zuordnungsfrage":

                        if self.picture_definitions_answer_index <= 10:
                            self.dict_entry_string = 'definitions_response_%s_img_label' % (str(self.picture_definitions_answer_index))
                            column_data = str(row[self.db_entry_to_index_dict[self.dict_entry_string]])  + " - img_data_string_placeholder"
                            self.picture_definitions_answer_index += 1



                        elif self.picture_terms_answer_index <= 10:
                             self.dict_entry_string = 'terms_response_%s_img_label' % (str(self.picture_terms_answer_index))
                             column_data = str(row[self.db_entry_to_index_dict[self.dict_entry_string]])  + " - img_data_string_placeholder"
                             self.picture_terms_answer_index += 1


                    # Wenn Fragen-Typ ---> "SINGLECHOICE"
                    elif row[self.db_entry_to_index_dict['question_type']].lower() == "singlechoice":
                        if self.picture_definitions_answer_index <= 10:
                            self.dict_entry_string = 'response_%s_img_label' % (str(self.sc_picture_answer_index))

                            if str(row[self.db_entry_to_index_dict[self.dict_entry_string]]) != "EMPTY":
                                column_data = str(row[self.db_entry_to_index_dict[self.dict_entry_string]])  + " - img_data_string_placeholder"
                                self.sc_picture_answer_index += 1

                    excel_sheet.write(row_index, column_index, column_data, body_cell_format)


                if isinstance(column_data, byteobj.ByteString) == True:
                    column_data = str(row[self.db_entry_to_index_dict['description_img_name_' + str(self.picture_index)]]) + " - img_data_string_placeholder"
                    image_data = row[self.db_entry_to_index_dict['description_img_data_' + str(self.picture_index)]]


                    excel_sheet.write(row_index, column_index, column_data, body_cell_format)
                    #column_index += 1

                    # Hier werden die Bilder (physisch) in die Ordner abgelegt
                    # Die zusätzliche Abfrage ist leider notwendig, da u.U. einfache Strings als 'TRUE' bei der "isinstance(column_data,byteobj.ByteString)" Abfrage eingestuft werden
                    # Diese einfachen Strings können aber natürlich nicht als Bild geschrieben werden
                    if row[self.db_entry_to_index_dict['description_img_data_' + str(self.picture_index)]] != "EMPTY":
                        with open(os.path.normpath(os.path.join(self.project_root_path, "Datenbank_Export", "image_files", self.database_dir_name,  str(row[self.db_entry_to_index_dict['description_img_name_' + str(self.picture_index)]]) + '.png')), 'wb') as image_file:
                            image_file.write(image_data)

                        self.picture_index += 1
                column_index += 1
            row_index += 1

            # Variablen zurücksetzen, für nächste Frage/Zeile
            self.picture_index = 1
            self.picture_definitions_answer_index = 1
            self.picture_terms_answer_index = 1
            self.sc_picture_answer_index = 1
        # Closing workbook
        excel.close()

        print(str(row_index) + ' rows written successfully to ' + excel.filename)


class Delete_Entry_from_Database:
    def __init__(self, modul_delete_box_id, question_type, modul_var_delete_all, project_root_path, db_entry_to_index_dict, database_path, database_name, database_table_name, xlsx_workbook_name, xlsx_worksheet_name):

        self.question_type = question_type.lower()
        self.modul_var_delete_all = modul_var_delete_all
        self.modul_delete_box_id = modul_delete_box_id

        # Datanebase Name und Table_name
        self.database_db_path = database_path
        self.database_db_name = database_name
        self.database_db_table_name = database_table_name




        self.modul_delete_mult = modul_delete_box_id
        self.modul_delete_mult_start = self.modul_delete_mult.split('-')[0]

        self.modul_delete_box_split = self.modul_delete_box_id.split(",")
        self.modul_delete_index_wrong = False

        for i in range(len(self.modul_delete_box_split)):
             if "1" in self.modul_delete_box_split[i] and len(self.modul_delete_box_split[i])==1:
                 print("delete TRUE")
                 self.modul_delete_index_wrong = True

        if self.modul_delete_box_id == "1":
            print("ID \"1\" kann nicht gelöscht werden! Eintrag ist Datenbank-Vorlage!")

        elif self.modul_delete_index_wrong == True:
            print("ID \"1\" kann nicht gelöscht werden! Eintrag ist Datenbank-Vorlage!")

        elif self.modul_delete_mult_start == "1":
            print("ID \"1\" kann nicht gelöscht werden! Eintrag ist Datenbank-Vorlage!")

        else:

            # Variablen
            self.modul_delete_list = []
            self.modul_delete_all_list = []
            self.modul_delete_index = 0



            # Zur Datenbank connecten
            conn = sqlite3.connect(self.database_db_path)
            c = conn.cursor()

            # Wenn in das Eingabefeld Kommagetrenne ID's eingetragen wurden, dann ->
            # den String nehmen, nach Komma trennen "," und einzelne DB-ID's löschen
            self.modul_delete_list = self.modul_delete_box_id.split(",")


            # Wenn in das Eingabefeld z.B. "1-5" eingetragen wurde, dann ->
            # den String nehmen, und nach Bindestrick "-" splitten
            # ID in Fach 1 = Start, ID in Fach [-1] (letztes Fach)

            self.modul_delete_mult = self.modul_delete_box_id
            self.modul_delete_mult_start = self.modul_delete_mult.split('-')[0]
            self.modul_delete_mult_end = self.modul_delete_mult.split('-')[-1]
            self.modul_delete_mult_symbol = "-" in self.modul_delete_mult


            if self.modul_var_delete_all == 1:
                now = datetime.now()  # current date and time
                date_time = now.strftime("%d.%m.%Y_%Hh-%Mm")
                actual_time = str(date_time)
                self.backup_table_name = "BACKUP_Export_from_SQL__" + str(actual_time)

                Import_Export_Database.excel_export_to_xlsx(self,  project_root_path, db_entry_to_index_dict, database_path, database_name, database_table_name, self.backup_table_name + " - " + xlsx_workbook_name, xlsx_worksheet_name)

                c.execute("SELECT *, oid FROM " + str(self.database_db_table_name))
                records = c.fetchall()
                for record in records:
                    self.modul_delete_all_list.append(int(record[len(record) - 1]))

                # Der Eintrag mit ID "1" dient als Vorlage für die Datenbank
                for i in range(len(self.modul_delete_all_list)):
                    if self.modul_delete_all_list[i] == 1:
                        self.modul_delete_index = i

                self.modul_delete_all_list.pop(self.modul_delete_index)


                for x in range(len(self.modul_delete_all_list)):
                    c.execute("DELETE from %s WHERE oid = %s " % (self.database_db_table_name, str(self.modul_delete_all_list[x])))
                print(self.question_type.upper() + ": All Entries removed!")


            elif self.modul_delete_mult_symbol == True:

                for x in range(int(self.modul_delete_mult_start), int(self.modul_delete_mult_end)+1):
                    c.execute("DELETE from %s WHERE oid = %s " % (self.database_db_table_name, str(x)))
                    print(self.question_type.upper() + ": Entry with ID " + str(x) + " removed!")



            else:
                for x in range(len(self.modul_delete_list)):
                    c.execute("DELETE from %s WHERE oid = %s " % (self.database_db_table_name, str(self.modul_delete_list[x])))
                    print(self.question_type.upper() + ": Entry with ID " + str(self.modul_delete_list[x]) + " removed!")



            conn.commit()
            conn.close()