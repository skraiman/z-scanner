#!/usr/bin/python3
# alternate-non-blocking-io
import sys
from threading import Thread
from queue import Queue, Empty

import re
import tkinter as tk
from tkinter import ttk
import netifaces
import subprocess

proc = None
listbox_data = None
addr_list = None
q = None
ON_POSIX = 'posix' in sys.builtin_module_names


def enqueue_output(out, queue):
    for line in iter(out.readline, b''):
        queue.put(line)
    out.close()


def get_gateways():
    gateway_list = []
    gateways = netifaces.gateways()
    if 'default' in gateways:
        def_gw = gateways['default']
        for (ip, _if) in def_gw.values():
            gateway_list.append((_if, 'gw ' + ip))
    return gateway_list


def get_ip_addresses():
    addr_list = []
    interfaces = netifaces.interfaces()
    for _if in interfaces:
        addresses = netifaces.ifaddresses(_if)
        for (type, if_info) in addresses.items():
            for info in if_info:
                if 'addr' in info:
                    ip = info['addr']
                    if 'netmask' in info:
                        ip = ip + ' netmask ' + info['netmask']
                    addr_list.append((_if, ip))

    return addr_list


def cb_callback(event):
    iface = v.get()
    update_listbox_ipaddr(iface)
    if iface != "":
        start_tcpdump(iface)

def b_cb():
    stop_tcpdump()
    cb.set("")
    update_listbox_ipaddr("")


def lb_callback(event):
    w = event.widget
    index = int(w.curselection()[0])
    item = w.get(index)
    p = item.split(':')
    if len(p) > 1:
        iface = p[0]
        update_listbox_ipaddr(iface)
        start_tcpdump(iface)
        cb.set(iface)


def update_listbox_vlan(vlan):
    global listbox_data
    if vlan not in listbox_data:
        listbox_data.append(vlan)
        listvar.set(listbox_data)


def update_listbox_ipaddr(interface: str):
    global listbox_data
    global addr_list
    global gw_list

    addr_list = get_ip_addresses()
    gateway_list = get_gateways()
    if interface == "":
        listbox_data = [a + ": " + b for (a, b) in addr_list + gateway_list]
    else:
        listbox_data = [a + ": " + b for (a, b) in addr_list + gateway_list if a == interface]

    listvar.set(listbox_data)

def stop_tcpdump():
    global proc

    if proc != None:
        proc.kill()
        proc = None

def start_tcpdump(iface):
    global proc
    global q

    stop_tcpdump()

    proc = subprocess.Popen(['/usr/sbin/tcpdump', '-n', '-l', '-i', iface, '-e', 'vlan'],
                            stdout=subprocess.PIPE, universal_newlines=True, close_fds=ON_POSIX,
                            bufsize=1,
                            )
    q = Queue()
    t = Thread(target=enqueue_output, args=(proc.stdout, q))
    t.daemon = True  # thread dies with the program
    t.start()


width = 50
w = tk.Tk()
w.title('CommunicationZ Scanner')

w.geometry("460x300")

lbl = tk.Label(w, text="Interface").grid(column=0, row=0)

listvar = tk.StringVar()

ifaces = netifaces.interfaces()
ifaces.insert(0, "")


b = tk.Button(w, text='Home', command=b_cb)
b.grid(column=1, row=1)


v = tk.StringVar()  # a string variable to hold user selection

cb = ttk.Combobox(w, textvariable=v, values=ifaces, width=width-15)
cb.grid(column=0, row=1)
cb.current(0)
cb.bind("<<ComboboxSelected>>", cb_callback)


update_listbox_ipaddr("")
listbox = tk.Listbox(w, listvariable=listvar,  width=width)
listbox.bind("<<ListboxSelect>>", lb_callback)

listbox.grid(column=0, row=2, columnspan=2)
# listbox.pack()

# w.mainloop()
vlan_re = re.compile('^.* (vlan \d+),.*$')

while True:
    w.update_idletasks()
    w.update()
    if proc != None:
        try:
            line = q.get_nowait()  # or q.get(timeout=.1)
            if line:
                line = line.rstrip()
                m = vlan_re.search(line)
                update_listbox_vlan(m.group(1))
        except Empty:
            pass

    #
