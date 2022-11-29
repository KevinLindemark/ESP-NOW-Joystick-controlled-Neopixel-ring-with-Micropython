import network
import espnow
import ubinascii
from machine import ADC, Pin, unique_id
from time import sleep
x = Pin(35)  
y = Pin(34)
btn = Pin(4)
x_joy = ADC(x)        # create an ADC object acting on a pin
y_joy = ADC(y)        # create an ADC object acting on a pin
x_joy.atten(ADC.ATTN_11DB)
x_joy.width(ADC.WIDTH_12BIT)
y_joy.atten(ADC.ATTN_11DB)
y_joy.width(ADC.WIDTH_12BIT)


print("MAC ADDRESS OF THIS DEVICE IS:", ubinascii.hexlify(unique_id()).decode())

# A WLAN interface must be active to send()/recv()
sta = network.WLAN(network.STA_IF)  # Or network.AP_IF
sta.active(True)
e = espnow.ESPNow()
e.active(True)
peer = b'\xaa\xaa\xaa\xaa\xaa\xaa'   # MAC address of peer's wifi interface
e.add_peer(peer)
while True:
    x_val_raw = x_joy.read()  # read a raw analog value in the range 0-4095
    y_val_raw = y_joy.read()  # read a raw analog value in the range 0-4095
    btn_val = btn.value()
    print(f"x {x_val_raw} y {y_val_raw} btn {btn_val}")
    values = f"{x_val_raw},{y_val_raw},{btn_val}"
    e.send(peer, values)
    sleep(0.1)
    
