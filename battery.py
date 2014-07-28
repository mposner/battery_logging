"""
Michael Posner
Windows Battery Status Logging
7/27/14
"""

import sys
import subprocess
from datetime import datetime

# Check and parse input arguments
if len(sys.argv) > 2:
	usage()
	exit(1)
elif len(sys.argv) == 2:
	logfile = sys.argv[1]
elif len(sys.argv) == 1:
	logfile = ""

# WMIC Win32_Battery fields to query
battery_vars = ['BatteryStatus', 'EstimatedChargeRemaining', 'EstimatedRunTime',
				'Status', 'TimeOnBattery','TimeToFullCharge']

# Start data with timestamp
result = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

for var in battery_vars:

	#execute wmic command and capture output
	temp = subprocess.check_output(["wmic", "path", "Win32_Battery", "get", var, "/value"])	
	
	result += ', ' + temp.strip()
	
# Log data to given file, or stdout if no logfile was provided
result = '[' + result + ']\n'

if logfile == "":
	print result
else:
	with open(logfile, 'a') as f:
		f.write(result)

exit(0)


def usage():
	print "Usage: \n\n" + \
		  "python battery.py [logfile]\n\n" + \
		  "Arguments: \n" + \
		  "    [logfile]    The output file where the data should be appended.\n" + \
		  "                   If no output file is specified, data is printed to stdout."