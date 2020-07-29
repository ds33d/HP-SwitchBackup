import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import os
import json
import sys
from orionsdk import SwisClient
import getpass
from netmiko import ConnectHandler

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

#Connection Settings, prompt for username/password
npm_server = '[orion server ip]'
username = getpass.getuser()
password = getpass.getpass("Password for {0}:".format(username), stream=None)

#connection setttings for switches, prompt
switchUser = input("Enter usename for switch access:")
switchPass = getpass.getpass()

#connect to SWIS
swis = SwisClient(npm_server, username, password)

results = swis.query(
"""SELECT NodeID, Caption, IPAddress, Status, Description
FROM Orion.Nodes
WHERE Caption like '%[Switch Name]%'
AND ((Description like '%Procurve%') or (Description like '%HP%') or (Description like '%Aruba%'))
"""

)

commandsTFTP =[
    'copy tftp flash [ip address] [firmware]',
    'y',
    'reboot',
    'y'
]
x = 0

for key,val in results.items():
    for e in val:
        
        #find ip address from results
        ipAddress=e['IPAddress']
        ipHostname=e['Caption']
        ipDescription=e['Description']
        print(ipHostname,"-",ipDescription,"-",ipAddress)

        #switch settings
        switch = {
        'device_type':'hp_procurve',
        'ip':ipAddress,
        'username':switchUser,
        'password':switchPass,
        'port':'22'
         }
        try:
                #connect to switch with settings from above
                print("Connecting to switch...")
                switch_connection = ConnectHandler(**switch)

                #find switch prompt KD-SW
                print("Finding switch prompt...")
                output = switch_connection.find_prompt()
                print(output)

                #send show version command
                print("Getting switch version...")
                version = switch_connection.send_command("show version")

                if "[firmware]" in version:
                        print(ipHostname,"- Firmware is up-to-date.")

                        #disconnect from switch
                        print("Disconnecting from:", ipHostname, "-",ipAddress)
                        switch_connection.disconnect()

                        print("-------------------------------------------")
                        print("\n")

                

                else:
                        #display current switch version as it is not up to date
                        print(version)
                        print(ipHostname," is not up to date.")

                        #determine if switch is a 2530
                        if "2530" in ipDescription:
                                print("Switch is a 2530")
                                print(ipDescription)
                                print("Sending commands and rebooting...")
                                output = switch_connection.send_config_set(commandsTFTP)
                                print(output)
                                print("TFTP Command Successful...")
                        
                        else:
                                #disconnect from switch
                                print("Switch is NOT 2530")
                                print("Disconnecting from: ", ipHostname, "-",ipAddress)
                                switch_connection.disconnect()
        
        except:
                print("!!!-ERROR-!!!")
        
        
        x=x+1


print(x)
    
