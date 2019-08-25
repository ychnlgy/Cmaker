import os

import pytest

from cmaker.config import Config

DIR = os.path.dirname(__file__)
CONF = os.path.join(DIR, "mock", "maker.config")
TEMP = "temp.config"

@pytest.fixture
def temp():
    if os.path.isfile(TEMP):
        os.remove(TEMP)
    yield Config.parse(CONF)
    if os.path.isfile(TEMP):
        os.remove(TEMP)

def test_parse():
    config = Config.parse(CONF)
    assert config.c_ext == ".cpp"
    assert config.obj_dirsep == "."
    assert (
        config.combine_cmd ==
        "g++ -MMD -std=c++98 --coverage -I../ {inp} -o {out}"
    )

def test_write(temp):
    temp.write(TEMP)
    config = Config.parse(TEMP)
    assert vars(temp) == vars(config)
