import pytest
# from tracker.app.isobar_fixes import *
from isoba import *

@pytest.fixture()
def dummy_timeline():
    timeline = iso.Timeline(output_device=iso.io.DummyOutputDevice(), clock_source=iso.DummyClock())
    timeline.stop_when_done = True
    return timeline