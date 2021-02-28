import numpy as np
import scipy as sp
from scipy import signal
import os

def read_csv_data(emg_csv):
	"""
	read the data from the csv files into numpy arrays and correct the data offset
	"""
	with open(emg_csv) as emg_file:
		# read the emg data into numpy arrays
		emg_data = np.array([row['emg_reading'] for row in DictReader(emg_file)])
		emg_time = np.array([row['time'] for row in DictReader(emg_file)])
	# correct the mean of the reading: centers the waves at 0 volts without changing amplitude or frequency
	emg_data = emg_data - np.mean(emg_data)
	return emg_data

def filter_data(emg_data, high_band=20, low_band=450, sampling_frequency=1000,):
	"""
	filter the emg data with high and low pass filters. then smooth the data and rectify it
	"""
	# create filter params (high-pass and low-pass)
	high = high_band / (sampling_frequency / 2)
	low = low_band / (sampling_frequency / 2)
	# create butterworth filter: returns filter coefficients
	b, a = sp.signal.butter(4, [high, low], btype='bandpass')
	# filter data (linear filter)
	emg_filtered = sp.signal.filtfilt(b, a, emg_data)
	# rectiy the filtered data
	emg = abs(emg_filtered)

def get_dir():
	"""
	get the directory with the test data and return the csv file paths
	"""
	path = input("full path of datasets:\n> ")
	files = os.listdir(path)
	csv_files = [path + '\\' + file for file in files if file.endswith("_emg.csv")]
	print(csv_files)
	return csv_files

def get_top_vals(filtered_emg):
	# sort descending and take the first 3 values (highest)
	top_three = sorted(filtered_emg, reverse=True)[:3]
	avg = sum(top_three) / len(top_three)
	return avg


if __name__ == '__main__':
	# get a list of files (including path)
	files = get_dir()
	# list to hold the average top value of each file
	top_vals = []
	for file in files:
		# read data from the current file
		emg_data = read_csv_data(file)
		# filter the data
		filtered_emg = filter_data(emg_data)
		# get the average of the top 3 values of each file and append it to the list
		top_avg = get_top_vals(filtered_emg)
		top_vals.append(top_avg)
	print(top_vals)
	print("average of averages: " + sum(top_vals) /len(top_vals))

