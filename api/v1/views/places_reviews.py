#!/usr/bin/python3
''' blueprint for Review'''
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models import State
from models import City
from models import Amenity
from models import User
from models import Place
from models import Review


@app_views.route("/places/<place_id>/reviews",
                 methods=["GET"], strict_slashes=False)
def place_reviews(place_id):
    '''Retrives a list of all the places reviews'''

    my_place = storage.get("Place", place_id)
    if my_place is None:
        abort(404)

    my_reviews = my_place.reviews
    my_reviews = [review.to_dict() for review in my_reviews]

    return (jsonify(my_reviews), 200)


@app_views.route("/reviews/<review_id>", methods=["GET"], strict_slashes=False)
def get_review(review_id):
    ''' Retrieve a review based on its id'''

    my_review = storage.get("Review", review_id)
    if my_review is None:
        abort(404)
    return (jsonify(my_review.to_dict()), 200)


@app_views.route("/reviews/<review_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_review(review_id):
    ''' Delete a review based on its id'''

    my_review = storage.get("Review", review_id)
    if my_review is None:
        abort(404)
    my_review.delete()

    return (jsonify({}), 200)


@app_views.route("/places/<place_id>/reviews",
                 methods=["POST"], strict_slashes=False)
def create_review(place_id):

    try:
        content = request.get_json()
    except:
        return (jsonify({"error": "Not a JSON"}), 400)

    my_place = storage.get("Place", place_id)
    if my_place is None:
        abort(404)

    user_id = content.get("user_id")
    if user_id is None:
        return (jsonify({"error": "Missing user_id"}), 400)

    my_user = storage.get("User", user_id)
    if my_user is None:
        abort(404)

    text = content.get("text")
    if text is None:
        return (jsonify({"error": "Missing text"}), 400)

    new_review = Review()
    new_review.place_id = my_place.id

    for key, val in content.items():
        setattr(new_review, key, val)

    new_review.save()
    return (jsonify(new_review.to_dict()), 201)


@app_views.route("/reviews/<review_id>",
                 methods=["PUT"], strict_slashes=False)
def update_review(review_id):
    ''' Update an existing review '''

    my_review = storage.get("Review", review_id)
    if my_review is None:
        abort(404)

    try:
        content = request.get_json()
    except:
        return (jsonify({"error": "Not a JSON"}), 400)

    not_allowed = ["id", "created_at", "updated_at", "user_id", "place_id"]
    for key, value in content.items():
        if key not in not_allowed:
            setattr(my_review, key, value)
    my_review.save()

    return (jsonify(my_review.to_dict()), 200)
