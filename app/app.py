import os
import settings
import json
from controllers.mongo import application, request, jsonify
from controllers.registry import search_licensee2, create_licensee, generate_licensees, remove_licensee, find_licensee

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
    
  uli = result['uli']
  if uli is not None:
    return jsonify(
      status=True,
      message = result.get('status', 'Found ULI!'),
      uli = str(uli)
    ), 201

  return jsonify(
    status=True,
    message='ULI Not Found!'
  ), 404

@application.route('/register', methods=['POST'])
def registerLicensee():
  post_data = request.get_json(force=True)
  result = search_licensee2(post_data)

  uli = result['uli']
  if uli is not None:
      return jsonify(
          status=True,
          message = result.get('status', "Found ULI!"),
          uli = str(uli)
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

### ADMIN METHODS ###
API_KEY = '_admin_token' #TODO: add real admin tokens

@application.route('/find_licensee', methods=['POST'])
def getLicensee():
  """This method fetches ULIs by Id"""
  post_data = request.get_json(force=True)
  api_key = post_data.get('token', None)
  uli = post_data.get('uli', None)

  if api_key is None or api_key != API_KEY:
    return jsonify(
        status=False,
        message='Invalid Access Token!'
    ), 403

  if uli is None:
    return jsonify(
        status=False,
        message='uli is required when making this request!'
    ), 400

  count = find_licensee(uli)

  if count == 1:
    return jsonify(
        status=True,
        message='uli: ' + uli + ' found!'
    ), 200
  else:
    return jsonify(
        status=False,
        message='uli: ' + uli + ' not found!'
    ), 404
  
@application.route('/remove_licensee', methods=['DELETE'])
def removeLicensee():
  """This method is primarily used for testing purposes and requires a token"""
  post_data = request.get_json(force=True)
  
  api_key = post_data.get('token', None)
  uli = post_data.get('uli', None)

  if api_key is None or api_key != API_KEY:
    return jsonify(
        status=False,
        message='Invalid Access Token!'
    ), 403

  if uli is None:
    return jsonify(
        status=False,
        message='uli is required when making this request!'
    ), 400

  count = remove_licensee(uli)

  if count == 1:
    return jsonify(
        status=True,
        message='uli: ' + uli + ' deleted!'
    ), 200
  else:
    return jsonify(
        status=False,
        message='uli: ' + uli + ' not found!'
    ), 404


if __name__ == "__main__":
    ENVIRONMENT_DEBUG = os.environ.get("APP_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("APP_PORT", 5000)
    application.run(host='0.0.0.0', port=ENVIRONMENT_PORT, debug=ENVIRONMENT_DEBUG)
