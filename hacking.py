import subprocess
import csv
from threading import Timer

kill = lambda process: process.kill()

subprocess.call(["airmon-ng", "start", "wlan0"])

cmd = ['airodump-ng', 'wlan0mon', '-w', 'output', '--output-format', 'csv']
try:
	subprocess.run(cmd, timeout=5)
except subprocess.TimeoutExpired:
	pass

#subprocess.call(['cat', 'output-01.csv'])

with open("output-01.csv") as f:
	for line in f:
		if "CS378-EthicalHacking-GDC-2.212" in line:
			print (line)


