import pytest
from freezegun import freeze_time

from mavconn.mavconn import Timer

@freeze_time("")

def test_timer_init():
    test_timer = Timer()
