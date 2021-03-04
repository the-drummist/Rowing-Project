# helper library for rowinguard
from datetime import datetime

class Rowinguard:

	def __init__(self):
		self.emg_file = generate_name('emg')
		self.vitals_file = generate_name('vitals')

	def generate_name(dataform):
		if dataform == 'emg' or dataform == 'vitals':
			date = datetime.now().strftime('_%Y_%m_%d-%I_%M_%S_%p')
			filename = dataform + date + '.csv'
			return filename


	def store_data(self):
		pass

	def start_workout(self):
		pass

	def end_workout(self):
		pass



