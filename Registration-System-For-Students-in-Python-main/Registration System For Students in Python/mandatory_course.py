from course import Course
import course_section
from semester import Semester
import logging



class MandatoryCourse(Course):
    
    def __init__(self, course_code, semester_num, credit, theoretical, practical, prerequisites, quota, reg_sys):
        super().__init__(course_code, quota, credit, theoretical, practical, reg_sys)
        self.prerequisites = prerequisites
        self.semester_num = semester_num
        self.set_semester()
        self.course_section = course_section.CourseSection(self)
        self.non_registered_prereq = set()
        
    def is_elligible_past_course(self, student) -> bool:
        has_passed_prereq = student.transcript.has_passed_courses(self.prerequisites)
        semester_condition = student.semester_num > self.semester_num
        
        return super().is_elligible_past_course(student) and has_passed_prereq and semester_condition
    
    def is_offerable_for_student(self, student):
        stu_transcript = student.transcript
        has_passed_this = stu_transcript.has_passed_course(self)
        is_same_semester = self.semester_num % 2  == student.semester_num % 2
        course_semester_le = student.semester_num >= self.semester_num ##course semester is less or equal to stu semester
        
        return not has_passed_this and course_semester_le and is_same_semester
            
    
    def when_requested(self, student):
        if not student.transcript.has_passed_courses(self.prerequisites):
            logging.warning(student.student_id.__str__() + " >> The system didn't allow " + self.__str__()  
                            +  " because student failed prerequisites -> " 
                            + ", ".join([prereq.__str__() 
                                    for prereq in self.prerequisites 
                                    if not student.transcript.has_passed_course(prereq)]))
            self.non_registered_prereq.add(student)
            return False
        
        if not super().when_requested(student):
            return False
        if not self.course_section.add_student(student):
            return False
        return True
    
    def set_semester(self):
        if self.semester_num % 2 == 0:
            self.semester = Semester.SPRING
        elif self.semester_num % 2 == 1:
            self.semester = Semester.FALL
        elif self.semester_num % 2 == 0.5:
            self.semester = Semester.SUMMER
        else:
            raise Exception("Incorrect Semester for Mandatory Course!")      