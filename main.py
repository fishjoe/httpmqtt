import network
import socket
import time
import json
from umqtt.simple import MQTTClient

class Message:
    def __init__(self):
        self.isDone=False
        self.msg=""
        self.topic=""
        self.print_screen=""
        self.from_server=""
        
    def log(self):
        subDic={'topic':self.topic,'message':self.msg}
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
        print(dic)
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



def make_page(server, homepage):
    html = homepage
    host = socket.getaddrinfo(server, 80)[0][-1]
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(host)
    s.listen(1)
    x = 0
    response=""
    while True:
        x+=1
        print('listening on', host)
        count = 0
        cl, addr = s.accept()
        print('client connected from', addr)
        request = cl.recv(1024)
        request = request.decode("utf8")
        # request = str(request)
        lines = request.split("\n")
        for line in lines:
            if ":" in line:
                k, v = line.lower().split(":", 1)
                if k.strip() == "topic":
                    msg.topic = v.strip()
                elif k.strip() == "message":
                    msg.msg = v.strip()
    #  .....................................             
        mqtt.publish(msg.topic, msg.msg)
        time.sleep(1)
        mqtt.wait_msg()
    #   ...........................
        if msg.isDone:
            response = f"<p> Sent: {msg.msg} at Topic : {msg.topic} </p>"
            msg.isDone=False
            msg.log()
            msg.msg=""
            msg.topic=""
            
        # print(response)
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        response=""
        cl.close()

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
    led_blink(2,.5,.5)
    topic = topic.decode('utf-8')
    payload = payload.decode('utf-8')
    msg.isDone = True
    print("\n'mqqt' received....")

def mqtt_connect(**kwargs):
        client = MQTTClient(**kwargs)
        # Initializing MQTT callback attributes
        client.set_callback(mqtt_callback)
        client.connect()
        print('Connected to ......... %s MQTT Broker' % kwargs["server"])
        client.subscribe("test")
        print('MQTT is ready. Subscribed to "test"', "\n")
        return client

if __name__ == "__main__":
    mqtt_server = 'dc87a3d9523a42798c3d086fd8acbdb5.s1.eu.hivemq.cloud'
    mqtt_port = 8883
    client_id = 'PicoW'
    mqtt_username = 'fishjoe'
    mqtt_psd = 'fish8264'
    topic_pub = 'test'
    topic_msg = 'PicoStart'
    msg=Message()
    mqtt = mqtt_connect(client_id=client_id, server=mqtt_server, port=mqtt_port, user=mqtt_username,
                         password=mqtt_psd, ssl=True, ssl_params={"server_hostname": mqtt_server})   
    print("Connecting to http ......")
    wlan=network.WLAN()
    if not wlan.isconnected():
        print("Please connected to WIFI")
    else:
        page = make_page(wlan.ifconfig()[0], xml)


    