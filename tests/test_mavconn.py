import pytest

from mavconn.mavconn import MAVLinkConnection
from mavconn.mavconn import Timer
from freezegun import freeze_time
from heapq import heappush, heappop
from pytest_mock import mocker
import datetime
import threading
import concurrent.futures
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

class MockMav:
    def recv_match(self, *args, **kwargs):
        pass

class MockMessage:
    def __init__(self, name):
        self.name = name

def test_initialization():
    test_mav = MAVLinkConnection(mavfile)
    assert test_mav.mav == 1.0
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
        handler = MockHandler()
        mocker.patch.object(MockMav, 'recv_match')
        mockmessage = MockMessage('HEARTBEAT')
        mockmav = MockMav()
        mockmav.recv_match.return_value = mockmessage
        test_case = MAVLinkConnection(mockmav)
        assert threading.active_count() == 1
        with test_case as m:
            test_case.push_handler('HEARTBEAT', handler2)
            test_case.add_timer(period2, handler2)
            test_case.add_timer(period, MockHandler.handler)
            test_case.add_timer(period3, handler3)
            assert threading.active_count() == 3
            MockHandler.handler.assert_not_called
            frozen_datetime.move_to(other_datetime)
            MockHandler.handler.assert_not_called
            frozen_datetime.move_to(last_datetime)
            time.sleep(0.5)
            MockHandler.handler.assert_called_with(test_case)
            test_case.pop_handler('HEARTBEAT')
            test_case.push_handler('*', handler2)
            time.sleep(0.5)
        assert threading.active_count() == 1

    
    
    
