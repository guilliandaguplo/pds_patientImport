class Job:
    def __init__(self, visit_date, resident, consultant, location, last_name, first_name, age, sex, *args):
        self.visit_date = visit_date
        self.resident = resident
        temp_consultant = str(consultant).lower()
        temp_consultant = temp_consultant[:temp_consultant.find(',')]
        self.consultant = temp_consultant
        self.location = location
        self.last_name = last_name
        self.first_name = first_name
        self.sex = sex
        self.age = age
        self.diagnosis = list(args)
    
    def __repr__(self) -> str:
        return f"({self.sex}){self.last_name}, {self.first_name} ({self.visit_date.strftime('%b %d %Y')})\n"

        