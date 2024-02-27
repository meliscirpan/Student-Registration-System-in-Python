from mandatory_course import MandatoryCourse
import logging 


class FinalProjectMandatoryCourse(MandatoryCourse):
    
    def __init__(self, course_code, semester_num, credit, theoretical, 
                 practical, prerequisites, quota, req_credits, reg_sys):
        super().__init__(course_code, semester_num, credit, theoretical, practical, prerequisites, quota, reg_sys)
        self.req_credits = req_credits
        self.non_registered_credit = set()
        
    
    def is_elligible_past_course(self, student) -> bool:
        return super().is_elligible_past_course(student) and self.check_req_credits(student)
    
    def when_requested(self, student):
        if not self.check_req_credits(student):
            logging.warning(student.student_id.__str__() + " >> The system didn't allow " 
                            + self.__str__() + " because student completed credits is less than " 
                            + str(self.req_credits))
            self.non_registered_credit.add(student)
            return False
        if not super().when_requested(student):
            return False
        
        return True
    
    
    def check_req_credits(self, student):
        stu_transcript = student.transcript
        return stu_transcript.get_completed_credits() >= self.req_credits
    
    
    def __str__(self):
        return super().__str__() + "(Final Project)"
    
    