import json
import math
import pymongo
import threading
import paho.mqtt.client as mqtt
import time
from collections.abc import MutableMapping
import dronekit
from dronekit import connect, Command, VehicleMode
from paho.mqtt.client import ssl
from pymavlink import mavutil
from pymongo import MongoClient
import mongoengine
from mongoengine.fields import ReferenceField



client_mongo = pymongo.MongoClient("mongodb://localhost:27018/")
db = client_mongo["DEE"]
collection = db["poligonos"]


#class PruebaPoligonosEsquema(BaseModel):
#    Jugadores: int
#    Poligonos: float

#class PruebaPoligonos(mongoengine.Document):
#    Jugadores = mongoengine.IntField(required=True)
#    Poligonos = mongoengine.FloatField(required=True)

#    meta = {'collection': 'poligonos'}


def get_prueba_poligonos():
    #poligonos = json.loads(PruebaPoligonos.objects().to_json())
    escenarios = collection.find()
    documentos = [doc for doc in escenarios]
    return {"Escenarios": documentos}

def add_prueba_poligono(nuevoPoligono):
        resultado = collection.insert_one(nuevoPoligono)
        print (resultado)

def delete_prueba_poligono(nuevoPoligono):
        print ("delete")
        print (nuevoPoligono)
        collection.delete_one({"Mapa": nuevoPoligono.get('Mapa')})




def publishmongo():
        client_mqtt.publish("mongo/mobileApp/readPoligonos", json.dumps(get_prueba_poligonos()))



def process_message(message, client):
    global vehicle
    global direction
    global go
    global sending_telemetry_info
    global sending_topic
    global op_mode
    global sending_topic
    global state

    splited = message.topic.split("/")
    origin = splited[0]
    command = splited[2]
    print ('recibo ', command)
    if command == "getPoligonos":
        print('1')
    if command == "addPoligonos":
        print('2')











def on_message(client_mqtt, userdata, message):
    print("helloworld")
    process_message(message, client_mqtt)
    data = message.payload.decode("utf-8")
    peticion = message.topic
    # Ejecutar función específica según los datos recibidos
    if peticion == "mongo/mobileApp/getPoligonos":
        Escenarios = get_prueba_poligonos()
        Escenarios_Sin_Id = eliminar_ids(Escenarios)
        print((get_prueba_poligonos()))

        print(json.dumps(Escenarios_Sin_Id))
        client_mqtt.publish("mobileApp/mongo/readPoligonos",json.dumps(Escenarios_Sin_Id))

    elif peticion =="mongo/mobileApp/addPoligonos":

        nuevopoligonoprueba = json.loads(message.payload.decode("utf-8"))
        add_prueba_poligono(nuevopoligonoprueba)
    elif peticion =="mongo/mobileApp/deletePoligonos":

        nuevopoligonoprueba = json.loads(message.payload.decode("utf-8"))
        delete_prueba_poligono(nuevopoligonoprueba)


def on_internal_message(client, userdata, message):
    global internal_client
    print("helloworl2")
    process_message(message, internal_client)

def on_external_message(client, userdata, message):
    global external_client
    process_message(message, external_client)

def on_connect(external_client, userdata, flags, rc):
    if rc==0:
        print("Connection OK")
    else:
        print("Bad connection")

def MongoService (connection_mode, operation_mode, external_broker, username, password):
    global op_mode
    global external_client
    global internal_client
    global state

    client_mqtt = mqtt.Client("testing")
    client_mqtt.on_message = on_message
    client_mqtt.connect("localhost", 1885)
    client_mqtt.subscribe("mongo/#")

    client_mongo = pymongo.MongoClient("mongodb://localhost:27018/")
    db = client_mongo["DEE"]
    collection = db["poligonos"]

    state = 'disconnected'

    print ('Connection mode: ', connection_mode)
    print ('Operation mode: ', operation_mode)
    op_mode = operation_mode

    client_mqtt = mqtt.Client ("MongoConect")
    client_mqtt.on_message = on_message
    client_mqtt.connect("localhost",1884)

    internal_client = mqtt.Client("Mongo_internal2")
    internal_client.on_message = on_internal_message
    internal_client.connect("localhost", 1884)


    external_client = mqtt.Client("Mongo_external", transport="websockets")
    external_client.on_message = on_external_message
    external_client.on_connect = on_connect

    if connection_mode== "global":
        if external_broker == "hivemq":
            external_client.connect("broker.hivemq.com", 8000)
            print('Connected to broker.hivemq.com:8000')

        elif external_broker == "hivemq_cert":
            external_client.tls_set(ca_certs=None, certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED,
                           tls_version=ssl.PROTOCOL_TLS, ciphers=None)
            external_client.connect("broker.hivemq.com", 8884)
            print('Connected to broker.hivemq.com:8884')

        elif external_broker == "classpip_cred":
            external_client.username_pw_set(
                username, password
            )
            external_client.connect("classpip.upc.edu", 8000)
            print('Connected to classpip.upc.edu:8000')

        elif external_broker == "classpip_cert":
            external_client.username_pw_set(
                username, password
            )
            external_client.tls_set(ca_certs=None, certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED,
                           tls_version=ssl.PROTOCOL_TLS, ciphers=None)
            external_client.connect("classpip.upc.edu", 8883)
            print('Connected to classpip.upc.edu:8883')
        elif external_broker == "localhost":
            external_client.connect("localhost", 8000)
            print('Connected to localhost:8000')
        elif external_broker == "localhost_cert":
            print('Not implemented yet')

    elif connection_mode == "local":
        if operation_mode == "simulation":
            external_client.connect("localhost", 8000)
            print('Connected to localhost:8000')
        else:
            external_client.connect("10.10.10.1", 8000)
            print('Connected to 10.10.10.1:8000')



    print("Waiting....")
    external_client.subscribe("+/autopilotService/#", 2)
    external_client.subscribe("cameraService/+/#", 2)
    internal_client.subscribe("+/autopilotService/#")
    client_mqtt.subscribe("mongo/#")
    client_mqtt.loop_start()
    internal_client.loop_start()
    if operation_mode == 'simulation':
        external_client.loop_forever()
    else:
        #external_client.loop_start() #when executed on board use loop_start instead of loop_forever
        external_client.loop_forever()




if __name__ == '__main__':
    import sys
    connection_mode = "local" # global or local
    operation_mode = "simulation" # simulation or production
    username = None
    password = None
    if connection_mode == 'global':
       external_broker = "sys.argv[3]"
      #  if external_broker == 'classpip_cred' or external_broker == 'classpip_cert':
       #     username = sys.argv[4]
        #    password = sys.argv[5]
    else:
        external_broker = None

    MongoService(connection_mode,operation_mode, external_broker, username, password)
