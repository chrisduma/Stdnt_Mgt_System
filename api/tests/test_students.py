import unittest
from flask_jwt_extended import create_access_token

from .. import create_app
from ..config.config import config_dict
from ..utils import db
from ..models.admin import Admin
from ..models.students import Student

class UserTestCase(unittest.TestCase):
    
    def setUp(self):

        self.app = create_app(config_app=config_dict['test'])
        self.appctx = self.app.app_context()
        self.appctx.push()
        self.client = self.app.test_client()
        db.create_all()
        
    def tearDown(self):

        db.drop_all()
        self.appctx.pop()
        self.app = None
        self.client = None


    def test_students(self):

        # Activate a test admin
        admin_signup_data = {
            "full_name": "test admin",
            "username": "asdme",
            "email": "test_admin@gmail.com",
            "password": "password"
        }

        response = self.client.post('/admin/register', json=admin_signup_data)

        assert response.status_code == 201

        admin = Admin.query.filter_by(email='test_admin@gmail.com').first()

        token = create_access_token(identity=admin.id)

        headers = {
            "Authorization": f"Bearer {token}"
        }

        
        # Register a student
        student_signup_data = {
            "full_name": "test student",
            "username": "student",
            "email": "test_student@gmail.com",
            "password": "password",
            "matric_no": "VM-888"
        }

        response = self.client.post('/students/register', json=student_signup_data, headers=headers)

        student = Student.query.filter_by(email='test_student@gmail.com').first()

        assert student.full_name == "test student"

        assert response.status_code == 201


        # Retrieve all students
        response = self.client.get('/students', headers=headers)

        assert response.status_code == 200

        # assert response.json == [{
        #     "id": 2,
        #     "full_name": "test student",
        #     "username": "studenta",
        #     "email": "test_student@gmail.com",
        #     "role": "student",
        #     "matric_no": "VM-888"
        # }]


#         # Sign a student in
#         student_login_data = {
#             "email":"test_student@gmail.com",
#             "password": "password"
#         }

#         response = self.client.post('/auth/login', json=student_login_data)

#         assert response.status_code == 201


# #         # Retrieve a student's details by ID
#         response = self.client.get('/students/2', headers=headers)

#         assert response.status_code == 200

#         assert response.json == {
#             "id": 2,
#             "full_name": "test student",
#             "username": "studenta",
#             "email": "test_student@gmail.com",
#             "role": "student",
#             "matric_no": "VM-888"
#         }


#         # Update a student's details
#         student_update_data = {
#             "full_name": "sample student",
#             "username": "studenta",
#             "email": "sample_student@gmail.com",
#             "password": "password"
#         }

#         response = self.client.put('/students/2', json=student_update_data, headers=headers)

#         assert response.status_code == 200

#         assert response.json == {
#             "id": 2,
#             "full_name": "sample student",
#             "username": "studenta",
#             "email": "sample_student@gmail.com",
#             "role": "student",
#             "matric_no": "VM-888"
#         }


#         # Register a test course
#         course_registration_data = {
#             "name": "test course",
#             "teacher": "test teacher"
#         }

#         response = self.client.post('/courses', json=course_registration_data, headers=headers)


#         # Enroll a student for a test course
#         response = self.client.post('/courses/1/students/2', headers=headers)        


#         # Retrieve a student's courses
#         response = self.client.get('/students/2/courses', headers=headers)

#         assert response.status_code == 200

#         assert response.json == [{
#             "id": 1,
#             "name": "test course",
#             "teacher": "test teacher"
#         }]

#         # Upload a student's grade in a course
#         grade_upload_data = {
#             "student_id": 2,
#             "course_id": 1,
#             "percent_grade": 85.7
#         }

#         response = self.client.post('/students/2/grades', json=grade_upload_data, headers=headers)

#         assert response.status_code == 201

#         assert response.json == {
#             "grade_id": 1,
#             "student_id": 2,
#             "student_full_name": "sample student",
#             "student_username": "student",
#             "student_matric_no": "VM-888",
#             "course_id": 1,
#             "course_name": "test course",
#             "course_teacher": "test teacher",
#             "percent_grade": 85.7,
#             "letter_grade": "B"
#         } 


# #         # Retrieve a student's grades
#         response = self.client.get('/students/2/grades', headers=headers)

#         assert response.status_code == 200

#         assert response.json == [{
#             "course_name": "test course",
#             "grade_id": 1,
#             "percent_grade": 85.7,
#             "letter_grade": "B"
#         }]


#         # Update a grade
#         grade_update_data = {
#             "percent_grade": 91.5
#         }

#         response = self.client.put('/students/grades/1', json=grade_update_data, headers=headers)

#         assert response.status_code == 200

#         assert response.json == {
#             "grade_id": 1,
#             "student_id": 2,
#             "course_id": 1,
#             "percent_grade": 91.5,
#             "letter_grade": "A"
#         }


        # # Calculate a student's CGPA
        # response = self.client.get('/students/2/cgpa', headers=headers)
        # assert response.status_code == 200
        # assert response.json["message"] == "Sample Student's CGPA is 4.0"


        # # Delete a grade
        # response = self.client.delete('/students/grades/1', headers=headers)
        # assert response.status_code == 200


        # Delete a student
        response = self.client.delete('/students/2', headers=headers)
        assert response.status_code == 200
