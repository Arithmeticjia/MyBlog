import stomp
import time
import sys


class SampleListener(stomp.ConnectionListener):
    def on_message(self, headers, msg):
        print(msg)

    def on_error(self, headers, message):
        print("headers:{0['destination']}, message:{1}".format(headers, message))


conn = stomp.Connection10()

conn.set_listener('SampleListener', SampleListener())

conn.connect()

conn.subscribe('SampleQueue')

time.sleep(1)
while True:
    pass

# conn.disconnect()