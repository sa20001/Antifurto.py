#Open cfg_file e create a thread
import ast
from threading import Thread
import time
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

read_file = open("cfg.json", "r")
file_read = read_file.read()
# print(read_file)
# print(type(read))

cfg_dict = ast.literal_eval(file_read)
# print(type(cfg_dict))
# print(cfg_dict)

wait_time = cfg_dict["Delay_time"]
# print(wait_time)

topic_base = 'afp/mr/home/'
device_id = "Centralina_antifurto"
broker_server = 'broker.hivemq.com'

i = 0
def code_My_Thread(nome, attesa):
    while True:
        global i
        i += 1
        print(nome + "Number of time program published to Broker: " + str(i))

        def callback_connessione(client, userdata, flags, rc):
            print("Connected to the server: \"", broker_server + " \" with result code", str(rc))
            # sottoscrivo gli argomenti di interesse
            client.subscribe(topic_base + "#")

        def callback_disconnessione(client, userdata, rc):
            if rc != 0:
                print('Disconnesso')

        client = mqtt.Client(client_id="AFP")
        client.on_connect = callback_connessione  # Define the connect callback implementation.
        client.on_disconnect = callback_disconnessione
        client.connect(broker_server)  # si connette al broker server

        publish.single(topic_base + device_id, payload="Message correctly sent: " + str(cfg_dict), hostname=broker_server)  # invio al server quello che ho ricevuto dal server

        time.sleep(attesa)

def test_1():
    # definisco i thread
    publish_centralina = Thread(target=code_My_Thread, args=("Publish to Broker--> ", wait_time)) # args qui vuole una tupla


    #eseguo i thread
    publish_centralina.start()

    # attendo fine esecuzione dei threads
    # publish_centralina.join() # con join() aspetta la fine di start() prima di passare all'istruzione successiva

    # print("Fine esecuzione dei thread")

