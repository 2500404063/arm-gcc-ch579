#include "CH57x_gpio.h"
#include "CH57x_uart.h"

int main()
{
    GPIOB_ModeCfg(GPIO_Pin_0, GPIO_ModeOut_PP_20mA);
    GPIOA_ModeCfg(GPIO_Pin_8, GPIO_ModeIN_PU);
    GPIOA_ModeCfg(GPIO_Pin_9, GPIO_ModeOut_PP_5mA);

    UART1_DefInit();
    UART1_BaudRateCfg(9600);
    UART1_ByteTrigCfg(UART_1BYTE_TRIG);
    UART1_INTCfg(TRUE, RB_IER_RECV_RDY);
    NVIC_EnableIRQ(UART1_IRQn);
    GPIOB_SetBits(GPIO_Pin_0);

    while (1)
        ;
}
