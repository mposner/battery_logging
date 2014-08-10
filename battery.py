"""
Michael Posner
Windows Battery Status Logging
7/27/14
"""

import sys
import subprocess
from datetime import datetime



def usage():
	print "Usage: \n\n" + \
		  "python battery.py [logfile]\n\n" + \
		  "Arguments: \n" + \
		  "    [logfile]    The output file where the data should be appended.\n" + \
		  "                   If no output file is specified, data is printed to stdout."



def getProcessInfo():
	"""Gets info on the top running processes"""
	
	#execute wmic command and capture output
	temp = subprocess.check_output(["wmic", "path", "Win32_PerfFormattedData_PerfProc_Process", "get", 
		"ElapsedTime,Name,PercentProcessorTime"])	
	
	#iterate over process and split into lists
	firstline = True
	result = []  #list of lists to contain the final result
		
	for line in temp.splitlines():
		if(firstline):
			firstline = False
			continue
		elif not line:  #skip empty lines
			continue
		
		proclist = line.split()  #split on whitespace to return a 3 element list
		
		if (proclist[1] != "_Total"):  #dont append empty lists or the "_Total" process
			result.append(proclist)
		
	# narrow process list down
	times = [int(x[2]) for x in result]
	times.sort()
	times.reverse()
	
	print "TIMES:", times
	
	print "10%:", len(times)/10
	
	nonzero = [x for x in times if x]
	
	ind = min(len(times)/10,len(nonzero))  #reduce processes to top 10% or to all with nonzero cpu time
	times = times[:ind]
	cutoff = max(times[-1],1)
	
	print "CUTOFF:", cutoff
	
	return [x for x in result if int(x[2]) >= cutoff]


	
# ======  MAIN  ======


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
				'Status']

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
	print getProcessInfo()
else:
	with open(logfile, 'a') as f:
		f.write(result)

exit(0)


