import hashlib
import json
import os
import re
import sys
import time

# Configuration
buildDir = './build'
compiler = 'arm-none-eabi-gcc'
linker = 'arm-none-eabi-gcc'
objcopy = 'arm-none-eabi-objcopy'
outputFileName = 'output.bin'
sourceSuffix = ['.c', '.cpp']
includeDirs = [
    "./inc",
    "./cmsis/inc",
    "./device/inc",
    "./driver/inc"
]
sourceDirs = [
    "./src",
    "./driver/src",
    "./device/src"
]
compileArgs = [
    # '--specs=nosys.specs',
    '--specs=nano.specs',
    "-mthumb",
    "-mcpu=cortex-m0",
    '-march=armv6-m',
    "-mfloat-abi=soft"
]
linkArgs = [
    '--specs=nano.specs',
    '-mcpu=cortex-m0',
    '-march=armv6-m',
    '-T ./device/src/gcc_ch579.ld'
]
objcopyArgs = [
    '-I elf32-littlearm',
    '-O binary'
]

# Building System Core Code

sources_hashes = {}


def Preprocess():
    if not os.path.exists(buildDir):
        os.mkdir(buildDir)
    if not os.path.exists('built.json'):
        WriteChanging()


def ReadChanging():
    global sources_hashes
    with open('built.json') as f:
        sources_hashes = json.load(f)


def WriteChanging():
    with open('built.json', 'w+') as f:
        json.dump(sources_hashes, f)


def fileFilter(files: list, suffix: list):
    filteredFiles = list()
    for f in files:
        for i in suffix:
            if f[-len(i):] == i:
                filteredFiles.append(f)
                break
    return filteredFiles


def compile():
    print(f'Start: Compile at {time.strftime("%H:%M:%S",time.localtime())}')
    hasChanged = False
    flag_arg = ' '.join(compileArgs)
    inc_dirs = ' '.join(list(map(lambda x: '-I'+x, includeDirs)))
    for dir in sourceDirs:
        # Filter files, remove not source files.
        files = os.listdir(dir)
        filteredFiles = fileFilter(files, sourceSuffix)
        for s in filteredFiles:
            input_file = os.path.join(dir, s)
            # Compute MD5 and update
            with open(input_file, 'rb') as f:
                featureEncoder = hashlib.md5()
                featureEncoder.update(f.read())
                cur_feature = featureEncoder.hexdigest()
            if input_file not in sources_hashes:
                sources_hashes[input_file] = cur_feature
                hasChanged = True
            elif sources_hashes[input_file] == cur_feature:
                continue
            else:
                sources_hashes[input_file] = cur_feature
                hasChanged = True
            # Start to compile
            print(f'Compile: {input_file}')
            output_file = os.path.join(
                buildDir, re.match('.*\.', s)[0][:-1] + '.o')
            os.system(
                f'{compiler} -c {input_file} {flag_arg} {inc_dirs} -o {output_file}'
            )
    if hasChanged:
        WriteChanging()
    print(f'End: Compile at {time.strftime("%H:%M:%S",time.localtime())}')


def link():
    print(f'Start: Link at {time.strftime("%H:%M:%S",time.localtime())}')
    flag_arg = ' '.join(linkArgs)
    files = os.path.join(buildDir, '*.o')
    outputFile = os.path.join(buildDir, outputFileName)
    os.system(f'{linker} {files} {flag_arg} -o {outputFile}')
    print(f'End: Link at {time.strftime("%H:%M:%S",time.localtime())}')


def copy():
    print(f'Start: Copy at {time.strftime("%H:%M:%S",time.localtime())}')
    flag_arg = ' '.join(objcopyArgs)
    file = os.path.join(buildDir, outputFileName)
    os.system(f'{objcopy} {file} {flag_arg}')
    print(f'End: Copy at {time.strftime("%H:%M:%S",time.localtime())}')


def build():
    print('-----------------------------------')
    compile()
    print('-----------------------------------')
    link()
    print('-----------------------------------')
    copy()
    print('-----------------------------------')


def clear():
    files = os.listdir(buildDir)
    for f in files:
        os.remove(os.path.join(buildDir, f))
    os.remove('built.json')


if __name__ == '__main__':
    Preprocess()
    ReadChanging()
    compile()
    try:
        todo = sys.argv[1]
        if todo == 'compile':
            compile()
        elif todo == 'link':
            link()
        elif todo == 'copy':
            copy()
        elif todo == 'build':
            build()
        elif todo == 'clear':
            clear()
    except IndexError as e:
        print("Error: Please set an option:build/link")
    except Exception as e:
        print(e)
