import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import ast  # da bytecode a dictionary
import Antifurto_centralina
from termcolor import colored

log_print = Antifurto_centralina.logger.info

read_file_parameters = open("Json parametrs.json", "r")  # apre il file cfg.json in modalità read (lettura)
file_read_parameters = read_file_parameters.read()  # creo variabile file_read che corrisponde alla lettura del file
read_file_parameters.close()

server_response_dictionary = ast.literal_eval(file_read_parameters)  # inizializzo il server_response_dictionary
server_response = None
program_killer = None
for_closing = True  # serve per quando si richiama la funzione on_closing sull'interfaccia grafica
kill_interface = False

def pass_sensor_win0():
    sensor_list = server_response_dictionary["sensor_list"]

    if sensor_list[0]["sensor_status"] == 0:
        # IL SENSORE WIN1 HA VALORE 0
        bool_check = False
    else:
        # IL SENSORE WIN1 HA VALORE 1
        bool_check = True

    # STAMPO IL VALORE DI BOOL CHECK
    return bool_check


def pass_sensor_win1():
    sensor_list = server_response_dictionary["sensor_list"]
    if sensor_list[1]["sensor_status"] == 0:
        bool_check = False
    else:
        bool_check = True
    return bool_check


def pass_sensor_win2():
    sensor_list = server_response_dictionary["sensor_list"]
    if sensor_list[2]["sensor_status"] == 0:
        bool_check = False
    else:
        bool_check = True
    return bool_check


def pass_sensor_win3():
    sensor_list = server_response_dictionary["sensor_list"]
    if sensor_list[3]["sensor_status"] == 0:
        bool_check = False
    else:
        bool_check = True
    return bool_check


def pass_sensor_door():
    sensor_list = server_response_dictionary["sensor_list"]
    if sensor_list[4]["sensor_status"] == 0:
        bool_check = False
    else:
        bool_check = True
    return bool_check


def pass_sensor_motion():
    sensor_list = server_response_dictionary["sensor_list"]
    if sensor_list[5]["sensor_status"] == 0:
        bool_check = False
    else:
        bool_check = True
    return bool_check


def pass_siren():
    sensor_list = server_response_dictionary["sensor_list"]
    if sensor_list[6]["sensor_status"] == 0:
        bool_check = False
    else:
        bool_check = True
    return bool_check


# nego i bool per riutilizzare le key dell'intent per passare le key da debug.class a sensors.class


def main_program():
    global server_response  # definita globale perchè devo estrarre il valore dal def
    global server_response_dictionary  # definita globale perchè devo estrarre il valore dal def
    global program_killer  # definita globale perchè devo estrarre il valore dal def

    Antifurto_centralina.start_thread_centralina()  # avvio il thread della centralina

    # faccio girare il programma in loop, fino a quando non arriva il comando "kill"
    # o fino a quando non richiamo la funzione for closing nell'interfaccia grafica
    while for_closing:

        server_response = 0  # variabile per estrarre la risposta dal server
        program_killer = 0  # inizializzata a 0 in caso di eccezione

        def callback_connessione(client, userdata, flags, rc):
            print(
                "Super Connected to the server: \"" + Antifurto_centralina.broker_server + " \" with result code " + str(
                    rc))

            log_print(
                Antifurto_centralina.date() + "Super Connected to the server: \"" + Antifurto_centralina.broker_server + "\" with "
                                                                                                                         "result "
                                                                                                                         "code " +
                str(
                    rc))

            # sottoscrivo gli argomenti di interesse
            client.subscribe(Antifurto_centralina.topic_base + "#")

        # fondamentalmente inutile
        def callback_disconnessione(client, userdata, rc):
            if rc != 0:
                print('Disconnesso')
                log_print(Antifurto_centralina.date() + ' Disconnesso')

        # fondamentalmente inutile

        def callback_ricezione(client, userdata, message):
            print(userdata)
            log_print(Antifurto_centralina.date() + str(userdata))
            print("Message received from " + message.topic + " with content " + str(message.payload))
            log_print(
                Antifurto_centralina.date() + "Message received from " + message.topic + " with content " + str(
                    message.payload))
            global server_response  # variabile definita global per estrarre la risposta del server dalla funzione
            server_response = message.payload  # estraggo la risposta da message.payload e la salvo in questa variabile

        client = mqtt.Client(client_id="AFP")
        client.on_connect = callback_connessione  # Define the connect callback implementation.
        client.on_disconnect = callback_disconnessione

        # Called when a message has been received on a topic that the client subscribes
        client.on_message = callback_ricezione
        client.connect(Antifurto_centralina.broker_server)  # si connette al broker server
        client.loop_start()  # inizia il loop per rimanere in attesa dei messaggi dal broker

        # entro nel ciclo sempre vero, fino a quando non richiamo la funzione for closing nell'interfaccia grafica
        while for_closing:

            try:  # gestione eccezione per il metodo literal_eval (a volte va in crash) e per bad json format

                if server_response != 0:  # se ho ricevuto un messaggio la variabile è diversa da 0
                    dict_str = server_response.decode(
                        "UTF-8")  # decodifco il byte code ricevuto secondo lo standard UTF-8
                    server_response_dictionary = ast.literal_eval(dict_str)  # converto il bytecode in dictionary

                    # The repr() function returns a printable representation of the given object.
                    # https://www.programiz.com/python-programming/methods/built-in/repr
                    print(repr(server_response_dictionary))
                    log_print(Antifurto_centralina.date() + repr(server_response_dictionary))
                    print(type(server_response_dictionary))  # stampo il tipo della variabile server_response_dictionary
                    log_print(Antifurto_centralina.date() + str(type(server_response_dictionary)))

                    checker = False

                    for i in server_response_dictionary["sensor_list"]:  # stampo tutti valori della lista dei sensori

                        if i["sensor_status"] == 0:  # se il sensore non ha rilevato nulla
                            print(colored(i["sensor_id"] + " No trigger", "blue"))
                            log_print(Antifurto_centralina.date() + i["sensor_id"] + " No trigger")

                        else:  # se il sensore ha rilevato qualcosa
                            checker = True

                            print(colored(i["sensor_id"] + " Sì trigger", "yellow"))
                            log_print(Antifurto_centralina.date() + i["sensor_id"] + " Sì trigger")
                            publish.single(Antifurto_centralina.topic_base + Antifurto_centralina.device_id_alarm,
                                           payload="Someone triggered a sensor!!!",
                                           hostname=Antifurto_centralina.broker_server)

                    if checker:
                        for index, element in enumerate(
                                server_response_dictionary["sensor_list"]):  # entro nella lista del dict
                            if element["sensor_id"] == "Siren":
                                server_response_dictionary["sensor_list"][index][
                                    "sensor_status"] = 1  # cambia lo stato della sirena a 1 all'interno del dict
                                print(colored(server_response_dictionary, "magenta"))  # debug
                                log_print(Antifurto_centralina.date() + str(server_response_dictionary))

                    break  # esco dal ciclo

            except (
                    KeyError, ValueError,
                    SyntaxError):  # gestisco l'eccezione solo se è ValueError, SyntaxError o KeyError
                print(colored("A ValueError, SyntaxError or KeyError occurred!!!", "red"))  # stampo in rosso
                log_print(Antifurto_centralina.date() + "A ValueError, SyntaxError or KeyError occurred!!!")
                break  # esco dal ciclo

        client.loop_stop()  # stoppo il client

        # if no errors occurred
        if server_response_dictionary != 0:

            try:  # gestisco l'eccezione se non è presente la chiave "System_status" nel file JSON
                program_killer = server_response_dictionary[
                    "System_status"]  # estraggo il valore della chiave "System_status" e lo associo alla variabile
                # programm_killer

            except KeyError:  # gestisco l'eccezione solo se è KeyError
                print(colored("Wrong key \"System_status\", maybe mistyped or missing\nCheck JSON sent", "red"))
                log_print(Antifurto_centralina.date() + "Wrong key \"System_status\", maybe mistyped or missing\n"
                          + Antifurto_centralina.date() + "Check JSON sent")
                print(colored("EXCEPTION CORRRECTLY HANDLED\nCheck \"System_status\" key", "green"))
                log_print(Antifurto_centralina.date() + "EXCEPTION CORRRECTLY HANDLED\n"
                          + Antifurto_centralina.date() + "Check \"System_status\" key")

            if program_killer == "kill":  # se la key "System_status" ha valore "kill"
                print(colored("Command \"kill\" received from Broker", "red"))
                log_print(Antifurto_centralina.date() + "Command \"kill\" received from Broker")

                publish.single(Antifurto_centralina.topic_base + Antifurto_centralina.device_id_kill,
                               payload="Message \"" + program_killer + "\" correctly received from server. System "
                                                                       "correctly terminated",
                               hostname=Antifurto_centralina.broker_server)  # stampo il messaggio di kill
                Antifurto_centralina.stop_thread_centralina()  # stoppo il thread della centralina
                global kill_interface
                kill_interface = True
                break  # esco dal ciclo while principale

            # invio al server quello che ho ricevuto dal server in un solo messaggio
            publish.single(Antifurto_centralina.topic_base + Antifurto_centralina.device_id_check,
                           payload="Message " + str(server_response_dictionary) +
                                   " correctly received", hostname=Antifurto_centralina.broker_server)

        else:
            # if errors occurred during conversion from bytecode to dicitonary
            print(colored("RECEIVED BAD/WRONG MESSAGE FROM BROKER\nAST FAILED TO EVAL", "red"))
            log_print(Antifurto_centralina.date() + "RECEIVED BAD/WRONG MESSAGE FROM BROKER\n"
                      + Antifurto_centralina.date() + "AST FAILED TO EVAL")
            print(colored("EXCEPTION CORRRECTLY HANDLED\nMAKE SURE TO SEND CORRECT JSON FORMAT NEXT TIME", "green"))
            log_print(Antifurto_centralina.date() + "EXCEPTION CORRRECTLY HANDLED\n"
                      + Antifurto_centralina.date() + "MAKE SURE TO SEND CORRECT JSON FORMAT NEXT TIME")

            # Publish multiple messages to a broker, then disconnect cleanly.
            multiple_publish = [{'topic': Antifurto_centralina.topic_base + Antifurto_centralina.device_id_error,
                                 'payload': "An error occurred"},
                                (Antifurto_centralina.topic_base + Antifurto_centralina.device_id_error_message,
                                 "With message BAD JSON FORMAT", 0, False)]
            publish.multiple(multiple_publish,
                             hostname=Antifurto_centralina.broker_server)  # invio al server più messaggi nello
            # stesso momento

    print("Fuori dal ciclo while main\nProgramma terminato grazie per averci testato")
    log_print(
        Antifurto_centralina.date() + "Fuori dal ciclo while main\n" +
        Antifurto_centralina.date() + "Programma terminato grazie per averci testato")


def on_destroy():
    Antifurto_centralina.stop_thread_centralina()
    print("Fuori dal ciclo while main\nProgramma terminato grazie per averci testato")
    log_print(
        Antifurto_centralina.date() + "Fuori dal ciclo while main\n" +
        Antifurto_centralina.date() + "Programma terminato grazie per averci testato")
