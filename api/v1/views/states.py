#!/usr/bin/python3
''' blueprint for state '''
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models import State


@app_views.route('/states', methods=["GET"], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=["GET"], strict_slashes=False)
def state(state_id=None):
    ''' retrieves a list of all states'''
    if state_id is None:
        states = storage.all("State")
        my_states = [value.to_dict() for key, value in states.items()]
        return jsonify(my_states)

    my_states = storage.get("State", state_id)
    if my_states is not None:
        return jsonify(my_states.to_dict())
    abort(404)


@app_views.route('/states/<s_id>', methods=["DELETE"], strict_slashes=False)
def delete_states(s_id):
    '''Deletes an specific state based on its id'''

    my_state = storage.get("State", s_id)
    if my_state is None:
        abort(404)
    storage.delete(my_state)
    return (jsonify({}))


@app_views.route('/states', methods=["POST"], strict_slashes=False)
def post_states():

    try:
        content = request.get_json()
    except:
        return (jsonify({"error": "Not a JSON"}), 400)
    name = content.get("name")
    if name is None:
        return (jsonify({"error": "Missing name"}), 400)

    new_state = State()
    new_state.name = name
    new_state.save()

    return (jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=["PUT"], strict_slashes=False)
def update_states(state_id):
    '''Updates a state'''

    try:
        content = request.get_json()
    except:
        return (jsonify({"error": "Not a JSON"}), 400)

    my_state = storage.get("State", state_id)
    if my_state is None:
        abort(404)

    for key, value in content.items():
        if key != "id" or key != "created_at" or key != "updated_at":
            setattr(my_state, key, value)

    my_state.save()
    return jsonify(my_state.to_dict())
