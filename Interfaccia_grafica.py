from tkinter import *
import Antifurto_main
import time
from threading import Thread

nome = "Bob"
attesa= 2

def code_My_Thread(nome, attesa):
    Antifurto_main.main_program()  # per iniziare tutto
    time.sleep(attesa)

th1 = Thread(target=code_My_Thread, args=(nome, attesa))
th1.start()


# Antifurto_main.on_Destroy()  # per killare tutto
# Antifurto_main.pass_sensor_win0()   # per passare gli stati dei sensori
# Antifurto_main.pass_sensor_win1()   # per passare gli stati dei sensori
# Antifurto_main.pass_sensor_win2()   # per passare gli stati dei sensori
# Antifurto_main.pass_sensor_win3()   # per passare gli stati dei sensori
# Antifurto_main.pass_sensor_door()   # per passare gli stati dei sensori
# Antifurto_main.pass_sensor_motion() # per passare gli stati dei sensori
# Antifurto_main.pass_siren() # per passare lo stato della sirena


def B_H():  # evento alla pressione del tasto #TASTO PRINCIPALE,HOME

    home = Label(f, width=145, height=50)
    home.place(y=100)

    home2 = Label(f, font="Times 25")
    home2.place(x=450, y=100)
    home2.config(text='HOME')

    def bh1():
        '''
        nuovo = Tk()
        nuovo.title("finestra") #titolo finstra
        nuovo.geometry("1000x700")
        nuovo.configure(background = "RED")
'''
        home = Label(f, font="Times 22")
        home.place(x=100, y=200)
        home.config(text='TESTO 1')

    def bh2():
        home = Label(f, font="Times 22")
        home.place(x=400, y=200)
        home.config(text='TESTO 2')

    def bh3():
        home = Label(f, font="Times 22")
        home.place(x=700, y=200)
        home.config(text='TESTO 3')

    b_h_1 = Button(f, text='B1', command=bh1)
    b_h_1.place(x=250, y=150)
    b_h_2 = Button(f, text='B2', command=bh2)
    b_h_2.place(x=450, y=150)
    b_h_3 = Button(f, text='B3', command=bh3)
    b_h_3.place(x=650, y=150)


def B_S():  # TASTO PRINCIPALE, STATO
    stato = Label(f, width=145, height=50)
    stato.place(y=100)

    stato2 = Label(f, font="Times 25")
    stato2.place(x=450, y=100)
    stato2.config(text='STATO')

    def bs1():
        home = Label(f, font="Times 22")
        home.place(x=100, y=200)
        home.config(text='TESTO 1')

    def bs2():
        home = Label(f, font="Times 22")
        home.place(x=300, y=200)
        home.config(text='TESTO 2')

    def bs3():
        home = Label(f, font="Times 22")
        home.place(x=600, y=200)
        home.config(text='TESTO 3')

    b_s_1 = Button(f, text='B1', command=bs1)
    b_s_1.place(x=250, y=150)
    b_s_2 = Button(f, text='B2', command=bs2)
    b_s_2.place(x=450, y=150)
    b_s_3 = Button(f, text='B3', command=bs3)
    b_s_3.place(x=650, y=150)


def B_L():  # TASTO PRINCIPALE, LOG
    log = Label(f, width=145, height=50)
    log.place(y=100)


def B_P():  # TASTO PRINCIPALE,POLICE
    police = Label(f, width=145, height=50)
    police.place(y=100)
    police.config(text='POLIZIAAAAAAA')


def B_SENS():  # TASTO PRINCIPALE,  SENSORI
    sensor = Label(f, width=145, height=50, bg='red')
    sensor.place(y=100)
    # sensor.config(text = 'SENSORI')

    sens = Label(f, font="Times 25", width=10)
    sens.place(x=495, y=100)
    sens.config(text='SENSORI')

    tela = Canvas(f, width=700, height=500)
    tela.place(x=200, y=200)
    # tela.create_rectangle(5, 5, 50, 50, fill = 'black', activefill = 'red')
    # tela.create_text (100, 100, text = 'CIAO', font = 'Comics 34')
    # tela.create_polygon(100, 100, 200, 200, 100, 200, 100, 100, fill = 'green', activefill = 'red')

    tela.create_line(50, 150, 125, 150)
    tela.create_line(125, 150, 175, 150, dash=3, fill='red')
    tela.create_line(175, 150, 250, 150)
    tela.create_text(150, 150, text='S1')

    tela.create_line(250, 150, 250, 50)

    tela.create_line(250, 50, 325, 50)
    tela.create_line(325, 50, 375, 50, dash=3, fill='red')
    tela.create_line(375, 50, 650, 50)
    tela.create_text(350, 50, text='S2')

    tela.create_line(450, 50, 450, 100)
    tela.create_line(450, 150, 450, 200)

    tela.create_line(450, 200, 650, 200)
    tela.create_line(650, 50, 650, 200)
    tela.create_line(650, 200, 650, 400)

    tela.create_line(650, 400, 350, 400)

    tela.create_line(350, 400, 350, 450)
    tela.create_line(350, 450, 50, 450)

    tela.create_line(50, 450, 50, 150)

    tela.create_line(350, 450, 350, 300)

    tela.create_line(350, 300, 250, 300)
    tela.create_line(250, 300, 200, 300, dash=3, fill='red')
    tela.create_line(200, 300, 50, 300)

    # tela.create_oval(125, 125, 150, 150, fill = 'black',  activefill = 'red')


'''
#b_sens_1 = Button(f, text = 'B3', command = bsens1)
#b_sens_1.place(x = 650, y = 150)

#def bsens1():

'''

# titolo e parametri finestra
f = Tk()
f.title("finestra")  # titolo finstra
f.geometry("1000x700")
f.configure(background="RED")

# testo
testo = Label(f, text="ANTIFURTO", background="blue", font="Times 22")
testo.pack(side=TOP)  # impacchetamento della label per poterlo vizualizzare
# side = lato del testo nella finestra
testo.configure(foreground="white")  # colore testo
testo.configure(cursor="hand2")  # cambiare cursore

# BOTTONI PRINCIPALI
b = Button(f, text="HOME", command=B_H, width=10)  # command per assegnare al bottone la funzione
b.place(x=50, y=50)

b1 = Button(f, text="STATUS", command=B_S, width=10)
b1.place(x=250, y=50)

b2 = Button(f, text="LOG", command=B_L, width=10)
b2.place(x=450, y=50)

b3 = Button(f, text="POLICE", command=B_P, width=10)
b3.place(x=650, y=50)

b4 = Button(f, text="SENSORI", command=B_SENS, width=10)
b4.place(x=850, y=50)

f.mainloop()  # serve per mandare in loop la fienstra
