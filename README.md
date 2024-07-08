# Mongo DB Service for the Drone Engineering Ecosystem

## Table of Contents
1. [Introduction](#introduction)
2. [Requirements](#requirements)
3. [Installation](#installation)
4. [Local set up](#local-set-up)
5. [Tutorial](#tutorial)

## Introduction
The MongoDB Service module is responsible for storing data on the ground and retrieving it as requested via MQTT. The module right now offers communications between MongoDB and the Controllers Game from Dashboard Games, allowing to save, load and delete scenarios. The data is stored in a MongoDB database.   
  

## Requirements

Before starting with the installation, make sure you have the following software installed on your system:

- Python 3.7
- MongoDB Community Edition
- MongoDB Database Tools
- MongoDB Compass (optional, but recommended for easier database management)

## Installation

You can install MongoDB and MongoDB Database Tools from the following links:
- [Install MongoDB](https://www.mongodb.com/docs/manual/administration/install-community/)
- [Install MongoDB Database Tools](https://www.mongodb.com/docs/database-tools/)

To make it easier to work with the database, it is also recommended to install [MongoDB Compass](https://www.mongodb.com/products/compass).


## Local set up

To run and contribute, clone this repository to your local machine and install the requirements.  

```
pip install -r requirements.txt

```
If you need to change your MongoDB por you have to modify your mongod.conf file.

```
C:\Program Files\MongoDB\Server\7.0\bin\mongod.conf
```
## Commands

In order to send a command to the MongoDB service module must publish a message in the broker. The topic of the message must have this form:
```
+/mongo/#

```
Where + is the module requiring this service and # is the name of the service. Obviously some message have requires data that must be included in the payload of the message to be published. Sometimes the MongoDB service publish a message as an answer, the topic of the message have this form:

```
mongo/+/#
```

Where + is the module requiring this service and # is the name of the service.

In the table below indicates all the current commands that MongoDB service accepts:

Command | Description 
--- | --- 
*getPoligonos* | The module is asking MongoDB service to return a list of scenarios
*addPoligonos* | The module send a Scenario JSON to add to the database
*deletePoligonos* | Tells to delete the Scenario that is the same as the one send.


Note: getpoligonos makes MongoDB service to send a list of scenarios with the service name *readPoligonos*

This is an example of an scenario packet:


```
{
    '_id': ObjectId('666134a6d50fd28480e1337e'),
    'PoligonosJugadores': Array (2)
    'Obstaculos': Array (empty)
    'NumeroJugadores': 2
    'Mapa': "data:image/jpeg;base64,/9j/4AAQS..."
}

```
