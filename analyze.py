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
          "    [outfile]    Output image file name (without extension)\n"


def parseLog(logfile):
    """
    Reads and parses log data from file,
    
    @param logfile: The filename (including path) of the log file to be parsed.
    
    @return: A dictionary of string to array mappings:
     - 'dates' => A list of datetime objects
     - 'statuses' => A list of integer status values
     - 'charges' => A list of integer charge percentages
     - 'runtimes' => A list of integer runtimes
    """
    
    result = {}
    
    result['dates'] = []
    result['statuses'] = []
    result['charges'] = []
    result['runtimes'] = []
    
    print "Parsing log"
    
    # Read input file
    with open(logfile, 'r') as f:
        
        dataline = f.readline()
        processline = f.readline()
        
        while (dataline):
            
            # Dataline sample:
            # [2016-02-03 20:11:23, BatteryStatus=2, EstimatedChargeRemaining=78, EstimatedRunTime=71582788, Status=OK]
            
            data = dataline.strip("[]\n").split(", ")
            
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

    
def graph_date_v_charge(data):
    """
    Graphs charge data over time.
    
    @param data: Parsed data from log file; output of L{parseLog}
    """
    
    print "Graphing Date v. Charge"
    
    # Build color data based on charge percentage
    colors = []
    for charge in data['charges']:
        
        colors.append((1-charge/100.0, charge/100.0, 0.3))


    f1 = pyplot.figure(1)

    for i in range(len(data['dates'])):
        pyplot.plot_date(data['dates'][i], data['charges'][i], 'o', color=colors[i], 
                         markersize=3, markeredgewidth=0.1)

    pyplot.ylim(0,100)
    pyplot.xlabel('Date')
    pyplot.ylabel('Charge [%]')
    pyplot.title('Laptop Battery Charge')
    pyplot.grid(True)
    pyplot.figure(1).autofmt_xdate()

    pyplot.savefig(outfile + ".png", dpi=500)

    pyplot.close(f1)
    



def graph_charge_v_runtime(data):
    """
    Graphs runtime data over charge, coloring by date of each sample.
    Removes runtimes > 24 hours (outliers that happen when laptop is plugged into AC power)
    
    @param data: Parsed data from log file; output of L{parseLog}
    """
    
    print "Graphing Charge v. Runtime"
    
    f2 = pyplot.figure(2)

    # Create color data based on the sample date
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
        if result['runtimes'][i] < 24*60:  # runtime data is considered bad if it is > 24 hours
            charges_cleaned.append(result['charges'][i]) 
            runtimes_cleaned.append(result['runtimes'][i] / 60.0)  # convert runtimes to hours 
            colors_cleaned.append(colors[i])
            
    for i in range(len(charges_cleaned)):
        pyplot.plot(charges_cleaned[i], runtimes_cleaned[i], 'o', color=colors_cleaned[i], 
                   markersize=2, markeredgewidth=0.1)


    pyplot.xlabel('Battery Charge [%]')
    pyplot.ylabel('Remaining Runtime [hr]')
    pyplot.title('Laptop - Windows 7 Estimated Runtime')
    pyplot.grid(True)

    pyplot.savefig(outfile + "_runtime.png", dpi=500)

    pyplot.close(f2)



    

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

# Graph data: Date vs. Charge
graph_date_v_charge(result)

# Graph data: Charge vs. Runtime
graph_charge_v_runtime(result)


exit(0)

