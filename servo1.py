import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

GPIO.setup(11, GPIO.OUT)
servo1 = GPIO.PWM(11, 50)

servo1.start(0)
i = 0
try:
    while i <= 10:
        if (i % 2 == 0):
            angulo = 90
        else:
            angulo = 0
        servo1.ChangeDutyCycle(2 + (angulo / 18))
        time.sleep(0.5)
        servo1.ChangeDutyCycle(0)
        i += 1
finally:
    servo1.stop()
    GPIO.cleanup()
    print("adios")
