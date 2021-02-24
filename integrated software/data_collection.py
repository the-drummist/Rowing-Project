# for version 1 of prototype
from devices import MAX30102, EMG
import csv
from multiprocessing import Process

def setup(emg_pin, pulse_pin):
	"""
	setup the peripheral devices
	"""
	vitals = MAX30102(pulse_pin)
	emg = EMG(emg_pin)
	# emg.calibrate()
	return emg, vitals

def collect_emg(emg):
	"""
	collect the data from the emg sensor and store it in a csv file
	"""
	# open the emg log (csv format) to start data collection
	with open('emg.csv', 'a') as emglog:
		# set the column header
		fieldnames = ['emg_reading']
		writer = csv.DictWriter(emglog, fieldnames=fieldnames)
		writer.writeheader()
		# collect and write data to the csv file
		while True:
			emg_val = emg.get_value()
			writer.writerow({'emg_reading': emg_val})

def collect_vitals(vitals):
	"""
	collect the data from the max30102 sensor and store it in a csv file
	"""
	# open the emg log (csv format) to start data collection
	with open('vitals.csv', 'a') as vitalslog:
		# set the column headers
		fieldnames = ['hr', 'hr_valid', 'spo2', 'spo2_valid',]
		writer = csv.DictWriter(emglog, fieldnames=fieldnames)
		writer.writeheader()
		# collect and write data to the csv file
		while True:
			# collect raw readings
			red, ir = vitals.read_sequential(amount=100)
			# process the readings: EXPERIMENTAL 
			hr, hr_valid, spo2, spo2_valid = hrcalc.calc_hr_and_spo2(ir, red)
			writer.writerow({'hr': hr, 'hr_valid': hr_valid, 'spo2': spo2, 'spo2_valid': spo2_valid})


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
	emg, vitals = setup()
	# run the data collection in parallel
	start_peripherals(collect_emg(emg), collect_vitals(vitals))