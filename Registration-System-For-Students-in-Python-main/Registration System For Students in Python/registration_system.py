import json
import os
import random
from advisor import Advisor
from faculty_technical_elective_course import FacultyTechnicalElectiveCourse
import final_project_mandatory_course
from mandatory_course import MandatoryCourse
from nontechnical_university_elective_course import NonTechnicalUniversityElectiveCourse
from student import Student
from semester import Semester
from technical_elective_course import TechnicalElectiveCourse
import logging


class RegistrationSystem(object):

    def __init__(self):
        self.data = {}
        self.read_data()
        self.set_semester()
        self.total_students = [0] * 4
        self.names = []
        self.surnames = []
        self.advisors = []
        self.students = []
        self.mandatory_courses = []
        self.final_courses = []  # Stores final project courses
        self.non_tech_elective_courses = []
        self.tech_elective_courses = []
        self.fac_tech_elective_courses = []

    def start_simulation(self):
        self.read_names()
        self.init_advisors()
        self.init_students()
        self.appoint_advisors()
        self.init_courses()
        self.add_past_courses()
        self.request_courses()
        self.print_statistics()
        self.create_output()
        
        
    def print_statistics(self):
        logging.warning("\n\n\nCourse Statistics:\n")
        self.print_collision_statistics()
        self.print_mandatory_statistics()
        self.print_final_statistics()
        self.print_te_statistics()
        
    def print_collision_statistics(self):
        courses = (self.mandatory_courses + self.non_tech_elective_courses 
                   + self.tech_elective_courses 
                   + self.fac_tech_elective_courses) 
        
        for course in courses:
            length = len(course.non_registered_collision)
            if length > 0:
                logging.warning(str(length) + " Students couldn't register to " + course.__str__() 
                             + " because of collision problem (" + ", ".join([stu.student_id.__str__() 
                                                                              for stu in course.non_registered_collision]) + ")")
    def print_mandatory_statistics(self):
        for course in self.mandatory_courses:
            length = len(course.non_registered_prereq)
            if length > 0:
                logging.warning(str(length) + " Students couldnt't register to " + course.__str__()
                                + " because of prerequisite problem (" + ", ".join([stu.student_id.__str__()
                                                                                    for stu in course.non_registered_prereq]) + ")")
    
    def print_final_statistics(self):
        for course in self.final_courses:
            length = len(course.non_registered_credit)
            if length > 0:
                logging.warning(str(length) + " Students couldn't register to " + course.__str__()
                                + " because of completed credit condition ("
                                + ", ".join([stu.student_id.__str__() for stu in course.non_registered_credit]) + ")")
    
    def print_te_statistics(self):
        non_registered = set()
        for course in self.tech_elective_courses:
            non_registered = non_registered.union(course.non_registered_credit)
        
        length = len(non_registered)    
        if length > 0:
                logging.warning(str(length) + " Students couldn't register to a Technical Elective this semester ("
                                + ", ".join([stu.student_id.__str__() for stu in non_registered]) + ")")
            
    def read_data(self):
        file = open("inputs/input.json", "r")
        self.data = json.load(file)

    def init_courses(self):
        self.init_mandatory_courses()
        self.init_final_mandatory_courses()
        self.init_nontech_courses()
        self.init_fac_tech_courses()
        self.init_tech_courses()

    def init_mandatory_courses(self):
        for course_data in self.data.get("MandatoryCourses"):
            ccode = course_data.get("courseCode")
            sem = course_data.get("semester")
            credit = course_data.get("credits")
            theoretical = course_data.get("theoretical")
            practical = course_data.get("practical")
            prereqs = course_data.get("preRequisites")
            quota = course_data.get("quota")

            prereq_courses = [self.find_course(
                course_str) for course_str in prereqs]

            course = MandatoryCourse(ccode, sem, credit, theoretical,
                                     practical, prereq_courses, quota, self)
            self.mandatory_courses.append(course)

    def init_final_mandatory_courses(self):
        req_credits = self.data.get("FinalProjectRequiredCredits")
        for course_data in self.data.get("FinalProjectMandatoryCourses"):
            ccode = course_data.get("courseCode")
            sem = course_data.get("semester")
            credit = course_data.get("credits")
            theoretical = course_data.get("theoretical")
            practical = course_data.get("practical")
            prereqs = course_data.get("preRequisites")
            quota = course_data.get("quota")

            prereq_courses = [self.find_course(
                course_str) for course_str in prereqs]

            course = final_project_mandatory_course.FinalProjectMandatoryCourse(ccode, sem, credit, theoretical,
                                                 practical, prereq_courses, quota, req_credits, self)
            self.mandatory_courses.append(course)
            self.final_courses.append(course)

    def init_nontech_courses(self):
        sem_nums = self.data["nonTechnicalSemesters"]
        nte_credits = self.data["nonTechnicalCredits"]
        nte_theoretical = self.data["nonTechnicalTheoretical"]
        nte_practical = self.data["nonTechnicalPractical"]

        for course_data in self.data["nonTechnicalElectiveCourses"]:
            ccode = course_data["courseCode"]
            quota = course_data["quota"]

            course = NonTechnicalUniversityElectiveCourse(ccode, quota, nte_credits, nte_theoretical,
                                                          nte_practical, sem_nums, self)
            self.non_tech_elective_courses.append(course)

    def init_fac_tech_courses(self):
        sem_nums = self.data["facultyTechnicalSemesters"]
        fte_credits = self.data["facultyTechnicalCredits"]
        fte_theoretical = self.data["facultyTechnicalTheoretical"]
        fte_practical = self.data["facultyTechnicalPractical"]

        for course_data in self.data["facultyTechnicalElectiveCourses"]:
            ccode = course_data["courseCode"]
            quota = course_data["quota"]

            course = FacultyTechnicalElectiveCourse(ccode, quota, fte_credits, fte_theoretical,
                                                    fte_practical, sem_nums, self)
            self.fac_tech_elective_courses.append(course)

    def init_tech_courses(self):
        te_req_credits = self.data["technicalRequiredCredits"]
        sem_nums = self.data["technicalSemesters"]
        te_credits = self.data["technicalCredits"]
        te_theoretical = self.data["technicalTheoretical"]
        te_practical = self.data["technicalPractical"]

        for course_data in self.data["technicalElectiveCourses"]:
            ccode = course_data["courseCode"]
            quota = course_data["quota"]
            prereqs = course_data["preRequisites"]

            prereq_courses = [self.find_course(course_str)
                              for course_str in prereqs]

            course = TechnicalElectiveCourse(ccode, quota, te_credits, te_theoretical,
                                             te_practical, sem_nums, self, te_req_credits, prereq_courses)
            self.tech_elective_courses.append(course)

    def find_course(self, course_code: str):
        """Finds course in courses list which have the same course code as the 
        parameter given"""
        for course in self.mandatory_courses:
            if course.course_code == course_code:
                return course
        return None

    def read_names(self):
        names_file = open("inputs/names.json", "r")
        surnames_file = open("inputs/surnames.json", "r")
        names = json.load(names_file)
        surnames = json.load(surnames_file)

        self.names = names.get("names")
        self.surnames = surnames.get("surnames")

    def get_rand_name(self):
        name = random.choice(self.names)
        surname = random.choice(self.surnames)
        return name + " " + surname

    def init_advisors(self):
        advisor_count = self.data.get("Advisors")

        for i in range(advisor_count):
            name = self.get_rand_name()
            self.advisors.append(Advisor(name))

    def init_students(self):
        first_year = self.data.get("1stYearStudents")
        second_year = self.data.get("2ndYearStudents")
        third_year = self.data.get("3rdYearStudents")
        fourth_year = self.data.get("4thYearStudents")

        self.init_students_by_count(1, first_year)
        self.init_students_by_count(2, second_year)
        self.init_students_by_count(3, third_year)
        self.init_students_by_count(4, fourth_year)

    def init_students_by_count(self, year, count):
        for i in range(count):
            name = self.get_rand_name()
            student = Student(
                name, year, self.total_students[year - 1] + 1, self)
            self.students.append(student)
            self.total_students[year - 1] += 1

    def appoint_advisors(self):
        for student in self.students:
            rand_advisor = random.choice(self.advisors)
            student.advisor = rand_advisor

    def add_past_courses(self):
        for student in self.students:
            self.add_past_mandatories(student)
            self.add_past_electives(student)


    def add_past_electives(self, student):
        nte_count = student.get_num_of_past_electives(self.data["nonTechnicalSemesters"])
        fte_count = student.get_num_of_past_electives(self.data["facultyTechnicalSemesters"])
        te_count = student.get_num_of_past_electives(self.data["technicalSemesters"])
        
        past_courses = []
        past_courses += random.sample(self.non_tech_elective_courses, nte_count)
        past_courses += random.sample(self.fac_tech_elective_courses, fte_count)
        past_courses += random.sample(self.tech_elective_courses, te_count)
        
        for course in past_courses:
            student.transcript.add_past_course(self.data["PassProbability"], course)
        
        
    
    def add_past_mandatories(self, student):
        for course in self.mandatory_courses:
            if course.is_elligible_past_course(student):
                transcript = student.transcript
                pass_prob = self.data.get("PassProbability")
                transcript.add_past_course(pass_prob, course)

    def request_courses(self):
        for student in self.students:
            student.request_courses()

    def get_offered_mandatories(self, student):
        return [course.course_section
                for course in self.mandatory_courses
                if course.is_offerable_for_student(student)]

    def get_offered_electives(self, student):
        nte_count = self.offered_nte_count(student)
        te_count = self.offered_te_count(student)
        fte_count = self.offered_fte_count(student)

        offered_courses = []

        offered_courses += random.sample(
            self.non_tech_elective_courses, nte_count)
        offered_courses += random.sample(self.tech_elective_courses, te_count)
        offered_courses += random.sample(
            self.fac_tech_elective_courses, fte_count)

        return [course.course_section for course in offered_courses]

    def offered_nte_count(self, student):
        count = 0
        for i in self.data.get("nonTechnicalSemesters"):
            if student.semester_num == i:
                count += 1
        return count

    def offered_te_count(self, student):
        count = 0
        for i in self.data.get("technicalSemesters"):
            if student.semester_num == i:
                count += 1
        return count

    def offered_fte_count(self, student):
        count = 0
        for i in self.data.get("facultyTechnicalSemesters"):
            if student.semester_num == i:
                count += 1
        return count

    def is_there_empty_nte_section(self):
        course_secs = [
            course.course_section for course in self.non_tech_elective_courses]
        return any((not course_sec.is_full() for course_sec in course_secs))

    def is_there_empty_te_section(self):
        course_secs = [
            course.course_section for course in self.tech_elective_courses]
        return any((not course_sec.is_full() for course_sec in course_secs))

    def is_there_empty_fte_section(self):
        course_secs = [
            course.course_section for course in self.fac_tech_elective_courses]
        return any((not course_sec.is_full() for course_sec in course_secs))

    def set_semester(self):
        if self.data.get("CurrentSemester").lower() == "spring":
            self.semester = Semester.SPRING
        elif self.data.get("CurrentSemester").lower() == "fall":
            self.semester = Semester.FALL
        else:
            raise Exception("Invalid Semester For Registration System")

    def create_output(self):
        if not os.path.exists("Students"):
            os.mkdir("Students")

            for student in self.students:
                file_name = student.student_id.__str__() + ".json"
                with open(os.path.join("Students", file_name), "w") as outfile:
                    json.dump(student.as_dict(), outfile, indent=4)
        else:
            raise Exception("Delete existing Students Folder first!!!")
