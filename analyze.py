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
          "python analysis.py [logfile] [outfile]\n\n" + \
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
            
            result['dates'].append(data[0])
            result['statuses'].append(data[1].split("=")[1])
            result['charges'].append(data[2].split("=")[1])
            result['runtimes'].append(data[3].split("=")[1])
            
            dataline = f.readline()
            processline = f.readline()
        
    
    
    print "DATES:\n"
    print result['dates']
    print "STATUSES:\n"
    print result['statuses']
    print "CHARGES:\n"
    print result['charges']
    print "RUNTIMES:\n"
    print result['runtimes']
    
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
    charge = int(charge)
    
    colors.append((1-charge/100.0, charge/100.0, 0.3))


# Convert date data into usable numbers
floatdates = [datetime.strptime(x, DATE_FORMAT) for x in result['dates']]

# Graph data
pyplot.figure(1)

for i in range(len(floatdates)):
    pyplot.plot_date(floatdates[i], result['charges'][i], 'o', color=colors[i], markersize=4, markeredgewidth=0.1)

pyplot.ylim(0,100)
pyplot.xlabel('Date')
pyplot.ylabel('Charge')
pyplot.title('Laptop Battery Charge')
pyplot.grid(True)
pyplot.figure(1).autofmt_xdate()

pyplot.savefig(outfile, dpi=500)


exit(0)

