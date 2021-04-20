import sqlite3
from DB_creator_testbed import generate_db

old_dbname = 'generaldb.db'
db = generate_db(old_dbname)


mydb = sqlite3.connect(old_dbname)
cursor = mydb.cursor()
table_list = ['formelfrage', 'singlechoice', 'multiplechoice', 'zuordnungsfrage']
#for table in table_list:  # Temporäre Datenbank wird gelöscht
    #cursor.execute("DELETE  FROM " + table + "")
Type = "multiplechoice"
# for i in range(10):
#     Title = "Title:{}" .format(i)
#
#     print(Title)
#     cursor.execute("INSERT INTO multiplechoice (question_title) VALUES (:Titel)",
#                                 {'Titel': Title})
#     mydb.commit()
#     cursor.execute("UPDATE multiplechoice SET 'question_type' = :Value WHERE question_title = '" +
#                     Title + "' ", {'Value': Type})
#     mydb.commit()
# Type = "singlechoice"
# for i in range(10):
#     Title = "Title:{}" .format(i+10)
#
#     print(Title)
#     cursor.execute("INSERT INTO singlechoice (question_title) VALUES (:Titel)",
#                                 {'Titel': Title})
#     cursor.execute("UPDATE singlechoice SET 'question_type' = :Value WHERE question_title = '" +
#                     Title + "' ", {'Value': Type})
# mydb.commit()
#
# Type = "zuordnungsfrage"
# for i in range(10):
#     Title = "Title:{}" .format(i+20)
#
#     print(Title)
#     cursor.execute("INSERT INTO zuordnungsfrage (question_title) VALUES (:Titel)",
#                                 {'Titel': Title})
#     cursor.execute("UPDATE zuordnungsfrage SET 'question_type' = :Value WHERE question_title = '" +
#                     Title + "' ", {'Value': Type})
# mydb.commit()