#!/usr/bin/env python
# encoding: utf-8
import os
import settings
import json
from models import Member
from registry import search_licensee, generate_licensees #, create_licensee
from flask import Flask, request, jsonify
from mongoengine import *

app = Flask(__name__)
connect(host='mongodb://' + os.environ['MONGODB_USERNAME'] + ':' + os.environ['MONGODB_PASSWORD'] + '@' + os.environ['MONGODB_HOSTNAME'] + ':27017/' + os.environ['MONGODB_DATABASE'])

@app.route('/')
def index():
    return jsonify(
        status=True,
        message='Welcome to the ULI Registry app!'
    )

@app.route('/query', methods=['POST'])
def licensee():
  record = json.loads(request.data)
  #license info optional
  if record.get('LicenseInfo') is None:
     record['LicenseInfo'] = ""

  member = Member(MemberNationalAssociationId=record['MemberNationalAssociationId'],
                  MemberFirstName=record['MemberFirstName'],
                  MemberLastName=record['MemberLastName'],
                  MemberEmail=record['MemberEmail'],
                  LicenseInfo=record['LicenseInfo']
          )
          
  result = search_licensee(member)

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

@app.route('/register', methods=['POST'])
def registerLicensee():
  record = json.loads(request.data)
  if record.get('LicenseInfo') is None:
     record['LicenseInfo'] = ""
  
  member = Member(MemberNationalAssociationId=record['MemberNationalAssociationId'],
                  MemberFirstName=record['MemberFirstName'],
                  MemberLastName=record['MemberLastName'],
                  MemberEmail=record['MemberEmail'],
                  LicenseInfo=record['LicenseInfo']
          )
  result = search_licensee(member)
  
  if result['has_error']:
    return jsonify(
      status=False,
      message = result.get('status_message')
    ), 201

  if result['has_match']:
      #We've found possible Licensees that match the registered data, return them
      return jsonify(
          status=True,
          message = result.get('status', 'ULI May Exist!')
      ), 201
      
  else:
      #We havent matched, create a new user and return ULI
      ULI = member.save()
      return jsonify(
          status=True,
          uli=str(ULI.id), 
          message='ULI saved successfully!'
      ), 201


@app.route('/generate_licensees', methods=['POST'])
def generateLicensees():
  post_data = request.get_json(force=True)
  num_licensees = generate_licensees(post_data)
  return jsonify(status=True,message=str(num_licensees) + ' generated!'), 201


if __name__ == "__main__":
    ENVIRONMENT_DEBUG = os.environ.get("APP_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("APP_PORT", 5000)
    app.run(host='0.0.0.0', port=ENVIRONMENT_PORT, debug=ENVIRONMENT_DEBUG)
