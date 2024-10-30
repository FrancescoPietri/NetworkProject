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

```bash
ryu-manager FlowController.py
```

<details>
<summary>output</summary>
    <p align="center">
      <img src="images/test.png" width="600">
    </p>
</details>

e su un altro terminale chiamare il comando per aprire la gui

```bash
sudo python3 GUImain.py
```
<details>
<summary>output</summary>
    <p align="center">
      <img src="images/test.png" width="600">
    </p>
</details>


## Descrizione del workingflow

<p align="center">
  <img src="images/test.png" width="1000">
</p>

#### Deploy
1. Inserire il nome del servizio voluto
2. premere start - verrànno chiamate a cascata le funzioni
3. start client
    ```python
    def sottrazione(a, b):
        """Restituisce la differenza tra due numeri."""
        return a - b
    ```

4. deploy client che contiene initflow
    ```python
    def sottrazione(a, b):
        """Restituisce la differenza tra due numeri."""
        return a - b
    ```


#### Stop
1. selezionare dal menu a tendina il servizio da fermare
2. premere stop
3. verranno chiamate le funzioni
4. stop client
  ```python
  def somma(a, b):
      """Restituisce la somma di due numeri."""
      return a + b
  ```

5. stop server
    ```python
    def sottrazione(a, b):
        """Restituisce la differenza tra due numeri."""
        return a - b
    ```


le operazioni verranno mostrate all'utente tramite un comodo schermo




## Testing

è possibile controllare tramita wireshark l'effettoivo scambio di messaggi tra client e server
<details>
<summary>output</summary>
    <p align="center">
      <img src="images/test.png" width="600">
    </p>
</details>

[Video demo](https://www.youtube.com/watch?v=0IURpXwvLrw)


<details>
<summary>output di esempio per verificare il corretto funzionamento</summary>

---

- [all good](images/test.png)
- [broken s1](images/test.png)

</details>
