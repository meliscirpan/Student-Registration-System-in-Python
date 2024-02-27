class StudentId(object):
    
    dep_code = "1501"
    
    def __init__(self, registration_order, current_year):
        self.registration_order = registration_order
        self.current_year = current_year
        self.set_student_id()
        

    def set_student_id(self):
        self.student_id = self.dep_code + self.get_year_string() + self.get_registration_string()
        
    def get_year_string(self):
        id_year = (2021 - self.current_year) % 100
        return str(id_year) 
        
    def get_registration_string(self):
        return f"{self.registration_order:03}"
    
    def __str__(self) -> str:
        return self.student_id