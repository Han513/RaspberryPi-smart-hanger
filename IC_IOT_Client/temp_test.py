import RPi.GPIO as GPIO

import time
import datetime
import dht11

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.cleanup()

instance = dht11.DHT11(pin = 7)

while True:
    ret = instance.read()
    print("-------------------------------------------------")
    if ret.is_valid():
        print(f"Current time {str(datetime.datetime.now())}")
        print(f"Current temperature: {ret.temperature} C")
        print(f"Current temperature: {ret.humidity} %")
        if ret.humidity <= 50.0 :
            print("You can collect your clothes!!!")
            break;
        elif 50.1 <= ret.humidity <= 60.0 :
            print('You can already check your clothes!!!')
            continue;

    time.sleep(3)
