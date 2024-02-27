import random
from grade import Grade


class Transcript(object):

    def __init__(self):
        self.current_courses = [] #list of current courses
        self.grades = [] #list of grades

    def get_completed_credits(self):
        passed_courses = self.get_passed_courses()
        return sum(course.credit for course in passed_courses)

    def get_passed_courses(self):
        return [grade.course for grade in self.grades if grade.is_passed()]

    def has_passed_course(self, course):
        if course is None:
            return True
        return course in self.get_passed_courses()

    def has_passed_courses(self, courses):
        if None in courses:
            return True
        
        return all((self.has_passed_course(course) for course in courses))
    
    def add_past_course(self, pass_prob, course):
        if random.random() < pass_prob:
            self.add_passed_course(course)
        else:
            self.add_failed_course(course)

    def add_passed_course(self, course):
        grade = random.randint(50, 100)
        self.grades.append(Grade(course, grade))

    def add_failed_course(self, course):
        grade = random.randint(0, 49)
        self.grades.append(Grade(course, grade))

    def as_dict(self):
        transcript_dict = {}
        
        transcript_dict["Past Courses"] = []
        for grade in self.grades:
            past_course_dict = {}
            past_course_dict["Course Code"] =  grade.course.__str__()
            past_course_dict["Integer Grade"] = grade.int_grade
            past_course_dict["Letter Grade"] = grade.letter_grade
            
            transcript_dict["Past Courses"].append(past_course_dict)

        transcript_dict["Current Courses"] = []
        for course in self.current_courses:
            curr_course_dict = {}
            curr_course_dict["Course Code"] = course.__str__()
            
            transcript_dict["Current Courses"].append(curr_course_dict)

        return transcript_dict
