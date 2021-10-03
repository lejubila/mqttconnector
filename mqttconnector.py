#
# Script python che implementa un bridge mqtt verso piGarden e piGuardian:
# vengono intecettati i messaggi mqtt publicati sui topic configurati nel file ini e vengono inoltrati ai server socket di piGarden e piGuardian
#
# Author: david.bigagli@gmail.com
# Url: https://github.com/lejubila/mqttconnector
#
# Installare libreria paho-mqtt, configparser:
# sudo pip install paho-mqtt configparser
#

import paho.mqtt.client as mqttClient
import time
import subprocess
import configparser
import calendar
import json
import sys

def on_connect(client, userdata, flags, rc):

    if rc == 0:

        print("Connected to broker")

        global Connected                # Use global variable
        Connected = True                # Signal connection 



        if pigarden_enabled == "1":
           topic = pigarden_topic+"/"+subtopic_command
           client.subscribe(topic)
           print "subscribe: "+topic

           if len(pigarden_ble_bridge) > 0:
              for topic, item in pigarden_ble_bridge.items():
                  client.subscribe(topic)
                  print "subscribe: "+topic

        if piguardian_enabled == "1":
           topic = piguardian_topic+"/"+subtopic_command
           client.subscribe(topic)
           print "subscribe: "+topic

           if len(piguardian_perimetral) > 0:
              for topic, item in piguardian_perimetral.items():
                  client.subscribe(topic)
                  print "subscribe: "+topic

           if len(piguardian_pir) > 0:
              for topic, item in piguardian_pir.items():
                  client.subscribe(topic)
                  print "subscribe: "+topic

           if len(piguardian_tamper) > 0:
              for topic, item in piguardian_tamper.items():
                  client.subscribe(topic)
                  print "subscribe: "+topic


    else:

        print("Connection failed")

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print "Unexpected MQTT disconnection. Will auto-reconnect"

def on_message(client, userdata, message):
    print "Topic           : " + message.topic
    print "Message received: " + message.payload

    #if message.topic.startswith(pigarden_topic+"/command/"):
    if message.topic == (pigarden_topic+"/"+subtopic_command):
        print "pigarden command: " + message.payload
        cmd = ""
        cmd = message.payload
        if pigarden_user != "" and pigarden_pwd != "":
            cmd = pigarden_user + '\n' + pigarden_pwd + '\n' + cmd 
        
        #p = subprocess.Popen([ path_connector + pigarden_exec_command, cmd, pigarden_path ], stdout=subprocess.PIPE)
        p = subprocess.Popen([ path_connector + pigarden_exec_command, cmd, pigarden_host, pigarden_port ], stdout=subprocess.PIPE)
        (output, err) = p.communicate()
        
        ## Wait for date to terminate. Get return returncode ##
        p_status = p.wait()
        print "Command : '" + cmd + "'"
        print "Command output : ", output
        print "Command exit status/return code : ", p_status

	if pigarden_result_enable== 1:
	    client.publish(pigarden_topic+"/"+subtopic_result, output, pigarden_topic_result_qos, pigarden_topic_result_retain)


    if len(pigarden_ble_bridge) > 0:
        for topic, item in pigarden_ble_bridge.items():
            payload = ""
            if message.topic == topic:
                try:
                    json_payload = json.loads(message.payload)
                    print "pigarden_ble_bridge: ", json_payload

                    if json_payload.has_key(item['sensor_name']):

                        # Valuta l'umidita'
                        if json_payload[item['sensor_name']].has_key(item['moisture_name']) and (
                            type(json_payload[item['sensor_name']][item['moisture_name']]) == int or 
                            type(json_payload[item['sensor_name']][item['moisture_name']]) == float
                        ):
                            cmd = "sensor_status_set " + item['alias'] + " moisture " + str(json_payload[item['sensor_name']][item['moisture_name']])
                            if pigarden_user != "" and pigarden_pwd != "":
                                cmd = pigarden_user + '\n' + pigarden_pwd + '\n' + cmd 
        
                            p = subprocess.Popen([ path_connector + pigarden_exec_command, cmd, pigarden_host, pigarden_port ], stdout=subprocess.PIPE)
                            (output, err) = p.communicate()
        
                            ## Wait for date to terminate. Get return returncode ##
                            p_status = p.wait()
                            print "Command : '" + cmd + "'"
                            print "Command output : ", output
                            print "Command exit status/return code : ", p_status

                        # Valuta la temperatura
                        if json_payload[item['sensor_name']].has_key(item['temperature_name']) and (
                            type(json_payload[item['sensor_name']][item['temperature_name']]) == int or 
                            type(json_payload[item['sensor_name']][item['temperature_name']]) == float
                        ):
                            cmd = "sensor_status_set " + item['alias'] + " temperature " + str(json_payload[item['sensor_name']][item['temperature_name']])
                            if pigarden_user != "" and pigarden_pwd != "":
                                cmd = pigarden_user + '\n' + pigarden_pwd + '\n' + cmd 
        
                            p = subprocess.Popen([ path_connector + pigarden_exec_command, cmd, pigarden_host, pigarden_port ], stdout=subprocess.PIPE)
                            (output, err) = p.communicate()
        
                            ## Wait for date to terminate. Get return returncode ##
                            p_status = p.wait()
                            print "Command : '" + cmd + "'"
                            print "Command output : ", output
                            print "Command exit status/return code : ", p_status

                        # Valuta la illuminazione
                        if json_payload[item['sensor_name']].has_key(item['illuminance_name']) and (
                            type(json_payload[item['sensor_name']][item['illuminance_name']]) == int or 
                            type(json_payload[item['sensor_name']][item['illuminance_name']]) == float
                        ):
                            cmd = "sensor_status_set " + item['alias'] + " illuminance " + str(json_payload[item['sensor_name']][item['illuminance_name']])
                            if pigarden_user != "" and pigarden_pwd != "":
                                cmd = pigarden_user + '\n' + pigarden_pwd + '\n' + cmd 
        
                            p = subprocess.Popen([ path_connector + pigarden_exec_command, cmd, pigarden_host, pigarden_port ], stdout=subprocess.PIPE)
                            (output, err) = p.communicate()
        
                            ## Wait for date to terminate. Get return returncode ##
                            p_status = p.wait()
                            print "Command : '" + cmd + "'"
                            print "Command output : ", output
                            print "Command exit status/return code : ", p_status

                        # Valuta la fertilita'
                        if json_payload[item['sensor_name']].has_key(item['fertility_name']) and (
                            type(json_payload[item['sensor_name']][item['fertility_name']]) == int or 
                            type(json_payload[item['sensor_name']][item['fertility_name']]) == float
                        ):
                            cmd = "sensor_status_set " + item['alias'] + " fertility " + str(json_payload[item['sensor_name']][item['fertility_name']])
                            if pigarden_user != "" and pigarden_pwd != "":
                                cmd = pigarden_user + '\n' + pigarden_pwd + '\n' + cmd 
        
                            p = subprocess.Popen([ path_connector + pigarden_exec_command, cmd, pigarden_host, pigarden_port ], stdout=subprocess.PIPE)
                            (output, err) = p.communicate()
        
                            ## Wait for date to terminate. Get return returncode ##
                            p_status = p.wait()
                            print "Command : '" + cmd + "'"
                            print "Command output : ", output
                            print "Command exit status/return code : ", p_status

                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    print "Error into pigarden_ble_bridge. Exception type:", exc_type, " --- line number: ", exc_tb.tb_lineno
                    print "Message.payload: ", message.payload
                    print ""

		print ""





    if message.topic == (piguardian_topic+"/"+subtopic_command):
        print "piguardian command: " + message.payload
        cmd = ""
        cmd = message.payload
        if piguardian_user != "" and piguardian_pwd != "":
            cmd = piguardian_user + '\n' + piguardian_pwd + '\n' + cmd 
        
        #p = subprocess.Popen([ path_connector + piguardian_exec_command, cmd, piguardian_path ], stdout=subprocess.PIPE)
        p = subprocess.Popen([ path_connector + piguardian_exec_command, cmd, piguardian_host, piguardian_port ], stdout=subprocess.PIPE)
        (output, err) = p.communicate()
        
        ## Wait for date to terminate. Get return returncode ##
        p_status = p.wait()
        print "Command : '" + cmd + "'"
        print "Command output : ", output
        print "Command exit status/return code : ", p_status

	if piguardian_result_enable== 1:
	    client.publish(piguardian_topic+"/"+subtopic_result, output, piguardian_topic_result_qos, piguardian_topic_result_retain)

    if len(piguardian_perimetral) > 0:
        for topic, item in piguardian_perimetral.items():
            payload = ""
            if message.topic == topic and message.payload == item["normal"]:
                payload = "perimetral_set_mqttstatus "+item["sensor"]+" 0"
            elif message.topic == topic and message.payload == item["alert"]:
                payload = "perimetral_set_mqttstatus "+item["sensor"]+" 1"
                #payload = "perimetral_set_mqttstatus "+item["sensor"]+" "+str(calendar.timegm(time.gmtime()))
               
            if payload != "":
	        client.publish(piguardian_topic+"/"+subtopic_command, payload, piguardian_topic_result_qos, piguardian_topic_result_retain)

    if len(piguardian_pir) > 0:
        for topic, item in piguardian_pir.items():
            payload = ""
            if message.topic == topic and message.payload == item["normal"]:
                payload = "pir_set_mqttstatus "+item["sensor"]+" 0"
            elif message.topic == topic and message.payload == item["alert"]:
                payload = "pir_set_mqttstatus "+item["sensor"]+" 1"
                #payload = "pir_set_mqttstatus "+item["sensor"]+" "+str(calendar.timegm(time.gmtime()))
               
            if payload != "":
	        client.publish(piguardian_topic+"/"+subtopic_command, payload, piguardian_topic_result_qos, piguardian_topic_result_retain)

    if len(piguardian_tamper) > 0:
        for topic, item in piguardian_tamper.items():
            payload = ""
            if message.topic == topic and message.payload == item["normal"]:
                payload = "tamper_set_mqttstatus "+item["sensor"]+" 0"
            elif message.topic == topic and message.payload == item["alert"]:
                payload = "tamper_set_mqttstatus "+item["sensor"]+" 1"
                #payload = "tamper_set_mqttstatus "+item["sensor"]+" "+str(calendar.timegm(time.gmtime()))
               
            if payload != "":
	        client.publish(piguardian_topic+"/"+subtopic_command, payload, piguardian_topic_result_qos, piguardian_topic_result_retain)




def timestamp(self):
    "Return POSIX timestamp as float"
    if self._tzinfo is None:
        s = self._mktime()
        return s + self.microsecond / 1e6
    else:
        return (self - _EPOCH).total_seconds()





config = configparser.ConfigParser()
config.read('/etc/mqttconnector.ini')


Connected = False   # global variable for the state of the connection

broker_address = config['mqtt']['broker_address']
port = int(config['mqtt']['port'])
user = config['mqtt']['user']
password = config['mqtt']['password']
client_id = config['mqtt']['client_id']
path_connector = config['mqtt']['path_connector']
subtopic_command = config['mqtt']['subtopic_command']
subtopic_result = config['mqtt']['subtopic_result']

pigarden_enabled = config['pigarden']['enabled']
#pigarden_path = config['pigarden']['path']
pigarden_host = config['pigarden']['host']
pigarden_port = config['pigarden']['port']
pigarden_exec_command = config['pigarden']['exec_command']
pigarden_user = config['pigarden']['user']
pigarden_pwd = config['pigarden']['pwd']
pigarden_topic = config['pigarden']['topic']
pigarden_result_enable = int(config['pigarden']['result_enable'])
pigarden_topic_result_qos = int(config['pigarden']['topic_result_qos'])
pigarden_topic_result_retain = int(config['pigarden']['topic_result_retain'])

#ble_bridge_mqtt_sensor= Mi_Flora;tele/ble_bridge/SENSOR;Flora6c7723;Moisture;Temperature;Illuminance;Fertility
pigarden_ble_bridge_mqtt_sensor = config['pigarden']['ble_bridge_mqtt_sensor']

pigarden_ble_bridge = dict()
if pigarden_ble_bridge_mqtt_sensor:
    items = pigarden_ble_bridge_mqtt_sensor.split("\n")
    for item in items:
 	item_data = item.split(";")
        pigarden_ble_bridge[item_data[1]] = dict()
        pigarden_ble_bridge[item_data[1]]['alias'] = item_data[0]
        pigarden_ble_bridge[item_data[1]]['sensor_name'] = item_data[2]
        pigarden_ble_bridge[item_data[1]]['moisture_name'] = item_data[3]
        pigarden_ble_bridge[item_data[1]]['temperature_name'] = item_data[4]
        pigarden_ble_bridge[item_data[1]]['illuminance_name'] = item_data[5]
        pigarden_ble_bridge[item_data[1]]['fertility_name'] = item_data[6]

print pigarden_ble_bridge

piguardian_enabled = config['piguardian']['enabled']
#piguardian_path = config['piguardian']['path']
piguardian_host = config['piguardian']['host']
piguardian_port = config['piguardian']['port']
piguardian_exec_command = config['piguardian']['exec_command']
piguardian_user = config['piguardian']['user']
piguardian_pwd = config['piguardian']['pwd']
piguardian_topic = config['piguardian']['topic']
piguardian_result_enable = int(config['piguardian']['result_enable'])
piguardian_topic_result_qos = int(config['piguardian']['topic_result_qos'])
piguardian_topic_result_retain = int(config['piguardian']['topic_result_retain'])

piguardian_perimetral_mqtt_sensor = config['piguardian']['perimetral_mqtt_sensor']
piguardian_pir_mqtt_sensor = config['piguardian']['pir_mqtt_sensor']
piguardian_tamper_mqtt_sensor = config['piguardian']['tamper_mqtt_sensor']

piguardian_perimetral = dict()
if piguardian_perimetral_mqtt_sensor:
    items = piguardian_perimetral_mqtt_sensor.split("\n")
    for item in items:
	item_data = item.split(";")
        piguardian_perimetral[item_data[1]] = dict()
        piguardian_perimetral[item_data[1]]['sensor'] = item_data[0]
        piguardian_perimetral[item_data[1]]['normal'] = item_data[2]
        piguardian_perimetral[item_data[1]]['alert'] = item_data[3]

piguardian_pir = dict()
if piguardian_pir_mqtt_sensor:
    items = piguardian_pir_mqtt_sensor.split("\n")
    for item in items:
	item_data = item.split(";")
        piguardian_pir[item_data[1]] = dict()
        piguardian_pir[item_data[1]]['sensor'] = item_data[0]
        piguardian_pir[item_data[1]]['normal'] = item_data[2]
        piguardian_pir[item_data[1]]['alert'] = item_data[3]

piguardian_tamper = dict()
if piguardian_tamper_mqtt_sensor:
    items = piguardian_tamper_mqtt_sensor.split("\n")
    for item in items:
	item_data = item.split(";")
        piguardian_tamper[item_data[1]] = dict()
        piguardian_tamper[item_data[1]]['sensor'] = item_data[0]
        piguardian_tamper[item_data[1]]['normal'] = item_data[2]
        piguardian_tamper[item_data[1]]['alert'] = item_data[3]


print piguardian_perimetral
print piguardian_pir
print piguardian_tamper


client = mqttClient.Client(client_id)              # create new instance
client.username_pw_set(user, password=password)    # set username and password
client.on_connect = on_connect                      # attach function to callback
client.on_message = on_message                      # attach function to callback
client.on_disconnect = on_disconnect





print broker_address, port, user, password

client.connect(broker_address, port=port)          # connect to broker

client.loop_start()        #start the loop

while Connected != True:    #Wait for connection
    time.sleep(0.1)





try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print "exiting"
    client.disconnect()
    client.loop_stop()



