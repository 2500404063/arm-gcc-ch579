#include "CH57x_uart.h"

void TMR0_IRQHandler(void) {}  // 0:  TMR0
void GPIO_IRQHandler(void) {}  // 1:  GPIO
void SLAVE_IRQHandler(void) {} // 2:  SLAVE
void SPI0_IRQHandler(void) {}  // 3:  SPI0
void BB_IRQHandler(void) {}    // 4:  BB
void LLE_IRQHandler(void) {}   // 5:  LLE
void USB_IRQHandler(void) {}   // 6:  USB
void ETH_IRQHandler(void) {}   // 7:  ETH
void TMR1_IRQHandler(void) {}  // 8:  TMR1
void TMR2_IRQHandler(void) {}  // 9:  TMR2
void UART0_IRQHandler(void) {} // 10:  UART0
void UART1_IRQHandler(void)
{
    char buf = UART1_RecvByte();
    UART1_SendByte(buf);
} // 11:  UART1
void RTC_IRQHandler(void) {}   // 12:  RTC
void ADC_IRQHandler(void) {}   // 13:  ADC
void SPI1_IRQHandler(void) {}  // 14:  SPI1
void LED_IRQHandler(void) {}   // 15:  LED
void TMR3_IRQHandler(void) {}  // 16:  TMR3
void UART2_IRQHandler(void) {} // 17:  UART2
void UART3_IRQHandler(void) {} // 18:  UART3
void WDT_IRQHandler(void) {}   // 19:  WDT