from jpype import *
from rocketmq import Settings

class JVM:

    def start():
        jvmPath = getDefaultJVMPath()
        startJVM(
            jvmPath, 
            Settings.JVM_RUN_MODE, 
            Settings.JVM_HEAP_XMS, 
            Settings.JVM_HEAP_XMX, 
            Settings.JVM_HEAP_XMN,
            Settings.JAVA_EXT_DIRS
        )

    def shutdown():
        shutdownJVM()
        