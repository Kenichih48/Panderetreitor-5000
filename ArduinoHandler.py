import serial
import time

class ArduinoHandler:

    def __init__(self):
        self.metronome = []
        self.pila = []
        self.i = 0

    def add_metronome(self, metronome):
        self.metronome.append(metronome+"\n")
    
    def add_pila(self,instruction):

        if (self.pila.length == 0):

            self.pila.append(instruction)
        else:
            self.pila[self.i] += instruction

    def next_pila(self):
        self.i += 1


arduinoData = serial.Serial('com4', baudrate= 9600,timeout=1)
time.sleep(3)

def send_data(entrada):
    
    arduinoData.write(entrada.encode())


while 1:
    Uinput = input("Get accion: ")

    send_data(Uinput)





    




