/*
  Creado: Luis del Valle (ldelvalleh@programarfacil.com)
  https://programarfacil.com
*/
 
// Incluímos la librería para poder controlar el servo
#include <Servo.h>
#include <EasyBuzzer.h>
 
// Declaramos la variable para controlar el servo
Servo servoEje1;
Servo servoEje2;
Servo servoGolpe1;
Servo servoGolpe2;
Servo servoGolpe3;
Servo servoGolpe4;
Servo servoGolpe5;


bool metroMode;
int freq1 = 440; 
int freq2 = 329;
int tempo;


int ledPin = 10;
String movement;
String wordRecieved = "";
int lastMove = 0;
int totalMoves = 0;
int movesQueue = 0;

bool reTurnOn = false;
bool UpDown = true;

void setup() {

  Serial.begin(9600);
 

  servoEje1.attach(3);
  servoEje2.attach(4);
  servoGolpe1.attach(6);
  servoGolpe2.attach(7);
  servoGolpe3.attach(8);
  servoGolpe4.attach(5);
  servoGolpe5.attach(11);
  
  EasyBuzzer.setPin(9);
  
  
  servoEje1.write(90);
  servoEje2.write(90);
  servoGolpe1.write(0);
  servoGolpe2.write(0);
  servoGolpe3.write(0);
  servoGolpe4.write(0);
  servoGolpe5.write(0);
  
  digitalWrite(ledPin, LOW); 
  
}
 
void loop() {
  
  checkMessages();
  metronomo();
}

void checkMessages(){
  
  if (Serial.available() > 0) {
    
    int incomingByte = 0;
    incomingByte = Serial.read();
    
    
    Serial.print("I received: ");
    Serial.println(incomingByte, DEC);

    if (incomingByte != 10){
      wordRecieved = wordRecieved + (char)incomingByte;
    }else{
      Serial.print("Recibo: ");
      Serial.println(wordRecieved);
      MessageProcessor(wordRecieved);
      wordRecieved = "";
    }


  }


}

void MessageProcessor(String message){
  
  if (message[0] == 'M'){
    float tempo1 = (float)String(message[1]).toInt();
    float tempo2 = (float)String(message[3]).toInt();
    float preTempo = (tempo1/tempo2)*1000;
    
    tempo = (int)preTempo;
    Serial.print("El tempo es de: ");
    Serial.println(preTempo);
    Serial.println(tempo);
    reTurnOn = true;
    metroMode = true;
    
  }else if(message[0] == 'P'){
    metroMode = false;
    reTurnOn = false;
    tempo = 0;
  }
  
  else{
    lastMove = 0;
    movement = (String)message;
    movesQueue = message.length();
    Serial.print("Se ejecuta el movimiento: ");
    Serial.println(movement);
    
  }
}

void metronomo(){

  if (metroMode && movement != ""){
    digitalWrite(ledPin, HIGH);
    EasyBuzzer.beep(freq1);
    if (lastMove < movesQueue){
      performMovement();
      lastMove ++;
    }else{
      movement = "";
    }
    delay(tempo);
    digitalWrite(ledPin, LOW);
    EasyBuzzer.stopBeep();
    returnMoves();
    delay(tempo);
  }else{
    digitalWrite(ledPin, LOW);
    EasyBuzzer.stopBeep();
  }
  
}


void performMovement(){
  Serial.println("Se procede a ejecutar el movimiento: ");

  if (movement[lastMove] == 'A'){
    servoEje1.write(45);
  }else if (movement[lastMove] == 'B'){
    servoEje1.write(135);
  }else if (movement[lastMove] == 'D'){
    servoEje2.write(45);
  }else if (movement[lastMove] == 'I'){
    servoEje2.write(135);
  }else if (movement[lastMove] == 'G'){
    servoGolpe3.write(45);
  }else if (movement[lastMove] == 'R'){
    servoGolpe1.write(90);
  }else if (movement[lastMove] == 'L'){
    servoGolpe2.write(90);
  }else if (movement[lastMove] == 'U'){
    servoGolpe4.write(90);
  }else if (movement[lastMove] == 'O'){
    servoGolpe5.write(90);
  }
  
}
void returnMoves(){
  if (movement[lastMove-1] == 'A' || movement[lastMove-1] == 'B'){
    servoEje1.write(90);
  }else if (movement[lastMove-1] == 'D' || movement[lastMove-1] == 'I'){
    servoEje2.write(90);
  }else if (movement[lastMove-1] == 'G'){
    servoGolpe3.write(0);
  }else if (movement[lastMove-1] == 'R'){
    servoGolpe1.write(0);
  }else if (movement[lastMove-1] == 'U'){
    servoGolpe4.write(0);
  }else if (movement[lastMove-1] == 'L'){
    servoGolpe2.write(0);
  }else if (movement[lastMove-1] == 'O'){
    servoGolpe5.write(0);
  }
}
