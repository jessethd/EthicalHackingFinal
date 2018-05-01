import subprocess

f = open('/var/www/html/log.txt', 'r')
# Parse log.txt for the first essid, password pair.
line = f.readline().strip('\n')

# credentials[0] contains the essid
# credentials[1] contains the password
credentials = line.split(':')
essid = credentials[0]
password = credentials[1]
print(credentials[0])
print(credentials[1])

# Use nmcli to try connecting to the network with credentials written in log.txt 
subprocess.call(['nmcli', 'd', 'wifi', 'connect', essid, 'password', password])
# Perform an nmap scan from within the network.
# May need to change IP range depending on network.
subprocess.call(['nmap', '-n', '10.202.208.0-255'])


