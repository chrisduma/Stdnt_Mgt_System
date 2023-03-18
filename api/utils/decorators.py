from ..models.users import User
from flask_jwt_extended import get_jwt, verify_jwt_in_request
from functools import wraps
from http import HTTPStatus



# getting an authorized user's role 
def get_user_role(id:int):
    
    user = User.query.filter_by(id=id).first()

    if user:
        return user.role
    else:
        return None
    

# verifying an admin's access
def is_admin():
    def wrapper(cd):
        @wraps(cd)

        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if get_user_role(claims['sub']) == 'admin':
                return cd(*args, **kwargs)
            else:
                return {'message': "Admin access required"}, HTTPStatus.FORBIDDEN
        return decorator
    return wrapper
