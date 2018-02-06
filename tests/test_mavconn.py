import pytest

from mavconn.mavconn import MAVLinkConnection
from mavconn.mavconn import Timer

mavfile = 1.0
test_stack = {'HEARTBEAT':['handler1','handler2'],'TELEMETRY':['handler3']}
test_push = {'HEARTBEAT':['handler1','handler2'],'TELEMETRY':['handler3']}
test_clear = {}

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
    
