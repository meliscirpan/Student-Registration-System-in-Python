from advisor import Advisor
from semester import Semester
from student_id import StudentId
from transcript import Transcript
from schedule import Schedule
from advisor import Advisor


class Student(object):
    
    
    def __init__(self, name, current_year, registration_order, registration_system):
        self.name = name
        self.current_year = current_year
        self.registration_order = registration_order
        self.registration_system = registration_system
        self.transcript = Transcript()
        self.student_id = StudentId(registration_order, current_year)
        self.set_semester_num()
        self.schedule = Schedule()
        self.advisor = None
        
    def add_to_current_courses(self, course_section):
        """Adds a new current course for the student"""
        self.schedule.add_to_program(course_section)
        self.transcript.current_courses.append(course_section.course) ## append the course, which course section is based on
        
    def request_course_section(self, course_section):
        self.advisor.approve_course_section(self, course_section)
        
    def request_courses(self):
        self.request_mandatory_courses()
        self.request_elective_courses()
        
    def request_mandatory_courses(self):
        offered_course_secs = self.registration_system.get_offered_mandatories(self)
        for course_sec in offered_course_secs:
            self.request_course_section(course_sec)
            
    def request_elective_courses(self):
        offered_course_secs = self.registration_system.get_offered_electives(self)
        
        for course_section in offered_course_secs:
            self.request_course_section(course_section)
            
    def get_num_of_past_electives(self, semester_nums):
        count = 0
        for i in semester_nums:
            if i < self.semester_num:
                count += 1
        return count
        
        
    def set_semester_num(self):
        if self.registration_system.semester == Semester.FALL:
            self.semester_num = self.current_year * 2 - 1
        elif self.registration_system.semester == Semester.SPRING:
            self.semester_num = self.current_year * 2
        else:
            raise Exception("Invalid Semester Number for student")
        
    def as_dict(self):
        stu_dict = {}
        stu_dict["Student Name"] = self.name
        stu_dict["Advisor Name"] = self.advisor.name
        stu_dict["Current Semester"] = self.semester_num
        stu_dict["Student Id"] = self.student_id.__str__()
        stu_dict["Completed Credits"] = self.transcript.get_completed_credits()
        stu_dict["Transcript"] = self.transcript.as_dict()

        return stu_dict