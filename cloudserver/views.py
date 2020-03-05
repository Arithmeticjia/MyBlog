from django.shortcuts import render
#from cloudserver.models import System_Monit
from django.views.decorators.csrf import csrf_exempt
import copy
import time
import psutil
import requests
import json
import numpy as np
import pandas as pd
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from django.http import HttpResponse
#from cloudserver.dcpower.feadeal import build_cpu_metric, calc_cpu_usage
#from cloudserver.dcpower.testpower import lasso_vm2pc_pred, lasso_vm2pc_train
#from cloudserver.dcpower.dockerpower import build_docker_metrics, calc_docker_power
#from cloudserver.dcpower.predpower import pcpower_pred_train, pcpower_pred
#from cloudserver.dcpower.nnpower import nn_vm2pc_train, nn_vm2pc_pred
from pandas import DataFrame
from pandas import concat
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense
import numpy


def chart(request):
    # 显示html文件
    return render(request, "cloudserver/line-time-series/index.htm")
    
    
def chart_pred(request):
    return render(request,"cloudserver/line-time-series/chart_pred.htm")


def getCPUstate(interval=1):
    cpu = psutil.cpu_percent(interval)
    return cpu


def getMemorystate():
    phymem = psutil.virtual_memory()
    cur_mem = phymem.percent
    mem_rate = int(phymem.used / 1024 / 1024)
    mem_all = int(phymem.total / 1024 / 1024)
    line = {
        'cur_mem': cur_mem,
        'mem_rate': mem_rate,
        'mem_all': mem_all,
    }
    return cur_mem


def server_cpu_json(request):
    data = []
    if request.method == "GET":
        i = 0
        while(i < 2):
            t = time.time()
            time_stamp = int(round(t * 1000))  # 转换为毫秒的时间戳
            cpu = getCPUstate()
            data.append([int(time_stamp), float('%.2f' % cpu)])
            print(data)
            i += 1
    isdict = json.dumps(data)  # json序列化列表
    return HttpResponse(isdict, content_type="application/json")
    
    
def server_mem_json(request):
    data = []
    if request.method == "GET":
        i = 0
        while(i < 2):
            t = time.time()
            time_stamp = int(round(t * 1000))  # 转换为毫秒的时间戳
            mem = getMemorystate()
            data.append([int(time_stamp), float('%.2f' % mem)])
            print(data)
            i += 1
    isdict = json.dumps(data)  # json序列化列表
    return HttpResponse(isdict, content_type="application/json")



def server_cpu_pred_json(request):
    data = []
    i = 0
    while (i < 30):
        t = time.time()
        time_stamp = int(round(t * 1000))  # 转换为毫秒的时间戳
        cpu = getCPUstate()
        data.append([int(time_stamp), float('%.2f' % cpu)])
        print(data)
        i += 1
    ori_data = copy.deepcopy(data)
    for i, cpu in enumerate(ori_data):
        del[cpu[0]]
    # to_csv = pd.DataFrame(columns=['time','cpu_info'], data=data)
    values = np.array(ori_data)
    dataset = values.astype('float32')
    # normalize the dataset
    scaler = MinMaxScaler(feature_range=(0, 1))
    dataset = scaler.fit_transform(dataset)
    # split into train and test sets
    train_size = int(len(dataset) * 0.67)
    test_size = len(dataset) - train_size
    train, test = dataset[0:train_size, :], dataset[train_size:len(dataset), :]
    # reshape dataset
    look_back = 3
    trainX, trainY = create_dataset(train, look_back)
    testX, testY = create_dataset(test, look_back)
    # create and fit Multilayer Perceptron model
    model = Sequential()
    model.add(Dense(12, input_dim=look_back, activation='relu'))
    model.add(Dense(8, activation='relu'))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    model.fit(trainX, trainY, epochs=100, batch_size=2, verbose=2)
    # model = load_model("/Users/Arithmetic/PycharmProjects/MyBlog/cloudserver/algorithm/airline_passengers/my_model.h5")
    trainScore = model.evaluate(trainX, trainY, verbose=0)
    trainPredict = model.predict(trainX)
    testPredict = model.predict(testX)
    mm = MinMaxScaler()
    trainPredict = mm.fit_transform(trainPredict)
    trainPredict = mm.inverse_transform(trainPredict)
    # print(trainPredict.tolist())
    tem = trainPredict.tolist()
    # print(data)
    # print(tem[0],len(tem),len(data))
    for i, item in enumerate(data[0:len(tem)]):
        item[1] = tem[i][0]
    # print(data)
    isdict = json.dumps(data)  # json序列化列表
    print("OJBK")
    return HttpResponse(isdict, content_type="application/json")
    

def chart_json(request):
    # 读取表所有记录
    system_monit = System_Monit.objects.all()
    data = []  # 创建一个空列表
    dic = {}
    for i in system_monit:  # 遍历，拼横纵坐标
        # 横坐标为时间戳,纵坐标为cpu使用率。注意，必须转换类型，否则数据不对。
        # t = int(i.time_stamp)
        # c = float('%.2f' % i.cpu)
        # dic['%d' % t] = c
        # data.append(dic)
        data.append([int(i.time_stamp), float('%.2f' % i.cpu)])

    # print(data)

    isdict = json.dumps(data)  # json序列化列表
    return HttpResponse(isdict, content_type="application/json")  # 执行类型为json

# Create your views here.
