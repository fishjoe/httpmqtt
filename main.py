import network
import socket
import time
import json
from simple_mqtt_modified import MQTTClient
import uselect as select

class Data:
    def __init__(self):
        self.isDone=False
        self.mess=""
        self.topic=""
        self.print_screen=""
        self.from_server=""
        self.mqtt_server = 'dc87a3d9523a42798c3d086fd8acbdb5.s1.eu.hivemq.cloud'
        self.mqtt_port = 8883
        self.client_id = 'PicoW'
        self.mqtt_username = 'fishjoe2'
        self.mqtt_psd = 'fishjoe2'
        self.topic_pub = 'test'
        self.topic_mess = 'PicoStart'
        
        
    def log(self):
        subDic={'topic':self.topic,'message':self.mess, 'from':self.from_server}
        timestr, *_ = dtstr()
        dicNew={timestr:subDic}
        dic={}
        text=""
        try:
            with open("log.json", "r+") as jsonS:
                dic = json.load(jsonS)
        except:
            pass
        dic.update(dicNew)
#         print(dic)
        if len(dic) >= 100:
            dic.popitem()
        with open("log.json", "w") as file:
            json.dump(dic, file)
        

def dtstr():  
    yyyy, *exYY = time.localtime()    
    mmd, dd, hh, mmt, ss, *_ = [str(i+100)[1:] for i in exYY]
    dtstr = f"{yyyy}-{mmd}-{dd}"
    tmstr = f"{hh}:{mmt}:{ss}"
    dttm = dtstr +"  " + tmstr
    return dttm, dtstr, tmstr


def make_page(mcu, homepage):
    html = homepage
    host = socket.getaddrinfo(mcu, 80)[0][-1]
    skt = socket.socket()
    print(skt)
    skt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    skt.bind(host)
    skt.listen(1)
    x = 0
    response=""
    print('listening on', host)
    while True:
        r, _, _ = select.select([skt], [], [], 1.0)
        x+=1
        if x%3 == 0:
            led_blink(1,.1,.5)
        if r:
            count = 0
            cl, addr = skt.accept()
            print('\nclient connected from', addr[0])
            me.from_server = addr[0]
            
            # use try except block to catch noise signal. ocasionally random ip would send noise signal
            # and cannot be parsed. This block filters it out.
            
            try:
                request = cl.recv(1024)
                request = request.decode("utf8")
                request = request.lower()
            except:
                request = ""
                
            # only both "topic" and "message" presenting would trigger the process go ahead.
            isValid = all(["topic" in request, "message" in request])
            me.topic = request.split("topic")[1].replace(":"," ").strip().split("\n")[0].split(" ")[0] if isValid else "ErrerTopic"
            me.mess = request.split("message")[1].replace(":"," ").strip().split("\n")[0].split(" ")[0] if isValid else "ErrerMessage"
            print(me.mess)
            print(me.topic)
            
            # TODO current design of the program is still experimental. Random error would occur.
            
            # This may becaused by the conflict of sockets process between to functionality. Http
            # requests gathering and MQTT sending / receiving confirmation. May update to fix the bugs.
            
            print(mqtt.sock_mqtt)
            mqtt.set_callback(mqtt_callback)
            print(mqtt.connect())
            mqtt.subscribe("test")
            mqtt.publish(me.topic, me.mess)
            mqtt.wait_msg()
            print("published")
            if me.isDone:
                me.isDone=False
                response = "Suceed"
                me.mess=""
                me.topic=""   
            cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
            cl.send(response)
            response=""
            cl.close()
        else:
            print("\r", x, sep="", end="")
            time.sleep(1)
            if x == 60:
                mqtt.publish("refreshed", "refreshed")
                print("\nmqtt refreshed")
                led_blink(5,.1,.1)
                x=0

xml ="""<xml>
<test><p>this is test</p>
</test>
</xml>"""

led = machine.Pin('LED', machine.Pin.OUT)

def led_blink(qty, on, off):
    if led.value() == 0:
        for i in range(qty):
            led.on()
            time.sleep(on)
            led.off()
            time.sleep(off)
    else:
        for i in range(qty):
            led.off()
            time.sleep(off)
            led.on()
            time.sleep(on)
    

def mqtt_callback(topic, payload):
    led_blink(3,.2,.2)
    me.isDone = True
    print("\n'mqqt' received....")

if __name__ == "__main__":
    me=Data()
    mqtt = MQTTClient(client_id=me.client_id, server=me.mqtt_server, port=me.mqtt_port, user=me.mqtt_username, password=me.mqtt_psd, ssl=True, ssl_params={"server_hostname": me.mqtt_server})
    mqtt.set_callback(mqtt_callback)
    print(mqtt.connect())
#     print(mqtt.sock_mqtt)
    print("Connecting to http ......")
    wlan=network.WLAN()
    if not wlan.isconnected():
        print("Please connected to WIFI")
    else:
        page = make_page(wlan.ifconfig()[0], xml)
    