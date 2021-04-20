from __future__ import print_function
from time import sleep
import numpy as np
import scipy as sp
from scipy import signal
import RPi.GPIO as GPIO
import smbus
import logging
import spidev
#import board
#import adafruit_mcp3xxx.mcp3008 as MCP
#from adafruit_mcp3xxx.analog_in import AnalogIn
#import digitalio
#import busio

# class for the EMG sensor
BASELINE = None
class EMG:
	# construct the class with the connected pin
	def __init__(self, channel=0):
		logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] [%(name)s] [%(levelname)s]: %(message)s')
		logger = logging.getLogger('EMG')
		self.logger = logger
		# create filter params (high-pass and low-pass)
		high = 20 / (1000 / 2)
		low = 450 / (1000 / 2)
		# create butterworth filter: returns filter coefficients
		self.b, self.a = sp.signal.butter(4, [high, low], btype='bandpass')
		# create spi bus
		self.spi = spidev.SpiDev()
		self.spi.open(0, 0)
		assert channel <= 7 and channel >=0, 'EMG channel not within bounds'
		self.spi.max_speed_hz = 1350000
		self.channel = channel
		self.logger.info(f'EMG initialized on channel {channel} at {self.spi.max_speed_hz}hz')

	# calibrate the EMG
	# this will only be necessary if different users get wildly different values 
	def calibrate(self):
		pass

	def read_analog(self):
		read = self.spi.xfer2([1, (8 + self.channel) << 4, 0])
		data = ((read[1] & 3) << 8) + read[2]
		return data

	def read_percent(self):
		"""
		returns a emg as a percentage of the maximum acceptable range
		"""
		_MAX = TODO!!
		return (self.read_analog() / _MAX) * 100
	"""
	# get the current value from the EMG
	def get_raw(self):
		return self.pin.value

	# read the emg to a buffer and return it to be normalized
	def read_sequential(self, amount=100):
		emg_buf = []
		for i in range(amount):
			emg_buf.append(self.get_raw())
		return np.array(emg_buf)

	def get_normalized(self):
		buf = self.read_sequential()

		# filter data (linear filter)
		emg_filtered = sp.signal.filtfilt(self.b, self.a, buf)
		# rectiy the filtered data
		emg = abs(emg_filtered) / BASELINE
		return emg
	"""



### credit for the following section: https://github.com/vrano714/max30102-tutorial-raspberrypi/blob/master/max30102.py ###
# this code is currently for python 2.7


# i2c address-es
# not required?
I2C_WRITE_ADDR = 0xAE
I2C_READ_ADDR = 0xAF

# register address-es
REG_INTR_STATUS_1 = 0x00
REG_INTR_STATUS_2 = 0x01

REG_INTR_ENABLE_1 = 0x02
REG_INTR_ENABLE_2 = 0x03

REG_FIFO_WR_PTR = 0x04
REG_OVF_COUNTER = 0x05
REG_FIFO_RD_PTR = 0x06
REG_FIFO_DATA = 0x07
REG_FIFO_CONFIG = 0x08

REG_MODE_CONFIG = 0x09
REG_SPO2_CONFIG = 0x0A
REG_LED1_PA = 0x0C

REG_LED2_PA = 0x0D
REG_PILOT_PA = 0x10
REG_MULTI_LED_CTRL1 = 0x11
REG_MULTI_LED_CTRL2 = 0x12

REG_TEMP_INTR = 0x1F
REG_TEMP_FRAC = 0x20
REG_TEMP_CONFIG = 0x21
REG_PROX_INT_THRESH = 0x30
REG_REV_ID = 0xFE
REG_PART_ID = 0xFF



class MAX30102():
	# by default, this assumes that physical pin 3 (GPIO 2) is used as interrupt
	# by default, this assumes that the device is at 0x57 on channel 1
	def __init__(self, channel=1, address=0x57, gpio_pin=3):
		logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] [%(name)s] [%(levelname)s]: %(message)s')
		logger = logging.getLogger('MAX30102')
		self.logger = logger

		self.logger.info('Channel: {0}, address: 0x{1:x}'.format(channel, address))
		self.address = address
		self.channel = channel
		self.bus = smbus.SMBus(self.channel)
		self.interrupt = gpio_pin

		# set gpio mode
		GPIO.setmode(GPIO.BOARD)
		try:
			GPIO.setup(self.interrupt, GPIO.IN)
		except:
			self.logger.critical('GPIO setup failed', exc_info=True)
		try:
			self.reset()
		except:
			self.logger.critical('internal reset method failed', exc_info=True)

		sleep(1)  # wait 1 sec

		# read & clear interrupt register (read 1 byte)
		reg_data = self.bus.read_i2c_block_data(self.address, REG_INTR_STATUS_1, 1)
		# print("[SETUP] reset complete with interrupt register0: {0}".format(reg_data))
		try:
			self.setup()
		except:
			self.logger.critical('internal setup function failed', exc_info=True)
		# print("[SETUP] setup complete")
		self.logger.info('initialized successfully')
		
	def shutdown(self):
		"""
		Shutdown the device.
		"""
		self.bus.write_i2c_block_data(self.address, REG_MODE_CONFIG, [0x80])

	def reset(self):
		"""
		Reset the device, this will clear all settings,
		so after running this, run setup() again.
		"""
		self.bus.write_i2c_block_data(self.address, REG_MODE_CONFIG, [0x40])

	def setup(self, led_mode=0x03):
		"""
		This will setup the device with the values written in sample Arduino code.
		"""
		# INTR setting
		# 0xc0 : A_FULL_EN and PPG_RDY_EN = Interrupt will be triggered when
		# fifo almost full & new fifo data ready
		self.bus.write_i2c_block_data(self.address, REG_INTR_ENABLE_1, [0xc0])
		self.bus.write_i2c_block_data(self.address, REG_INTR_ENABLE_2, [0x00])

		# FIFO_WR_PTR[4:0]
		self.bus.write_i2c_block_data(self.address, REG_FIFO_WR_PTR, [0x00])
		# OVF_COUNTER[4:0]
		self.bus.write_i2c_block_data(self.address, REG_OVF_COUNTER, [0x00])
		# FIFO_RD_PTR[4:0]
		self.bus.write_i2c_block_data(self.address, REG_FIFO_RD_PTR, [0x00])

		# 0b 0100 1111
		# sample avg = 4, fifo rollover = false, fifo almost full = 17
		self.bus.write_i2c_block_data(self.address, REG_FIFO_CONFIG, [0x4f])

		# 0x02 for read-only, 0x03 for SpO2 mode, 0x07 multimode LED
		self.bus.write_i2c_block_data(self.address, REG_MODE_CONFIG, [led_mode])
		# 0b 0010 0111
		# SPO2_ADC range = 4096nA, SPO2 sample rate = 100Hz, LED pulse-width = 411uS
		self.bus.write_i2c_block_data(self.address, REG_SPO2_CONFIG, [0x27])

		# choose value for ~7mA for LED1
		self.bus.write_i2c_block_data(self.address, REG_LED1_PA, [0x24])
		# choose value for ~7mA for LED2
		self.bus.write_i2c_block_data(self.address, REG_LED2_PA, [0x24])
		# choose value fro ~25mA for Pilot LED
		self.bus.write_i2c_block_data(self.address, REG_PILOT_PA, [0x7f])

	# this won't validate the arguments!
	# use when changing the values from default
	def set_config(self, reg, value):
		self.bus.write_i2c_block_data(self.address, reg, value)

	def read_fifo(self):
		"""
		This function will read the data register.
		"""
		red_led = None
		ir_led = None

		# read 1 byte from registers (values are discarded)
		reg_INTR1 = self.bus.read_i2c_block_data(self.address, REG_INTR_STATUS_1, 1)
		reg_INTR2 = self.bus.read_i2c_block_data(self.address, REG_INTR_STATUS_2, 1)

		# read 6-byte data from the device
		d = self.bus.read_i2c_block_data(self.address, REG_FIFO_DATA, 6)

		# mask MSB [23:18]
		red_led = (d[0] << 16 | d[1] << 8 | d[2]) & 0x03FFFF
		ir_led = (d[3] << 16 | d[4] << 8 | d[5]) & 0x03FFFF

		return red_led, ir_led

	def read_sequential(self, amount=100):
		"""
		This function will read the red-led and ir-led `amount` times.
		This works as blocking function.
		"""
		red_buf = []
		ir_buf = []
		for i in range(amount):
			while(GPIO.input(self.interrupt) == 1):
				# wait for interrupt signal, which means the data is available
				# do nothing here
				pass

			red, ir = self.read_fifo()

			red_buf.append(red)
			ir_buf.append(ir)

		return red_buf, ir_buf
### end credited section ###