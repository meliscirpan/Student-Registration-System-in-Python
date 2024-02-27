from abc import abstractmethod
from course import Course
import course_section


class ElectiveCourse(Course):
    
    
    def __init__(self, course_code, quota, credit, theoretical, practical, semesters, reg_sys):
        super().__init__(course_code, quota, credit, theoretical, practical, reg_sys)
        self.semesters = semesters
        
        self.course_section = course_section.CourseSection(self)
        
        
    def when_requested(self, student):
        if not super().when_requested(student):
            self.when_rejected(student)
            return False
        
        if not self.course_section.add_student(student):
            self.when_rejected(student)
            return False
        
        return True
    
    @abstractmethod
    def when_rejected(self, student):
        pass
    
    @abstractmethod
    def get_random_elective():
        pass