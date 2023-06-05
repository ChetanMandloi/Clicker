import requests
from collections import Counter
import matplotlib.pyplot as plt
import time
start_time = time.time()
num_stations = 2
station_start_ip4 = 70
station_ip_prefix = "http://192.168.0."

def generate_http_list():
    http_list = []
    for i in range(num_stations):
        http_list.append(station_ip_prefix + str(i+station_start_ip4))
    return http_list

if __name__ == '__main__':
    http_list = generate_http_list()
    response_list = []
    for add in http_list:
        try:
            r = requests.get(add)
            print(r.text),
            response_list.append(r.text.split("!")[-2])
        except requests.exceptions.ConnectionError:
            print("Connection Failed to ", add)
            continue
    tally = Counter(response_list)
    plt.bar(tally.keys(), tally.values())
    end_time = time.time()
    plt.show()
    plt.savefig("mygraph.png")
    print(tally)
    print(end_time-start_time)
