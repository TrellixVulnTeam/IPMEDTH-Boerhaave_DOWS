#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN 10
#define SS_2_PIN 5
#define RST_PIN 9
#define SS_ANSWER_PIN 3

#define NR_OF_READERS   3
//SS_ANSWER_PIN als laatste
byte ssPins[] = {SS_PIN, SS_2_PIN, SS_ANSWER_PIN};
MFRC522 mfrc522[NR_OF_READERS];
bool statusReaders[NR_OF_READERS];

int pushButton = 2; 
bool buttonPressed = false;

void setup() {
  Serial.begin(9600);
  SPI.begin(); // init SPI bus
//  rfid.PCD_Init(); // init MFRC522
  //second_rfid.PCD_Init();

  for (uint8_t reader = 0; reader < NR_OF_READERS; reader++) {
    mfrc522[reader].PCD_Init(ssPins[reader], RST_PIN);
    Serial.print(F("Reader "));
    Serial.print(reader);
    Serial.print(F(": "));
    mfrc522[reader].PCD_DumpVersionToSerial();
    //mfrc522[reader].PCD_SetAntennaGain(mfrc522[reader].RxGain_max);
  }

  for(int i = 0; i < sizeof(statusReaders); i++){
    statusReaders[i] = false;
  }

  Serial.println("Tap RFID/NFC Tag on reader");
  pinMode(pushButton, INPUT);
}

void check_code(String code, uint8_t numberReader){
  String arduinoMessage;
  //checkt of het de laatste nfc reader (antwoord) en zet de naam van de nfcreader in de message
  if(numberReader == (NR_OF_READERS - 1)){
     arduinoMessage = "a";
  }else{
     arduinoMessage = String(numberReader);
  }
  if(code == " 04 77 42 7c b0 e9 30"){
    arduinoMessage = arduinoMessage + "_mn";
  }else if(code == " 04 77 42 ca c1 e4 30"){
     arduinoMessage = arduinoMessage + "_sn";
  }
  Serial.println(arduinoMessage);
}

void translate_input(byte * buffer, byte bufferSize, uint8_t numberReader ){
  String NFCCode = "";
   for (int i = 0; i < bufferSize; i++) {
       NFCCode = NFCCode + String(buffer[i] < 0x10 ? " 0" : " ");
       NFCCode = NFCCode + String(buffer[i], HEX);
    }
    check_code(NFCCode, numberReader);
}

void resetScan(){
  for(uint8_t reader = 0; reader < NR_OF_READERS; reader++){
    Serial.print("scanner momenteel: ");
    Serial.println(statusReaders[reader]);
     if(mfrc522[reader].PICC_IsNewCardPresent() ){
        if(mfrc522[reader].PICC_ReadCardSerial()){
          
          mfrc522[reader].PICC_ReadCardSerial();
          
          translate_input(mfrc522[reader].uid.uidByte, mfrc522[reader].uid.size, reader);
          mfrc522[reader].PICC_HaltA(); // halt PICC
          mfrc522[reader].PCD_StopCrypto1();
        }
     }
     else{
      String arduinoMessage = String(reader);
      arduinoMessage = arduinoMessage + "_none";
      Serial.println(arduinoMessage);
     }
     delay(100);
  }
}

void loop() {
  //checkt of de "reset" knop is in gedruk
  if(digitalRead(pushButton)){
      if(digitalRead(pushButton) && !(buttonPressed)){
      buttonPressed = true;
      Serial.println("reset");
      resetScan();
    }
  }
  //als de knop los gelaten wordt, return naar niet ingedrukte state
  else if( !(digitalRead(pushButton)) && buttonPressed){
      Serial.print("in");
      buttonPressed = false;
  }
  //leest de veranderingen van de NFCreaders
  else{
    for (uint8_t reader = 0; reader < NR_OF_READERS; reader++) {
     // Serial.println(NR_OF_READERS);
    
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
      }else{
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
