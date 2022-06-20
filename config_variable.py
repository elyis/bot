from classes import newLearners, newElective

TOKEN = '5378657511:AAGBXSLkAZA-AJFD6tp78PLiMfIx1Hfc5MY'

categoriesSuitableForStudentByAge = list()
new_learner = {}
new_elective = newElective()

admin_id = 5329451369

#Состояния для подачи заявки
AGE, ELECTIVE, FULLNAME, GENDER, NUMPHONE, RESULT = range(6)

#Состояния для удаления поступающего/электива
CHOOSE_RM, DISTRIBUTOR, REMOVE_MORE, REMOVE_ELECTIVE = range(4)

#Состояния для принятия/отклонения заявок поступающих
APPLICANTS_MENU, ACCEPT_MENU = range(2)

#Состояния для добавления учащихся/электива
ADD_ELECTIVE_NAME, ADD_ELECTIVE_DESCRIPTION, ADD_ELECTIVE_AGE_LIMITS, ADD_ELECTIVE_TOTAL_SEATS, ADD_ELECTIVE = range(5)

# bd
host = "localhost"
user = "root"
password = "root"
db = "it_cub"
