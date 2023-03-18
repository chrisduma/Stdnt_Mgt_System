from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required
from http import HTTPStatus

from ..models.courses import Course
from ..models.students import Student
from ..models.enroll import Enrolled

from ..utils.decorators import is_admin



course_namespace = Namespace('courses', description='Namespace for Courses')



course_model = course_namespace.model(
    'Course', {
        'id': fields.Integer(description="Course ID"),
        'name': fields.String(description="Course Name", required=True),
        'teacher': fields.String(description="Course Teacher", required=True)
    }
)

enrolled_model = course_namespace.model(
    'Enrollment', {
        'course_id': fields.Integer(description="Course ID"),
        'student_id': fields.Integer(description="Student ID")
    }
)


@course_namespace.route('')
class Create_Retrieve_Course(Resource):

    @course_namespace.marshal_with(course_model)
    @course_namespace.doc(description = "Get All Courses")
    @jwt_required()
    def get(self):
        
        """ Get All Courses """

        courses = Course.query.all()

        return courses, HTTPStatus.OK
    

    @course_namespace.expect(course_model)
    @course_namespace.doc(description='Register a Course - Admins Only')
    @is_admin()
    def post(self):
        
        """ Register a Course - Admins Only """

        data = course_namespace.payload

        # Check if course already exists
        course = Course.query.filter_by(name=data['name']).first()
        if course:
            return {"message": "Course Already Exists"}, HTTPStatus.CONFLICT

        # Register new course
        new_course = Course(
            name = data['name'],
            teacher = data['teacher']
        )

        new_course.save()

        course_resp = {}
        course_resp['id'] = new_course.id
        course_resp['name'] = new_course.name
        course_resp['teacher'] = new_course.teacher

        return course_resp, HTTPStatus.CREATED
    


@course_namespace.route('/<int:course_id>')
class Get_Update_Delete_Course(Resource):
    
    @course_namespace.marshal_with(course_model)
    @course_namespace.doc(description = "Retrieve a Course by ID - Admin Only")
    @is_admin()
    def get(self, course_id):
        
        """ Retrieve a Course by ID """

        course = Course.get_course_by_id(course_id)
        
        return course, HTTPStatus.OK
    

    @course_namespace.expect(course_model)
    @course_namespace.marshal_with(course_model)
    @course_namespace.doc(description = "Update a Course by ID - Admins Only")
    @is_admin()
    def put(self, course_id):
        
        """ Update a Course by ID - Admin Only """

        course = Course.get_course_by_id(course_id)

        data = course_namespace.payload

        course.name = data['name']
        course.teacher = data['teacher']

        course.update()

        return course, HTTPStatus.OK
    

    @course_namespace.doc(description = "Delete a Course by ID - Admins Only")
    @is_admin()
    def delete(self, course_id):
        
        """ Delete a Course by ID - Admins Only """

        course = Course.get_course_by_id(course_id)

        course.delete()

        return {"message": "Course Successfully Deleted"}, HTTPStatus.OK




@course_namespace.route('/<int:course_id>/students')
class Get_All_Enrolled_Students(Resource):

    @course_namespace.doc(description = "Get all Students Enrolled for a Course - Admins Only")
    @is_admin()
    def get(self, course_id):
        
        """ Get all Enrolled Students """

        students = Enrolled.get_students_by_course(course_id)

        resp = []

        for student in students:

            student_resp = {}

            student_resp['id'] = student.id
            student_resp['full_name'] = student.full_name
            student_resp['username'] = student.username
            student_resp['matric_no'] = student.matric_no
            # student_resp['created_on'] = student.created_on

            resp.append(student_resp)

        return resp, HTTPStatus.OK




@course_namespace.route('/<int:course_id>/students/<int:student_id>')
class Enroll_Drop_Student(Resource):
    
    @course_namespace.doc(description = "Enroll a Student for a Course (Admins Only)")
    @is_admin()
    def post(self, course_id, student_id):
        
        """ Enroll a Student for a Course """

        course = Course.get_course_by_id(course_id)
        student = Student.get_student_by_id(student_id)
        
        enrolled = Enrolled.query.filter_by(student_id=student.id, course_id=course.id).first()

        if enrolled:
            return {
              "message": f"{student.username} is already registered for {course.name}"},HTTPStatus.OK
        
        course_student =  Enrolled(
            course_id = course_id,
            student_id = student_id
        )

        course_student.save()

        course_student_resp = {}
        course_student_resp['course_id'] = course_student.course_id
        course_student_resp['course_name'] = course.name
        course_student_resp['course_teacher'] = course.teacher
        
        course_student_resp['student_id'] = course_student.student_id
        course_student_resp['student_full_name'] = student.full_name
        course_student_resp['student_username'] = student.username
        course_student_resp['student_matric_no'] = student.matric_no
        # course_student_resp['student_created_on'] = student.created_on

        return course_student_resp, HTTPStatus.CREATED



    @course_namespace.doc(description='Delete a Student from a Course')
    @is_admin()
    def delete(self, course_id, student_id):
        
        """ Delete a Student from a Course - Admins Only """

        # Check if student and course exist
        course = Course.query.filter_by(id=course_id).first()
        student = Student.query.filter_by(id=student_id).first()

        if not student or not course:
            return {"message": "Student or Course Incorrect"}, HTTPStatus.NOT_FOUND
        
        # Check if student is not registered for the course
        enrolled = Enrolled.query.filter_by(student_id=student.id, course_id=course.id).first()

        if not enrolled:
          return {
          "message": f"{student.username} is not registered for {course.name}"}, HTTPStatus.NOT_FOUND

        enrolled.delete()

        return {"message": f"{student.username} has been deleted from {course.name}"}, HTTPStatus.OK