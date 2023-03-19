import unittest
from flask_jwt_extended import create_access_token
# from datetime import datetime
# from flask import json

from .. import create_app

from ..utils import db
from ..config.config import config_dict
from ..models.admin import Admin

class User_TestCase(unittest.TestCase):
    
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



    def test_admin(self):

        # Register an admin
        admin_signup_data = {
            "full_name": "test admin",
            "username": "admin",
            "email": "test_admin@gmail.com",
            "password": "password"
        }

        response = self.client.post('/admin/register', json=admin_signup_data)

        admin = Admin.query.filter_by(username='admin').first()

        assert admin.full_name == "test admin"

        assert admin.username == "admin"

        assert response.status_code == 201
        

        # Sign an admin in
        admin_login_data = {
            "username":"test_admin@gmail.com",
            "password": "password"
        }
        response = self.client.post('/auth/login', json=admin_login_data)

        assert response.status_code == 200

        token = create_access_token(identity=admin.id)

        headers = {
            "Authorization": f"Bearer {token}"
        }


#         # Retrieve all admins
        response = self.client.get('/admin', headers=headers)

        assert response.status_code == 200

        assert response.json == [{
            "id": 1,
            "full_name": "test admin",
            "username": "admin",
            "email": "test_admin@gmail.com",
            "role": "admin"
        }]


        # Retrieve an admin's details by ID
        response = self.client.get('/admin/1', headers=headers)

        assert response.status_code == 200

        assert response.json == {
            "id": 1,
            "full_name": "test admin",
            "username": "admin",
            "email": "test_admin@gmail.com",
            "role": "admin"
        }


        # Update an admin's details
        admin_update_data = {
            "id": 1,
            "full_name": "sample admin",
            "username": "admin",
            "email": "sample_admin@gmail.com",
            "password": "password"
        }

        response = self.client.put('/admin/1', json=admin_update_data, headers=headers)

        assert response.status_code == 200

        assert response.json == {
            "id": 1,
            "full_name": "sample admin",
            "username": "admin",
            "email": "sample_admin@gmail.com",
            "role": "admin"
        }


#         # # Delete an admin
        response = self.client.delete('/admin/1', headers=headers)

        assert response.status_code == 200