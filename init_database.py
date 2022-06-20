import logging

from mysql.connector import connect, Error

# database
from database.ElectivesDb import create_table_electives
from database.LearnersDb import create_table_learner
from database.applicantForAdmissionDb import create_table_applicantForAdmission
from static_data.Electives import inserts_electives
from static_data.Learners import insert_learners


def init_database():
    try:
        with connect(
                host="localhost",
                user="root",
                password="root",
                database="it_cub"
        ) as connection:

            with connection.cursor() as cursor:
                cursor.execute(create_table_electives)
                cursor.execute(create_table_learner)
                cursor.execute(create_table_applicantForAdmission)
                cursor.execute(inserts_electives)
                cursor.execute(insert_learners)
                connection.commit()
    except Error as e:
        print(e)
