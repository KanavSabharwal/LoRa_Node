from network import WLAN,LoRa
import time
import socket
import machine
import pycom
import os

# Switch off heartbeat LED
pycom.heartbeat(False)

# Indicate Wifi Connection with red LED
pycom.rgbled(0xFF0000)
time.sleep(1)
pycom.rgbled(0x000000)

wlan = WLAN(mode=WLAN.STA)
nets = wlan.scan()
for net in nets:
    if net.ssid == 'NUS_STU':
        print('Network found!',net)
        # wlan.connect(net.ssid, auth=(net.sec, 'cirlab@123'))
        wlan.connect(net.ssid, auth=(net.sec, 'nusstu\e0575775', '@Jaiguruji160407@'), identity='nusstu\e0575775')
        while not wlan.isconnected():
            pass
        print('WLAN connection succeeded!')
        break

pycom.rgbled(0xFFFF00)

rtc = machine.RTC()
rtc.ntp_sync("0.ubuntu.pool.ntp.org",update_period = 3600)

while not rtc.synced():
    pass

#Indicate Time sync with blue light
pycom.rgbled(0x0000FF)
time.sleep(1)
starting = True

lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868,power_mode = LoRa.TX_ONLY, bandwidth = LoRa.BW_125KHZ)

if lora.power_mode()==LoRa.TX_ONLY:
    pycom.rgbled(0xFFFF00)
    time.sleep(1)

pycom.rgbled(0x000000)
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# Set the frequencies and spreading factors for the messages

hex_values = [0x0, 0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8,
       0x9, 0xa, 0xb, 0xc, 0xd, 0xe, 0xf, 0x10, 0x11,
       0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19,
       0x1a, 0x1b, 0x1c, 0x1d, 0x1e, 0x1f, 0x20, 0x21,
       0x22, 0x23, 0x24, 0x25, 0x26, 0x27, 0x28, 0x29,
       0x2a, 0x2b, 0x2c, 0x2d, 0x2e, 0x2f, 0x30, 0x31,
       0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39,
       0x3a, 0x3b, 0x3c, 0x3d, 0x3e, 0x3f, 0x40, 0x41,
       0x42, 0x43, 0x44, 0x45, 0x46, 0x47, 0x48, 0x49,
       0x4a, 0x4b, 0x4c, 0x4d, 0x4e, 0x4f, 0x50, 0x51,
       0x52, 0x53, 0x54, 0x55, 0x56, 0x57, 0x58, 0x59,
       0x5a, 0x5b, 0x5c, 0x5d, 0x5e, 0x5f, 0x60, 0x61,
       0x62, 0x63, 0x64, 0x65, 0x66, 0x67, 0x68, 0x69,
       0x6a, 0x6b, 0x6c, 0x6d, 0x6e, 0x6f, 0x70, 0x71,
       0x72, 0x73, 0x74, 0x75, 0x76, 0x77, 0x78, 0x79,
       0x7a, 0x7b, 0x7c, 0x7d, 0x7e, 0x7f, 0x80, 0x81,
       0x82, 0x83, 0x84, 0x85, 0x86, 0x87, 0x88, 0x89,
       0x8a, 0x8b, 0x8c, 0x8d, 0x8e, 0x8f, 0x90, 0x91,
       0x92, 0x93, 0x94, 0x95, 0x96, 0x97, 0x98, 0x99,
       0x9a, 0x9b, 0x9c, 0x9d, 0x9e, 0x9f, 0xa0, 0xa1,
       0xa2, 0xa3, 0xa4, 0xa5, 0xa6, 0xa7, 0xa8, 0xa9,
       0xaa, 0xab, 0xac, 0xad, 0xae, 0xaf, 0xb0, 0xb1,
       0xb2, 0xb3, 0xb4, 0xb5, 0xb6, 0xb7, 0xb8, 0xb9,
       0xba, 0xbb, 0xbc, 0xbd, 0xbe, 0xbf, 0xc0, 0xc1,
       0xc2, 0xc3, 0xc4, 0xc5, 0xc6, 0xc7, 0xc8, 0xc9,
       0xca, 0xcb, 0xcc, 0xcd, 0xce, 0xcf, 0xd0, 0xd1,
       0xd2, 0xd3, 0xd4, 0xd5, 0xd6, 0xd7, 0xd8, 0xd9,
       0xda, 0xdb, 0xdc, 0xdd, 0xde, 0xdf, 0xe0, 0xe1,
       0xe2, 0xe3, 0xe4, 0xe5, 0xe6, 0xe7, 0xe8, 0xe9,
       0xea, 0xeb, 0xec, 0xed, 0xee, 0xef, 0xf0, 0xf1,
       0xf2, 0xf3, 0xf4, 0xf5, 0xf6, 0xf7, 0xf8, 0xf9,
       0xfa, 0xfb, 0xfc, 0xfd, 0xfe, 0xff]

message_ind = [[134, 56, 185, 0, 14, 111, 51, 108],
 [171, 45, 129, 50, 208, 24, 23, 194],
 [235, 22, 16, 141, 150, 233, 54, 110],
 [160, 95, 177, 1, 203, 6, 135, 207],
 [97, 225, 48, 149, 104, 147, 92, 213],
 [252, 70, 161, 183, 62, 130, 30, 211],
 [53, 102, 78, 125, 176, 113, 9, 156],
 [47, 26, 33, 226, 69, 221, 118, 98],
 [42, 63, 222, 157, 228, 17, 191, 169],
 [155, 217, 193, 139, 204, 241, 145, 52],
 [148, 61, 164, 236, 107, 117, 86, 12],
 [114, 29, 10, 119, 116, 167, 189, 142],
 [153, 249, 36, 197, 151, 40, 246, 137],
 [128, 75, 182, 209, 13, 88, 210, 11],
 [231, 196, 55, 206, 143, 195, 38, 140],
 [138, 5, 8, 215, 21, 144, 87, 124],
 [65, 174, 80, 201, 93, 238, 212, 46],
 [223, 229, 131, 175, 19, 163, 136, 187],
 [20, 133, 234, 89, 68, 172, 121, 192],
 [199, 126, 109, 74, 35, 165, 58, 250],
 [146, 220, 120, 71, 237, 7, 224, 132],
 [245, 79, 84, 152, 72, 244, 127, 230],
 [242, 179, 15, 170, 3, 57, 202, 253],
 [101, 76, 205, 18, 73, 43, 158, 232],
 [103, 90, 162, 180, 159, 34, 166, 31],
 [222, 84, 53, 3, 241, 159, 233, 172],
 [20, 223, 86, 35, 160, 158, 76, 133],
 [137, 245, 120, 119, 221, 78, 146, 153],
 [143, 11, 226, 203, 228, 125, 57, 107],
 [34, 9, 169, 58, 193, 88, 109, 23],
 [207, 177, 8, 194, 182, 111, 217, 162],
 [92, 63, 149, 201, 156, 74, 140, 48],
 [108, 192, 148, 163, 234, 29, 33, 117],
 [104, 155, 242, 10, 24, 229, 215, 68],
 [73, 176, 244, 151, 179, 46, 43, 47],
 [131, 136, 79, 157, 252, 55, 128, 65],
 [71, 121, 114, 6, 51, 220, 52, 161],
 [70, 113, 26, 22, 185, 118, 95, 50],
 [195, 69, 208, 93, 250, 0, 187, 213],
 [134, 209, 165, 89, 7, 175, 167, 235],
 [231, 45, 101, 202, 116, 5, 236, 189],
 [174, 72, 183, 232, 97, 102, 110, 145],
 [164, 142, 199, 204, 237, 138, 210, 166],
 [127, 56, 152, 42, 180, 132, 246, 144],
 [30, 253, 87, 62, 14, 1, 19, 17],
 [13, 103, 206, 224, 249, 98, 40, 36],
 [54, 21, 197, 139, 38, 31, 170, 135],
 [191, 212, 90, 141, 129, 211, 147, 15],
 [61, 75, 238, 16, 80, 18, 205, 126],
 [171, 196, 230, 130, 124, 12, 225, 150],
 [50, 159, 207, 238, 48, 8, 142, 18],
 [196, 249, 56, 6, 206, 61, 54, 221],
 [171, 244, 30, 9, 126, 124, 88, 46],
 [215, 201, 78, 35, 120, 211, 73, 93],
 [132, 138, 15, 155, 52, 33, 187, 65],
 [92, 129, 213, 133, 197, 253, 42, 145],
 [103, 121, 102, 148, 246, 222, 117, 58],
 [220, 21, 231, 13, 87, 104, 75, 174],
 [156, 34, 166, 119, 131, 144, 180, 241],
 [55, 217, 43, 163, 134, 29, 203, 68],
 [80, 95, 162, 113, 153, 137, 252, 141],
 [245, 38, 70, 57, 175, 97, 172, 143],
 [40, 226, 118, 125, 202, 191, 165, 14],
 [23, 51, 152, 7, 24, 36, 195, 47],
 [130, 140, 182, 235, 107, 250, 71, 63],
 [3, 26, 11, 84, 233, 31, 116, 74],
 [136, 185, 108, 242, 234, 192, 193, 79],
 [169, 90, 205, 232, 229, 151, 199, 10],
 [0, 101, 150, 164, 179, 228, 176, 204],
 [72, 89, 189, 86, 111, 230, 212, 19],
 [127, 1, 114, 16, 69, 160, 157, 147],
 [53, 236, 12, 98, 161, 139, 146, 149],
 [224, 158, 237, 110, 62, 128, 223, 225],
 [22, 17, 170, 76, 210, 177, 194, 208],
 [183, 45, 167, 20, 5, 209, 135, 109],
 [175, 132, 63, 225, 6, 76, 151, 172],
 [69, 119, 12, 193, 215, 1, 148, 45],
 [249, 15, 234, 196, 79, 97, 164, 40],
 [149, 244, 73, 207, 222, 104, 224, 30],
 [185, 74, 152, 9, 142, 221, 170, 131],
 [211, 93, 166, 158, 210, 90, 102, 252],
 [192, 208, 38, 133, 197, 144, 56, 55],
 [92, 116, 46, 195, 57, 47, 180, 107],
 [226, 52, 111, 150, 35, 232, 156, 0],
 [16, 204, 11, 165, 117, 72, 231, 14],
 [22, 230, 125, 202, 88, 17, 36, 65],
 [24, 245, 143, 213, 223, 238, 145, 205],
 [126, 62, 177, 29, 110, 124, 120, 138],
 [140, 108, 21, 237, 113, 176, 31, 139],
 [51, 174, 134, 155, 53, 250, 171, 118],
 [3, 26, 70, 217, 160, 157, 50, 199],
 [209, 86, 80, 58, 179, 7, 48, 71],
 [241, 10, 87, 19, 95, 5, 189, 163],
 [121, 103, 167, 98, 114, 109, 75, 159],
 [68, 147, 61, 191, 42, 127, 84, 89],
 [153, 141, 228, 136, 129, 43, 169, 206],
 [162, 13, 128, 23, 54, 18, 20, 183],
 [203, 194, 34, 212, 130, 135, 8, 233],
 [101, 236, 182, 235, 78, 246, 253, 201],
 [187, 146, 137, 220, 229, 242, 161, 33],
 [159, 211, 116, 70, 89, 171, 139, 217],
 [88, 193, 21, 50, 19, 111, 7, 135],
 [121, 93, 132, 160, 176, 163, 33, 58],
 [189, 54, 148, 78, 76, 124, 0, 95],
 [205, 252, 128, 120, 179, 152, 153, 145],
 [5, 146, 206, 52, 192, 107, 142, 182],
 [34, 9, 73, 210, 166, 177, 229, 215],
 [8, 236, 204, 133, 157, 62, 230, 131],
 [149, 164, 65, 144, 71, 92, 208, 119],
 [23, 84, 155, 183, 110, 10, 203, 172],
 [3, 14, 195, 24, 242, 43, 97, 56],
 [156, 125, 46, 48, 220, 207, 143, 16],
 [175, 245, 130, 101, 150, 55, 98, 244],
 [185, 202, 35, 20, 134, 57, 221, 197],
 [196, 53, 165, 17, 246, 102, 232, 187],
 [161, 238, 191, 222, 69, 228, 235, 61],
 [36, 226, 224, 151, 201, 212, 11, 113],
 [79, 162, 138, 127, 253, 233, 237, 6],
 [13, 250, 1, 51, 86, 38, 169, 194],
 [26, 15, 170, 108, 129, 63, 118, 90],
 [31, 117, 140, 209, 74, 72, 80, 180],
 [223, 29, 47, 12, 45, 234, 137, 213],
 [104, 141, 136, 30, 225, 87, 231, 42],
 [114, 174, 167, 40, 199, 109, 22, 126],
 [75, 249, 158, 241, 147, 18, 68, 103],
 [172, 84, 135, 252, 206, 167, 228, 72],
 [42, 0, 144, 253, 58, 148, 160, 192],
 [34, 196, 12, 223, 78, 187, 35, 189],
 [220, 10, 120, 225, 126, 128, 217, 201],
 [110, 208, 63, 131, 230, 14, 138, 18],
 [13, 242, 7, 174, 38, 50, 158, 166],
 [62, 56, 193, 89, 250, 51, 22, 171],
 [149, 33, 8, 54, 165, 213, 80, 98],
 [101, 48, 224, 177, 24, 236, 195, 199],
 [30, 140, 74, 241, 143, 127, 92, 207],
 [103, 244, 209, 6, 69, 183, 197, 222],
 [134, 151, 95, 137, 114, 70, 118, 233],
 [17, 107, 36, 159, 88, 146, 16, 52],
 [11, 229, 194, 29, 1, 19, 109, 235],
 [9, 124, 185, 141, 249, 71, 23, 142],
 [245, 73, 61, 238, 31, 68, 125, 147],
 [108, 21, 117, 170, 102, 162, 164, 5],
 [119, 139, 221, 237, 79, 153, 204, 43],
 [20, 202, 45, 211, 210, 113, 87, 136],
 [97, 104, 90, 15, 169, 150, 152, 175],
 [111, 163, 3, 145, 180, 176, 53, 157],
 [212, 155, 86, 232, 231, 75, 156, 76],
 [215, 179, 132, 47, 205, 26, 116, 226],
 [191, 130, 182, 121, 133, 46, 234, 246],
 [55, 203, 161, 129, 40, 57, 65, 93],
 [58, 17, 86, 31, 147, 221, 24, 34],
 [179, 228, 101, 193, 236, 160, 192, 54],
 [72, 118, 245, 92, 135, 84, 241, 141],
 [189, 95, 15, 69, 129, 93, 35, 231],
 [119, 20, 22, 197, 18, 252, 87, 38],
 [140, 138, 80, 113, 145, 176, 209, 202],
 [206, 196, 51, 33, 62, 50, 153, 162],
 [142, 174, 109, 212, 220, 237, 70, 65],
 [132, 13, 182, 223, 134, 26, 253, 102],
 [76, 108, 1, 79, 177, 244, 149, 5],
 [48, 12, 36, 204, 71, 185, 158, 155],
 [73, 250, 29, 167, 156, 246, 238, 0],
 [183, 53, 195, 90, 3, 194, 128, 144],
 [42, 242, 170, 139, 159, 217, 7, 143],
 [163, 10, 249, 166, 226, 203, 55, 157],
 [146, 19, 169, 74, 215, 161, 150, 45],
 [229, 125, 61, 110, 78, 230, 120, 222],
 [111, 211, 210, 199, 23, 16, 98, 68],
 [208, 137, 97, 8, 172, 207, 107, 9],
 [165, 21, 63, 127, 57, 234, 131, 151],
 [232, 233, 213, 75, 117, 148, 152, 235],
 [103, 52, 180, 89, 130, 14, 224, 205],
 [6, 171, 43, 116, 114, 136, 11, 191],
 [164, 225, 56, 126, 121, 47, 133, 175],
 [46, 104, 201, 40, 124, 30, 187, 88],
 [166, 238, 177, 114, 117, 217, 226, 5],
 [68, 165, 50, 21, 104, 159, 62, 31],
 [55, 118, 93, 75, 22, 119, 121, 108],
 [157, 80, 229, 192, 193, 167, 88, 79],
 [16, 150, 162, 253, 102, 58, 169, 241],
 [15, 202, 98, 17, 176, 172, 19, 179],
 [138, 38, 103, 73, 204, 92, 242, 249],
 [191, 220, 152, 89, 129, 195, 135, 244],
 [142, 180, 174, 46, 194, 196, 211, 124],
 [245, 6, 182, 221, 252, 29, 231, 136],
 [57, 3, 12, 84, 212, 128, 197, 63],
 [14, 250, 1, 13, 144, 30, 141, 116],
 [36, 199, 69, 132, 183, 222, 8, 139],
 [43, 97, 74, 52, 113, 234, 33, 236],
 [24, 125, 120, 131, 149, 137, 133, 95],
 [232, 111, 107, 143, 101, 109, 171, 170],
 [130, 11, 209, 90, 0, 145, 189, 187],
 [20, 61, 26, 235, 56, 87, 110, 86],
 [51, 246, 153, 78, 10, 65, 163, 147],
 [35, 70, 40, 45, 175, 164, 237, 126],
 [203, 207, 134, 201, 213, 140, 225, 224],
 [208, 206, 34, 23, 9, 71, 47, 151],
 [54, 155, 18, 146, 185, 158, 156, 127],
 [210, 48, 160, 148, 233, 7, 205, 72],
 [42, 230, 215, 53, 228, 223, 76, 161]]

messages = [[hex_values[i] for i in message_ind_j] for message_ind_j in message_ind]
freq = 868000000
sf = 8
power = 14
bandwidth = LoRa.BW_125KHZ

lora.frequency(freq)
lora.sf(sf)
lora.tx_power(power)
lora.coding_rate(LoRa.CODING_4_5)
lora.bandwidth(bandwidth)

node_offset = 18 # 0/2/4/6/8/10/12/14/16/18

while True:
    current_time = rtc.now()
    time_now = current_time[4]*60+current_time[5]

    time_now %= 3600
    message_id = time_now//20  # 0-179 messages only
    message = messages[message_id]
    
    # time_now = current_time[5]
    # message = messages[0]

    if time_now%20==node_offset:
        # print("Sending {} at {}".format(message_id,current_time,time_now))
        # print("Lora configuration: ",lora.stats())
        big_buffer = bytes(message)
        s.send(big_buffer)
        pycom.rgbled(0x00FF00)  
        time.sleep(0.5)
        pycom.rgbled(0x000000)
        time.sleep(3)