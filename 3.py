#-*-coding:utf-8-*-

import RPi.GPIO as GPIO
import time

num_bits = 8

GPIO.setmode(GPIO.BCM)
GPIO.setup(10, GPIO.OUT)
GPIO.setup(9, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)

D = [10, 9, 11, 5, 6, 13, 19, 26]

GPIO.output(D[:], 0)

def decToBinList(decNumber):
    decNumber = decNumber % 256
    N = num_bits - 1
    bits = []
    while N > 0:
        if(int(decNumber/(2**N)) == 1):
            bits.append(1)
            decNumber -= 2**N
        else:
            bits.append(0)
        N -= 1
    bits.append(decNumber)
    return bits

def num2dac(value):
    bits = decToBinList(value)
    for i in range (0, num_bits):
        GPIO.output(D[i], bits[num_bits - (i + 1)])

def translation(value):
    return (((value % 256) * 3.3)/255)

def adc_procedure():
    N = 7
    middle = 128 
    while N > 0:
        num2dac(middle)
        time.sleep(0.001)
        if GPIO.input(24) == 1:
            middle -= 2**(N - 1)
        else:
            middle += 2**(N - 1)
        N -= 1
    return middle-1

try:
    while True:
        num = adc_procedure()
        print("Digital value:", num,", Analog value:", translation(num), "V")
       
except KeyboardInterrupt:
    print("\n############################################")
    print("# Программа была остановлена пользователем #")
    print("############################################\n")
    exit()
finally:
	GPIO.cleanup()
