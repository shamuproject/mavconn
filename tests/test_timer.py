import pytest
from freezegun import freeze_time
import datetime

from mavconn.mavconn import Timer

period = 1
handler = 5.0
time = datetime.datetime(2018,2,6,8,58,59)

@freeze_time("2018-02-06 08:58:58")

def test_timer_init():
    test_timer = Timer(period,handler)
    assert test_timer.period == 1
    assert test_timer.handler == 5.0
    assert test_timer._next_time == time
    
