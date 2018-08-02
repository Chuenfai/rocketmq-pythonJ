# -*- coding: utf-8 -*-

import sys
import os
import time
sys.path.append(os.path.split(os.path.realpath(__file__))[0] + '/..')
from jpype import *
import settings

jvmPath = getDefaultJVMPath()
startJVM(
    jvmPath, 
    settings.JVM_RUN_MODE, 
    settings.JVM_HEAP_XMS, 
    settings.JVM_HEAP_XMX, 
    settings.JVM_HEAP_XMN,
    settings.JAVA_EXT_DIRS
)

import threading
from rocketmq.DefaultMQProducer import *
from rocketmq.Message import *
from rocketmq.DefaultMQPushConsumer import *
from rocketmq.MessageListener import msgListenerConcurrentlyProxy

# def processMessages(msgs):
#     for msg in msgs:
#         print('[' + msg.getTopic() + '] [' + msg.getMsgId() + '] [' + msg.getBody() + ']')
    
#     return True

# producer = DefaultMQProducer('python_producer', '10.61.2.125:9876')
# producer.start()
# msg = Message('PythonTest', '', '', 'this is a first message from python sdk.'.encode('utf-8'))
# producer.send(msg.getMessage())

def startConsumer():
    consumer = DefaultMQPushConsumer('python_push_consumer', '10.61.2.125:9876')
    consumer.subscribe('PythonTest', '')
    consumer.setClientIP('10.61.2.125')
    consumer.registerMessageListenerConcurrently(msgListenerConcurrentlyProxy)
    consumer.start()
    print('consumer stated')

threading.Thread(target=action,args=(0,)).start()

time.sleep(2 * 1000)
print('main thread end')
# consumer.shutdown()
# producer.shutdown()
# shutdownJVM()
