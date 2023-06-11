import httpx
import asyncio
import time
from collections import Counter
import matplotlib.pyplot as plt


async def post_async(url):
    async with httpx.AsyncClient() as client:
        return await client.post(url, data={'key': 'value'})


num_stations = 3
station_start_ip4 = 70
station_ip_prefix = "http://192.168.0."
datalist = []


def generate_http_list():
    http_list = []
    for i in range(num_stations):
        http_list.append(station_ip_prefix + str(i + station_start_ip4) + '/RESET')
    return http_list


httplist = generate_http_list()


async def launch(httplist):
    resp = await asyncio.gather(*map(post_async, httplist), return_exceptions=True)
    print(resp)

if __name__ == '__main__':
    start_time = time.time()
    response_list = []
    asyncio.run(launch(httplist))
    end_time = time.time()
    plt.show()
    plt.savefig("mygraph.png")
    print(end_time - start_time)
