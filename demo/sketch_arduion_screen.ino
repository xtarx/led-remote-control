// NeoPixel Ring simple sketch (c) 2013 Shae Erisson
// released under the GPLv3 license to match the rest of the AdaFruit NeoPixel library

#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
  #include <avr/power.h>
#endif

// Which pin on the Arduino is connected to the NeoPixels?
// On a Trinket or Gemma we suggest changing this to 1
#define PIN            13

// How many NeoPixels are attached to the Arduino?
#define NUMPIXELS      180 //76 //real count is 57



// When we setup the NeoPixel library, we tell it how many pixels, and which pin to use to send signals.
// Note that for older NeoPixel strips you might need to change the third parameter--see the strandtest
// example for more information on possible values.
Adafruit_NeoPixel pixels = Adafruit_NeoPixel(NUMPIXELS, PIN, NEO_RGBW+NEO_KHZ800);
uint32_t green = pixels.Color(255, 0, 0,0);
uint32_t red = pixels.Color(0, 255, 0,0);
uint32_t blue = pixels.Color(0, 0, 255,0);
uint32_t off = pixels.Color(0, 0, 0,0);
uint32_t backgorund = pixels.Color(0, 0, 0,1);

int delayval = 50; // delay for half a second



void setPixel(int x, int y, uint32_t color) {
  if (x==0) {
    pixels.setPixelColor(y, color);
  } else if (x==1) {
    pixels.setPixelColor(119-y, color);
  } else if (x==2) {
    pixels.setPixelColor(120+y, color);
  }
}

void setRange(int starting_index, int offset, uint32_t color) {

    for(int i=starting_index;i<offset+1;i++){
      setPixel(0, i, color);
      setPixel(1, i, color); 
      setPixel(2, i, color); 
  }
}

void setRangeRow(int row, int starting_index, int offset, uint32_t color) {

    for(int i=starting_index;i<offset+1;i++){
      setPixel(row, i, color); 
  }
}






void setArrowRight(int index, uint32_t color) {
  for (int i=index; i < index + 5; i++) {
    setPixel(1, i, color);   
  }
  setPixel(0, index+3, color);
  setPixel(2, index+3, color);
  
  
}

void setArrowLeft(int index, uint32_t color) {
  for (int i=index; i < index+5; i++) {
    setPixel(1, i, color);   
  }
  setPixel(0, index+1, color);
  setPixel(2, index+1, color);
}

void setArrowRight1(int index, uint32_t color) {
  setRange(index, index, color);
  setPixel(1, index+1, color);
}

void setArrowLeft1(int index, uint32_t color) {
  setRange(index+1, index+1, color);
  setPixel(1, index, color);
}


void door(int index, uint32_t color) {
  setRange(index, index+4, backgorund);
  setRangeRow(0, index, index+4, color);
  setRangeRow(1, index+1, index+3, color);
  setPixel(2, index+2, color);
}

void greenDoorBlinking(int index) {
  for(int i=0; i<3; i++) {
    setRange(index, index+8, pixels.Color(0, 0, 0,1));
    door(index+2, blue);
    setArrowRight1(index+i, green);
    setArrowLeft1(index+7-i, green);
    pixels.show();
    delay(200);
  }
}

void greenDoorStatic(int index) {
  setRange(index, index, pixels.Color(255, 0, 0,200));
  setRange(index+1, index+1, pixels.Color(255, 0, 0,100));
  setArrowRight1(index+2, green);
  door(index+3, blue);
  setArrowLeft1(index+5, green);
  setRange(index+6, index+6, pixels.Color(255, 0, 0,100));
  setRange(index+7, index+7, pixels.Color(255, 0, 0,200));
  pixels.show();
}

void ex(int index, uint32_t color) {
  setRange(index, index+4, backgorund);
  setPixel(0, index, color);
  setPixel(2, index, color);
  setPixel(1, index+1, color);
  setPixel(0, index+2, color);
  setPixel(2, index+2, color);
}

void staticLights(){
  setRange(0, NUMPIXELS, pixels.Color(0, 0, 0,1));
  door(5, green);
  door(20, green);
  door(35, green);
  door(50, green);
}

void setup() {
  Serial.print("test");
  Serial.begin(9600);

  // This is for Trinket 5V 16MHz, you can remove these three lines if you are not using a Trinket
#if defined (__AVR_ATtiny85__)
  if (F_CPU == 16000000) clock_prescale_set(clock_div_1);
#endif
  // End of trinket special code

  pixels.begin(); // This initializes the NeoPixel library.
  staticLights();
  pixels.show();
  pixels.setBrightness(120);
}

void repeat(){
  greenDoorBlinking(5);
  greenDoorBlinking(35);
}



void loop() {
//  repeat();
    if(Serial.available()){
      int section = Serial.parseInt();
      Serial.print(section);
      
      if(section == 0){
          staticLights();
      }
      else if(section == 1){
          ex(5, red);
      }
      else if(section == 2){
          ex(20, red);
      }
      else if(section == 3){
          ex(35, red);

      }
      else if(section == 4){
          ex(50, red);
      }

      else if(section == 5){
          door(5, green);
      }
      else if(section == 6){
          door(20, green);
      }
      else if(section == 7){
          door(35, green);

      }
      else if(section == 8){
          door(50, green);
      }
      pixels.show();
      delay(200);

  }


}
