from mavconn.mavconn import MAVLinkConnection

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
#	unittest.TestCase.assertRaises(test_mav,IndexError,test_mav.pop_handler,'TELEMETRY')
#	unittest.TestCase.assertRaises(test_mav,KeyError,test_mav.pop_handler,'NOTKEY')
	test_mav.clear_handler('HEARTBEAT')
	test_mav.clear_handler('TELEMETRY')
	assert test_mav._stacks == test_clear  
    
