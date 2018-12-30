# Screen colors to led strip

Clone repository and submodules
```
git clone --recurse-submodules https://github.com/Rifhice/ScreenToLedExtender.git
```
Follow this tutorial to setup hardware and all the dependencies.
https://tutorials-raspberrypi.com/connect-control-raspberry-pi-ws2812-rgb-led-strips/

Command to start the server (to be executed from the folder : rpi_ws281x
```
sudo PYTHONPATH=".:build/lib.linux-armv7l-2.7" python examples/server.py
```

To get the input from a webcam use :
```
python3 webcam.py
```

> Note : needs to change the webcam ID as well as filling out the correct IP adrress for the server and the correct numbers for total count of led, led on the right, led on top and on the left. 

To get the input from the screen :
```
python3 screenRecord.py
```
> Note : needs to fill out the correct IP adrress for the server and the correct numbers for total count of led, led on the right, led on top and on the left. 