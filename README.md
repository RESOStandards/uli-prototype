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

# Interactive Swagger Documentation
After the project has been started, view the Open API Specification and test it out with the Swagger UI available at http://localhost/api/docs

![Swagger-UI](/app/static/swagger-screenshot.png?raw=true "Optional Title")
# Sample Requests
## Registering a User

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
## Sample Return - Potential Matches Found, No User Created, ULI Returned
    {
        "message": "Found ULI!",
        "status": true,
        "uli": "602c6bbead2cef1872ea1e8d"
    }
## Querying a User
POST http://localhost/query

    {
        "MemberNationalAssociationId": "hjRWlmDkIHlxvrcQTbYBSvmKvVRcBw",
        "MemberFirstName": "Tracy",
        "MemberLastName": "Washington",
        "MemberEmail": "william05@marquez.com",
        "LicenseInfo": [
            {
                "agency": "SD",
                "number": "7385311",
                "type": "Broker"
            },
            {
                "agency": "NY",
                "number": "8479311",
                "type": "Broker"
            }
        ]
    }
## Sample Return - Match Found
    {
        "message": "Found ULI!",
        "status": true,
        "uli": "602c6bbead2cef1872ea1e8d"
    }

## Sample Return - No Match Found
    {
        "message": "ULI Not Found!",
        "status": true,
        "uli": null
    }

# Admin Functions
## Find Licensee

POST to http://localhost/find_licensee

    {
        "token": "_admin_token",
        "uli": "602c5445dadc7a3f8160971f"
    }


{
    "message": "ULI found!",
    "status": true,
    "uli": "602c6bbead2cef1872ea1e8d"
}
## Remove Licensee
DELETE http://localhost/remove_licensees

    {
        "token": "_admin_token",
        "uli": "602c5445dadc7a3f8160971f"
    }

## Generate Test Data 
Sample POST to http://localhost/generate_licensees

    {   
        "token": "_admin_token",
        "NumLicensees": 1000
    }

Sample Return

    {
        "message": "1000 generated!",
        "status": true
    }
## Outstanding Questions

1) Is mongo the right technology for this? Will it scale to millions of users?
2) Can the matching be improved? 
3) How do we avoid leaking data?
4) Do we need to deploy this?
