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
    assert test_timer._period == 1
    assert test_timer._handler == 5.0
    assert test_timer._next_time == time
    assert test_timer2 > test_timer
    assert test_timer2 >= test_timer
    assert not (test_timer2 < test_timer)
    assert not (test_timer2 <= test_timer)
    assert test_timer2 != test_timer
    assert test_timer2 == test_timer2
    assert test_timer == test_timer3
    assert not (test_timer == period)

#def test_add_timer():
#    add_test = MAVLinkConnection(mavfile)
#    add_test.start()
#    assert add_test._timers == []
#    add_test.stop()
    
#def test_timer_handler():
#    handler_test = MAVLinkConnection(mavfile)
#    handler_test.start()
#    timer_test = Timer(period,handler)
#    timer_test.handle(handler_test)
#    handler_test.stop()
