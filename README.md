# Zé Delivery Test

by marcosbitetti@gmail.com

## Setup

* copy **.env.example** inside **"application"** and renamed to **.env**

* run in project root:
    
       pip install -r requirements.txt

### **Troubleshooting**

#### Missing permissions on mongo-volume
* add permissions to write, ex: **sudo chmod -R 775 ./docker/mongo-volume**

#### Changing ports
* if you wish to change ports, just change oin .env and docker-compose.yml

## Running / Deploy

#### I recommend a conteiner:

    cd docker
    docker-compose up --build

It's make a server running faster.

#### Or run python localy:

1º run database:

    cd docker-dev
    docker-compose up --build

2º run python

    pip install -r requirements.txt
    cd application
    python main.py

## Server

http://localhost:5050/

I use a compound from Flask and Connexion, I never done a complete server in Python before, then I used some knowledge thequinices from other environments.
A **model** folder remains for manage future web-server requests, and I used **resources** nomenclature, to use in REST.

And choice PyCharm IDE for dev.

## Rest API

http://localhost:5050/api/ui

In swagger doc, are additional information about implementation of each end-point.

I opted by an Swagger environment, because it is family to me, and a good comercial resource.

Swagger can handle requests and pass it as normalized data to "api resources". I preferred dispend time writing data models than make the risk to made security functions by myself inside model/resources.


## Tests

## automated tests

If pytest has successful instaled, run in project's root:

    pytest --rootdir=./application/ -v

## manual tests

This is the entry point used in devlopment tests:

#### Search : GET
http://localhost:5050/api/partner/search?lat=-43.297337&lon=-23.013538&radius=10

#### Get : GET
http://localhost:5050/api/partner/1

#### Create : POST
http://localhost:5050/api/partner

data example:

    {
          "tradingName": "TESTE Adega Osasco ",
          "ownerName": "Ze da Ambev",
          "document": "02.453.716/000170",
          "coverageArea": {
             "type": "MultiPolygon",
             "coordinates": [
                [
                   [
                      [
                         -43.36556,
                         -22.99669
                      ],
                      [
                         -43.36539,
                         -23.01928
                      ],
                      [
                         -43.26583,
                         -23.01802
                      ],
                      [
                         -43.36556,
                         -22.99669
                      ]
                   ]
                ]
             ]
          },
          "address": {
             "type": "Point",
             "coordinates": [
                -43.297337,
                -23.013538
             ]
          }
       }
