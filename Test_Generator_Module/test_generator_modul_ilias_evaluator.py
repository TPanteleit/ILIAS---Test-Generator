"""
********************************************
test_generator_modul_ilias_evaluator.py
@digitalfellowship - Stand 07/2022
Autor: Tobias Panteleit
********************************************


"""


import sqlite3
import os
import shutil

from Test_Generator_Module import test_generator_modul_ilias_import_test_datei
from Test_Generator_Module import test_generator_modul_datenbanken_erstellen


class ILIAS_Evaluator:
    def __init__(self, project_root_path):

        # Pfade
        self.project_root_path = project_root_path
        self.ff_database_orig_path = os.path.normpath(os.path.join(self.project_root_path, "Test_Generator_Datenbanken", "ilias_formelfrage_db.db"))
        self.ff_database_temp_path = os.path.normpath(os.path.join(self.project_root_path, "ff_db_temp.db"))

        self.sc_database_orig_path = os.path.normpath(os.path.join(self.project_root_path, "Test_Generator_Datenbanken", "ilias_singlechoice_db.db"))
        self.sc_database_temp_path = os.path.normpath(os.path.join(self.project_root_path, "sc_db_temp.db"))

        self.mc_database_orig_path = os.path.normpath(os.path.join(self.project_root_path, "Test_Generator_Datenbanken", "ilias_multiplechoice_db.db"))
        self.mc_database_temp_path = os.path.normpath(os.path.join(self.project_root_path, "mc_db_temp.db"))

        self.mq_database_orig_path = os.path.normpath(os.path.join(self.project_root_path, "Test_Generator_Datenbanken", "ilias_zuordnungsfrage_db.db"))
        self.mq_database_temp_path = os.path.normpath(os.path.join(self.project_root_path, "mq_db_temp.db"))

        # Weitere Zuweisungen
        self.ilias_evaluator_flag = 1

        shutil.copyfile(self.ff_database_orig_path, self.ff_database_temp_path)
        shutil.copyfile(self.sc_database_orig_path, self.sc_database_temp_path)
        shutil.copyfile(self.mc_database_orig_path, self.mc_database_temp_path)
        shutil.copyfile(self.mq_database_orig_path, self.mq_database_temp_path)

        ILIAS_Evaluator.clear_db(self, self.ff_database_temp_path, "formelfrage_table")
        ILIAS_Evaluator.clear_db(self, self.sc_database_temp_path, "singlechoice_table")
        ILIAS_Evaluator.clear_db(self, self.mc_database_temp_path, "multiplechoice_table")
        ILIAS_Evaluator.clear_db(self, self.mq_database_temp_path, "zuordnungsfrage_table")


        # Testdatei importieren
        self.selected_tst_path = test_generator_modul_ilias_import_test_datei.Import_ILIAS_Datei_in_DB.__init__(self, self.project_root_path, 1)

        self.database_path_collection = [self.ff_database_temp_path, self.sc_database_temp_path, self.mc_database_temp_path, self.mq_database_temp_path]

        self.database_collection = ["ilias_formelfrage_db.db", "ilias_singlechoice_db.db", "ilias_multiplechoice_db.db", "ilias_zuordnungsfrage_db.db"]
        self.database_table_collection = ["formelfrage_table", "singlechoice_table", "multiplechoice_table", "zuordnungsfrage_table"]
        self.xlsx_workbook_name_collection = ["Formelfrage_DB_export_file", "SingleChoice_DB_export_file", "MultipleChoice_DB_export_file", "Zuordnungsfrage_DB_export_file"]
        self.xlsx_worksheet_name_collection = ["Formelfrage - Database", "SingleChoice - Database", "MultipleChoice - Database", "Zuordnungsfrage - Database"]


        # Daten aus temp DB exportieren
        for i in range(len(self.database_path_collection)):


            self.db_entry_to_index_dict = ILIAS_Evaluator.create_dict(self, self.database_path_collection[i], self.database_table_collection[i])

            test_generator_modul_datenbanken_erstellen.Import_Export_Database.excel_export_to_xlsx(self,
                                                                                               self.project_root_path,
                                                                                               self.db_entry_to_index_dict,
                                                                                               self.database_path_collection[i],
                                                                                               self.database_collection[i],
                                                                                               self.database_table_collection[i],
                                                                                               self.xlsx_workbook_name_collection[i],
                                                                                               self.xlsx_worksheet_name_collection[i],
                                                                                               self.ilias_evaluator_flag,
                                                                                               self.selected_tst_path)
            #print("Datenbank exportiert --> " + self.xlsx_worksheet_name_collection[i])

        # Temp Datenbanken wieder entfernen
        ILIAS_Evaluator.delete_temp_db(self, self.ff_database_temp_path)
        ILIAS_Evaluator.delete_temp_db(self, self.sc_database_temp_path)
        ILIAS_Evaluator.delete_temp_db(self, self.mc_database_temp_path)
        ILIAS_Evaluator.delete_temp_db(self, self.mq_database_temp_path)

    def clear_db(self, db_temp_path, table_name):

        self.db_temp_path = db_temp_path
        self.table_name  = table_name

        # Create a database or connect to one
        conn = sqlite3.connect(self.db_temp_path)

        # Create cursor
        c = conn.cursor()

        # Alle vorhandenen Daten in dieser "temp" Datenbank löschen
        c.execute('DELETE FROM ' + self.table_name)

        conn.commit()

        print("all Data from " + self.table_name +  " cleared!")


    def delete_temp_db(self, db_temp_path):
        self.db_temp_path = db_temp_path

        if os.path.exists(db_temp_path):
            os.remove(db_temp_path)
        else:
            print("The file does not exist")

    def create_dict(self, database_path, database_table):
        ###################### DATENBANK ENTRIES UND INDEX DICT ERSTELLEN  ###################

        self.database_path = database_path
        self.database_table = database_table

        # Dictionary aus zwei Listen erstellen
        self.db_find_entries = []
        self.db_find_indexes = []
        self.db_column_names_list = []

        connect = sqlite3.connect(self.database_path)
        cursor = connect.execute('select * from ' + self.database_table)

        # Durch list(map(lambdax: x[0])) werden die Spaltennamen aus der DB ausgelesen
        self.db_column_names_list = list(map(lambda x: x[0], cursor.description))
        self.db_column_names_string = ', :'.join(self.db_column_names_list)
        self.db_column_names_string = ":" + self.db_column_names_string

        for i in range(len(self.db_column_names_list)):
            self.db_find_indexes.append(i)

        self.db_entry_to_index_dict = dict(zip((self.db_column_names_list), (self.db_find_indexes)))

        connect.commit()
        connect.close()

        return self.db_entry_to_index_dict