import os

import pytest

from cmaker.dfile import DFile
from cmaker.fcentral import FCentral

DIR = "tests"
HARD_D = os.path.join(DIR, "mock", "hard.d")
PROJ1 = os.path.join(DIR, "mock", "project1")
MAIN_D = os.path.join(PROJ1, "main.d")
MAIN_O = os.path.join(PROJ1, "main.o")
HELPER1_D = os.path.join(PROJ1, "helper1.d")
HELPER1_C = os.path.join(PROJ1, "helper1.cpp")
HELPER1_H = os.path.join(PROJ1, "helper1.h")
NOSRC_D = os.path.join(PROJ1, "nosrc.d")
NOTARGET_D = os.path.join(PROJ1, "notarget.d")
NEWHEAD_D = os.path.join(PROJ1, "newhead.d")

@pytest.fixture
def fcentral():
    return FCentral()

def test_exist_nocompile(fcentral):
    mfile = fcentral[MAIN_D]
    ofile = fcentral[MAIN_O]
    hfile = fcentral[HELPER1_H]
    assert hfile < mfile
    assert hfile < ofile
    dfile = DFile.parse(fcentral, mfile)
    assert not dfile.should_compile()

def test_exist_srcnew(fcentral):
    mfile = fcentral[HELPER1_D]
    cfile = fcentral[HELPER1_C]
    assert mfile < cfile
    assert cfile.exists
    dfile = DFile.parse(fcentral, mfile)
    assert dfile.should_compile()

def test_nosrc(fcentral):
    mfile = fcentral[NOSRC_D]
    dfile = DFile.parse(fcentral, mfile)
    assert not dfile.should_compile()

def test_notarget(fcentral):
    mfile = fcentral[NOTARGET_D]
    dfile = DFile.parse(fcentral, mfile)
    assert dfile.should_compile()

def test_newheader(fcentral):
    mfile = fcentral[NEWHEAD_D]
    dfile = DFile.parse(fcentral, mfile)
    assert dfile.should_compile()

def test_shorthead(fcentral):
    mfile = fcentral[HARD_D]
    dfile = DFile.parse(fcentral, mfile)
    assert (
        dfile.recipe() == \
        "dump/mock.project2.src.h.h1.o:"
        " mock/project2/src/h/h1.cpp"
        " mock/project2/src/h/h1.h"
    )
