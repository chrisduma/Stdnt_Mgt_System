from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import get_jwt_identity
from werkzeug.security import generate_password_hash
from http import HTTPStatus
from ..models.admin import Admin
from ..utils.decorators import is_admin
# from datetime import datetime


admin_namespace = Namespace('admin', description='Namespace for Admins')


#  --- serializers ---

admin_signup_model = admin_namespace.model(
    'Admin_Signup', {
        'full_name': fields.String(required=True, description="Admin's Full_Name"),
        'username': fields.String(required=True, description="Admin's username"),
        'email': fields.String(required=True, description="Admin's Email"),
        'password': fields.String(required=True, description="Admin's Password")
    }
)

admin_model = admin_namespace.model(
    'Admin', {
        'id': fields.Integer(description="Admin's User ID"),
        'full_name': fields.String(required=True, description="Admin's Full_Name"),
        'username': fields.String(required=True, description="Admin's username"),
        'email': fields.String(required=True, description="Admin's Email"),
        'role': fields.String(required=True, description='user role in school'),
        # 'created_on': fields.DateTime(description='Date&time when the admin was added')
    }
)



# --- admin routing ---
@admin_namespace.route('')
class Get_All_Admins(Resource):

    @admin_namespace.marshal_list_with(admin_model)
    @admin_namespace.doc(description="Retrieve All Admins")
    @is_admin()
    def get(self):
        
        """ Retrieve All Admins """
        admins = Admin.query.all()

        return admins, HTTPStatus.OK



# register/create admins
@admin_namespace.route('/register')
class Register_Admin(Resource):

    @admin_namespace.expect(admin_signup_model)
    # Uncomment the @is_admin() decorator below after registering the first admin
    # This ensures that only an existing admin can register a new admin account on the app
    # @is_admin()
    @admin_namespace.doc(description = "Register an Admin")
    def post(self):
        
        """ Register an Admin """        
        data = admin_namespace.payload

        # Check if the admin account already exists
        admin = Admin.query.filter_by(username=data['username'], email=data['email']).first()
        if admin:
            return {"message": "Admin Account Already Exists"}, HTTPStatus.CONFLICT


        new_admin = Admin(
            full_name = data['full_name'],
            username = data['username'],
            email = data['email'],
            password_hash = generate_password_hash(data['password']),
            # created_on = datetime.utcnow,
            role = 'admin'
        )

        new_admin.save()

        # resp -> response
        admin_resp = {}

        admin_resp['id'] = new_admin.id
        admin_resp['full_name'] = new_admin.full_name
        admin_resp['username'] = new_admin.username
        admin_resp['email'] = new_admin.email
        admin_resp['role'] = new_admin.role
        # admin_resp['created_on'] = new_admin.created_on

        return admin_resp, HTTPStatus.CREATED



# retrieve, update & delete admins
@admin_namespace.route('/<int:admin_id>')
class Get_Update_Delete_Admins(Resource):
    
    @admin_namespace.marshal_with(admin_model)
    @admin_namespace.doc(description = "Retrieve an Admin's Details by ID")
    @is_admin()
    def get(self, admin_id):
        
        """ Retrieve an Admin's Details by ID """

        admin = Admin.get_admin_by_id(admin_id)
        return admin, HTTPStatus.OK
    


    @admin_namespace.expect(admin_signup_model)
    @admin_namespace.doc(description = "Update an Admin's Details by ID (Admins Only)")
    @is_admin()
    def put(self, admin_id):
        
        """ Update an Admin's Details by ID """

        admin = Admin.get_admin_by_id(admin_id)

        current_admin = get_jwt_identity()
        if current_admin != admin_id:
            return {"message": "Admin Access_Denied"}, HTTPStatus.FORBIDDEN

        data = admin_namespace.payload

        admin.full_name = data['full_name']
        admin.username = data['username']
        admin.email = data['email']
        admin.password_hash = generate_password_hash(data['password'])

        admin.update()

        admin_resp = {}

        admin_resp['id'] = admin.id
        admin_resp['full_name'] = admin.full_name
        admin_resp['username'] = admin.username
        admin_resp['email'] = admin.email
        admin_resp['role'] = admin.role
        # admin_resp['created_on'] = admin.created_on
        

        return admin_resp, HTTPStatus.OK
    
    @admin_namespace.doc(description = "Delete an Admin by ID")
    @is_admin()
    def delete(self, admin_id):
        
        """ Delete an Admin by ID """

        admin = Admin.get_admin_by_id(admin_id)

        admin.delete()

        return {"message": "Admin Deleted"}, HTTPStatus.OK