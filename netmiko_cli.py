#!/usr/bin/env python3
"""Module docstring."""

import sys
import os
import time
import datetime
import netmiko
import keyring
from netmiko import ConnectHandler
from vchosts import all_devices #Lists of devices and their Credentials
from netmiko.ssh_exception import NetMikoTimeoutException, NetMikoAuthenticationException
from paramiko.ssh_exception import SSHException
from multiprocessing import Pool

keyringPassword = keyring.get_password("label", "user")

def start_commands(a_device, termuser):
    try:
        net_connect = ConnectHandler(**a_device)
        hostname = net_connect.send_command("show hostname")
        output = net_connect.send_command("vpn-sessiondb logoff name {} noconfirm").format(str(termuser))
        print(hostname + " " + output)
        net_connect.disconnect()
    except (NetMikoTimeoutException, NetMikoAuthenticationException) as e:
        print("Could not connect to " + a_device.get("ip") + ", Error: ", e)
        
#Format of Device list:
#cisco_asa = {
#    'device_type': 'cisco_asa',
#    'ip':   '<>',
#    'username': username,
#    'password': password,
#    'port': 22,          # optional, defaults to 22
#    'secret': password,     # optional, defaults to ''
#    'verbose': False,       # optional, defaults to False
#}

def apply_async_with_callback(termuser):
    try:
        with Pool(processes=10) as pool:
            results = [pool.apply_async(start_commands, args = (a_device, termuser)) for a_device in all_devices]
            pool.close()
            pool.join()
    except Exception as e:
        print(e)

# if __name__=='__main__':
#     main()
