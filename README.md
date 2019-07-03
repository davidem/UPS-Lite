# UPS-Lite

I like the (rewritten) script a lot, but it doesn't give much information. I also have a rpi 3b+ with a PiCO UPS, for which a nice python-script is written with lots of useful information. This is my attempt to add some features to UPS-Lite.py... And any help is welcome :)

Please note that I'm not a seasoned developer / debugger and this is an ongoing quest, 

## Wishlist... 
as said: I'm spoiled with the output of pico_status.py:
![alt text](https://github.com/Siewert308SW/pico_status/blob/master/pico_status.png "pico_status.py output")

Stuff on my wishlist: 
- Powering mode
- Charge state
- Temperature

## i2c & UPS-Lite
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
i2cdetect shows that only one chip-address is accessible. 

```
i2cdump -y 1 0x36
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00: ff ff b5 20 23 0f 00 00 00 02 ff ff 97 00 ff ff
10: ff ff ff ff fb fa ff ff ff ff ff ff ff ff ff ff
30: ff ff ff ff ff ff ff ff ff ff ff ff ff ff 00 00
```
i2cdump shows several data-addresses, of which currently only 0x02 (Voltage) and 0x04 (Capacity) are used. So... main question is: what does the rest do? 

Not much information to be found, but Max17040.pdf offers an interesting table:
![alt text](images/Max17040_registry.png "Max17040 registry table")




