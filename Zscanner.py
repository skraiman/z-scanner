#!/usr/bin/python3
# alternate-non-blocking-io
import re
import tkinter as tk
from tkinter import ttk
import netifaces
import subprocess



proc = None
listbox_data = None

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
    print(event)
    iface = v.get()
    print(iface)
    update_listbox_ipaddr(iface)
    if iface != "":
        start_tcpdump(iface)

def update_listbox_vlan(vlan):
    if not vlan in listvar_data:
        listvar.append(vlan)
    listvar.set(list_box_data)


def update_listbox_ipaddr(interface:str):
    if interface=="":
        listbox_data=  [a + ": " + b for (a,b) in addr_list]
    else:
        listbox_data = [a + ": " + b for (a, b) in addr_list if a == interface]

    listvar.set(listbox_data)

def start_tcpdump(iface):
    global proc
    global nbsr
    if proc != None:
        proc.kill()
        proc = None
        nbsr = None

    proc = subprocess.Popen(['/usr/sbin/tcpdump', '-i', iface, '-e', 'vlan'],
                            stdout=subprocess.PIPE, bufsize=1, universal_newlines=True
                            #stderr=subprocess.PIPE
                            )
    nbsr = NBSR(proc.stdout)

w = tk.Tk()
w.title('CommunicationZ Scanner')

w.geometry("460x300")

lbl = tk.Label(w, text="Interface").grid(column=0, row=0)


ifaces = netifaces.interfaces()
ifaces.insert(0, "")

v = tk.StringVar()#a string variable to hold user selection

cb = ttk.Combobox(w, textvariable=v, values=ifaces, width=40)
print(dict(cb))
cb.grid(column=0, row=1)
cb.current(0)
cb.bind("<<ComboboxSelected>>", cb_callback)

addr_list = get_ip_addresses()
listvar = tk.StringVar()
update_listbox_ipaddr("")
listbox = tk.Listbox(w, listvariable = listvar, width=40)



listbox.grid(column=0, row=2)
#listbox.pack()

#w.mainloop()
vlan_re = re.compile('^.* (vlan \d+),.*$')

while True:
    w.update_idletasks()
    w.update()
    if proc != None:
        try:
            line = nbsr.readline(0.1)
            if line:
                line = line.rstrip()
                print("line={}".format(line))
                m = vlan.re.search(line)
                update_listbox_vlan(m.group(1))
        except UnexpectedEndOfStream:
            pass

    #
