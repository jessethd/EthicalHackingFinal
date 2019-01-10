# evil-twin

Linux tool in Python that scans all available wireless access points and launches a fake clone of a selected access point, mimicking its ESSID (name) and serving connected clients a local login portal page in an attempt to steal the credentials of the actual network. Provides a tool that facilitates the process of sending deauth packets to said network, disconnecting one or all connected clients and providing them with an opportunity to connect to our fake clone AP. Uses the aircrack-ng suite for target scanning, info gathering, and deauthentication, hostapd to launch the fake access point, dnsmasq to serve as a lightweight DNS and DHCP server for our AP, and Apache to host our local login portal. Group project for CS378 Ethical Hacking course.

Presentation: https://github.com/jthaden/evil-twin/blob/master/Presentation.pdf
Writeup: https://github.com/jthaden/evil-twin/blob/master/Ethical%20Hacking%20Final%20Paper.pdf
