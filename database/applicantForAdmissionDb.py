create_table_applicantForAdmission = "CREATE TABLE Applicants(" \
                                     "id INT AUTO_INCREMENT PRIMARY KEY," \
                                     "name VARCHAR(80) NOT NULL," \
                                     "surname VARCHAR(80) NOT NULL," \
                                     "patronymic VARCHAR(80) NOT NULL," \
                                     "gender INT NOT NULL," \
                                     "chatId BIGINT NOT NULL," \
                                     "phoneNum VARCHAR(20) NOT NULL," \
                                     "age INT NOT NULL," \
                                     "elective_id INT," \
                                     "FOREIGN KEY (elective_id) REFERENCES Electives(id)" \
                                   ")"