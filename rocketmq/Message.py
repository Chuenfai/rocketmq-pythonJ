from jpype import *
import logging

logger = logging.getLogger('Message')

__all__ = ['Message']

MessageJ = JPackage('org.apache.rocketmq.common.message').Message

class Message(object):

    def __init__(self, topic, tags, keys, body):
        if not isinstance(body, bytes):
            pass

        self.__topic = topic
        self.__tags = tags
        self.__keys = keys
        self.__body = body

        self.__message = MessageJ(JString(topic), JString(tags), JString(keys), body)

    def getMessage(self):
        return self.__message

    pass