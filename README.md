![Test Flask App](https://github.com/RESOStandards/uli-prototype/workflows/Test%20Flask%20App/badge.svg)

# Centralized ULI Registry Proof of Concept
Welcome to the rough proof of concept of a centralized ULI Service


## Tech Stack
* Python 3 Flask API 
* Mongo DB
* NGINX Reverse Proxy w/ Gunicorn
* Docker Compose


To run, simply bring up the webserver, web app,  and database with the following command.

    docker-compose build
    docker-compose up -d

# Registering a User
To register a user

    POST http://localhost/register 
    {
    "MemberNationalAssociationId": "084001677",
    "MemberEmail": "dconroy@gmail.com",
    "MemberFirstName": "David",
    "MemberLastName": "Conroy",
    "LicenseInfo": [
        {
        "agency": "NY",
        "number": "1234586",
        "type": "Broker"
        },
        {
        "agency": "NY",
        "number": "a12356",
        "type": "Appraisal"
        },
        {
        "agency": "MA",
        "number": "78910",
        "type": "Salesperson"
        },
        {
        "agency": "NH",
        "number": "654321",
        "type": "Salesperson"
        }
    ]
    }
## Sample Return - No Match Found, New User Created
    {
        "message": "ULI saved successfully!",
        "status": true,
        "uli": "602ac76cd790ab1c770cbbbf"
    }
## Sample Return - Potential Matches Found
{
    "message": "ULI May Exist!",
    "status": true
}
# Querying a User
Sample POST to http://localhost/query

    {
        "MemberNationalAssociationId": "08400162342349", 
        "licenseNumber": "12354",
        "MemberEmail": "dconroy1234@gmail.com",
        "MemberFirstName" : "David",
        "MemberLastName" : "Conroy"
    }
## Sample Return 
{
    "message": "ULI May Exist!",
    "status": true
}
## Outstanding Questions

1) Is mongo the right technology for this? Will it scale to millions of users?
2) Can the matching be improved? Right now only doing MemberEmail, or combination of first and last name. How can we ensure millisecond response time on multiple search types on a NOSQL collection? Elastic Search?
3) Do I need to nest the license information like the DID spec?
4) How do we avoid leaking data?
   1) Do we need to obsfucate license numbers? 
   2) MemberNationalAssociationId?
   3) Names?
5) Do we need to deploy this?
