import warnings
warnings.simplefilter('ignore')

import time
import board
import busio
import adafruit_ds3231
from time import sleep
from gpiozero import LED
from subprocess import run


i2c = busio.I2C(board.SCL, board.SDA)
ds3231 = adafruit_ds3231.DS3231(i2c)


activity_led = LED(26) #activity LED blink pin
timer_latch = LED(17)       #Trigger the timer latching switch

print('Blinking PiWild activity LED')

activity_led.on()
sleep(2)
activity_led.off()

print('Setting alarm')

t=ds3231.datetime
t=list(t)
print(t)
t[4] = t[4] + 10
if t[4] > 60:
	t[4] = t[4] - 60
	t[3] += 1
t=tuple(t)

ds3231.alarm1 = (time.struct_time(t),'daily')
if ds3231.alarm1_status:
	print("wake up!")
	ds3231.alarm1_status = False

print('The system will wake up at: ', t)

sleep(2)

print('Triggering timer circuit to switch off power to Pi after about 2 minutes...')

timer_latch.on() #Set GPIO pin 18 high to trigger the latching switch of the timer circuit
sleep(1)
timer_latch.off()


print('Pi about to shutdown ...')
sleep(3)
run(['sudo', 'shutdown', 'now'], check=True)
