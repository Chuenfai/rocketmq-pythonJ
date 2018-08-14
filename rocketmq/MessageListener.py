from jpype import *
from rocketmq.Status import *

__all__ = ['msgListenerConcurrentlyProxy']

class MessageListenerConcurrently:
    
    def consumeMessage(self, msgs, context):
        
        # print('receive msg: ' + str(len(msgs)))
        for msg in msgs:
            print('[' + msg.getTopic() + '] [' + msg.getMsgId() + ']')
        return ConsumeConcurrentlyStatus['SUCCESS']

    def toString(self):
        return "this is message listener concurrently."

msgListenerConcurrently = MessageListenerConcurrently()
# JProxy("MessageListenerConcurrently", inst = msgListenerConcurrently)
msgListenerConcurrentlyProxy = JProxy(
    "org.apache.rocketmq.client.consumer.listener.MessageListenerConcurrently", 
    inst = msgListenerConcurrently
)

class MessageListenerOrderly(object):
    def consumeMessage(self, msgs, context):
        pass
    pass
