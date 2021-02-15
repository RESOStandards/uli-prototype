import json
import random
from faker import Faker
from utils import ordered
from models import Member
from flask import jsonify
from mongoengine import *

# TODO: not sure whether this would work in production because the nested licensees would likely
# have different key or modification timestamp fields but would be the same if their defining license
# data matches, i.e. state, license number, and type
def match_licenses(licensees, licenses_to_check):
    for licensee in licensees: #for each licensee 
        for individual_license in licenses_to_check: # and every license provided in the search
            for license_held in licensee["LicenseInfo"]:
                if(ordered(individual_license) == ordered(license_held)): #order the json to make sure you get exact matches
                    return licensee


# TODO: this method will allow dupe records to be created with NRDS and distinct name parts...
def search_licensee(member):
  #check MemberNationalAssociationId, and if matches, confirm first name last name match
  if member.MemberNationalAssociationId is not None:
      stored_licensees = Member.objects(MemberNationalAssociationId=member.MemberNationalAssociationId)
      for licensee in stored_licensees:
          if(member.MemberFirstName == licensee["MemberFirstName"] and member.MemberLastName == licensee["MemberLastName"]):
              return {'has_match': True, 'status_message' : 'Found match!', 'has_error': False}

  #temp store licensees that are matched by license data
  matched_by_license = [] 

  #get the licenses provided by the search for comparison against licenses held by people with same first and last name
  #TODO: is license data ever passed with a search? 
  licenses_to_check = member.LicenseInfo

  #pull users with matching first/last using query sets
  _licensees = Member.objects.filter(Q(MemberFirstName=member.MemberFirstName) & 
                                      Q(MemberLastName=member.MemberLastName))
  
  #check every license submitted against every license held by people with same first and last name
  matched_by_license = match_licenses(_licensees, licenses_to_check)
  if matched_by_license is not None:
    return {'has_match': True, 'status_message' : 'Found match!', 'has_error': False}
              
  return {'has_match': False, 'status_message' : 'ULI Not Found!', 'has_error': False}


def search_licensee2(post_data):
  status_message = ""
  has_error = False
  has_match = False

  MEMBER_NATIONAL_ASSOCIATION_ID = "MemberNationalAssociationId"
  MEMBER_FIRST_NAME =  "MemberFirstName"
  MEMBER_LAST_NAME =  "MemberLastName"
  LicenseInfo = "LicenseInfo"

  #TODO: add model and paraeter deserializer
  member_national_association_id = post_data.get(MEMBER_NATIONAL_ASSOCIATION_ID, None)
  member_first_name = post_data.get(MEMBER_FIRST_NAME, None)
  member_last_name = post_data.get(MEMBER_LAST_NAME, None)
  LicenseInfo = post_data.get(LicenseInfo, [])

  if member_national_association_id is not None:
      licensees = db.registry.find({ MEMBER_NATIONAL_ASSOCIATION_ID: member_national_association_id })
      if licensees.count() > 1:
        has_error = True
        status_message = 'ERROR: more than one record was found with the given ' + MEMBER_NATIONAL_ASSOCIATION_ID
      elif licensees.count() == 1:
        if member_first_name == licensees[0].get(MEMBER_FIRST_NAME) and member_last_name == licensees[0].get(MEMBER_LAST_NAME):
          has_match = True
          status_message = 'Found match for ' + MEMBER_NATIONAL_ASSOCIATION_ID + '=' + member_national_association_id
          #TODO: return ULI in this case? 
        else:
          has_error = True
          status_message = 'ERROR: identity information is not correct for the given ' + MEMBER_NATIONAL_ASSOCIATION_ID


	#• First Name
	#• Middle Name
	#• Last Name
	#• Full Name
	#• Nick Name
	#• License Number
	#• License State
	#• License Sub-Type (Agent, Managing Broker, etc. based on state law)
	#• NRDS Number
	#• Office Name
	#• Office ID
	#• Office Address  

  if not has_error and not has_match:
    for licenses in LicenseInfo:
      licenses = db.registry.find({LicenseInfo : LicenseInfo})
      for licensee in licenses:
        if member_first_name == licensee.get(MEMBER_FIRST_NAME) and member_last_name == licensee.get(MEMBER_LAST_NAME):
          has_match = True
              
  return {'has_match': has_match, 'status_message' : status_message, 'has_error': has_error}


#TODO: add parameter validation to the creation, no empty items allowed...
# Perhaps we move the validation of these items to here so this method can't be accidentally called?
def create_licensee(record):
    member = Member(MemberNationalAssociationId=record['MemberNationalAssociationId'],
                    MemberFirstName=record['MemberFirstName'],
                    MemberLastName=record['MemberLastName'],
                    MemberEmail=record['MemberEmail'],
                    LicenseInfo=record['LicenseInfo']
             )
    member.save()
    #print(member.to_json())
    return (member.to_json())

    #uli = db.registry.insert_one(member).inserted_id
    #return uli

def generate_licensees(post_data):
  num = post_data["NumLicensees"] or 0
  fake = Faker()
  types = ["Broker", "Agent", "Salesperson"]

  for _ in range(num):
    member = Member(MemberNationalAssociationId=fake.pystr(30, 30),
                    MemberFirstName=fake.first_name(),
                    MemberLastName=fake.last_name(),
                    MemberEmail=fake.email(),
                    LicenseInfo=[
                      {"agency": fake.state_abbr(),"number": str(fake.pyint()),"type": random.choice(types)}, 
                      {"agency": fake.state_abbr(),"number": str(fake.pyint()),"type": random.choice(types)},
                      {"agency": fake.state_abbr(),"number": str(fake.pyint()),"type": random.choice(types)} 
                    ]
             )
    member.save()

  return num