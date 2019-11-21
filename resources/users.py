import models

from flask import request, jsonify, Blueprint
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user
from playhouse.shortcuts import model_to_dict

# first argument is blueprint name 
# second argument is import name

user = Blueprint('users', 'user')

@user.route('/register', methods=["POST"])
def register():
    # accepts a post request with new users email and password
    # see request payload analagous to req.body in express
    # This has all the data
    payload = request.get_json()

    if not payload['email'] or not payload['password']:
        return jsonify(status=400)
    # Make sure we handle:
    #  - Username/email has not been used before
    #  - Passwords match 
    try:
        # Won't throw an exception if email already in DB
        models.User.get(models.User.email ** payload['email']) 
        return jsonify(data={}, status={'code': 400, 'message': 'A user with that email already exists.'}) 
    except models.DoesNotExist:  
        payload['password'] = generate_password_hash(payload['password']) # Hash user's password
        new_user = models.User.create(**payload)
        # profile = models.Profile.create(user=new_user)

        # Start a new session with the new user
        login_user(new_user)
        user_dict = model_to_dict(new_user)
        print(user_dict)
        print(type(user_dict))

        # delete the password before sending user dict back to the client/browser
        del user_dict['password']
        return jsonify(data=user_dict, status={'code': 201, 'message': 'User created'})