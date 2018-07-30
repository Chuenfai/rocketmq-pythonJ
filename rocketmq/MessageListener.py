from jpype import *

__all__ = ['msgListenerConcurrentlyProxy']
from Status import *

class MessageListenerConcurrently(object):
    
    def consumeMessage(self, msgs, context):
        for msg in msgs:
            print('[' + msg.getTopic() + '] [' + msg.getMsgId() + '] [' + msg.getBody() + ']')
        return ConsumeConcurrentlyStatus['SUCCESS']

msgListenerConcurrently = MessageListenerConcurrently()
#JProxy("MessageListenerConcurrently", inst = msgListenerConcurrently)
msgListenerConcurrentlyProxy = JProxy(
    "org.apache.rocketmq.client.consumer.listener.MessageListenerConcurrently", 
    inst = msgListenerConcurrently
)

class MessageListenerOrderly(object):
    def consumeMessage(self, msgs, context):
        pass
    pass