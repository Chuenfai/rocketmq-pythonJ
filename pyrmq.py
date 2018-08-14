""" this is a simple python sdk of RocketMQ(under 4.2.0), which is a packing of Java application.
    So if you want to run it, you should setup the Java Runtime Environment in your 
    machine firstly.
"""

""" Some JVM arguments, you can modify the ROCKETMQ_PATH and JAVA_OPTION
"""
import os
import sys

ROCKETMQ_HOME = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'lib')
JAVA_EXT_DIRS = "-Djava.ext.dirs=" + ROCKETMQ_HOME
JAVA_OPTIONS_DICT = {
    "JVM_HEAP_XMS": "-Xms8g",
    "JVM_HEAP_XMX": "-Xmx8g",
    "JVM_HEAP_XMN": "-Xmn4g",
    "JVM_RUN_MODE": "-server"
}
# JVM_OPTIONS_TUPLE = ('-server', '-Xms256m', '-Xmx256m', '-Xmn128m', JAVA_EXT_DIRS)

""" import Java class from Java package.
"""
from jpype import *

jvmPath = getDefaultJVMPath()
startJVM(
    jvmPath,
    JAVA_OPTIONS_DICT['JVM_RUN_MODE'], 
    JAVA_OPTIONS_DICT['JVM_HEAP_XMS'], 
    JAVA_OPTIONS_DICT['JVM_HEAP_XMX'], 
    JAVA_OPTIONS_DICT['JVM_HEAP_XMN'],
    JAVA_EXT_DIRS
)
# startJVM(
#     jvmPath,
#     JVM_OPTIONS_TUPLE
# )               

_MessageJ = JPackage('org.apache.rocketmq.common.message').Message
_DefaultMQProducerJ = JPackage('org.apache.rocketmq.client.producer').DefaultMQProducer
_DefaultMQPushConsumerJ = JPackage('org.apache.rocketmq.client.consumer').DefaultMQPushConsumer

def buildMessage(topic, tags, keys, body):
    """ body must be type of bytes.
    """
    if not isinstance(body, bytes):
        raise Exception("body must be type of bytes.")
    else:
        return _MessageJ(JString(topic), JString(tags), JString(keys), body)

def buildProducer(groupname, namesrv):
    producer = _DefaultMQProducerJ(JString(groupname))
    producer.setNamesrvAddr(JString(namesrv))
    return producer

def sendMessage(producer, message):
    return producer.send(message)

def startProducer(producer):
    producer.start()

def shutdownProducer(producer):
    producer.shutdown()
    print('producer shutdown.')

def buildPushConsumer(groupname, namesrv):
    consumer = _DefaultMQPushConsumerJ(JString(groupname))
    consumer.setNamesrvAddr(namesrv)
    return consumer

def subscribe(consumer, topic, subexpression):
    consumer.subscribe(JString(topic), JString(subexpression))

def setConsumerClientIP(consumer, clientip):
    """ if there are two more ip address on a machine, you should 
        specify one of address.
    """
    consumer.setClientIP(JString(clientip))

def registerListener(consumer, process):
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
        consumer.registerMessageListener(listener)

def shutdownConsumer(consumer):
    consumer.shutdown()

def shutdownENV():
    print('jvm shutdown.')
    shutdownJVM()
