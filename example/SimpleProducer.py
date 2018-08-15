import sys
import os
sys.path.append(os.path.split(os.path.realpath(__file__))[0] + '/..')

from pyrmq import *
producer = buildProducer('python_producer', '10.61.2.125:9876')
startProducer(producer)

for i in range(10):
    msg = buildMessage('PythonTest', '', '', ('杨春晖123abc#$% ' + str(i)).encode('utf-8'))
    res = sendMessage(producer, msg)
    print(res.getSendStatus())

shutdownProducer(producer)
# shutdownENV()