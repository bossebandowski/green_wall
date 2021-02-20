from flask import Flask, render_template, request, redirect
import paho.mqtt.client as mqtt
from setup import *

app = Flask(__name__)
LAST_MSG = "no message yet"
sensors = [0, -1, 69]
thresholds = [50, 50, 50]
BROKER_ADDRESS = get_broker_addr()


def set_last_message(content):
    global LAST_MSG
    LAST_MSG = content

@app.route('/')
def hello_world():
    return render_template("index.html", msg=LAST_MSG, sensors=sensors, thresholds=thresholds)

@app.route('/threshold_req', methods=["POST"])
def set_threshold():
    id = request.form['id']
    val = request.form['val']
    print("in here")
    global thresholds
    try:
        thresholds[int(id)] = int(val)
        print("Successfully updated threholds")
    except Exception as e:
        print(e)
    return redirect("/", code=302)

def on_connect(client, userdata, flags, rc):
    print("subscribed to readings")
    client.subscribe('readings')

def on_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    print("got message reading", data['topic'])
    print("content:", data['payload'])
    set_last_message(data['payload'])

if __name__ == '__main__':
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER_ADDRESS)
    client.loop_start()
    app.run(host="0.0.0.0", port=5000, debug=False)