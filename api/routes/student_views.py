from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from werkzeug.security import generate_password_hash
from http import HTTPStatus
# from datetime import datetime

from ..models.grades import Grading
from ..models.courses import Course
from ..models.students import Student
from ..models.enroll import Enrolled

from ..utils.decorators import is_admin, get_user_role
from ..utils.convert_grade import get_letter_grade, convert_grade_to_gpa




student_namespace = Namespace('students', description='Namespace for Students')




# --- serializers ---
student_signup_model = student_namespace.model(
    'Student_Signup', {
        'full_name': fields.String(required=True, description="Student's Full_Name"),
        'username': fields.String(required=True, description="Student's username"),
        'email': fields.String(required=True, description="Student's Email"),
        'password': fields.String(required=True, description="Student's Password"),
        'matric_no': fields.String(required=True, description="Student's matriculation_No.")
    }
)

student_model = student_namespace.model(
    'Student', {
        'id': fields.Integer(description="Student's User ID"),
        'full_name': fields.String(required=True, description="Full Name"),
        'username': fields.String(required=True, description="userame"),
        'email': fields.String(required=True, description="Student's Email"),   
        'role': fields.String(required=True, description="Type of User"),
        'matric_no': fields.String(required=True, description="Student's matriculation_No."),
        # 'created_on': fields.DateTime(description='Date & Time of student enrollment')
    }
)

enrolled_model = student_namespace.model(
    'Enrollment', {
        'student_id': fields.Integer(description="Student's User ID"),
        'course_id': fields.Integer(description="Course's ID")
    }
)

grading_model = student_namespace.model(
    'Grade', {
        'id': fields.Integer(description="Grade ID"),
        'course_id': fields.Integer(required=True, description="Course ID"),
        'percent_grade': fields.Float(required=True, description="Grade out of 100")       
    }
)

grade_update_model = student_namespace.model(
    'Update_Grade', {
        'percent_grade': fields.Float(required=True, description="Grade out of 100")         
    }
)



# Verify User_Access basing on User.role
def user_role(student_id:int) -> bool:
    claims = get_jwt()
    current_user_id = get_jwt_identity()
    if (get_user_role(claims['sub']) == 'admin') or (current_user_id == student_id):
        return True
    else:
        return False



# Getting all Students
@student_namespace.route('')
class Get_All_Students(Resource):

    @student_namespace.marshal_with(student_model)
    @student_namespace.doc(description = "Retrieve All Students")
    @is_admin()
    def get(self):
        
        """ Retrieve All Students """
        students = Student.query.all()
        return students, HTTPStatus.OK



# Registering/Creating a student
@student_namespace.route('/register')
class Register_A_Student(Resource):

    @student_namespace.expect(student_signup_model)
    @student_namespace.doc(description = "Register a Student")
    @is_admin()
    def post(self):
        
        """ Register a Student """        
        data = student_namespace.payload

        student = Student.query.filter_by(username=data['username']).first()
        if student:
            return {"message": "Student account already exists"}, HTTPStatus.CONFLICT

        new_student = Student(
            full_name = data['full_name'],
            username = data['username'],
            email = data['email'],
            password_hash = generate_password_hash(data['password']),
            role = 'student',
            matric_no = data['matric_no'],
            # created_on = datetime.utcnow
        )

        new_student.save()

        student_resp = {}

        student_resp['id'] = new_student.id
        student_resp['full_name'] = new_student.full_name
        student_resp['username'] = new_student.username
        student_resp['email'] = new_student.email
        student_resp['role'] = new_student.role
        student_resp['matric_no'] = new_student.matric_no
        # student_resp['created_on'] = new_student.created_on

        return student_resp, HTTPStatus.CREATED



# Retrieve/Get..Update..Delete -> a Student
@student_namespace.route('/<int:student_id>')
class Get_Update_Delete_Student(Resource):
    
    @student_namespace.doc(description = "Retrieve a Student's Details by ID")
    @jwt_required()
    def get(self, student_id):
        
        """ Retrieve a Student's Details by ID """
        
        if user_role(student_id):
            
            student = Student.get_student_by_id(student_id)

            student_resp = {}  
            student_resp['id'] = student.id
            student_resp['full_name'] = student.full_name
            student_resp['username'] = student.username
            student_resp['email'] = student.email
            student_resp['role'] = student.role
            student_resp['matric_no'] = student.matric_no
            # student_resp['created_on'] = student.created_on

            return student_resp, HTTPStatus.OK
        
        else:
            return {"message": "Admin or Active Student Only"}, HTTPStatus.FORBIDDEN

    
    @student_namespace.expect(student_signup_model)
    # @student_namespace.marshal_with(student_model)
    @student_namespace.doc(description = "Update a Student's Details by ID")
    @jwt_required()
    def put(self, student_id):
        
        """ Update a Student's Details by ID """

        if user_role(student_id):
            
            student = Student.get_student_by_id(student_id)
            
            data = student_namespace.payload

            student.full_name = data['full_name']
            student.username = data['username']
            student.email = data['email']
            student.password_hash = generate_password_hash(data['password'])

            student.update()

            student_resp = {}  
            student_resp['id'] = student.id
            student_resp['full_name'] = student.full_name
            student_resp['username'] = student.username
            student_resp['email'] = student.email
            student_resp['role'] = student.role
            student_resp['matric_no'] = student.matric_no
            # student_resp['created_on'] = student.created_on

            return student_resp, HTTPStatus.OK

        else:
            return {"message": "Admin or Active Student Only"}, HTTPStatus.FORBIDDEN
    

    @student_namespace.doc(description = 'Delete a Student by ID')
    @is_admin()
    def delete(self, student_id):
        
        """ Delete a Student by ID (Admin Only) """

        student = Student.get_student_by_id(student_id)

        student.delete()

        return {"message": "Student Account Deleted"}, HTTPStatus.OK
    



# Get a Specific Student's Courses
@student_namespace.route('/<int:student_id>/courses')
class Get_Student_Courses(Resource):

    @student_namespace.doc(description = "Retrieve a Student's Courses - Admin or Active Student")
    @jwt_required()
    def get(self, student_id):
        
        """ Retrieve a Student's Courses """

        if user_role(student_id):
            
            courses = Enrolled.get_courses_by_student(student_id)

            resp = []

            for course in courses:
                course_resp = {}
                course_resp['id'] = course.id
                course_resp['name'] = course.name
                course_resp['teacher'] = course.teacher

                resp.append(course_resp)

            return resp, HTTPStatus.OK
    
        else:
            return {"message": "Admin or Active Student Only"}, HTTPStatus.FORBIDDEN




# Adding & Updating Student Grades by Admin, & Getting Grades by Student ID or Admin
@student_namespace.route('/<int:student_id>/grades')
class Add_Get_Update_Grades(Resource):

    @student_namespace.doc(description = "Retrieve a Student's Grades - Admin or Active Student")
    @jwt_required()
    def get(self, student_id):
        
        """ Retrieve a Student's Grades """

        if user_role(student_id):

            # Check if student exists
            student = Student.query.filter_by(id=student_id).first()
            if not student:
                return {"message": "Student Not Found"}, HTTPStatus.NOT_FOUND
            
            # Retrieve the student's grades        
            courses = Enrolled.get_courses_by_student(student_id)

            resp = []

            for course in courses:

                grade_resp = {}

                course_grade = Grading.query.filter_by(student_id=student_id, course_id=course.id).first()

                grade_resp['course_name'] = course.name # testing grade ownership for course_grade

                if course_grade:
                    grade_resp['grade_id'] = course_grade.id
                    grade_resp['percent_grade'] = course_grade.percent_grade
                    grade_resp['letter_grade'] = course_grade.letter_grade
                else:
                    grade_resp['percent_grade'] = None
                    grade_resp['letter_grade'] = None
                
                resp.append(grade_resp)
            
            return resp, HTTPStatus.OK
        
        else:
            return {"message": "Admins or Active Student Only"}, HTTPStatus.FORBIDDEN
        


    @student_namespace.expect(grading_model)
    @student_namespace.doc(description = "Upload a Student's Grade in a Course - (Admins Only)")
    @is_admin()
    def post(self, student_id):

        """ Upload a Student's Grade in a Course - (Admins Only) """

        data = student_namespace.payload

        student = Student.get_student_by_id(student_id)
        course = Course.get_course_by_id(id=data['course_id'])
        
        # Confirm that the student is taking the course
        student_course = Enrolled.query.filter_by(student_id=student_id, course_id=course.id).first()
        if not student_course:
            return {"message": f"{student.username} is not taking {course.name}"}, HTTPStatus.NOT_FOUND
        
        # Add a new grade
        new_grade = Grading(
            student_id = student_id,
            course_id = data['course_id'],
            percent_grade = data['percent_grade'],
            letter_grade = get_letter_grade(data['percent_grade'])
        )

        new_grade.save()

        grade_resp = {}
        grade_resp['grade_id'] = new_grade.id
        grade_resp['student_id'] = new_grade.student_id
        grade_resp['student_full_name'] = student.full_name
        grade_resp['student_username'] = student.username
        grade_resp['student_matric_no'] = student.matric_no
        # grade_resp['student_created_on'] = student.created_on

        grade_resp['course_id'] = new_grade.course_id
        grade_resp['course_name'] = course.name
        grade_resp['course_teacher'] = course.teacher
        grade_resp['percent_grade'] = new_grade.percent_grade
        grade_resp['letter_grade'] = new_grade.letter_grade

        return grade_resp, HTTPStatus.CREATED
        


# Update & Delete a Grade
@student_namespace.route('/grades/<int:grade_id>')
class Update_Delete_Grade(Resource):

    @student_namespace.expect(grade_update_model)
    @student_namespace.doc(description = "Update a Grade - (Admins Only)")
    @is_admin()
    def put(self, grade_id):

        """ Update a Grade """

        data = student_namespace.payload

        grade = Grading.get_grade_by_id(grade_id)
        
        grade.percent_grade = data['percent_grade']
        grade.letter_grade = get_letter_grade(data['percent_grade'])
        
        grade.update()

        grade_resp = {}
        grade_resp['grade_id'] = grade.id
        grade_resp['student_id'] = grade.student_id
        grade_resp['course_id'] = grade.course_id
        grade_resp['percent_grade'] = grade.percent_grade
        grade_resp['letter_grade'] = grade.letter_grade

        return grade_resp, HTTPStatus.OK
    


    @student_namespace.doc(description = "Delete a Grade (Admins Only)")
    @is_admin()
    def delete(self, grade_id):

        """ Delete a Grade """

        grade = Grading.get_grade_by_id(grade_id)
        grade.delete()

        return {"message": "Grade Successfully Deleted"}, HTTPStatus.OK



# Getting a student's CGPA
@student_namespace.route('/<int:student_id>/cgpa')
class Get_Student_CGPA(Resource):

    @student_namespace.doc(description = "Calculate a Student's CGPA - Admin or Active Student Only")
    @jwt_required()
    def get(self, student_id):

        """ Calculate a Student's CGPA """

        if user_role(student_id):

            student = Student.get_student_by_id(student_id)
            
            courses = Enrolled.get_courses_by_student(student_id)
            
            total_gpa = 0
            
            for course in courses:
                grade = Grading.query.filter_by(student_id=student_id, course_id=course.id).first()
                
                if grade:
                    letter_grade = grade.letter_grade
                    gpa = convert_grade_to_gpa(letter_grade)
                    total_gpa += gpa
                
            cgpa = total_gpa / len(courses)
            rounded_cgpa = float("{:.2f}".format(cgpa))

            return {"message": f"{student.username}'s CGPA is {rounded_cgpa}"}, HTTPStatus.OK
    
        else:
            return {"message": "Admin or Active Student Only"}, HTTPStatus.FORBIDDEN