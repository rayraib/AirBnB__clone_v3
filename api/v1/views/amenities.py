#!/usr/bin/python3
''' blueprint for state '''
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models import State
from models import City
from models import Amenity


@app_views.route('/amenities/', methods=["GET"], strict_slashes=False)
@app_views.route('/amenities/<a_id>', methods=["GET"], strict_slashes=False)
def amenities(a_id=None):
    ''' retrieves a list of all amenities'''

    if a_id is None:
        my_amenities = storage.all("Amenity")
        amenities = [value.to_dict() for key, value in my_amenities.items()]
        return jsonify(amenities)

    amenities = storage.get("Amenity", a_id)
    if amenities is None:
        abort(404)

    return jsonify(amenities.to_dict())


@app_views.route('/amenities/<a_id>', methods=["DELETE"], strict_slashes=False)
def delete_amenity(a_id):
    '''Deletes an amenity based on its id'''

    amenities = storage.get("Amenity", a_id)
    if amenities is None:
        abort(404)

    amenities.delete()
    return jsonify({})


@app_views.route('/amenities', methods=["POST"], strict_slashes=False)
def create_amenity():
    ''' Creates an Amenity '''
    try:
        content = request.get_json()
    except:
        return (jsonify({"error": "Not a JSON"}), 400)
    name = content.get("name")
    if name is None:
        return (jsonify({"error": "Missing name"}), 400)

    new_amenity = Amenity()
    new_amenity.name = name
    new_amenity.save()
    return (jsonify(new_amenity.to_dict()), 201)


@app_views.route('/amenities/<a_id>', methods=["PUT"], strict_slashes=False)
def update_amenity(a_id):
    ''' updates an amenity '''

    try:
        content = request.get_json()
    except:
        return (jsonify({"error": "Not a JSON"}), 400)

    my_amenity = storage.get("Amenity", a_id)
    if my_amenity is None:
        abort(404)

    for key, value in content.items():
        if key != "id" or key != "created_at" or key != "updated_at":
            setattr(my_amenity, key, value)

    my_amenity.save()
    return jsonify(my_amenity.to_dict())
