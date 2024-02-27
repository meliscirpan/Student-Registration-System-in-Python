import random
import logging
import mandatory_course

from schedule import Schedule

class CourseSection(object):
    
    def __init__(self, course):
        self.course = course
        self.course_program = [[0] * Schedule.DAYS for _ in range(Schedule.HOURS)]
        self.students = []
        self.set_course_program()
        
    def set_course_program(self):
        section_hours = self.course.total_hours()
        
        x = 0
        while x < section_hours:
            rand_hour = random.randint(0, Schedule.HOURS - 1)
            rand_day = random.randint(0, Schedule.DAYS - 1)
            
            if self.course_program[rand_hour][rand_day] == 0 and not self.collides_with_same_semester(rand_hour, rand_day):
                self.course_program[rand_hour][rand_day] = 1
            else:
                x -= 1
            x += 1
                 
    
    def add_student(self, student):
        if not self.is_full():
            self.students.append(student)
            student.add_to_current_courses(self)
            return True
        else:
            logging.warning(student.student_id.__str__() + " >> The system didn't allow " 
                            + self.course.__str__() + " because course section is full.")
            return False
                
                
    def collides_with_same_semester(self, rand_hour, rand_day):
        """Checks if there is collision between same semester mandatory courses and returns True
        if there is at least one hour collision"""
        
        if not isinstance(self.course, mandatory_course.MandatoryCourse):
            return False
        
        mandatory_courses = self.course.reg_sys.mandatory_courses
        
        return any((self.course.semester_num == c.semester_num and  c.course_section.course_program[rand_hour][rand_day] == 1 
                   for c in mandatory_courses))
        
    
    def is_full(self):
        return len(self.students) >= self.course.quota