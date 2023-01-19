from simple_mqtt_modified import MQTTClient
import time

class CB:
    def __init__(self):
        self.isDone = False
cb=CB()    

# Essential coding blocks

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

def dtstr():  
    yyyy, *exYY = time.localtime()    
    mmd, dd, hh, mmt, ss, *_ = [str(i+100)[1:] for i in exYY] # processing value from list to add 0 if value's from 1-9
    dtstr = f"{yyyy}-{mmd}-{dd}"
    tmstr = f"{hh}:{mmt}:{ss}"
    dttm = dtstr + "\t" + tmstr
    return dttm, dtstr, tmstr

def timer():
    print(time.mktime(time.localtime()))
    # unfishineshed 

# essential coding block ends



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

mqtt=MQTTClient(client_id=client_id, server=mqtt_server, port=mqtt_port, user=mqtt_username,password=mqtt_psd, ssl=True, ssl_params={"server_hostname": mqtt_server})
mqtt.set_callback(mqtt_callback)
print(mqtt.connect())
print(mqtt.ping())
mqtt.subscribe("test")
att=1
timer_start = time.mktime(time.localtime())
while True:
#     if att%60 == 0: # 265 sec
#     if att%30 ==0: #141
    if att%120 == 0: # 651 sec
        print("")
        mqtt.publish("test", f"{str(att)+dtstr()[1]}__{dtstr()[2]}")
        mqtt.wait_msg()
        if cb.isDone:
            print("Done")
            cb.isDone=False
    else:
        print("\r", dtstr()[0], "\tCyclye ---  ", time.mktime(time.localtime())-timer_start, sep="", end="")
    att+=1
    led_blink(1,.2,.8)
        
    
