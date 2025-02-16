from channels.generic.websocket import AsyncWebsocketConsumer
import json, time
from pysnmp.hlapi import *

def check_device_status(ip):
    """Checks if a device is up or down using SNMP"""
    result = next(getCmd(SnmpEngine(), CommunityData('public', mpModel=0),
                         UdpTransportTarget((ip, 161)), ContextData(),
                         ObjectType(ObjectIdentity('1.3.6.1.2.1.1.3.0'))))
    return result[3] if result[0] is None else 'Down'

class NetworkMonitorConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        while True:
            device_status = check_device_status("192.168.1.1")
            await self.send(text_data=json.dumps({'device_status': device_status}))
            time.sleep(5)
