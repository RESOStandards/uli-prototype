import pytest
import json
from app.controllers.utils import format_uli, hide_MemberEmail, ordered

def test_format_uli():
  licensee = dict(
    _id=123, 
    MemberEmail="test@email.com", 
    MemberFirstName="jane", 
    MemberLastName="doe",
    license_data=[],
    MemberNationalAssociationId="abc"
  )
  
  assert format_uli(licensee) == json.loads('{"uli":"123","MemberEmail":"t**t@email.com","MemberFirstName":"jane","MemberLastName":"doe","license_data":[],"MemberNationalAssociationId":"abc"}')

def test_hide_MemberEmail():
  email = "ohai@email.com"
  assert hide_MemberEmail(email) == "o**i@email.com"

def test_ordered():
  a = dict(a=1, b=2,c=[2,3])
  b = dict(b=2, a=1,c=[3,2])
  
  assert a != b
  assert sorted(a.items()) != sorted(b.items())
  assert ordered(a) == ordered(b)

