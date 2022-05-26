from urllib.request import urlopen
from zipfile import ZipFile
from io import BytesIO
from datetime import datetime, date, timedelta
import sys
import os
import shutil
import pandas as pd


# get dates in-between start and end(excluded)
def dateRange(start, end):
	dd,mm,yyyy = list(map(int, start.split('-')))

	# check if valid date is passed
	try:
		start = date(yyyy,mm,dd)
	except ValueError:
		print("Wrong day or month value for start day")
		sys.exit(0)
	dd,mm,yyyy = list(map(int, end.split('-')))
	try:
		end = date(yyyy,mm,dd)
	except ValueError:
		print("Wrong day or month value for end day")
		sys.exit(0)

	for n in range((end-start).days):
		curr_date = start+timedelta(n)

		# exclude saturdays and sundays
		if curr_date.weekday() in [5,6]: 
			continue
		yield curr_date


class DataFetcher:
	months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
	
	def decompress_data(self):
		extract_dir = os.path.join('data', '')

		# check is extarct dir exist. If not, create one 
		if not os.path.isdir(extract_dir):
			os.mkdir('data')

		# extract all the csv files into extract dir 
		if os.path.isfile('BharvData.zip'):
			shutil.unpack_archive('BharvData.zip', extract_dir)
			os.remove('BharvData.zip')


	def BharvFetchFrom(self, start, end):

		# decompress existing data
		self.decompress_data()
		
		for date in dateRange(start, end):
			
			# split date into year, month and day
			yyyy, mm, dd = date.strftime("%Y-%m-%d").split('-')

			# get resptv. url
			url = self.geturl(yyyy,mm,dd)

			# target file inside ziparchive obtained
			date_format = f"{dd}{self.months[int(mm)-1]}{yyyy}"

			# trying to download archive
			try:
			    response = urlopen(url, timeout=2)
			except:
				print(f"No Data Available for date {date_format}")
				continue
			else:
				# create zipf object
				zipf = ZipFile(BytesIO(response.read()))

				# load it as dataframe object
				df = pd.read_csv(zipf.open(f'fo{date_format}bhav.csv', mode = 'r'))
				df['TIMESTAMP'] = pd.to_datetime(df['TIMESTAMP'])
				# name of all the unique stocks
				ar = df["SYMBOL"].unique()

				# loop through each name, query df and finally store in file name 
				for name in ar:
					
					# separate a dataframe based on stock name
					df2 = df.loc[df["SYMBOL"] == name]

					# filename for this particular stock
					filename = os.path.join('data', f'{name}.csv')

					# check if file already exists 
					if (os.path.isfile(filename)):
						print(f'Rewriting {filename}')
						df2.to_csv(filename, mode='a', header=False, index=False)
					else:
						print(f'Created {filename}')
						df2.to_csv(filename, index=False)

		# sort the final data
		self.sort_by_date()

		# finally compress data dir and remove it
		self.compress_data()

	def sort_by_date(self):

		# iterate over all the files in data dir
		for root, dirs, files in os.walk(os.path.join('data', '')):
			for file in files:
				df = pd.read_csv(os.path.join(root, file))
				df = df.sort_values(by='TIMESTAMP')
				df.to_csv(os.path.join(root, file), index=False)


	def compress_data(self):

		# make zip archive from all the files in data dir
		shutil.make_archive('BharvData', 'zip', os.path.join('data', ''))

		# remove data dir
		shutil.rmtree(os.path.join('data',''))


	def geturl(self,yyyy,mm,dd):
		url_bharv = f"https://archives.nseindia.com/content/historical/DERIVATIVES/{yyyy}/{self.months[int(mm)-1]}/fo{dd}{self.months[int(mm)-1]}{yyyy}bhav.csv.zip"
		return url_bharv


d = DataFetcher()
d.BharvFetchFrom("01-04-2022", "05-04-2022")





			


