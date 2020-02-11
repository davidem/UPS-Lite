#!/usr/bin/env python3
import os
import struct
import smbus
import sys
import time

class UPS():

        def __init__(self):

                # Set the bus port either 1 or 0
                self.bus = smbus.SMBus(1)
                # set low capacity alert for the battery
                self.low_capacity = 20
                self.full_capacity = 99

        def read_prev_capacity(self):
                # This function is to read the previous capacity to determing battery Status
                try:
                    with open("/tmp/ups_lite_capacity.tmp","r") as tmpfile:
                        prev_capacity = tmpfile.read()
                except FileNotFoundError:
                        prev_capacity = "1000"
                return int(prev_capacity)


        def read_voltage(self):

                # This function returns the voltage as float from the UPS-Lite via SMBus object
                address = 0x36
                read = self.bus.read_word_data(address, 2)
                swapped = struct.unpack("<H", struct.pack(">H", read))[0]
                voltage = swapped * 1.25 /1000/16
                return voltage


        def read_capacity(self):

                # This function returns the ramaining capacitiy in int as precentage of the battery connect to the UPS-Lite
                address = 0x36
                read = self.bus.read_word_data(address, 4)
                swapped = struct.unpack("<H", struct.pack(">H", read))[0]
                capacity = int(swapped/256)

                # Write capacity to tempfile. Needed to determine state.
                tmpfile= open("/tmp/ups_lite_capacity.tmp","w+")
                tmpfile.write(str(capacity))
                tmpfile.close

                return capacity

        def read_status(self,capacity,prev_capacity):

                # This function returns the status of  the battery: low (<20), full (100) or loading/drawing
                if(capacity <= self.low_capacity):
                        status = "LOW"
                elif(capacity >= self.full_capacity):
                        status = "CHARGED"
                elif(prev_capacity == "1000"):
                        status = "Too soon too tell"
                elif(int(prev_capacity) > int(capacity)):
                        status = "DECHARGING"
                elif(int(prev_capacity) < int(capacity)):
                        status = "CHARGING"
                else:
                        status = "Too soon too tell"
                return status

        def read_temp(self):
                import os
                stream = os.popen('/opt/vc/bin/vcgencmd measure_temp')
                temp = stream.read()
                bla, temp = temp.split("=",2)
                return temp

def main():

        ups_lite = UPS()
        prev_capacity = ups_lite.read_prev_capacity()
        voltage = ups_lite.read_voltage()
        capacity = ups_lite.read_capacity()
        status = ups_lite.read_status(capacity,prev_capacity)
        temp = ups_lite.read_temp()

        print ("[-] Voltage: %s" % voltage)
        print ("[-] Capacity: %s" % capacity)
        print ("[-] Status: %s" % status)
        print ("[-] Temp: %s" % temp)

main()
