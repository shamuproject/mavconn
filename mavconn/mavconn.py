from pymavlink.mavutil import mavudp
from collections import defaultdict
import datetime
from datetime import timedelta


class MAVLinkConnection:
    """Definition of MAVCONN class"""

    def __init__(self, mavfile):
        self.mav = mavfile
        self._stacks = defaultdict(list)

    def push_handler(self, message_name, handler):
        self._stacks[message_name].append(handler)

    def pop_handler(self, message_name):
        """return function(mav,message)"""
        try:
       	    handler = self._stacks[message_name].pop()
       	    return handler
        except (KeyError, IndexError):
            raise KeyError('That message name key does not exist!')

    def clear_handler(self, message_name=None):
        if message_name:
            self._stacks.pop(message_name)
        else:
            self._stacks.clear()

    def add_timer(period, handler):
        pass

class Timer:
    """Definition of Timer class"""

    def __init__(self, period, handler):
        self.period = period
        self.handler = handler
        current_time = datetime.datetime.now()
        period_seconds = timedelta(seconds=self.period)
        self._next_time = current_time + period_seconds
        
