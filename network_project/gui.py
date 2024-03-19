import tkinter as tk

def mostra_testo():
    testo_inserito = campo_di_testo.get()
    print("Hai inserito: ", testo_inserito)

finestra = tk.Tk()
finestra.title("Interfaccia di Input")

campo_di_testo = tk.Entry(finestra)
campo_di_testo.pack()

bottone = tk.Button(finestra, text="Invia", command=mostra_testo)
bottone.pack()

finestra.mainloop()
