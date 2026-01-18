import time

import cbor2
import random
import threading
import paho.mqtt.client as mqtt


BROKER = "localhost"
NUM_BOTS = 10


class PatientBot(threading.Thread):
    def __init__(self, bot_id):
        threading.Thread.__init__(self)
        self.bot_id = f"bot_{bot_id}"
        self.client = mqtt.Client()
        self.running = True

    def run(self):
        try:
            self.client.connect(BROKER, 1883, 60)
        except:
            print(f"[{self.bot_id}] Connection Failed")
            return


        while self.running:
            data = {
                "timestamp": time.time(),
                "heart_rate": int(60 + random.random() * 40),
                "temperature": round(36.5 + random.random(), 1),
                "spo2": int(95 + random.random() * 5)
            }


            payload = cbor2.dumps(data)
            topic = f"health/{self.bot_id}/vitals"

            self.client.publish(topic, payload)


            time.sleep(random.uniform(2.0, 5.0))

    def stop(self):
        self.running = False
        self.client.disconnect()



if __name__ == "__main__":
    print(f"Launching {NUM_BOTS} virtual patients...")
    bots = []


    for i in range(NUM_BOTS):
        bot = PatientBot(i)
        bot.start()
        bots.append(bot)
        time.sleep(0.05)

    print(" Crowd Simulation Active. Press Ctrl+C to stop.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping bots...")
        for bot in bots:
            bot.stop()
        print("Simulation Ended.")