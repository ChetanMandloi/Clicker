import requests
#import httpx
import asyncio


station_ip = "http://192.168.0.76"

r = requests.post('http://192.168.0.76/RESET', data ={'key':'value'})
print(r)