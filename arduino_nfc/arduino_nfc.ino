#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN 10
#define SS_2_PIN 8
#define SS_3_PIN 7
#define SS_4_PIN 6
#define SS_5_PIN 5
#define SS_6_PIN 4
#define RST_PIN 9
#define SS_ANSWER_PIN 3

#define NR_OF_READERS 7
//SS_ANSWER_PIN als laatste
byte ssPins[] = {SS_PIN, SS_2_PIN, SS_3_PIN, SS_4_PIN, SS_5_PIN,SS_6_PIN, SS_ANSWER_PIN};
MFRC522 mfrc522[NR_OF_READERS];
bool statusReaders[NR_OF_READERS];

int pushButton = 2; 
bool buttonPressed = false;

void setup() {
  Serial.begin(9600);
  SPI.begin(); // init SPI bus

  for (uint8_t reader = 0; reader < NR_OF_READERS; reader++) {
    mfrc522[reader].PCD_Init(ssPins[reader], RST_PIN);
    Serial.print(F("Reader "));
    Serial.print(reader);
    Serial.print(F(": "));
    mfrc522[reader].PCD_DumpVersionToSerial();
  }

  for(int i = 0; i < sizeof(statusReaders); i++){
    statusReaders[i] = false;
  }

  Serial.println("Tap RFID/NFC Tag on reader");
  pinMode(pushButton, INPUT);
}

//krijgt een NFC-chip id binnen met een nfc reader ID en kijkt of de chip ID overheen komt met een gehardcode ID
void check_code(String code, uint8_t numberReader){
  String arduinoMessage;
  //checkt of het de laatste nfc reader (antwoord) en zet de naam van de nfcreader in de message
  if(numberReader == (NR_OF_READERS - 1)){
     arduinoMessage = "a";
  }else{
     arduinoMessage = String(numberReader);
  }
  //alle ge-hardcoded NFC chip IDs
  if(code == " 04 77 42 7c b0 e9 30"){
    arduinoMessage = arduinoMessage + "_mn";
  }else if(code == " 04 77 42 ca c1 e4 30"){
     arduinoMessage = arduinoMessage + "_sn";
  }else if(code == " 04 77 42 d9 3f ea 30"){
     arduinoMessage = arduinoMessage + "_ts";
  }else if(code == " 04 77 42 07 4c d9 30"){
     arduinoMessage = arduinoMessage + "_jm";
  }else if(code == " 04 77 42 b7 aa e3 30"){
     arduinoMessage = arduinoMessage + "_sc";
  }else if(code == " 04 77 42 fb 87 df 30"){
     arduinoMessage = arduinoMessage + "_rs";
  }else{
    arduinoMessage = "bad_read";
  }
  Serial.println(arduinoMessage);
}

//krijgt de byte message van NFC-reader binnen en zet dit bericht om naar een String
void translate_input(byte * buffer, byte bufferSize, uint8_t numberReader ){
  String NFCCode = "";
   for (int i = 0; i < bufferSize; i++) {
       NFCCode = NFCCode + String(buffer[i] < 0x10 ? " 0" : " ");
       NFCCode = NFCCode + String(buffer[i], HEX);
    }
    check_code(NFCCode, numberReader);
}

//verstuurt reset naar de Pi & leest alle NFC-readers een keer door
void resetScan(){
  Serial.println("reset");
  for(uint8_t reader = 0; reader < NR_OF_READERS; reader++){
     if(mfrc522[reader].PICC_IsNewCardPresent() ){
        if(mfrc522[reader].PICC_ReadCardSerial()){
          
          mfrc522[reader].PICC_ReadCardSerial();
          
          translate_input(mfrc522[reader].uid.uidByte, mfrc522[reader].uid.size, reader);
          mfrc522[reader].PICC_HaltA(); // halt PICC
          mfrc522[reader].PCD_StopCrypto1();
        }
     }
     else{
      if(reader == (NR_OF_READERS - 1)){
        Serial.println("a_none");
      }else{
        String arduinoMessage = String(reader);
        arduinoMessage = arduinoMessage + "_none";
        Serial.println(arduinoMessage);
      }
     
     }
     delay(100);
  }
}

void loop() {
  //checkt of de "reset" knop is in gedruk
  if(digitalRead(pushButton)){
      if(digitalRead(pushButton) && !(buttonPressed)){
      buttonPressed = true;
      resetScan();
    }
  }
  //als de knop los gelaten wordt, return naar niet ingedrukte state
  else if( !(digitalRead(pushButton)) && buttonPressed){
      buttonPressed = false;
  }
  //leest de veranderingen van de NFCreaders
  else{
    for (uint8_t reader = 0; reader < NR_OF_READERS; reader++) {
    
      if(mfrc522[reader].PICC_IsNewCardPresent() ){
        if(mfrc522[reader].PICC_ReadCardSerial()){
         // !! DIT IS GEEN REDUCANT CODE. HIERDOOR WERKT HET, LAAT DEZE REGEL STAAN !!!! 
         mfrc522[reader].PICC_ReadCardSerial();
         if(statusReaders[reader] == false){
           translate_input(mfrc522[reader].uid.uidByte, mfrc522[reader].uid.size, reader);
           statusReaders[reader] = true;
         
            mfrc522[reader].PICC_HaltA(); // halt PICC
            mfrc522[reader].PCD_StopCrypto1(); // stop encryption on PCD
            }
        }
      }
      else{
          if(statusReaders[reader] == true){
            //checkt of het de laatste nfc reader (antwoord) en maakt bericht welk reader een voorwerp opgetild is
            if(reader == (NR_OF_READERS - 1))
            {
              String arduinoMessage = "a_none";
              Serial.println(arduinoMessage);
              statusReaders[reader] = false;
            }else{
              String arduinoMessage = String(reader);
              arduinoMessage = arduinoMessage + "_none";
              Serial.println(arduinoMessage);
              statusReaders[reader] = false;
            }
          }
      
        
      }
    }
  }
  
}
