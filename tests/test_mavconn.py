from mavconn.mavconn import MAVLinkConnection

mavfile = 1.0

def test_initialization():
	test_mav = MAVLinkConnection(mavfile)
	assert test_mav.mav == 1.0
	assert test_mav._stacks == {}
