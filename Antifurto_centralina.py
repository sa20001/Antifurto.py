# Open cfg_file e create a thread
import ast
from threading import Thread
import time
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

read_file = open("cfg.json", "r")  # apre il file cfg.json in modalità read (lettura)
file_read = read_file.read()  # creo variabile file_read che corrisponde alla lettura del file
# print(read_file)
# print(type(read))


cfg_dict = ast.literal_eval(file_read)  # converto il la variabile file_read (str) in dizionario
# print(type(cfg_dict))
# print(cfg_dict)

wait_time = cfg_dict["Delay_time"]  # estraggo dal dizionario il valore della chiave delay time
# print(wait_time)

topic_base = 'afp/mr/home/'  # | configurazione per connettermi al broker
device_id = "Centralina_antifurto"  # | rispetto ad antifurto_main cambio il topic in Centralina_antifurto
broker_server = 'broker.hivemq.com'  # |

i = 0  # inizializzo la variabile i a 0

while_trigger = True  # trigger per rendere il ciclo while vero, con stato false serve per sbloccare il thread


def code_My_Thread(nome, attesa):
    while while_trigger:
        global i  # la definisco global
        i += 1  # aumenta di uno ad ogni ciclo
        print(nome + "Number of time program published to Broker: " + str(
            i))  # per controllo, per verificare quante volte ha pubblicato a Broker

        client = mqtt.Client(client_id="AFP")
        client.connect(broker_server)  # si connette al broker server

        publish.single(topic_base + device_id, payload="Message correctly sent: " + str(cfg_dict),
                       hostname=broker_server)  # invio al server il file cfg.json

        time.sleep(attesa)


# definisco il thread
publish_centralina = Thread(target=code_My_Thread,
                            args=("Publish to Broker--> ", wait_time))  # args qui vuole una tupla


def Start_thread_centralina():
    # eseguo il thread
    publish_centralina.start()


def Stop_thread_centralina():
    global while_trigger
    while_trigger = False  # in questo modo rendo il ciclo while false e sblocco il thread
    publish_centralina.join()  # killa il thread
    print("Fine esecuzione del thread \"" + device_id + "\"")  # Messaggio di verifica
