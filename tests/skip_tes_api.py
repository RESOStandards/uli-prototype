import pytest
import requests
import json
from urllib.parse import urljoin
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from application import create_app
from flask import jsonify

FAKE_TESTING_ID = 'fakey-fake-id'
FAKE_TESTING_RECORD = '{ "UniqueLicenseeIdentifier": "%s", "MemberNationalAssociationId" : "%s", "MemberFirstName" : "Fakey", "MemberLastName" : "Fake", "MemberEmail" : "fakey@fake.com", "LicenseInfo" : [ { "agency" : "HI", "number" : "fake", "type" : "Broker" }, { "agency" : "AZ", "number" : "fake", "type" : "Broker" }, { "agency" : "OH", "number" : "fake", "type" : "Agent" } ] }' % (FAKE_TESTING_ID, FAKE_TESTING_ID)
FAKE_ADMIN_TOKEN = '_admin_token' #TODO: add real admin tokens
ULI_FOUND_MESSAGE = 'Unique Licensee Identifier: %s found!'

__ULI__ = None



@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app()
    flask_app.config.from_object('config.TestConfig')

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client  # this is where the testing happens!
# MONGODB_HOST = 'mongomock://localhost'


# # Invoking this fixture: 'function_scoped_container_getter' starts all services
# @pytest.fixture(scope="function")
# def wait_for_api(function_scoped_container_getter):
#   request_session = requests.Session()
#   retries = Retry(total=5,
#                   backoff_factor=0.1,
#                   status_forcelist=[500, 502, 503, 504])
#   request_session.mount('http://', HTTPAdapter(max_retries=retries))

#   service = function_scoped_container_getter.get("webserver").network_info[0]
#   api_url = "http://%s/" % (service.hostname)
#   assert request_session.get(api_url)
#   return request_session, api_url

def test_home_page(test_client):
  # TODO: add teardown that removes this record
  response = test_client.get('/')
  #print(response)
  assert response.status_code == 200
  assert b"Welcome to the ULI Registry app!" in response.data
  #assert response["message"]  == "Welcome to the ULI Registry app!"

def test_successful_registration(test_client):
#   # TODO: add teardown that removes this record
    response = test_client.post('/register', data = FAKE_TESTING_RECORD).json()
    print(response.data)
    #__ULI__ = response['uli']

#   #ensure that record was inserted
    inserted = test_client.post('/find_licensee', data = '{"token": "%s", "uli": "%s"}' % (FAKE_ADMIN_TOKEN, __ULI__)).json() 
    assert inserted['uli'] == __ULI__

# def test_successful_query(test_client):
#   item = test_client.post('%s/query' % api_url, data = FAKE_TESTING_RECORD).json()
#   assert item['uli'] == __ULI__
#   assert item['message'] == 'Found ULI!'

# def test_remove_licensee(test_client):
#   item = test_client.delete('%s/remove_licensee' % api_url, data = '{"token": "%s", "uli": "%s"}' % (FAKE_ADMIN_TOKEN, __ULI__)).json()
#   assert item['message'] == 'uli: ' + __ULI__ + ' deleted!'

#   inserted = test_client.post('%s/find_licensee' % api_url, data = '{"token": "%s", "uli": "%s"}' % (FAKE_ADMIN_TOKEN, __ULI__)).json() 
#   assert inserted['message'] == 'uli: ' + __ULI__ + ' not found!'

