# httpmqtt

# Author: Joe YU

This is a simple http - mqtt server on Raspberry Pi Pico W or any other NodeMCU board with Micropython.

The only function is to receive topic, message as header key-value chains from http requests and turn them into MQTT message and send it away. 

Arecord is made into a "log.json" file.