#include <ESP8266WiFi.h>

#ifndef STASSID
#define STASSID "AI_Robot"
#define STAPSK  "88888888"
#endif

const int ledPin =  LED_BUILTIN;


int ledState = LOW;             // ledState used to set the LED
unsigned long previousMillis = 0;        // will store last time LED was updated
const long interval = 1000;           // interval at which to blink (milliseconds)

const char* ssid     = STASSID;
const char* password = STAPSK;

const char* host = "192.168.43.186";
const uint16_t port = 8000;

char  id[11];
char  RXbuff[11];
char  RXover = 0;
char  RXcount = 0;
char  head_flag = 0;
char  TCP_RXbuff[11];
char  TCP_RXover = 0;
char  TCP_RXcount = 0;
char  TCP_head_flag = 0;
int incomingByte = 0;                 // for incoming serial data
unsigned int i = 0 ; 


// 创建WIFI对象
WiFiClient client;


void setup() 
{
  pinMode(ledPin, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH);  
  
  Serial.begin(115200);
  
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) 
  {
      delay(50);
  }
  LED_Blink_2();
  Serial.print("\r\nWiFi connected\r\n");
  
  while (!client.connect(host, port)) 
  {
      delay(50);
  }
  LED_Blink_3();
  Serial.print("\r\nserver connected\r\n");

  id[0] = 0x55;
  id[1] = 0x01;
  id[2] = 0x03; //命名位
  id[3] = 0x00;
  id[4] = 0x00;
  id[5] = 0x00;
  id[6] = 0x00;
  id[7] = 0x00;
  id[8] = 0x00;
  id[9] = 0x00;
  id[10] = 0x00;
  client.write(id,11);
}

void loop() 
{    
      //若没有找到TCP服务器则一直寻找
RESET:
      while(1)
      {
          USART_pro();
          GYRO_pro(RXbuff); 
          TCP_pro();
          LED_Blink_always();
      }
}

void GYRO_pro(char* RXbuff)
{
    if (RXover == 1 && client.connected())
    {
        client.write(RXbuff,11);
        RXover = 0;  
    }
}

void USART_pro(void)
{
    if (Serial.available() > 0)
    {
        incomingByte = Serial.read();
        
        if (incomingByte == 0x55)
        {
            RXcount = 0;
            head_flag = 1;        
        }
    
        if (head_flag == 1)
        {
            if (RXcount < 11)
            {
                RXbuff[RXcount] = incomingByte;
                RXcount++;
            }

            if (RXcount == 11) 
            {
                RXover = 1;
                RXcount = 0; 
            } 
        }
    }  
}

void TCP_pro(void)
{
    if (client.connected())
    {
        if (client.available()) 
        {
            char incomingByte = static_cast<char>(client.read());

            if (incomingByte == 0xFF)
            {
                TCP_RXcount = 0;
                TCP_head_flag = 1;        
            }
        
            if (TCP_head_flag == 1)
            {
                if (TCP_RXcount <= 5)
                {
                    TCP_RXbuff[TCP_RXcount] = incomingByte;
                    TCP_RXcount++;
                }
    
                if (TCP_RXcount == 5)
                {
                    TCP_RXover = 1;
                    TCP_RXcount = 0; 
                    TCP_head_flag = 0; 
                } 
            }
        }

        if(TCP_RXover == 1)
        {
            Serial.write(TCP_RXbuff,5);  
            TCP_RXover = 0;
        }
    }
    else
    {
        while (!client.connect(host, port)) 
        {
            delay(50);
        }
        client.write(id,11);     
    }    
}

void LED_Blink_always()
{
  unsigned long currentMillis = millis();

  if (currentMillis - previousMillis >= interval) {

    previousMillis = currentMillis;

    if (ledState == LOW) {
      ledState = HIGH;
    } else {
      ledState = LOW;
    }

    digitalWrite(ledPin, ledState);
  }
}

void LED_Blink_2()
{
  digitalWrite(LED_BUILTIN, LOW);   // turn the LED on (HIGH is the voltage level)
  delay(500);                       // wait for a second
  digitalWrite(LED_BUILTIN, HIGH);    // turn the LED off by making the voltage LOW
  delay(500);                       // wait for a second  
    digitalWrite(LED_BUILTIN, LOW);   // turn the LED on (HIGH is the voltage level)
  delay(500);                       // wait for a second
  digitalWrite(LED_BUILTIN, HIGH);    // turn the LED off by making the voltage LOW
  delay(500);                       // wait for a second  
}


void LED_Blink_3()
{
  digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
  delay(500);                       // wait for a second
  digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW
  delay(500);                       // wait for a second  
  digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
  delay(500);                       // wait for a second
  digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW
  delay(500);                       // wait for a second 
    digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
  delay(500);                       // wait for a second
  digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW
  delay(500);  
}
