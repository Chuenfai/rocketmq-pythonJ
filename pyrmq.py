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
from inspect import isfunction

jvmPath = getDefaultJVMPath()
startJVM(
    jvmPath,
    "-Xms8g", 
    '-Xmx8g', 
    '-Xmn4g', 
    '-server',
    '-XX:+UseG1GC',
    '-XX:G1HeapRegionSize=16m',
    '-XX:G1ReservePercent=25',
    '-XX:InitiatingHeapOccupancyPercent=30',
    '-XX:SoftRefLRUPolicyMSPerMB=0',
    '-XX:SurvivorRatio=8'
    '-XX:+UseGCLogFileRotation',
    '-XX:NumberOfGCLogFiles=5',
    '-XX:GCLogFileSize=30m',
    '-XX:MaxDirectMemorySize=15g',
    '-XX:-OmitStackTraceInFastThrow',
    '-XX:+AlwaysPreTouch',
    '-XX:-UseLargePages',
    '-XX:-UseBiasedLocking',
    JAVA_EXT_DIRS
)
# startJVM(
#     jvmPath,
#     JVM_OPTIONS_TUPLE
# )               

_MessageJ = JPackage('org.apache.rocketmq.common.message').Message
_DefaultMQProducerJ = JPackage('org.apache.rocketmq.client.producer').DefaultMQProducer
_DefaultMQPushConsumerJ = JPackage('org.apache.rocketmq.client.consumer').DefaultMQPushConsumer
_SendStatusJ = JPackage('org.apache.rocketmq.client.producer').SendStatus
_ConsumerConcurrentlyStatusJ = JPackage('org.apache.rocketmq.client.consumer.listener').ConsumerConcurrentlyStatus
_ConsumeOrderlyStatusJ = JPackage('org.apache.rocketmq.client.consumer.listener').ConsumeOrderlyStatus

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

def buildPushConsumer(groupname, namesrv):
    consumer = _DefaultMQPushConsumerJ(JString(groupname))
    consumer.setNamesrvAddr(namesrv)
    return consumer

def startConsumer(consumer):
    consumer.start()

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
                print(1)
                return _ConsumerConcurrentlyStatusJ.SUCCESS
            else:
                return _ConsumerConcurrentlyStatusJ.RECONSUME_LATER
        listener = JProxy(
            "org.apache.rocketmq.client.consumer.listener.MessageListenerConcurrently", 
            dict={'consumeMessage': consumeMessage_}
        )
        consumer.registerMessageListener(listener)

def shutdownConsumer(consumer):
    consumer.shutdown()

def shutdownENV():
    shutdownJVM()
