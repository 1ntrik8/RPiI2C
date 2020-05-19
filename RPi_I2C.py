# Leigh Rowell
# ID: 219309149
# SIT210 - 8.1D
# RPi I2C Temperature

'''
References
http://blog.bitify.co.uk/2013/11/interfacing-raspberry-pi-and-mpu-6050.html
https://www.raspberrypi.org/forums/viewtopic.php?t=183445
https://www.electronicwings.com/raspberry-pi/raspberry-pi-i2c
https://www.electronicwings.com/raspberry-pi/mpu6050-accelerometergyroscope-interfacing-with-raspberry-pi
https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c
https://docs.particle.io/tutorials/learn-more/about-i2c/
https://www.electronicwings.com/download/attachment=Tue-01-18-12-09-06.MPU-6050_DataSheet.pdf
https://www.electronicwings.com/download/attachment=Tue-01-18-12-09-34.RM-MPU-60xxA.pdf
'''

'''
Setup:
This script operates a GY-521 Gyro-Accelerometer Sensor fitted with a MPU6050 chip.
Connect as follows:
Sensor - RPi:
VCC - 3V3
GND - GND
SCL - SCL
SDA - SDA
(Refer links above for installing relevent drivers and configuring RPi for I2C communications)
'''

# Imports
import smbus
from time import sleep

# MPU6050 Registers and Memory Address
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
TEMP_OUT = 0x41

def MPU_Init():
	#write to sample rate register
	bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)
	
	#Write to power management register
	bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)
	
	#Write to Configuration register
	bus.write_byte_data(Device_Address, CONFIG, 0)
	
	#Write to Gyro configuration register
	bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)
	
	#Write to interrupt enable register
	bus.write_byte_data(Device_Address, INT_ENABLE, 1)

def read_raw_data(addr):
	#Accelero and Gyro value are 16-bit
        high = bus.read_byte_data(Device_Address, addr)
        low = bus.read_byte_data(Device_Address, addr+1)
    
        #concatenate higher and lower value
        value = ((high << 8) | low)
        
        #to get signed value from mpu6050
        if(value > 32768):
                value = value - 65536
        return value


bus = smbus.SMBus(1) 	# or bus = smbus.SMBus(0) for older version boards
Device_Address = 0x68   # MPU6050 device address

MPU_Init()

print (" Reading GY-521 Temperature Data")

while True:

    #Read temp data
    #Temperature in degrees C = ((temperature sensor data)/340 + 36.53) °/c.
    temp_raw = read_raw_data(TEMP_OUT)

    Temp_c = temp_raw / 340 + 36.53

    print (" Temp = %.2f 'C" %Temp_c ) 	
    sleep(1)