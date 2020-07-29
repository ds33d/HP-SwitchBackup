import requests 
import sys
import time
import datetime
from orionsdk import SwisClient
import getpass
from multiprocessing.dummy import Pool
from netmiko import ConnectHandler


#Ignore SSL Certificate errors
verify = False 
#if not verify:

Switches = [
    '[ip address]',
    '[ip address]',
    '[ip address]'
]
NoSNMP_Public=[
        'no snmp-server community "public"',
        'snmp-server community "enter here" operator',
        'LLDP run',
        'spanning tree',
        'ip default-gateway [enter ip here]',
        'no telnet-server'
    ]

print("We made it to the functions")
print("We are in the function now")
for x in Switches:
    print(x)
    ipaddr = x
    switch_local = {
        'device_type':'hp_procurve',
        'ip':ipaddr,
        'username':'[username]',
        'password':'[password]',
        'port':'22'
        }   
    try:
        switch_connection = ConnectHandler(**switch_local)
        print("Connected to " + ipaddr)
        #Save config now in case of any previous changes
        switch_connection.send_command('write memory')
        ad_auth_connection = ConnectHandler(**switch_local)
        TestOutput = switch_connection.send_command("show run")
        if 'snmp-server community "public"' not in TestOutput:
            #It worked, clean up and save
            print("Public SNMP not found")
            ad_auth_connection.send_command('write memory')
            ad_auth_connection.disconnect()
            switch_connection.disconnect()
            switch_connection.disconnect()
            print("Disconnecting from " + ipaddr)
            print ("-------------------------")
        else:
            #Send configuration for SNMP
            output=None
            output = switch_connection.send_config_set(NoSNMP_Public)
            print(output)
            output = None
            #Test settings so we don't get locked out
            #SNMP Local found

    except:
        print("Unknown failure")
        ipaddr = ""
        exit
    output = None
    print ("-------------------------")
    
