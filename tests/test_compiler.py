import os

import pytest

from cmaker.compiler import Compiler
from tests.mock_fout import MockFout

CMD = "python3 -c \"print({inp}, '{out}')\""
CMD2 = "python3 -c \"print({inp}, '{out}'); assert False\""
DIR = "temp"
OUT = os.path.join(DIR, "temp.txt")

@pytest.fixture
def fout():
    if os.path.isdir(DIR):
        os.rmdir(DIR)
    yield MockFout()
    if os.path.isdir(DIR):
        os.rmdir(DIR)

def test_success(fout):
    compiler = Compiler(CMD, fout)
    compiler.compile(inp=3, out=DIR)
    assert len(fout.record) == 1
    expect = CMD.format(inp=3, out=DIR)
    assert fout.record[0] == expect
    
    assert not os.path.isdir(DIR)
    compiler.compile(inp=4, out=OUT)
    expect = CMD.format(inp=4, out=OUT)
    assert fout.record[-1] == expect
    assert os.path.isdir(DIR)

def test_failure(fout):
    compiler = Compiler(CMD2, fout)
    with pytest.raises(Compiler.Error):
        compiler.compile(inp=3, out=DIR)
    expect = CMD2.format(inp=3, out=DIR)
    print(expect)
    assert fout.record[0] == expect
