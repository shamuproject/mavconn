from pymavlink.mavutil import mavudp
from collections import defaultdict


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
        except KeyError:
            raise KeyError('That message name key does not exist yet!')
        except IndexError:
            raise IndexError('No handlers for that message name exist!')

    def clear_handler(self, message_name):
        self._stacks.pop('message_name', None)

    def add_timer(period, handler):
        pass
