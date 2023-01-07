import network
import socket
import time
import json
from umqtt.simple import MQTTClient
import uselect as select

class Message:
    def __init__(self):
        self.isDone=False
        self.msg=""
        self.topic=""
        self.print_screen=""
        self.from_server=""
        
    def log(self):
        subDic={'topic':self.topic,'message':self.msg, 'from':self.from_server}
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
        return str(dic)
        

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
    print('listening on', host)
    while True:
        r, _, _ = select.select([s], [], [], 1.0)
        x+=1
        if x%3 == 0:
            led_blink(1,.1,.5)
        if r:
            count = 0
            cl, addr = s.accept()
            print('\nclient connected from', addr)
            msg.from_server = addr[0]
            request = cl.recv(1024)
            request = request.decode("utf8")
            print("line 66 request = cl.recv(1024)",request)
            requestTopic = request.lower()
            requestMsg = request.lower()
            isValid = all(["topic" in request, "message" in request])
            msg.topic = requestTopic.split("topic")[1].replace(":"," ").strip().split("\n")[0].split(" ")[0] if isValid else "ErrerTopic"
            msg.msg = requestMsg.split("message")[1].replace(":"," ").strip().split("\n")[0].split(" ")[0] if isValid else "ErrerMessage"
            
#             lines = request.split("\n")
#             for line in lines:
#                 if ":" in line:
#                     k, v = line.lower().split(":", 1)
#                     if k.strip() == "topic":
#                         msg.topic = v.strip()
#                     elif k.strip() == "message":
#                         msg.msg = v.strip()
            print(msg.topic)
            print(msg.msg)
        #  .....................................
            mqtt.subscribe(msg.topic)
            print(f"(line79)subcribed to {msg.topic}")
            mqtt.publish(msg.topic, msg.msg)
            print(f"(line86)published message: {msg.msg}")
            time.sleep(3)
            mqtt.wait_msg()
            print(f"(line83)Succesfully waited msg")
        #   ...........................
            if msg.isDone:
                # response = f"<p> Sent: {msg.msg} at Topic : {msg.topic} </p>"
                msg.isDone=False
                response = msg.log()
                msg.msg=""
                msg.topic=""
            # print(response)
            cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
            cl.send(response)
            response=""
            cl.close()
        else:
            print("\r", x, sep="", end="")
            time.sleep(1)
            if x == 60:
                mqtt.publish("refresh", "refresh")
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
#     topic = topic.decode('utf-8')
#     payload = payload.decode('utf-8')
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


    