import time
import board
import digitalio 
import pulseio
from adafruit_motor import servo
import adafruit_dotstar

MIN = 155
MAX = 40
HALF = 90
JIGGLE = 130
ALMOST = 72


# Servo
pwm = pulseio.PWMOut(board.D3, duty_cycle=2 ** 15, frequency=50)
my_servo = servo.Servo(pwm, min_pulse = 580, max_pulse = 2400)

# Button
button = digitalio.DigitalInOut(board.D4)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

# On-board LED
led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT
led.value = False

onboard = adafruit_dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1)
onboard[0] = (0, 0, 0)

def control(servo, start, end, delay, increment=1, loop=False):
    if end < start :
        increment = -increment
    for angle in range(start, end, increment):  # min to max degrees
        my_servo.angle = angle
        time.sleep(delay)
    if loop == True :
        for angle in range(end, start, -increment):  # min to max degrees
            my_servo.angle = angle
            time.sleep(delay)
    
my_servo.angle = MIN


iteration = 1
while True :
    if button.value :
        print(iteration)
        if iteration==2 :
            control(my_servo, MIN, MAX, 0.015, loop=True)
            time.sleep(0.3)
            control(my_servo, MIN, HALF, 0.003)
            time.sleep(2)
            control(my_servo, HALF, MIN, 0.01)
        elif iteration == 4 :
            time.sleep(3)
            control(my_servo, MIN, HALF, 0.003)
            time.sleep(2)
            control(my_servo, HALF, MAX, 0.03)
            control(my_servo, MAX, MIN, 0.005)
        elif iteration == 5 :
            control(my_servo, MIN, JIGGLE, 0.005, loop=True)
            control(my_servo, MIN, JIGGLE, 0.005, loop=True)
            control(my_servo, MIN, JIGGLE, 0.005, loop=True)
            control(my_servo, MIN, JIGGLE, 0.005, loop=True)
            control(my_servo, MIN, JIGGLE, 0.005, loop=True)
            time.sleep(2)
            control(my_servo, MIN, MAX, 0.02)
            control(my_servo, MAX, HALF, 0.02)
            time.sleep(1)
            control(my_servo, HALF, ALMOST, 0.005)
            time.sleep(0.2)
            control(my_servo, ALMOST, HALF, 0.005, loop=True)
            time.sleep(1)
            control(my_servo, ALMOST, MIN, 0.01)
        elif iteration == 6 :
            time.sleep(3)
            control(my_servo, MIN, ALMOST, 0.005)
            time.sleep(1)
            control(my_servo, ALMOST, HALF, 0.005)
            time.sleep(1)
            control(my_servo, HALF, ALMOST, 0.01)
            time.sleep(3)
            control(my_servo, ALMOST, MIN, 0.03)
            time.sleep(7)
        else :
            control(my_servo, MIN, MAX, 0.005, loop=True)
            if iteration >=7 :
                iteration = 0
        iteration+=1
    time.sleep(1)