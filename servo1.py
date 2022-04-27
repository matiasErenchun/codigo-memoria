import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

GPIO.setip(11,GPIO.OUT)
servo1 = GPIO.PWM(11,50)

servo1.start(0)
try:
    while True:
        angulo = float(input('ingrese un angulo:'))
        servo1.ChangeDutyCycle(2+(angulo/18))
        time.sleep(0.5)
        servo1.ChangeDutyCycle(0)
finally:
    servo1.stop()
    GPIO.cleanup()
    print("adios")