import pytest
from freezegun import freeze_time
import datetime
from heapq import heappush, heappop

from mavconn.mavconn import Timer
from mavconn.mavconn import MAVLinkConnection

period = 1
period2 = 2
handler = 5.0
mavfile = 3.0
time = datetime.datetime(2018,2,6,8,58,59)

@freeze_time("2018-02-06 08:58:58")

def test_timer_init():
    test_timer = Timer(period,handler)
    test_timer2 = Timer(period2,handler)
    test_timer3 = Timer(period,handler)
    assert test_timer.period == 1
    assert test_timer.handler == 5.0
    assert test_timer._next_time == time
    assert test_timer2 > test_timer
    assert test_timer2 >= test_timer
    assert (test_timer2 < test_timer) == False
    assert (test_timer2 <= test_timer) == False
    assert test_timer2 != test_timer
    assert test_timer2 == test_timer2
    assert test_timer == test_timer3
    assert (test_timer == period) == False

def test_add_timer():
    add_test = MAVLinkConnection(mavfile)
    assert add_test._timers == []
