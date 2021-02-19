import pytest
import requests
import json
from urllib.parse import urljoin
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from application import create_app

FAKE_TESTING_ID = 'fakey-fake-id'
FAKE_TESTING_RECORD = '{ "UniqueLicenseeIdentifier": "%s", "MemberNationalAssociationId" : "%s", "MemberFirstName" : "Fakey", "MemberLastName" : "Fake", "MemberEmail" : "fakey@fake.com", "LicenseInfo" : [ { "agency" : "HI", "number" : "fake", "type" : "Broker" }, { "agency" : "AZ", "number" : "fake", "type" : "Broker" }, { "agency" : "OH", "number" : "fake", "type" : "Agent" } ] }' % (FAKE_TESTING_ID, FAKE_TESTING_ID)
FAKE_ADMIN_TOKEN = '_admin_token' #TODO: add real admin tokens
ULI_FOUND_MESSAGE = 'Unique Licensee Identifier: %s found!'
FAKE_TESTING_RECORD = {
    "token" :"_admin_token",
    "uli" : "123"
    }

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

def test_home_page(test_client):
  # TODO: add teardown that removes this record
  response = test_client.get('/')
  assert response.status_code == 200
  assert b"Welcome to the ULI Registry app!" in response.data


# def test_find_ULI(test_client):
#   response = test_client.post('/find_licensee', data=json.dumps(FAKE_TESTING_RECORD), follow_redirects=True)
#   # global __ULI__
#   # __ULI__ = item['uli']
#   print(response.data)
#   assert response.status_code == 200
  
# def test_successful_registration(test_client):
# response.client.post('/login', data=dict(
#         username=username,
#         password=password
#     ), follow_redirects=True)
#    = test_client.post('/register', FAKE_TESTING_RECORD)
#   global __ULI__
#   __ULI__ = item['uli']
  
#   assert response.status_code == 200

  #assert b"Welcome to the ULI Registry app!" in response.data


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
  
# def test_successful_registration(wait_for_api):
#   # TODO: add teardown that removes this record
#   request_session, api_url = wait_for_api
#   item = request_session.post('%s/register' % api_url, data = FAKE_TESTING_RECORD).json()
#   global __ULI__
#   __ULI__ = item['uli']

#   #ensure that record was inserted
#   inserted = request_session.post('%s/find_licensee' % api_url, data = '{"token": "%s", "uli": "%s"}' % (FAKE_ADMIN_TOKEN, __ULI__)).json() 
#   assert inserted['uli'] == __ULI__

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
