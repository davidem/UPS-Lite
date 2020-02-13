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

        def read_prev_values(self):
                # This function is to read the previous capacity to determing battery Status
                try:
                    with open("/tmp/ups_lite_capacity.tmp","r") as tmpfile:
                        all_values = tmpfile.read()

                        prev_voltage,prev_capacity,prev_status = all_values.split(':')

                except FileNotFoundError:
                        prev_capacity = "1000"
                        prev_voltage = "1000.0001"
                        prev_status = "Too_soon_to_tell"
                return float(prev_voltage),int(prev_capacity),prev_status


        def read_voltage(self):

                # This function returns the voltage as float from the UPS-Lite via SMBus object
                address = 0x36
                read = self.bus.read_word_data(address, 2)
                swapped = struct.unpack("<H", struct.pack(">H", read))[0]
                voltage = swapped * 1.25 /1000/16
                # Write voltage to tempfile. Needed to determine state.
                tmpfile= open("/tmp/ups_lite_capacity.tmp","w+")
                tmpfile.write(str(voltage))
                tmpfile.close
                return voltage


        def read_capacity(self):

                # This function returns the ramaining capacitiy in int as precentage of the battery connect to the UPS-Lite
                address = 0x36
                read = self.bus.read_word_data(address, 4)
                swapped = struct.unpack("<H", struct.pack(">H", read))[0]
                capacity = int(swapped/256)

                # Write capacity to tempfile. Needed to determine state.
                tmpfile= open("/tmp/ups_lite_capacity.tmp","a+")
                tmpfile.write(":")
                tmpfile.write(str(capacity))
                tmpfile.close

                return capacity

        def read_status(self,capacity,prev_capacity,prev_status):

                # This function returns the status of  the battery: # C: low,charged,up/down, V: going up/down
                if(capacity >= self.full_capacity):
                    status = "CHARGED"
                elif(prev_capacity == "1000"):
                    status = "Too_soon_to_tell"
                # low if not charging and below 20 based on voltage, else discharging
                elif(int(prev_capacity) > int(capacity)):
                    if(capacity <= self.low_capacity):
                        status = "LOW"
                    else:
                        status = "DISCHARGING"
                elif(int(prev_capacity) < int(capacity)):
                    status = "CHARGING"
                elif(int(prev_capacity) == int(capacity)):
                    status = prev_status
                else:
                    status = "Too_soon_to_tell"

                # Append status to tmp File
                tmpfile= open("/tmp/ups_lite_capacity.tmp","a+")
                tmpfile.write(":")
                tmpfile.write(str(status))
                tmpfile.close
                return status


        def read_temp(self):
                import os
                stream = os.popen('/opt/vc/bin/vcgencmd measure_temp')
                temp = stream.read()
                bla, temp = temp.split("=",2)
                return temp

def main():

        ups_lite = UPS()
        prev_voltage,prev_capacity,prev_status = ups_lite.read_prev_values()
        voltage = ups_lite.read_voltage()
        capacity = ups_lite.read_capacity()
        status = ups_lite.read_status(capacity,prev_capacity,prev_status)
        temp = ups_lite.read_temp()

        print ("******************************************")
        print ("*        UPS-Lite Status                 *")
        print ("*     for Raspberry Pi Zero              *")
        print ("******************************************")
        print (" ")
        #print " ","- UPS-Lite firmware..........:",fw_version()
        print (" ","- Voltage...........:",voltage)
        print (" ","- Capacity..........:",capacity)
        print (" ","- Status............:",status)
        print (" ","- SOC Temperature...:",temp)
        print ("[-] Voltage: %s" % voltage)
        print ("[-] Capacity: %s" % capacity)
        print ("[-] Status: %s" % status)
        print ("[-] Temp: %s" % temp)

main()
