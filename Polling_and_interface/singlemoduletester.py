import requests
from collections import Counter
import matplotlib.pyplot as plt

num_stations = 1
station_start_ip4 = 60
station_ip_prefix = "http://192.168.0."

def generate_http_list():
    http_list = []
    for i in range(10):
        http_list.append(station_ip_prefix + str(i+station_start_ip4))
    return http_list

if __name__ == '__main__':
    http_list = generate_http_list()
    response_list = []
    for add in http_list:
        try:
            r = requests.get(add)
            #print(r.text[:-2:-1]),
            response_list.append(r.text[:-2:-1])
        except requests.exceptions.ConnectionError:
            print("Connection Failed to ", add)
            continue
    tally = Counter(response_list)
    plt.bar(tally.keys(), tally.values())
    plt.show()
    print(tally)
