from jpype import *

__all__ = ['msgListenerConcurrentlyProxy']
from Status import *

class MessageListenerConcurrently(object):
    
    def consumeMessage(self, msgs, context):
        try:
            print('receive msg: ' + str(len(msgs)))
            # for msg in msgs:
            #     print type(msg)
            #         # print('[' + msg.getTopic() + ']')
        except jpype.JException(java.lang.RuntimeException):
            print("Caught the runtime exception : " + JavaException.message())
            print(JavaException.stackTrace())
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