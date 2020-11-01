import time
import board
import random

# For Trinket M0, Gemma M0, ItsyBitsy M0 Express, and ItsyBitsy M4 Express
import adafruit_dotstar
led = adafruit_dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1)

from analogio import AnalogOut

analog_out = AnalogOut(board.A0)

led.brightness = 1.0
i = 50
j = 50

GOING_UP_BEAT_ONE = 1
GOING_DOWN_BEAT_ONE = 2
MID_BEAT = 3
GOING_UP_BEAT_TWO = 4
GOING_DOWN_BEAT_TWO = 5
PAUSE = 6

state1 = GOING_UP_BEAT_ONE
state2 = GOING_UP_BEAT_ONE
led2Level = 50
heart_constant = 70

def heartFlash(state, i, brightness):
    #Add a random integer of wait time for beginning the next beat during the PAUSE state
    randomInt = random.randrange(100,250,1)
    if(state == GOING_UP_BEAT_ONE or state == GOING_UP_BEAT_TWO):
        i+=70
        led1Level = i/5 + 0.2*brightness
        led[0] = (0, led1Level, 0)
    elif(state == GOING_DOWN_BEAT_ONE or state == GOING_DOWN_BEAT_TWO):
        i-=70
        led1Level = i/5 + 0.2*brightness
        led[0] = (0, led1Level, 0)

    elif(state == MID_BEAT or state == PAUSE):
        i+=1
        led[0] = (0, 50, 0)

    if(state == GOING_UP_BEAT_ONE and i >200):
        state = GOING_DOWN_BEAT_ONE
    elif(state == GOING_DOWN_BEAT_ONE and i <= 50):
        state = MID_BEAT
    elif(state == MID_BEAT and i >= 60):
        state = GOING_UP_BEAT_TWO
        i = 50
    elif(state == GOING_UP_BEAT_TWO and i >200):
        state = GOING_DOWN_BEAT_TWO
    elif(state == GOING_DOWN_BEAT_TWO and i <= 80):
        state = PAUSE
    elif(state == PAUSE and i >=randomInt):
        state = GOING_UP_BEAT_ONE
        i = 50

    return (state, i)

def breathFlash(state, i):
    led2Level = i/8 + 172
    analog_out.value = round(led2Level/255*65535)
    if(state == GOING_UP_BEAT_ONE):
        i+=0.5
    elif(state == GOING_DOWN_BEAT_ONE):
        i-=0.5

    if(i==255):
        state = GOING_DOWN_BEAT_ONE
    elif(i==50):
        state = GOING_UP_BEAT_ONE
    return (state, i, led2Level)

while True:
    (state2, j, led2level) = breathFlash(state2,j)
    (state1, i) = heartFlash(state1,i,led2level)

    time.sleep(0.01)
