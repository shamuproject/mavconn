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
period = 0.1
handler = 1.0
period2 = 0.2
handler2 = 2.0
period3 = 0.3
handler3 = 3

@freeze_time("2018-02-06 08:58:58")

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

def test_add_timer_work():
    test_case = MAVLinkConnection(mavfile)
    assert threading.active_count() == 1
    with test_case as m:
        test_case.add_timer(period, handler)
        test_case.add_timer(period2, handler2)
        test_case.add_timer(period3, handler3)
        assert threading.active_count() == 2
    assert threading.active_count() == 1
    
    
