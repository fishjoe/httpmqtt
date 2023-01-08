from simple_mqtt_modified import MQTTClient

class CB:
    def __init__(self):
        self.isDone = False
cb=CB()    




def mqtt_callback(topic, payload):
    led_blink(3,.2,.2)
    cb.isDone = True



mqtt_server = 'dc87a3d9523a42798c3d086fd8acbdb5.s1.eu.hivemq.cloud'
mqtt_port = 8883
client_id = 'PicoW'
mqtt_username = 'fishjoe2'
mqtt_psd = 'fishjoe2'
topic_pub = 'test'
topic_msg = 'PicoStart'

bt = b"\x30\0\0\0"
print(bt.decode('utf-8'))

mqtt=MQTTClient(client_id=client_id, server=mqtt_server, port=mqtt_port, user=mqtt_username,password=mqtt_psd, ssl=True, ssl_params={"server_hostname": mqtt_server})
mqtt.set_callback(mqtt_callback)
print(mqtt.connect())
print(mqtt.sock)
print(mqtt.ping())
mqtt.subscribe("test")
time.sleep(1)
mqtt.wait_msg()
if cb.isDone:
    print("Done")
