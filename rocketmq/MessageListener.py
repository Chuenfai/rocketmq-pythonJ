from jpype import *

__all__ = []

class MessageListenerConcurrently(object):
    
    def consumeMessage(self, msgs, context):
        
        pass


class MessageListenerOrderly(object):
    def consumeMessage(self, msgs, context):
        pass
    pass