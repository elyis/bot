import logging

from mysql.connector import connect, Error

# database
from database.ElectivesDb import create_table_electives
from database.LearnersDb import create_table_learner
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
                cursor.execute(insert_learners)
                # cursor.execute(create_table_electives)
                # cursor.execute(create_table_learner)
                # cursor.execute(inserts_electives)
                connection.commit()
    except Error as e:
        print(e)
