import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import ast  # da bytecode a dictionary
import Antifurto_centralina

# TODO: gestione eccezioni
# TODO: fare in modo che se almeno un sensore è 1, il publish.single in Antifurto_centralina.py cambia lo stato della sirena a 1
# TODO: sirena temporizzata, quindi ON tot sec, OFF tot sec
# TODO: gestire due connesioni, fix --> non avere due utenti con stesso id
# TODO: aggiungere supporto log, con data e ora --> meglio farlo in Android

topic_base = 'afp/mr/home/'
device_id = "Antifurto_Uf_SEhh"
broker_server = 'broker.hivemq.com'

Antifurto_centralina.Start_thread_centralina()  # avvio il thread della centralina

# faccio girare il programma in loop, fino a quando non arriva il comando "kill"
while True:

    server_response = 0  # variabile per estrarre la risposta dal server

    def callback_connessione(client, userdata, flags, rc):
        print("Super Connected to the server: \"", broker_server + " \" with result code", str(rc))
        # sottoscrivo gli argomenti di interesse
        client.subscribe(topic_base + "#")

    def callback_disconnessione(client, userdata, rc):
        if rc != 0:
            print('Disconnesso')

    def callback_ricezione(client, userdata, message):
        print(userdata)
        print("Messagge received from " + message.topic + " with content " + str(message.payload))
        global server_response # variabile per estrarre la risposta dal server, definita global per estrarla dalla funzione
        server_response = message.payload # estraggo la risposta da message.payload e la salvo in questa variabile

    client = mqtt.Client(client_id="AFP")
    client.on_connect = callback_connessione  # Define the connect callback implementation.
    client.on_disconnect = callback_disconnessione
    client.on_message = callback_ricezione  # Called when a message has been received on a topic that the client subscribes
    client.connect(broker_server) # si connette al broker server
    client.loop_start() # inizia il loop per rimanere in attesa dei messaggi dal broker

    # entro nel ciclo sempre vero
    while True:
        if server_response != 0: # se ho ricevuto un messaggio la variabile è diversa da 0
            dict_str = server_response.decode("UTF-8") # decodifco il byte code ricevuto secondo lo standard UTF-8

            server_response_dictionary = ast.literal_eval(dict_str) # converto il bytecode in dictionary

            print(repr(server_response_dictionary)) # The repr() function returns a printable representation of the given object. https://www.programiz.com/python-programming/methods/built-in/repr
            print(type(server_response_dictionary)) # stampo il tipo della variabile server_responde_disctionary
            break # esco dal ciclo

    client.loop_stop() #stoppo il client

    program_killer = server_response_dictionary["System_status"] #estraggo il valore della chiave "System_status" e lo associo alla variabile programm_killer

    if program_killer == "kill":
        publish.single(topic_base + device_id,
                       payload="Message \"" + program_killer + "\" correctly received from server. System correctly terminated",
                       hostname=broker_server) # stampo il messaggio di kill
        Antifurto_centralina.Stop_thread_centralina()  # stoppo il thread della centralina
        break # esco dal ciclo while principale

    publish.single(topic_base + device_id, payload="Message " + str(server_response_dictionary) + " correctly received",
                   hostname=broker_server) # invio al server quello che ho ricevuto dal server


print("Fuori dal ciclo while main\nProgramma terminato grazie per averci testato")

