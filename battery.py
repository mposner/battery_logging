"""
Michael Posner
Windows Battery Status Logging
7/27/14
"""

import subprocess

result = subprocess.check_output(["wmic", "path", "Win32_Battery", "get", "/value"])

result = result.strip()

print "====== Result: "
print result