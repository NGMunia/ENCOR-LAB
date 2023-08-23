
from netmiko import ConnectHandler
from rich import print as rp
from Devices import Routers
import ntc_templates

'''
Backing up Running configurations
'''
filepath = input('File storage location: ')
for devices in Routers.values():
    conn = ConnectHandler(**devices)
    conn.enable()
    
    hostname = conn.send_command('show version',use_textfsm=True)[0]['hostname']
    output   = conn.send_command('show running-config')

    with open(f'{filepath}/{hostname}','w') as f:
        f.write(output)
        conn.disconnect()
    rp(f'[cyan] Host {hostname} backup successful!')
