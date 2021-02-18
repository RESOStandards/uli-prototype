import json
from flask import current_app as app, request, jsonify
from .  import models
from . import registry

@app.route('/')
def index():
    return jsonify(
        status=True,
        message='Welcome to the ULI Registry app!'
    )

@app.route('/register', methods=['POST'])
def registerLicensee():
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


