from pymavlink.mavutil import mavudp


class MAVLinkConnection:
    """Definition of MAVCONN class"""

    def __init__(self, mavfile):
        self.mav = mavfile
	
    def push_handler(self, message, handler):
        pass

    def pop_handler(self, message):
        """return function(mav,message)"""
        pass

    def clear_handler(message):
        pass

    def add_timer(period, handler):
        pass
