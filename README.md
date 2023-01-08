# httpmqtt

# Author: Joe YU

This is a simple http - mqtt server on Raspberry Pi Pico W or any other NodeMCU board with Micropython.

The only function is to receive topic, message as header key-value chains from http requests and turn them into MQTT message and send it away. 

Arecord is made into a "log.json" file.

It's still faulty for two reasons 
1. MQTT and Http both use socket connection at same time and sometimes conflict with each other. 
2. It is open to WAN so it's easy to pickup noise and I'm still working on the noise filter. Learning regex for micropython