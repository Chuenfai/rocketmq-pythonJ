import sys
import os
sys.path.append(os.path.split(os.path.realpath(__file__))[0] + '/..')

# print(sys.path)

# # from rocketmq import Settings

# from jpype import *

# jvmPath = getDefaultJVMPath()
# startJVM(
#     jvmPath, 
#     Settings.JVM_RUN_MODE, 
#     Settings.JVM_HEAP_XMS, 
#     Settings.JVM_HEAP_XMX, 
#     Settings.JVM_HEAP_XMN,
#     Settings.JAVA_EXT_DIRS
# )
# ROCKETMQ_HOME = os.path.split(os.path.realpath(__file__))[0] + '/lib'
# JAVA_EXT_DIRS = "-Djava.ext.dirs=" + ROCKETMQ_HOME
# startJVM(
#     jvmPath, 
#     '-server', 
#     '-Xmx8g', 
#     '-Xmn4g', 
#     '-Xms8g',
#     JAVA_EXT_DIRS
# )
# startJVM(
#     jvmPath,
#     settings.JVM_OPTIONS
# )

# from rocketmq.JVM import JVM
# env = JVM()
# env.start()

# from rocketmq.DefaultMQProducer import *
# from rocketmq.Message import *
# from rocketmq.DefaultMQPushConsumer import *

# def processMessages(msgs):
#     for msg in msgs:
#         print('[' + msg.getTopic() + '] [' + msg.getMsgId() + '] [' + msg.getBody() + ']')
    
#     return True

# producer = DefaultMQProducer('python_producer', '10.61.2.125:9876')
# producer.start()
# print('producer start...')
# msg = Message('PythonTest', '', '', 'this is a first message from python sdk.'.encode('utf-8'))
# for i in range(10):
#     producer.send(msg.getMessage())
# consumer = DefaultMQPushConsumer('python_push_consumer', '10.61.2.125:9876')
# consumer.subscribe('PythonTest', '')
# consumer.setClientIP('10.61.2.125')
# consumer.registerMessageListenerConcurrently(processMessages)
# consumer.start()
# print('consumer ip - ' + consumer.getClientIP())
# time.sleep(2 * 1000)
# consumer.shutdown()
# producer.shutdown()
# shutdownJVM()
# env.shutdown()

from pyrmq import *
producer = buildProducer('python_producer', '10.61.2.125:9876')
startProducer(producer)

for i in range(10):
    msg = buildMessage('PythonTest', '', '', ('message ' + str(i)).encode('utf-8'))
    print(sendMessage(producer.msg))

shutdownProducer(producer)
shutdownJVM()