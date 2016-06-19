#Windows Battery Logging

This script is designed to be run periodically and will gather 
current data on your laptop battery and append it to a file.  If 
scheduled to run every few minutes for an extended period of 
time, it will build up data about your laptop battery charge and
process usage for later analysis.


##Data Collection

###Usage
```
python battery.py [logfile]
```
If no logfile is supplied, current battery info is printed to stdout.

###Details
This script uses the Windows Management Instrumentation Command-line tool (WMIC) to 
request system data from Windows.  Commands are issued as sub-processes and the 
results are parsed and organized.

#####Battery
The following fields are requested using the `Win32_Battery` class:
- **BatteryStatus**: Information about whether the battery is charged, charging, discharging, etc.
- **EstimatedChargeRemaining**: Estimated battery charge [%]
- **EstimatedRunTime**: Estimated battery time remaining based on current usage [min]
- **Status**: Health of the battery

More information on the WMI `Win32_Battery` class can be found at:  
http://msdn.microsoft.com/en-us/library/aa394074(v=vs.85).aspx

#####Processes
The following fields are requested using the `Win32_PerfRawData_PerfProc_Process` class:
- **Name**:  Name of each process
- **PercentProcessorTime**:  Despite its name, this field is not the CPU usage of this process.
In this class, this field contains the total time that the process has run instructions on the CPU.
This time is represented in 100-nanosecond intervals.  Unfortunately this is not a great indicator
of *current* CPU usage, just an indicator of total CPU usage since the process was created.
This seems to be the best I can get from WMI.

**Note**:  There also exists a `Win32_PerfFormattedData_PerfProc_Process` class, as well as several
others.  This class also has a "PercentProcessorTime" field, which actually corresponds to CPU usage,
but when tinkering with this the results seemed inconsistent.  Processes would often report varied
CPU usage when they were in the background the entire time.  The data seemed to be dependent on 
whatever instant you decided to request the data from WMI.  I decided the above class was a slightly
better option.

More information on the `Win32_PerfRawData_PerfProc_Process` class can be found at:
http://msdn.microsoft.com/en-us/library/aa394323(v=vs.85).aspx


###Task Scheduling

Task scheduling on windows can be accomplished by using `Schedule Tasks` in the Control
Panel, or by using `schtasks.exe` on the command line.



##Data Analysis

###Usage
```
python analyze.py [logfile] [outfile]
```

###Example
![Charge v Runtime] (https://github.com/mposner/battery_logging/blob/master/charge_v_runtime.png "Charge v Runtime")

In this graph, the color of the markers represents the age of the data.  The oldest data is in green,
and the newest data is in red.  We can see that, for the same charge level, the average runtime decreases
as the age of the battery increases.


##See Also

For working with more data from Windows, Tim Golden's [WMI Python package](https://pypi.python.org/pypi/WMI/) 
may be more useful

-----------------------

Inspired by http://www.ifweassume.com/2013/08/the-de-evolution-of-my-laptop-battery.html