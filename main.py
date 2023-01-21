#  TODO improve loging by combining print and log function



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
        self.response = ''
        
        
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
        while len(dic) >= 20:
            dic.popitem()
        with open("log.json", "w") as file:
            json.dump(dic, file)
        

# Function to process localtime() into string of date, time and date_and_time 2023-01-10

def dtstr():  
    yyyy, *exYY = time.localtime()    
    mmd, dd, hh, mmt, ss, *_ = [str(i+100)[1:] for i in exYY] # processing value from list to add 0 if value's from 1-9
    dtstr = f"{yyyy}-{mmd}-{dd}"
    tmstr = f"{hh}:{mmt}:{ss}"
    dttm = dtstr + "\t" + tmstr
    return dttm, dtstr, tmstr


def mqtt_send(mqtt, tpc, msg, r=0):
    
#     while not me.isDone:
#         try:
#             print(f"\t\t\t\t{mqtt.connect()}")
#             mqtt.subscribe(tpc)
#             mqtt.publish(tpc, msg)
#             print(f"\t\t{dtstr()[2]}\tconnected to {me.mqtt_server}...")
#         except OSError:
#             time.sleep(1)
    while True:
        try:
            mqtt.publish(tpc, msg)
            print(f"\t\t{dtstr()[2]}\tconnected to {me.mqtt_server}...")
            break
        except OSError:
            mqtt.connect()
            time.sleep(2)
    
    
   # TODO need to fix
    
    
    if me.isDone:
        me.isDone=False
        me.response = f"published to\n\n topic : {me.topic}\n message : {me.mess}"
        me.mess=""
        me.topic=""
    return mqtt
    

def make_page(mqtt, mcu, homepage):
    html = homepage
    host = socket.getaddrinfo(mcu, 80)[0][-1]
    skt = socket.socket()
    print(f"\t\t\t\tSocket status: {skt}")
    skt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    skt.bind(host)
    skt.listen(1)
    x = 0
    count = 0
    me.response=""
    print('\t\t\t\tlistening on', host)
    while True:
        r, _, _ = select.select([skt], [], [], 0.5)
        x+=1
        led_blink(1,.2,.3)
        if r: # kick in main cyle when http request received
            count+=1
            cl, addr = skt.accept()
            print("\r\t\t", dtstr()[2], "\tclient connected from ", addr[0], sep="")
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
                me.topic = str(request.split("topic")[1].replace(":"," ").strip().replace("\n"," ").replace("\r", " ").split(" ")[0])
                me.mess = str(request.split("message")[1].replace(":"," ").strip().replace("\n"," ").replace("\r", " ").split(" ")[0])
                print(f"\t\t{dtstr()[2]}\tTopic: {me.topic}  Message: {me.mess}")
                mqtt = mqtt_send(mqtt, me.topic, me.mess)
            else:
                print("***********ERROR MSG**********\n\n", request, "\n\n")
                me.response = "Error"
                led_blink(5,.2,.2)
            print(f"\t\t{dtstr()[2]}\tSending feedback to Http request......")
            cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
            print(me.response)
            cl.send(me.response)
            print(f"\t\t\t\tSent, Complete {count} attempts at {x} cycle")
            me.response=""
            cl.close()
        else:
#             print("\r\t\t", dtstr()[2], "\t " if x%3==2 else "\t.", "." if x%3==1 else " ", sep="", end="")
            tdstr = dtstr()[2]
            if tdstr[-1:] =="0":
                print("\r\t\t", tdstr, "\t", x, sep="", end="")
            

           
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
    print(f"\t\t{dtstr()[2]}\tMQTT response received....callback triggered")

if __name__ == "__main__":
    me=Data()
    mqtt = MQTTClient(client_id=me.client_id, server=me.mqtt_server, port=me.mqtt_port, user=me.mqtt_username, password=me.mqtt_psd, ssl=True, ssl_params={"server_hostname": me.mqtt_server})
    mqtt.set_callback(mqtt_callback)
    mqtt.connect()
#     print(mqtt.connect())
#     print(mqtt.sock_mqtt)
    
    
    wlan=network.WLAN()
    *_, wlan_mode, wlan_sta, wlan_ip = str(wlan).replace("<","").replace(">","").split(" ")
    print(f"{dtstr()[0]}\tWIFI is {wlan_sta}")
    print(f"\t\t\t\tConnecting to http ......")
    if not wlan.isconnected():
        print("Please connected to WIFI")
    else:
        page = make_page(mqtt, wlan.ifconfig()[0], xml)
    