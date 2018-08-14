"""
"""

import logging
from inspect import isfunction
from jpype import *
import Settings

__all__ = ['DefaultMQPushConsumer']

__DefaultMQPushConsumerJ = JPackage('org.apache.rocketmq.client.consumer').DefaultMQPushConsumer

class DefaultMQPushConsumer:
    """
    """

    def __init__(self, groupname, namesrv):
        """
        """
        self.__consumerGroup = groupname
        self.__namesrvAddr = namesrv
        self.__consumer = __DefaultMQPushConsumerJ(JString(groupname))
        self.__consumer.setNamesrvAddr(JString(namesrv))

    def subscribe(self, topic, subexpression):
        self.__consumer.subscribe(JString(topic), JString(subexpression))

    def start(self):
        self.__consumer.start()

    def getClientIP(self):
        return self.__consumer.getClientIP()

    def setClientIP(self, clientip):
        """ if there are two more ip address on a machine, you should 
            specify one of address.
        """
        self.__consumer.setClientIP(JString(clientip))

    def registerMessageListenerConcurrently(self, process):
        """ process must be a function and must return a bool value.
        """
        if not isfunction(process):
            raise Exception("second argument must be a function.")
        else:
            def consumeMessage_(messages, context):
                if process(messages):
                    return ConsumeConcurrentlyStatus['SUCCESS']
                else:
                    return ConsumeConcurrentlyStatus['RECONSUME_LATER']
            listener = JProxy(
                "org.apache.rocketmq.client.consumer.listener.MessageListenerConcurrently", 
                dict={'consumeMessage': consumeMessage_}
            )
            self.__consumer.registerMessageListener(listener)
    
    def shutdown(self):
        self.__consumer.shutdown()

    pass