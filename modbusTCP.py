import struct
from threading import Thread
from datetime import datetime
import time

from pyModbusTCP.client import ModbusClient

from model import TagMasterModel, TagModel, DeviceConnectionLog


class ModbusTCP(Thread):

    def __init__(self,DriverDetailID, slavid,client,FrequncyOfGetData,NetworkAddress,Port):
        super(ModbusTCP, self).__init__()
        self.DriverDetailID=DriverDetailID,
        self.slavid = slavid,
        self.client=client
        self.FrequncyOfGetData=FrequncyOfGetData
        self.NetworkAddress=NetworkAddress
        self.Port=Port
        self.SlavID=slavid

    def kelvinToCelsius(self,kelvin):
        return kelvin - 273.15
    def getDataFromRTU(self):


        Isconnect = 0

        while True:

            taglist = TagMasterModel().find_by_DriverDetailID(self.DriverDetailID[0])

            try:

                for tagdata in taglist:
                    print(tagdata)
                    # if(tagdata[8]=='YES'):

                    if(tagdata[5]=='INPUT REGISTER'):

                        client = ModbusClient(host=self.NetworkAddress, port=int(self.Port), unit_id=int(self.SlavID), auto_open=True,
                                              auto_close=True)


                        data = client.read_input_registers(int(tagdata[3]), int(tagdata[4]))


                        packed_string=""
                        # print("data",data)
                        if(tagdata[7]=='NO'):
                            packed_string = struct.pack("HH", data[0], data[1])
                        else:
                            packed_string = struct.pack("HH", data[1], data[0])


                        unpacked_float = struct.unpack("f", packed_string)[0]
                        # print(unpacked_float)
                        now = datetime.now()
                        dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
                        tagvalue=self.kelvinToCelsius(unpacked_float)
                        if(tagdata[9]=='YES'):
                        #     print("yyyyyyy")
                            TagModel().insert(tagdata[0], tagvalue, dt_string)
                            # else:
                            #     Isconnect = 2
                            #     if (self.client.connected==False and Isconnect == 2):
                            #         now = datetime.now()
                            #         dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
                            #         DeviceConnectionLog().insert(self.DriverDetailID[0], self.client.connected,
                            #                                      'disconnect device', dt_string)
                            #         Isconnect = 3
                            #     print(res)
                            #     print("3")
                                # print(self.client.connected)
            except:
            #
            #     if (self.client.connected == False and Isconnect != 3):
            #         now = datetime.now()
            #         dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
            #         DeviceConnectionLog().insert(self.DriverDetailID[0], self.client.connected,
            #                                      'disconnect device', dt_string)
            #         Isconnect = 5
               self.getDataFromRTU()


            time.sleep(self.FrequncyOfGetData)

    def run(self) -> None:

        self.getDataFromRTU()

        # time.sleep(1)








