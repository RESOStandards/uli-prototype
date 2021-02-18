from . import utils
from . import models
import random
from faker import Faker
from flask_mongoengine import *
from mongoengine import *

# TODO: not sure whether this would work in production because the nested licensees would likely
# have different key or modification timestamp fields but would be the same if their defining license
# data matches, i.e. state, license number, and type
def match_licenses(licensees, licenses_to_check):
    for licensee in licensees: #for each licensee 
      for individual_license in licenses_to_check: # and every license provided in the search
          for license_held in licensee["LicenseInfo"]:
              if(utils.ordered(individual_license) == utils.ordered(license_held)): #order the json to make sure you get exact matches
                  return licensee

# TODO: this method will allow dupe records to be created with NRDS and distinct name parts...
def search_licensee(member):
  status_message = ""
  has_error = False
  has_match = False
  uli = None
  
  #check MemberNationalAssociationId, and if matches, confirm first name last name match
  if member.MemberNationalAssociationId is not None:
      licensees = models.Member.objects(MemberNationalAssociationId=member.MemberNationalAssociationId)
      if licensees.count() > 1:
        has_error = True
        status_message = 'ERROR: More than one record was found with the given MemberNationalAssociationId'
      elif licensees.count() == 1:
          if(member.MemberFirstName == licensees[0]["MemberFirstName"] and member.MemberLastName == licensees[0]["MemberLastName"]):
            has_match = True
            status_message = 'Found match!'
            uli = str(licensees[0].id)

  if not has_error and not has_match:
    #temp store licensees that are matched by license data
    matched_by_license = [] 

    #get the licenses provided by the search for comparison against licenses held by people with same first and last name
    #TODO: is license data ever passed with a search? 
    licenses_to_check = member.LicenseInfo

    #pull users with matching first/last using query sets
    _licensees = models.Member.objects.filter(Q(MemberFirstName=member.MemberFirstName) & 
                                        Q(MemberLastName=member.MemberLastName))
    
    #check every license submitted against every license held by people with same first and last name
    matched_by_license = match_licenses(_licensees, licenses_to_check)
    if matched_by_license is not None:
      has_match = True
      status_message = 'Found match!'
      uli = str(matched_by_license.id)
              
  return {'has_match': has_match, 'status_message' : status_message, 'has_error': has_error, 'uli': uli}
 
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

def remove_licensee(uli):
  """Deletes a licensee with the given ULI"""
  try:
    member = Member.objects.get(id=uli).delete()
    return True
  except:
    pass

  return False

def find_licensee(uli):
  """Finds a licensee with the given ULI"""
  try:
    count = Member.objects.get(id=uli)
  except:
    count = None

  return count

def generate_licensees(num_licensees):
  num = num_licensees or 0
  fake = Faker()
  types = ["Broker", "Agent", "Salesperson", "Appraiser"]

  for _ in range(num):
    member = models.Member(MemberNationalAssociationId=fake.pystr(30, 30),
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

