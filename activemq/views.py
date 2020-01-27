from django.shortcuts import render
import stomp
import sys
import time
from django.http.response import HttpResponse, HttpResponseBadRequest


class SampleListener(stomp.ConnectionListener):
    def __init__(self, conn):
        self.conn = conn

    def on_message(self, headers, message):
        print("headers:{0}['destination'], message:{1}".format(headers, message))
        destination = headers['destination']
        destination = destination[7:]
        # print(self.conn.ack(id=headers['message-id']))
        print(destination)

    def on_error(self, headers, message):
        print("headers:{0}['destination'], message:{1}".format(headers, message))


def testactivemq(request):
    conn = stomp.Connection10()
    conn.set_listener('SampleListener', SampleListener(conn))
    conn.connect()
    conn.subscribe('SampleQueue1', id=1)
    print()
    return HttpResponse('response {}'.format(1))


def send_to_queue(request, task_id):
    conn = stomp.Connection()
    conn.connect('admin', 'admin', wait=True)

    if task_id == '1':
        queue_1 = 'SampleQueue1'
        # send message
        message = 'test1'
        try:
            conn.send("{0}".format(queue_1), message)
            print('send {} to {}'.format(message, queue_1))
        except Exception:
            print('error:{0}'.format(task_id))

    elif task_id == '2':
        queue_2 = 'SampleQueue2'
        # send message
        message = 'test2'
        try:
            conn.send("{0}".format(queue_2), "test2")
            print('send {} to {}'.format(message, queue_2))
        except Exception:
            print('error:{0}'.format(task_id))

    elif task_id == '3':
        queue_3 = 'SampleQueue3'
        # send message
        message = 'test3'
        try:
            conn.send("{0}".format(queue_3), "test3")
            print('send {} to {}'.format(message, queue_3))
        except Exception:
            print('error:{0}'.format(task_id))

    conn.disconnect()

    # return task_id

    return HttpResponse('success!task{0}'.format(task_id))


def back_to_queue(request, task_id):
    conn = stomp.Connection()
    conn.connect('admin', 'admin', wait=True)

    if task_id == '1':
        queue_1 = 'SampleQueue1'
        # send message
        try:
            conn.send("{0}".format(queue_1), "test1")
        except Exception:
            print('error:{0}'.format(task_id))

    elif task_id == '2':
        queue_2 = 'SampleQueue2'
        # send message
        try:
            conn.send("{0}".format(queue_2), "test2")
        except Exception:
            print('error:{0}'.format(task_id))

    elif task_id == '3':
        queue_3 = 'SampleQueue3'
        # send message
        try:
            conn.send("{0}".format(queue_3), "test3")
        except Exception:
            print('error:{0}'.format(task_id))

    conn.disconnect()

    return HttpResponse('success!task{0}'.format(task_id))


def listen_from_queue(request, queue_id):
    conn = stomp.Connection10()
    conn.set_listener('SampleListener', SampleListener(conn))
    conn.connect()
    if queue_id == '1':
        try:
            conn.subscribe('SampleQueue1', ack='auto')
        except Exception as e:
            print('error:{0}'.format('error'))
    elif queue_id == '2':
        try:
            conn.subscribe('SampleQueue2', ack='auto')
        except Exception as e:
            print('error:{0}'.format('error'))
    elif queue_id == '3':
        try:
            conn.subscribe('SampleQueue3', ack='auto')
        except Exception as e:
            print('error:{0}'.format('error'))

    # conn.disconnect()
    return HttpResponse('Listen SampleQueue{} successfully!'.format(queue_id))

# Create your views here.
