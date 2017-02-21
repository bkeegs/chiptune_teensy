#include <pitches.h>

int melody0[] = {
NOTE_E4,
NOTE_FS4,
NOTE_GS4,
NOTE_GS4,
NOTE_GS4,
NOTE_B4,
NOTE_CS5,
NOTE_DS5,
NOTE_DS5,
NOTE_DS5,
NOTE_E5,
};

int start_time0[] = {
0.0,
194805.0,
389610.0,
584415.0,
681817.5,
779220.0,
974025.0,
1168830.0,
1363635.0,
1461037.5,
1558440.0,
};

int duration0[] = {
194805.0,
194805.0,
97402.5,
97402.5,
97402.5,
194805.0,
194805.0,
97402.5,
97402.5,
97402.5,
779220.0,
};

int melody1[] = {
NOTE_GS5,
NOTE_GS5,
NOTE_GS5,
NOTE_E5,
NOTE_E5,
NOTE_E5,
NOTE_B5,
NOTE_B5,
NOTE_B5,
NOTE_A5,
NOTE_A5,
NOTE_A5,
NOTE_GS5,
};

int start_time1[] = {
0.0,
194805.0,
292207.5,
389610.0,
584415.0,
681817.5,
779220.0,
974025.0,
1071427.5,
1168830.0,
1363635.0,
1461037.5,
1558440.0,
};

int duration1[] = {
194805.0,
97402.5,
97402.5,
194805.0,
97402.5,
97402.5,
194805.0,
97402.5,
97402.5,
194805.0,
97402.5,
97402.5,
779220.0,
};

int melody2[] = {
NOTE_B4,
NOTE_CS5,
NOTE_DS5,
NOTE_FS5,
NOTE_G5,
NOTE_GS5,
};

int start_time2[] = {
0.0,
389610.0,
779220.0,
1168830.0,
1363635.0,
1558440.0,
};

int duration2[] = {
194805.0,
194805.0,
194805.0,
194805.0,
194805.0,
1168830.0,
};



int main_cycle_usec = 10;
int master_time = 0;

int notepin0 = 3;
int notepin2 = 5;
int notepin1 = 25;

int elapsed0 = 0;
int elapsed1 = 0;
int elapsed2 = 0;

int state0 = 0;
int state1 = 0;
int state2 = 0;

void setup() {
  Serial.begin(9600);
  pinMode(13, OUTPUT);
  pinMode(notepin0, OUTPUT);
  pinMode(notepin1, OUTPUT);
  pinMode(notepin2, OUTPUT);

  digitalWrite(13, HIGH);
  delay(500);
  digitalWrite(13, LOW);
  delay(500);
  digitalWrite(13, HIGH);
  delay(500);
  digitalWrite(13, LOW);
  delay(500);
//  tone(3, 40);
//  tone(9, 440);
  
}

float current_time;

int size0 = sizeof(melody0)/sizeof(melody0[0]);
int size1 = sizeof(melody1)/sizeof(melody1[0]);
int size2 = sizeof(melody2)/sizeof(melody2[0]);


void loop() {
  Serial.println(size0);
  Serial.println(size1);
  Serial.println(size2);
  
  int usec2 = 0;//(1000000/freq2)/2;

  int end0 = 0;
  int end1 = 0;
  int end2 = 0;

  int i = -1;
  int j = -1;
  int k = -1;
    
  int note0_active = 0;
  float note0_start = 0;
  float note0_end = micros();
  float wait_time0 = 0;
  
  int note1_active = 0;
  float note1_start = 0;
  float note1_end = micros();
  float wait_time1 = 0;
  
  int note2_active = 0;
  float note2_start = 0;
  float note2_end = micros();
  float wait_time2 = 0;

  float start_time = micros();

  while(1){

    current_time = micros();


    // ### VOICE 0 ### //
        
    if (!note0_active){
      // Check if voice is already done, do nothing if True
      if (end0){
        i;
      }
      // Check if note needs to start
      else if ((current_time - note0_end) >= wait_time0){
        i++;
//        Serial.print("I: ");
//        Serial.println(i);
        note0_active = 1;
        analogWriteFrequency(notepin0, melody0[i]);
        analogWrite(notepin0, 128);
        note0_start = micros();
      }
    }
    else{
      // Check if note needs to end      
      if ((current_time - note0_start) >= duration0[i]){
        note0_active = 0;
        analogWrite(notepin0, 0);

        // Check if already at song end
        if (i+1 == size0){
//          Serial.println("END0");
          end0 = 1;
        }
        else{
          note0_end = micros();
          wait_time0 = start_time0[i+1] - (start_time0[i] + duration0[i]); // consider hardcoding this to reduce cycle time
        }
      }  
    }



    // ### VOICE 1 ### //
    
    if (!note1_active){
      // Check if voice is already done, do nothing if True
      if (end1){
        j;
      }
      // Check if note needs to start
      else if ((current_time - note1_end) >= wait_time1){
        j++;
//        Serial.print("J: ");
//        Serial.println(j);
        note1_active = 1;
        analogWriteFrequency(notepin1, melody1[j]);
        analogWrite(notepin1, 128);
        note1_start = micros();
      }
    }
    else{
      // Check if note needs to end      
      if ((current_time - note1_start) >= duration1[j]){
        note1_active = 0;
        analogWrite(notepin1, 0);

        // Check if already at song end
        if (j+1 == size1){
//          Serial.println("END1");
          end1 = 1;
        }
        else{
          note1_end = micros();
          wait_time1 = start_time1[j+1] - (start_time1[j] + duration1[j]); // consider hardcoding this to reduce cycle time
        }
      }
    }


    // ### VOICE 2 ### //

    if (!note2_active){
      // Check if voice is already done, do nothing if True
      if (end2){
        k;
      }
      // Check if note needs to start
      else if ((current_time - note2_end) >= wait_time2){
        k++;
//        Serial.print("k: ");
//        Serial.println(k);
        note2_active = 1;
        analogWriteFrequency(notepin2, melody2[k]);
        analogWrite(notepin2, 128);
        note2_start = micros();
      }
    }
    else{
      // Check if note needs to end      
      if ((current_time - note2_start) >= duration2[k]){
        note2_active = 0;
        analogWrite(notepin2, 0);

        // Check if already at song end
        if (k+1 == size2){
//          Serial.println("END2");
          end2 = 1;
        }
        else{
          note2_end = micros();
          wait_time2 = start_time2[k+1] - (start_time2[k] + duration2[k]); // consider hardcoding this to reduce cycle time
        }
      }
    }
//
//    if (!note2_active){
//      // Check if voice is already done, do nothing if True
//      if (end2){
//        k;
//      }
//      // Check if note needs to start
//      else if ((current_time - note2_end) >= wait_time2){
//        k++;
////        Serial.print("K: ");
////        Serial.println(k);
//        note2_active = 1;
//        digitalWrite(notepin2, HIGH);
//        elapsed2 = 0;
//        note2_start = micros();
//        usec2 = (1000000/melody2[k])/2;
//      }
//    }
//    else{
//      // Check if note needs to end      
//      if ((current_time - note2_start) >= duration2[k]){
//        note2_active = 0;
//        digitalWrite(notepin2, LOW);
//
//        // Check if already at song end
//        if (k+1 == size2){
////          Serial.println("END2");
//          end2 = 1;
//        }
//        else{
//          note2_end = micros();
//          wait_time2 = start_time2[k+1] - (start_time2[k] + duration2[k]); // consider hardcoding this to reduce cycle time
//        }
//      }

//      // If didn't end, check proper note state and set if needed
//      if (elapsed2 > usec2){
//        state2 = !state2;
//        digitalWrite(notepin2, state2);
//        elapsed2 = 0;
//      }      
//    }

    // If all voices are finished, break out of while loop and play song again
    if (end0 & end1 & end2){
      break;
    }

//    elapsed2 += main_cycle_usec;
    delayMicroseconds(main_cycle_usec);
  }

  digitalWrite(13, HIGH);
  delay(500);
  digitalWrite(13, LOW);
  delay(500);
  digitalWrite(13, HIGH);
  delay(500);
  digitalWrite(13, LOW);
  delay(500);
}
