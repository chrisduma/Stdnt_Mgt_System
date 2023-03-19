from flask_restx import Namespace, Resource, fields
from ..models.users import User
from ..utils.decorators import is_admin
from ..utils.blacklist import BLACKLIST
from werkzeug.security import check_password_hash #generate_password_hash
from http import HTTPStatus
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required, get_jwt



auth_namespace = Namespace('auth', description='Namespace for Authentication')



# --- serializers ---

User_Model = auth_namespace.model(
  'User', {
    'id': fields.Integer(description='unique identifier'),
    'full_name': fields.String(required=True, description='Full_Name'),
    'username': fields.String(required=True, description='Prefered username'),
    'email': fields.String(required=True, description='An email'),
    'password_hash': fields.String(required=True, description='A Password'),
    'role': fields.String(required=True, enum=['ADMIN','STUDENT']),
    'created_on': fields.DateTime(description='This shows when the user was created')
  }
)

# on login for registered user
Login_Model = auth_namespace.model(
  'Login', {
    'username': fields.String(required=True, description='A username'),
    'password': fields.String(required=True, description='A Password')
  }
)



# --- routing ---


@auth_namespace.route('/users')
class Get_All_Users(Resource):
    @auth_namespace.marshal_with(User_Model)
    @auth_namespace.doc(description="Retrieve all users (Admins Only)")
    @is_admin()
    def get(self):
        
        """ Retrieve all Users """
        users = User.query.all()

        return users, HTTPStatus.OK
    


#Login
@auth_namespace.route('/login')
class Login(Resource):
  
  @auth_namespace.expect(Login_Model)
  def post(self):
    
    data = auth_namespace.payload 

    username = data['username']
    password = data['password']

    user = User.query.filter_by(username=username).first()


    if (user is not None) and check_password_hash(user.password_hash, password):

      access_token = create_access_token(identity=user.id)
      refresh_token = create_refresh_token(identity=user.id)

      response = {
        'access_token': access_token,
        'refresh_token': refresh_token
      }

      print(response)
      return response, HTTPStatus.CREATED
    

# on Refresh
@auth_namespace.route('/refresh')
class Refresh(Resource):

  @jwt_required(refresh=True)
  def post(self):

    user = get_jwt_identity()

    access_token = create_access_token(identity=user)

    return {'access_token': access_token}, HTTPStatus.OK
  


# log_out
@auth_namespace.route('/logout')
class Logout(Resource):
    
  @jwt_required(verify_type=False)
  def post(self):
        
    """ Logout / Revoke Access """
        
    access_token = get_jwt() #jwt gives you in out access, 'revoke' is one of its property types

    revoke = access_token["revoke"]
    token_type = access_token["type"]
    BLACKLIST.add(revoke)
    
    return {"message": f"{token_type.capitalize()} access successfully revoked"}, HTTPStatus.OK
