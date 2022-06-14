create_table_learner = "CREATE TABLE Learners(" \
                           "id INT AUTO_INCREMENT PRIMARY KEY," \
                           "name VARCHAR(80) NOT NULL," \
                           "surname VARCHAR(80) NOT NULL," \
                           "patronymic VARCHAR(80) NOT NULL," \
                           "gender INT NOT NULL," \
                           "phone_number VARCHAR(13)," \
                           "elective_id INT," \
                           "FOREIGN KEY (elective_id) REFERENCES Electives(id)" \
                       ")"