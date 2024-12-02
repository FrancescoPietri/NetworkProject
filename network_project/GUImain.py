import tkinter as tk
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSKernelSwitch, RemoteController
from mininet.link import TCLink
from topology import ShipTopo
from topologyD import ShipTopoD
from deployer import WebServiceDeployer 
from connectivity import FlowManager 
import sys
import threading
import json

class CommandGUI:
    def __init__(self, net, deployer):

        self.service_manager = {}
        self.portCout = 8080

        self.net = net
        self.deployer = deployer
        self.deployed_services = []  
        self.window = tk.Tk()
        self.window.title("Command Sender")
        self.window.geometry("400x400")
        self.window.configure(bg="#2e2e2e")

        title_label = tk.Label(self.window, text="Service Deployment Interface", fg="white", bg="#2e2e2e", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=15)

        input_frame = tk.Frame(self.window, bg="#2e2e2e")
        input_frame.pack(pady=10)

        label = tk.Label(input_frame, text="Service Name:", fg="white", bg="#2e2e2e", font=("Helvetica", 12))
        label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.command_entry = tk.Entry(input_frame, width=30, font=("Helvetica", 12))
        self.command_entry.grid(row=0, column=1, padx=5, pady=5)

        self.selected_service = tk.StringVar(self.window)
        self.selected_service.set("Select the deployed service to Stop")
        
        menu_frame = tk.Frame(self.window, bg="#2e2e2e")
        menu_frame.pack(pady=10)
        self.service_menu = tk.OptionMenu(menu_frame, self.selected_service, "")
        self.service_menu.config(width=30, font=("Helvetica", 12))
        self.service_menu.pack(pady=5)

        button_frame = tk.Frame(self.window, bg="#2e2e2e")
        button_frame.pack(pady=10)

        send_button = tk.Button(button_frame, text="Deploy", command=lambda: self.start_thread_deploy(), bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold"), width=10)
        send_button.grid(row=0, column=0, padx=10, pady=10)

        delete_button = tk.Button(button_frame, text="Delete", command=lambda: self.start_thread_delete(), bg="#F44336", fg="white", font=("Helvetica", 12, "bold"), width=10)
        delete_button.grid(row=0, column=1, padx=10, pady=10)

        self.log_area = tk.Text(self.window, height=8, width=50, font=("Helvetica", 10), bg="#1e1e1e", fg="white")
        self.log_area.pack(pady=10)

        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
        self.window.mainloop()

    def start_thread_deploy(self):
        t = threading.Thread(target=self.deploy_service, args=())
        t.start()

    def start_thread_delete(self):
        t = threading.Thread(target=self.delete_service, args=())
        t.start()

    def delete_service(self):

        service_name = self.selected_service.get().strip()

        if service_name == "Select the deployed service to Stop":
            return

        self.log_area.insert(tk.END, f"Stopping client and service for {service_name}>>\n")

        self.deployer.stop_service(self.net, service_name,self.service_manager[f"{service_name}"][0])

        fm=FlowManager()

        self.log_area.insert(tk.END, f"Removing flow for {service_name}>>\n")
        
        #scorre tutte le porte utilizzate su h1 e controlla su h2 se è utilizzata la stessa porta e non è la porta del servizio da rimuovere, in quel caso vuol
        #dire che c'è un altro servizio che necessita connettività tra h1 e h2 e quindi non elimina il flow
        flag_flow = True
        for port in self.deployer.service_count[self.service_manager[f'{service_name}'][1]]["services"]:
            if port in self.deployer.service_count[self.service_manager[f'{service_name}'][2]]["services"] and port != self.service_manager[f'{service_name}'][0]:
                flag_flow = False

        if flag_flow:    
            fm.delete_flow(self.net, self.service_manager[f'{service_name}'][1], self.service_manager[f'{service_name}'][2])

        self.service_manager.pop(f"{service_name}")

        self.log_area.insert(tk.END, f"Done! Service {service_name} removed>>\n")

        #print(str(self.deployer.get_service_count()))

        if service_name and service_name in self.deployed_services:
            self.deployed_services.remove(service_name)
            self.update_service_menu()
            self.selected_service.set("")


    def deploy_service(self):
        service_name = self.command_entry.get().strip()
        if service_name and service_name not in self.deployed_services:
            self.deployed_services.append(service_name)
            self.update_service_menu()

        if service_name in self.service_manager.keys():
            print("already deployed!")
            return

        self.service_manager[f"{service_name}"] = [self.portCout]

        self.portCout = self.portCout + 1

        self.log_area.insert(tk.END, f"Deploying server for {service_name}>>\n")

        hostx = self.deployer.deploy_service(self.net, "server.py", self.service_manager[f"{service_name}"][0])

        self.service_manager[f"{service_name}"].append(hostx)

        self.log_area.insert(tk.END, f"Deploying client for {service_name}>>\n")

        self.log_area.insert(tk.END, f"Adding flow for {service_name}>>\n")

        hosty = self.deployer.deploy_service(self.net, "client.py", self.service_manager[f"{service_name}"][0], hostx)

        self.service_manager[f"{service_name}"].append(hosty)

        self.log_area.insert(tk.END, f"Done! Service {service_name} deployed>>\n")

        print(self.net.get(hostx).cmd("cat log"))

        #print(str(self.deployer.get_service_count()))

        for i in self.service_manager:
            print(i + " " + str(self.service_manager[i]))

    def update_service_menu(self):
        menu = self.service_menu["menu"]
        menu.delete(0, "end")
        
        for service in self.deployed_services:
            menu.add_command(label=service, command=lambda value=service: self.selected_service.set(value))

    def on_close(self):
        self.net.stop()
        self.window.destroy()

def main():

    reset_flow = []

    with open('flow.json', 'w') as json_file:
        json.dump(reset_flow, json_file, indent=4)

    if len(sys.argv) < 2:
        print("Usage: A: ShipTopo B: ShipTopoDestroyed")
        print("Exiting...")
        sys.exit()

    a, topoE = sys.argv

    print(topoE)

    if(topoE == "B"):
        topo = ShipTopoD()
    else:
        topo = ShipTopo()
        
    net = Mininet(
        topo=topo,
        switch=OVSKernelSwitch,
        build=False,
        autoSetMacs=True,
        autoStaticArp=True,
        link=TCLink
    )

    controller = net.addController('controller', controller=RemoteController, ip='127.0.0.1', port=6633)
    net.build()
    net.start()

    deployer = WebServiceDeployer()

    CommandGUI(net, deployer)  

if __name__ == "__main__":
    main()



