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
    "license_data": [
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
        "ULI": "600c5b0d762ace88ef66f2ca",
        "message": "ULI saved successfully!",
        "status": true
    }
## Sample Return - Potential Matches Found

    {
        "data": [
            {
                "MemberEmail": "d*****y@gmail.com",
                "MemberFirstName": "David",
                "MemberLastName": "Conroy",
                "license_data": [
                    {
                        "agency": "NY",
                        "number": "1234586",
                        "type": "Broker"
                    },
                    {
                        "agency": "NY",
                        "number": "a12356ddd",
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
                ],
                "MemberNationalAssociationId": "084001677",
                "uli": "601032f9bd167f2a38b080bc"
            },
            {
                "possible_matches:": 1
            }
        ],
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
## Sample Return - Single Match Found
    {
        "data": [
            {
                "MemberEmail": "d*****y@gmail.com",
                "MemberFirstName": "David",
                "MemberLastName": "Conroy",
                "license_data": [
                    {
                        "agency": "NY",
                        "number": "1234586",
                        "type": "Broker"
                    },
                    {
                        "agency": "NY",
                        "number": "a12356ddd",
                        "type": "Appraiseral"
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
                ],
                "MemberNationalAssociationId": "084001677",
                "uli": "601032f9bd167f2a38b080bc"
            },
            {
                "possible_matches:": 1
            }
        ],
        "message": "ULI May Exist!",
        "status": true
    }

## Sample Return - Multiple Matches Found
TBC

## Outstanding Questions

1) Is mongo the right technology for this? Will it scale to millions of users?
2) Can the matching be improved? Right now only doing MemberEmail, or combination of first and last name. How can we ensure millisecond response time on multiple search types on a NOSQL collection? Elastic Search?
3) Do I need to nest the license information like the DID spec?
4) How do we avoid leaking data?
   1) Do we need to obsfucate license numbers? 
   2) MemberNationalAssociationId?
   3) Names?
5) Do we need to deploy this?