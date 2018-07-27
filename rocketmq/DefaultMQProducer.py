from jpype import *
import logging
import time

logger = logging.getLogger("MQProducer")

__all__ = ['DefaultMQProducer']

DefaultMQProducerJ = JPackage('org.apache.rocketmq.client.producer').DefaultMQProducer
MQClientExceptionJ = JPackage('org.apache.rocketmq.client.producer').MQClientException
SendResultJ = JPackage('org.apache.rocketmq.client.producer').SendResult

class DefaultMQProducer(object):

    def __init__(self, groupName, nameServer):
        self.__producerGroup = groupName
        self.__nameServer = nameServer
        self.__producer = DefaultMQProducerJ(JString(groupName))
        self.__producer.setNamesrvAddr(JString(nameServer))
        

    def start(self):
        self.__producer.start()
        pass

    def send(self, message):
        return self.__producer.send(message)

    def shutdown(self):
        self.__producer.shutdown()
        pass