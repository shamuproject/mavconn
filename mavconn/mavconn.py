"""Library provides a threadsafe, callback-based interface
     to the Python MAVLink library"""

import time
import threading
import datetime
from datetime import timedelta
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from heapq import heappush, heappop


class MAVLinkConnection:
    """Manages threads that handle mavlink messages

    Attributes
    ----------
        _mavfile : ()
            A generic mavlink port
        _mav_lock : ()
            Threading lock for mavfile
        _timer_thread : ()
            Thread that manages timers associated with periodic handlers
        _listening_thread : ()
            Thread that listens for mav messages and passes handlers to threadpool
        _threadpool : ()
            Pool of worker threads that execute handlers passed from timer/listening
            threads
        _stacks_lock: ()
            Threading lock for _stacks
        _stacks : (dict of str: func)
            Contains stacks for various MAVLink message types and the associated
            handlers for those message types. For example,
            {'Heartbeat',[handler1, handler2, handler3']}
        _futures : (list)
            Contains futures from jobs submitted to threadpool to keep track of
            unfinished jobs
        _timers : (list)
            A heap queue that stores and compares handlers based on
            the time to next call.
        _timers_cv: ()
            A condition variable that notifies the timer thread to start
            when a timer is added into the _timers heap queue.
        _continue: (bool)
            Keeps timer thread active in a loop while True.
        _continue_lock: ()
            Lock for _continue to ensure the boolean value can be toggled.
    """

    def __init__(self, mavfile):
        self._mavfile = mavfile
        self._mav_lock = threading.Lock()
        self._timer_thread = None
        self._listening_thread = None
        self._threadpool = None
        self._stacks_lock = threading.Lock()
        self._stacks = defaultdict(list)
        self._futures = []
        self._timers = []
        self._timers_cv = threading.Condition()
        self._continue = True
        self._continue_lock = threading.Lock()

    def start(self):
        """ Initializes the timer, listening, and handler worker threads."""
        self._threadpool = ThreadPoolExecutor()
        self._listening_thread = threading.Thread(target=self.listening_work)
        self._timer_thread = threading.Thread(target=self.timer_work)
        self._listening_thread.start()
        self._timer_thread.start()

    def stop(self):
        """ Stops the timer, listening, and handler worker threads."""
        with self._continue_lock:
            self._continue = False
        self._timer_thread.join()
        self._listening_thread.join()
        self._threadpool.shutdown()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()

    def push_handler(self, message_name, handler):
        """Pushes MAVLink message and associated handler unto appropriate stack

        Parameters
        ----------
        message_name : (str)
            The type of MAVLink message. For example, 'HEARTBEAT'
        handler : (func)
            The function that is to be performed
            (associated with a type of MAVLink message)
        """
        with self._stacks_lock:
            self._stacks[message_name].append(handler)

    def pop_handler(self, message_name):
        """Pops the last handler in a stack with a given MAVLink message type

        Parameters
        ----------
        message_name : (str)
            The type of MAVlink message. For example, 'HEARTBEAT'

        Returns
        -------
        handler : (func)
            The function that is to be performed
            (associated with a type of MAVLink message)
        """
        with self._stacks_lock:
            try:
                handler = self._stacks[message_name].pop()
                return handler
            except (KeyError, IndexError):
                raise KeyError('That message name key does not exist!')

    def clear_handler(self, message_name=None):
        """Removes all handlers in the stack assoc. with a given MAVLink message type

        Parameters
        ----------
        message_name : (str)
            The type of MAVLink message. For example, 'HEARTBEAT'
        """
        with self._stacks_lock:
            if message_name:
                self._stacks.pop(message_name)
            else:
                self._stacks.clear()

    def add_timer(self, period, handler):
        """Adds a timer object to heap queue with assoc. repeating period and handler

        Parameters
        ----------
        period : (int)
            The time period in seconds between each time the handler should be called
        handler : (func)
            The function that is to be performed at intervals indicated by
            the timer period)
        """
        with self._timers_cv:
            heappush(self._timers, Timer(period, handler))
            self._timers_cv.notify()

    def timer_work(self):
        """Target for the timer thread. Processes timers from/to the heap queue"""
        def get_cont_val():
            """Returns boolean which controls if 
                thread should keep running"""
            with self._continue_lock:
                return self._continue
        def timer_status():
            """Returns boolean and checks if heap is not empty"""
            return self._timers != []
        while get_cont_val():
            with self._timers_cv:
                self._timers_cv.wait_for(timer_status) #check if heap is empty
                current_timer = heappop(self._timers)
            current_timer.handle(self)
            with self._timers_cv:
                heappush(self._timers, current_timer)
                self._timers_cv.notify()

    def listening_work(self):
        """Target for the listening thread."""
        def get_cont_val():
            """Returns boolean which controls if 
                thread should keep running"""
            with self._continue_lock:
                return self._continue
        while get_cont_val():
            with self._stacks_lock:
                mav_message = self._mavfile.recv_match(
                    blocking=True, timeout=timedelta(milliseconds=100))
                try:
                    handler = self._stacks[mav_message.name][-1]
                    self._futures = [x for x in self._futures if not x.done()]
                    self._futures.append(self._threadpool.submit(
                        handler, self, mav_message))
                except:
                    try:
                        handler = self._stacks['*'][-1]
                        self._futures = [x for x in self._futures if not x.done()]
                        self._futures.append(self._threadpool.submit(
                            handler, self, mav_message))
                    except (KeyError, IndexError):
                        pass

    def __getattr__(self, name):
        '''Wrapper provides exclusionary access to mavfile; threadsafe'''
        def wrapper(*args, **kwargs):
            with self._mav_lock:
                return getattr(self._mavfile.mav, name)(*args, **kwargs)
        return wrapper


class Timer:
    """Creates objects with a time period interval, handler, and next calendar
    time for handler call.

    Note
    ----
    Timer objects are comparable based on their _next_time attribute.
    This is useful for popping and pushing onto the heap queue.

    Attributes
    ----------
        _period : (int)
            Time interval in seconds between when a handler is called and the next
            time the handler should be called.
        _handler : (func)
            The function that is to be performed at intervals indicated by
            the timer period
        _next_time : (datetime)
            A datetime that indicates the next calendar time a handler
            should be called.
    """

    def __init__(self, period, handler):
        self._period = period
        self._handler = handler
        self._futures = []
        current_time = datetime.datetime.now()
        period_seconds = timedelta(seconds=self._period)
        self._next_time = current_time + period_seconds

    def wait_time(self):
        """Delays timer thread until timer object _next_time is now"""
        current_time = datetime.datetime.now()
        delta_time = (self._next_time - current_time).total_seconds()
        if delta_time >= 0:
            time.sleep(delta_time)

    def handle(self, mavconn_instance):
        """Passes handler to worker thread and updates _next_time"""
        self.wait_time()
        self._futures = [x for x in self._futures if not x.done()]
        self._futures.append(mavconn_instance._threadpool.submit(
            self._handler, mavconn_instance))
        current_time = datetime.datetime.now()
        period_seconds = timedelta(seconds=self._period)
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
