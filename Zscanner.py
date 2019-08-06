import tkinter as tk
from tkinter import ttk
import netifaces

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
    print(v.get())
    update_listbox(v.get())

def update_listbox(interface:str):
    if interface=="":
        l=  [a + ": " + b for (a,b) in addr_list]
    else:
        l = [a + ": " + b for (a, b) in addr_list if a == interface]

    listvar.set(l)
    print(listvar)

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
update_listbox("")
listbox = tk.Listbox(w, listvariable = listvar, width=40)



listbox.grid(column=0, row=2)
#listbox.pack()

w.mainloop()