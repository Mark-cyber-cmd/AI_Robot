/*
编写者：Kevin
网址：http://RobotControl.taobao.com
作者E-mail：1609370741@qq.com
编译环境：MDK-Lite  Version: 5.17
初版时间: 2016-1-31
测试： 本程序已在【君悦智控】的STM32Core平台上完成测试
功能：
用STM32Core平台串口2读取JY901的数据，然后通过串口1打印到串口助手,串口助手波特率要选为9600。
JY-901的波特率要修改为9600.
注意：示例程序输出的是ASCLL码，用16进制（HEX）显示是不能看到准确数据的。
硬件接线：
USB-TTL工具                 STM32Core               JY901
VCC          -----           VCC        ----         VCC
TX           -----           RX1（管脚10）     
RX           -----           TX1（管脚9）
GND          -----           GND        ----          GND
                             RX2 （管脚3）       ----  TX
							 TX2  （管脚2）      ----  RX
------------------------------------
 */
#include <string.h>
#include <stdio.h>
#include "Main.h"
#include "stm32f10x_rcc.h"
#include "stm32f10x_gpio.h"
#include "UART1.h"
#include "UART2.h"
#include "delay.h"
#include "IOI2C.h"
#include "hw_config.h"
#include "JY901.h"
#include "DIO.h"

struct STime		stcTime;
struct SAcc 		stcAcc;
struct SGyro 		stcGyro;
struct SAngle 	stcAngle;
struct SMag 		stcMag;
struct SDStatus stcDStatus;
struct SPress 	stcPress;
struct SLonLat 	stcLonLat;
struct SGPSV 		stcGPSV;
struct SQ       stcQ;

//CopeSerialData为串口2中断调用函数，串口每收到一个数据，调用一次这个函数。
void CopeSerial2Data(unsigned char ucData)
{
	static unsigned char ucRxBuffer[250];
	static unsigned char ucRxCnt = 0;	
	
	LED_REVERSE();					//接收到数据，LED灯闪烁一下
	USB_TxWrite(&ucData,1);			//向USB-HID端口转发收到的串口数据，可直接用接上位机看到模块输出的数据。
	ucRxBuffer[ucRxCnt++]=ucData;	//将收到的数据存入缓冲区中
	if (ucRxBuffer[0]!=0x55) //数据头不对，则重新开始寻找0x55数据头
	{
		ucRxCnt=0;
		return;
	}
	if (ucRxCnt<11) {return;}//数据不满11个，则返回
	else
	{
		switch(ucRxBuffer[1])//判断数据是哪种数据，然后将其拷贝到对应的结构体中，有些数据包需要通过上位机打开对应的输出后，才能接收到这个数据包的数据
		{
			case 0x50:	memcpy(&stcTime,&ucRxBuffer[2],8);break;//memcpy为编译器自带的内存拷贝函数，需引用"string.h"，将接收缓冲区的字符拷贝到数据结构体里面，从而实现数据的解析。
			case 0x51:	memcpy(&stcAcc,&ucRxBuffer[2],8);break;
			case 0x52:	memcpy(&stcGyro,&ucRxBuffer[2],8);break;
			case 0x53:	memcpy(&stcAngle,&ucRxBuffer[2],8);break;
			case 0x54:	memcpy(&stcMag,&ucRxBuffer[2],8);break;
			case 0x55:	memcpy(&stcDStatus,&ucRxBuffer[2],8);break;
			case 0x56:	memcpy(&stcPress,&ucRxBuffer[2],8);break;
			case 0x57:	memcpy(&stcLonLat,&ucRxBuffer[2],8);break;
			case 0x58:	memcpy(&stcGPSV,&ucRxBuffer[2],8);break;
			case 0x59:	memcpy(&stcQ,&ucRxBuffer[2],8);break;
		}
		ucRxCnt=0;//清空缓存区
	}
}

void CopeSerial1Data(unsigned char ucData)
{	
	UART2_Put_Char(ucData);//转发串口1收到的数据给串口2（JY模块）
}


int main(void)
{  
	char str[100];
	unsigned char len,i;
		
	USB_Config();		//配置USB-HID
	SysTick_init(72,10);//设置时钟频率
	Initial_UART1(9600);//接PC的串口
	Initial_UART2(9600);//接JY-901模块的串口	
	
	LED_ON();
	delay_ms(1000);//等等JY-91初始化完成
	while(1)
	{			
			delay_ms(500);
		//输出时间
		sprintf(str,"Time:20%d-%d-%d %d:%d:%.3f\r\n",stcTime.ucYear,stcTime.ucMonth,stcTime.ucDay,stcTime.ucHour,stcTime.ucMinute,(float)stcTime.ucSecond+(float)stcTime.usMiliSecond/1000);
			UART1_Put_String(str);		
			delay_ms(10);
		//输出加速度
		sprintf(str,"Acc:%.3f %.3f %.3f\r\n",(float)stcAcc.a[0]/32768*16,(float)stcAcc.a[1]/32768*16,(float)stcAcc.a[2]/32768*16);
			UART1_Put_String(str);
			delay_ms(10);
		//输出角速度
		sprintf(str,"Gyro:%.3f %.3f %.3f\r\n",(float)stcGyro.w[0]/32768*2000,(float)stcGyro.w[1]/32768*2000,(float)stcGyro.w[2]/32768*2000);
			UART1_Put_String(str);
			delay_ms(10);
		//输出角度
		sprintf(str,"Angle:%.3f %.3f %.3f\r\n",(float)stcAngle.Angle[0]/32768*180,(float)stcAngle.Angle[1]/32768*180,(float)stcAngle.Angle[2]/32768*180);
			UART1_Put_String(str);
			delay_ms(10);
		//输出磁场
		sprintf(str,"Mag:%d %d %d\r\n",stcMag.h[0],stcMag.h[1],stcMag.h[2]);
			UART1_Put_String(str);		
			delay_ms(10);
		//输出气压、高度
		sprintf(str,"Pressure:%ld Height%.2f\r\n",stcPress.lPressure,(float)stcPress.lAltitude/100);
			UART1_Put_String(str); 
			delay_ms(10);
		//输出端口状态
		sprintf(str,"DStatus:%d %d %d %d\r\n",stcDStatus.sDStatus[0],stcDStatus.sDStatus[1],stcDStatus.sDStatus[2],stcDStatus.sDStatus[3]);
			UART1_Put_String(str);
			delay_ms(10);
		//输出经纬度
		sprintf(str,"Longitude:%ldDeg%.5fm Lattitude:%ldDeg%.5fm\r\n",stcLonLat.lLon/10000000,(double)(stcLonLat.lLon % 10000000)/1e5,stcLonLat.lLat/10000000,(double)(stcLonLat.lLat % 10000000)/1e5);
			UART1_Put_String(str);
			delay_ms(10);
		//输出地速
		sprintf(str,"GPSHeight:%.1fm GPSYaw:%.1fDeg GPSV:%.3fkm/h\r\n",(float)stcGPSV.sGPSHeight/10,(float)stcGPSV.sGPSYaw/10,(float)stcGPSV.lGPSVelocity/1000);
			UART1_Put_String(str);
			delay_ms(10);
		//输出四元素
		sprintf(str,"Four elements:%.5f %.5f %.5f %.5f\r\n\r\n",(float)stcQ.q[0]/32768,(float)stcQ.q[1]/32768,(float)stcQ.q[2]/32768,(float)stcQ.q[3]/32768);
			UART1_Put_String(str);
		    delay_ms(10);//等待传输完成
	}//主循环
}



