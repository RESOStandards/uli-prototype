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
    "MemberEmail": "SarahConnor@gmail.com",
    "MemberFirstName": "Sarah",
    "MemberLastName": "Connor",
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
        "MemberNationalAssociationId": "084001677",
        "MemberEmail": "dconroy@gmail.com",
        "MemberFirstName": "David",
        "MemberLastName": "Conroy",
        "LicenseInfo": [
            {
                "agency": "NY",
                "number": "1234586",
                "type": "Broker"
            }
        ]
    }
## Sample Return - Match Found
    {
        "message": "ULI May Exist!",
        "status": true
    }

## Sample Return - No Match Found
    {
        "message": "ULI Not Found!",
        "status": true
    }

## Generate Test Data 
Sample POST to http://localhost/generate_licensees

    {
        "NumLicensees": 100000
    }
## Outstanding Questions

1) Is mongo the right technology for this? Will it scale to millions of users?
2) Can the matching be improved? 
3) How do we avoid leaking data?
4) Do we need to deploy this?
