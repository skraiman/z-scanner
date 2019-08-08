# Zscanner
Zscanner is a Python app designed to run on a Raspbeery Pi on a small OLED display.

With Zscanner you can:
* Display all of the IP addresses associated with the network interfaces and the default gateway.
* When a specific network interface is selected:
  * Shows the IP addresses associated with the interface
  * The default gateway, if it is associated with the selected interface.
  * vlan IDs.
  
  
##  Environment
* This app was tested on a Raspberry Pi 3B running the July 10th, 2019 release of Raspbian Buster Lite.
* 3.5 inch OLED display and case.  I used this [display](https://www.amazon.com/gp/product/B07DWSQMKR/ref=ppx_yo_dt_b_asin_title_o01_s00?ie=UTF8&psc=1).  
[This OLED display](https://www.amazon.com/Raspberry-320x480-Monitor-Raspbian-RetroPie/dp/B07N38B86S/ref=sr_1_1?keywords=for+Raspberry+Pi+3+B%2B+3.5+inch+Touch+Screen+with+Case%2C+320x480+Pixel+Monitor+TFT+LCD+Game+Display+%5BSupport+Raspbian%2C+Ubuntu%2C+Kali%2C+RetroPie+System%5D&qid=1565227362&s=electronics&sr=1-1) 
and case looks a bit nicer as the case encloses the display.
* Execute this command `sudo visudo` and modify section around root to look like this:
```
# User privilege specification
root    ALL=(ALL:ALL) ALL
pi      ALL=(root:root) /usr/sbin/tcpdump
```

## Setup
* Clone the repo
* `cd` into the `z-scanner` directory.
* Install the dependencies with this command: ```pip install -r requirements.txt```
* You must run the app from the GUI.  You can do this by clicking on ```Zscanner.py```.  
