import logging
import os
logging.basicConfig(
    level=logging.DEBUG,  
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',  
    datefmt='%a, %d %b %Y %H:%M:%S',  
    filename='client.log',  
    filemode='a'
)

ROCKETMQ_HOME = os.path.split(os.path.realpath(__file__))[0] + '/lib'
JAVA_EXT_DIRS = "-Djava.ext.dirs=" + ROCKETMQ_HOME

#startJVM中的options参数不能包含空格！只能一项一项填写
# JVM_OPTIONS = ['-server', '-Xms256m', '-Xmx256m', '-Xmn128m', JAVA_EXT_DIRS]
JVM_HEAP_XMS = '-Xms8g'
JVM_HEAP_XMX = '-Xmx8g'
JVM_HEAP_XMN = '-Xmn4g'
JVM_RUN_MODE = '-server'

pullMaxNums = 32
MsgBodyEncoding = 'utf-8'