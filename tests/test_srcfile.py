import os
import shutil

import pytest

from cmaker.config import Config
from cmaker.compiler import Compiler
from cmaker.fcentral import FCentral
from cmaker.dcentral import DCentral
from cmaker.srcfile import SrcFile

from tests.mock_fout import MockFout

DIR = os.path.dirname(__file__)
MOCK = os.path.join(DIR, "mock")
CONF = os.path.join(MOCK, "maker.config")
PROJ2 = os.path.join(MOCK, "project2")
PROJ2_MAIN = os.path.join(PROJ2, "main.cpp")
ABS = os.path.abspath(DIR)
H1 = os.path.join(PROJ2, "src", "h", "h1.h")
H1_CONTENT = "int h1();"
H1_TEMP_CONTENT = "int h1(); // hello!"

def write(fpath, msg):
    with open(fpath, "w") as f:
        os.fsync(f.fileno())
        f.write(msg)
        f.flush()

@pytest.fixture
def init():
    fcentral = FCentral()
    dcentral = DCentral(fcentral)
    config = Config.parse(CONF)
    
    if os.path.isdir(config.obj_dir):
        shutil.rmtree(config.obj_dir)
    
    yield (fcentral, dcentral, config)
    
    if os.path.isdir(config.obj_dir):
        shutil.rmtree(config.obj_dir)
    write(H1, H1_CONTENT)

def create_compiler(config):
    fout = MockFout()
    comp = Compiler(config.compile_cmd, fout)
    name = lambda s: os.path.join(
        config.obj_dir,
        ABS.replace(os.sep, config.obj_dirsep) + s
    )
    return fout, comp, name

def check_proj2_objs(objs, name):
    assert len(objs) == 4
    obj_set = {obj.fpath for obj in objs}
    expected = {
        name(".mock.project2.main.o"),
        name(".mock.project2.src.a1.o"),
        name(".mock.project2.src.h.h1.o"),
        name(".mock.project2.src.g.g1.o")
    }
    assert obj_set == expected

def test(init):
    fcentral, dcentral, config = init
    fout, compiler, name = create_compiler(config)
    srcfile = SrcFile.create(fcentral, dcentral, config, PROJ2_MAIN)
    objs = srcfile.rcompile(compiler)
    check_proj2_objs(objs, name)
    assert len(fout.record) == 4
    
    # recompile
    fout.record.clear()
    objs = srcfile.rcompile(compiler)
    check_proj2_objs(objs, name)
    assert len(fout.record) == 0  # no compilations made

    # adjust src/h/h1.h ==>
    #   src/h/h1.cpp,
    #   src/h/a1.cpp,
    #   src/g/g1.cpp
    # need to be compiled.
    write(H1, H1_TEMP_CONTENT)
    fcentral[H1].await_update(tries=100)
    fout.record.clear()
    objs = srcfile.rcompile(compiler)
    check_proj2_objs(objs, name)
    assert len(fout.record) == 3
