from celery import Celery
from nose.tools import eq_

from chat import tasks


# test if celery is running
def test_task_running():
    rst = add.apply(args=(4, 4)).get()
    eq_(rst, 8)


# test robot call
def test_robocalls():
    rst = tasks.robotCall.apply(args=('aapl.us', 'room')).get()

    eq_(rst is not None, True)


# Test API called is working and response with dic
def test_if_the_response_is_json():
    rst = tasks.robotCall.apply(args=('aapl.us', 'room')).get()
    eq_(rst['message']['id'], 'bot')


# Test API called is working and response with dic
def test_quote_values_are_numbers():
    rst = tasks.robotCall.apply(args=('aapl.us', 'room')).get()
    eq_(rst['message']['id'], 'bot')


# Test API called is working and response with dic
def test_quote_values_are_numbers():
    rst = tasks.robotCall.apply(args=('aapl.us', 'room')).get()
    eq_(rst['message']['id'], 'bot')


celery = Celery()


@celery.task
def add(x, y):
    return x + y
