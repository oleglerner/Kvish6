from datetime import datetime

# Credentials
LOGIN_CREDENTIALS = ["userName", "idNumber", "password"]

# Web Config
URL = "https://mybill.kvish6.co.il/"
LOGIN_PAGE = "Login.do"
REPORT_FILTER_PAGE = "DrivesDetailsReport.do"
DOWNLOAD_XLS_PAGE = "DrivesDetailsReportShow.do?displayType=XLS"


# Download Config
today_date = datetime.today().strftime("%Y%m%d%H%M%S")

file_name = "%s_bill" %(today_date)
DOWNLOAD_FOLDER = r"C:\temp"

FILE_PATH = r"%s\%s" %(DOWNLOAD_FOLDER, file_name)

# Data
MONTHS = 6