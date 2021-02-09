import os
import settings
import json
from controllers.mongo import application, request, jsonify
from controllers.registry import search_licensee2, create_licensee, generate_licensees

@application.route('/')
def index():
    return jsonify(
        status=True,
        message='Welcome to the ULI Registry app!'
    )

@application.route('/query', methods=['POST'])
def licensee():
  post_data = request.get_json(force=True)
  result = search_licensee2(post_data)

  if result['has_error']:
    return jsonify(
      status=False,
      message = result.get('status_message')
    ), 201
    

  if result['has_match']:
    return jsonify(
      status=True,
      message = result.get('status', 'ULI May Exist!')
    ), 201


  return jsonify(
    status=True,
    message='ULI Not Found!'
  ), 404

@application.route('/register', methods=['POST'])
def registerLicensee():
  post_data = request.get_json(force=True)
  result = search_licensee2(post_data)
  if result['has_match']:
      #We've found possible Licensees that match the registered data, return them
      return jsonify(
          status=True,
          message = result.get('status', 'ULI May Exist!')
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


@application.route('/generate_licensees', methods=['POST'])
def generateLicensees():
  post_data = request.get_json(force=True)
  num_licensees = generate_licensees(post_data)
  return jsonify(status=True,message=str(num_licensees) + ' generated!'), 201


if __name__ == "__main__":
    ENVIRONMENT_DEBUG = os.environ.get("APP_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("APP_PORT", 5000)
    application.run(host='0.0.0.0', port=ENVIRONMENT_PORT, debug=ENVIRONMENT_DEBUG)
