class Advisor(object):
    
    def __init__(self, name: str):
        self.name = name
    
    
    def approve_course_section(self, student, course_section):
        course = course_section.course
        course.when_requested(student)
        
        
        