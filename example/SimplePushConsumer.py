import sys
import os
import time
sys.path.append(os.path.split(os.path.realpath(__file__))[0] + '/..')
from pyrmq import *

NUMBER = 0

def processMessages(messages):
    global NUMBER
    for msg in messages:
        print('[' + msg.getTopic() + '] [' + msg.getMsgId() + '] [' + NUMBER + ']')
        NUMBER += 1
    return True

consumer = buildPushConsumer('python_push_consumer', '10.61.2.125:9876')
subscribe(consumer, 'PythonBenchmarkTest', '')
setConsumerClientIP(consumer, '10.61.2.125')

registerListener(consumer, processMessages)
startConsumer(consumer)

while True:
    time.sleep(10)
