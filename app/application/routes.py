import json
from flask import current_app as app, request, jsonify
from .  import models
from . import registry

@app.route('/')
def index():
  """This method returns a one line home page"""
  return jsonify(
      status=True,
      message='Welcome to the ULI Registry app!'
  )

@app.route('/query', methods=['POST'])
def licensee():
  """This method is not often used but can tell you if a ULI exists for a member without creating one"""
  record = json.loads(request.data)
  #license info optional
  if record.get('LicenseInfo') is None:
     record['LicenseInfo'] = ""

  member = models.Member(MemberNationalAssociationId=record['MemberNationalAssociationId'],
                  MemberFirstName=record['MemberFirstName'],
                  MemberLastName=record['MemberLastName'],
                  MemberEmail=record['MemberEmail'],
                  LicenseInfo=record['LicenseInfo']
          )
          
  result = registry.search_licensee(member)

  if result['has_error']:
    return jsonify(
      status=False,
      message = result.get('status_message')
    ), 200
    
  if result['has_match']:
    return jsonify(
      status=True,
      message = result.get('status', 'Found ULI!'),
      uli = result.get('uli')
    ), 200

  return jsonify(
    status=True,
    message='ULI Not Found!',
    uli = result.get('uli')
  ), 404

@app.route('/register', methods=['POST'])
def registerLicensee():
  """This method is used for registering a new ULI if one does exist"""
  record = json.loads(request.data)
  if record.get('LicenseInfo') is None:
     record['LicenseInfo'] = ""
  
  member = models.Member(MemberNationalAssociationId=record['MemberNationalAssociationId'],
                  MemberFirstName=record['MemberFirstName'],
                  MemberLastName=record['MemberLastName'],
                  MemberEmail=record['MemberEmail'],
                  LicenseInfo=record['LicenseInfo']
          )
  result = registry.search_licensee(member)
  
  if result['has_error']:
    return jsonify(
      status=False,
      message = result.get('status_message'),
      uli = result.get('uli')
    ), 201

  if result['has_match']:
      #We've found possible Licensees that match the registered data, return them
      return jsonify(
          status=True,
          message = result.get('status', "Found ULI!"),
          uli = result.get('uli')
      ), 201
      
  else:
      #We havent matched, create a new user and return ULI
      ULI = member.save()
      return jsonify(
          status=True,
          uli=str(ULI.id), 
          message='ULI saved successfully!'
      ), 201


### ADMIN METHODS ###
API_KEY = '_api_key' #TODO: add real admin api keys/ tokens

@app.route('/generate_licensees', methods=['POST'])
def generateLicensees():
  """This method is primarily used for testing purposes and generates X number of fake licensees"""
  post_data = request.get_json(force=True)
  api_key=request.headers.get('X-API-KEY')
  num_licensees = post_data.get('NumLicensees', None)
  
  if api_key is None or api_key != API_KEY:
    return jsonify(
        status=False,
        message='Invalid API Key!'
    ), 403

  num_licensees = registry.generate_licensees(num_licensees)
  
  return jsonify(
        status=True,
        message=str(num_licensees) + ' generated!'
    ), 201

@app.route('/find_licensee', methods=['POST'])
def getLicensee():
  """This method fetches ULIs by Id"""
  api_key=request.headers.get('X-API-KEY')
  post_data = request.get_json(force=True)
  uli = post_data.get('uli', None)

  if api_key is None or api_key != API_KEY:
    return jsonify(
        status=False,
        message='Invalid API Key!'
    ), 403

  if uli is None:
    return jsonify(
        status=False,
        message='uli is required when making this request!'
    ), 400

  licensee = registry.find_licensee(uli)

  if licensee:
    return jsonify(
        status=True,
        message='ULI found!'
    ), 200
  else:
    return jsonify(
        status=False,
        message='uli: ' + uli + ' not found!'
    ), 404
  
@app.route('/remove_licensee', methods=['DELETE'])
def removeLicensee():
  """This method is primarily used for testing purposes and requires an api key"""
  post_data = request.get_json(force=True)
  api_key=request.headers.get('X-API-KEY')
  uli = post_data.get('uli', None)

  if api_key is None or api_key != API_KEY:
    return jsonify(
        status=False,
        message='Invalid API Key!'
    ), 403

  if uli is None:
    return jsonify(
        status=False,
        message='uli is required when making this request!'
    ), 400

  licensee = registry.remove_licensee(uli)

  if licensee:
    return jsonify(
        status=True,
        message='uli: ' + uli + ' deleted!'
    ), 200
  else:
    return jsonify(
        status=False,
        message='uli: ' + uli + ' not found!'
    ), 404
