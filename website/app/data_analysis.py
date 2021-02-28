# data analysis software goes here
from csv import DictReader
from bokeh.plotting import figure, curdoc
from bokeh.embed import file_html
from bokeh.models import ColumnDataSource, BoxAnnotation, NumeralTickFormatter
from bokeh.layouts import column
class Data:
	def __init__(self, emgfile, vitalsfile, age, weight, gender):
		"""
		Construct the Data class, parse the files into lists
		"""
		self.age = age
		# convert weight to kilograms
		self.weight = weight * 0.453592
		self.gender = gender
		# parse emg data and time into lists and dicts
		with open(emgfile, mode='r') as emg:
			# list comprehension to form the lists
			self.emg_data = {
				'y_values': [row['emg_reading'] for row in DictReader(emg)],
				'x_values': [row['time'] for row in DictReader(emg)]
				}
			# calculate the duration (minutes) based on the last time reading
			self.duration = self.emg_data[-1][1] / 60

		# parse pulse data and time into a dict of lists and SpO2 data and time into a dict of lists

		hr_avg = 0.0
		with open(vitalsfile, mode='r') as vitals:
			# list comprehension to form the lists with ONLY valid data
			self.hr_data = {
				'y_values': [row['hr'] if row['hr_valid'] is True for row in DictReader(vitals)]
				'x_values': [[row['time'] if row['hr_valid'] is True for row in DictReader(vitals)]]
				}
			self.spo2_data = {
				'y_values': [row['spo2'] if row['spo2_valid'] is True for row in DictReader(vitals)]
				'x_values': [[row['time'] if row['spo2_valid'] is True for row in DictReader(vitals)]]
			}
			self.hr_avg = hr_avg / len(hr)



	def get_calories(self):
		"""
		calculate the calories burnt based on age weight avg heart rate and duration
		"""
		if self.gender is 'male':
			calories = ((-55.0969 + (0.6309 * self.hr_avg) + (0.1988 * self.weight) + (0.2017 * self.age)) / 4.184) * self.duration
		elif self.gender is 'female':
			calories = ((-20.4022 + (0.4472 * self.hr_avg) - (0.1263 * self.weight) + (0.074 * self.age)) / 4.184) * self.duration
		else:
			# if no gender is provided, calculate male (more common with rowers)
			calories = ((-55.0969 + (0.6309 * self.hr_avg) + (0.1988 * self.weight) + (0.2017 * self.age)) / 4.184) * self.duration
		return calories


	def hr_range(self):
		"""
		calculate upper and lower bounds for the target heart rate
		"""
		max_rate = 220 - self.age
		upper_limit = 0.85 * max_rate
		lower_limit = 0.6 * max_rate
		return upper_limit, lower_limit


	def shear_load_graph(self):
		"""this would take the emg readings an map it to aproximate load force
			can't do this until we test
		"""
		pass


	def intensity_graph(self):
		"""
		calculate the intensity of the workout over time and graph it
		"""
		pass


	def emg_graph(self):
		"""
		create the emg_graph html
		"""
		source = ColumnDataSource(self.emg_data)
		curdoc().theme = 'dark_minimal'
		plot = figure(title='Electromyography of the Lats', x_axis_label='Workout Duration', y_axis_label='Muscle Activation', toolbar_location='right')
		# low_box = BoxAnnotation(top=85, fill_alpha=0.1, fill_color='red')
		# mid_box = BoxAnnotation(bottom=85, top=92, fill_alpha=0.1, color='green')
		# high_box = BoxAnnotation(bottom=92, fill_alpha=0.1, color='yellow')
		# plot.add_layout(low_box)
		# plot.add_layout(mid_box)
		# plot.add_layout(high_box)
		# draw line
		plot.line(x='x_values', y='y_values', sorce=source)
		return plot


	def spo2_graph(self):
		"""
		create the spo2 graph html
		"""
		source = ColumnDataSource(self.spo2_data)
		curdoc().theme = 'dark_minimal'
		plot = figure(title='Oxygen Saturation', x_axis_label='Workout Duration', y_axis_label='SpO2 Level', toolbar_location='right')
		# add colors
		low_box = BoxAnnotation(top=85, fill_alpha=0.1, fill_color='red')
		mid_box = BoxAnnotation(bottom=85, top=92, fill_alpha=0.1, color='green')
		high_box = BoxAnnotation(bottom=92, fill_alpha=0.1, color='yellow')
		plot.add_layout(low_box)
		plot.add_layout(mid_box)
		plot.add_layout(high_box)
		# draw line
		plot.line(x='x_values', y='y_values', sorce=source)
		return plot

	def hr_graph(self, max_hr, min_hr):
		"""
		create the heart rate graph html
		"""
		source = ColumnDataSource(self.hr_data)
		curdoc().theme = 'dark_minimal'
		plot = figure(title='Heart Rate', x_axis_label='Workout Duration', y_axis_label='BPM', toolbar_location='right')
		# add colors
		low_box = BoxAnnotation(top=min_hr, fill_alpha=0.1, fill_color='red')
		mid_box = BoxAnnotation(bottom=min_hr, top=max_hr, fill_alpha=0.1, color='green')
		high_box = BoxAnnotation(bottom=max_hr, fill_alpha=0.1, color='red')
		plot.add_layout(low_box)
		plot.add_layout(mid_box)
		plot.add_layout(high_box)
		# draw line
		plot.line(x='x_values', y='y_values', sorce=source)
		return plot

	def analyse():
		"""
		callable function to tie the class together
		consider using multithreading if this takes too long
		"""
		calories = get_calories()
		max_hr, min_hr = hr_range()
		hr_plot = hr_graph(max_hr,min_hr)
		spot_plot = spo2_graph()
		emg_plot = emg_graph()
		intensity_plot = intensity_graph()
		shear_plot = shear_load_graph()
		return calories, file_html(column(hr_plot, spo2_plot, emg_plot, intensity_plot, shear_plot, sizing_mode='scale_width'))
