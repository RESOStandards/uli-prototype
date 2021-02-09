import json
import random
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

def search_licensee2(post_data):
  status_message = ""
  has_error = False
  has_match = False

  MEMBER_NATIONAL_ASSOCIATION_ID = "MemberNationalAssociationId"
  MEMBER_FIRST_NAME =  "MemberFirstName"
  MEMBER_LAST_NAME =  "MemberLastName"
  LICENSE_DATA = "license_data"

  #TODO: add model and paraeter deserializer
  member_national_association_id = post_data.get(MEMBER_NATIONAL_ASSOCIATION_ID, None)
  member_first_name = post_data.get(MEMBER_FIRST_NAME, None)
  member_last_name = post_data.get(MEMBER_LAST_NAME, None)
  license_data = post_data.get(LICENSE_DATA, [])

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
    for licenses in license_data:
      licenses = db.registry.find({LICENSE_DATA : license_data})
      for licensee in licenses:
        if member_first_name == licensee.get(MEMBER_FIRST_NAME) and member_last_name == licensee.get(MEMBER_LAST_NAME):
          has_match = True
              
  return {'has_match': has_match, 'status_message' : status_message, 'has_error': has_error}


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

def generate_licensees(post_data):
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
  


