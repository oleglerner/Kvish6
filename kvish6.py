"""
Auth: OLEG A
Exp: Download bill files from kvish6 web site
"""

#### IMPORTS ########################################################
import urllib, urllib2, cookielib
from collections import OrderedDict
from config import *
from datetime import date
from datetime import timedelta
from datetime import datetime
import calendar
from Tkinter import *

#### CONSTANTS #####################################################
MONTHS_IN_YEAR = 365/12
FIRST_DAY = 1


#### CODE ###########################################################
"""
Sorry for this auful code! :(
"""

def login(opener, login_data):	
	# Encode to post the data as needed
	form_data = urllib.urlencode(login_data)
	
	# Submit data
	opener.open(URL + LOGIN_PAGE, form_data)

	
def get_to_date():
	today_date = datetime.today()
	
	# To date will be the last day of month
	if today_date.day != calendar.monthrange(today_date.year, today_date.month)[1]:
		to_date = date(today_date.year, today_date.month - 1, calendar.monthrange(today_date.year, today_date.month - 1)[1])
	else:
		to_date = today_date
		
	return to_date
	
def get_from_date(to_date):
	from_date = to_date - timedelta(MONTHS*MONTHS_IN_YEAR)
	
	# From date will be first day of month
	if from_date.day != FIRST_DAY:
		from_date = date(from_date.year, from_date.month + 1, FIRST_DAY)
		
	return from_date

def create_dates(from_date, to_date, num_files):
	# Calculate delta between dates
	delta = (to_date - from_date) / num_files
	one_day_delta = timedelta(1)
	print delta
	
	# First date
	dates = [from_date]
	
	# Make list of dates. we have last date
	for i in xrange(num_files - 1):
		if len(dates) == 1:
			dates.append(dates[len(dates) - 1] + delta)
		else:
			dates.append(dates[len(dates) - 2] + delta)
		
		dates.append(dates[len(dates) - 1] + one_day_delta)
	
	# Last date
	dates.append(to_date)
	
	
	for i in xrange(len(dates)):
		dates[i] = convert_date_to_str(dates[i])
		
	return dates
	
def convert_date_to_str(date):
	# Convert to date to str
	return date.strftime("%d/%m/%Y")
	

def create_filter_page_params(num_files):
	to_date = get_to_date()
	from_date = get_from_date(to_date)
	
	dates = create_dates(from_date, to_date, num_files)	
	print dates
	form_data = []
	
	for i in xrange(0, len(dates), 2):
		print dates[i], dates[i + 1]
		# Ordered dict, test if ordered param will solve filter
		params = OrderedDict([("reportAccCarsRadioSelect", "accNum"), 
		("accounts.value", "all"), 
		("fromDate", dates[i]), 
		("toDate", dates[i + 1]), 
		("sortFields.value", "VehiclePlateNumRep")])	
		
		# Encode to post the data as needed
		form_data.append(urllib.urlencode(params))		
	
	return form_data

		
def download(opener, num_files):
	form_data_list = create_filter_page_params(num_files)
	
	file_index = 0
	for form_data in form_data_list:
		print "filter"
		# Get page after filter
		opener.open(URL + REPORT_FILTER_PAGE, form_data)
		
		# Download the xls file
		resp = opener.open(URL + DOWNLOAD_XLS_PAGE)		
		file_path = r"%s_%s.csv" %(FILE_PATH, file_index)
		write_to_file(file_path, resp.read())
		file_index += 1
	
def download_safe(opener, num_files):
	try:
		download(opener, num_files)
		return True
	except urllib2.HTTPError, ex:		
		print ex
		return False
		
def write_to_file(file_path, data):
	# Write data to file
	file_test = open(file_path, 'wb')
	file_test.write(data)
	file_test.close()

	
def main():
	# Main UI
	labels = []
	text_boxes = []
	root = Tk()
	row_index = 0
	for credential in LOGIN_CREDENTIALS:
		label = Label(root, text=credential)
		label.grid(row = row_index, column = 0)
		labels.append(label)
		
		text_box = Entry(root)
		text_box.grid(row = row_index, column = 1)
		text_boxes.append(text_box)
		
		labels.append(label)
		text_boxes.append(text_box)
		row_index += 1	
	
	submit_button = Button(root, text="Start!", command = lambda: submit(labels, text_boxes, root)).grid(row =  row_index)
	mainloop()
	
	
def submit(labels, text_boxes, root):
	login_credentials = {}
	
	for i in xrange(len(labels) - 1):
		login_credentials[labels[i].cget("text")] = text_boxes[i].get()
		
	root.destroy()
	start(login_credentials)
	
def start(login_data):	
	# Cookie jar
	jar = cookielib.CookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(jar))	
	
	login(opener, login_data)
	
	# Download bill files, May be more than one file
	rv = None
	num_files = 1
	while rv != True:
		rv = download_safe(opener, num_files)
		num_files += 1	

	
if __name__ == "__main__":
	main()