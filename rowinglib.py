# helper library for rowinguard
from datetime import datetime
from multiprocessing import Process
import RPi.GPIO as GPIO
from time import sleep
import logging
from devices import EMG, MAX30102

class Rowinguard:

	def __init__(self, interrupt, buzz):
		logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] [%(name)s] [%(levelname)s]: %(message)s')
		logger = logging.getLogger('ROWINGLIB')
		self.logger = logger
		self.emg_file = self.generate_name('emg')
		self.vitals_file = self.generate_name('vitals')
		self.interrupt = interrupt
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(self.interrupt, GPIO.IN)
		GPIO.setup(buzz, GPIO.OUT)
		GPIO.output(buzz, GPIO.LOW)
		self.buzz = buzz


	def generate_name(self, dataform):
		if dataform == 'emg' or dataform == 'vitals':
			date = datetime.now().strftime('%Y_%m_%d-%I_%M_%S_%p_')
			filename = date + dataform + '.csv'
			return filename
		else:
			self.logger.error('invalid file type provided')

	def start_peripherals(self, args):
		processes = list()
		# create a process for each target function and start it
		for arg in args:
			process = Process(target=arg[0], args=arg[1])
			process.start()
			processes.append(process)
		# join the processes
		self.logger.debug('all processes started')
		return processes


	def alert(self, _type):
		buzzer = GPIO.PWM(self.buzz, 1000)
		if _type == 'form':
			self.logger.debug('starting form alert')
			buzzer.start(2)
			sleep(1)
			buzzer.stop()
			sleep(1)
		elif _type == 'fatigue':
			self.logger.debug('starting fatigue alert')
			buzzer.start(2)
			sleep(.5)
			buzzer.stop()
			sleep(.5)
		else:
			self.logger.warning('invalid alert type')

	def start_workout(self):
		# wait for interupt here
		GPIO.wait_for_edge(self.interrupt,	GPIO.RISING)
		self.logger.info('rising edge detected')
		emg = EMG(0)
		vitals = MAX30102()
		return emg, vitals

	def end_workout(self):
		# wait for interupt
		GPIO.wait_for_edge(self.interrupt,	GPIO.FALLING)
		self.logger.info('falling edge detected')
		



