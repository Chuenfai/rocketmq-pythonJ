# -*- coding: utf-8 -*-

import sys
import os
import time
from threading import Thread, Lock
sys.path.append(os.path.split(os.path.realpath(__file__))[0] + '/..')
from pyrmq import *

MESSAGE_NUM = 1000  # 100w total defalut
MESSAGE_SIZE = 1024  # 1kb per message default
THREAD_NUM = 1  # 64 threads to send message default
MESSAGE = '杨春晖123abc#$%'
TOPIC = 'PythonBenchmarkTest'
PRODUCER_GROUP = 'python_benchmark_producer'
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

m = ""
while len(m) < MESSAGE_SIZE:
    m += MESSAGE
print(m)
SEND_MESSAGE = buildMessage(TOPIC, '', '', m.encode('utf-8'))

COUNT_DOWN = THREAD_NUM
def send(p, number):
    global SEND_MESSAGE_TOTAL, SEND_LOCK, COUNT_DOWN, SEND_MESSAGE
    while number:
        res = sendMessage(p, SEND_MESSAGE)
        SEND_MESSAGE_TOTAL += 1
        number -= 1
    print('message send finished!')
    # with SEND_LOCK:
    #     COUNT_DOWN -= 1

producer = buildProducer(PRODUCER_GROUP, NAMESRV)
startProducer(producer)
print("topic: %s, thread count: %d, message size: %d, total send: %d" % (TOPIC, THREAD_NUM, MESSAGE_SIZE, MESSAGE_NUM, ))

tmp = int(MESSAGE_NUM / THREAD_NUM)
for i in range(THREAD_NUM):
    if i < THREAD_NUM - 1:
        send_per_thread = tmp
    else:
        send_per_thread = MESSAGE_NUM - i * tmp
    t = Thread(target=send, args=(producer, send_per_thread, ))
    t.start()
    print('thread %s started, which will produce %d messages.' % (t.getName(), tmp, ))
# send(producer, tmp)

def sampling(producer):
    global COUNT_DOWN, SEND_MESSAGE_TOTAL
    last = 0
    start = time.time()
    stop = 0
    while True:
        time.sleep(1)
        print("send TPS: %d, total message: %d" % (SEND_MESSAGE_TOTAL - last, SEND_MESSAGE_TOTAL, ))
        last = SEND_MESSAGE_TOTAL
        if COUNT_DOWN <= 0:
            time.sleep(5)
            stop = time.time()
            break
    print("cost time: %fs" % (stop - start, ))
    # shutdownProducer(producer)

# def sampling(producer):
#     global COUNT_DOWN, SEND_MESSAGE_TOTAL
#     last = 0
#     start = time.time()
#     while True:
#         time.sleep(1)
#         print("send TPS: %d, total message: %d" % (SEND_MESSAGE_TOTAL - last, SEND_MESSAGE_TOTAL, ))
#         SEND_MESSAGE_TOTAL = 0
#         last = SEND_MESSAGE_TOTAL
#         if SEND_MESSAGE_TOTAL >= 10:
#             break
#     print("cost time: %fs" % (time.time() - start, ))

t = Thread(target=sampling, args=(producer, ))
t.start()
print('sampling thread ' + t.getName() + ' started.\n')