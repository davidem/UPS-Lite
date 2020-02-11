#!/usr/bin/env python
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
                tmpfile= open("/tmp/ups_lite_capacity.tmp","r")
                if tmpfile.mode == 'r':
                    prev_capacity = tmpfile.read()
                return prev_capacity


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
                capacity = swapped/256

                # Write capacity to tempfile. Needed to determine state.
                tmpfile= open("/tmp/ups_lite_capacity.tmp","w+")
                tmpfile.write(str(capacity))
                tmpfile.close

                return int(capacity)

        def is_battery_full(self,capacity):

                # This function returns True if the battery is full, else return False
                if(capacity == 100):
                        return True
                return False

        def is_battery_low(self,capacity):

                # This function returns True if the battery capacity is low, else return False
                if(capacity <= self.low_capacity):
                        return True
                return False

        def read_status(self,capacity,prev_capacity):

                # This function returns the status of  the battery: low (<20), full (100) or loading/drawing
                if(capacity <= self.low_capacity):
                        status = "LOW"
                elif(capacity >= self.full_capacity):
                        status = "CHARGED"
                elif(prev_capacity >= capacity):
                        status = "CHARGING"
                elif(prev_capacity < capacity):
                        status = "DECHARGING"
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


        # read capacity from tempfile
        ups_lite = UPS()
        prev_capacity = ups_lite.read_prev_capacity()
        voltage = ups_lite.read_voltage()
        capacity = ups_lite.read_capacity()
        # write capacity to tempfile
        is_low = ups_lite.is_battery_low(capacity)
        is_full = ups_lite.is_battery_full(capacity)
        status = ups_lite.read_status(capacity,prev_capacity)
        # compare old and new capacity
        temp = ups_lite.read_temp()

        print "[-] Voltage: %s" % voltage
        print "[-] Capacitiy: %s" % capacity
        print "[-] Status: %s" % status
        print "[-] Temp: %s" % temp

main()
