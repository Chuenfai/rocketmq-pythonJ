import sys
import os
sys.path.append(os.path.split(os.path.realpath(__file__))[0] + '/..')

from pyrmq import *
producer = buildProducer('python_producer', '10.61.2.125:9876')
startProducer(producer)

for i in range(10):
    msg = buildMessage('PythonTest', '', '', ('message ' + str(i)).encode('utf-8'))
    res = sendMessage(producer, msg)
    print(type(res))
    print(res)

shutdownProducer(producer)
# shutdownENV()