from devices import EMG
import csv
import time

def collect_emg(emg, tester):
	"""
	collect the data from the emg sensor and store it in a csv file
	"""
	emg = EMG(channel=0)
	tester = input('name of tester: ')
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
