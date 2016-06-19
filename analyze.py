"""
Michael Posner
Windows Battery Status Analysis
2/21/2016
"""

import sys
import matplotlib.pyplot as pyplot
from datetime import datetime

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

def usage():
    print "Usage: \n\n" + \
          "python analyze.py [logfile] [outfile]\n\n" + \
          "Arguments: \n" + \
          "    [logfile]    Input file with data written by battery.py\n" + \
          "    [outfile]    Output image file name\n"


def parseLog(logfile):
    """Reads and parses log data from file"""
    
    result = {}
    
    result['dates'] = []
    result['statuses'] = []
    result['charges'] = []
    result['runtimes'] = []
    
    
    # Read input file
    with open(logfile, 'r') as f:
        
        dataline = f.readline()
        processline = f.readline()
        
        while (dataline):
            
            # Dataline sample:
            # [2016-02-03 20:11:23, BatteryStatus=2, EstimatedChargeRemaining=78, EstimatedRunTime=71582788, Status=OK]
            
            data = dataline.strip("[]\n").split(", ")
            
            #print data;
            
            # Parse Date
            floatdate = datetime.strptime(data[0], DATE_FORMAT)  #convert date string into datetime object
            result['dates'].append(floatdate)
            
            # Parse Battery Status
            strstatus = data[1].split("=")[1]
            result['statuses'].append(int(strstatus))
            
            # Parse Charge
            strcharge = data[2].split("=")[1]
            result['charges'].append(int(strcharge))
            
            # Parse Runtime
            strruntime = data[3].split("=")[1]
            result['runtimes'].append(int(strruntime))
            
            dataline = f.readline()
            processline = f.readline()
        
    
    
    # print "DATES:\n"
    # print result['dates']
    # print "\nSTATUSES:\n"
    # print result['statuses']
    # print "\nCHARGES:\n"
    # print result['charges']
    # print "\nRUNTIMES:\n"
    # print result['runtimes']
    
    return result

    
# ======  MAIN  ======


# Check and parse input arguments
if len(sys.argv) == 3:
    logfile = sys.argv[1]
    outfile = sys.argv[2]
else:   
    usage()
    exit(1)

# Parse log data
result = parseLog(logfile)

colors = []
for charge in result['charges']:
    
    colors.append((1-charge/100.0, charge/100.0, 0.3))


# Graph data: Date vs. Charge
f1 = pyplot.figure(1)

for i in range(len(result['dates'])):
    pyplot.plot_date(result['dates'][i], result['charges'][i], 'o', color=colors[i], markersize=4, markeredgewidth=0.1)

pyplot.ylim(0,100)
pyplot.xlabel('Date')
pyplot.ylabel('Charge [%]')
pyplot.title('Laptop Battery Charge')
pyplot.grid(True)
pyplot.figure(1).autofmt_xdate()

pyplot.savefig(outfile, dpi=500)

pyplot.close(f1)


# Graph data: Charge vs. Runtime
f2 = pyplot.figure(2)

# Remove outlier runtime data
charges_cleaned = []
runtimes_cleaned = []
for i in range(len(result['runtimes'])):
    if result['runtimes'][i] < 1000000:
        charges_cleaned.append(result['charges'][i]) 
        runtimes_cleaned.append(result['runtimes'][i] / 60.0)  # convert runtimes to hours 

pyplot.plot(charges_cleaned, runtimes_cleaned, 'o', markersize=4, markeredgewidth=0.1)

#pyplot.ylim(0,200)
pyplot.xlabel('Battery Charge [%]')
pyplot.ylabel('Runtime [hr]')
pyplot.title('Laptop - Windows 7 Estimated Runtime')
pyplot.grid(True)

pyplot.savefig(outfile + "_runtime.png", dpi=500)

pyplot.close(f2)


exit(0)

