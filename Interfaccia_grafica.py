from tkinter import *
from tkinter import messagebox
import Antifurto_centralina
import Antifurto_main
import time
from threading import Thread
from datetime import datetime
import os
import sys

log_print = Antifurto_centralina.logger.info
stringer = (datetime.now().strftime(Antifurto_centralina.formato_data_ora))
stringer = stringer + ": Nothing to report"
log_print(stringer)


def code_antifuto_main(attesa):
    Antifurto_main.main_program()  # per iniziare tutto
    if Antifurto_main.kill_interface:
        on_closing()
    time.sleep(attesa)


thread_antifurto_main = Thread(target=code_antifuto_main, args=(2,))
thread_antifurto_main.start()


def B_H():  # evento alla pressione del tasto #TASTO PRINCIPALE,HOME

    home = Label(f, width=175, height=50)
    home.place(y=100)
    xlog = 400
    ylog = 250

    home1 = Label(f, text='AUTENTIFICAZIONE', font='Times 22')
    home1.place(x=xlog + 10, y=130)

    def PressionePulsante():
        user = c_user.get()
        password = c_pass.get()

        if (password == Antifurto_centralina.pwd) & (user == Antifurto_centralina.user):
            b1.configure(state=ACTIVE)
            b2.configure(state=ACTIVE)
            b1.configure(cursor="hand2")
            b2.configure(cursor="hand2")
            l_mex.config(text="Ciao \"" + Antifurto_centralina.user + "\" log-in effettuato correttamente")
        else:
            l_mex.config(text='Credenziali di log-in errate')

    def elimina():
        answer = messagebox.askyesno('Login', 'Vuoi annullare?')
        messagebox.showwarning('Attenzione', 'Login annullato')
        c_user.delete(0, 100)
        c_pass.delete(0, 100)
        l_mex.config(text='')

    # LABEL
    l_login = Label(f, text='Login')
    l_login.place(x=xlog, y=ylog)

    l_pass = Label(f, text='Password')
    l_pass.place(x=xlog, y=ylog + 50)

    l_mex = Label(f, text='')
    l_mex.place(x=xlog, y=370)

    # BOTTONI
    bl1 = Button(f, text='Accedi', command=PressionePulsante)
    bl1.place(x=xlog + 70, y=330)

    bl2 = Button(f, text='Annulla', command=elimina)
    bl2.place(x=xlog + 140, y=330)

    # TESTO
    c_user = Entry(f)
    c_user.place(x=xlog + 70, y=ylog)
    c_user.focus_set()  # va a impostare il cursore già sulla casella di testo(tastiera)
    c_user.insert(0, "Inserisci nome utente")
    c_user.select_range(0, END)

    c_pass = Entry(f, show='*****')
    c_pass.place(x=xlog + 70, y=ylog + 50)
    c_pass.focus_set()  # va a impostare il cursore già sulla casella di testo(tastiera)
    c_pass.insert(0, "Inserisci password")
    c_pass.select_range(0, END)



def button_log():  # TASTO PRINCIPALE, LOG
    os.startfile("Log.log")


s_color = 'light grey'
color_bck= "cyan"

def button_sensors():  # TASTO PRINCIPALE,  SENSORI
    global color_bck
    sensor = Label(f, width=175, height=50, bg=color_bck)

    sensor.place(y=100)

    global s_color

    tela = Canvas(f, width=700, height=500)
    tela.place(x=300, y=150)

    tela.create_line(50, 150, 125, 150)
    tela.create_line(125, 150, 175, 150, dash=3, fill='red')
    tela.create_line(175, 150, 250, 150)
    tela.create_line(250, 150, 250, 50)

    tela.create_line(250, 50, 325, 50)
    tela.create_line(325, 50, 375, 50, dash=3, fill='red')
    tela.create_line(375, 50, 650, 50)

    tela.create_line(450, 50, 450, 100)
    tela.create_rectangle(445, 100, 455, 150)
    tela.create_line(450, 150, 450, 200)

    tela.create_line(450, 200, 650, 200)
    tela.create_line(650, 50, 650, 100)
    tela.create_line(650, 100, 650, 150, dash=3, fill='red')
    tela.create_line(650, 150, 650, 200)

    tela.create_line(650, 200, 650, 400)

    tela.create_line(650, 400, 550, 400)
    tela.create_line(550, 400, 500, 400, dash=3, fill='red')
    tela.create_line(500, 400, 350, 400)

    tela.create_line(350, 400, 350, 450)
    tela.create_line(350, 450, 50, 450)

    tela.create_line(50, 450, 50, 250)
    tela.create_line(50, 250, 50, 200, dash=3, fill='red')
    tela.create_line(50, 200, 50, 150)
    tela.create_rectangle(45, 250, 55, 200)

    tela.create_line(350, 450, 350, 300)

    tela.create_line(350, 300, 250, 300)
    tela.create_line(250, 300, 200, 300, dash=3, fill='green')
    tela.create_line(200, 300, 50, 300)
    tela.create_rectangle(250, 295, 200, 305)

    tela.create_oval(195, 160, 220, 185, fill='black')
    tela.create_line(50, 225, 207.5, 172.5, dash=3)

    # creo etichette prendendo i valori boolean da antifurto main usando le funzioni pass
    etichetta_x = 220
    msg_true = "True"
    msg_false = "False"

    s1_label = Label(f, text='SENSORE FINESTRA 1: ')
    s1_label.place(x=50, y=150)
    s1_status = Label(f)
    s1_status.place(x=etichetta_x, y=150)
    if not Antifurto_main.pass_sensor_win0():
        s1_status.config(text=msg_false)
        s_color = "light green"
        tela.create_oval(140, 140, 160, 160, fill=s_color)
        tela.create_text(150, 150, text='S1')
    else:
        s1_status.config(text=msg_true)
        s_color = "red"
        tela.create_oval(140, 140, 160, 160, fill=s_color)
        tela.create_text(150, 150, text='S1')

    s2_label = Label(f, text='SENSORE FINESTRA 2: ')
    s2_label.place(x=50, y=200)
    s2_status = Label(f)
    s2_status.place(x=etichetta_x, y=200)
    if not Antifurto_main.pass_sensor_win1():
        s2_status.config(text=msg_false)
        s_color = "light green"
        tela.create_oval(340, 40, 360, 60, fill=s_color)
        tela.create_text(350, 50, text='S2')
    else:
        s2_status.config(text=msg_true)
        s_color = "red"
        tela.create_oval(340, 40, 360, 60, fill=s_color)
        tela.create_text(350, 50, text='S2')

    s3_label = Label(f, text='SENSORE FINESTRA 3: ')
    s3_label.place(x=50, y=250)
    s3_status = Label(f)
    s3_status.place(x=etichetta_x, y=250)
    if not Antifurto_main.pass_sensor_win2():
        s3_status.config(text=msg_false)
        s_color = "light green"
        tela.create_oval(640, 115, 660, 135, fill=s_color)
        tela.create_text(650, 125, text='S3')
    else:
        s3_status.config(text=msg_true)
        s_color = "red"
        tela.create_oval(640, 115, 660, 135, fill=s_color)
        tela.create_text(650, 125, text='S3')

    s4_label = Label(f, text='SENSORE FINESTRA 4: ')
    s4_label.place(x=50, y=300)
    s4_status = Label(f)
    s4_status.place(x=etichetta_x, y=300)
    if not Antifurto_main.pass_sensor_win3():
        s4_status.config(text=msg_false)
        s_color = "light green"
        tela.create_oval(515, 390, 535, 410, fill=s_color)
        tela.create_text(525, 400, text='S4')
    else:
        s4_status.config(text=msg_true)
        s_color = "red"
        tela.create_oval(515, 390, 535, 410, fill=s_color)
        tela.create_text(525, 400, text='S4')

    s5_label = Label(f, text='SENSORE PORTA: ')
    s5_label.place(x=50, y=350)
    s5_status = Label(f)
    s5_status.place(x=etichetta_x, y=350)
    if not Antifurto_main.pass_sensor_door():
        s5_status.config(text=msg_false)
        s_color = "light green"
        tela.create_oval(215, 290, 235, 310, fill=s_color)
        tela.create_text(225, 300, text='SP')
    else:
        s5_status.config(text=msg_true)
        s_color = "red"
        tela.create_oval(215, 290, 235, 310, fill=s_color)
        tela.create_text(225, 300, text='SP')

    s6_label = Label(f, text='SENSORE DI MOVIMENTO: ')
    s6_label.place(x=50, y=400)
    s6_status = Label(f)
    s6_status.place(x=etichetta_x, y=400)
    if not Antifurto_main.pass_sensor_motion():
        s6_status.config(text=msg_false)
        s_color = "light green"
        tela.create_polygon(195, 160, 230, 150, 220, 185, 195, 160, fill=s_color)
        tela.create_text(213, 164, text='SM')
    else:
        s6_status.config(text=msg_true)
        s_color = "red"
        tela.create_polygon(195, 160, 230, 150, 220, 185, 195, 160, fill=s_color)
        tela.create_text(213, 164, text='SM')

    s7_label = Label(f, text='SIRENA: ')
    s7_label.place(x=50, y=500)
    s7_status = Label(f)
    s7_status.place(x=etichetta_x, y=500)
    if not Antifurto_main.pass_siren():
        s7_status.config(text=msg_false)
    else:
        s7_status.config(text=msg_true)
        color_bck = "red"
    # creo etichette prendendo i valori boolean da antifurto main usando le funzioni pass

    f.after(5000, button_sensors)  # ripeto il codice ogni 5  secondi, usando il metodo after di tkinter


def on_closing():
    if Antifurto_main.kill_interface:
        f.destroy()  # distruggo la finestra
        thread_antifurto_main.join()
        sys.exit()
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        Antifurto_main.on_destroy()  # richiamo la funzione destroy del main
        f.destroy()  # distruggo la finestra
        Antifurto_main.for_closing = False  # false così posso stoppare i while nel main
        thread_antifurto_main.join()




# titolo e parametri finestra
f = Tk()
f.title("finestra")  # titolo finestra
f.geometry("1100x700")
f.configure(background="CYAN")
f.resizable(FALSE, FALSE)
f.protocol("WM_DELETE_WINDOW", on_closing)  # per distruggere la finestra
welcome = Label(f, font="Times 50", width=15)
welcome.place(x=275 + 15 / 2, y=400)
welcome.config(text='Benvenuto')
# titolo e parametri finestra


# testo nome app
testox = Label(f, text="Pezzini, Vulcan, La Sala", font="italic 15", bg="cyan")
testox.pack(side=BOTTOM)
testo = Label(f, text="ANTIFURTO", background="cyan", font="Times 28 bold underline")
testo.pack(side=TOP)  # impacchetamento della label per poterlo visualizzare
# side = lato del testo nella finestra
testo.configure(foreground="black")  # colore testo
testo.configure(cursor="hand2")  # cambiare cursore
# testo nome app

# Pulsanti
b0 = Button(f, text="HOME", command=B_H, width=10)  # command per assegnare al bottone la funzione
b0.place(x=50, y=50)
b1 = Button(f, text="SENSORI", command=button_sensors, width=10)
b1.place(x=500, y=50)
b1.configure(state=DISABLED)
b2 = Button(f, text="LOG", command=button_log, width=10)
b2.place(x=950, y=50)
b2.configure(state=DISABLED)
# Pulsanti

f.mainloop()  # serve per mandare in loop la finestra
