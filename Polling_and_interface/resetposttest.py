import requests
#import httpx
#import asyncio


# station_ip = "http://192.168.0.76"
#
# r = requests.post('http://192.168.0.76/RESET', data ={'key':'value'})
# print(r)

import time
start_time = time.time()
num_stations = 40
station_start_ip4 = 70
station_ip_prefix = "http://192.168.0."

def generate_http_list():
    http_list = []
    for i in range(num_stations):
        http_list.append(station_ip_prefix + str(i+station_start_ip4) + '/RESET')
    return http_list

if __name__ == '__main__':
    http_list = generate_http_list()
    response_list = []
    for add in http_list:
        try:
            r = requests.post(add, data ={'key':'value'})
        except requests.exceptions.ConnectionError:
            print("Connection Failed to ", add)
            continue
    end_time = time.time()
    print(end_time-start_time)
