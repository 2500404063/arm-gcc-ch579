import os
import sys


def build():
    command = 'arm-none-eabi-gcc'
    includePath = [
        "./../inc",
        "./../cmsis/inc",
        "./../device/inc",
        "./../driver/inc",
    ]
    sourcePath = [
        "./../src/*.c",
        "./../driver/src/*.c",
        "./../device/src/*.c"
    ]
    args = [
        '-c',
        # '--specs=nosys.specs',
        '-lnosys',
        '--specs=nano.specs',
        "-mthumb",
        "-mcpu=cortex-m0",
        "-mfloat-abi=soft"
    ]
    # Create Include flags
    flag_inc = ''
    for i in range(len(includePath)):
        flag_inc += f'-I{includePath[i]}'
        if i < len(includePath)-1:
            flag_inc += ' '

    flag_arg = ''
    for i in range(len(args)):
        flag_arg += args[i]
        if i < len(args)-1:
            flag_arg += ' '

    flag_src = ''
    for i in range(len(sourcePath)):
        flag_src += f'{sourcePath[i]}'
        if i < len(sourcePath)-1:
            flag_src += ' '

    cmd_lind = f'{command} {flag_src} {flag_arg} {flag_inc}'
    print('Start to compile')
    os.system(cmd_lind)


def link():
    print('Start to link')
    command = 'arm-none-eabi-gcc'
    ld = './../device/src/gcc_ch579.ld'
    os.system(f'{command} *.o -o output.bin -lnosys --specs=nano.specs -mcpu=cortex-m0 -march=armv6-m -T {ld}')
    os.system(f'{command} *.o -o output.elf -lnosys --specs=nano.specs -mcpu=cortex-m0 -march=armv6-m -T {ld}')
    command = 'arm-none-eabi-objcopy'
    os.system(f'{command} output.bin -I elf32-littlearm -O binary')


def clean():
    files = os.listdir('./')
    for f in files:
        os.remove(files)


todo = sys.argv[1]
print(todo)
if todo == 'build':
    build()
elif todo == 'link':
    link()
