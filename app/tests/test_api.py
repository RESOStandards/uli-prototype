import pytest
import json
import requests
from app.application import create_app

class TestConfig:
    """Base config."""
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
    MONGO_DB = 'flaskdb'
    MONGODB_HOST = 'mongomock://localhost/'

__ULI__ = None
FAKE_ADMIN_TOKEN = '_admin_token' #TODO: add real admin tokens
ULI_FOUND_MESSAGE = 'Unique Licensee Identifier: %s found!'
ULI_NOT_FOUND_MESSAGE = 'Unique Licensee Identifier: %s found!'
FAKE_TESTING_RECORD = {
"MemberNationalAssociationId" : "fakey-fake-id",
"MemberFirstName" : "Faker",
"MemberLastName" : "Fake", 
"MemberEmail" : "fakey@fake.com", 
"LicenseInfo" : [ 
  { "agency" : "HI", "number" : "fake", "type" : "Broker"  },
  { "agency" : "AZ", "number" : "fake", "type" : "Broker" },
  { "agency" : "OH", "number" : "fake", "type" : "Agent" }
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
  #__ULI__ = (response_data['uli'])
  response_data = json.loads(response.data)

  assert response.status_code == 201
  assert b"ULI saved successfully!" in response.data
  assert response_data["uli"] is not None

  #ensure the record was inserted
  FAKE_FIND_ULI_BODY = {
    "token" :"_admin_token",
    "uli" : response_data["uli"]
    }
  response = test_client.post('/find_licensee', data=json.dumps(FAKE_FIND_ULI_BODY), follow_redirects=True)
 
  assert response.status_code == 200


def test_ULI_not_found(test_client):
  FAKE_FIND_ULI_BODY = {
    "token" :"_admin_token",
    "uli" : "9999999999"
    }
  response = test_client.post('/find_licensee', data=json.dumps(FAKE_FIND_ULI_BODY), follow_redirects=True)
 
  assert response.status_code == 404
  

# def test_successful_query(wait_for_api):
#   request_session, api_url = wait_for_api
#   item = request_session.post('%s/query' % api_url, data = FAKE_TESTING_RECORD).json()
#   assert item['uli'] == __ULI__
#   assert item['message'] == 'Found ULI!'

# def test_remove_licensee(wait_for_api):
#   request_session, api_url = wait_for_api
#   item = request_session.delete('%s/remove_licensee' % api_url, data = '{"token": "%s", "uli": "%s"}' % (FAKE_ADMIN_TOKEN, __ULI__)).json()
#   assert item['message'] == 'uli: ' + __ULI__ + ' deleted!'

#   inserted = request_session.post('%s/find_licensee' % api_url, data = '{"token": "%s", "uli": "%s"}' % (FAKE_ADMIN_TOKEN, __ULI__)).json() 
#   assert inserted['message'] == 'uli: ' + __ULI__ + ' not found!'
#assert 'uli' in response.data
