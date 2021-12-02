#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN 10
#define SS_2_PIN 5
#define RST_PIN 9

#define NR_OF_READERS   2
byte ssPins[] = {SS_PIN, SS_2_PIN};
MFRC522 mfrc522[NR_OF_READERS];
bool statusReaders[NR_OF_READERS];


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
}

void check_code(String code, uint8_t numberReader){
  String arduinoMessage = String(numberReader);
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

void loop() {
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
    }else{
        if(statusReaders[reader] == true){
          String arduinoMessage = String(reader);
          arduinoMessage = arduinoMessage + "_none";
          Serial.println(arduinoMessage);
         // Serial.print("geen kaart op ");
        //  Serial.println(reader);
          statusReaders[reader] = false;
        }
    
      
    }
  }
  
}
