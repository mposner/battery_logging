"""
Michael Posner
Windows Battery Status Analysis
2/21/2016
"""

import sys
import matplotlib.pyplot as pyplot
from datetime import datetime
from time import mktime

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
    # print [mktime(d.timetuple()) for d in result['dates']]
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
    pyplot.plot_date(result['dates'][i], result['charges'][i], 'o', color=colors[i], markersize=3, markeredgewidth=0.1)

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

# create color data based on the sample date
date_start = mktime(result['dates'][0].timetuple())
date_end = mktime(result['dates'][-1].timetuple())


#print "start: %d, end: %d, diff: %d" % (date_start, date_end, date_end - date_start)
colors = []
for date in result['dates']:
    d = mktime(date.timetuple())
    colors.append(( (d - date_start) / float(date_end-date_start), 
                    1 - (d - date_start) / float(date_end-date_start), 0.3))

# Remove outlier runtime data
charges_cleaned = []
runtimes_cleaned = []
colors_cleaned = []

for i in range(len(result['runtimes'])):
    if result['runtimes'][i] < 24*60:
        charges_cleaned.append(result['charges'][i]) 
        runtimes_cleaned.append(result['runtimes'][i] / 60.0)  # convert runtimes to hours 
        colors_cleaned.append(colors[i])
        
for i in range(len(charges_cleaned)):
    pyplot.plot(charges_cleaned[i], runtimes_cleaned[i], 'o', color=colors_cleaned[i], 
               markersize=3, markeredgewidth=0.1)


pyplot.xlabel('Battery Charge [%]')
pyplot.ylabel('Runtime [hr]')
pyplot.title('Laptop - Windows 7 Estimated Runtime')
pyplot.grid(True)

pyplot.savefig(outfile + "_runtime.png", dpi=500)

pyplot.close(f2)


exit(0)

