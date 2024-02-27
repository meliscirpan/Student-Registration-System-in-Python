from abc import ABC
import logging


class Course(ABC):
    
    def __init__(self, course_code, quota, credit, theoretical, practical, reg_sys):
        self.course_code = course_code
        self.quota = quota
        self.credit = credit
        self.theoretical = theoretical
        self.practical = practical
        self.reg_sys = reg_sys
        self.course_section = None
        self.non_registered_collision = set()
        self.non_registered_quota = set()
        
        
    def is_elligible_past_course(self, student):
        stu_transcript = student.transcript
        return not stu_transcript.has_passed_course(self) ##If student hasn't passed this course yet
    
    
    def when_requested(self, student):
        collided_sections = student.schedule.collided_sections(self.course_section)
        
        if student.schedule.is_collision(self.course_section):
            logging.warning(student.student_id.__str__() + " >> Advisor didn't approve " 
                            + self.__str__() + " because of more than one hour collision with " 
                            + ", ".join([cs.course.__str__() for cs in collided_sections]) 
                            +  " in schedule")
            self.non_registered_collision.add(student)
            return False
        return True


    def total_hours(self):
        return self.theoretical + self.practical
    
    
    
    def __str__(self):
        return self.course_code
        
    
    