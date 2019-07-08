# UPS-Lite

I like the (rewritten) script a lot, but it doesn't give much information. I also have a rpi 3b+ with a PiCO UPS, for which a nice python-script is written with lots of useful information. This is my attempt to add some features to UPS-Lite.py... And any help is welcome :)

Please note that I'm not a seasoned developer / debugger and this is work in progress... ;)

## Wishlist... 
as said: I'm spoiled with the output of [pico_status.py](https://github.com/Siewert308SW/pico_status):
![alt text](https://github.com/Siewert308SW/pico_status/blob/master/pico_status.png "pico_status.py output")

Stuff on my wishlist: 
- Powering mode
- Charge state
- Temperature

## i2c & UPS-Lite
i2cdetect shows that only one chip-address is accessible:

```
i2cdetect -y 1
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- -- 
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
30: -- -- -- -- -- -- 36 -- -- -- -- -- -- -- -- -- 
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
70: -- -- -- -- -- -- -- --
```

i2cdump shows several data-addresses, of which currently only 0x02 (Voltage) and 0x04 (Capacity) are used in the current script. 
```
i2cdump -y 1 0x36
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00: ff ff b5 20 23 0f 00 00 00 02 ff ff 97 00 ff ff
10: ff ff ff ff fb fa ff ff ff ff ff ff ff ff ff ff
30: ff ff ff ff ff ff ff ff ff ff ff ff ff ff 00 00
```
 So... main question is: what does the rest do? 

Not much information is to be found, but Max17040.pdf offers an interesting table:
![alt text](images/Max17040_registry.png "Max17040 registry table")

The downside is that it only covers 0x00 - 0x0d and 0xfe - 0xff, and the text states that all remaining addresses are reserved and undefined... 


| data address | Function | Remark  | byte Value | word Value
| ------------- |-------------|-------|-------|-------|
| 0x00 | - | - |ff|0xffff |
| 0x01 | - | - |ff|fluctuates |
| 0x02 | VCELL | Used for Voltage calculation | fluctuates  | fluctuates |
| 0x03 | VCELL | - | fluctuates| fluctuates |
| 0x04 | SOC | Used for State of charge | fluctuates |fluctuates |
| 0x05 | SOC | - |fluctuates |fluctuates |
| 0x06 | MODE | - |00 | 0x0000 |
| 0x07 | MODE | - |00 | 0x0000 |
| 0x08 | VERSION | - |00 | 0x0200 |
| 0x09 | VERSION | - |02 | 0xff02 |
| 0x0a | - | - |ff | 0xffff | 
| 0x0b | - | - |ff | 0x97ff |
| 0x0c | RCOMP | - |97 | 0x0097 | 
| 0x0d | RCOMP | - |00 | 0xff00 |
| 0x0e | - | - |ff | 0xffff |
| 0x0f | - | - |ff | 0xffff |
| 0x14 | - |Another kind of charge state counter | fluctuates | fluctuates |
| 0x15 | - | - |fluctuates   | fluctuates |
| 0x3e | - | - |00 | 0x0000 |
| 0x3f | - | - |00 | 0xff00 |







## Powering Mode
I'm looking for a simple way to check if the pi is running on battery or not. From the current 2 outputs from the script (voltage and capacity) I can't determine the source of power. 

My first idea was to take a closer look at 0x14, but it turned out to be another kind of state counter. Then I noticed address 0x01, which in some specific states it has a specific (fixed) value: 

| Value (hex) | Value (dec) | Possible State  | Remarks |
| ------------- |-------------|-------|-------|
| 0xd0ff |  | power > accu? | | 
| 0xcfff |  | decharging ?  | | 
| 0xd0ff |  | decharging ?  | | 
| 0xd2ff |  | charging | | 
| 0xd1ff |  | charged / checking?  | when battery <= 98%  |
| 0xd2ff |  | charging  | | 
| 0xd1ff |  | charged  | when Battery => 98% |


## Charge state

## Temperature
Not sure if this is possible on a zero, but I'll give it a try...






