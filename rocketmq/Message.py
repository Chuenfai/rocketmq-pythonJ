from jpype import *
import logging

__all__ = ['Message']

MessageJ = JPackage('org.apache.rocketmq.common.message').Message

class Message:

    def __init__(self, topic, tags, keys, body):

        """ body must be type of bytes.
        """
        if not isinstance(body, bytes):
            raise Exception, "body must be type of bytes."
        else:    
            self.__topic = topic
            self.__tags = tags
            self.__keys = keys
            self.__body = body
            self.__message = MessageJ(JString(topic), JString(tags), JString(keys), body)

    def getMessage(self):
        return self.__message

    pass