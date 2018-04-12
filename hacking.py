import subprocess
import csv
from threading import Timer
from os import system
import time


subprocess.call(['airmon-ng', 'start', 'wlan0'])
p = subprocess.Popen(["airodump-ng", "wlan0mon", "-w", "output", "--output-format", "csv"])
time.sleep(5)
p.terminate()

#subprocess.call(["airmon-ng", "start", "wlan0"])
#print('Press Ctrl + C to choose an Access Point')
#system('airodump-ng wlan0mon -w output --output-format csv')


with open('output-01.csv', newline='') as f:
    name = ' ' + input("Type in Access Point name: ")
    for row in f:
        line = row.split(',')
        macAddr = ''
        # If you take in some argument here instead of hardcoded AP name
        #name = ' luchador69'
        channel = ''
        if (name in line):
            print(line)
            macAddr = line[0]
            channel = line[3].replace(" ", "")
        print(macAddr)
        print(channel)


