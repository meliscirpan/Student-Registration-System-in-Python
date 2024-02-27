class Grade(object):
    
    def __init__(self, course, int_grade):
        self.course = course
        self.int_grade = int_grade
        self.set_letter_grade()
        
    def is_passed(self):
        return self.int_grade >= 50
        
    
    def set_letter_grade(self):
        if self.int_grade < 0 or self.int_grade > 100:
            print("Grades must be between 0-100!!")
            exit(-1)
        elif self.int_grade <= 44:
            letter_grade = "FF"
        elif self.int_grade <= 49:
            letter_grade = "FD"
        elif self.int_grade <= 54:
            letter_grade = "DD"
        elif self.int_grade <= 64:
            letter_grade = "DC"
        elif self.int_grade <= 74:
            letter_grade = "CC"
        elif self.int_grade <= 79:
            letter_grade = "CB"
        elif self.int_grade <= 84:
            letter_grade = "BB"
        elif self.int_grade <= 89:
            letter_grade = "BA"
        else:
            letter_grade = "AA"
            
        self.letter_grade = letter_grade