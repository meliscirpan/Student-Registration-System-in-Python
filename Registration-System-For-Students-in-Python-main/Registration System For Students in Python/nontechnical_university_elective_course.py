import random
from elective_course import ElectiveCourse


class NonTechnicalUniversityElectiveCourse(ElectiveCourse):
    
    def __init__(self, course_code, quota, credit, theoretical, practical, semesters, reg_sys):
        super().__init__(course_code, quota, credit, theoretical, practical, semesters, reg_sys)
        
        
    
    def when_rejected(self, student):
        if self.reg_sys.is_there_empty_nte_section():
            stu_advisor = student.advisor
            stu_advisor.approve_course_section(student, self.get_random_elective().course_section)
        else:
            pass
        
    def get_random_elective(self):
         courses = self.reg_sys.non_tech_elective_courses
         return random.choice(courses)
     
     
    def __str__(self):
        return super().__str__() + "(NTE/UE)"