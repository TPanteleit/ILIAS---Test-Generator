import sqlite3
import os



class CreateDatabases:

    def __init__(self, project_root_path):
        self.project_root_path = project_root_path
        self.database_formelfrage_exists = os.path.exists(os.path.normpath(os.path.join(self.project_root_path, "ilias_questions_db.db")))
        self.database_singlechoice_exists = os.path.exists(os.path.normpath(os.path.join(self.project_root_path, "ilias_singlechoice_db.db")))
        self.database_test_settings_profiles_exists = os.path.exists(os.path.normpath(os.path.join(self.project_root_path, "test_settings_profiles_db.db")))

        print("##    Datenbank -> Formelfrage:                        " + str(self.database_formelfrage_exists))
        print("##    Datenbank -> SingleChoice:                       " + str(self.database_singlechoice_exists))
        print("##    Datenbank -> Test-Einstellungen_Profile:         " + str(self.database_test_settings_profiles_exists))
        print("\n")

    def create_database_formelfrage(self):
        if self.database_formelfrage_exists != True:

            try:
                # Create a database or connect to one
                conn = sqlite3.connect('ilias_questions_db.db')

                # Create cursor
                c = conn.cursor()

                # Create table
                c.execute("""CREATE TABLE IF NOT EXISTS my_table (
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
                        img_name text,
                        img_data blop,
                        test_time text,
                        var_number int,
                        res_number int,
                        question_pool_tag text
                        )""")


                # Commit Changes
                conn.commit()

                # Close Connection
                conn.close()

                print("Formelfrage Datenbank erstellt!")

            except:
                print("Datenbank \"Formelfrage\" bereits vorhanden!")


    def create_database_singlechoice(self):
        if self.database_singlechoice_exists != True:
            try:
                # Create a database or connect to one
                conn = sqlite3.connect('ilias_singlechoice_db.db')

                # Create cursor
                c = conn.cursor()

                # Create table
                c.execute("""CREATE TABLE IF NOT EXISTS my_table (
                        question_difficulty text,
                        question_category text,
                        question_type text,
                        question_title text,
                        question_description_title text,
                        question_description_main text,
                        response_1_text text,
                        response_2_text text,
                        response_3_text text,
                        response_4_text text,
                        response_5_text text,
                        response_6_text text,
                        response_7_text text,
                        response_8_text text,
                        response_9_text text,
                        response_10_text text,
                        respone_1_pts int,
                        respone_2_pts int,
                        respone_3_pts int,
                        respone_4_pts int,
                        respone_5_pts int,
                        respone_6_pts int,
                        respone_7_pts int,
                        respone_8_pts int,
                        respone_9_pts int,
                        respone_10_pts int,
                        response_1_img_label text,
                        response_2_img_label text,
                        response_3_img_label text,
                        response_4_img_label text,
                        response_5_img_label text,
                        response_6_img_label text,
                        response_7_img_label text,
                        response_8_img_label text,
                        response_9_img_label text,
                        response_10_img_label text,
                        response_1_img_string_base64_encoded text,
                        response_2_img_string_base64_encoded text,
                        response_3_img_string_base64_encoded text,
                        response_4_img_string_base64_encoded text,
                        response_5_img_string_base64_encoded text,
                        response_6_img_string_base64_encoded text,
                        response_7_img_string_base64_encoded text,
                        response_8_img_string_base64_encoded text,
                        response_9_img_string_base64_encoded text,
                        response_10_img_string_base64_encoded text,
                        description_img_name text,
                        description_img_data blop,
                        test_time text,
                        var_number int,
                        res_number int,
                        question_pool_tag text
                        )""")

                # Commit Changes
                conn.commit()

                # Close Connection
                conn.close()

                print("SingleChoice Datenbank erstellt!")

            except:
                print("Datenbank \"SingleChoice\" bereits vorhanden!")


    def create_database_test_settings_profiles(self):
        if self.database_test_settings_profiles_exists != True:
            try:
                # Create a database or connect to one
                conn = sqlite3.connect('test_settings_profiles_db.db')

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