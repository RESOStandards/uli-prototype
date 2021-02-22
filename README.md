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

![Swagger-UI](/app/application/static/swagger-screenshot.png?raw=true "Optional Title")

# Disclaimer - This repository is meant for local testing only and contains no access control

## Outstanding Questions
1) Is mongo the right technology for this? Will it scale to millions of users?
2) Can the matching be improved? Should we add scoring?
3) How do we avoid leaking data?
