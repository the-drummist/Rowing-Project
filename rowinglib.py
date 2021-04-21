# helper library for rowinguard
from datetime import datetime
from multiprocessing import Process
import RPi.GPIO as GPIO
from time import sleep
import logging

class Rowinguard:

	def __init__(self, interupt, buzz):
		logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] [%(name)s] [%(levelname)s]: %(message)s')
		logger = logging.getLogger('ROWINGLIB')
		self.logger = logger
		self.emg_file = self.generate_name('emg')
		self.vitals_file = self.generate_name('vitals')
		self.interupt = interupt
		GPIO.setup(buzz, GPIO.OUT)
		GPIO.output(buzz, GPIO.LOW)
		self.buzz = buzz
		GPIO.setmode(GPIO.BOARD)


	def generate_name(self, dataform):
		if dataform == 'emg' or dataform == 'vitals':
			date = datetime.now().strftime('%Y_%m_%d-%I_%M_%S_%p_')
			filename = date + dataform + '.csv'
			return filename
		else:
			self.logger.error('invalid file type provided')

	def start_peripherals(self, *funcs):
	toJoin = list()
	# create a process for each target function and start it
	for func in funcs:
		process = Process(target=func)
		process.start()
		toJoin.append(process)
	# join the processes
	for process in toJoin:
		process.join()
	self.logger.debug('peripherals starting')
	return toJoin


	def alert(self, _type):
		if _type == 'form':
			self.logger.debug('starting form alert')
			GPIO.output(self.buzz, GPIO.HIGH)
			sleep(1)
			GPIO.output(self.buzz, GPIO.LOW)
			sleep(1)
		elif _type == 'fatigue':
			self.logger.debug('starting fatigue alert')
			GPIO.output(self.buzz, GPIO.HIGH)
			sleep(.5)
			GPIO.output(self.buzz, GPIO.LOW)
			sleep(.5)
		else:
			self.logger.warning('invalid alert type')

	def start_workout(self):
		# wait for interupt here
		GPIO.wait_for_edge(self.interupt, GPIO.RISING)
		self.logger.info('rising edge detected')
		emg = EMG(0)
		vitals = MAX30102()
		return emg, vitals

	def end_workout(self):
		# wait for interupt
		GPIO.wait_for_edge(self.interupt, GPIO.FALLING)
		self.logger.info('falling edge detected')
		



