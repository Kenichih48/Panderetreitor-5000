import serial
import time

class ArduinoHandler:

    def __init__(self):
        self.metronome = []
        self.pila = []
        self.i = -1
        self.arduinoData = None
        self.start()

    def start(self):
        self.arduinoData = serial.Serial('/dev/ttyACM0', baudrate= 9600,timeout=1)
        time.sleep(3)
        

    def add_metronome(self, metronome):
        self.metronome.append(metronome)
        self.next_pila()
    
    def add_pila(self,instruction):

        if (len(self.pila) == 0):

            self.pila.append(instruction)
        else:
            try:
                self.pila[self.i] += instruction
            except IndexError:
                self.pila.append(instruction)

    def next_pila(self):
        self.i += 1

    def send_data(self):

        i1=0
        while i1<len(self.metronome):
            
            met = self.metronome[i1]+"\n"
            self.arduinoData.write(met.encode())

            pil = self.pila[i1]+"\n"
            self.arduinoData.write(pil.encode())
            i1+=1

    def reset(self):
        self.metronome = []
        self.pila = []
        self.i =-1






    




