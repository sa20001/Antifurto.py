import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import ast  # da bytecode a dictionary
import Antifurto_centralina
from termcolor import colored

# TODO: fare in modo che se almeno un sensore è 1, il publish.single in Antifurto_centralina.py cambia lo stato della sirena a 1
# TODO: sirena temporizzata, quindi ON tot sec, OFF tot sec
# TODO: gestire due connesioni, fix --> non avere due utenti con stesso id, oppure gestire eccezione
# TODO: aggiungere supporto log, con data e ora --> meglio farlo in Android
# TODO: vedere perché (raramente perde i messaggi dal server)
# TODO: verificare se si possono togliere le variabili non usate, forse servono per usi futuri

topic_base = 'afp/mr/home/'
device_id = "Antifurto_Uf_SEhh"
broker_server = 'broker.hivemq.com'

Antifurto_centralina.Start_thread_centralina()  # avvio il thread della centralina

# faccio girare il programma in loop, fino a quando non arriva il comando "kill"
while True:

    server_response = 0  # variabile per estrarre la risposta dal server
    server_response_dictionary = 0  # inizializzata a 0 in caso di eccezione
    program_killer = 0  # inizializzata a 0 in caso di eccezione

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
        global server_response  # variabile definita global per estrarre la risposta del server dalla funzione
        server_response = message.payload  # estraggo la risposta da message.payload e la salvo in questa variabile

    client = mqtt.Client(client_id="AFP")
    client.on_connect = callback_connessione  # Define the connect callback implementation.
    client.on_disconnect = callback_disconnessione

    # Called when a message has been received on a topic that the client subscribes
    client.on_message = callback_ricezione
    client.connect(broker_server)  # si connette al broker server
    client.loop_start()  # inizia il loop per rimanere in attesa dei messaggi dal broker

    # entro nel ciclo sempre vero
    while True:

        try:  # gestione eccezione per il metodo literal_eval (a volte va in crash) e per bad json format

            if server_response != 0:  # se ho ricevuto un messaggio la variabile è diversa da 0
                dict_str = server_response.decode("UTF-8")  # decodifco il byte code ricevuto secondo lo standard UTF-8
                server_response_dictionary = ast.literal_eval(dict_str)  # converto il bytecode in dictionary

                # The repr() function returns a printable representation of the given object.
                # https://www.programiz.com/python-programming/methods/built-in/repr
                print(repr(server_response_dictionary))
                print(type(server_response_dictionary))  # stampo il tipo della variabile server_response_dictionary
                break  # esco dal ciclo

        except ValueError:  # gestisco l'eccezione solo se è ValueError (finora l'unico errore che si è presentato)
            print(colored("A ValueError occurred!!!", "red"))  # stampo in rosso
            break  # esco dal ciclo

    client.loop_stop()  # stoppo il client

    # if no errors occurred
    if server_response_dictionary != 0:

        try:  # gestisco l'eccezione se non è presente la chiave "System_status" nel file JSON
            program_killer = server_response_dictionary[
                "System_status"]  # estraggo il valore della chiave "System_status" e lo associo alla variabile programm_killer

        except KeyError: # gestisco l'eccezione solo se è KeyError
            print(colored("Wrong key \"System_status\", maybe mistyped or missing\nCheck JSON sent", "red"))
            print(colored("EXCEPTION CORRRECTLY HANDLED\nCheck \"System_status\" key", "green"))

        if program_killer == "kill":  # se la key "System_status" ha valore "kill"
            publish.single(topic_base + device_id,
                           payload="Message \"" + program_killer + "\" correctly received from server. System correctly terminated",
                           hostname=broker_server)  # stampo il messaggio di kill
            Antifurto_centralina.Stop_thread_centralina()  # stoppo il thread della centralina
            break  # esco dal ciclo while principale

        # invio al server quello che ho ricevuto dal server in un solo messaggio
        publish.single(topic_base + device_id + ("_single"), payload="Message " + str(server_response_dictionary) +
                                                                     " correctly received", hostname=broker_server)

    else:
        # if errors occurred during conversion from bytecode to dicitonary
        print(colored("RECEIVED BAD/WRONG MESSAGE FROM BROKER\nAST FAILED TO EVAL", "red"))
        print(colored("EXCEPTION CORRRECTLY HANDLED\nMAKE SURE TO SEND THE CORRECT MESSAGE NEXT TIME", "green"))

        # Publish multiple messages to a broker, then disconnect cleanly.
        multiple_publish = [{'topic': topic_base + device_id + ("_error"),
                             'payload': "An error occurred"},
                            (topic_base + device_id + ("_error_message"), "With message BAD JSON FORMAT", 0, False)]
        publish.multiple(multiple_publish, hostname=broker_server)  # invio al server più messaggi nello stesso momento

print("Fuori dal ciclo while main\nProgramma terminato grazie per averci testato")
