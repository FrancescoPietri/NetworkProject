import tkinter as tk
from tkinter import messagebox
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSKernelSwitch, RemoteController
from mininet.link import TCLink
from topology import ShipTopo
from deployer import WebServiceDeployer  # Importa la classe WebServiceDeployer
from connectivity import FlowManager


class CommandGUI:
    def __init__(self, net, deployer):
        self.net = net
        self.deployer = deployer
        self.window = tk.Tk()
        self.window.title("Command Sender")

        # Crea un'etichetta
        label = tk.Label(self.window, text="Inserisci un comando:")
        label.pack(pady=10)

        # Crea un campo di input
        self.command_entry = tk.Entry(self.window, width=50)
        self.command_entry.pack(pady=5)

        # Crea un pulsante
        send_button = tk.Button(self.window, text="Invia", command=self.send_command)
        send_button.pack(pady=10)

        # Gestisci chiusura della finestra
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

        # Avvia l'interfaccia grafica
        self.window.mainloop()

    def send_command(self):
        command = self.command_entry.get()
        if command:
            try:
                # Esegui il comando qui (adatta questa parte in base a come vuoi gestire i comandi)
                result = self.handle_command(command)
                messagebox.showinfo("Risultato", f"Comando eseguito: {result}")
            except Exception as e:
                messagebox.showerror("Errore", f"Errore nell'esecuzione del comando: {e}")
            self.command_entry.delete(0, tk.END)  # Pulisci il campo di input
        else:
            messagebox.showwarning("Errore", "Per favore, inserisci un comando.")

    def handle_command(self, command):
        # Implementa qui la logica per eseguire il comando
        print(f"Eseguendo comando: {command}")
        return f"Comando '{command}' eseguito."

    def on_close(self):
        # Ferma la rete e chiudi la finestra
        self.net.stop()
        self.window.destroy()

def main():
    # Crea la topologia e avvia Mininet
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

    # Inizializza il WebServiceDeployer
    deployer = WebServiceDeployer()
    print(f"DEBUG: Initialized WebServiceDeployer: {deployer}")

    # Avvia l'interfaccia grafica per inviare comandi
    CommandGUI(net, deployer)  # Passa net e deployer alla GUI

if __name__ == "__main__":
    main()


