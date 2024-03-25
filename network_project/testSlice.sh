#!/bin/sh

echo '---------- Creating Slice 1 ----------'
echo 'Switch 1:'

sudo ovs-vsctl set port s1-eth1 qos=@newqos -- \
--id=@newqos create QoS type=linux-htb \
other-config:max-rate=1000 \
queues:1=@1q -- \
--id=@1q create queue other-config:min-rate=500 other-config:max-rate=1000

sudo ovs-vsctl set port s2-eth1 qos=@newqos -- \
--id=@newqos create QoS type=linux-htb \
other-config:max-rate=1000 \
queues:1=@1q -- \
--id=@1q create queue other-config:min-rate=500 other-config:max-rate=1000 

sudo ovs-ofctl add-flow s1 ip,priority=65500,nw_src=10.0.0.1,nw_dst=10.0.0.2,idle_timeout=0,actions=set_queue:1,output:1

sudo ovs-ofctl add-flow s2 ip,priority=65500,nw_src=10.0.0.2,nw_dst=10.0.0.1,idle_timeout=0,actions=set_queue:1,output:1

