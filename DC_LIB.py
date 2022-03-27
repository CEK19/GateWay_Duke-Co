import sys
import serial.tools.list_ports

ADAFRUIT_IO_FEED_ID = {
    "CTRL_LOCK": "action-bctrllockstate", ## OK
    "CTRL_FAPP": "action-bnotifyfireapp", 
    "CTRL_FBUZZ": "action-bnotifyfirebuzzer", 
    "CTRL_FRAPP": "action-bnotifyfraudapp", 
    "CTRL_FRBUZZ": "action-bnotifyfraudbuzzer", 
    "VISUAL_WARFIRE": "visual-bwarningfire", 
    "VISUAL_WARFRAUD": "visual-bwarningfraud", 
    "VISUAL_TEMP": "visual-ftemp", ## OK
    "VISUAL_GAS": "visual-igas", ## OK
    "VISUAL_HUMID": "visual-ihumid" ## OK
}

ADAFRUIT_IO_USERNAME = "duke_and_co"
ADAFRUIT_IO_KEY = ""

def connected(client):
    for field in ADAFRUIT_IO_FEED_ID:
        client.subscribe(ADAFRUIT_IO_FEED_ID[field])
        print("Successfully Connected to " + ADAFRUIT_IO_FEED_ID[field])

def subscribe(client, userdata, mid, grandted_qos):
    pass


def disconnected(client):
    print("Disconected")
    sys.exit(1)

def getPort():
    ports = serial.tools.list_ports.comports() 
    N = len(ports)
    commPort = "None"
    for i in range(0, N):
        port = ports[i]
        strPort = str(port)
        if "USB Serial Device" in strPort:
            splitPort = strPort.split(" ")
            commPort = (splitPort[0]) 
    return commPort

