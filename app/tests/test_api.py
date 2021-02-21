import pytest
import json
import requests
from app.application import create_app

class TestConfig:
    """Base config."""
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    SWAGGER_URL = '/api/docs'  
    API_URL = '/static/swagger.yaml'  
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
    MONGO_DB = 'flaskdb'
    MONGODB_HOST = 'mongomock://localhost/'

FAKE_TESTING_RECORD = {
"MemberNationalAssociationId" : "fakey-fake-id",
"MemberFirstName" : "Faker",
"MemberLastName" : "Fake", 
"MemberEmail" : "fakey@fake.com", 
"LicenseInfo" : [ 
  { "agency" : "HI", "number" : "123", "type" : "Broker"  },
  { "agency" : "AZ", "number" : "456", "type" : "Broker" },
  { "agency" : "OH", "number" : "789", "type" : "Agent" }
  ] 
}
FAKE_TESTING_RECORD2 = {
"MemberNationalAssociationId" : "fakey-fake-id2",
"MemberFirstName" : "Fakest",
"MemberLastName" : "Fake", 
"MemberEmail" : "fakey@fake.com", 
"LicenseInfo" : [ 
  { "agency" : "HI", "number" : "789", "type" : "Broker"  },
  { "agency" : "AZ", "number" : "123", "type" : "Broker" },
  { "agency" : "OH", "number" : "456", "type" : "Agent" }
  ] 
}

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app(TestConfig)

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client  # this is where the testing happens!

def test_home_page(test_client):
  response = test_client.get('/')

  assert response.status_code == 200
  assert b"Welcome to the ULI Registry app!" in response.data

def test_register_ULI(test_client):
  response = test_client.post('/register', data=json.dumps(FAKE_TESTING_RECORD), follow_redirects=True)
  response_data = json.loads(response.data)

  assert response.status_code == 201
  assert b"ULI saved successfully!" in response.data
  assert response_data["uli"] is not None

def test_query_ULI(test_client):
  response = test_client.post('/query', data=json.dumps(FAKE_TESTING_RECORD), follow_redirects=True)
  assert b"Found ULI" in response.data
  assert response.status_code == 200

def test_query_ULI_not_found(test_client):
  response = test_client.post('/query', data=json.dumps(FAKE_TESTING_RECORD2), follow_redirects=True)
  assert b"ULI Not Found!" in response.data
  assert response.status_code == 404

##############################################
############ Admin Functions #################
##############################################

FAKE_ADMIN_TOKEN = '_admin_token' #TODO: add real admin tokens
FAKE_GENERATION_RECORD = {   
    "token": FAKE_ADMIN_TOKEN,
    "NumLicensees": 100
}
FAKE_FIND_ULI_BODY = {
    "token" :"_admin_token",
    "uli" : "9999999999"
}
FAKE_REMOVE_ULI_BODY = {
    "token" :"_admin_token",
    "uli" : "9999999999"
}


def test_find_ULI(test_client):
  response = test_client.post('/register', data=json.dumps(FAKE_TESTING_RECORD), follow_redirects=True)
  response_data = json.loads(response.data)
  FIND_ULI_BODY = {
    "token" :"_admin_token",
    "uli" : response_data["uli"]
    }
  response = test_client.post('/find_licensee', data=json.dumps(FIND_ULI_BODY), follow_redirects=True)
 
  assert response.status_code == 200


def test_find_ULI_not_found(test_client):
  response = test_client.post('/find_licensee', data=json.dumps(FAKE_FIND_ULI_BODY), follow_redirects=True)
 
  assert response.status_code == 404

def test_admin_generate_licensees(test_client):
  response = test_client.post('/generate_licensees', data=json.dumps(FAKE_GENERATION_RECORD), follow_redirects=True)
  response_data = json.loads(response.data)

  assert response.status_code == 201
  assert b"100 generated!" in response.data
  assert response_data["status"] is True

def test_remove_licensee(test_client):
  response = test_client.post('/register', data=json.dumps(FAKE_TESTING_RECORD), follow_redirects=True)
  response_data = json.loads(response.data)
  REMOVE_ULI_BODY = {
    "token" :"_admin_token",
    "uli" : response_data["uli"]
  }

  response = test_client.delete('/remove_licensee', data=json.dumps(REMOVE_ULI_BODY), follow_redirects=True)

  assert response.status_code == 200
  assert b"deleted!" in response.data


def test_remove_licensee_not_found(test_client):
  response = test_client.delete('/remove_licensee', data=json.dumps(FAKE_REMOVE_ULI_BODY), follow_redirects=True)

  assert response.status_code == 404
  assert b"not found!" in response.data




