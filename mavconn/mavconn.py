from pymavlink.mavutil import mavudp
from collections import defaultdict
import datetime
from datetime import timedelta
from heapq import heappush, heappop


class MAVLinkConnection:
    """Definition of MAVCONN class"""

    def __init__(self, mavfile):
        self.mav = mavfile
        self._stacks = defaultdict(list)
        self._timers = []

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

    def add_timer(self, period, handler):
        heappush(self._timers, Timer(period, handler))

class Timer:
    """Definition of Timer class"""

    def __init__(self, period, handler):
        self.period = period
        self.handler = handler
        current_time = datetime.datetime.now()
        period_seconds = timedelta(seconds=self.period)
        self._next_time = current_time + period_seconds

    def __eq__(self, other):
        if self is other:
            return True
        elif type(self) != type(other):
            return False
        else:
            return self._next_time == other._next_time

    def __lt__(self, other):
        return self._next_time < other._next_time

    def __le__(self, other):
        return self._next_time <= other._next_time

    def __ge__(self, other):
        return self._next_time >= other._next_time

    def __gt__(self, other):
        return self._next_time > other._next_time

    def __ne__(self, other):
        return self._next_time != other._next_time


