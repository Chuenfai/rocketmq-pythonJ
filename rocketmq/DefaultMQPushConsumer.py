from jpype import *
import logging
logger = logging.getLogger('MQPushConsumer')
from Status import *

__all__ = ['DefaultMQPushConsumer']

_DefaultMQPushConsumerJ = JPackage('org.apache.rocketmq.client.consumer').DefaultMQPushConsumer

class DefaultMQPushConsumer(object):

    def __init__(self, groupName, nameServer):
        self._consumerGroup = groupName
        self._namesrvAddr = nameServer
        self.__consumer = _DefaultMQPushConsumerJ(JString(groupName))
        self.__consumer.setNamesrvAddr(JString(nameServer))

    def subscribe(self, topic, subExpression):
        self.__consumer.subscribe(JString(topic), JString(subExpression))

    def start(self):
        self.__consumer.start()

    def getClientIP(self):
        return self.__consumer.getClientIP()

    def registerMessageListenerConcurrently(self, func):
        def _consumeMessage(msgs, context):
            if func(msgs):
                return ConsumeConcurrentlyStatus['SUCCESS']
            else:
                return ConsumeConcurrentlyStatus['RECONSUME_LATER']
        print('register listener...')
        listener = JProxy(
            "org.apache.rocketmq.client.consumer.listener.MessageListenerConcurrently", 
            dict={'consumeMessage': _consumeMessage}
        )
        self.__consumer.registerMessageListener(listener)
    
    def shutdown(self):
        self.__consumer.shutdown()

    pass