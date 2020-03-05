# #!/bin/bash
#
# import threading
# import time
# import os
# import string
# import sys
#
#
# class ControlThread(threading.Thread):
#
#     def __init__(self):
#         threading.Thread.__init__(self)
#         self.runflag = True  # 线程运行标示，用于将来减少线程时能够正常结束
#
#     def run(self):
#         while self.runflag:
#             # os.popen('sleep ' + sys.argv[5])
#             time.sleep(int(sys.argv[5]))
#
#     # 这里使用的是linux下shell里面的usleep，而不是python自带的sleep函数。
#     # 相比之下，usleep还是相当强大的，而python的sleep单位为秒，虽然可以输入浮点数，但还是相对弱了些
#
#     def stop(self):
#         self.runflag = False
#
#
# # 让其正常终止循环
# threadList = []
#
# print('Start Thread Number:' + sys.argv[3] + '\tSleep Time(ms):' + sys.argv[5])
#
# # 初始化一定数量的线程，否则从零开始，可能需要很长的时间才能达到指定范围
# for i in range(0, int(sys.argv[3])):
#     thread = ControlThread()
#     threadList.append(thread)
#     thread.start()
#
# # 这里使用sar来抓取cpu利用率，这里指的是总的cpu利用率。然后通过比较，进行自适应调整
# while True:
#     output = 100 - int(os.popen('sar 1 1 | grep ^Average | awk \'{print $8}\'').read())
#     print('CPU Usage:' + str(output) + '\tCurrent Thread Number:' + str(len(threadList)))
#
#     if output < int(sys.argv[1]):  # 增加线程
#         for i in range(0, int(sys.argv[4])):
#             thread = ControlThread()
#             thread.start()
#             threadList.append(thread)
#         print("+++++")
#     if output > int(sys.argv[2]):  # 减少线程
#         for i in range(0, int(sys.argv[4])):
#             thread = threadList.pop()
#             thread.stop()
#         print("-----")

import ctypes
ll = ctypes.cdll.LoadLibrary
lib = ll("./control_cpu")
lib.main()
