#include <ESP8266WiFi.h>
#include <string.h>
#define MAX_SRV_CLIENTS 2          //最大同时连接数，即你想要接入的设备数量，8266tcpserver只能接入五个，哎
#define MAX_GYRO_DATA_LEN 11       //最长陀螺仪数据长度
#define MAX_SERVO_DATA_LEN  100    //最长舵机控制命令


const char *ssid = "AI_Robot";     //这里是我的wifi，你使用时修改为你要连接的wifi ssid
const char *password = "88888888"; //你要连接的wifi密码


static char client_index[6];
static char client_ready_flag = 0;
static char client_status[6];
static char client_data[6][MAX_GYRO_DATA_LEN];
static char client_data_RXcount = 0;
static char client_data_RXready = 0;
static char client_data_head_flag = 0;


static short gyro_data[6][MAX_GYRO_DATA_LEN];
static char  servo_data[MAX_SERVO_DATA_LEN];
 
WiFiServer server(8000);           //你要的端口号，随意修改，范围0-65535
WiFiClient serverClients[6];
 
void setup()
{
    Serial.begin(115200);
    pinMode(2, OUTPUT);
    digitalWrite(2, 1);
    WiFi.begin(ssid, password);
 
    while (WiFi.status() != WL_CONNECTED)
    {
        delay(50);
    }

    Serial.print("\r\nWIFI CONNECTED!\r\n");
    Serial.print("Local IP:");
    Serial.println(WiFi.localIP());
    server.begin();
    server.setNoDelay(true);  //加上后才正常些    

    while(client_ready_flag == 0)
    {
        tcp_calibrate();
        tcp_handshaking();
        tcp_recieve();
        blink_pro();
        delay(50);      
    }

    Serial.print("client index:");
    Serial.print(client_index[0],HEX);
    Serial.print(" ");
    Serial.print(client_index[1],HEX);
    Serial.print(" ");
    Serial.print(client_index[2],HEX);
    Serial.print(" ");
    Serial.print(client_index[3],HEX);
    Serial.print(" ");
    Serial.print(client_index[4],HEX);
    Serial.print(" ");
    Serial.print(client_index[5],HEX);
    Serial.print(" ");
    Serial.print(client_index[6],HEX);
}
 
void loop()
{
    unsigned char i=0,j=0;
    
    tcp_handshaking(); 
    tcp_recieve();
    tcp_calibrate();
    tcp_send();
   

    gyro_pro();
    servo_pro();
    

    blink_pro();
    client_data_clean();
}

void tcp_calibrate(void)
{
    static long   previousMillis;
    uint8_t i=0,j=0,temp=0,assume=0;


    //若发生断链则提示
    if (millis() - previousMillis > 500)  //大于1s未出现新数据
    {
        previousMillis = millis();
        
        if (client_ready_flag == 1)
        {
            for (i = 0; i < MAX_SRV_CLIENTS; i++)
            {
                if (client_status[i] == 0 && client_index[i] != 0x05 && client_index[i] != 0x00 )
                {
                    serverClients[i].stop();
                    Serial.print("\r\nClient ID:");
                    Serial.print(client_index[i],HEX);
                    Serial.print(" IS OFFLINE!\r\n");
                    Serial.print("Please check clients.....\r\n");
                    client_index[i] = 0;
                    client_ready_flag = 0;       
                }
            }

            for (i = 0; i < 6; i++)
            {
                 client_status[i] = 0; 
            }
        } 
    }
       
    //ID校准代码
    if ( client_ready_flag == 0)
    {
        for (i = 0; i < MAX_SRV_CLIENTS; i++)
        {
            if(client_data[i][0] == 0x55 && client_data[i][1] == 0x01 && client_index[i] == 0 )
            {
                client_index[i] = client_data[i][2];  
                Serial.print("CLIENT ID:");
                Serial.print(client_index[i],HEX);
                Serial.print(" IS ONLINE\r\n");
            }
        }

        for (i = 0; i < MAX_SRV_CLIENTS; i++)
        {
            if(serverClients[i].connected() && client_index[i] != 0)
            {  
                temp = temp | (1 << i);  
            }
            assume = assume | (1 << i);
        }

        if (temp == assume)
        {
            client_ready_flag = 1;  
            Serial.print("ALL CLIENTS ARE READY!\r\n");   
        }
    }

  
}

void tcp_handshaking(void)
{
    uint8_t i=0,j=0;
    
    //握手部分
    for (i = 0; i < MAX_SRV_CLIENTS; i++)
    {
        if (!serverClients[i].connected())
        {
            serverClients[i].stop();//未联接,就释放
            if (server.hasClient())  serverClients[i] = server.available();//分配新的
        }
    }
    //超出链接上限则杀死进程
    WiFiClient serverClient = server.available();
    serverClient.stop(); 
}

void tcp_send(void)
{
    uint8_t i=0,j=0;
    //数据发送
    if (Serial.available())
    {
        size_t len = Serial.available();
        uint8_t sbuf[len];
        Serial.readBytes(sbuf, len);
        //push UART data to all connected telnet clients
        for (i = 0; i < MAX_SRV_CLIENTS; i++)
        {
            if (serverClients[i] && serverClients[i].connected())
            {
                serverClients[i].write(sbuf, len);  //向所有客户端发送数据
                delay(1);
            }
        }
    } 

    //陀螺仪数据转送主机
    if (client_data_RXready == 1 && client_ready_flag == 1)
    {
        for (i = 0; i < MAX_SRV_CLIENTS; i++)
        {
            if (serverClients[i] && serverClients[i].connected() && client_index[i] == 0x05)
            {
                serverClients[i].write(client_data[1],11);  //向控制主机发送数据
                serverClients[i].write(client_data[2],11);
                serverClients[i].write(client_data[3],11);
                serverClients[i].write(client_data[4],11);
            }
        }     
    }

    //主机数据转送陀螺仪
    if (client_data_RXready == 1 && client_ready_flag == 1 && client_data[5][0] != 0x00)
    {
        for (i = 0; i < MAX_SRV_CLIENTS; i++)
        {
            if (serverClients[i] && serverClients[i].connected() && (client_index[i] == 0x01 | client_index[i] == 0x02 | client_index[i] == 0x03 | client_index[i] == 0x04))
            {
                    for (j = 1;j < 6;j++)
                    {
                        serverClients[i].write(client_data[5][j]); //向陀螺仪门发送指令  
                    } 
            }
        }   
    }
}


void tcp_recieve(void)
{
    uint8_t i=0,j=0;
    int incomingByte = 0; 
    //数据读取
    for (i = 0; i < MAX_SRV_CLIENTS; i++)
    {
        if (serverClients[i].connected() && serverClients[i].available())
        {
            client_status[i] = 1;  
                          
            while (serverClients[i].available()) 
            {
                incomingByte = serverClients[i].read();
                
                if (incomingByte == 0x55)
                {
                    client_data_RXcount = 0;
                    client_data_head_flag = 1;        
                }
            
                if (client_data_head_flag == 1)
                {
                    if (client_data_RXcount < 11)
                    {
                        if (client_ready_flag == 0)  client_data[i][j] = incomingByte;

                        
                        if (client_ready_flag == 1)  client_data[client_index[i]][j] = incomingByte;
                        client_data_RXcount++;
                    }
        
                    if (client_data_RXcount == 11)
                    {
                        client_data_RXcount = 0; 
                        client_data_RXready = 1;
                        client_data_head_flag = 0; 
                        break;
                    } 
                }
                j++;
            }
            j = 0;
        }
    }  
}

void gyro_pro(void)
{
    uint8_t i=0,j=0;
    if ( client_data_RXready ==1 && client_ready_flag == 1)
    {
        for (i = 1; i < MAX_SRV_CLIENTS; i++)
        {
            switch (client_data[i][1])
            {
                case 0x53:  gyro_data[i][0] = ((short)((short)client_data[i][3]<<8 | client_data[i][2]))/32768.0*180;
                            gyro_data[i][1] = ((short)((short)client_data[i][5]<<8 | client_data[i][4]))/32768.0*180;
                            gyro_data[i][2] = ((short)((short)client_data[i][7]<<8 | client_data[i][6]))/32768.0*180;
                            break;
            }         
        }
    }    
}

void servo_pro(void)
{
    uint8_t i=0,j=0;
    if (client_data_RXready == 1 && client_ready_flag == 1)
    {
        servo_data[0] = 0x55;
        servo_data[1] = 0x55;
        servo_data[2] = 6*3+5;
        servo_data[3] = 0x03;
        servo_data[4] = 0x06;   //控制舵机的个数
        servo_data[5] = 0x2C;   //时间低八位
        servo_data[6] = 0x01;   //时间高八位
        
        servo_data[7] = 0x01;   //舵机ID：1号
        servo_data[8] = 0xF4;   //未知 位置居中
        servo_data[9] = 0x01;
        
        servo_data[10] = 0x02;   //舵机ID：2号
        servo_data[11] = (char)( 500 + (int)(gyro_data[2][0]/90.0*500));        //位置依照ID:1陀螺仪翻滚角决定(低八位)
        servo_data[12] = (char)((500 + (int)(gyro_data[2][0]/90.0*500))>>8);   //位置依照ID:1陀螺仪翻滚角决定(高八位)
        
        servo_data[13] = 0x03;  //舵机ID：3号
        servo_data[14] = (char)( 500 + (int)(gyro_data[3][0]/90.0*500));        //位置依照ID:3陀螺仪翻滚角决定(低八位)
        servo_data[15] = (char)((500 + (int)(gyro_data[3][0]/90.0*500))>>8);   //位置依照ID:3陀螺仪翻滚角决定(高八位)
        
        servo_data[16] = 0x04;  //舵机ID：4号
        servo_data[17] = 0xF4;
        servo_data[18] = 0x01; 

        servo_data[19] = 0x05;  //舵机ID：5号
        servo_data[20] = (char)(500 -  (int)(gyro_data[2][0]/90.0*500));         //位置依照ID:1陀螺仪翻滚角决定(低八位)
        servo_data[21] = (char)((500 - (int)(gyro_data[2][0]/90.0*500))>>8);    //位置依照ID:1陀螺仪翻滚角决定(高八位)

        servo_data[22] = 0x06;  //舵机ID：6号
        servo_data[23] = (char)( 500 - (int)(gyro_data[3][0]/90.0*500));        //位置依照ID:3陀螺仪翻滚角决定(低八位)
        servo_data[24] = (char)((500 - (int)(gyro_data[3][0]/90.0*500))>>8);   //位置依照ID:3陀螺仪翻滚角决定(高八位)   
         
        Serial.write(servo_data,25);
        delay(10);
        client_data_RXready == 0;
    }
}


void client_data_clean(void)
{
    unsigned char i = 0,j = 0;  
    for (i = 0; i < 6; i++)
    {
        for (j = 0; j < 11; j++)
        {
            client_data[i][j] = 0;     
        }     
    }  
}

void blink_pro(void)
{
    static long previousMillis = 0;
    static int currstate = 0;


    uint8_t i=0,j=0;
    if (millis() - previousMillis > 200)  //200ms
    {
        previousMillis = millis();
        currstate = 1 - currstate;
        digitalWrite(2, currstate);

        /*
        if (client_ready_flag == 1)
        {
            for (i=0;i<6;i++)
            {
                for (j=0;j<11;j++)
                {
                    Serial.print(client_data[i][j],HEX); 
                    Serial.print(" ");
                }
                Serial.print("\r\n"); 
            }
        }
        */
    }

    if (client_ready_flag == 1)
    {
        digitalWrite(2, 0);                           //就一直长亮  
    }
  
}
