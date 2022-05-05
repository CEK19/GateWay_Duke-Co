from random import randrange
import time
from tokenize import Single, single_quoted
import serial
from Adafruit_IO import MQTTClient
import DC_LIB

class IoTSystem:
    __instance = None

    @staticmethod
    def getInstance():
        if IoTSystem.__instance == None:
            IoTSystem(  ADA_FEED_ID=DC_LIB.ADAFRUIT_IO_FEED_ID,
                        ADA_USERNAME=DC_LIB.ADAFRUIT_IO_USERNAME,
                        ADA_KEY_DB=DC_LIB.ADAFRUIT_IO_KEY)
        return IoTSystem.__instance

    def __init__(self, ADA_FEED_ID, ADA_USERNAME, ADA_KEY_DB):
        if IoTSystem.__instance == None:
            self.__ADA_FEED_ID = ADA_FEED_ID
            self.__ADA_USER_NAME = ADA_USERNAME
            self.__ADA_KEY_DB = ADA_KEY_DB
            self.__client = MQTTClient(ADA_USERNAME, ADA_KEY_DB)
            self.__port = "None"
            IoTSystem.__instance = self
    
    def __message(self, client, feed_id, payload):
        FIELD = [k for k, v in DC_LIB.ADAFRUIT_IO_FEED_ID.items() if v == feed_id]
        print("Received Data: " + payload + " from " + FIELD[0])        
        if "CTRL" in FIELD[0]:
            SEND_MESSAGE = "!" + FIELD[0] + ":" + payload + "#"   
            if self.bMicrobitConnected():
                global gSerialPort
                print('SEND MESSAGE: ' + SEND_MESSAGE + ' TO MICROBIT')
                gSerialPort.write(SEND_MESSAGE.encode())
        
    def vConfigSystemAdafruit(self):
        self.__client.on_connect = DC_LIB.connected
        self.__client.on_disconnect = DC_LIB.disconnected
        self.__client.on_message = self.__message
        self.__client.on_subscribe = DC_LIB.subscribe
        self.__client.connect()
        self.__client.loop_background()

    def vSetupPortConnect(self):
        if (DC_LIB.getPort() != "None"):
            print("Port Connected")
            self.__port = serial.Serial(port=DC_LIB.getPort(), baudrate=1152000)
    
    def vPublishData(self, data):
        data = data.replace("!", "") 
        data = data.replace("#", "")
        splitData = data.split(":")
        FIELD_DATA = splitData[0]
        VALUE_DATA = splitData[1]
        if FIELD_DATA in DC_LIB.ADAFRUIT_IO_FEED_ID:
            self.__client.publish(DC_LIB.ADAFRUIT_IO_FEED_ID[FIELD_DATA], VALUE_DATA)
    
    def vReadSerialFromMicrobit(self):
        global gSerialPort
        bytesFormat = gSerialPort.inWaiting()
        if(bytesFormat > 0):
            global gMess
            gMess = gMess + gSerialPort.read(bytesFormat).decode("UTF-8")
            while ("#" in gMess) and ("!" in gMess):
                print(gMess)
                start = gMess.find("!")
                end = gMess.find("#")
                try:
                    self.vPublishData(gMess[start:end + 1])
                except:
                    pass

                if (len(gMess) == end):
                    gMess = ""
                else:
                    gMess = gMess[end + 1:]

    def objGetPort(self):
        return self.__port

    def bMicrobitConnected(self):
        if self.__port != "None":
            return True
        return False

gMess = ""
GateWay = IoTSystem.getInstance()
GateWay.vConfigSystemAdafruit()
GateWay.vSetupPortConnect()
gSerialPort = GateWay.objGetPort()

while True:
    if GateWay.bMicrobitConnected():
        GateWay.vReadSerialFromMicrobit()
