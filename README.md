# UPS-Lite

I like the (rewritten) script a lot, but it doesn't give much information. I also have a rpi 3b+ with a PiCO UPS, for which a nice python-script is written with lots of useful information. This is my attempt to add some features to UPS-Lite.py... :)

## Information I like to have... 
as said: I'm spoiled with the output of pico_status.py:
![alt text](https://github.com/Siewert308SW/pico_status/blob/master/pico_status.png "pico_status.py output")

Stuff on my wishlist: 
- Powering mode
- Charge state
- Temperature

## i2c & UPS-Lite
```i2cdetect -y 1
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- -- 
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
30: -- -- -- -- -- -- 36 -- -- -- -- -- -- -- -- -- 
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
70: -- -- -- -- -- -- -- --```



Not much information to be found, but Max17040.pdf offers an interesting table:
![alt text](images/Max17040_registry.png "Max17040 registry table")


