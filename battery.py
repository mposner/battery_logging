"""
Michael Posner
Windows Battery Status Logging
7/27/14
"""

import subprocess

battery_vars = ['BatteryStatus', 'EstimatedChargeRemaining', 'EstimatedRunTime',
				'Status', 'TimeOnBattery','TimeToFullCharge']

result = ""
				
for var in battery_vars:			
	temp = subprocess.check_output(["wmic", "path", "Win32_Battery", "get", var, 
									   "/value"])	
	result += ' ' + temp.strip()
	
print "====== Result: "
print result