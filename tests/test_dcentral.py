import os

from cmaker.dcentral import DCentral
from cmaker.fcentral import FCentral

DIR = os.path.dirname(__file__)
PROJ1 = os.path.join(DIR, "mock", "project1")
MAIN_D = os.path.join(PROJ1, "main.d")
HELPER1_D = os.path.join(PROJ1, "helper1.d")

def test():
    fcentral = FCentral()
    dcentral = DCentral(fcentral)
    
    main_d1 = dcentral[fcentral[MAIN_D]]
    assert not main_d1.should_compile()
    
    main_d2 = dcentral[fcentral[MAIN_D]]
    assert not main_d2.should_compile()
    
    assert id(main_d1) == id(main_d2)
    
    assert dcentral[fcentral[HELPER1_D]].should_compile()
