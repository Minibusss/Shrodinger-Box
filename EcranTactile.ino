#include <XPT2046_Touchscreen.h>
#include <Adafruit_ILI9341.h>      // Bibliothèque pour l'écran TFT ILI9341
#include <SPI.h>

// Pins pour l'écran TFT ILI9341
#define CS_PIN    10
#define RST_PIN   8
#define DC_PIN    9

Adafruit_ILI9341 tft = Adafruit_ILI9341(CS_PIN, DC_PIN, RST_PIN);

//XPT2046_Touchscreen ts(CS_PIN);
#define TIRQ_PIN  2
XPT2046_Touchscreen ts(CS_PIN);  // Param 2 - NULL - No interrupts
//XPT2046_Touchscreen ts(CS_PIN, 255);  // Param 2 - 255 - No interrupts
//XPT2046_Touchscreen ts(CS_PIN, TIRQ_PIN);  // Param 2 - Touch IRQ Pin - interrupt enabled polling

// Définition des couleurs et des dimensions du bouton
#define BUTTON_COLOR ILI9341_BLUE
#define BUTTON_PRESS_COLOR ILI9341_RED
#define BUTTON_X 50
#define BUTTON_Y 100
#define BUTTON_WIDTH 200
#define BUTTON_HEIGHT 50
#define BUTTON_TEXT "LANCER LE JEU"


void setup() {
  Serial.begin(38400);


  //deselect all SPI devices
  pinMode(8, OUTPUT);
  pinMode(7, OUTPUT);
  digitalWrite(8, HIGH);
  digitalWrite(7, HIGH);

  // Initialisation de l'écran TFT
  tft.begin();  // Ajuste la rotation de l'écran (selon votre configuration)
  tft.setRotation(3);

  
  ts.begin();
  ts.setRotation(1);

  drawButton(BUTTON_COLOR);



}

void loop() {
  digitalWrite(7, LOW);
  if (ts.touched()) {
    digitalWrite(7, HIGH);
    TS_Point p = ts.getPoint();
    Serial.print("Pressure = ");
    Serial.print(p.z);
    Serial.print(", x = ");
    Serial.print(p.x);
    Serial.print(", y = ");
    Serial.print(p.y);
    delay(30);
    Serial.println();

    p.x = map(p.x, 0, 4095, 0, tft.width());
    p.y = map(p.y, 0, 4095, 0, tft.height());
    

    // Vérifier si le point touché est dans les limites du bouton
    if (p.x > BUTTON_X && p.x < BUTTON_X + BUTTON_WIDTH &&
        p.y > BUTTON_Y && p.y < BUTTON_Y + BUTTON_HEIGHT) {
          Serial.println("Boutton OK");
          drawButton(BUTTON_PRESS_COLOR);
        }
         else{
          drawButton(BUTTON_COLOR);
          }
    }
    digitalWrite(7, LOW);
  }
  



void drawButton(unsigned color) {
  
  // Dessiner le bouton
  tft.fillRect(BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT, color);
  tft.setTextColor(ILI9341_BLACK);
  tft.setTextSize(2);
  tft.setCursor(BUTTON_X + 20, BUTTON_Y + 15);  // Position du texte dans le bouton
  tft.println(BUTTON_TEXT);}
