# import necessary libraries
import RPi.GPIO as GPIO, time

# initialize the GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)

# define a function to turn the light on and off
def blinkOnce(pin,rate):
    GPIO.output(pin,True)
    time.sleep(rate)
    GPIO.output(pin,False)
    time.sleep(rate)

# Blink until told to stop
try:
    while True:
        blinkOnce(17,0.5)
except KeyboardInterrupt:
    print "Interupting program"
    sys.exit()    

# cleanup
GPIO.cleanup()
