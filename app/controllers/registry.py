import json, bson, random
from faker import Faker
from controllers.mongo import db, request
from controllers.utils import hide_MemberEmail, ordered, format_uli

# TODO: not sure whether this would work in production because the nested licensees would likely
# have different key or modification timestamp fields but would be the same if their defining license
# data matches, i.e. state, license number, and type
def match_licenses(licensees, licenses_to_check):
    for licensee in licensees: #for each licensee 
        for individual_license in licenses_to_check: # and every license provided in the search
            for license_held in licensee["license_data"]:
                if(ordered(individual_license) == ordered(license_held)): #order the json to make sure you get exact matches
                    return licensee


# TODO: this method will allow dupe records to be created with NRDS and distinct name parts...
def search_licensee(post_data):
    data = []
    possible_matches = 0

    #check MemberNationalAssociationId, and if matches, confirm first name last name match
    if post_data["MemberNationalAssociationId"] is not None:
        _licensees = db.registry.find({ "MemberNationalAssociationId": post_data["MemberNationalAssociationId"] })
        for licensee in _licensees:
            if(post_data["MemberFirstName"] == licensee["MemberFirstName"] and post_data["MemberLastName"] == licensee["MemberLastName"]):
                possible_matches += 1
                data.append(format_uli(licensee))

    #If no MemberNationalAssociationId search first name, last name, then check licenses
    if possible_matches == 0:
        #temp store licensees that are matched by license data
        matched_by_license = [] 

        #get the licenses provided by the search for comparison against licenses held by people with same first and last name
        #TODO: is license data ever passed with a search? 
        licenses_to_check = post_data.get("license_data", [])

        #pull users with matching first/last
        _licensees = db.registry.find({"$and": [{"MemberFirstName": post_data["MemberFirstName"]}, 
                                                {"MemberLastName": post_data["MemberLastName"]}]})
        
        #check every license submitted against every license held by people with same first and last name
        matched_by_license = match_licenses(_licensees, licenses_to_check)
        if matched_by_license is not None:
            possible_matches += 1
            data.append(format_uli(matched_by_license))
                
    data.append({"possible_matches:" : possible_matches})

    if possible_matches == 0:
        return None
    else:
        return data


# First Name
# Middle Name
# Last Name
# Full Name
# Nick Name
# License Number
# License State
# License Sub-Type (Agent, Managing Broker, etc. based on state law)
# NRDS Number
# Office Name
# Office ID
# Office Address  
def search_licensee2(post_data):
  status_message = ""
  has_error = False
  has_match = False
  uli = None

  MEMBER_NATIONAL_ASSOCIATION_ID = "MemberNationalAssociationId"
  MEMBER_FIRST_NAME =  "MemberFirstName"
  MEMBER_LAST_NAME =  "MemberLastName"
  LICENSE_DATA = "license_data"

  #TODO: add model and parameter deserializer
  member_national_association_id = post_data.get(MEMBER_NATIONAL_ASSOCIATION_ID, None)
  member_first_name = post_data.get(MEMBER_FIRST_NAME, None)
  member_last_name = post_data.get(MEMBER_LAST_NAME, None)
  license_data = post_data.get(LICENSE_DATA, [])

  # try and match by NRDS first
  if member_national_association_id is not None:
    licensees = db.registry.find({ MEMBER_NATIONAL_ASSOCIATION_ID: member_national_association_id })
    if licensees.count() > 1:
      has_error = True
      status_message = 'ERROR: more than one record was found with the given ' + MEMBER_NATIONAL_ASSOCIATION_ID
    elif licensees.count() == 1:
      if member_first_name == licensees[0].get(MEMBER_FIRST_NAME) and member_last_name == licensees[0].get(MEMBER_LAST_NAME):
        uli = licensees[0].get('_id')
        status_message = 'Found match for ' + MEMBER_NATIONAL_ASSOCIATION_ID + '=' + member_national_association_id
      else:
        has_error = True
        status_message = 'ERROR: identity information is not correct for the given ' + MEMBER_NATIONAL_ASSOCIATION_ID

  # if that doesn't yield results, match by license data and first + last name
  if not has_error and uli is None:
    for licenses in license_data:
      licenses = db.registry.find({ LICENSE_DATA : license_data, MEMBER_FIRST_NAME: member_first_name, MEMBER_LAST_NAME: member_last_name })
      if licenses.count() == 1:
        uli = licenses[0].get('_id')
        status_message = 'Found match for ' + LICENSE_DATA + ', ' + MEMBER_FIRST_NAME + ', ' + MEMBER_LAST_NAME
      elif licenses.count() > 1:
        has_error = True
        status_message = 'ERROR: more than one record was found with the given ' + LICENSE_DATA
      else:
        has_error = True
        status_message = 'ERROR: identity information is not correct for the given ' + LICENSE_DATA
  
  return {'status_message' : status_message, 'has_error': has_error, 'uli': uli}


#TODO: add parameter validation to the creation, no empty items allowed...
# Perhaps we move the validation of these items to here so this method can't be accidentally called?
def create_licensee(post_data):
  item = {
      "MemberNationalAssociationId": post_data["MemberNationalAssociationId"],
      "MemberFirstName": post_data["MemberFirstName"],
      "MemberLastName": post_data["MemberLastName"],
      "MemberEmail": post_data["MemberEmail"],
      "license_data": post_data["license_data"]
  }
  uli = db.registry.insert_one(item).inserted_id
  return uli

def remove_licensee(uli):
  """Deletes a licensee with the given ULI"""
  item = {
      "_id": bson.ObjectId(oid=str(uli)),
  }

  count = db.registry.delete_one(item).deleted_count
  return count

def find_licensee(uli):
  """Finds a licensee with the given ULI"""
  item = {
      "_id": bson.ObjectId(oid=str(uli)),
  }

  count = db.registry.count(item)
  return count

def generate_licensees(post_data):
  """Generates random licensee data for NumLicensees records"""
  num = post_data["NumLicensees"] or 0
  fake = Faker()

  types = ["Broker", "Agent", "Salesperson"]

  for _ in range(num):
    item = {
      "MemberNationalAssociationId": fake.pystr(30, 30),
      "MemberFirstName": fake.first_name(),
      "MemberLastName": fake.last_name(),
      "MemberEmail": fake.email(),
      "license_data": [
        {"agency": fake.state_abbr(),"number": str(fake.pyint()),"type": random.choice(types)}, 
        {"agency": fake.state_abbr(),"number": str(fake.pyint()),"type": random.choice(types)},
        {"agency": fake.state_abbr(),"number": str(fake.pyint()),"type": random.choice(types)} 
      ]
    }
    print(item, flush=True)
    db.registry.insert_one(item)

  return num
  
