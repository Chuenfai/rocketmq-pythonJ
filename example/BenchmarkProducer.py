# -*- coding: utf-8 -*-

import sys
import os
import time
from threading import Thread, Lock
sys.path.append(os.path.split(os.path.realpath(__file__))[0] + '/..')
from pyrmq import *

MESSAGE_NUM = 1000  # 100w total defalut
MESSAGE_SIZE = 1024  # 1kb per message default
THREAD_NUM = 64  # 64 threads to send message default
MESSAGE = "杨春晖123abc#$%"
TOPIC = 'python_producer'
NAMESRV = '10.61.2.125:9876'

SEND_LOCK = Lock()
SEND_MESSAGE_TOTAL = 0

if len(sys.argv) == 2 and int(sys.argv[1]):
    MESSAGE_NUM *= int(sys.argv[1])
elif len(sys.argv) == 3:
    if int(sys.argv[1]):
        MESSAGE_NUM *= int(sys.argv[1])
    if int(sys.argv[2]):
        MESSAGE_SIZE = sys.argv[2]
elif len(sys.argv) == 4:
    if int(sys.argv[1]):
        MESSAGE_NUM *= int(sys.argv[1])
    if int(sys.argv[2]):
        MESSAGE_SIZE = sys.argv[2]
    if int(sys.argv[3]):
        THREAD_NUM = sys.argv[3]

message = ""
while len(message) < MESSAGE_SIZE:
    message += MESSAGE

countdown = THREAD_NUM
def send(producer, number):
    while SEND_MESSAGE_TOTAL < MESSAGE_NUM:
        sendMessage(producer, message.encode('utf-8'))
        SEND_MESSAGE_TOTAL += 1
    with SEND_LOCK:
        countdown -= 1

def sampling(producer):
    last = 0
    start = time.time()
    while True:
        time.sleep(1000)
        print("send TPS: %d, total message: %d" % (SEND_MESSAGE_TOTAL - last, SEND_MESSAGE_TOTAL, ))
        last = SEND_MESSAGE_TOTAL
        if countdown <= 0:
            break
    print("cost time: %fs" % (time.time() - start, ))
    shutdownProducer(producer)


producer = buildProducer(TOPIC, NAMESRV)
startProducer(producer)
print("topic: %s, thread count: %d, message size: %d, total send: %d" % (TOPIC, THREAD_NUM, MESSAGE_SIZE, MESSAGE_NUM, ))

tmp = MESSAGE_NUM / THREAD_NUM
for i in range(THREAD_NUM):
    if i < THREAD_NUM - 1:
        Thread(target=send, args=(producer, tmp, )).start()
    else:
        Thread(target=send, args=(producer, MESSAGE_NUM - (i + 1) * tmp, ).start()

Thread(target=sampling, args=(producer, )).start()
