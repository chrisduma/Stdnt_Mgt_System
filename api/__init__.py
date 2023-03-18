from flask import Flask
from flask_restx import Api
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from werkzeug.exceptions import NotFound, MethodNotAllowed

from .utils import db
from .utils.blacklist import BLACKLIST
from .config.config import config_dict
from .auth.views import auth_namespace

from .routes.admin_views import admin_namespace
from .routes.student_views import student_namespace
from .routes.course_views import course_namespace

from .models.users import User
from .models.courses import Course
from .models.enroll import Enrolled
from .models.grades import Grading
from .models.admin import Admin
from .models.students import Student
from http import HTTPStatus
from dotenv import load_dotenv



def create_app(config_app=config_dict['dev']):

  app = Flask(__name__)

  load_dotenv()

  app.config.from_object(config_app)

  db.init_app(app)

  jwt = JWTManager(app)

  migrate = Migrate(app, db)



  @jwt.token_in_blocklist_loader
  def check_if_token_in_blacklist(jwt_header, jwt_payload):
      return jwt_payload['type'] in BLACKLIST
    
  @jwt.revoked_token_loader
  def revoked_token_callback(jwt_header, jwt_payload):
      return {
            "message": "The token has been revoked",
            "error": "token_revoked"
        }, HTTPStatus.UNAUTHORIZED
    
  @jwt.expired_token_loader
  def expired_token_callback(jwt_header, jwt_payload):
      return {
            "message": "The token has expired",
            "error": "token_expired"
        }, HTTPStatus.UNAUTHORIZED
    
  @jwt.invalid_token_loader
  def invalid_token_callback(error):
      return {
            "message": "Token verification failed",
            "error": "invalid_token"
        }, HTTPStatus.UNAUTHORIZED
    
  @jwt.unauthorized_loader
  def missing_token_callback(error):
      return {
            "message": "Request is missing an access token",
            "error": "authorization_required"
        }, HTTPStatus.UNAUTHORIZED
    
  @jwt.needs_fresh_token_loader
  def token_not_fresh_callback():
      return {
            "message": "The token is not fresh",
            "error": "fresh_token_required"
        }, HTTPStatus.UNAUTHORIZED


  authorizations = {
        "Bearer Auth": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "Add a JWT token to the header with ** Bearer &lt;JWT&gt; ** token to authorize"
        }
    }


  api = Api(app,
            title='student_management_API', 
            description='An api managing new & registered users, their courses of choice, grades and the teachers responsible for those courses.',
            authorizations=authorizations,
            security='Bearer Auth')
  api.add_namespace(auth_namespace, path='/auth')
  api.add_namespace(admin_namespace, path='/admin')
  api.add_namespace(student_namespace, path='/students')
  api.add_namespace(course_namespace, path='/courses')



  # ------------ error handlers ------------------
  @api.errorhandler(NotFound)
  def not_found(error):
    return {"error": "Not Found"}, 404

  @api.errorhandler(MethodNotAllowed)
  def method_error(error):
    return {"error": "This method is not allowed"}, 404




  @app.shell_context_processor
  def make_shell_context():
    return {
      'db': db,
      'user': User,
      'student': Student,
      'admin': Admin,
      'course': Course,
      'enroll': Enrolled,
      'grade': Grading
    }

  return app