import os
import time
import threading

import pytest

from cmaker.mfile import MFile

DIR = os.path.dirname(__file__)
HELLO_CPP = os.path.join(DIR, "mock", "hello.cpp")

def test_nonexisting_file():
    mfile = MFile.create("nonexisting_file.blah")
    assert not mfile.exists
    mfile.update()
    assert not mfile.exists

def test_existing_file():
    mfile = MFile.create(HELLO_CPP)
    assert mfile.exists
    mtime = mfile.mtime
    mfile.update()
    assert mfile.mtime == mtime
    
    lines = list(mfile.parse())
    assert lines == [
        "int main() {",
        "    return 0;",
        "}"
    ]

def test_hash_eq():
    mfile = MFile.create(HELLO_CPP)
    twin = MFile(HELLO_CPP)
    assert hash(mfile) == hash(twin)
    assert mfile == twin
    negt = MFile("what.txt")
    assert not mfile == negt
    assert not hash(mfile) == hash(negt)

@pytest.fixture
def tempfile():
    fname = "temp.txt"
    mfile = MFile.create(fname)
    mfile.rm()
    assert not mfile.exists
    
    yield mfile
    
    mfile.rm()
    assert not mfile.exists
    
    mfile2 = MFile.create(fname)
    assert not mfile2.exists

def test_update(tempfile):
    thread = threading.Thread(target=tempfile.await_update)
    thread.start()
    
    with open(tempfile.fpath, "w") as f:
        time.sleep(0.01)
        os.fsync(f.fileno())
        f.write("hello world")
        f.flush()
    
    thread.join()
    assert tempfile.exists
    
    oldf = MFile.create(HELLO_CPP)
    assert oldf < tempfile
