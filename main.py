from network import WLAN,LoRa
import time
import socket
import machine
import pycom
import os

# Switch off heartbeat LED
pycom.heartbeat(False)
# pycom.pybytes_on_boot(False) 
# pycom.smart_config_on_boot(False)
# pycom.wifi_on_boot(True)

# Connect to WiFi
wlan = WLAN(mode=WLAN.STA)
wlan.connect("NUS_STU", auth=(WLAN.WPA2_ENT, 'nusstu\e0575775', '@Jaiguruji7July@'), identity='nusstu\e0575775')
while not wlan.isconnected():
    machine.idle()

# print(wlan.ifconfig())
# Indicate Wifi Connection with red LED
pycom.rgbled(0xFF0000)

time.sleep(1)
rtc = machine.RTC()
rtc.ntp_sync("2.sg.pool.ntp.org",update_period = 3600)

while not rtc.synced():
    machine.idle()
#Indicate Time sync with blue light
pycom.rgbled(0x0000FF)
time.sleep(1)
starting = True

lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868)
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# Set the frequencies and spreading factors for the messages
frequencies = [868000000]
sfs = [7]

freq_sf = [(freq,sf) for freq in frequencies for sf in sfs]

# print(freq_sf)
while True:
    # Send the messages with green light
    i = 0
    num = machine.rng()
    while i<len(freq_sf):
        # if i == 3:
        #     pycom.rgbled(0xFFFF00)
        #     time.sleep(5)
        #     pycom.rgbled(0x000000)
        current_time = rtc.now()
        lora.frequency(freq_sf[i][0])
        lora.sf(freq_sf[i][1])
        # s.send("Hello, Jai Guruji {}".format(num))
        big_buffer = bytes([0x01,0x00,0x00,0x00,0x00,0x00,0x00,0x01,0x01,0x00,0x00,0x00,0x00,0x00,0x00,0x01])
        # big_buffer = bytes([0x00,0x01,0x01,0x01,0x01,0x01,0x01,0x00,0x00,0x01,0x01,0x01,0x01,0x01,0x01,0x00])

        if current_time[5]%15==0:
            print("\n{}/{}/{}-{}:{}:{}:{},{},{},{}".format(current_time[2],current_time[1], current_time[0],current_time[3],current_time[4], current_time[5], current_time[6],num,freq_sf[i][1],freq_sf[i][0]))
            s.send(big_buffer)
            pycom.rgbled(0x00FF00)  
            time.sleep(2)
            pycom.rgbled(0x000000)
        # with open('/flash/test_jgj.txt','a') as f:
        
        # time.sleep(60)
        i+=1
    # time.sleep(2)






#     current_time = rtc.now()
#     if current_time[5]%3==0:


#     starting = False
#     # Print the time with millisecond precision
#     print("{}/{}/{} {}:{}:{}:{}".format(current_time[2],current_time[1], current_time[0],current_time[3],current_time[4], current_time[5], current_time[6]))
    
#     if not rtc.synced():
#         print("Not synced")
#         pycom.rgbled(0x00FFFF)

#     time.sleep(5)


# # pycom.rgbled(0x000000)


# # lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868)
# # s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
# # s.setblocking(False)
# # i = 0
# # pycom.rgbled(0x00FF00)
# # while True:
# #     s.send('Ping')
# #     print('Ping {}'.format(i))
# #     i= i+1
# #     time.sleep(5)