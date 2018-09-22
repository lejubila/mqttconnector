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

def on_connect(client, userdata, flags, rc):

    if rc == 0:

        print("Connected to broker")

        global Connected                # Use global variable
        Connected = True                # Signal connection 



        if pigarden_enabled == "1":
           topic = pigarden_topic+"/"+subtopic_command
           client.subscribe(topic)
           print "subscribe: "+topic

        if piguardian_enabled == "1":
           topic = piguardian_topic+"/"+subtopic_command
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



