import os
import shutil

import pytest

from cmaker.maker import Maker

from tests.mock_fout import MockFout

TEMP = "temp"
TEMP_EXE = os.path.join(TEMP, "temp.exe")

DIR = os.path.dirname(__file__)
MOCK = os.path.join(DIR, "mock")
CONF = os.path.join(MOCK, "maker.config")
PROJ = os.path.join(MOCK, "project2")
MAIN = os.path.join(PROJ, "main.cpp")

@pytest.fixture
def init():
    
    fout = MockFout()
    maker = Maker(CONF, fout)
    
    if os.path.isdir(TEMP):
        shutil.rmtree(TEMP)
    
    if os.path.isdir(maker.config.obj_dir):
        shutil.rmtree(maker.config.obj_dir)
    
    yield fout, maker
    
    if os.path.isdir(maker.config.obj_dir):
        shutil.rmtree(maker.config.obj_dir)
    
    if os.path.isdir(TEMP):
        shutil.rmtree(TEMP)

def test(init):
    
    fout, maker = init
    
    assert len(fout.record) == 0
    assert not os.path.isfile(TEMP_EXE)
    
    maker.make(MAIN, TEMP_EXE)
    
    assert len(fout.record) == 5
    assert os.path.isfile(TEMP_EXE)
    t1 = os.path.getmtime(TEMP_EXE)
    
    fout.record.clear()
    maker.make(MAIN, TEMP_EXE)
    assert len(fout.record) == 0
    assert os.path.isfile(TEMP_EXE)
    t2 = os.path.getmtime(TEMP_EXE)
    
    assert t1 == t2
