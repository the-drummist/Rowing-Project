# helper library for rowinguard
from datetime import datetime
from multiprocessing import Process
import RPi.GPIO as GPIO

class Rowinguard:

	def __init__(self, interupt):
		self.emg_file = self.generate_name('emg')
		self.vitals_file = self.generate_name('vitals')
		self.interupt = interupt
		GPIO.setmode(GPIO.BOARD)


	def generate_name(self, dataform):
		if dataform == 'emg' or dataform == 'vitals':
			date = datetime.now().strftime('%Y_%m_%d-%I_%M_%S_%p_')
			filename = date + dataform + '.csv'
			return filename

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
	return toJoin


	def alert(self, type):


	def start_workout(self):
		# wait for interupt here
		GPIO.wait_for_edge(self.interupt, GPIO.RISING)
		emg = EMG(0)
		vitals = MAX30102(3)
		return emg, vitals

	def end_workout(self):
		# wait for interupt
		GPIO.wait_for_edge(self.interupt, GPIO.FALLING)
		



