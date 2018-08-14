import logging
import time
from jpype import *
import Settings

logger = logging.getLogger("MQProducer")

__all__ = ['DefaultMQProducer']

DefaultMQProducerJ = JPackage('org.apache.rocketmq.client.producer').DefaultMQProducer
MQClientExceptionJ = JPackage('org.apache.rocketmq.client.producer').MQClientException
SendResultJ = JPackage('org.apache.rocketmq.client.producer').SendResult

class DefaultMQProducer(object):
    """
    """
    def __init__(self, groupName, nameServer):
        jvmPath = getDefaultJVMPath()
        startJVM(
            jvmPath, 
            Settings.JVM_RUN_MODE, 
            Settings.JVM_HEAP_XMS, 
            Settings.JVM_HEAP_XMX, 
            Settings.JVM_HEAP_XMN,
            Settings.JAVA_EXT_DIRS
        )
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
        shutdownJVM()
        pass