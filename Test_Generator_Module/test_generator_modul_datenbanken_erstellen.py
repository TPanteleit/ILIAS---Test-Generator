"""
********************************************
test_generator_moduL_datenbanken_erstellen.py
@digitalfellowship - Stand 07/2021
Autor: Tobias Panteleit
********************************************

Dieses Modul dient der Erstellung von Datenbanken,
Import von Excel-Fragen, Import von bestehenden ILIAS-Test/Pools,
Export von Datenbanken nach Excel
"""


import sqlite3
import os
import xlsxwriter                       # import/export von excel Dateien
import pandas as pd
from pandas import ExcelWriter
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import pathlib
import collections.abc as byteobj
import base64
from collections import Counter
from tkscrolledframe import ScrolledFrame



class CreateDatabases:

    def __init__(self, project_root_path):

        # -----Example Python Program to add new columns to an existing SQLite Table-----

        # self.database_formelfrage_path = os.path.normpath(
        #     os.path.join(self.project_root_path, "Test_Generator_Datenbanken", "ilias_formelfrage_db.db"))
        #
        # # Make a connection to the SQLite DB
        #
        # dbCon = sqlite3.connect(self.database_formelfrage_path)

        # def add_column_to_db(new_entry, new_entry_type):
        #
        #     # Obtain a Cursor object to execute SQL statements
        #     existing_db_entry = ""
        #
        #     cur = dbCon.cursor()
        #
        #     cur.execute('PRAGMA table_info(formelfrage_table)')
        #     data = cur.fetchall()
        #
        #     for d in data:
        #         existing_db_entry += str(d[1])
        #
        #     if new_entry not in existing_db_entry:
        #         cur.execute("ALTER TABLE formelfrage_table ADD COLUMN %s %s " % (new_entry, new_entry_type))
        #
        #     print("SQL done")

        # add_column_to_db("Address_new0", "INTEGER")
        # add_column_to_db("Address_new1", "INTEGER")
        # add_column_to_db("Address_new3", "INTEGER")
        # add_column_to_db("Address_new2", "INTEGER")
        # add_column_to_db("Address_new4", "INTEGER")
        # add_column_to_db("Address_new5", "INTEGER")
        # add_column_to_db("Address_new7", "INTEGER")
        # add_column_to_db("Address_new6", "INTEGER")
        # add_column_to_db("Address_new8", "INTEGER")



        # close the database connection

        #dbCon.close()


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

        # print("##    Datenbank -> Formelfrage:                        " + str(self.database_formelfrage_exists))
        # print("##    Datenbank -> SingleChoice:                       " + str(self.database_singlechoice_exists))
        # print("##    Datenbank -> MultipleChoice:                     " + str(self.database_multiplechoice_exists))
        # print("##    Datenbank -> Zuordnungsfrage:                    " + str(self.database_zuordnungsfrage_exists))
        # print("##    Datenbank -> Formelfrage_Permutation:            " + str(self.database_formelfrage_permutation_exists))
        # print("##    Datenbank -> Test-Einstellungen_Profile:         " + str(self.database_test_settings_profiles_exists))
        # print("\n")

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


            print("Neue Formelfrage Datenbank erstellt")



####### Neue -- FORMELFRAGE PERMUTATION --  Datenbank erstellen und befüllen #########

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


            print("Neue Formelfrage_Permutation Datenbank erstellt!")





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
                    question_author text,
                    mix_answers text
                    )""")

            # Commit Changes
            connect.commit()

            # Close Connection
            connect.close()

            print("Neue SingleChoice Datenbank erstellt!")




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

                print("Neue MultipleChoice Datenbank erstellt!")




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

            print("Neue Zuordnungsfrage Datenbank erstellt!")



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

    def show_dublicates_from_excel_import(self, excel_dublicates_list):
        ### Neues Fenster "Taxonomie" erzeugen

        # New Window must be "Toplevel" not "Tk()" in order to get Radiobuttons to work properly
        self.excel_dublicates_window = Toplevel()
        self.excel_dublicates_window.title("Doppelte Einträge beim Import")

        ### Frame
        # Create a ScrolledFrame widget
        self.sf_dublicates = ScrolledFrame(self.excel_dublicates_window, width=300, height=300)
        self.sf_dublicates.pack(expand=1, fill="both")

        # Create a frame within the ScrolledFrame
        self.dublicates = self.sf_dublicates.display_widget(Frame)

        for i in range(len(excel_dublicates_list)):
            label = Label(self.dublicates, text= str(i) + ") Frage: " + str(excel_dublicates_list[i]), fg="red")
            label.grid(row=i,column=0)




    def excel_import_to_db(self, question_type, db_entry_to_index_dict, question_type_GUI_tab):

        def img_path_to_base64_encoded_string(response_var_label, response_var_path, row):

            # Wenn der Bild_Name ".jpg", ".jpeg", ".png", ".gif" enthält
            # dann öffne den Bild_Pfad (rb = read byte) und speichere als base64 encoded String
            if any(x in str(row[self.db_entry_to_index_dict[response_var_label]+1]) for x in self.ilias_image_types):

                # Wird ein Bild als base64.b64encode.. eingelesen startet der Bild_String mit "b'"
                # decode('utf-8') sorgt dafür dass diese zwei character "b'" aus dem String entfernt werden
                # ilias kann einen Image_String der mit "b'" beginnt nicht verarbeiten
                with open(row[self.db_entry_to_index_dict[response_var_path] + 1], 'rb') as image_file:
                    base64_encoded_string = base64.b64encode(image_file.read())
                    base64_encoded_string = base64_encoded_string.decode('utf-8')

            else:
                base64_encoded_string = ""

            return base64_encoded_string


        self.question_type = question_type.lower()
        self.db_entry_to_index_dict = db_entry_to_index_dict

        ################################  IMPORT EXCEL FILE TO DB  #################################

        self.xlsx_path = filedialog.askopenfilename(initialdir=pathlib.Path().absolute(), title="Select a File")

        # Wenn in dem Pfad zur Datei ".ods" enthalten ist, wird eine entsprechende "engine" zum
        # richtigen einlesen der Tabelle verwendet (für OpenOffice und LibreOffice)


        if ".ods" in self.xlsx_path:
            print(self.xlsx_path)
            self.xlsx_path = self.xlsx_path.replace('/', "\\")
            print(self.xlsx_path)
            self.xlsx_data = pd.read_excel(self.xlsx_path, engine="odf")
            #print(self.xlsx_data)
        # Enthält der Pfad kein ".ods" wird davon ausgegangen, dass es sich um eine Excel-Datei handelt
        else:
            self.xlsx_data = pd.read_excel(self.xlsx_path)

        self.xlsx_file_column_labels = []
        self.sql_values_question_marks = "("
        self.sql_labels_param = ""

        self.ff_description_img_data = ""
        self.sc_description_img_data = ""
        self.mc_description_img_data = ""

        # Auflistung der Fragentitel in Datenbank
        self.db_entries_list = []
        self.edited_questions_list = []
        entry_string = ""
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

        self.excel_titles = []
        self.temp_list = []
        self.whole_excel_titles = []

        for i in range(len(self.dataframe)):
            self.temp_list = self.dataframe.iloc[i]['question_title'].split(' ')
            self.excel_titles.append(self.temp_list[0])
            self.whole_excel_titles.append(self.dataframe.iloc[i]['question_title'])



        self.id_dublicates_counter = Counter(self.excel_titles)
        self.id_dublicates_results = [k for k, v in self.id_dublicates_counter.items() if v > 1]

        self.titels_dublicates_counter = Counter(self.whole_excel_titles)
        self.titles_dublicates_results = [k for k, v in self.titels_dublicates_counter.items() if v > 1]


        if len(self.id_dublicates_results) >= 1:

            self.question_type_GUI_tab = question_type_GUI_tab

            self.dublicates_frame = LabelFrame(self.question_type_GUI_tab, text="Doppelte Einträge", padx=5, pady=5)

            self.warning_lable = Label(self.dublicates_frame, text="ACHTUNG!\nDoppelte Einträge beim Import!", fg="red", font= ('Helvetica 10 underline bold'))

            self.warning_lable2 = Label(self.dublicates_frame, text="WARNUNG! - identische Fragen-ID beim Import gefunden", fg="red")

            # "id_dublicates" bezieht sich auf die "ID" der Frage bis zum ersten Leerzeichen
            # z.B.: 07.1.01 Parallelgeschalteter Widerstand in MOhm  --> ID = 07.1.01
            self.show_id_dublicates_btn = Button(self.dublicates_frame, text="(" + str(len(self.id_dublicates_results)) + ") " + "Doppelte ID-Einträge anzeigen", command=lambda: Import_Export_Database.show_dublicates_from_excel_import(self, self.id_dublicates_results))

            # "title_dublicates" bezieht sich auf den gesamten Titel
            self.show_title_dublicates_btn = Button(self.dublicates_frame, text="(" + str(len(self.titles_dublicates_results)) + ") " + "Doppelte Titel-Einträge anzeigen", command=lambda: Import_Export_Database.show_dublicates_from_excel_import(self, self.titles_dublicates_results))



            self.dublicates_frame.grid(row=2, column=1,  pady=175, padx=10, sticky=NW)
            self.warning_lable.grid(row=0, column=0, sticky=NE)
            #self.warning_lable2.grid(row=2, column = 1)
            self.show_id_dublicates_btn.grid(row=1, column=0,  ipadx=10, pady=10, sticky=NE)
            self.show_title_dublicates_btn.grid(row=2, column=0, ipadx=10,pady=5, sticky=NE)






        for i in range(len(self.xlsx_file_column_labels)-1):
            self.sql_values_question_marks += "?,"

            if i == (len(self.xlsx_file_column_labels)-2):
                self.sql_values_question_marks += "?)"




        if self.question_type == "singlechoice" or self.question_type == "single choice":
            print("-------------- SC - Frage -----------------------")
            print("Öffne Datei:  \"" + self.xlsx_path + "\"...", end="", flush=True)
            # Mit SingleChoice Datenbank verbinden
            conn = sqlite3.connect(self.database_singlechoice_path)
            c = conn.cursor()

            self.number_of_new_entries_from_excel = 0
            self.number_of_entries_edited = 0
            self.titles_in_excel_list = []
            #####
            query = 'SELECT * FROM singlechoice_table '
            c.execute(query)

            database_rows = c.fetchall()
            
            # Alle Fragen-Titel der Datenbank-Einträge in einer String zusammen fassen
            for database_row in database_rows:
                entry_string += database_row[db_entry_to_index_dict['question_title']]


            
            for sc_row in self.dataframe.itertuples():

                # Wenn exakter Fragentitel im String gefunden wird und der Titel somit bereits in DB vorhanden ist, dann editieren und keine neue Frage hinzufügen
                if sc_row[db_entry_to_index_dict['question_title']+1] in entry_string:
                    c.execute(
                        """UPDATE singlechoice_table SET
                                question_difficulty = :question_difficulty,
                                question_category = :question_category,
                                question_type = :question_type,
            
                                question_title = :question_title,
                                question_description_title = :question_description_title,
                                question_description_main = :question_description_main,
                    
                                response_1_text= :response_1_text,
                                response_1_pts= :response_1_pts,
                                response_1_img_label= :response_1_img_label,
                                response_1_img_string_base64_encoded= :response_1_img_string_base64_encoded,
                                response_1_img_path = :response_1_img_path,
                
                                response_2_text= :response_2_text,
                                response_2_pts= :response_2_pts,
                                response_2_img_label= :response_2_img_label,
                                response_2_img_string_base64_encoded= :response_2_img_string_base64_encoded,
                                response_2_img_path= :response_2_img_path,
                
                                response_3_text= :response_3_text,
                                response_3_pts= :response_3_pts,
                                response_3_img_label= :response_3_img_label,
                                response_3_img_string_base64_encoded= :response_3_img_string_base64_encoded,
                                response_3_img_path= :response_3_img_path,
                
                                response_4_text= :response_4_text,
                                response_4_pts= :response_4_pts,
                                response_4_img_label= :response_4_img_label,
                                response_4_img_string_base64_encoded= :response_4_img_string_base64_encoded,
                                response_4_img_path= :response_4_img_path,
                
                                response_5_text= :response_5_text,
                                response_5_pts= :response_5_pts,
                                response_5_img_label= :response_5_img_label,
                                response_5_img_string_base64_encoded= :response_5_img_string_base64_encoded,
                                response_5_img_path= :response_5_img_path,
                
                                response_6_text= :response_6_text,
                                response_6_pts= :response_6_pts,
                                response_6_img_label= :response_6_img_label,
                                response_6_img_string_base64_encoded= :response_6_img_string_base64_encoded,
                                response_6_img_path= :response_6_img_path,
                
                                response_7_text= :response_7_text,
                                response_7_pts= :response_7_pts,
                                response_7_img_label= :response_7_img_label,
                                response_7_img_string_base64_encoded= :response_7_img_string_base64_encoded,
                                response_7_img_path= :response_7_img_path,
                
                                response_8_text= :response_8_text,
                                response_8_pts= :response_8_pts,
                                response_8_img_label= :response_8_img_label,
                                response_8_img_string_base64_encoded= :response_8_img_string_base64_encoded,
                                response_8_img_path= :response_8_img_path,
                
                                response_9_text= :response_9_text,
                                response_9_pts= :response_9_pts,
                                response_9_img_label= :response_9_img_label,
                                response_9_img_string_base64_encoded= :response_9_img_string_base64_encoded,
                                response_9_img_path= :response_9_img_path,
                
                                response_10_text= :response_10_text,
                                response_10_pts= :response_10_pts,
                                response_10_img_label= :response_10_img_label,
                                response_10_img_string_base64_encoded= :response_10_img_string_base64_encoded,
                                response_10_img_path= :response_10_img_path,
                                
                                
                                
                                picture_preview_pixel= :picture_preview_pixel,
                
                                description_img_name_1= :description_img_name_1,
                                description_img_data_1= :description_img_data_1,
                                description_img_path_1= :description_img_path_1,
                
                                description_img_name_2= :description_img_name_2,
                                description_img_data_2= :description_img_data_2,
                                description_img_path_2= :description_img_path_2,
                
                                description_img_name_3= :description_img_name_3,
                                description_img_data_3= :description_img_data_3,
                                description_img_path_3= :description_img_path_3,
                
                                test_time= :test_time,

                                question_pool_tag= :question_pool_tag,
                                question_author= :question_author,
                                mix_answers= :mix_answers
                                
                                WHERE question_title = :question_title""",
                                {'question_difficulty': sc_row[db_entry_to_index_dict['question_difficulty'] + 1],
                                 'question_category': sc_row[db_entry_to_index_dict['question_category'] + 1],
                                 'question_type': sc_row[db_entry_to_index_dict['question_type'] + 1],
                
                                 'question_title': sc_row[db_entry_to_index_dict['question_title'] + 1],
                                 'question_description_title': sc_row[db_entry_to_index_dict['question_description_title'] + 1],
                                 'question_description_main': sc_row[db_entry_to_index_dict['question_description_main'] + 1],
                
                                 'response_1_text': sc_row[db_entry_to_index_dict['response_1_text'] + 1],
                                 'response_1_pts': sc_row[db_entry_to_index_dict['response_1_pts'] + 1],
                                 'response_1_img_label': sc_row[db_entry_to_index_dict['response_1_img_label'] + 1],
                                 'response_1_img_string_base64_encoded': sc_row[db_entry_to_index_dict['response_1_img_string_base64_encoded'] + 1],
                                 'response_1_img_path': sc_row[db_entry_to_index_dict['response_1_img_path'] + 1],
                                 
                                 'response_2_text': sc_row[db_entry_to_index_dict['response_2_text'] + 1],
                                 'response_2_pts': sc_row[db_entry_to_index_dict['response_2_pts'] + 1],
                                 'response_2_img_label': sc_row[db_entry_to_index_dict['response_2_img_label'] + 1],
                                 'response_2_img_string_base64_encoded': sc_row[db_entry_to_index_dict['response_2_img_string_base64_encoded'] + 1],
                                 'response_2_img_path': sc_row[db_entry_to_index_dict['response_2_img_path'] + 1],
                                 
                                 'response_3_text': sc_row[db_entry_to_index_dict['response_3_text'] + 1],
                                 'response_3_pts': sc_row[db_entry_to_index_dict['response_3_pts'] + 1],
                                 'response_3_img_label': sc_row[db_entry_to_index_dict['response_3_img_label'] + 1],
                                 'response_3_img_string_base64_encoded': sc_row[db_entry_to_index_dict['response_3_img_string_base64_encoded'] + 1],
                                 'response_3_img_path': sc_row[db_entry_to_index_dict['response_3_img_path'] + 1],
                                 
                                 'response_4_text': sc_row[db_entry_to_index_dict['response_4_text'] + 1],
                                 'response_4_pts': sc_row[db_entry_to_index_dict['response_4_pts'] + 1],
                                 'response_4_img_label': sc_row[db_entry_to_index_dict['response_4_img_label'] + 1],
                                 'response_4_img_string_base64_encoded': sc_row[db_entry_to_index_dict['response_4_img_string_base64_encoded'] + 1],
                                 'response_4_img_path': sc_row[db_entry_to_index_dict['response_4_img_path'] + 1],
                                 
                                 'response_5_text': sc_row[db_entry_to_index_dict['response_5_text'] + 1],
                                 'response_5_pts': sc_row[db_entry_to_index_dict['response_5_pts'] + 1],
                                 'response_5_img_label': sc_row[db_entry_to_index_dict['response_5_img_label'] + 1],
                                 'response_5_img_string_base64_encoded': sc_row[db_entry_to_index_dict['response_5_img_string_base64_encoded'] + 1],
                                 'response_5_img_path': sc_row[db_entry_to_index_dict['response_5_img_path'] + 1],
                                 
                                 'response_6_text': sc_row[db_entry_to_index_dict['response_6_text'] + 1],
                                 'response_6_pts': sc_row[db_entry_to_index_dict['response_6_pts'] + 1],
                                 'response_6_img_label': sc_row[db_entry_to_index_dict['response_6_img_label'] + 1],
                                 'response_6_img_string_base64_encoded': sc_row[db_entry_to_index_dict['response_6_img_string_base64_encoded'] + 1],
                                 'response_6_img_path': sc_row[db_entry_to_index_dict['response_6_img_path'] + 1],
                                 
                                 'response_7_text': sc_row[db_entry_to_index_dict['response_7_text'] + 1],
                                 'response_7_pts': sc_row[db_entry_to_index_dict['response_7_pts'] + 1],
                                 'response_7_img_label': sc_row[db_entry_to_index_dict['response_7_img_label'] + 1],
                                 'response_7_img_string_base64_encoded': sc_row[db_entry_to_index_dict['response_7_img_string_base64_encoded'] + 1],
                                 'response_7_img_path': sc_row[db_entry_to_index_dict['response_7_img_path'] + 1],
                                 
                                 'response_8_text': sc_row[db_entry_to_index_dict['response_8_text'] + 1],
                                 'response_8_pts': sc_row[db_entry_to_index_dict['response_8_pts'] + 1],
                                 'response_8_img_label': sc_row[db_entry_to_index_dict['response_8_img_label'] + 1],
                                 'response_8_img_string_base64_encoded': sc_row[db_entry_to_index_dict['response_8_img_string_base64_encoded'] + 1],
                                 'response_8_img_path': sc_row[db_entry_to_index_dict['response_8_img_path'] + 1],
                                 
                                 'response_9_text': sc_row[db_entry_to_index_dict['response_9_text'] + 1],
                                 'response_9_pts': sc_row[db_entry_to_index_dict['response_9_pts'] + 1],
                                 'response_9_img_label': sc_row[db_entry_to_index_dict['response_9_img_label'] + 1],
                                 'response_9_img_string_base64_encoded': sc_row[db_entry_to_index_dict['response_9_img_string_base64_encoded'] + 1],
                                 'response_9_img_path': sc_row[db_entry_to_index_dict['response_9_img_path'] + 1],
                                 
                                 'response_10_text': sc_row[db_entry_to_index_dict['response_10_text'] + 1],
                                 'response_10_pts': sc_row[db_entry_to_index_dict['response_10_pts'] + 1],
                                 'response_10_img_label': sc_row[db_entry_to_index_dict['response_10_img_label'] + 1],
                                 'response_10_img_string_base64_encoded': sc_row[db_entry_to_index_dict['response_10_img_string_base64_encoded'] + 1],
                                 'response_10_img_path': sc_row[db_entry_to_index_dict['response_10_img_path'] + 1],
                


                                 'picture_preview_pixel': sc_row[db_entry_to_index_dict['picture_preview_pixel'] + 1],
                
                                 
                                 
                                 'description_img_name_1': sc_row[db_entry_to_index_dict['description_img_name_1'] + 1],
                                 'description_img_data_1': sc_row[db_entry_to_index_dict['description_img_data_1'] + 1],
                                 'description_img_path_1': sc_row[db_entry_to_index_dict['description_img_path_1'] + 1],

                                 'description_img_name_2': sc_row[db_entry_to_index_dict['description_img_name_2'] + 1],
                                 'description_img_data_2': sc_row[db_entry_to_index_dict['description_img_data_2'] + 1],
                                 'description_img_path_2': sc_row[db_entry_to_index_dict['description_img_path_2'] + 1],

                                 'description_img_name_3': sc_row[db_entry_to_index_dict['description_img_name_3'] + 1],
                                 'description_img_data_3': sc_row[db_entry_to_index_dict['description_img_data_3'] + 1],
                                 'description_img_path_3': sc_row[db_entry_to_index_dict['description_img_path_3'] + 1],
                
                                 'test_time': sc_row[db_entry_to_index_dict['test_time'] + 1],
                                 'question_pool_tag': sc_row[db_entry_to_index_dict['question_pool_tag'] + 1],
                                 'question_author': sc_row[db_entry_to_index_dict['question_author'] + 1],
                                 'mix_answers': sc_row[db_entry_to_index_dict['mix_answers'] + 1],
                                 'oid': sc_row[-1]
                                 })
                    
                    conn.commit()
                    
                    self.edited_questions_list.append(sc_row[db_entry_to_index_dict['question_title'] + 1])
                    self.number_of_entries_edited += 1

                # Wenn Fragentitel nicht vorhanden ist, dann neu in DB importieren
                else:
                    self.number_of_new_entries_from_excel += 1
                    
                   
                    self.response_1_img_string_base64_encoded = img_path_to_base64_encoded_string('response_1_img_label', 'response_1_img_path', sc_row)
                    self.response_2_img_string_base64_encoded = img_path_to_base64_encoded_string('response_2_img_label', 'response_2_img_path', sc_row)
                    self.response_3_img_string_base64_encoded = img_path_to_base64_encoded_string('response_3_img_label', 'response_3_img_path', sc_row)
                    self.response_4_img_string_base64_encoded = img_path_to_base64_encoded_string('response_4_img_label', 'response_4_img_path', sc_row)
                    self.response_5_img_string_base64_encoded = img_path_to_base64_encoded_string('response_5_img_label', 'response_5_img_path', sc_row)
                    self.response_6_img_string_base64_encoded = img_path_to_base64_encoded_string('response_6_img_label', 'response_6_img_path', sc_row)
                    self.response_7_img_string_base64_encoded = img_path_to_base64_encoded_string('response_7_img_label', 'response_7_img_path', sc_row)
                    self.response_8_img_string_base64_encoded = img_path_to_base64_encoded_string('response_8_img_label', 'response_8_img_path', sc_row)
                    self.response_9_img_string_base64_encoded = img_path_to_base64_encoded_string('response_9_img_label', 'response_9_img_path', sc_row)
                    self.response_10_img_string_base64_encoded = img_path_to_base64_encoded_string('response_10_img_label', 'response_10_img_path', sc_row)
    
    
                    self.sc_description_img_data_1 = Import_Export_Database.excel_import_placeholder_to_data(self, sc_row, self.db_entry_to_index_dict['description_img_data_1'], self.db_entry_to_index_dict['description_img_path_1'])
                    self.sc_description_img_data_2 = Import_Export_Database.excel_import_placeholder_to_data(self, sc_row, self.db_entry_to_index_dict['description_img_data_2'], self.db_entry_to_index_dict['description_img_path_2'])
                    self.sc_description_img_data_3 = Import_Export_Database.excel_import_placeholder_to_data(self, sc_row, self.db_entry_to_index_dict['description_img_data_3'], self.db_entry_to_index_dict['description_img_path_3'])
    

                    c.execute("INSERT INTO singlechoice_table VALUES " + self.sql_values_question_marks, (
                       sc_row.question_difficulty,
                       sc_row.question_category,
                       sc_row.question_type,
                       sc_row.question_title,
                       sc_row.question_description_title,
                       sc_row.question_description_main,
    
                       sc_row.response_1_text,
                       sc_row.response_1_pts,
                       sc_row.response_1_img_label,
                       self.response_1_img_string_base64_encoded,
                       sc_row.response_1_img_path,
    
                       sc_row.response_2_text,
                       sc_row.response_2_pts,
                       sc_row.response_2_img_label,
                       self.response_2_img_string_base64_encoded,
                       sc_row.response_2_img_path,
    
                       sc_row.response_3_text,
                       sc_row.response_3_pts,
                       sc_row.response_3_img_label,
                       self.response_3_img_string_base64_encoded,
                       sc_row.response_3_img_path,
    
                       sc_row.response_4_text,
                       sc_row.response_4_pts,
                       sc_row.response_4_img_label,
                       self.response_4_img_string_base64_encoded,
                       sc_row.response_4_img_path,
    
                       sc_row.response_5_text,
                       sc_row.response_5_pts,
                       sc_row.response_5_img_label,
                       self.response_5_img_string_base64_encoded,
                       sc_row.response_5_img_path,
    
                       sc_row.response_6_text,
                       sc_row.response_6_pts,
                       sc_row.response_6_img_label,
                       self.response_6_img_string_base64_encoded,
                       sc_row.response_6_img_path,
    
                       sc_row.response_7_text,
                       sc_row.response_7_pts,
                       sc_row.response_7_img_label,
                       self.response_7_img_string_base64_encoded,
                       sc_row.response_7_img_path,
    
                       sc_row.response_8_text,
                       sc_row.response_8_pts,
                       sc_row.response_8_img_label,
                       self.response_8_img_string_base64_encoded,
                       sc_row.response_8_img_path,
    
                       sc_row.response_9_text,
                       sc_row.response_9_pts,
                       sc_row.response_9_img_label,
                       self.response_9_img_string_base64_encoded,
                       sc_row.response_9_img_path,
    
                       sc_row.response_10_text,
                       sc_row.response_10_pts,
                       sc_row.response_10_img_label,
                       self.response_10_img_string_base64_encoded,
                       sc_row.response_10_img_path,



                       sc_row.picture_preview_pixel,
    
                       sc_row.description_img_name_1,
                       self.sc_description_img_data_1,
                       sc_row.description_img_path_1,
    
                       sc_row.description_img_name_2,
                       self.sc_description_img_data_2,
                       sc_row.description_img_path_2,
    
                       sc_row.description_img_name_3,
                       self.sc_description_img_data_3,
                       sc_row.description_img_path_3,
    
                       sc_row.test_time,
                       sc_row.var_number,
                       sc_row.question_pool_tag,
                       sc_row.question_author,
                       sc_row.mix_answers
                     ))
        
        
        
                    conn.commit()

            print("     Datei geladen!")
            print(" ")
            print("SC_DB-Einträge: ", "NEU: " + str(self.number_of_new_entries_from_excel), " -- EDITIERT: " + str(self.number_of_entries_edited))

            for i in range(len(self.edited_questions_list)):
                print("     Frage editiert: ", self.edited_questions_list[i])

            print(" ")

        elif self.question_type == "formelfrage" or self.question_type == "formel frage":
            print("-------------------------------------")
            print("Öffne Datei:  \"" + self.xlsx_path + "\"...", end="", flush=True)
            # Mit Formelfrage Datenbank verbinden
            conn = sqlite3.connect(self.database_formelfrage_path)
            c = conn.cursor()

            self.number_of_new_entries_from_excel = 0
            self.number_of_entries_edited = 0
            #####
            query = 'SELECT * FROM formelfrage_table '
            c.execute(query)

            database_rows = c.fetchall()

            # Alle Fragen-Titel der Datenbank-Einträge in einer String zusammen fassen
            for database_row in database_rows:
                entry_string += database_row[db_entry_to_index_dict['question_title']]

            #####

            for ff_row in self.dataframe.itertuples():

                # Wenn exakter Fragentitel im String gefunden wird und der Titel somit bereits in DB vorhanden ist, dann editieren und keine neue Frage hinzufügen
                if ff_row[db_entry_to_index_dict['question_title']+1] in entry_string:
                    c.execute(
                        """UPDATE formelfrage_table SET
                                                question_difficulty = :question_difficulty,
                                                question_category = :question_category,
                                                question_type = :question_type,
                                                question_title = :question_title,
                                                question_description_title = :question_description_title,
                                                question_description_main = :question_description_main,
                                                res1_formula = :res1_formula,
                                                res2_formula = :res2_formula,
                                                res3_formula = :res3_formula,
                                                res4_formula = :res4_formula,
                                                res5_formula = :res5_formula,
                                                res6_formula = :res6_formula,
                                                res7_formula = :res7_formula,
                                                res8_formula = :res8_formula,
                                                res9_formula = :res9_formula,
                                                res10_formula = :res10_formula,
                                                var1_name = :var1_name,
                                                var1_min = :var1_min,
                                                var1_max = :var1_max,
                                                var1_prec = :var1_prec,
                                                var1_divby = :var1_divby,
                                                var1_unit = :var1_unit,
                                                var2_name = :var2_name,
                                                var2_min = :var2_min,
                                                var2_max = :var2_max,
                                                var2_prec = :var2_prec,
                                                var2_divby = :var2_divby,
                                                var2_unit = :var2_unit,
                                                var3_name = :var3_name,
                                                var3_min = :var3_min,
                                                var3_max = :var3_max,
                                                var3_prec = :var3_prec,
                                                var3_divby = :var3_divby,
                                                var3_unit = :var3_unit,
                                                var4_name = :var4_name,
                                                var4_min = :var4_min,
                                                var4_max = :var4_max,
                                                var4_prec = :var4_prec,
                                                var4_divby = :var4_divby,
                                                var4_unit = :var4_unit,
                                                var5_name = :var5_name,
                                                var5_min = :var5_min,
                                                var5_max = :var5_max,
                                                var5_prec = :var5_prec,
                                                var5_divby = :var5_divby,
                                                var5_unit = :var5_unit,
                                                var6_name = :var6_name,
                                                var6_min = :var6_min,
                                                var6_max = :var6_max,
                                                var6_prec = :var6_prec,
                                                var6_divby = :var6_divby,
                                                var6_unit = :var6_unit,
                                                var7_name = :var7_name,
                                                var7_min = :var7_min,
                                                var7_max = :var7_max,
                                                var7_prec = :var7_prec,
                                                var7_divby = :var7_divby,
                                                var7_unit = :var7_unit,
                                                var8_name = :var8_name,
                                                var8_min = :var8_min,
                                                var8_max = :var8_max,
                                                var8_prec = :var8_prec,
                                                var8_divby = :var8_divby,
                                                var8_unit = :var8_unit,
                                                var9_name = :var9_name,
                                                var9_min = :var9_min,
                                                var9_max = :var9_max,
                                                var9_prec = :var9_prec,
                                                var9_divby = :var9_divby,
                                                var9_unit = :var9_unit,
                                                var10_name = :var10_name,
                                                var10_min = :var10_min,
                                                var10_max = :var10_max,
                                                var10_prec = :var10_prec,
                                                var10_divby = :var10_divby,
                                                var10_unit = :var10_unit,
                                                var11_name = :var11_name,
                                                var11_min = :var11_min,
                                                var11_max = :var11_max,
                                                var11_prec = :var11_prec,
                                                var11_divby = :var11_divby,
                                                var11_unit = :var11_unit,
                                                var12_name = :var12_name,
                                                var12_min = :var12_min,
                                                var12_max = :var12_max,
                                                var12_prec = :var12_prec,
                                                var12_divby = :var12_divby,
                                                var12_unit = :var12_unit,
                                                var13_name = :var13_name,
                                                var13_min = :var13_min,
                                                var13_max = :var13_max,
                                                var13_prec = :var13_prec,
                                                var13_divby = :var13_divby,
                                                var13_unit = :var13_unit,
                                                var14_name = :var14_name,
                                                var14_min = :var14_min,
                                                var14_max = :var14_max,
                                                var14_prec = :var14_prec,
                                                var14_divby = :var14_divby,
                                                var14_unit = :var14_unit,
                                                var15_name = :var15_name,
                                                var15_min = :var15_min,
                                                var15_max = :var15_max,
                                                var15_prec = :var15_prec,
                                                var15_divby = :var15_divby,
                                                var15_unit = :var15_unit,
                                                res1_name = :res1_name,
                                                res1_min = :res1_min,
                                                res1_max = :res1_max,
                                                res1_prec = :res1_prec,
                                                res1_tol = :res1_tol,
                                                res1_points = :res1_points,
                                                res1_unit = :res1_unit,
                                                res2_name = :res2_name,
                                                res2_min = :res2_min,
                                                res2_max = :res2_max,
                                                res2_prec = :res2_prec,
                                                res2_tol = :res2_tol,
                                                res2_points = :res2_points,
                                                res2_unit = :res2_unit,
                                                res3_name = :res3_name,
                                                res3_min = :res3_min,
                                                res3_max = :res3_max,
                                                res3_prec = :res3_prec,
                                                res3_tol = :res3_tol,
                                                res3_points = :res3_points,
                                                res3_unit = :res3_unit,
                                                res4_name = :res4_name,
                                                res4_min = :res4_min,
                                                res4_max = :res4_max,
                                                res4_prec = :res4_prec,
                                                res4_tol = :res4_tol,
                                                res4_points = :res4_points,
                                                res4_unit = :res4_unit,
                                                res5_name = :res5_name,
                                                res5_min = :res5_min,
                                                res5_max = :res5_max,
                                                res5_prec = :res5_prec,
                                                res5_tol = :res5_tol,
                                                res5_points = :res5_points,
                                                res5_unit = :res5_unit,
                                                res6_name = :res6_name,
                                                res6_min = :res6_min,
                                                res6_max = :res6_max,
                                                res6_prec = :res6_prec,
                                                res6_tol = :res6_tol,
                                                res6_points = :res6_points,
                                                res6_unit = :res6_unit,
                                                res7_name = :res7_name,
                                                res7_min = :res7_min,
                                                res7_max = :res7_max,
                                                res7_prec = :res7_prec,
                                                res7_tol = :res7_tol,
                                                res7_points = :res7_points,
                                                res7_unit = :res7_unit,
                                                res8_name = :res8_name,
                                                res8_min = :res8_min,
                                                res8_max = :res8_max,
                                                res8_prec = :res8_prec,
                                                res8_tol = :res8_tol,
                                                res8_points = :res8_points,
                                                res8_unit = :res8_unit,
                                                res9_name = :res9_name,
                                                res9_min = :res9_min,
                                                res9_max = :res9_max,
                                                res9_prec = :res9_prec,
                                                res9_tol = :res9_tol,
                                                res9_points = :res9_points,
                                                res9_unit = :res9_unit,
                                                res10_name = :res10_name,
                                                res10_min = :res10_min,
                                                res10_max = :res10_max,
                                                res10_prec = :res10_prec,
                                                res10_tol = :res10_tol,
                                                res10_points = :res10_points,
                                                res10_unit = :res10_unit,
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
                    
                                                WHERE question_title = :question_title""",
                              {'question_difficulty': ff_row[db_entry_to_index_dict['question_difficulty']+1],
                               'question_category': ff_row[db_entry_to_index_dict['question_category']+1],
                               'question_type': ff_row[db_entry_to_index_dict['question_type']+1],
                               'question_title': ff_row[db_entry_to_index_dict['question_title']+1],
                               'question_description_title': ff_row[db_entry_to_index_dict['question_description_title']+1],
                               'question_description_main': ff_row[db_entry_to_index_dict['question_description_main']+1],

                               'res1_formula': ff_row[db_entry_to_index_dict['res1_formula']+1],
                               'res2_formula': ff_row[db_entry_to_index_dict['res2_formula']+1],
                               'res3_formula': ff_row[db_entry_to_index_dict['res3_formula']+1],
                               'res4_formula': ff_row[db_entry_to_index_dict['res4_formula']+1],
                               'res5_formula': ff_row[db_entry_to_index_dict['res5_formula']+1],
                               'res6_formula': ff_row[db_entry_to_index_dict['res6_formula']+1],
                               'res7_formula': ff_row[db_entry_to_index_dict['res7_formula']+1],
                               'res8_formula': ff_row[db_entry_to_index_dict['res8_formula']+1],
                               'res9_formula': ff_row[db_entry_to_index_dict['res9_formula']+1],
                               'res10_formula': ff_row[db_entry_to_index_dict['res10_formula']+1],

                               'var1_name': ff_row[db_entry_to_index_dict['var1_name']+1],
                               'var1_min': ff_row[db_entry_to_index_dict['var1_min']+1],
                               'var1_max': ff_row[db_entry_to_index_dict['var1_max']+1],
                               'var1_prec': ff_row[db_entry_to_index_dict['var1_prec']+1],
                               'var1_divby': ff_row[db_entry_to_index_dict['var1_divby']+1],
                               'var1_unit': ff_row[db_entry_to_index_dict['var1_unit']+1],

                               'var2_name': ff_row[db_entry_to_index_dict['var2_name'] + 1],
                               'var2_min': ff_row[db_entry_to_index_dict['var2_min'] + 1],
                               'var2_max': ff_row[db_entry_to_index_dict['var2_max'] + 1],
                               'var2_prec': ff_row[db_entry_to_index_dict['var2_prec'] + 1],
                               'var2_divby': ff_row[db_entry_to_index_dict['var2_divby'] + 1],
                               'var2_unit': ff_row[db_entry_to_index_dict['var2_unit'] + 1],

                               'var3_name': ff_row[db_entry_to_index_dict['var3_name'] + 1],
                               'var3_min': ff_row[db_entry_to_index_dict['var3_min'] + 1],
                               'var3_max': ff_row[db_entry_to_index_dict['var3_max'] + 1],
                               'var3_prec': ff_row[db_entry_to_index_dict['var3_prec'] + 1],
                               'var3_divby': ff_row[db_entry_to_index_dict['var3_divby'] + 1],
                               'var3_unit': ff_row[db_entry_to_index_dict['var3_unit'] + 1],

                               'var4_name': ff_row[db_entry_to_index_dict['var4_name'] + 1],
                               'var4_min': ff_row[db_entry_to_index_dict['var4_min'] + 1],
                               'var4_max': ff_row[db_entry_to_index_dict['var4_max'] + 1],
                               'var4_prec': ff_row[db_entry_to_index_dict['var4_prec'] + 1],
                               'var4_divby': ff_row[db_entry_to_index_dict['var4_divby'] + 1],
                               'var4_unit': ff_row[db_entry_to_index_dict['var4_unit'] + 1],

                               'var5_name': ff_row[db_entry_to_index_dict['var5_name'] + 1],
                               'var5_min': ff_row[db_entry_to_index_dict['var5_min'] + 1],
                               'var5_max': ff_row[db_entry_to_index_dict['var5_max'] + 1],
                               'var5_prec': ff_row[db_entry_to_index_dict['var5_prec'] + 1],
                               'var5_divby': ff_row[db_entry_to_index_dict['var5_divby'] + 1],
                               'var5_unit': ff_row[db_entry_to_index_dict['var5_unit'] + 1],

                               'var6_name': ff_row[db_entry_to_index_dict['var6_name'] + 1],
                               'var6_min': ff_row[db_entry_to_index_dict['var6_min'] + 1],
                               'var6_max': ff_row[db_entry_to_index_dict['var6_max'] + 1],
                               'var6_prec': ff_row[db_entry_to_index_dict['var6_prec'] + 1],
                               'var6_divby': ff_row[db_entry_to_index_dict['var6_divby'] + 1],
                               'var6_unit': ff_row[db_entry_to_index_dict['var6_unit'] + 1],

                               'var7_name': ff_row[db_entry_to_index_dict['var7_name'] + 1],
                               'var7_min': ff_row[db_entry_to_index_dict['var7_min'] + 1],
                               'var7_max': ff_row[db_entry_to_index_dict['var7_max'] + 1],
                               'var7_prec': ff_row[db_entry_to_index_dict['var7_prec'] + 1],
                               'var7_divby': ff_row[db_entry_to_index_dict['var7_divby'] + 1],
                               'var7_unit': ff_row[db_entry_to_index_dict['var7_unit'] + 1],

                               'var8_name': ff_row[db_entry_to_index_dict['var8_name'] + 1],
                               'var8_min': ff_row[db_entry_to_index_dict['var8_min'] + 1],
                               'var8_max': ff_row[db_entry_to_index_dict['var8_max'] + 1],
                               'var8_prec': ff_row[db_entry_to_index_dict['var8_prec'] + 1],
                               'var8_divby': ff_row[db_entry_to_index_dict['var8_divby'] + 1],
                               'var8_unit': ff_row[db_entry_to_index_dict['var8_unit'] + 1],

                               'var9_name': ff_row[db_entry_to_index_dict['var9_name'] + 1],
                               'var9_min': ff_row[db_entry_to_index_dict['var9_min'] + 1],
                               'var9_max': ff_row[db_entry_to_index_dict['var9_max'] + 1],
                               'var9_prec': ff_row[db_entry_to_index_dict['var9_prec'] + 1],
                               'var9_divby': ff_row[db_entry_to_index_dict['var9_divby'] + 1],
                               'var9_unit': ff_row[db_entry_to_index_dict['var9_unit'] + 1],

                               'var10_name': ff_row[db_entry_to_index_dict['var10_name'] + 1],
                               'var10_min': ff_row[db_entry_to_index_dict['var10_min'] + 1],
                               'var10_max': ff_row[db_entry_to_index_dict['var10_max'] + 1],
                               'var10_prec': ff_row[db_entry_to_index_dict['var10_prec'] + 1],
                               'var10_divby': ff_row[db_entry_to_index_dict['var10_divby'] + 1],
                               'var10_unit': ff_row[db_entry_to_index_dict['var10_unit'] + 1],

                               'var11_name': ff_row[db_entry_to_index_dict['var11_name'] + 1],
                               'var11_min': ff_row[db_entry_to_index_dict['var11_min'] + 1],
                               'var11_max': ff_row[db_entry_to_index_dict['var11_max'] + 1],
                               'var11_prec': ff_row[db_entry_to_index_dict['var11_prec'] + 1],
                               'var11_divby': ff_row[db_entry_to_index_dict['var11_divby'] + 1],
                               'var11_unit': ff_row[db_entry_to_index_dict['var11_unit'] + 1],

                               'var12_name': ff_row[db_entry_to_index_dict['var12_name'] + 1],
                               'var12_min': ff_row[db_entry_to_index_dict['var12_min'] + 1],
                               'var12_max': ff_row[db_entry_to_index_dict['var12_max'] + 1],
                               'var12_prec': ff_row[db_entry_to_index_dict['var12_prec'] + 1],
                               'var12_divby': ff_row[db_entry_to_index_dict['var12_divby'] + 1],
                               'var12_unit': ff_row[db_entry_to_index_dict['var12_unit'] + 1],

                               'var13_name': ff_row[db_entry_to_index_dict['var13_name'] + 1],
                               'var13_min': ff_row[db_entry_to_index_dict['var13_min'] + 1],
                               'var13_max': ff_row[db_entry_to_index_dict['var13_max'] + 1],
                               'var13_prec': ff_row[db_entry_to_index_dict['var13_prec'] + 1],
                               'var13_divby': ff_row[db_entry_to_index_dict['var13_divby'] + 1],
                               'var13_unit': ff_row[db_entry_to_index_dict['var13_unit'] + 1],

                               'var14_name': ff_row[db_entry_to_index_dict['var14_name'] + 1],
                               'var14_min': ff_row[db_entry_to_index_dict['var14_min'] + 1],
                               'var14_max': ff_row[db_entry_to_index_dict['var14_max'] + 1],
                               'var14_prec': ff_row[db_entry_to_index_dict['var14_prec'] + 1],
                               'var14_divby': ff_row[db_entry_to_index_dict['var14_divby'] + 1],
                               'var14_unit': ff_row[db_entry_to_index_dict['var14_unit'] + 1],

                               'var15_name': ff_row[db_entry_to_index_dict['var15_name'] + 1],
                               'var15_min': ff_row[db_entry_to_index_dict['var15_min'] + 1],
                               'var15_max': ff_row[db_entry_to_index_dict['var15_max'] + 1],
                               'var15_prec': ff_row[db_entry_to_index_dict['var15_prec'] + 1],
                               'var15_divby': ff_row[db_entry_to_index_dict['var15_divby'] + 1],
                               'var15_unit': ff_row[db_entry_to_index_dict['var15_unit'] + 1],

                               'res1_name': ff_row[db_entry_to_index_dict['res1_name'] + 1],
                               'res1_min': ff_row[db_entry_to_index_dict['res1_min'] + 1],
                               'res1_max': ff_row[db_entry_to_index_dict['res1_max'] + 1],
                               'res1_prec': ff_row[db_entry_to_index_dict['res1_prec'] + 1],
                               'res1_tol': ff_row[db_entry_to_index_dict['res1_tol'] + 1],
                               'res1_points': ff_row[db_entry_to_index_dict['res1_points'] + 1],
                               'res1_unit': ff_row[db_entry_to_index_dict['res1_unit'] + 1],

                               'res2_name': ff_row[db_entry_to_index_dict['res2_name'] + 1],
                               'res2_min': ff_row[db_entry_to_index_dict['res2_min'] + 1],
                               'res2_max': ff_row[db_entry_to_index_dict['res2_max'] + 1],
                               'res2_prec': ff_row[db_entry_to_index_dict['res2_prec'] + 1],
                               'res2_tol': ff_row[db_entry_to_index_dict['res2_tol'] + 1],
                               'res2_points': ff_row[db_entry_to_index_dict['res2_points'] + 1],
                               'res2_unit': ff_row[db_entry_to_index_dict['res2_unit'] + 1],

                               'res3_name': ff_row[db_entry_to_index_dict['res3_name'] + 1],
                               'res3_min': ff_row[db_entry_to_index_dict['res3_min'] + 1],
                               'res3_max': ff_row[db_entry_to_index_dict['res3_max'] + 1],
                               'res3_prec': ff_row[db_entry_to_index_dict['res3_prec'] + 1],
                               'res3_tol': ff_row[db_entry_to_index_dict['res3_tol'] + 1],
                               'res3_points': ff_row[db_entry_to_index_dict['res3_points'] + 1],
                               'res3_unit': ff_row[db_entry_to_index_dict['res3_unit'] + 1],

                               'res4_name': ff_row[db_entry_to_index_dict['res4_name'] + 1],
                               'res4_min': ff_row[db_entry_to_index_dict['res4_min'] + 1],
                               'res4_max': ff_row[db_entry_to_index_dict['res4_max'] + 1],
                               'res4_prec': ff_row[db_entry_to_index_dict['res4_prec'] + 1],
                               'res4_tol': ff_row[db_entry_to_index_dict['res4_tol'] + 1],
                               'res4_points': ff_row[db_entry_to_index_dict['res4_points'] + 1],
                               'res4_unit': ff_row[db_entry_to_index_dict['res4_unit'] + 1],

                               'res5_name': ff_row[db_entry_to_index_dict['res5_name'] + 1],
                               'res5_min': ff_row[db_entry_to_index_dict['res5_min'] + 1],
                               'res5_max': ff_row[db_entry_to_index_dict['res5_max'] + 1],
                               'res5_prec': ff_row[db_entry_to_index_dict['res5_prec'] + 1],
                               'res5_tol': ff_row[db_entry_to_index_dict['res5_tol'] + 1],
                               'res5_points': ff_row[db_entry_to_index_dict['res5_points'] + 1],
                               'res5_unit': ff_row[db_entry_to_index_dict['res5_unit'] + 1],

                               'res6_name': ff_row[db_entry_to_index_dict['res6_name'] + 1],
                               'res6_min': ff_row[db_entry_to_index_dict['res6_min'] + 1],
                               'res6_max': ff_row[db_entry_to_index_dict['res6_max'] + 1],
                               'res6_prec': ff_row[db_entry_to_index_dict['res6_prec'] + 1],
                               'res6_tol': ff_row[db_entry_to_index_dict['res6_tol'] + 1],
                               'res6_points': ff_row[db_entry_to_index_dict['res6_points'] + 1],
                               'res6_unit': ff_row[db_entry_to_index_dict['res6_unit'] + 1],

                               'res7_name': ff_row[db_entry_to_index_dict['res7_name'] + 1],
                               'res7_min': ff_row[db_entry_to_index_dict['res7_min'] + 1],
                               'res7_max': ff_row[db_entry_to_index_dict['res7_max'] + 1],
                               'res7_prec': ff_row[db_entry_to_index_dict['res7_prec'] + 1],
                               'res7_tol': ff_row[db_entry_to_index_dict['res7_tol'] + 1],
                               'res7_points': ff_row[db_entry_to_index_dict['res7_points'] + 1],
                               'res7_unit': ff_row[db_entry_to_index_dict['res7_unit'] + 1],

                               'res8_name': ff_row[db_entry_to_index_dict['res8_name'] + 1],
                               'res8_min': ff_row[db_entry_to_index_dict['res8_min'] + 1],
                               'res8_max': ff_row[db_entry_to_index_dict['res8_max'] + 1],
                               'res8_prec': ff_row[db_entry_to_index_dict['res8_prec'] + 1],
                               'res8_tol': ff_row[db_entry_to_index_dict['res8_tol'] + 1],
                               'res8_points': ff_row[db_entry_to_index_dict['res8_points'] + 1],
                               'res8_unit': ff_row[db_entry_to_index_dict['res8_unit'] + 1],

                               'res9_name': ff_row[db_entry_to_index_dict['res9_name'] + 1],
                               'res9_min': ff_row[db_entry_to_index_dict['res9_min'] + 1],
                               'res9_max': ff_row[db_entry_to_index_dict['res9_max'] + 1],
                               'res9_prec': ff_row[db_entry_to_index_dict['res9_prec'] + 1],
                               'res9_tol': ff_row[db_entry_to_index_dict['res9_tol'] + 1],
                               'res9_points': ff_row[db_entry_to_index_dict['res9_points'] + 1],
                               'res9_unit': ff_row[db_entry_to_index_dict['res9_unit'] + 1],

                               'res10_name': ff_row[db_entry_to_index_dict['res10_name'] + 1],
                               'res10_min': ff_row[db_entry_to_index_dict['res10_min'] + 1],
                               'res10_max': ff_row[db_entry_to_index_dict['res10_max'] + 1],
                               'res10_prec': ff_row[db_entry_to_index_dict['res10_prec'] + 1],
                               'res10_tol': ff_row[db_entry_to_index_dict['res10_tol'] + 1],
                               'res10_points': ff_row[db_entry_to_index_dict['res10_points'] + 1],
                               'res10_unit': ff_row[db_entry_to_index_dict['res10_unit'] + 1],

                               'description_img_name_1': ff_row[db_entry_to_index_dict['description_img_name_1'] + 1],
                               'description_img_data_1': ff_row[db_entry_to_index_dict['description_img_data_1'] + 1],
                               'description_img_path_1': ff_row[db_entry_to_index_dict['description_img_path_1'] + 1],

                               'description_img_name_2': ff_row[db_entry_to_index_dict['description_img_name_2'] + 1],
                               'description_img_data_2': ff_row[db_entry_to_index_dict['description_img_data_2'] + 1],
                               'description_img_path_2': ff_row[db_entry_to_index_dict['description_img_path_2'] + 1],

                               'description_img_name_3': ff_row[db_entry_to_index_dict['description_img_name_3'] + 1],
                               'description_img_data_3': ff_row[db_entry_to_index_dict['description_img_data_3'] + 1],
                               'description_img_path_3': ff_row[db_entry_to_index_dict['description_img_path_3'] + 1],

                               'test_time': ff_row[db_entry_to_index_dict['test_time'] + 1],
                               'question_pool_tag': ff_row[db_entry_to_index_dict['question_pool_tag'] + 1],
                               'question_author': ff_row[db_entry_to_index_dict['question_author'] + 1],
                               'oid': ff_row[-1]
                               })

                    conn.commit()


                    self.edited_questions_list.append(ff_row[db_entry_to_index_dict['question_title']+1])
                    self.number_of_entries_edited += 1

                # Wenn Fragentitel nicht vorhanden ist, dann neu in DB importieren
                else:
                    self.number_of_new_entries_from_excel += 1

                    # Bilder auslesen
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


            #print("Load File: \"" + self.xlsx_path + "\" in formelfrage_table...done!")


            print("     Datei geladen!")
            print(" ")
            print("FF_DB-Einträge: ", "NEU: " + str(self.number_of_new_entries_from_excel), " -- EDITIERT: " + str(self.number_of_entries_edited))

            for i in range(len(self.edited_questions_list)):
                print("     Frage editiert: ",self.edited_questions_list[i])
            print(" ")


        elif self.question_type == "multiplechoice" or self.question_type == "multiple choice":
            print("-------------------------------------")
            print("Öffne Datei:  \"" + self.xlsx_path + "\"...", end="", flush=True)
            
            # Mit MultipleChoice Datenbank verbinden
            conn = sqlite3.connect(self.database_multiplechoice_path)
            c = conn.cursor()

            self.number_of_new_entries_from_excel = 0
            self.number_of_entries_edited = 0
            #####
            query = 'SELECT * FROM multiplechoice_table '
            c.execute(query)

            database_rows = c.fetchall()

            # Alle Fragen-Titel der Datenbank-Einträge in einer String zusammen fassen
            for database_row in database_rows:
                entry_string += database_row[db_entry_to_index_dict['question_title']]
            
            for mc_row in self.dataframe.itertuples():

                # Wenn exakter Fragentitel im String gefunden wird und der Titel somit bereits in DB vorhanden ist, dann editieren und keine neue Frage hinzufügen
                if mc_row[db_entry_to_index_dict['question_title'] + 1] in entry_string:
                    c.execute(
                        """UPDATE multiplechoice_table SET
                                question_difficulty= :question_difficulty,
                                question_category= :question_category,
                                question_type= :question_type,
                
                                question_title= :question_title,
                                question_description_title= :question_description_title,
                                question_description_main= :question_description_main,
                                
                                response_1_text= :response_1_text,
                                response_1_pts_correct_answer= :response_1_pts_correct_answer,
                                response_1_pts_false_answer= :response_1_pts_false_answer,
                                response_1_img_label= :response_1_img_label,
                                response_1_img_string_base64_encoded= :response_1_img_string_base64_encoded,
                                response_1_img_path= :response_1_img_path,
                
                                response_2_text= :response_2_text,
                                response_2_pts_correct_answer= :response_2_pts_correct_answer,
                                response_2_pts_false_answer= :response_2_pts_false_answer,
                                response_2_img_label= :response_2_img_label,
                                response_2_img_string_base64_encoded= :response_2_img_string_base64_encoded,
                                response_2_img_path= :response_2_img_path,
                
                                response_3_text= :response_3_text,
                                response_3_pts_correct_answer= :response_3_pts_correct_answer,
                                response_3_pts_false_answer= :response_3_pts_false_answer,
                                response_3_img_label= :response_3_img_label,
                                response_3_img_string_base64_encoded= :response_3_img_string_base64_encoded,
                                response_3_img_path= :response_3_img_path,
                
                                response_4_text= :response_4_text,
                                response_4_pts_correct_answer= :response_4_pts_correct_answer,
                                response_4_pts_false_answer= :response_4_pts_false_answer,
                                response_4_img_label= :response_4_img_label,
                                response_4_img_string_base64_encoded= :response_4_img_string_base64_encoded,
                                response_4_img_path= :response_4_img_path,
                
                                response_5_text= :response_5_text,
                                response_5_pts_correct_answer= :response_5_pts_correct_answer,
                                response_5_pts_false_answer= :response_5_pts_false_answer,
                                response_5_img_label= :response_5_img_label,
                                response_5_img_string_base64_encoded= :response_5_img_string_base64_encoded,
                                response_5_img_path= :response_5_img_path,
                
                                response_6_text= :response_6_text,
                                response_6_pts_correct_answer= :response_6_pts_correct_answer,
                                response_6_pts_false_answer= :response_6_pts_false_answer,
                                response_6_img_label= :response_6_img_label,
                                response_6_img_string_base64_encoded= :response_6_img_string_base64_encoded,
                                response_6_img_path= :response_6_img_path,
                
                                response_7_text= :response_7_text,
                                response_7_pts_correct_answer= :response_7_pts_correct_answer,
                                response_7_pts_false_answer= :response_7_pts_false_answer,
                                response_7_img_label= :response_7_img_label,
                                response_7_img_string_base64_encoded= :response_7_img_string_base64_encoded,
                                response_7_img_path= :response_7_img_path,
                
                                response_8_text= :response_8_text,
                                response_8_pts_correct_answer= :response_8_pts_correct_answer,
                                response_8_pts_false_answer= :response_8_pts_false_answer,
                                response_8_img_label= :response_8_img_label,
                                response_8_img_string_base64_encoded= :response_8_img_string_base64_encoded,
                                response_8_img_path= :response_8_img_path,
                
                                response_9_text= :response_9_text,
                                response_9_pts_correct_answer= :response_9_pts_correct_answer,
                                response_9_pts_false_answer= :response_9_pts_false_answer,
                                response_9_img_label= :response_9_img_label,
                                response_9_img_string_base64_encoded= :response_9_img_string_base64_encoded,
                                response_9_img_path= :response_9_img_path,
                
                                response_10_text= :response_10_text,
                                response_10_pts_correct_answer= :response_10_pts_correct_answer,
                                response_10_pts_false_answer= :response_10_pts_false_answer,
                                response_10_img_label= :response_10_img_label,
                                response_10_img_string_base64_encoded= :response_10_img_string_base64_encoded,
                                response_10_img_path= :response_10_img_path,
                
                                picture_preview_pixel= :picture_preview_pixel,
                
                                description_img_name_1= :description_img_name_1,
                                description_img_data_1= :description_img_data_1,
                                description_img_path_1= :description_img_path_1,
                
                                description_img_name_2= :description_img_name_2,
                                description_img_data_2= :description_img_data_2,
                                description_img_path_2= :description_img_path_2,
                
                                description_img_name_3= :description_img_name_3,
                                description_img_data_3= :description_img_data_3,
                                description_img_path_3= :description_img_path_3,
                
                                test_time= :test_time,
                
                                
                                question_pool_tag= :question_pool_tag,
                                question_author= :question_author
    
                                WHERE question_title = :question_title""",

                                # "+1" ist notwendig weil "mc_row" mit '1' anfängt und das DICT mit '0'
                                {'question_difficulty': mc_row[db_entry_to_index_dict['question_difficulty'] + 1],
                                 'question_category': mc_row[db_entry_to_index_dict['question_category'] + 1],
                                 'question_type': mc_row[db_entry_to_index_dict['question_type'] + 1],
                
                                 'question_title': mc_row[db_entry_to_index_dict['question_title'] + 1],
                                 'question_description_title': mc_row[db_entry_to_index_dict['question_description_title'] + 1],
                                 'question_description_main': mc_row[db_entry_to_index_dict['question_description_main'] + 1],
                                

                                'response_1_text':                       mc_row[db_entry_to_index_dict['response_1_text'] + 1],
                                'response_1_pts_correct_answer':         mc_row[db_entry_to_index_dict['response_1_pts_correct_answer'] + 1],
                                'response_1_pts_false_answer':           mc_row[db_entry_to_index_dict['response_1_pts_false_answer'] + 1],
                                'response_1_img_label':                  mc_row[db_entry_to_index_dict['response_1_img_label'] + 1],
                                'response_1_img_string_base64_encoded':  mc_row[db_entry_to_index_dict['response_1_img_string_base64_encoded'] + 1],
                                'response_1_img_path':                   mc_row[db_entry_to_index_dict['response_1_img_path'] + 1],
                                
                                'response_2_text':                       mc_row[db_entry_to_index_dict['response_2_text'] + 1],
                                'response_2_pts_correct_answer':         mc_row[db_entry_to_index_dict['response_2_pts_correct_answer'] + 1],
                                'response_2_pts_false_answer':           mc_row[db_entry_to_index_dict['response_2_pts_false_answer'] + 1],
                                'response_2_img_label':                  mc_row[db_entry_to_index_dict['response_2_img_label'] + 1],
                                'response_2_img_string_base64_encoded':  mc_row[db_entry_to_index_dict['response_2_img_string_base64_encoded'] + 1],
                                'response_2_img_path':                   mc_row[db_entry_to_index_dict['response_2_img_path'] + 1],
                                 
                                'response_3_text':                       mc_row[db_entry_to_index_dict['response_3_text'] + 1],
                                'response_3_pts_correct_answer':         mc_row[db_entry_to_index_dict['response_3_pts_correct_answer'] + 1],
                                'response_3_pts_false_answer':           mc_row[db_entry_to_index_dict['response_3_pts_false_answer'] + 1],
                                'response_3_img_label':                  mc_row[db_entry_to_index_dict['response_3_img_label'] + 1],
                                'response_3_img_string_base64_encoded':  mc_row[db_entry_to_index_dict['response_3_img_string_base64_encoded'] + 1],
                                'response_3_img_path':                   mc_row[db_entry_to_index_dict['response_3_img_path'] + 1],
                                 
                                'response_4_text':                       mc_row[db_entry_to_index_dict['response_4_text'] + 1],
                                'response_4_pts_correct_answer':         mc_row[db_entry_to_index_dict['response_4_pts_correct_answer'] + 1],
                                'response_4_pts_false_answer':           mc_row[db_entry_to_index_dict['response_4_pts_false_answer'] + 1],
                                'response_4_img_label':                  mc_row[db_entry_to_index_dict['response_4_img_label'] + 1],
                                'response_4_img_string_base64_encoded':  mc_row[db_entry_to_index_dict['response_4_img_string_base64_encoded'] + 1],
                                'response_4_img_path':                   mc_row[db_entry_to_index_dict['response_4_img_path'] + 1],
                                 
                                'response_5_text':                       mc_row[db_entry_to_index_dict['response_5_text'] + 1],
                                'response_5_pts_correct_answer':         mc_row[db_entry_to_index_dict['response_5_pts_correct_answer'] + 1],
                                'response_5_pts_false_answer':           mc_row[db_entry_to_index_dict['response_5_pts_false_answer'] + 1],
                                'response_5_img_label':                  mc_row[db_entry_to_index_dict['response_5_img_label'] + 1],
                                'response_5_img_string_base64_encoded':  mc_row[db_entry_to_index_dict['response_5_img_string_base64_encoded'] + 1],
                                'response_5_img_path':                   mc_row[db_entry_to_index_dict['response_5_img_path'] + 1],
                                 
                                'response_6_text':                       mc_row[db_entry_to_index_dict['response_6_text'] + 1],
                                'response_6_pts_correct_answer':         mc_row[db_entry_to_index_dict['response_6_pts_correct_answer'] + 1],
                                'response_6_pts_false_answer':           mc_row[db_entry_to_index_dict['response_6_pts_false_answer'] + 1],
                                'response_6_img_label':                  mc_row[db_entry_to_index_dict['response_6_img_label'] + 1],
                                'response_6_img_string_base64_encoded':  mc_row[db_entry_to_index_dict['response_6_img_string_base64_encoded'] + 1],
                                'response_6_img_path':                   mc_row[db_entry_to_index_dict['response_6_img_path'] + 1],
                                 
                                'response_7_text':                       mc_row[db_entry_to_index_dict['response_7_text'] + 1],
                                'response_7_pts_correct_answer':         mc_row[db_entry_to_index_dict['response_7_pts_correct_answer'] + 1],
                                'response_7_pts_false_answer':           mc_row[db_entry_to_index_dict['response_7_pts_false_answer'] + 1],
                                'response_7_img_label':                  mc_row[db_entry_to_index_dict['response_7_img_label'] + 1],
                                'response_7_img_string_base64_encoded':  mc_row[db_entry_to_index_dict['response_7_img_string_base64_encoded'] + 1],
                                'response_7_img_path':                   mc_row[db_entry_to_index_dict['response_7_img_path'] + 1],
                                 
                                'response_8_text':                       mc_row[db_entry_to_index_dict['response_8_text'] + 1],
                                'response_8_pts_correct_answer':         mc_row[db_entry_to_index_dict['response_8_pts_correct_answer'] + 1],
                                'response_8_pts_false_answer':           mc_row[db_entry_to_index_dict['response_8_pts_false_answer'] + 1],
                                'response_8_img_label':                  mc_row[db_entry_to_index_dict['response_8_img_label'] + 1],
                                'response_8_img_string_base64_encoded':  mc_row[db_entry_to_index_dict['response_8_img_string_base64_encoded'] + 1],
                                'response_8_img_path':                   mc_row[db_entry_to_index_dict['response_8_img_path'] + 1],
                                 
                                'response_9_text':                       mc_row[db_entry_to_index_dict['response_9_text'] + 1],
                                'response_9_pts_correct_answer':         mc_row[db_entry_to_index_dict['response_9_pts_correct_answer'] + 1],
                                'response_9_pts_false_answer':           mc_row[db_entry_to_index_dict['response_9_pts_false_answer'] + 1],
                                'response_9_img_label':                  mc_row[db_entry_to_index_dict['response_9_img_label'] + 1],
                                'response_9_img_string_base64_encoded':  mc_row[db_entry_to_index_dict['response_9_img_string_base64_encoded'] + 1],
                                'response_9_img_path':                   mc_row[db_entry_to_index_dict['response_9_img_path'] + 1],
                                 
                                'response_10_text':                       mc_row[db_entry_to_index_dict['response_10_text'] + 1],
                                'response_10_pts_correct_answer':         mc_row[db_entry_to_index_dict['response_10_pts_correct_answer'] + 1],
                                'response_10_pts_false_answer':           mc_row[db_entry_to_index_dict['response_10_pts_false_answer'] + 1],
                                'response_10_img_label':                  mc_row[db_entry_to_index_dict['response_10_img_label'] + 1],
                                'response_10_img_string_base64_encoded':  mc_row[db_entry_to_index_dict['response_10_img_string_base64_encoded'] + 1],
                                'response_10_img_path':                   mc_row[db_entry_to_index_dict['response_10_img_path'] + 1],
                                
                                
                                'picture_preview_pixel': mc_row[db_entry_to_index_dict['picture_preview_pixel'] + 1],
                                
                                'description_img_name_1': mc_row[db_entry_to_index_dict['description_img_name_1'] + 1],
                                'description_img_data_1': mc_row[db_entry_to_index_dict['description_img_data_1'] + 1],
                                'description_img_path_1': mc_row[db_entry_to_index_dict['description_img_path_1'] + 1],
                                
                                'description_img_name_2': mc_row[db_entry_to_index_dict['description_img_name_2'] + 1],
                                'description_img_data_2': mc_row[db_entry_to_index_dict['description_img_data_2'] + 1],
                                'description_img_path_2': mc_row[db_entry_to_index_dict['description_img_path_2'] + 1],
                                
                                'description_img_name_3': mc_row[db_entry_to_index_dict['description_img_name_3'] + 1],
                                'description_img_data_3': mc_row[db_entry_to_index_dict['description_img_data_3'] + 1],
                                'description_img_path_3': mc_row[db_entry_to_index_dict['description_img_path_3'] + 1],
                                
                                'test_time': mc_row[db_entry_to_index_dict['test_time'] + 1],
                                'question_pool_tag': mc_row[db_entry_to_index_dict['question_pool_tag'] + 1],
                                'question_author': mc_row[db_entry_to_index_dict['question_author'] + 1],
                                'oid': mc_row[-1]
                                })

                    conn.commit()

                    self.edited_questions_list.append(mc_row[db_entry_to_index_dict['question_title'] + 1])
                    self.number_of_entries_edited += 1


    
                # Wenn Fragentitel nicht vorhanden ist, dann neu in DB importieren
                else:
                    self.number_of_new_entries_from_excel += 1
                    self.response_1_img_string_base64_encoded = img_path_to_base64_encoded_string('response_1_img_label', 'response_1_img_path', mc_row)
                    self.response_2_img_string_base64_encoded = img_path_to_base64_encoded_string('response_2_img_label', 'response_2_img_path', mc_row)
                    self.response_3_img_string_base64_encoded = img_path_to_base64_encoded_string('response_3_img_label', 'response_3_img_path', mc_row)
                    self.response_4_img_string_base64_encoded = img_path_to_base64_encoded_string('response_4_img_label', 'response_4_img_path', mc_row)
                    self.response_5_img_string_base64_encoded = img_path_to_base64_encoded_string('response_5_img_label', 'response_5_img_path', mc_row)
                    self.response_6_img_string_base64_encoded = img_path_to_base64_encoded_string('response_6_img_label', 'response_6_img_path', mc_row)
                    self.response_7_img_string_base64_encoded = img_path_to_base64_encoded_string('response_7_img_label', 'response_7_img_path', mc_row)
                    self.response_8_img_string_base64_encoded = img_path_to_base64_encoded_string('response_8_img_label', 'response_8_img_path', mc_row)
                    self.response_9_img_string_base64_encoded = img_path_to_base64_encoded_string('response_9_img_label', 'response_9_img_path', mc_row)
                    self.response_10_img_string_base64_encoded = img_path_to_base64_encoded_string('response_10_img_label', 'response_10_img_path', mc_row)
        
        
                    self.mc_description_img_data_1 = Import_Export_Database.excel_import_placeholder_to_data(self, mc_row, self.db_entry_to_index_dict['description_img_data_1'], self.db_entry_to_index_dict['description_img_path_1'])
                    self.mc_description_img_data_2 = Import_Export_Database.excel_import_placeholder_to_data(self, mc_row, self.db_entry_to_index_dict['description_img_data_2'], self.db_entry_to_index_dict['description_img_path_2'])
                    self.mc_description_img_data_3 = Import_Export_Database.excel_import_placeholder_to_data(self, mc_row, self.db_entry_to_index_dict['description_img_data_3'], self.db_entry_to_index_dict['description_img_path_3'])
        
        
                    c.execute("INSERT INTO multiplechoice_table VALUES " + self.sql_values_question_marks, (
                       mc_row.question_difficulty,
                       mc_row.question_category,
                       mc_row.question_type,
                       mc_row.question_title,
                       mc_row.question_description_title,
                       mc_row.question_description_main,
        
                       mc_row.response_1_text,
                       mc_row.response_1_pts_correct_answer,
                       mc_row.response_1_pts_false_answer,
                       mc_row.response_1_img_label,
                       self.response_1_img_string_base64_encoded,
                       mc_row.response_1_img_path,
        
                       mc_row.response_2_text,
                       mc_row.response_2_pts_correct_answer,
                       mc_row.response_2_pts_false_answer,
                       mc_row.response_2_img_label,
                       self.response_2_img_string_base64_encoded,
                       mc_row.response_2_img_path,
        
                       mc_row.response_3_text,
                       mc_row.response_3_pts_correct_answer,
                       mc_row.response_3_pts_false_answer,
                       mc_row.response_3_img_label,
                       self.response_3_img_string_base64_encoded,
                       mc_row.response_3_img_path,
        
                       mc_row.response_4_text,
                       mc_row.response_4_pts_correct_answer,
                       mc_row.response_4_pts_false_answer,
                       mc_row.response_4_img_label,
                       self.response_4_img_string_base64_encoded,
                       mc_row.response_4_img_path,
        
                       mc_row.response_5_text,
                       mc_row.response_5_pts_correct_answer,
                       mc_row.response_5_pts_false_answer,
                       mc_row.response_5_img_label,
                       self.response_5_img_string_base64_encoded,
                       mc_row.response_5_img_path,
        
                       mc_row.response_6_text,
                       mc_row.response_6_pts_correct_answer,
                       mc_row.response_6_pts_false_answer,
                       mc_row.response_6_img_label,
                       self.response_6_img_string_base64_encoded,
                       mc_row.response_6_img_path,
        
                       mc_row.response_7_text,
                       mc_row.response_7_pts_correct_answer,
                       mc_row.response_7_pts_false_answer,
                       mc_row.response_7_img_label,
                       self.response_7_img_string_base64_encoded,
                       mc_row.response_7_img_path,
        
                       mc_row.response_8_text,
                       mc_row.response_8_pts_correct_answer,
                       mc_row.response_8_pts_false_answer,
                       mc_row.response_8_img_label,
                       self.response_8_img_string_base64_encoded,
                       mc_row.response_8_img_path,
        
                       mc_row.response_9_text,
                       mc_row.response_9_pts_correct_answer,
                       mc_row.response_9_pts_false_answer,
                       mc_row.response_9_img_label,
                       self.response_9_img_string_base64_encoded,
                       mc_row.response_9_img_path,
        
                       mc_row.response_10_text,
                       mc_row.response_10_pts_correct_answer,
                       mc_row.response_10_pts_false_answer,
                       mc_row.response_10_img_label,
                       self.response_10_img_string_base64_encoded,
                       mc_row.response_10_img_path,
        
                       mc_row.picture_preview_pixel,
        
                       mc_row.description_img_name_1,
                       self.mc_description_img_data_1,
                       mc_row.description_img_path_1,
        
                       mc_row.description_img_name_2,
                       self.mc_description_img_data_2,
                       mc_row.description_img_path_2,
        
                       mc_row.description_img_name_3,
                       self.mc_description_img_data_3,
                       mc_row.description_img_path_3,
        
                       mc_row.test_time,
                       mc_row.var_number,
                       mc_row.question_pool_tag,
                       mc_row.question_author
                    ))
        
                    conn.commit()
        
                    print("Load File: \"" + self.xlsx_path + "\"  ---> in multiplechoice_table...done!")
                    print("Excel-Einträge: " + str(len(mc_row)))

            print("     Datei geladen!")
            print(" ")
            print("MC_DB-Einträge: ", "NEU: " + str(self.number_of_new_entries_from_excel),
                  " -- EDITIERT: " + str(self.number_of_entries_edited))

            for i in range(len(self.edited_questions_list)):
                print("     Frage editiert: ", self.edited_questions_list[i])

            print(" ")

        elif self.question_type == "zuordnungsfrage" or self.question_type == "zuordnungs frage":
            print("-------------------------------------")
            print("Öffne Datei:  \"" + self.xlsx_path + "\"...", end="", flush=True)
            
            # Mit Zuordnungsfrage Datenbank verbinden
            conn = sqlite3.connect(self.database_zuordnungsfrage_path)
            c = conn.cursor()

            self.number_of_new_entries_from_excel = 0
            self.number_of_entries_edited = 0
            #####
            query = 'SELECT * FROM zuordnungsfrage_table '
            c.execute(query)

            database_rows = c.fetchall()

            # Alle Fragen-Titel der Datenbank-Einträge in einer String zusammen fassen
            for database_row in database_rows:
                entry_string += database_row[db_entry_to_index_dict['question_title']]
            
            for mq_row in self.dataframe.itertuples():

                # Wenn exakter Fragentitel im String gefunden wird und der Titel somit bereits in DB vorhanden ist, dann editieren und keine neue Frage hinzufügen
                if mq_row[db_entry_to_index_dict['question_title'] + 1] in entry_string:
                    c.execute(
                        """UPDATE zuordnungsfrage_table SET
                                    question_difficulty = :question_difficulty,
                                    question_category = :question_category,
                                    question_type = :question_type,
                    
                                    question_title = :question_title,
                                    question_description_title = :question_description_title,
                                    question_description_main = :question_description_main,
                                    
                                    mix_answers = :mix_answers,
                                    assignment_mode = :assignment_mode,
                    
                                    definitions_response_1_text = :definitions_response_1_text,
                                    definitions_response_1_img_label = :definitions_response_1_img_label,
                                    definitions_response_1_img_path = :definitions_response_1_img_path,
                                    definitions_response_1_img_string_base64_encoded = :definitions_response_1_img_string_base64_encoded,
                                    
                                    definitions_response_2_text = :definitions_response_2_text,
                                    definitions_response_2_img_label = :definitions_response_2_img_label,
                                    definitions_response_2_img_path = :definitions_response_2_img_path,
                                    definitions_response_2_img_string_base64_encoded = :definitions_response_2_img_string_base64_encoded,
                                    
                                    definitions_response_3_text = :definitions_response_3_text,
                                    definitions_response_3_img_label = :definitions_response_3_img_label,
                                    definitions_response_3_img_path = :definitions_response_3_img_path,
                                    definitions_response_3_img_string_base64_encoded = :definitions_response_3_img_string_base64_encoded,
                                    
                                    definitions_response_4_text = :definitions_response_4_text,
                                    definitions_response_4_img_label = :definitions_response_4_img_label,
                                    definitions_response_4_img_path = :definitions_response_4_img_path,
                                    definitions_response_4_img_string_base64_encoded = :definitions_response_4_img_string_base64_encoded,
                                    
                                    definitions_response_5_text = :definitions_response_5_text,
                                    definitions_response_5_img_label = :definitions_response_5_img_label,
                                    definitions_response_5_img_path = :definitions_response_5_img_path,
                                    definitions_response_5_img_string_base64_encoded = :definitions_response_5_img_string_base64_encoded,
                                    
                                    definitions_response_6_text = :definitions_response_6_text,
                                    definitions_response_6_img_label = :definitions_response_6_img_label,
                                    definitions_response_6_img_path = :definitions_response_6_img_path,
                                    definitions_response_6_img_string_base64_encoded = :definitions_response_6_img_string_base64_encoded,
                                    
                                    definitions_response_7_text = :definitions_response_7_text,
                                    definitions_response_7_img_label = :definitions_response_7_img_label,
                                    definitions_response_7_img_path = :definitions_response_7_img_path,
                                    definitions_response_7_img_string_base64_encoded = :definitions_response_7_img_string_base64_encoded,
                                    
                                    definitions_response_8_text = :definitions_response_8_text,
                                    definitions_response_8_img_label = :definitions_response_8_img_label,
                                    definitions_response_8_img_path = :definitions_response_8_img_path,
                                    definitions_response_8_img_string_base64_encoded = :definitions_response_8_img_string_base64_encoded,
                                    
                                    definitions_response_9_text = :definitions_response_9_text,
                                    definitions_response_9_img_label = :definitions_response_9_img_label,
                                    definitions_response_9_img_path = :definitions_response_9_img_path,
                                    definitions_response_9_img_string_base64_encoded = :definitions_response_9_img_string_base64_encoded,
                                    
                                    definitions_response_10_text = :definitions_response_10_text,
                                    definitions_response_10_img_label = :definitions_response_10_img_label,
                                    definitions_response_10_img_path = :definitions_response_10_img_path,
                                    definitions_response_10_img_string_base64_encoded = :definitions_response_10_img_string_base64_encoded,
                                    
                                    
                    
                                    terms_response_1_text = :terms_response_1_text,
                                    terms_response_1_img_label = :terms_response_1_img_label,
                                    terms_response_1_img_path = :terms_response_1_img_path,
                                    terms_response_1_img_string_base64_encoded = :terms_response_1_img_string_base64_encoded,
                                    
                                    terms_response_2_text = :terms_response_2_text,
                                    terms_response_2_img_label = :terms_response_2_img_label,
                                    terms_response_2_img_path = :terms_response_2_img_path,
                                    terms_response_2_img_string_base64_encoded = :terms_response_2_img_string_base64_encoded,
                                    
                                    terms_response_3_text = :terms_response_3_text,
                                    terms_response_3_img_label = :terms_response_3_img_label,
                                    terms_response_3_img_path = :terms_response_3_img_path,
                                    terms_response_3_img_string_base64_encoded = :terms_response_3_img_string_base64_encoded,
                                    
                                    terms_response_4_text = :terms_response_4_text,
                                    terms_response_4_img_label = :terms_response_4_img_label,
                                    terms_response_4_img_path = :terms_response_4_img_path,
                                    terms_response_4_img_string_base64_encoded = :terms_response_4_img_string_base64_encoded,
                                    
                                    terms_response_5_text = :terms_response_5_text,
                                    terms_response_5_img_label = :terms_response_5_img_label,
                                    terms_response_5_img_path = :terms_response_5_img_path,
                                    terms_response_5_img_string_base64_encoded = :terms_response_5_img_string_base64_encoded,
                                    
                                    terms_response_6_text = :terms_response_6_text,
                                    terms_response_6_img_label = :terms_response_6_img_label,
                                    terms_response_6_img_path = :terms_response_6_img_path,
                                    terms_response_6_img_string_base64_encoded = :terms_response_6_img_string_base64_encoded,
                                    
                                    terms_response_7_text = :terms_response_7_text,
                                    terms_response_7_img_label = :terms_response_7_img_label,
                                    terms_response_7_img_path = :terms_response_7_img_path,
                                    terms_response_7_img_string_base64_encoded = :terms_response_7_img_string_base64_encoded,
                                    
                                    terms_response_8_text = :terms_response_8_text,
                                    terms_response_8_img_label = :terms_response_8_img_label,
                                    terms_response_8_img_path = :terms_response_8_img_path,
                                    terms_response_8_img_string_base64_encoded = :terms_response_8_img_string_base64_encoded,
                                    
                                    terms_response_9_text = :terms_response_9_text,
                                    terms_response_9_img_label = :terms_response_9_img_label,
                                    terms_response_9_img_path = :terms_response_9_img_path,
                                    terms_response_9_img_string_base64_encoded = :terms_response_9_img_string_base64_encoded,
                                    
                                    terms_response_10_text = :terms_response_10_text,
                                    terms_response_10_img_label = :terms_response_10_img_label,
                                    terms_response_10_img_path = :terms_response_10_img_path,
                                    terms_response_10_img_string_base64_encoded = :terms_response_10_img_string_base64_encoded,
                                    
                    
                                    assignment_pairs_definition_1 = :assignment_pairs_definition_1,
                                    assignment_pairs_term_1 = :assignment_pairs_term_1,
                                    assignment_pairs_1_pts = :assignment_pairs_1_pts,
                                    
                                    assignment_pairs_definition_2 = :assignment_pairs_definition_2,
                                    assignment_pairs_term_2 = :assignment_pairs_term_2,
                                    assignment_pairs_2_pts = :assignment_pairs_2_pts,
                                    
                                    assignment_pairs_definition_3 = :assignment_pairs_definition_3,
                                    assignment_pairs_term_3 = :assignment_pairs_term_3,
                                    assignment_pairs_3_pts = :assignment_pairs_3_pts,
                                    
                                    assignment_pairs_definition_4 = :assignment_pairs_definition_4,
                                    assignment_pairs_term_4 = :assignment_pairs_term_4,
                                    assignment_pairs_4_pts = :assignment_pairs_4_pts,
                                    
                                    assignment_pairs_definition_5 = :assignment_pairs_definition_5,
                                    assignment_pairs_term_5 = :assignment_pairs_term_5,
                                    assignment_pairs_5_pts = :assignment_pairs_5_pts,
                                    
                                    assignment_pairs_definition_6 = :assignment_pairs_definition_6,
                                    assignment_pairs_term_6 = :assignment_pairs_term_6,
                                    assignment_pairs_6_pts = :assignment_pairs_6_pts,
                                    
                                    assignment_pairs_definition_7 = :assignment_pairs_definition_7,
                                    assignment_pairs_term_7 = :assignment_pairs_term_7,
                                    assignment_pairs_7_pts = :assignment_pairs_7_pts,
                                    
                                    assignment_pairs_definition_8 = :assignment_pairs_definition_8,
                                    assignment_pairs_term_8 = :assignment_pairs_term_8,
                                    assignment_pairs_8_pts = :assignment_pairs_8_pts,
                                    
                                    assignment_pairs_definition_9 = :assignment_pairs_definition_9,
                                    assignment_pairs_term_9 = :assignment_pairs_term_9,
                                    assignment_pairs_9_pts = :assignment_pairs_9_pts,
                                    
                                    assignment_pairs_definition_10 = :assignment_pairs_definition_10,
                                    assignment_pairs_term_10 = :assignment_pairs_term_10,
                                    assignment_pairs_10_pts = :assignment_pairs_10_pts,
                                    
                    
                                    picture_preview_pixel = :picture_preview_pixel,
                    
                    
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
                                    
                                    WHERE question_title = :question_title""",
                               {'question_difficulty': mq_row[db_entry_to_index_dict['question_difficulty'] + 1],
                                'question_category': mq_row[db_entry_to_index_dict['question_category'] + 1],
                                'question_type': mq_row[db_entry_to_index_dict['question_type'] + 1],

                                'question_title': mq_row[db_entry_to_index_dict['question_title'] + 1],
                                'question_description_title': mq_row[db_entry_to_index_dict['question_description_title'] + 1],
                                'question_description_main': mq_row[db_entry_to_index_dict['question_description_main'] + 1],

                                'mix_answers': mq_row[db_entry_to_index_dict['mix_answers'] + 1],
                                'assignment_mode': mq_row[db_entry_to_index_dict['assignment_mode'] + 1],

                                'definitions_response_1_text':                        mq_row[db_entry_to_index_dict['definitions_response_1_text'] + 1],
                                'definitions_response_1_img_label':                   mq_row[db_entry_to_index_dict['definitions_response_1_img_label'] + 1],
                                'definitions_response_1_img_path':                    mq_row[db_entry_to_index_dict['definitions_response_1_img_path'] + 1],
                                'definitions_response_1_img_string_base64_encoded':   mq_row[db_entry_to_index_dict['definitions_response_1_img_string_base64_encoded'] + 1],

                                'definitions_response_2_text':                        mq_row[db_entry_to_index_dict['definitions_response_2_text'] + 1],
                                'definitions_response_2_img_label':                   mq_row[db_entry_to_index_dict['definitions_response_2_img_label'] + 1],
                                'definitions_response_2_img_path':                    mq_row[db_entry_to_index_dict['definitions_response_2_img_path'] + 1],
                                'definitions_response_2_img_string_base64_encoded':   mq_row[db_entry_to_index_dict['definitions_response_2_img_string_base64_encoded'] + 1],

                                'definitions_response_3_text':                        mq_row[db_entry_to_index_dict['definitions_response_3_text'] + 1],
                                'definitions_response_3_img_label':                   mq_row[db_entry_to_index_dict['definitions_response_3_img_label'] + 1],
                                'definitions_response_3_img_path':                    mq_row[db_entry_to_index_dict['definitions_response_3_img_path'] + 1],
                                'definitions_response_3_img_string_base64_encoded':   mq_row[db_entry_to_index_dict['definitions_response_3_img_string_base64_encoded'] + 1],

                                'definitions_response_4_text':                        mq_row[db_entry_to_index_dict['definitions_response_4_text'] + 1],
                                'definitions_response_4_img_label':                   mq_row[db_entry_to_index_dict['definitions_response_4_img_label'] + 1],
                                'definitions_response_4_img_path':                    mq_row[db_entry_to_index_dict['definitions_response_4_img_path'] + 1],
                                'definitions_response_4_img_string_base64_encoded':   mq_row[db_entry_to_index_dict['definitions_response_4_img_string_base64_encoded'] + 1],

                                'definitions_response_5_text':                        mq_row[db_entry_to_index_dict['definitions_response_5_text'] + 1],
                                'definitions_response_5_img_label':                   mq_row[db_entry_to_index_dict['definitions_response_5_img_label'] + 1],
                                'definitions_response_5_img_path':                    mq_row[db_entry_to_index_dict['definitions_response_5_img_path'] + 1],
                                'definitions_response_5_img_string_base64_encoded':   mq_row[db_entry_to_index_dict['definitions_response_5_img_string_base64_encoded'] + 1],

                                'definitions_response_6_text':                        mq_row[db_entry_to_index_dict['definitions_response_6_text'] + 1],
                                'definitions_response_6_img_label':                   mq_row[db_entry_to_index_dict['definitions_response_6_img_label'] + 1],
                                'definitions_response_6_img_path':                    mq_row[db_entry_to_index_dict['definitions_response_6_img_path'] + 1],
                                'definitions_response_6_img_string_base64_encoded':   mq_row[db_entry_to_index_dict['definitions_response_6_img_string_base64_encoded'] + 1],

                                'definitions_response_7_text':                        mq_row[db_entry_to_index_dict['definitions_response_7_text'] + 1],
                                'definitions_response_7_img_label':                   mq_row[db_entry_to_index_dict['definitions_response_7_img_label'] + 1],
                                'definitions_response_7_img_path':                    mq_row[db_entry_to_index_dict['definitions_response_7_img_path'] + 1],
                                'definitions_response_7_img_string_base64_encoded':   mq_row[db_entry_to_index_dict['definitions_response_7_img_string_base64_encoded'] + 1],

                                'definitions_response_8_text':                        mq_row[db_entry_to_index_dict['definitions_response_8_text'] + 1],
                                'definitions_response_8_img_label':                   mq_row[db_entry_to_index_dict['definitions_response_8_img_label'] + 1],
                                'definitions_response_8_img_path':                    mq_row[db_entry_to_index_dict['definitions_response_8_img_path'] + 1],
                                'definitions_response_8_img_string_base64_encoded':   mq_row[db_entry_to_index_dict['definitions_response_8_img_string_base64_encoded'] + 1],

                                'definitions_response_9_text':                        mq_row[db_entry_to_index_dict['definitions_response_9_text'] + 1],
                                'definitions_response_9_img_label':                   mq_row[db_entry_to_index_dict['definitions_response_9_img_label'] + 1],
                                'definitions_response_9_img_path':                    mq_row[db_entry_to_index_dict['definitions_response_9_img_path'] + 1],
                                'definitions_response_9_img_string_base64_encoded':   mq_row[db_entry_to_index_dict['definitions_response_9_img_string_base64_encoded'] + 1],

                                'definitions_response_10_text':                       mq_row[db_entry_to_index_dict['definitions_response_10_text'] + 1],
                                'definitions_response_10_img_label':                  mq_row[db_entry_to_index_dict['definitions_response_10_img_label'] + 1],
                                'definitions_response_10_img_path':                   mq_row[db_entry_to_index_dict['definitions_response_10_img_path'] + 1],
                                'definitions_response_10_img_string_base64_encoded':  mq_row[db_entry_to_index_dict['definitions_response_10_img_string_base64_encoded'] + 1],

                                'terms_response_1_text':                              mq_row[db_entry_to_index_dict['terms_response_1_text'] + 1],
                                'terms_response_1_img_label':                         mq_row[db_entry_to_index_dict['terms_response_1_img_label'] + 1],
                                'terms_response_1_img_path':                          mq_row[db_entry_to_index_dict['terms_response_1_img_path'] + 1],
                                'terms_response_1_img_string_base64_encoded':         mq_row[db_entry_to_index_dict['terms_response_1_img_string_base64_encoded'] + 1],

                                'terms_response_2_text':                              mq_row[db_entry_to_index_dict['terms_response_2_text'] + 1],
                                'terms_response_2_img_label':                         mq_row[db_entry_to_index_dict['terms_response_2_img_label'] + 1],
                                'terms_response_2_img_path':                          mq_row[db_entry_to_index_dict['terms_response_2_img_path'] + 1],
                                'terms_response_2_img_string_base64_encoded':         mq_row[db_entry_to_index_dict['terms_response_2_img_string_base64_encoded'] + 1],

                                'terms_response_3_text':                              mq_row[db_entry_to_index_dict['terms_response_3_text'] + 1],
                                'terms_response_3_img_label':                         mq_row[db_entry_to_index_dict['terms_response_3_img_label'] + 1],
                                'terms_response_3_img_path':                          mq_row[db_entry_to_index_dict['terms_response_3_img_path'] + 1],
                                'terms_response_3_img_string_base64_encoded':         mq_row[db_entry_to_index_dict['terms_response_3_img_string_base64_encoded'] + 1],

                                'terms_response_4_text':                              mq_row[db_entry_to_index_dict['terms_response_4_text'] + 1],
                                'terms_response_4_img_label':                         mq_row[db_entry_to_index_dict['terms_response_4_img_label'] + 1],
                                'terms_response_4_img_path':                          mq_row[db_entry_to_index_dict['terms_response_4_img_path'] + 1],
                                'terms_response_4_img_string_base64_encoded':         mq_row[db_entry_to_index_dict['terms_response_4_img_string_base64_encoded'] + 1],

                                'terms_response_5_text':                              mq_row[db_entry_to_index_dict['terms_response_5_text'] + 1],
                                'terms_response_5_img_label':                         mq_row[db_entry_to_index_dict['terms_response_5_img_label'] + 1],
                                'terms_response_5_img_path':                          mq_row[db_entry_to_index_dict['terms_response_5_img_path'] + 1],
                                'terms_response_5_img_string_base64_encoded':         mq_row[db_entry_to_index_dict['terms_response_5_img_string_base64_encoded'] + 1],

                                'terms_response_6_text':                              mq_row[db_entry_to_index_dict['terms_response_6_text'] + 1],
                                'terms_response_6_img_label':                         mq_row[db_entry_to_index_dict['terms_response_6_img_label'] + 1],
                                'terms_response_6_img_path':                          mq_row[db_entry_to_index_dict['terms_response_6_img_path'] + 1],
                                'terms_response_6_img_string_base64_encoded':         mq_row[db_entry_to_index_dict['terms_response_6_img_string_base64_encoded'] + 1],

                                'terms_response_7_text':                              mq_row[db_entry_to_index_dict['terms_response_7_text'] + 1],
                                'terms_response_7_img_label':                         mq_row[db_entry_to_index_dict['terms_response_7_img_label'] + 1],
                                'terms_response_7_img_path':                          mq_row[db_entry_to_index_dict['terms_response_7_img_path'] + 1],
                                'terms_response_7_img_string_base64_encoded':         mq_row[db_entry_to_index_dict['terms_response_7_img_string_base64_encoded'] + 1],

                                'terms_response_8_text':                              mq_row[db_entry_to_index_dict['terms_response_8_text'] + 1],
                                'terms_response_8_img_label':                         mq_row[db_entry_to_index_dict['terms_response_8_img_label'] + 1],
                                'terms_response_8_img_path':                          mq_row[db_entry_to_index_dict['terms_response_8_img_path'] + 1],
                                'terms_response_8_img_string_base64_encoded':         mq_row[db_entry_to_index_dict['terms_response_8_img_string_base64_encoded'] + 1],

                                'terms_response_9_text':                              mq_row[db_entry_to_index_dict['terms_response_9_text'] + 1],
                                'terms_response_9_img_label':                         mq_row[db_entry_to_index_dict['terms_response_9_img_label'] + 1],
                                'terms_response_9_img_path':                          mq_row[db_entry_to_index_dict['terms_response_9_img_path'] + 1],
                                'terms_response_9_img_string_base64_encoded':         mq_row[db_entry_to_index_dict['terms_response_9_img_string_base64_encoded'] + 1],

                                'terms_response_10_text':                             mq_row[db_entry_to_index_dict['terms_response_10_text'] + 1],
                                'terms_response_10_img_label':                        mq_row[db_entry_to_index_dict['terms_response_10_img_label'] + 1],
                                'terms_response_10_img_path':                         mq_row[db_entry_to_index_dict['terms_response_10_img_path'] + 1],
                                'terms_response_10_img_string_base64_encoded':        mq_row[db_entry_to_index_dict['terms_response_10_img_string_base64_encoded'] + 1],


                                'assignment_pairs_definition_1':                      mq_row[db_entry_to_index_dict['assignment_pairs_definition_1'] + 1],
                                'assignment_pairs_term_1':                            mq_row[db_entry_to_index_dict['assignment_pairs_term_1'] + 1],
                                'assignment_pairs_1_pts':                             mq_row[db_entry_to_index_dict['assignment_pairs_1_pts'] + 1],

                                'assignment_pairs_definition_2':                      mq_row[db_entry_to_index_dict['assignment_pairs_definition_2'] + 1],
                                'assignment_pairs_term_2':                            mq_row[db_entry_to_index_dict['assignment_pairs_term_2'] + 1],
                                'assignment_pairs_2_pts':                             mq_row[db_entry_to_index_dict['assignment_pairs_2_pts'] + 1],

                                'assignment_pairs_definition_3':                      mq_row[db_entry_to_index_dict['assignment_pairs_definition_3'] + 1],
                                'assignment_pairs_term_3':                            mq_row[db_entry_to_index_dict['assignment_pairs_term_3'] + 1],
                                'assignment_pairs_3_pts':                             mq_row[db_entry_to_index_dict['assignment_pairs_3_pts'] + 1],

                                'assignment_pairs_definition_4':                      mq_row[db_entry_to_index_dict['assignment_pairs_definition_4'] + 1],
                                'assignment_pairs_term_4':                            mq_row[db_entry_to_index_dict['assignment_pairs_term_4'] + 1],
                                'assignment_pairs_4_pts':                             mq_row[db_entry_to_index_dict['assignment_pairs_4_pts'] + 1],

                                'assignment_pairs_definition_5':                      mq_row[db_entry_to_index_dict['assignment_pairs_definition_5'] + 1],
                                'assignment_pairs_term_5':                            mq_row[db_entry_to_index_dict['assignment_pairs_term_5'] + 1],
                                'assignment_pairs_5_pts':                             mq_row[db_entry_to_index_dict['assignment_pairs_5_pts'] + 1],

                                'assignment_pairs_definition_6':                      mq_row[db_entry_to_index_dict['assignment_pairs_definition_6'] + 1],
                                'assignment_pairs_term_6':                            mq_row[db_entry_to_index_dict['assignment_pairs_term_6'] + 1],
                                'assignment_pairs_6_pts':                             mq_row[db_entry_to_index_dict['assignment_pairs_6_pts'] + 1],

                                'assignment_pairs_definition_7':                      mq_row[db_entry_to_index_dict['assignment_pairs_definition_7'] + 1],
                                'assignment_pairs_term_7':                            mq_row[db_entry_to_index_dict['assignment_pairs_term_7'] + 1],
                                'assignment_pairs_7_pts':                             mq_row[db_entry_to_index_dict['assignment_pairs_7_pts'] + 1],

                                'assignment_pairs_definition_8':                      mq_row[db_entry_to_index_dict['assignment_pairs_definition_8'] + 1],
                                'assignment_pairs_term_8':                            mq_row[db_entry_to_index_dict['assignment_pairs_term_8'] + 1],
                                'assignment_pairs_8_pts':                             mq_row[db_entry_to_index_dict['assignment_pairs_8_pts'] + 1],

                                'assignment_pairs_definition_9':                      mq_row[db_entry_to_index_dict['assignment_pairs_definition_9'] + 1],
                                'assignment_pairs_term_9':                            mq_row[db_entry_to_index_dict['assignment_pairs_term_9'] + 1],
                                'assignment_pairs_9_pts':                             mq_row[db_entry_to_index_dict['assignment_pairs_9_pts'] + 1],

                                'assignment_pairs_definition_10':                     mq_row[db_entry_to_index_dict['assignment_pairs_definition_10'] + 1],
                                'assignment_pairs_term_10':                           mq_row[db_entry_to_index_dict['assignment_pairs_term_10'] + 1],
                                'assignment_pairs_10_pts':                            mq_row[db_entry_to_index_dict['assignment_pairs_10_pts'] + 1],


                                'picture_preview_pixel':                              mq_row[db_entry_to_index_dict['picture_preview_pixel'] + 1],

                                'description_img_name_1':                             mq_row[db_entry_to_index_dict['description_img_name_1'] + 1],
                                'description_img_data_1':                             mq_row[db_entry_to_index_dict['description_img_data_1'] + 1],
                                'description_img_path_1':                             mq_row[db_entry_to_index_dict['description_img_path_1'] + 1],

                                'description_img_name_2':                             mq_row[db_entry_to_index_dict['description_img_name_2'] + 1],
                                'description_img_data_2':                             mq_row[db_entry_to_index_dict['description_img_data_2'] + 1],
                                'description_img_path_2':                             mq_row[db_entry_to_index_dict['description_img_path_2'] + 1],

                                'description_img_name_3':                             mq_row[db_entry_to_index_dict['description_img_name_3'] + 1],
                                'description_img_data_3':                             mq_row[db_entry_to_index_dict['description_img_data_3'] + 1],
                                'description_img_path_3':                             mq_row[db_entry_to_index_dict['description_img_path_3'] + 1],


                                'test_time': mq_row[db_entry_to_index_dict['test_time'] + 1],
                                'question_pool_tag': mq_row[db_entry_to_index_dict['question_pool_tag'] + 1],
                                'question_author': mq_row[db_entry_to_index_dict['question_author'] + 1],
                                'oid': mq_row[-1]

                                })

                    conn.commit()

                    self.edited_questions_list.append(mq_row[db_entry_to_index_dict['question_title'] + 1])
                    self.number_of_entries_edited += 1
                else:
                    self.number_of_new_entries_from_excel += 1

                    self.definitions_response_1_img_string_base64_encoded = img_path_to_base64_encoded_string('definitions_response_1_img_label', 'definitions_response_1_img_path', mq_row)
                    self.definitions_response_2_img_string_base64_encoded = img_path_to_base64_encoded_string('definitions_response_2_img_label', 'definitions_response_2_img_path', mq_row)
                    self.definitions_response_3_img_string_base64_encoded = img_path_to_base64_encoded_string('definitions_response_3_img_label', 'definitions_response_3_img_path', mq_row)
                    self.definitions_response_4_img_string_base64_encoded = img_path_to_base64_encoded_string('definitions_response_4_img_label', 'definitions_response_4_img_path', mq_row)
                    self.definitions_response_5_img_string_base64_encoded = img_path_to_base64_encoded_string('definitions_response_5_img_label', 'definitions_response_5_img_path', mq_row)
                    self.definitions_response_6_img_string_base64_encoded = img_path_to_base64_encoded_string('definitions_response_6_img_label', 'definitions_response_6_img_path', mq_row)
                    self.definitions_response_7_img_string_base64_encoded = img_path_to_base64_encoded_string('definitions_response_7_img_label', 'definitions_response_7_img_path', mq_row)
                    self.definitions_response_8_img_string_base64_encoded = img_path_to_base64_encoded_string('definitions_response_8_img_label', 'definitions_response_8_img_path', mq_row)
                    self.definitions_response_9_img_string_base64_encoded = img_path_to_base64_encoded_string('definitions_response_9_img_label', 'definitions_response_9_img_path', mq_row)
                    self.definitions_response_10_img_string_base64_encoded = img_path_to_base64_encoded_string('definitions_response_10_img_label', 'definitions_response_10_img_path', mq_row)

                    self.terms_response_1_img_string_base64_encoded = img_path_to_base64_encoded_string('terms_response_1_img_label', 'terms_response_1_img_path', mq_row)
                    self.terms_response_2_img_string_base64_encoded = img_path_to_base64_encoded_string('terms_response_2_img_label', 'terms_response_2_img_path', mq_row)
                    self.terms_response_3_img_string_base64_encoded = img_path_to_base64_encoded_string('terms_response_3_img_label', 'terms_response_3_img_path', mq_row)
                    self.terms_response_4_img_string_base64_encoded = img_path_to_base64_encoded_string('terms_response_4_img_label', 'terms_response_4_img_path', mq_row)
                    self.terms_response_5_img_string_base64_encoded = img_path_to_base64_encoded_string('terms_response_5_img_label', 'terms_response_5_img_path', mq_row)
                    self.terms_response_6_img_string_base64_encoded = img_path_to_base64_encoded_string('terms_response_6_img_label', 'terms_response_6_img_path', mq_row)
                    self.terms_response_7_img_string_base64_encoded = img_path_to_base64_encoded_string('terms_response_7_img_label', 'terms_response_7_img_path', mq_row)
                    self.terms_response_8_img_string_base64_encoded = img_path_to_base64_encoded_string('terms_response_8_img_label', 'terms_response_8_img_path', mq_row)
                    self.terms_response_9_img_string_base64_encoded = img_path_to_base64_encoded_string('terms_response_9_img_label', 'terms_response_9_img_path', mq_row)
                    self.terms_response_10_img_string_base64_encoded = img_path_to_base64_encoded_string('terms_response_10_img_label', 'terms_response_10_img_path', mq_row)


                    self.mq_description_img_data_1 = Import_Export_Database.excel_import_placeholder_to_data(self, mq_row, self.db_entry_to_index_dict['description_img_data_1'], self.db_entry_to_index_dict['description_img_path_1'])
                    self.mq_description_img_data_2 = Import_Export_Database.excel_import_placeholder_to_data(self, mq_row, self.db_entry_to_index_dict['description_img_data_2'], self.db_entry_to_index_dict['description_img_path_2'])
                    self.mq_description_img_data_3 = Import_Export_Database.excel_import_placeholder_to_data(self, mq_row, self.db_entry_to_index_dict['description_img_data_3'], self.db_entry_to_index_dict['description_img_path_3'])




                    c.execute("INSERT INTO zuordnungsfrage_table VALUES " + self.sql_values_question_marks, (
                       mq_row.question_difficulty,
                       mq_row.question_category,
                       mq_row.question_type,
                       mq_row.question_title,
                       mq_row.question_description_title,
                       mq_row.question_description_main,

                       mq_row.mix_answers,
                       mq_row.assignment_mode,

                       mq_row.definitions_response_1_text,
                       mq_row.definitions_response_1_img_label,
                       mq_row.definitions_response_1_img_path,
                       self.definitions_response_1_img_string_base64_encoded,

                       mq_row.definitions_response_2_text,
                       mq_row.definitions_response_2_img_label,
                       mq_row.definitions_response_2_img_path,
                       self.definitions_response_2_img_string_base64_encoded,

                       mq_row.definitions_response_3_text,
                       mq_row.definitions_response_3_img_label,
                       mq_row.definitions_response_3_img_path,
                       self.definitions_response_3_img_string_base64_encoded,

                       mq_row.definitions_response_4_text,
                       mq_row.definitions_response_4_img_label,
                       mq_row.definitions_response_4_img_path,
                       self.definitions_response_4_img_string_base64_encoded,

                       mq_row.definitions_response_5_text,
                       mq_row.definitions_response_5_img_label,
                       mq_row.definitions_response_5_img_path,
                       self.definitions_response_5_img_string_base64_encoded,

                       mq_row.definitions_response_6_text,
                       mq_row.definitions_response_6_img_label,
                       mq_row.definitions_response_6_img_path,
                       self.definitions_response_6_img_string_base64_encoded,

                       mq_row.definitions_response_7_text,
                       mq_row.definitions_response_7_img_label,
                       mq_row.definitions_response_7_img_path,
                       self.definitions_response_7_img_string_base64_encoded,

                       mq_row.definitions_response_8_text,
                       mq_row.definitions_response_8_img_label,
                       mq_row.definitions_response_8_img_path,
                       self.definitions_response_8_img_string_base64_encoded,

                       mq_row.definitions_response_9_text,
                       mq_row.definitions_response_9_img_label,
                       mq_row.definitions_response_9_img_path,
                       self.definitions_response_9_img_string_base64_encoded,

                       mq_row.definitions_response_10_text,
                       mq_row.definitions_response_10_img_label,
                       mq_row.definitions_response_10_img_path,
                       self.definitions_response_10_img_string_base64_encoded,



                       mq_row.terms_response_1_text,
                       mq_row.terms_response_1_img_label,
                       mq_row.terms_response_1_img_path,
                       self.terms_response_1_img_string_base64_encoded,

                       mq_row.terms_response_2_text,
                       mq_row.terms_response_2_img_label,
                       mq_row.terms_response_2_img_path,
                       self.terms_response_2_img_string_base64_encoded,

                       mq_row.terms_response_3_text,
                       mq_row.terms_response_3_img_label,
                       mq_row.terms_response_3_img_path,
                       self.terms_response_3_img_string_base64_encoded,

                       mq_row.terms_response_4_text,
                       mq_row.terms_response_4_img_label,
                       mq_row.terms_response_4_img_path,
                       self.terms_response_4_img_string_base64_encoded,

                       mq_row.terms_response_5_text,
                       mq_row.terms_response_5_img_label,
                       mq_row.terms_response_5_img_path,
                       self.terms_response_5_img_string_base64_encoded,

                       mq_row.terms_response_6_text,
                       mq_row.terms_response_6_img_label,
                       mq_row.terms_response_6_img_path,
                       self.terms_response_6_img_string_base64_encoded,

                       mq_row.terms_response_7_text,
                       mq_row.terms_response_7_img_label,
                       mq_row.terms_response_7_img_path,
                       self.terms_response_7_img_string_base64_encoded,

                       mq_row.terms_response_8_text,
                       mq_row.terms_response_8_img_label,
                       mq_row.terms_response_8_img_path,
                       self.terms_response_8_img_string_base64_encoded,

                       mq_row.terms_response_9_text,
                       mq_row.terms_response_9_img_label,
                       mq_row.terms_response_9_img_path,
                       self.terms_response_9_img_string_base64_encoded,

                       mq_row.terms_response_10_text,
                       mq_row.terms_response_10_img_label,
                       mq_row.terms_response_10_img_path,
                       self.terms_response_10_img_string_base64_encoded,




                       mq_row.assignment_pairs_definition_1,
                       mq_row.assignment_pairs_term_1,
                       mq_row.assignment_pairs_pts_1,

                       mq_row.assignment_pairs_definition_2,
                       mq_row.assignment_pairs_term_2,
                       mq_row.assignment_pairs_pts_2,

                       mq_row.assignment_pairs_definition_3,
                       mq_row.assignment_pairs_term_3,
                       mq_row.assignment_pairs_pts_3,

                       mq_row.assignment_pairs_definition_4,
                       mq_row.assignment_pairs_term_4,
                       mq_row.assignment_pairs_pts_4,

                       mq_row.assignment_pairs_definition_5,
                       mq_row.assignment_pairs_term_5,
                       mq_row.assignment_pairs_pts_5,

                       mq_row.assignment_pairs_definition_6,
                       mq_row.assignment_pairs_term_6,
                       mq_row.assignment_pairs_pts_6,

                       mq_row.assignment_pairs_definition_7,
                       mq_row.assignment_pairs_term_7,
                       mq_row.assignment_pairs_pts_7,

                       mq_row.assignment_pairs_definition_8,
                       mq_row.assignment_pairs_term_8,
                       mq_row.assignment_pairs_pts_8,

                       mq_row.assignment_pairs_definition_9,
                       mq_row.assignment_pairs_term_9,
                       mq_row.assignment_pairs_pts_9,

                       mq_row.assignment_pairs_definition_10,
                       mq_row.assignment_pairs_term_10,
                       mq_row.assignment_pairs_pts_10,

                       mq_row.picture_preview_pixel,

                       mq_row.description_img_name_1,
                       self.mq_description_img_data_1,
                       mq_row.description_img_path_1,

                       mq_row.description_img_name_2,
                       self.mq_description_img_data_2,
                       mq_row.description_img_path_2,

                       mq_row.description_img_name_3,
                       self.mq_description_img_data_3,
                       mq_row.description_img_path_3,

                       mq_row.test_time,
                       mq_row.var_number,
                       mq_row.res_number,
                       mq_row.question_pool_tag,
                       mq_row.question_author
                    ))

                    conn.commit()

            print("     Datei geladen!")
            print(" ")
            print("MQ_DB-Einträge: ", "NEU: " + str(self.number_of_new_entries_from_excel),
                  " -- EDITIERT: " + str(self.number_of_entries_edited))

            for i in range(len(self.edited_questions_list)):
                print("     Frage editiert: ", self.edited_questions_list[i])

            print(" ")


            conn.close()

            # Bestätigungsfenster für Import
            messagebox.showinfo("Excel-Datei importieren", "Einträge wurden importiert!")

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
            self.description_img_data = ""

        return self.description_img_data


    def excel_export_to_xlsx(self,  project_root_path, db_entry_to_index_dict, database_path, database_name, database_table_name, xlsx_workbook_name, xlsx_worksheet_name):

    ##################

    ##################

        self.xlsx_workbook_name = xlsx_workbook_name
        self.database_path = database_path
        self.database_table_name = database_table_name
        self.xlsx_worksheet_name = xlsx_worksheet_name
        self.project_root_path = project_root_path
        self.db_entry_to_index_dict = db_entry_to_index_dict

        # Abfrage in welchem Format die Datenbank exportiert wrden soll
        # Messagebox liefert ein "Standard" Abfragefenster mit der Möglichkeit "Ja" / "Nein" auszuwählen
        # Die Rückgabewerte dieser Box sind entsprechend "Yes" / "No"
        self.export_filetype_choice = messagebox.askquestion("Datenbank exportieren", "Datenbank als XLSX-Dateiformat exportieren?\n(\"Nein\" exportiert die Datei im ODS-Dateiformat)")





        # Datenbank-Name lautet z.B.: ilias_singlechoice_db.db
        # durch den Zusatz [:-3] werden die letzten 3 Zeichen gelöscht
        self.database_dir_name = str(database_name[:-3])
        self.database_dir_name += "_images"

        #if self.export_filetype_choice == "yes":
        self.orig_workbook_name = self.xlsx_workbook_name
        self.xlsx_workbook_name += ".xlsx"

        self.ods_workbook_name = self.orig_workbook_name
        self.ods_workbook_name += ".ods"

#        else:
#            self.xlsx_workbook_name += ".ods"
        print("________________________________________________")
        print("Datenbank wird exportiert...", end="", flush=True)


        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()
        #query = 'SELECT * FROM {} LIMIT -1 OFFSET 1'.format(self.database_table_name)
        query = 'select * from ' + self.database_table_name
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
                if isinstance(column_data,byteobj.ByteString) == False and len(str(column_data)) > 40 and str(column_data).count(' ') < 3 :

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
                        if self.sc_picture_answer_index <= 10:



                            self.dict_entry_string = 'response_%s_img_label' % (str(self.sc_picture_answer_index))


                            #if str(row[self.db_entry_to_index_dict[self.dict_entry_string]]) != "":

                                #column_data = str(row[self.db_entry_to_index_dict[self.dict_entry_string]])  + " - img_data_string_placeholder"


                            self.sc_picture_answer_index += 1



                    excel_sheet.write(row_index, column_index, column_data, body_cell_format)

                # Bilder für Fragen-Text
                if isinstance(column_data, byteobj.ByteString) == True:
                    column_data = str(row[self.db_entry_to_index_dict['description_img_name_' + str(self.picture_index)]]) + " - img_data_string_placeholder"
                    image_data = row[self.db_entry_to_index_dict['description_img_data_' + str(self.picture_index)]]


                    excel_sheet.write(row_index, column_index, column_data, body_cell_format)
                    #column_index += 1

                    # Hier werden die Bilder (physisch) in die Ordner abgelegt
                    # Die zusätzliche Abfrage ist leider notwendig, da u.U. einfache Strings als 'TRUE' bei der "isinstance(column_data,byteobj.ByteString)" Abfrage eingestuft werden
                    # Diese einfachen Strings können aber natürlich nicht als Bild geschrieben werden
                    if row[self.db_entry_to_index_dict['description_img_data_' + str(self.picture_index)]] != "":
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

        print("     abgeschlossen!")

        print(str(row_index-1) + ' Zeilen exportiert --->  ' + excel.filename)
        print("________________________________________________")



        # Exportiert die Datenbank als ".xlsx" und konvertiert die Datei nach ".ods"
        if self.export_filetype_choice == "no":
            dataframe = pd.read_excel(os.path.normpath(os.path.join(self.project_root_path, "Datenbank_Export", self.xlsx_workbook_name)))
            with ExcelWriter(os.path.normpath(os.path.join(self.project_root_path, "Datenbank_Export", self.ods_workbook_name)).format('ods')) as writer:
                dataframe.to_excel(writer, engine='ods')

        messagebox.showinfo("Datenbank exportieren", "Datenbank wurde exportiert!")






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

            # Alle Fragen in der DB löschen - popup
            # showinfo, showwarning, showerror, askquestion, askokcancel, askyesno
            self.response_delete_all = messagebox.askquestion("Alle Einträge in der DB löschen", "Sollen ALLE Einträge aus der DB gelöscht werden?")

            if self.response_delete_all == "yes":

                # ---- War als Backup gedacht, bevor ein Abfrage-Fenster integriert wurde
                #now = datetime.now()  # current date and time
                #date_time = now.strftime("%d.%m.%Y_%Hh-%Mm")
                #actual_time = str(date_time)
                #self.backup_table_name = "BACKUP_Export_from_SQL__" + str(actual_time)
                #Import_Export_Database.excel_export_to_xlsx(self,  project_root_path, db_entry_to_index_dict, database_path, database_name, database_table_name, self.backup_table_name + " - " + xlsx_workbook_name, xlsx_worksheet_name)

                c.execute("SELECT *, oid FROM " + str(self.database_db_table_name))
                records = c.fetchall()
                for record in records:
                    self.modul_delete_all_list.append(int(record[len(record) - 1]))

                # Der Eintrag mit ID "1" dient als Vorlage für die Datenbank
                #for i in range(len(self.modul_delete_all_list)):
                #    if self.modul_delete_all_list[i] == 1:
                #        self.modul_delete_index = i

                # .pop(index) löscht den DB Eintrag mit dem DB_Index
                #self.modul_delete_all_list.pop(self.modul_delete_index)


                for x in range(len(self.modul_delete_all_list)):
                    c.execute("DELETE from %s WHERE oid = %s " % (self.database_db_table_name, str(self.modul_delete_all_list[x])))
                print(self.question_type.upper() + ":Datenbank gelöscht!")

            else:
                print("Vorgang abgebrochen")

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
