import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import ast

# import json

topic_base = 'afp/mr/home/'
device_id = "SV"
broker_server = 'broker.hivemq.com'

# faccio girare il programma in loop,
while True:
    server_response = 0

    def callback_connessione(client, userdata, flags, rc):
        print("Connected to the server: \"", broker_server + " \" with result code", str(rc))
        # sottoscrivo gli argomenti di interesse
        client.subscribe(topic_base + "#")


    def callback_disconnessione(client, userdata, rc):
        if rc != 0:
            print('Disconnesso')


    def callback_ricezione(client, userdata, message):
        print(userdata)
        print("Messagge received on " + message.topic + " with content " + str(message.payload))
        global server_response
        server_response = message.payload


    client = mqtt.Client(client_id="AFP")
    client.on_connect = callback_connessione  # Define the connect callback implementation.
    client.on_disconnect = callback_disconnessione
    client.on_message = callback_ricezione  # Called when a message has been received on a topic that the client subscribes
    client.connect(broker_server)
    client.loop_start()

    # quando ricevo dal server qualcosa subito scatta l'azione
    # altri segnali verrano ignorati
    while True:
        if server_response != 0:
            dict_str = server_response.decode("UTF-8")
            server_response_dictionary = ast.literal_eval(dict_str)
            print(repr(server_response_dictionary))
            print(type(server_response_dictionary))
            break

    client.loop_stop()
    publish.single(topic_base + device_id, payload="Message " + str(server_response_dictionary) + " correctly received",
                   hostname=broker_server)
