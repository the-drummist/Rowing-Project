from devices import MAX30102, EMG
import hrcalc
from rowinglib import Rowinguard
import csv
import time
from time import sleep
import logging

def collect_emg(emg, filename, logger):
	"""
	collect the data from the emg sensor and store it in a csv file
	"""
	# open the emg log (csv format) to start data collection
	with open(filename, mode='a') as emglog:
		# set the column header
		fieldnames = ['emg_reading', 'time']
		writer = csv.DictWriter(emglog, fieldnames=fieldnames)
		writer.writeheader()
		logger.debug('starting collect_emg()')
		# start timer
		start = time.process_time()
		# collect and write data to the csv file
		while True:
			emg_val = emg.read_analog()
			elapsed = time.process_time() - start
			print('emg: ', emg_val)
			writer.writerow({'emg_reading': emg_val, 'time': elapsed})
			sleep(0.5)

def collect_vitals(vitals, filename, logger):
	"""
	collect the data from the max30102 sensor and store it in a csv file
	"""
	# open the emg log (csv format) to start data collection
	with open(filename, mode='a') as vitalslog:
		# set the column headers
		fieldnames = ['hr', 'hr_valid', 'spo2', 'spo2_valid', 'time']
		writer = csv.DictWriter(vitalslog, fieldnames=fieldnames)
		writer.writeheader()
		logger.debug('starting collect_vitals()')
		# collect and write data to the csv file
		# start timer
		start = time.process_time()
		#time.clock() 
		while True:
			# collect raw readings
			red, ir = vitals.read_sequential(amount=100)
			elapsed = time.process_time() - start
			# process the readings: EXPERIMENTAL 
			hr, hr_valid, spo2, spo2_valid = hrcalc.calc_hr_and_spo2(ir, red)
			print('hr: ', hr, 'spo2', spo2)
			writer.writerow({'hr': hr, 'hr_valid': hr_valid, 'spo2': spo2, 'spo2_valid': spo2_valid, 'time': elapsed})
			sleep(0.5)

def form_monitor(emg, rowinguard, logger):
	"""
	checks if emg is consistantly reading higher than threshold
	"""
	THRESHOLD = 95 # percent... experimental
	logger.debug(f'starting form_monitor() with theshold of {THRESHOLD}%')
	emg_list = []
	for i in range(10):
		emg_list.append(emg.read_analog())
		delay(0.3)
	while True:
		avg = sum(emg_list) / len(emg_list)
		if avg >= THRESHOLD:
			rowinguard.alert('form')
		del emg_list[0]
		emg_list.append(emg.read_analog())
		delay(0.25)



def fatigue_monitor(emg, vitals, rowinguard, logger):
	"""
	checks if emg and oxygen are reading lower than they should be
	"""
	THRESHOLD = 90
	SPO2_MAX = 75 # minimum IDEAL range for a workout is 85%
	logger.debug(f'starting fatigue_monitor() with EMG threshold of {THRESHOLD}% and SpO2 threshold of {SPO2_MAX}%')
	emg_list = []
	spo2_list = []
	for i in range(50)
		emg_list.append(emg.read_analog())
		red, ir = vitals.read_sequential(amount=100)
		hr, hr_valid, spo2, spo2_valid = hrcalc.calc_hr_and_spo2(ir, red)
		if spo2_valid:
			spo2_list.append(spo2)
		delay(0.5)
	while True:
		avg_emg = sum(emg_list) / len(emg_list)
		avg_spo2 = sum(spo2_list) / len(spo2_list)
		if avg_emg >= THRESHOLD and avg_spo2 <= SPO2_MAX:
			rowinguard.alert('fatigue')
		del emg_list[0]
		del spo2_list[0]
		emg_list.append(emg.read_analog())
		red, ir = vitals.read_sequential(amount=100)
		hr, hr_valid, spo2, spo2_valid = hrcalc.calc_hr_and_spo2(ir, red)
		if spo2_valid:
			spo2_list.append()
		delay(0.25)

#def error_detection(emg, vitals, rowinguard)

def log_init():
	logger = logging.getLogger('ROWINGUARD')
	ch = logging.StreamHandler()
	formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s]: %(message)s')
	ch.setFormatter(formatter)
	logger.addHandler(ch)
	return logger

if __name__ == '__main__':
	logger = log_init()
	logger.info('Program Started')
	logger.info('Waiting for interrupt to continue')
	rowinguard = Rowinguard(interrupt=11,buz=13) # GPIO 17 and 27 respectivly 
	logger.info('Rowinguard instance created')
	logger.info('initializing EMG and Pulse Oximeter')
	emg, vitals = rowinguard.start_workout()
	logger.info('starting all threads')
	process_list = rowinguard.start_peripherals(collect_emg(emg, rowinguard.emg_file, logger), 
		collect_vitals(vitals, rowinguard.vitals_file, logger), 
		form_monitor(emg, rowinguard, logger), 
		fatigue_monitor(emg, vitals, rowinguard, logger))
	logger.info('parent thread waiting for interrupt to terminate the program')
	rowinguard.wait()
	for process in process_list:
		process.terminate()
	logger.info('all threads terminated')
	logger.info('goodbye')
	exit(0)