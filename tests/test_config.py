import os

from cmaker.config import Config

DIR = os.path.dirname(__file__)
CONF = os.path.join(DIR, "mock", "maker.config")

def test():
    config = Config.parse(CONF)
    assert config.c_ext == ".cpp"
    assert config.obj_dirsep == "."
    assert (
        config.combine_cmd == \
        "g++ -MMD --coverage {inp} -o {out}"
    )
