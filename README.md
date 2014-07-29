Windows Battery Logging
=======================

This script is designed to be run periodically and will gather 
current data on your laptop battery and append it to a file.

##Usage
```
python batery.py [logfile]
```

##Task Scheduling

Task scheduling on windows can be accomplished by using `Schedule Tasks` in the Control
Panel, or by using `schtasks.exe` on the command line.

##See Also

Information on the WMI Win32_Battery class and the units of its properties can
be found at:  http://msdn.microsoft.com/en-us/library/aa394074(v=vs.85).aspx

For working with more data from Windows, Tim Golden's [WMI Python package](https://pypi.python.org/pypi/WMI/) 

-----------------------

Inspired by http://www.ifweassume.com/2013/08/the-de-evolution-of-my-laptop-battery.html