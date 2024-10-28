# NetworkProject
### dependences
Flask, networkx (pip install)

#### comandi mininet
sudo -E python3 main.py <br>
mininet> deploy <nome servizio> <path_locale> <host opzionale> -> fa il deploy, se non specifico host seceglie quello con meno <br> servizi <br>
mininet> service_count -> lista servizi sugli host <br>
mininet> stop <nome servizio> <host opzionale> -> stoppa il servzio nell'host, se non specifico l'host rimuove il servizio da ovunque <br>
mininet> check_status <host> <porta> -> vede la risposta del servizio nell'host <br>

##### esempio
sudo -E python3 main.py <br>
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
service_count <br>

