from devices import MAX30102, EMG
import hrcalc
from rowinglib import Rowinguard
import csv
import time
from time import sleep


def collect_emg(emg, filename):
	"""
	collect the data from the emg sensor and store it in a csv file
	"""
	# open the emg log (csv format) to start data collection
	with open(filename, mode='a') as emglog:
		# set the column header
		fieldnames = ['emg_reading', 'time']
		writer = csv.DictWriter(emglog, fieldnames=fieldnames)
		writer.writeheader()
		# start timer
		start = time.time()
		time.clock() 
		# collect and write data to the csv file
		while True:
			emg_val = emg.read_analog()
			elapsed = time.time() - start
			print('emg: ', emg_val)
			writer.writerow({'emg_reading': emg_val, 'time': elapsed})
			sleep(0.5)

def collect_vitals(vitals, filename):
	"""
	collect the data from the max30102 sensor and store it in a csv file
	"""
	# open the emg log (csv format) to start data collection
	with open(filename, mode='a') as vitalslog:
		# set the column headers
		fieldnames = ['hr', 'hr_valid', 'spo2', 'spo2_valid', 'time']
		writer = csv.DictWriter(vitalslog, fieldnames=fieldnames)
		writer.writeheader()
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

def form_monitor(emg, rowinguard):
	"""
	checks if emg is consistantly reading higher than threshold
	"""
	THRESHOLD = 95 # percent... experimental
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



def fatigue_monitor(emg, vitals, rowinguard):
	"""
	checks if emg and oxygen are reading lower than they should be
	"""
	THRESHOLD = 90
	SPO2_MAX = 75 # minimum IDEAL range for a workout is 85%
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

if __name__ == '__main__':
	rowinguard = Rowinguard(interrupt=,buz=)
	emg, vitals = rowinguard.start_workout()
	process_list = rowinguard.start_peripherals(collect_emg(emg, rowinguard.emg_file), 
		collect_vitals(vitals, rowinguard.vitals_file), 
		form_monitor(emg, rowinguard), 
		fatigue_monitor(emg, vitals, rowinguard), 
		error_detection(emg, vitals, rowinguard))
	rowinguard.wait()
	for process in process_list:
		process.terminate()
	exit(0)