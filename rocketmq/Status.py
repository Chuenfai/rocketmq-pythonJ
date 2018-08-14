from jpype import *

__all__ = ['SendStatus', 'ConsumeConcurrentlyStatus']

_SendStatusJ = JPackage('org.apache.rocketmq.client.producer').SendStatus
_ConsumerConcurrentlyStatusJ = JPackage('org.apache.rocketmq.client.consumer.listener').ConsumerConcurrentlyStatus
_ConsumeOrderlyStatusJ = JPackage('org.apache.rocketmq.client.consumer.listener').ConsumeOrderlyStatus

SendStatus = {
    'SEND_OK': _SendStatusJ.SEND_OK,
    'FLUSH_DISK_TIMEOUT': _SendStatusJ.FLUSH_DISK_TIMEOUT,
    'FLUSH_SLAVE_TIMEOUT': _SendStatusJ.FLUSH_SLAVE_TIMEOUT,
    'SLAVE_NOT_AVAILABLE': _SendStatusJ.SLAVE_NOT_AVAILABLE
}

ConsumeConcurrentlyStatus = {
    'SUCCESS': _ConsumerConcurrentlyStatusJ.SUCCESS,
    'RECONSUME_LATER': _ConsumerConcurrentlyStatusJ.RECONSUME_LATER
}