# for version 1 of prototype
from devices import MAX30102, EMG
import hrcalc
import csv
from multiprocessing import Process
import time
from time import sleep

def setup(emg_channel=0, pulse_pin=3):
	"""
	setup the peripheral devices
	"""
	vitals = MAX30102(gpio_pin=pulse_pin)
	emg = EMG(emg_channel)
	tester = input('name of tester: ')
	# emg.calibrate()
	return emg, vitals, tester

def collect_emg(emg, tester):
	"""
	collect the data from the emg sensor and store it in a csv file
	"""
	tester += '_emg.csv'
	# open the emg log (csv format) to start data collection
	with open(tester, mode='a') as emglog:
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

def collect_vitals(vitals, tester):
	"""
	collect the data from the max30102 sensor and store it in a csv file
	"""
	tester += '_vitals.csv'
	# open the emg log (csv format) to start data collection
	with open(tester, mode='a') as vitalslog:
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

# collect the sensor data in parallel 
def start_peripherals(*funcs):
	toJoin = list()
	# create a process for each target function and start it
	for func in funcs:
		process = Process(target=func)
		process.start()
		toJoin.append(process)
	# join the processes
	for process in toJoin:
		process.join()

if __name__ == '__main__':
	# construct the EMG and MAX30102
	emg, vitals, tester = setup() # set pins here
	# run the data collection in parallel
	start_peripherals(collect_emg(emg, tester), collect_vitals(vitals, tester))
