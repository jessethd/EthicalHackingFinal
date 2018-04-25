import subprocess

f = open('/var/www/html/log.txt', 'r')
# Get first line. Remove possible newlines from end
line = f.readline().strip('\n')

# credentials[0] contains the essid
# credentials[1] contains the password
credentials = line.split(':')
essid = credentials[0]
password = credentials[1]
print(credentials[0])
print(credentials[1])

subprocess.call(['nmcli', 'd', 'wifi', 'connect', essid, 'password', password])
# May need to change IP range depending on network.
subprocess.call(['nmap', '-n', '10.202.208.0-255'])


