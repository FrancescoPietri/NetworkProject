English version [here](README.md)

---

# Title

> Il porgetto Title è progettato per creare una rete virtuale flessibile a cambi nella rete rendendol il sistema versatile e che permetta il deploy e lo stop automatici dei servizi mantenendo gli host della rete bilanciati migliorando sfruttando al meglio tutte le risorse della rete fornendo inoltre una comoda GUI, scambio di messaggi presente


## Contenuti
- [Caratteristiche Principali](#caratteristiche-principali)
- [Benefici](#benefici)
- [Casi d'Uso](#casi-duso)
- [Iniziare](#iniziare)
- [Descrizione Workingflow](#descrizione-del-workingflow)
- [Testing](#testing)

---

### Caratteristiche Principali

- **Indipendenza dalla Topologia della rete**:
    - La topologia non è hardcodata nella rete
    - Il sistema prende la topologia in input e crea la rete da essa


- **Totale Autonomia di Deploy**:
    - Implementa la possibilità di lanciare il servizio senza specificare gli host
    - Il sistema rileverà gli host ocn meno sevizi e ci caricherà il nuovo
    - Verrà inoltre creato un canale di comunicazio tra i due host
    - Deploy automatico specificando solo il servizio


### Benefici

- **Flessibilità**: Riduce la necessità di intervenire nel sistema se è richiesto un cambio nella topologia della rete
- **Autonomia**: Permette all'utente un deploy automatico tramite GUI garantendo la rete bilanciata senza che debba alzare un dito

### Casi d'Uso

- **Reti Aziendali**: Garantisce la continuità aziendale date le modifiche minie da apportare in caso di un cambiamento alla rete
- **Personale con poca esperienza**: Permette di effettuare deploy da parte di personale senza conoscenza tecnica



## Iniziare

Comandi di Inizializzazione
Per avviare la rete e il controller, basta eseguire le seguenti istruzioni per avviare il controller:

```python
./ryu manager flowcontroller
```

<details>
<summary>output</summary>
    <p align="center">
      <img src="images/test.png" width="600">
    </p>
</details>

e su un altro terminale chiamare il comando per aprire la gui

```python
./GUI
```
<details>
<summary>output</summary>
    <p align="center">
      <img src="images/test.png" width="600">
    </p>
</details>









## Descrizione del workingflow
Inserire il nome del servizio voluto
premere start
verrànno chiamate a cascata le funzioni
deploy server
deploy client ceh contiene initflow



per lo stop
selezionare dal menu a tendina il servizio da fermare
premere stop
verranno chiamate le funzioni
stop client
stop server


le operazioni verranno mostrate all'utente tramite un comodo schermo




## Testing

è possibile controllare tramita wireshark l'effettoivo scambio di messaggi tra client e server

[Video demo](https://youtu.be/SWiC3gSeuXk)


<details>
<summary>output di esempio per verificare il corretto funzionamento</summary>

---

- [all good](images/test.png)
- [broken s1](images/test.png)

</details>
