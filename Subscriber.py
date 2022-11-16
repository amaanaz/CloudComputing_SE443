import paho.mqtt.client as paho
import json as js

# broker = "localhost"
# broker = "test.mosquitto.org"
broker = "10.20.1.95"

# def on_message(client, userdata, msg):
#     print("topic: "+msg.topic+", Msg: "+str(msg.payload))


def get_json_msg(client, userdata, msg):
    a = js.loads(msg.payload)
    print("topic: "+msg.topic +
          '\n'+"StudentID: " + str(a["StudentID"]) +
          '\n'+"Name: " + a["Name"] +
          '\n'+"Surname: " + a["Surname"] +
          '\n' + "Telephone: "+a["Telephone"] +
          '\n' + "Grade: " + str(a["Grade"])
          )


client = paho.Client()
# client.on_message = on_message
client.on_message = get_json_msg
client.connect(broker, 1883)
client.subscribe("se443/midterm2")
client.loop_forever()
