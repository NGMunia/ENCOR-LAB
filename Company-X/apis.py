from fastapi import FastAPI, status
from jinja2 import Environment, FileSystemLoader
from pydantic import BaseModel
from netmiko import ConnectHandler
from rich import print as rp
from Devices import Routers
import ntc_templates


app = FastAPI()

'''
API that Configures SNMP on the Routers
'''
class snmpclass(BaseModel):
    snmp_server : str
@app.post('/Devices/{Device_ID}/Configure/SNMP',status_code=status.HTTP_201_CREATED)
def snmpconfig(Device_ID: str, post:snmpclass):
    device = Routers[Device_ID]
    conn   = ConnectHandler(**device)
    conn.enable()
    commands = ['ip access-list standard SNMP-SERVER',
                'permit udp host '+post.snmp_server+' '+'eq 161',
                'snmp-server community device_snmp ro SNMP-SERVER',
                'snmp-server system-shutdown',
                'snmp-server enable traps config',
                'snmp-server host '+post.snmp_server+' traps version 2c device_snmp']
    result = conn.send_config_set(commands)
    return result.splitlines()


'''
API that configures NTP on the Routers
'''
class ntpclass(BaseModel):
    ntp_server : str
    template_filepath : str
@app.post('/Devices/{Device_ID}/Configure/NTP',status_code=status.HTTP_201_CREATED)
def snmpconfig(Device_ID: str, post:ntpclass):
    device = Routers[Device_ID]
    conn   = ConnectHandler(**device)
    conn.enable()

    env = Environment(loader=FileSystemLoader(f'{post.filepath}'))
    template = env.get_template('ntp.j2')
    variables = {'ntp_server': post.ntp_server}
    commands = template.render(variables)

    result = conn.send_config_set(commands.splitlines())
    conn.save_config()
    conn.disconnect()
    return result.splitlines()


'''
API that configures NetFlow
'''
class netflowclass(BaseModel):
    flow_server: str
    udp_port : int
    source_intf : str
@app.post('/Devices/{Device_ID}/Configure/NetFlow',status_code=status.HTTP_201_CREATED)
def netflow(Device_ID: str, post:netflowclass):
    device = Routers[Device_ID]
    conn   = ConnectHandler(**device)
    conn.enable()
    commands = ['ip flow-export destination '+post.flow_server+' '+str(post.udp_port),
                'ip flow-export source '+post.source_intf,
                'ip flow-export version 9',
                'ip flow-cache timeout active 1',
                'int '+post.source_intf,
                'ip nbar protocol-discovery',
                'ip flow ingress',
                'ip flow egress',
                'ip flow-top-talkers',
                'top 5',
                'sort-by bytes']
    result = conn.send_config_set(commands)
    return result.splitlines()


'''
API that shows Router Information/Health
'''
@app.get('/Get/Devices/{Device_ID}/Health')
def device_health(Device_ID: str):
    device = Routers[Device_ID]
    conn = ConnectHandler(**device)
    conn.enable()
    command = conn.send_command('show version',use_textfsm=True)
    return command
    

'''
API that verifies DMVPN status on tunnel routers
'''
@app.get('/Get/Devices/Tunnel-Routers/{Device_ID}/DMVPN')
def showdmvpn(Device_ID: str):
    device = Routers[Device_ID]
    conn = ConnectHandler(**device)
    conn.enable()
    command = conn.send_command('show dmvpn',use_textfsm=True)
    return command