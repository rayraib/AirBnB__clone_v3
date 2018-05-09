#!/usr/bin/python3
''' blueprint for state '''
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models import State
from models import City
from models import Amenity
from models import User


@app_views.route('/users', methods=["GET"], strict_slashes=False)
@app_views.route('/users/<u_id>', methods=["GET"], strict_slashes=False)
def users(u_id=None):
    ''' retrieves a list of all amenities'''

    if u_id is None:
        my_users = storage.all("User")
        users = [value.to_dict() for key, value in my_users.items()]
        return jsonify(users)

    users = storage.get("User", u_id)
    if users is None:
        abort(404)

    return jsonify(users.to_dict())


@app_views.route('/users/<u_id>', methods=["DELETE"], strict_slashes=False)
def delete_users(u_id):
    '''Deletes an user based on its id'''

    user = storage.get("User", u_id)
    if user is None:
        abort(404)

    user.delete()
    return jsonify({})


@app_views.route('/users', methods=["POST"], strict_slashes=False)
def create_users():
    ''' Creates an User'''
    try:
        content = request.get_json()
    except:
        return (jsonify({"error": "Not a JSON"}), 400)
    email = content.get("email")
    if email is None:
        return (jsonify({"error": "Missing email"}))
    password = content.get("password")
    if password is None:
        return (jsonify({"error": "Missing password"}), 400)

    new_user = User()
    for key, value in content.items():
        setattr(new_user, key, value)
    new_user.save()
    return (jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<u_id>', methods=["PUT"], strict_slashes=False)
def update_users(u_id):
    ''' updates an user'''

    try:
        content = request.get_json()
    except:
        return (jsonify({"error": "Not a JSON"}), 400)

    my_user = storage.get("User", u_id)
    if my_user is None:
        abort(404)

    not_allowed = ["id", "created_at", "updated_at", "email"]
    for key, value in content.items():
        if key not in not_allowed:
            setattr(my_user, key, value)

    my_user.save()
    return jsonify(my_user.to_dict())
