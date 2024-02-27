

class Schedule(object):

    DAYS = 5
    HOURS = 8

    def __init__(self):
        self.program = [[0] * self.DAYS for _ in range(self.HOURS)]

    def add_to_program(self, course_section):
        course_program = course_section.course_program

        for i in range(self.HOURS):
            for j in range(self.DAYS):
                if course_program[i][j] == 1:
                    self.program[i][j] = course_section
                    

    def collided_sections(self, course_section):
        course_program = course_section.course_program
        collided_sections = []

        for i in range(self.HOURS):
            for j in range(self.DAYS):
                if self.program[i][j] != 0 and course_program[i][j] == 1:
                    collided_sections.append(self.program[i][j])

        return collided_sections

    def is_collision(self, course_section):
        return len(self.collided_sections(course_section)) > 1
