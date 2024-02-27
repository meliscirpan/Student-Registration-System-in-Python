import random
from elective_course import ElectiveCourse
import logging


class TechnicalElectiveCourse(ElectiveCourse):
    
    
    def __init__(self, course_code, quota, credit, theoretical, practical, semesters, reg_sys, required_credits, prereqs):
        super().__init__(course_code, quota, credit, theoretical, practical, semesters, reg_sys)
        self.required_credits = required_credits
        self.prereqs = prereqs
        self.non_registered_credit = set()
        
        
    def is_elligible_past_course(self, student):
        has_passed_prereq = student.transcript.has_passed_courses(self.prerequisites)
        return super().is_elligible_past_course(student) and has_passed_prereq and self.check_credit_condition(student)
    
    def when_requested(self, student):
        if not self.check_credit_condition(student):
            logging.warning(student.student_id.__str__() + " >> The system didn't allow "
                            + self.__str__() + " because Student completed credits is less than " 
                            + str(self.required_credits))
            self.non_registered_credit.add(student)
            return False
        
        if not student.transcript.has_passed_courses(self.prereqs):
            logging.warning(student.student_id.__str__() + " >> The system didn't allow " + self.__str__()  
                            +  " because student failed prerequisites -> " 
                            + ", ".join([prereq.__str__() 
                                    for prereq in self.prereqs 
                                    if not student.transcript.has_passed_course(prereq)]))
            #self.non_registered_prereq.add(student)
            return False
        
        return super().when_requested(student)
        
    
    def when_rejected(self, student):
        if self.reg_sys.is_there_empty_te_section():
            stu_advisor = student.advisor
            stu_advisor.approve_course_section(student, self.get_random_elective().course_section)
        else:
            pass
        
    def get_random_elective(self):
         courses = self.reg_sys.tech_elective_courses
         return random.choice(courses)
        
    
    def check_credit_condition(self, student):
        return student.transcript.get_completed_credits() >= self.required_credits
    
    def __str__(self):
        return super().__str__() + "(TE)"