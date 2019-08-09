import os
import time


REST_DT = 0.01


class MFile:
    
    @staticmethod
    def create(fpath):
        mfile = MFile(fpath)
        mfile.update()
        return mfile
    
    def parse(self):
        with open(self.fpath, "r") as f:
            for line in f:
                yield line.rstrip()
    
    def rm(self):
        if self.exists:
            os.remove(self.fpath)
            self.exists = False
            self.mtime = None
    
    def __init__(self, fpath):
        self.fpath = fpath
        self.exists = False
        self.mtime = None
    
    def __hash__(self):
        return hash(self.fpath)
    
    def __eq__(self, mfile):
        return self.fpath == mfile.fpath
    
    def __lt__(self, mfile):
        return self.mtime < mfile.mtime
    
    def update(self):
        self.exists = os.path.isfile(self.fpath)
        updated = False
        if self.exists:
            new_mtime = os.path.getmtime(self.fpath)
            updated = new_mtime > self.mtime
            self.mtime = new_mtime
        return updated
    
    def await_update(self):
        while not self.update():
            time.sleep(REST_DT)
