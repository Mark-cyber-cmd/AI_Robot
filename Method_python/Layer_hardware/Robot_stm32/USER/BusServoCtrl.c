#include "include.h"

static bool fUart2RxComplete = FALSE;
static uint8 UartRxBuffer[26];
uint8 Uart2RxBuffer[26];


void InitUart2(void)
{
	NVIC_InitTypeDef NVIC_InitStructure;
	GPIO_InitTypeDef GPIO_InitStructure;
	USART_InitTypeDef USART_InitStructure;
	RCC_APB1PeriphClockCmd(RCC_APB1Periph_USART2, ENABLE);
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA|RCC_APB2Periph_AFIO, ENABLE);
	//USART2_TX   PA.2
	GPIO_InitStructure.GPIO_Pin = GPIO_Pin_2;
	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AF_PP;
	GPIO_Init(GPIOA, &GPIO_InitStructure);

	//USART2_RX	  PA.3
	GPIO_InitStructure.GPIO_Pin = GPIO_Pin_3;
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_IPU;
	GPIO_Init(GPIOA, &GPIO_InitStructure);


	USART_InitStructure.USART_BaudRate = 115200;
	USART_InitStructure.USART_WordLength = USART_WordLength_8b;
	USART_InitStructure.USART_StopBits = USART_StopBits_1;
	USART_InitStructure.USART_Parity = USART_Parity_No;
	USART_InitStructure.USART_HardwareFlowControl = USART_HardwareFlowControl_None;
	USART_InitStructure.USART_Mode = USART_Mode_Rx | USART_Mode_Tx;

	USART_Init(USART2, &USART_InitStructure);

	USART_ITConfig(USART2, USART_IT_RXNE, ENABLE);//开启中断

	USART_Cmd(USART2, ENABLE);                    //使能串口
	
	
	
	NVIC_InitStructure.NVIC_IRQChannel = USART2_IRQn;
	NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority=1 ;
	NVIC_InitStructure.NVIC_IRQChannelSubPriority = 2;		//
	NVIC_InitStructure.NVIC_IRQChannelCmd = ENABLE;			//IRQ通道使能
	NVIC_Init(&NVIC_InitStructure);
}


void InitBusServoCtrl(void)
{
	GPIO_InitTypeDef  GPIO_InitStructure;

	InitUart2();//串口2初始化
	
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA, ENABLE);	 //
	GPIO_InitStructure.GPIO_Pin = GPIO_Pin_0 | GPIO_Pin_1;	//
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_Out_PP;		 //推挽输出
	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
	GPIO_Init(GPIOA, &GPIO_InitStructure);

	UART_TX_ENABLE();
}

void USART2SendDataPacket(uint8 tx[],uint32 count)
{
	uint32 i;
	for(i = 0; i < count; i++)
	{
		while((USART2->SR&0X40)==0);//循环发送,直到发送完毕
		USART2->DR = tx[i];
		while((USART2->SR&0X40)==0);//循环发送,直到发送完毕
	}
}


void BusServoCtrl(uint8 id,uint8 cmd,uint16 prm1,uint16 prm2)
{
	uint32 i;
	uint8 tx[20];
	uint8 datalLen = 4;
	uint32 checkSum = 0;

	switch(cmd)
	{
	case SERVO_MOVE_TIME_WRITE:
		datalLen = SERVO_MOVE_TIME_DATA_LEN;
		break;
	}
	
	tx[0] = 0x55;
	tx[1] = 0x55;
	tx[2] = id;
	tx[3] = datalLen;
	tx[4] = cmd;
	tx[5] = prm1;
	tx[6] = prm1 >> 8;
	tx[7] = prm2;
	tx[8] = prm2 >> 8;
	for(i = 2; i <= datalLen + 1; i++)
	{
		checkSum += tx[i];
	}
	tx[datalLen + 2] = ~checkSum;
	UART_TX_ENABLE();
	USART2SendDataPacket(tx,datalLen + 3);
}

uint8* BusServoRead(uint8 id,uint8 cmd)
{
	uint32 i;
	uint8 tx[20];
	uint8 datalLen = 3;
	uint32 checkSum = 0;

	switch(cmd)
	{
		case SERVO_TEMP_READ:
			datalLen = SERVO_TEMP_READ_DATA_LEN;
			break;
		case SERVO_VIN_READ:
			datalLen = SERVO_VIN_READ_DATA_LEN;
			break;		
		case SERVO_POS_READ:
			datalLen = SERVO_POS_READ_DATA_LEN;
			break;		
	}
	tx[0] = 0x55;
	tx[1] = 0x55;
	tx[2] = id;
	tx[3] = datalLen;
	tx[4] = cmd;

	for(i = 2; i <= datalLen + 1; i++)
	{
		checkSum += tx[i];
	}
	tx[datalLen + 2] = ~checkSum;
	UART_TX_ENABLE();
	USART2SendDataPacket(tx,datalLen + 3);
	UART_RX_ENABLE();
	while(Uart2RxOK() == FALSE);
	UART_TX_ENABLE();
return UartRxBuffer;
}

void USART2_IRQHandler(void)                	//串口2中断服务程序
{
	uint8 i;
	uint8 rxBuf;
	static uint8 startCodeSum = 0;
	static bool fFrameStart = FALSE;
	static uint8 messageLength = 0;
	static uint8 messageLengthSum = 2;
	if (USART_GetFlagStatus(USART2, USART_FLAG_PE) != RESET)
    {
      USART_ReceiveData(USART2);
      USART_ClearFlag(USART2, USART_FLAG_PE);
    }
     
  if (USART_GetFlagStatus(USART2, USART_FLAG_ORE) != RESET)
    {
      USART_ReceiveData(USART2);
      USART_ClearFlag(USART2, USART_FLAG_ORE);
    }
     
	if (USART_GetFlagStatus(USART2, USART_FLAG_FE) != RESET)
    {
			  USART_ClearITPendingBit(USART2, USART_IT_RXNE);
        USART_ClearFlag(USART2, USART_FLAG_FE);
    }
		
	if(USART_GetITStatus(USART2, USART_IT_RXNE) != RESET)  //接收中断(接收到的数据必须是0x0d 0x0a结尾)
	{
		USART_ClearFlag(USART2, USART_FLAG_RXNE);
		USART_ClearITPendingBit(USART2, USART_IT_RXNE);
		rxBuf =USART_ReceiveData(USART2);//(USART1->DR);	//读取接收到的数据
		if(!fFrameStart)
		{
			if(rxBuf == 0x55)
			{

				startCodeSum++;
				Uart2RxBuffer[0] = rxBuf;
				if(startCodeSum == 2)
				{
					startCodeSum = 0;
					fFrameStart = TRUE;
					messageLength = 1;
				}
			}
			else
			{
				fFrameStart = FALSE;
				messageLength = 0;
	
				startCodeSum = 0;
			}
		}
		
		if(fFrameStart)
		{
			Uart2RxBuffer[messageLength] = rxBuf;
			if(messageLength == 3)
			{
				messageLengthSum = Uart2RxBuffer[messageLength];
				if(messageLengthSum < 2)// || messageLengthSum > 30
				{
					messageLengthSum = 2;
					fFrameStart = FALSE;
				}
			}
			messageLength++;
	
			if(messageLength == messageLengthSum + 3) 
			{
				if(fUart2RxComplete == FALSE)
				{
					fUart2RxComplete = TRUE;
				}
				
				for(i = 0;i < messageLength;i++)
				{
					UartRxBuffer[i] = Uart2RxBuffer[i];
				}
				fFrameStart = FALSE;
			}
		}
	}
}
static bool Uart2RxOK(void)
{
	if(fUart2RxComplete)
	{
		fUart2RxComplete = FALSE;
		return TRUE;
	}
	else
	{
		return FALSE;
	}
}
