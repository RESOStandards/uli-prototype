import pytest
import requests
import json
from urllib.parse import urljoin
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

pytest_plugins = ["docker_compose"]

FAKE_TESTING_ID = 'fakey-fake-id'
FAKE_TESTING_RECORD = '{ "UniqueLicenseeIdentifier": "%s", "MemberNationalAssociationId" : "%s", "MemberFirstName" : "Fakey", "MemberLastName" : "Fake", "MemberEmail" : "fakey@fake.com", "LicenseInfo" : [ { "agency" : "HI", "number" : "fake", "type" : "Broker" }, { "agency" : "AZ", "number" : "fake", "type" : "Broker" }, { "agency" : "OH", "number" : "fake", "type" : "Agent" } ] }' % (FAKE_TESTING_ID, FAKE_TESTING_ID)
FAKE_ADMIN_TOKEN = '_admin_token' #TODO: add real admin tokens
ULI_FOUND_MESSAGE = 'Unique Licensee Identifier: %s found!'

__ULI__ = None

# Invoking this fixture: 'function_scoped_container_getter' starts all services
@pytest.fixture(scope="function")
def wait_for_api(function_scoped_container_getter):
  request_session = requests.Session()
  retries = Retry(total=5,
                  backoff_factor=0.1,
                  status_forcelist=[500, 502, 503, 504])
  request_session.mount('http://', HTTPAdapter(max_retries=retries))

  service = function_scoped_container_getter.get("webserver").network_info[0]
  api_url = "http://%s/" % (service.hostname)
  assert request_session.get(api_url)
  return request_session, api_url
  
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
