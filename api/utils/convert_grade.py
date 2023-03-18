
# Convert grade from percent(%) value
def get_letter_grade(percent_grade):
    
    if percent_grade >= 85:
        return 'A+'
    elif percent_grade < 85 and percent_grade >= 80:
        return 'A'
    elif percent_grade < 80 and percent_grade >= 70:
        return 'B'
    elif percent_grade < 70 and percent_grade >= 65:
        return 'C'
    elif percent_grade < 65 and percent_grade >= 55:
        return 'D'
    elif percent_grade < 55 and percent_grade >= 50:
        return 'E'
    elif percent_grade < 50 and percent_grade >= 34:
        return 'P'
    else:
        return 'F'
    
# Getting the GPA from the grade
def convert_grade_to_gpa(letter_grade):
    if letter_grade == 'A+':
        return 5.0
    elif letter_grade == 'A':
        return 4.5
    elif letter_grade == 'B':
        return 3.8
    elif letter_grade == 'C':
        return 3.4
    elif letter_grade == 'D':
        return 3.0
    elif letter_grade == 'E':
        return 2.4
    elif letter_grade == 'P':
        return 1.8
    else:
        return 0
