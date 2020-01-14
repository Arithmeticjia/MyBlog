import stomp
import sys
import time

conn = stomp.Connection()
conn.connect('admin', 'admin', wait=True)
# send queue name 'test'
conn.send(body=''.join(sys.argv[1:]), destination='/queue/SampleQueue')
# send message
for i in range(10):
    # 第一个参数：队列的名称
    # 第二个参数：消息的内容
    conn.send("SampleQueue", "message{0}:{1}".format(i, i))
    time.sleep(3)
conn.disconnect()