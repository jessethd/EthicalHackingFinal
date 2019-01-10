# evil-twin

Linux tool in Python that scans all available wireless access points and launches a fake clone of a selected access point, mimicking its ESSID (name) and serving connected clients a local login portal page in an attempt to steal the credentials of the actual network. Provides a tool that facilitates the process of sending deauth packets to said network, disconnecting one or all connected clients and providing them with an opportunity to connect to our fake clone AP. If valid credentials are successfully obtained, a third tool can be used to automatically connect to the targeted access point and perform an internal nmap (network) scan. Uses the aircrack-ng suite for target scanning, info gathering, and deauthentication, hostapd to launch the fake access point, dnsmasq to serve as a lightweight DNS and DHCP server for our AP, Apache to host our local login portal, nmcli to control NetworkManager via command line and connect to the access point with obtained credentials, and finally nmap to perform an internal network scan on the compromised network. Group project for CS378 Ethical Hacking course.

Refer to Section IV of writeup for step-by-step instructions on running this tool.

[Presentation](./Presentation.pdf)

[Writeup](./Ethical%20Hacking%20Final%20Paper.pdf)
