import unittest
from .. import create_app
from ..config.config import config_dict
from ..utils import db
from ..models.admin import Admin
from ..models.courses import Course
from flask_jwt_extended import create_access_token

class CourseTestCase(unittest.TestCase):
    
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


    def test_courses(self):

        # Activate a test admin
        admin_signup_data = {
            "full_name": "test admin",
            "username": "admin",
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
        

        # Register a test student
        student_signup_data = {
            "full_name": "test student",
            "username": "student",
            "email": "test_student@gmail.com",
            "password": "password",
            "matric_no": "VM-888"
        }

        response = self.client.post('/students/register', json=student_signup_data, headers=headers)


        # Register a course
        course_registration_data = {
            "name": "test course",
            "teacher": "test teacher"
        }

        response = self.client.post('/courses', json=course_registration_data, headers=headers)

        assert response.status_code == 201

        courses = Course.query.all()

        course_id = courses[0].id

        course_name = courses[0].name

        teacher = courses[0].teacher

        assert len(courses) == 1

        assert course_id == 1

        assert course_name == "test course"

        assert teacher == "test teacher"

        
        # Get all courses
        response = self.client.get('/courses', headers=headers)

        assert response.status_code == 200

        assert response.json == [{
            "id": 1,
            "name": "test course",
            "teacher": "test teacher"            
        }]


        # Retrieve a course's details by ID
        response = self.client.get('/courses/1', headers=headers)

        assert response.status_code == 200

        assert response.json == {
            "id": 1,
            "name": "test course",
            "teacher": "test teacher"            
        }


        # 'Update a course's details
        course_update_data = {
            "name": "sample course",
            "teacher": "sample teacher"
        }

        response = self.client.put('/courses/1', json=course_update_data, headers=headers)

        assert response.status_code == 200

        assert response.json == {
            "id": 1,
            "name": "sample course",
            "teacher": "sample teacher"            
        }


#         # Enroll a student for a course
        response = self.client.post('/courses/1/students/2', headers=headers)

        assert response.status_code == 201

        # assert response.json == [{
        #     "course_id": 1,
        #     "course_name": "sample course",
        #     "course_teacher": "sample teacher",
        #     "student_id": 2,
        #     "student_full_name": "test student",
        #     "student_username": "student",
        #     "matric_no": "VM-888"
        # }]


        # Get all students enrolled for a course
        response = self.client.get('/courses/1/students', headers=headers)

        assert response.status_code == 200

        assert response.json == [{
            "id": 2,
            "full_name": "test student",
            "username": "student",
            "matric_no": "VM-888"
        }]


        # Remove a student from a course
        response = self.client.delete('/courses/1/students/2', headers=headers)
        assert response.status_code == 200


        # Delete a course
        response = self.client.delete('/courses/1', headers=headers)
        assert response.status_code == 200