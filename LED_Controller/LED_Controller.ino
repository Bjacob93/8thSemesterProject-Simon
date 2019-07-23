#include <FastLED.h>

#define num_leds 22
#define red_pin A2
#define yellow_pin A3
#define green_pin A4
#define blue_pin A5
#define red_lamp_pin 6
#define yellow_lamp_pin 9
#define green_lamp_pin 10
#define blue_lamp_pin 11


CRGB red_leds[num_leds];
CRGB yellow_leds[num_leds];
CRGB green_leds[num_leds];
CRGB blue_leds[num_leds];

int level = 1;
float difficulty = 1000;

int victoryBlinkDelay = 100;
int lossBlinkDelay = 500;
int baseDelay = 300;

void setup(){
  Serial.begin(9600);
    
  FastLED.addLeds<NEOPIXEL, red_pin>(red_leds, num_leds);
  FastLED.addLeds<NEOPIXEL, yellow_pin>(yellow_leds, num_leds);
  FastLED.addLeds<NEOPIXEL, green_pin>(green_leds, num_leds);
  FastLED.addLeds<NEOPIXEL, blue_pin>(blue_leds, num_leds);

  pinMode(red_lamp_pin, OUTPUT);
  pinMode(yellow_lamp_pin, OUTPUT);
  pinMode(green_lamp_pin, OUTPUT);
  pinMode(blue_lamp_pin, OUTPUT);
}

void loop(){    
  int incoming = 10;
  if(Serial.available()){
    incoming = Serial.read() - '0';
  }
  
  switch(incoming){
    case 1:
      blink_red();
      break;
    case 2:
      blink_yellow();
      break;
    case 3:
      blink_green();
      break;
    case 4:
      blink_blue();
      break;
    case 5:
      red_pressed();
      break;
    case 6:
      yellow_pressed();
      break;
    case 7:
      green_pressed();
      break;
    case 8:
      blue_pressed();
      break; 
    case 9:
      blink_victory();
      break;
    case 0:
      blink_loss();
      break;
    default:
      break;
  }
}

void blink_red(){
  for(int i = 0; i < num_leds; i++){
    red_leds[i] = CRGB(255, 40, 0);
  }
  FastLED.show();
  analogWrite(red_lamp_pin, 255);

  delay(difficulty);
  
  for(int i = 0; i < num_leds; i++){
    red_leds[i] = CRGB::Black;
  }
  FastLED.show();
  analogWrite(red_lamp_pin, 0);
}

void blink_yellow(){
  for(int i = 0; i < num_leds; i++){
    yellow_leds[i] = CRGB(255, 140, 0);
  }
  FastLED.show();
  analogWrite(yellow_lamp_pin, 255);
  
  delay(difficulty);
  
  for(int i = 0; i < num_leds; i++){
    yellow_leds[i] = CRGB::Black;
  }
  FastLED.show();
  analogWrite(yellow_lamp_pin, 0);
}

void blink_green(){
  for(int i = 0; i < num_leds; i++){
    green_leds[i] = CRGB::Green;
  }
  FastLED.show();
  analogWrite(green_lamp_pin, 255);
  
  delay(difficulty);
  
  for(int i = 0; i < num_leds; i++){
    green_leds[i] = CRGB::Black;
  }
  FastLED.show();
  analogWrite(green_lamp_pin, 0);
}

void blink_blue(){
  for(int i = 0; i < num_leds; i++){
    blue_leds[i] = CRGB::Blue;
  }
  FastLED.show();
  analogWrite(blue_lamp_pin, 255);
  
  delay(difficulty);
  
  for(int i = 0; i < num_leds; i++){
    blue_leds[i] = CRGB::Black;
  }
  FastLED.show();
  analogWrite(blue_lamp_pin, 0);
}

void red_pressed(){
  for(int i = 0; i < num_leds; i++){
    red_leds[i] = CRGB(255, 40, 0);
  }
  FastLED.show();
  analogWrite(red_lamp_pin, 255);

  delay(baseDelay);
  
  for(int i = 0; i < num_leds; i++){
    red_leds[i] = CRGB::Black;
  }
  FastLED.show();
  analogWrite(red_lamp_pin, 0);
}

void yellow_pressed(){
  for(int i = 0; i < num_leds; i++){
    yellow_leds[i] = CRGB(255, 140, 0);
  }
  FastLED.show();
  analogWrite(yellow_lamp_pin, 255);

  delay(baseDelay);
  
  for(int i = 0; i < num_leds; i++){
    yellow_leds[i] = CRGB::Black;
  }
  FastLED.show();
  analogWrite(yellow_lamp_pin, 0);
}

void green_pressed(){
  for(int i = 0; i < num_leds; i++){
    green_leds[i] = CRGB::Green;
  }
  FastLED.show();
  analogWrite(green_lamp_pin, 255);

  delay(baseDelay);
  
  for(int i = 0; i < num_leds; i++){
    green_leds[i] = CRGB::Black;
  }
  FastLED.show();
  analogWrite(green_lamp_pin, 0);
}

void blue_pressed(){
  for(int i = 0; i < num_leds; i++){
    blue_leds[i] = CRGB::Blue;
  }
  FastLED.show();
  analogWrite(blue_lamp_pin, 255);

  delay(baseDelay);
  
  for(int i = 0; i < num_leds; i++){
    blue_leds[i] = CRGB::Black;
  }
  FastLED.show();
  analogWrite(blue_lamp_pin, 0);
}

void blink_loss(){
  level = 1;
  difficulty = 1000;
  
  for(int i = 0; i < 3; i++){
    for(int j = 0; j < num_leds; j++){
    red_leds[j] = CRGB(255, 40, 0);
    yellow_leds[j] = CRGB(255, 140, 0);
    green_leds[j] = CRGB::Green;
    blue_leds[j] = CRGB::Blue;
    }
    FastLED.show();
    analogWrite(red_lamp_pin, 255);
    analogWrite(yellow_lamp_pin, 255);
    analogWrite(green_lamp_pin, 255);
    analogWrite(blue_lamp_pin, 255);
    
    delay(lossBlinkDelay);
    
    for(int j = 0; j < num_leds; j++){
    red_leds[j] = CRGB::Black;
    yellow_leds[j] = CRGB::Black;
    green_leds[j] = CRGB::Black;
    blue_leds[j] = CRGB::Black;
    }
    FastLED.show();
    analogWrite(red_lamp_pin, 0);
    analogWrite(yellow_lamp_pin, 0);
    analogWrite(green_lamp_pin, 0);
    analogWrite(blue_lamp_pin, 0);
    
    delay(lossBlinkDelay);
  }
}

void blink_victory(){
  
  if(level < 11) difficulty -= 70;
  else if(level < 16) difficulty -= 40;
  if(difficulty < 100) difficulty = 100;
  level++;
  
  for(int i = 0; i < 10; i++){
    for(int j = 0; j < num_leds; j++){
    red_leds[j] = CRGB(255, 40, 0);
    yellow_leds[j] = CRGB(255, 140, 0);
    green_leds[j] = CRGB::Green;
    blue_leds[j] = CRGB::Blue;
    }
    FastLED.show();
    analogWrite(red_lamp_pin, 255);
    analogWrite(yellow_lamp_pin, 255);
    analogWrite(green_lamp_pin, 255);
    analogWrite(blue_lamp_pin, 255);
    
    delay(victoryBlinkDelay);
    
    for(int j = 0; j < num_leds; j++){
    red_leds[j] = CRGB::Black;
    yellow_leds[j] = CRGB::Black;
    green_leds[j] = CRGB::Black;
    blue_leds[j] = CRGB::Black;
    }
    FastLED.show();
    analogWrite(red_lamp_pin, 0);
    analogWrite(yellow_lamp_pin, 0);
    analogWrite(green_lamp_pin, 0);
    analogWrite(blue_lamp_pin, 0);
    
    delay(victoryBlinkDelay);
  }
}
