void setup() {
  Serial.begin(9600);
}
void loop() {
   /*
   //TESTING - Repeat antwoord 
   Serial.println("a_ts");
  delay(3000);
   Serial.println("a_none");
  delay(3000);
   Serial.println("a_ts");
  delay(3000);
   Serial.println("a_none");
  delay(3000);
 Serial.println("a_ts");
  delay(1000); */

  //Autoreset_test
  /*
  Serial.println("a_ts");
  delay(301000);

   */

  //Error_Oppak_test
  /*
  Serial.println("0_none");
  delay(2000);
  Serial.println("2_none");
  delay(2000);
  Serial.println("5_none");
  delay(2000);
  Serial.println("2_ts");
  delay(2000);
  Serial.println("5_rs");
  delay(2000);
   */

//Doorloop_test
/*
  //Geeft telkens het "fake" antwoord met verschillende tijd er tussen
   Serial.println("a_ts");
   delay(5000);
   Serial.println("a_ts");
   delay(4000);
   Serial.println("a_ts");
   delay(6700);
   Serial.println("a_ts");
   delay(4500);
   Serial.println("a_ts");
   delay(5100);
 */


//Reset_test
/*
 //Beantwoord twee vragen en geeft het reset command naar de Pi
  Serial.println("a_ts");
  delay(3000);
  Serial.println("a_ts");
  delay(3000);
  Serial.println("reset");
  delay(8000);
  */

  //Informatie_test
 /*
  //Arduino code om alle informatie af te gaan
   Serial.println("0_none");
  delay(2000);
    Serial.println("0_mn");
  delay(2000);
   Serial.println("1_none");
  delay(2000);
    Serial.println("1_sn");
  delay(2000);
  Serial.println("2_none");
  delay(2000);
    Serial.println("2_ts");
  delay(2000);
  Serial.println("3_none");
  delay(2000);
    Serial.println("3_jm");
  delay(2000);
    Serial.println("4_none");
  delay(2000);
    Serial.println("4_sc");
  delay(2000);
    Serial.println("5_none");
  delay(2000);
    Serial.println("5_rs");
  delay(2000);
  */
  
}
