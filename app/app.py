import os
import settings
import json
from controllers.mongo import application, request, jsonify
from controllers.registry import search_licensee, create_licensee

@application.route('/')
def index():
    return jsonify(
        status=True,
        message='Welcome to the ULI Registry app!'
    )

@application.route('/query', methods=['POST'])
def licensee():
    post_data = request.get_json(force=True)
    _licensees = search_licensee(post_data)
    if _licensees:
        #We've found possible Licensees that match the registered data, return them
        return jsonify(
            status=True,
            data=_licensees,
            message='ULI May Exist!'
        ), 201
    return jsonify(
        status=True,
         message='ULI Not Found!'
    )

@application.route('/register', methods=['POST'])
def registerLicensee():
    post_data = request.get_json(force=True)
    _licensees = search_licensee(post_data)
    if _licensees:
        #We've found possible Licensees that match the registered data, return them
        return jsonify(
            status=True,
            data=_licensees,
            message='ULI May Exist!'
        ), 201
        
    else:
        #We havent matched, create a new user and return ULI
        data = create_licensee(post_data)
        return jsonify(
            status=True,
            uli=str(data),
            message='ULI saved successfully!'
        ), 201

    return jsonify(
            status=True,
            message='Unexpected Error!'
        ), 500
    

if __name__ == "__main__":
    ENVIRONMENT_DEBUG = os.environ.get("APP_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("APP_PORT", 5000)
    application.run(host='0.0.0.0', port=ENVIRONMENT_PORT, debug=ENVIRONMENT_DEBUG)