/*
编写者：Kevin
网址：http://RobotControl.taobao.com
作者E-mail：1609370741@qq.com
编译环境：MDK-Lite  Version: 5.17
初版时间: 2016-1-31
测试： 本程序已在【君悦智控】的STM32Core平台上完成测试
功能：
用STM32Core平台串口2读取JY901的数据，然后通过串口1直接接到上位机，上位机上选择波特率9600。
用串口调试软件看到的是16进制数。
接线
USB-TTL工具                 STM32Core              JY901
VCC          -----           VCC        ----        VCC
TX           -----           RX1  （管脚10）   
RX           -----           TX1   (管脚9)
GND          -----           GND    ----                GND
                             RX2     （管脚3）  ----        TX
														 TX2     （管脚2） ----        RX
------------------------------------
 */
#include <string.h>
#include <stdio.h>
#include "Main.h"
#include "REG.h"
#include "stm32f10x_rcc.h"
#include "stm32f10x_gpio.h"
#include "UART1.h"
#include "UART2.h"
#include "delay.h"
#include "IOI2C.h"
#include "hw_config.h"
#include "DIO.h"
void CopeSerial1Data(unsigned char ucData)
{	
	UART2_Put_Char(ucData);
}
void CopeSerial2Data(unsigned char ucData)
{
	LED_REVERSE();
	UART1_Put_Char(ucData);
	USB_TxWrite(&ucData,1);
}
int main(void)
{  
	unsigned char str[100];
	unsigned char len,i;
		
	USB_Config();		
	SysTick_init(72,10);
	Initial_UART1(9600);//接PC的串口
	Initial_UART2(9600);//接JY-901模块的串口	
	
	LED_ON();
	while (1)
	{
		delay_ms(1000);
		len = USB_RxRead(str, sizeof(str));
		for (i=0;i<len;i++)
		{
				UART2_Put_Char(str[i]);
		}
	}
}



