import sys
import os
import time
sys.path.append(os.path.split(os.path.realpath(__file__))[0] + '/..')
from pyrmq import *

def processMessages(messages):
    for msg in messages:
        print('[' + msg.getTopic() + '] [' + msg.getMsgId() + '] [' + msg.getBody().decode('utf-8') + ']')
    return True

consumer = buildPushConsumer('python_push_consumer', '10.61.2.125:9876')
subscribe(consumer, 'PythonTest', '')
setConsumerClientIP(consumer, '10.61.2.125')

registerListener(consumer, processMessages)
consumer.start()

while True:
    time.sleep(10)
