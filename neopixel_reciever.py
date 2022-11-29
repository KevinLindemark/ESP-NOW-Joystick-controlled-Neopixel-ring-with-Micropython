import network
import espnow
import ubinascii
from machine import Pin, unique_id
from neopixel import NeoPixel

print("MAC ADDRESS OF THIS DEVICE IS:",ubinascii.hexlify(unique_id(), ":").decode().upper())
sta = network.WLAN(network.STA_IF) # A WLAN interface must be active to send()/recv()
sta.active(True)
e = espnow.ESPNow()
e.active(True)
peer = b'\xbb\xbb\xbb\xbb\xbb\xbb'   # MAC address of peer's wifi interface
e.add_peer(peer)
np = NeoPixel(Pin(4), 12) # Neopixel object

def set_pixel(pixel, r, g, b):
    for i in range(12):
        np[i] = (0,0,0)
    np[pixel] = (r, g, b)
    np.write()
    
def convert_to_list(data_string):
    data_string = msg.decode('utf-8')
    data_list = data_string.split(",")
    for i in range(0, len(data_list)):
        data_list[i] = int(data_list[i])
    return data_list

button_status = True
presses = 0
while True:
    host, msg = e.recv()
    if msg:             # msg == None if timeout in recv()
        data_list = convert_to_list(msg)
        print(data_list)
        if data_list[2] == False and button_status == True:
            print(f"Button pressed {presses} times, and button status is {button_status}")
            presses +=1
        button_status = data_list[2]        
        if data_list[0] < 1500:
            set_pixel(6, 0,abs(round((data_list[0] -2048) /8)+1),0)
            print(abs(round((data_list[0] -2048) /8)+1))
            print("UP")
        elif data_list[0] > 2000:
            set_pixel(0, 0,abs(round((data_list[0] -2048) /8)-1),0)
            print(abs(round((data_list[0] -2048) /8)-1))
            print("DOWN")
        elif data_list[1] < 1500:
            set_pixel(3, abs(round((data_list[1] -2048) /8)+1),0,0)
            print(abs(round((data_list[1] -2048) /8)+1))
            print("LEFT")
        elif data_list[1] > 2000:
            set_pixel(9, abs(round((data_list[1] -2048) /8)-1) ,0,0)
            print(abs(round((data_list[1] -2048) /8)-1))
            print("RIGHT")
            
        else:
            set_pixel(0, 0,0,0)
                  