![Test Flask App](https://github.com/RESOStandards/uli-prototype/workflows/Test%20Flask%20App/badge.svg)

# Centralized ULI Registry Proof of Concept
This repository contains a prototyped API and Database for the RESO Unique Licensee Identifier Project. You can find out more about ULI at [reso.org](https://reso.org)


## Tech Stack
* Python 3 Flask API w/ Gunicorn
* MongoDB
* NGINX
* Docker Compose for ease in local development

## Running Locally
To run, simply bring up the webserver, web app,  and database with the following commands. You may then edit the flask app from the /app directory which hot reloads inside the container.

    docker-compose build
    docker-compose up -d

## Testing
Testing does not require docker and can be done locally with the following command from the project root.

    python3 -m pytest app -v
# Documentation
After the project has been started, view the Open API Specification and test it out with the Swagger UI available at http://localhost/api/docs

![Swagger-UI](/app/application/static/swagger-screenshot.png?raw=true "Documentation")

## Outstanding Questions
1) Is mongo the right technology for this? Will it scale to millions of users?
2) Can the matching be improved? Should we add scoring?
3) How do we avoid leaking data?


## Disclaimer: This repository is meant for local testing only and contains no access control
