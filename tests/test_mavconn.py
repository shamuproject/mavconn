import pytest

from mavconn.mavconn import MAVLinkConnection
from mavconn.mavconn import Timer
from freezegun import freeze_time
from heapq import heappush, heappop
from pytest_mock import mocker
import datetime
import threading
from concurrent.futures import ThreadPoolExecutor
import time

mavfile = 1.0
test_stack = {'HEARTBEAT':['handler1','handler2'],'TELEMETRY':['handler3']}
test_push = {'HEARTBEAT':['handler1','handler2'],'TELEMETRY':['handler3']}
test_clear = {}
period = 2
handler = 1.0
period2 = 3
handler2 = 2.0
period3 = 4
handler3 = 3

class MockHandler:
    def handler(self, mavconn_instance):
        pass

    def handler2(self, mav_message):
        pass

    def handler3(self, mav_message):
        pass

    def handler4(self, mav_message):
        pass

class MockMav:
    def recv_match(self, *args, **kwargs):
        pass

class MockMessage:
    def __init__(self, name):
        self.name = name

class Mav:
    def ping_send(self):
        pass

    def heartbeat_send(self):
        time.sleep(5)

class MockMavWrapper:
    def __init__(self, mav):
        self.mav = mav

def test_initialization():
    test_mav = MAVLinkConnection(mavfile)
    assert test_mav._mavfile == 1.0
    assert test_mav._stacks == {}
    test_mav.push_handler('HEARTBEAT','handler1')
    test_mav.push_handler('HEARTBEAT','handler2')
    test_mav.push_handler('TELEMETRY','handler3')
    assert test_mav._stacks == test_stack
    handler_test = test_mav.pop_handler('TELEMETRY')
    assert handler_test == 'handler3'
    with pytest.raises(KeyError, message="That message name key does not exist!"):
        test_mav.pop_handler('TELEMETRY')
    test_mav.clear_handler('TELEMETRY')
    test_mav.clear_handler()
    assert test_mav._stacks == test_clear

def test_add_timer_work(mocker):
    initial_datetime = datetime.datetime(year=2018, month=2, day=6, hour=8, minute=50, second=3)
    other_datetime = datetime.datetime(year=2018, month=2, day=6, hour=8, minute=50, second=4)
    last_datetime = datetime.datetime(year=2018, month=2, day=6, hour=8, minute=50, second=6)
    with freeze_time(initial_datetime) as frozen_datetime:
        mocker.patch.object(MockHandler, 'handler')
        mocker.patch.object(MockHandler, 'handler2')
        mocker.patch.object(MockHandler, 'handler3')
        mocker.patch.object(MockHandler, 'handler4')
        handler = MockHandler()
        mocker.patch.object(MockMav, 'recv_match')
        mockmessage = MockMessage('HEARTBEAT')
        mockmav = MockMav()
        mockmav.recv_match.return_value = mockmessage
        test_case = MAVLinkConnection(mockmav)
        assert threading.active_count() == 1
        with test_case as m:
            assert threading.active_count() == 3
            MockHandler.handler2.assert_not_called
            MockHandler.handler3.assert_not_called
            test_case.push_handler('HEARTBEAT', MockHandler.handler2)
            test_case.push_handler('*', MockHandler.handler3)
            test_case.push_handler('TELEMETRY', MockHandler.handler4)
            time.sleep(0.2)
            MockHandler.handler2.assert_called_with(test_case, mockmessage)
            test_case.add_timer(period2, handler2)
            test_case.add_timer(period, MockHandler.handler)
            test_case.add_timer(period3, handler3)
            MockHandler.handler.assert_not_called
            frozen_datetime.move_to(other_datetime)
            MockHandler.handler.assert_not_called
            frozen_datetime.move_to(last_datetime)
            time.sleep(0.5)
            MockHandler.handler.assert_called_with(test_case)
            MockHandler.handler3.assert_not_called
            test_case.pop_handler('HEARTBEAT')
            time.sleep(0.5)
            MockHandler.handler3.assert_called_with(test_case, mockmessage)
            MockHandler.handler4.assert_not_called
        assert threading.active_count() == 1

def test_wrapper(mocker):
    futures = []
    mocker.patch.object(Mav, 'ping_send')
    mocker.patch.object(Mav, 'heartbeat_send')
    mav = Mav()
    mock_mav = MockMavWrapper(mav)
    test_case = MAVLinkConnection(mock_mav)
    mav.ping_send.assert_not_called()
    threadpool = ThreadPoolExecutor()
    futures.append(threadpool.submit(test_case.heartbeat_send))
    futures.append(threadpool.submit(test_case.ping_send))
    assert futures[0].done() is not True
    mav.ping_send.assert_called_with()
    time.sleep(3)
    assert futures[1].done() is not True
    time.sleep(3)
    assert futures[0].done() is True
    assert futures[1].done() is True
    threadpool.shutdown()
    
