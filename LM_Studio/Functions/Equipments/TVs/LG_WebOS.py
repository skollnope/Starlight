from pywebostv.discovery import *    # Because I'm lazy, don't do this.
from pywebostv.connection import *
from pywebostv.controls import *


store = {}
# Scans the current network to discover TV. Avoid [0] in real code. If you already know the IP,
# you could skip the slow scan and # instead simply say:
#    client = WebOSClient("<IP Address of TV>")
# or for newer models:
#    client = WebOSClient("<IP Address of TV>", secure=True)
client = WebOSClient.discover()[0] # Use discover(secure=True) for newer models.
client.connect()
for status in client.register(store):
    if status == WebOSClient.PROMPTED:
        print("Please accept the connect on the TV!")
    elif status == WebOSClient.REGISTERED:
        print("Registration successful!")