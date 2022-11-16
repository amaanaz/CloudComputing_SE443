import paho.mqtt.client as paho
import json as js

broker = "10.20.1.95"
# broker = "localhost"
# broker = "test.mosquitto.org"

x = {"StudentID": 200226,
     "Name": "Amaan",
     "Surname": "Zubairi",
     "Telephone": "7418529630",
     "Grade": 97
     }

msg = js.dumps(x)

client = paho.Client()
client.connect(broker, 1883)

# client.publish("se443/midterm2", "Zubairi")
client.publish("se443/midterm2", msg)
