from mavconn.mavconn import MAVLinkConnection

mavfile = 1.0
test_stack = {'HEARTBEAT':['handler1','handler2'],'TELEMETRY':['handler1']}

def test_initialization():
	test_mav = MAVLinkConnection(mavfile)
	assert test_mav.mav == 1.0
	assert test_mav._stacks == {}
	test_mav.push_handler('HEARTBEAT','handler1')
	test_mav.push_handler('HEARTBEAT','handler2')
	test_mav.push_handler('TELEMETRY','handler1')
	assert test_mav._stacks == test_stack
