# -----------------------------------------------------
# Clicker GUI
# Provides a Graphical User Interface for the clicker
# that polls modules parallely and plots bar graph
# of the obtained data and lets us reset
# -----------------------------------------------------
# Chetan Mandloi
# chetan.mandloi@live.com
# HBCSE, TIFR
# -----------------------------------------------------
from tkinter import *                                               # For Interface
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg     # Plotting stuff
from matplotlib.figure import Figure
from matplotlib.ticker import MaxNLocator
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import httpx                                                        # For asseccing http servers
import asyncio                                                      # For polling asynchronously
import time                                                         # For timing execution times
from collections import Counter                                     # For counting number of responses
from collections import OrderedDict

matplotlib.use("TkAgg")
# Some global variables because async functions don't behave properly with good encapsulation
datalist = []
httplist = []


async def get_async(url):
    """
    gets responses from a list of urls asynchronously
    :param url: list of urls
    :return: list of responses from each of the urls on a get request
    """
    timeouts = (1.2, 1.2)
    async with httpx.AsyncClient() as client:
        return await client.get(url, timeout=timeouts)

async def post_async(url):
    """
    posts a request to a list of urls asynchronously
    :param url: list of urls
    :return: list of responses from each of the urls on a post request
    """
    timeouts = (1.2, 1.2)
    async with httpx.AsyncClient() as client:
        return await client.post(url, data={'key': 'value'}, timeout=timeouts)

async def launchp():
    """
    Launch a post request for all clickers.
    :return: Nil
    """
    global httplist
    resp = await asyncio.gather(*map(post_async, httplist), return_exceptions=True)   # To avoid crash from ConnectionError

async def launch():
    """
    Launch a get request to all clickers.
    :return: Null
    """
    global httplist
    global datalist
    data = []
    resps = await asyncio.gather(*map(get_async, httplist), return_exceptions=True)         # To avoid crash from ConnectionError

    for resp in resps:
        try:
            data.append(resp.text)
            print(resp.text)
        except AttributeError:
            print("Connection error")
            continue
    datalist = data[:]
    return data


def generate_http_list(num_stations, station_ip_prefix, station_start_ip4, subd=""):
    """
    Generate a list of http urls given the number of online clicker modules and ip start location
    :param num_stations: int number of clickers connected to network
    :param station_ip_prefix: string containing http: and the first three numbers of the ip address
    :param station_start_ip4: int 4th ip address number of the first clicker. Assuming clickers are numbered serially
    :param subd: string Suffix that specifies any subdirectory in the url
    :return: Null
    """
    global httplist
    httplist = []
    for i in range(num_stations):
        httplist.append(station_ip_prefix + str(i + station_start_ip4) + subd)
    print("global httplist: ", httplist)

class MyWindow:
    def __init__(self, win):
        x0, xt0, y0 = 10, 120, 50
        self.num_stations = 45
        self.station_ip_prefix = "http://192.168.0."
        self.station_start_ip4 = 70
        self.httplist = []
        self.response_list = []
        self.atten_list = []
        self.option_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.color_list = ['lightsteelblue', 'red', 'green', 'blue', 'cyan', 'gold', 'purple', 'coral', 'brown', 'forestgreen', 'indigo']

        # ---- First label and entry -------
        self.lbl0 = Label(win, text='Enter IP Prefix')
        self.lbl0.config(font=('Arial', 9))
        self.lbl0.place(x=x0, y=y0)
        self.t0 = Entry()
        self.t0.place(x=xt0, y=y0)
        self.t0.insert(END, self.station_ip_prefix)
        self.station_ip_prefix = str(self.t0.get())

        # ---- Second label and entry -------
        self.lbl1 = Label(win, text='Total Modules')
        self.lbl1.config(font=('Arial', 10))
        self.lbl1.place(x=x0, y=y0 + 40)
        self.t1 = Entry()
        self.t1.place(x=xt0, y=y0 + 40)
        self.t1.insert(END, str(self.num_stations))
        self.num_stations = int(self.t1.get())

        # ---- Third label and entry -------
        self.lbl2 = Label(win, text='Start IP address')
        self.lbl2.config(font=('Arial', 10))
        self.lbl2.place(x=x0, y=y0 + 80)
        self.t2 = Entry()
        self.t2.place(x=xt0, y=y0 + 80)
        self.t2.insert(END, str(self.station_start_ip4))
        self.station_start_ip4 = int(self.t2.get())

        # ---- Fetch button -------
        self.fbtn = Button(win, text='Fetch responses')
        self.fbtn.bind('<Button-1>', self.plot)
        self.fbtn.place(x=xt0, y=y0 + 120)

        # ---- Reset button -------
        self.rbtn = Button(win, text='Reset clickers', command=lambda: self.reset())
        self.rbtn.bind('<Button-2>', self.reset)
        self.rbtn.place(x=xt0, y=y0 + 160)

        # ---- Fourth label and entry -------
        self.lbl3 = Label(win, text='Start IP address')
        self.lbl3.config(font=('Arial', 10))
        self.lbl3.place(x=x0, y=y0 + 80)
        self.t3 = Entry()
        self.t3.place(x=xt0, y=y0 + 80)
        self.t3.insert(END, str(self.station_start_ip4))
        self.station_start_ip4 = int(self.t3.get())

        self.figure = Figure(figsize=(10.5, 3), dpi=100)

        # ---- subplot 1 -------
        self.subplot1 = self.figure.add_subplot(111)
        # self.subplot1.set_xlim(self.t_0, self.t_1)

        # ---- Show the plot-------
        self.plots = FigureCanvasTkAgg(self.figure, win)
        self.plots.get_tk_widget().pack(side=RIGHT, fill=BOTH, expand=0)

    def up_ent_vals(self):
        """
        Updates variable values from the stuff entered in fields
        :return: Null
        """
        self.station_ip_prefix = str(self.t0.get())
        self.num_stations = int(self.t1.get())
        self.station_start_ip4 = int(self.t2.get())

    def plot(self, event):
        """
        Updates the graphical window on pressing the Fetch Responses button
        :param event: No idea why this variable is here, it isn't even used but code doesn't run without it
        :return: Null
        """
        global datalist, httplist
        self.up_ent_vals()
        generate_http_list(self.num_stations, self.station_ip_prefix, self.station_start_ip4)
        datalist = asyncio.run(launch())
        for i in datalist:
            self.response_list.append(int(i.split("!")[-2]))
            self.atten_list.append(int(i.split("!")[-3]))
        print(self.response_list, self.atten_list)
        tally =  {n:self.response_list.count(n) for n in self.option_list}

        #tally = Counter(self.response_list)
        print(tally.keys(), tally.values())
        #srt_tally = dict(sorted(tally.items(), key=lambda item: item[1], reverse=True))
        srt_tally = OrderedDict(sorted(tally.items()))

        self.subplot1.clear()
        self.subplot1.bar(srt_tally.keys(), srt_tally.values(), color=self.color_list)
        for i, v in enumerate(srt_tally.values()):
            #print(i,v)
            self.subplot1.text(i-0.1, v, str(v), color='black', fontweight='bold', fontsize=18)
        self.subplot1.set_xticks(self.option_list)
        self.subplot1.tick_params(axis="x", labelsize=24)
        self.subplot1.tick_params(axis="y", labelsize=18)
        self.subplot1.yaxis.set_major_locator(MaxNLocator(integer=True))
        self.response_list = []
        self.plots.draw()

    def reset(self):
        self.up_ent_vals()
        #print("here")
        global datalist
        generate_http_list(self.num_stations, self.station_ip_prefix, self.station_start_ip4, '/RESET')
        # print(httplist)
        asyncio.run(launchp())
        # print("data_list= ", datalist)



window = Tk()
mywin = MyWindow(window)
window.title('Clicker')
window.geometry("1500x600+10+10")
window.mainloop()
