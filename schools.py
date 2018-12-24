import json, os, psycopg2

def main():
    test_student()

def test_student():


def init():
    DATABASE_URL = os.environ['DATABASE_URL']
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')

# Student
class Student:
    def __init__(self, given_names='', surname='', grade=-1, parent_given_names='', parent_surname='', parent_no='', parent_email='', ec_given_names='', ec_surname='', ec_no=''):
        details = {
                'given_names': given_names,
                'surname': surname,
                'grade': grade,
                'parent_given_names': parent_given_name,
                'parent_surname': parent_surn
                'parent_no': parent_no,
                'parent_email': parent_email,
                'ec_given_names': ec_given_names,
                'ec_surname': ec_surname,
                'ec_no': ec_no
        }

    def update(self, field_name, new_value):
        field = lower(field_name)
        if field_name not in details:
            print('Field does not exist')
        elif type(new_value) != type(self.details[field]):
            print('Invalid datatype')
        else:
            self.details[field] = new_value


    def get_json(self):
        return json.dumps(self.details)


# Teacher
class Teacher:
    def __init__(self, given_names='', surname='', email='', mobile='', start_day='', dob='', wwcc='', wwcc_expiry=''):
        details = {
                'given_names': given_names,
                'surname': surname,
                'email'=email,
                'mobile'=mobile,
                'start_day'=start_day,
                'dob'=dob,
                'wwcc'=wwcc,
                'wwcc_expiry'=wwcc_expiry
        }

    def update(self, field_name, new_value):
        field = lower(field_name)
        if field_name not in details:
            print('Field does not exist')
        elif type(new_value) != type(self.details[field]):
            print('Invalid datatype')
        else:
            self.details[field] = new_value


    def get_json(self):
        return json.dumps(self.details)


# School - stores information about the school name, location, admin contact, IT contact, supervising teacher

# Roster - stores information about the teacher and the classes they teach

# Class - stores information about the first date, last date, day of week, school, start time, duration, classroom and course

# Enrolments - stores information about the students enrolled in classes

# Course - stores information about the topic, resource location, type of resource (project, notes, outline)

# Course Documentation - stores the teacher, course and date of contribution

# Student Feedback

# Teacher Feedback


if __name__ == '__main__':
    main()

