# NetworkProject
### dependences
Flask, networkx (pip install) <br>

#### comandi mininet
ryu-manager FlowController.py (in un altro terminale)<br>
sudo -E python3 main.py <br>
mininet> deploy 'nome servizio' 'path_locale' 'host opzionale' -> fa il deploy, se non specifico host seceglie quello con meno <br> servizi <br>
mininet> service_count -> lista servizi sugli host <br>
mininet> stop 'nome servizio' 'host opzionale' -> stoppa il servzio nell'host, se non specifico l'host rimuove il servizio da ovunque <br>
mininet> check_status 'host' 'porta' -> vede la risposta del servizio nell'host <br>
mininet> initflow 'hostX' 'hostY' -> crea un flow tra hostX e hostY <br>
mininet> run_client 'hostX' 'hostY' -> scambia messaggi tra hostX e hostY <br>

##### esempio
ryu-manager FlowController.py <br>
sudo -E python3 main.py <br> <br>

deploy MyWebApp.py /home/vagrant/comnetsemu/network_project/MyWebApp.py h5 <br>
service_count <br>
deploy simpleWS.py /home/vagrant/comnetsemu/network_project/simpleWS.py <br>
deploy simpleWS.py /home/vagrant/comnetsemu/network_project/simpleWS.py h5 <br>
deploy simpleWS.py /home/vagrant/comnetsemu/network_project/simpleWS.py <br>
service_count <br>
check_status h5 80 <br>
check_status h1 90 <br>
stop h5 MyWebApp.py <br>
service_count <br>
stop simpleWS.py <br>
service_count <br> <br>

deploy server.py /home/vagrant/comnetsemu/network_project/server.py h7 <br>
deploy client.py /home/vagrant/comnetsemu/network_project/client.py h4 <br>
run_client h2 h1 9090 <br>
initflow h2 h1 <br>
run_client h2 h1 9090 <br>



