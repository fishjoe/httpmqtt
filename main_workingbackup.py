import network
import socket
import time
import json
from umqtt.simple import MQTTClient
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
        

# Function to process localtime() into string of date, time and date_and_time 2023-01-10

def dtstr():  
    yyyy, *exYY = time.localtime()    
    mmd, dd, hh, mmt, ss, *_ = [str(i+100)[1:] for i in exYY] # processing value from list to add 0 if value's from 1-9
    dtstr = f"{yyyy}-{mmd}-{dd}"
    tmstr = f"{hh}:{mmt}:{ss}"
    dttm = dtstr +"  " + tmstr
    return dttm, dtstr, tmstr


def make_page(mcu, homepage):
    html = homepage
    host = socket.getaddrinfo(mcu, 80)[0][-1]
    skt = socket.socket()
    print(f"Socket status: {skt}")
    skt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    skt.bind(host)
    skt.listen(1)
    x = 0
    i = 0
    response=""
    print('listening on', host)
    while True:
        r, _, _ = select.select([skt], [], [], 0.5)
        x+=1
        led_blink(1,.2,.3)
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
            if all(["topic" in request, "message" in request]):
                me.topic = str(request.split("topic")[1].replace(":"," ").strip().split("\n")[0].split(" ")[0].replace(" ","").replace("\n",""))[:-1]
                me.mess = str(request.split("message")[1].replace(":"," ").strip().split("\n")[0].split(" ")[0].replace(" ","").replace("\n",""))[:-1]               
                i+=1
                print(f"Attempts {i}")
                print(me.mess)
                mqtt = MQTTClient(client_id=me.client_id, server=me.mqtt_server, port=me.mqtt_port, user=me.mqtt_username, password=me.mqtt_psd, ssl=True, ssl_params={"server_hostname": me.mqtt_server})
                mqtt.set_callback(mqtt_callback)
                if mqtt.connect() == 0:
                    print(f"connected to {me.mqtt_server}...") 
                    mqtt.subscribe(me.topic)
                    mqtt.publish(me.topic, me.mess)
                    mqtt.wait_msg()
                    if me.isDone:
                        me.isDone=False
                        response = f"published to\n topic: {me.topic}\n message: {me.mess}"
                        me.mess=""
                        me.topic=""
                        thistopic=""
            else:
                response = "Error"
                led_blink(5,.2,.2)
            cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
            cl.send(response)
            response=""
            cl.close()
        else:
            print("\r", dtstr()[0], sep="", end="")

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
    print(topic, payload)
    me.isDone = True
    print("\nmqqt response received....callback triggered")

if __name__ == "__main__":
    me=Data()
#     mqtt = MQTTClient(client_id=me.client_id, server=me.mqtt_server, port=me.mqtt_port, user=me.mqtt_username, password=me.mqtt_psd, ssl=True, ssl_params={"server_hostname": me.mqtt_server})
#     mqtt.set_callback(mqtt_callback)
#     mqtt.connect()
#     print(mqtt.connect())
#     print(mqtt.sock_mqtt)
    print("Connecting to http ......")
    wlan=network.WLAN()
    if not wlan.isconnected():
        print("Please connected to WIFI")
    else:
        page = make_page(wlan.ifconfig()[0], xml)
    