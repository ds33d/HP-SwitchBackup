import requests
import os
import colorama 
import sys
import time
import datetime
from orionsdk import SwisClient
import getpass
from multiprocessing.dummy import Pool
from netmiko import ConnectHandler
from colorama import Fore, Back, Style

colorama.init()
verify = False

x=39

while x<=240:
    #Set progress and show
    progress = x/240
    progress = progress * 100
    print(Fore.GREEN + 'Percent completed:',progress)
    print(Fore.WHITE)

    #set login information
    ipAddress="192.168.1."+str(x)
    switch_local = {
    'device_type':'hp_procurve',
    'ip':ipAddress,
    'username':'[username]',
    'password':'[password]',
    'port':'22'
    }
    print(ipAddress)
    hostname =""
    try:
        #ping system to see if its up
        print("Ping IP to verify connectivity...")
        response = os.system("ping -n 1 " + ipAddress)
        if response == 1:
            print(Fore.RED+"Unable to ping to:",ipAddress)
        else:
            print(Fore.GREEN+"Successful ping to:",ipAddress)
            print(Fore.WHITE)
            switch_connection = ConnectHandler(**switch_local)
            print("Connected to " + ipAddress)
            #Save config now in case of any previous changes
            switch_connection.send_command('write memory')
            local_auth_connection = ConnectHandler(**switch_local)
            output = switch_connection.send_command("show run")
            hostname = local_auth_connection.find_prompt()
            print(hostname)
            #Create file for saving the config to
            print("Creating file...")
            fileName = open("%s.txt" % hostname,"w")
            print("Writing config to file...")
            #Write output to file
            fileName.write(output)
            print("Closing file...")
            fileName.close()
            #Close connection from switch
            local_auth_connection.disconnect()
            switch_connection.disconnect()
            switch_connection.disconnect()
            print("Disconnecting from " + ipAddress)
            print ("-----------------------------------")
            hostname=""
    except:
        print(Fore.RED + "!!!!!!!ERROR!!!!!!!")
        print("Problem with:",hostname," - ",ipAddress)
        print ("-----------------------------------")
    x=x+1
