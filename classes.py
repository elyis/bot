# gender : 0 - парень, 1 - девушка

class newLearners:
    def __init__(self):
        self.name = ""
        self.surname = ""
        self.patronymic = ""
        self.age = 0
        self.phoneNum = ""
        self.elective = ""
        self.gender = 0

    def setFullname(self, fullname):
        self.name = fullname[1]
        self.surname = fullname[0]
        self.patronymic = fullname[2]


class newElective:
    def __init__(self):
        self.name = ""
        self.description = ""
        self.init_age = 0
        self.final_age = 0
        self.total_seats = 0
