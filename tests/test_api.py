import pytest
import requests
import json
from urllib.parse import urljoin
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

pytest_plugins = ["docker_compose"]

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

def test_successful_registration(wait_for_api):
  # TODO: add teardown that removes this record
  request_session, api_url = wait_for_api
  data = '{ "MemberNationalAssociationId" : "hjRWlmDkIHlxvrcQTbYBSvmKvVRcBw", "MemberFirstName" : "Tracy", "MemberLastName" : "Washington", "MemberEmail" : "william05@marquez.com", "license_data" : [ { "agency" : "SD", "number" : "7385", "type" : "Broker" }, { "agency" : "NY", "number" : "8479", "type" : "Broker" }, { "agency" : "OH", "number" : "495", "type" : "Agent" } ] }'
  item = request_session.post('%s/register' % api_url, data = data).json()
  assert item['status'] == True

def test_successful_query(wait_for_api):
  request_session, api_url = wait_for_api
  data = '{ "MemberNationalAssociationId" : "hjRWlmDkIHlxvrcQTbYBSvmKvVRcBw", "MemberFirstName" : "Tracy", "MemberLastName" : "Washington", "MemberEmail" : "william05@marquez.com"}'
  item = request_session.post('%s/query' % api_url, data = data).json()

  assert item == json.loads('{"message": "ULI May Exist!", "status": true}')

#def test_duplicate_association_id(wait_for_api):
  #time curl -d '{"MemberNationalAssociationId": "rKwpWBNFJNZFOAvPmYYgwDxoehlvfE","MemberEmail": "jenkinsvictoria@gmail.com","MemberFirstName": "Richard","MemberLastName": "Washington"}' -X POST http://localhost/query
  #{
  #  "message": "ERROR: more than one record was found with the given MemberNationalAssociationId", 
  #  "status": false
 #}



