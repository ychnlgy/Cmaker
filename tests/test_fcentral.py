from cmaker.fcentral import FCentral

def test():
    fcentral = FCentral()
    key = "./temp.txt"
    mfile = fcentral[key]
    key2 = "temp.txt"
    mfile2 = fcentral[key2]
    assert id(mfile) == id(mfile2)
