# import necessary libraries
import sys
import RPi.GPIO as GPIO, time
import datetime
import random
import threading

global lastPress
global ledChannels
global ledState
global exit_flag

def setLEDState(state):
    global ledChannels
    flag = state
    for i, var in enumerate(ledChannels):
        GPIO.output(var, flag)
        flag = not flag

def clearLEDs():
    for i, var in enumerate(ledChannels):
        GPIO.output(var, False)

def blinkLoop():
    global exit_flag
    blinkTimeout = random.random()
    ledState = False
    while not exit_flag.wait(timeout=blinkTimeout):
        print "Blinking for " + str(blinkTimeout) + " seconds" 
        setLEDState(ledState)
        ledState = not ledState
        blinkTimeout = random.random()
    print "Setting LED to off before exiting"
    clearLEDs()
    print "Exiting blink loop"
    exit_flag.clear()

def onButtonPress(channel):
    global lastPress
    global ledState
    global exit_flag
    eventTime = datetime.datetime.now()
    if eventTime - lastPress > datetime.timedelta(0, 1):
        print "Edge trigger at " + str(eventTime)
        print "Setting LED to " + str(ledState)

        if ledState is True:
            print "Starting blink loop"
            t = threading.Thread(target=blinkLoop)
            t.daemon = False
            t.start()
        else:
            print "Stopping blink loop"
            exit_flag.set()
        
        lastPress = eventTime
        ledState = not ledState

def _initializeGPIO(inputChannel, ledChannels):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(inputChannel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(inputChannel, GPIO.RISING, callback=onButtonPress)

    for i, var in enumerate(ledChannels):
        print "Initializing channel " + str(var) + " for GPIO.OUT"
        GPIO.setup(var, GPIO.OUT)

# initialize the GPIO
ledChannels = [17,27]
inputChannel = 26
_initializeGPIO (inputChannel, ledChannels)

# init global state
lastPress = datetime.datetime.now()
ledState = True
exit_flag = threading.Event()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print "Interupting program"

print "Stopping blinker function"
exit_flag.set()

# TODO: Wait for thread to exit...
time.sleep(1)

print "Cleaning up GPIO"
GPIO.cleanup()

print "Exiting program"
sys.exit(0)
