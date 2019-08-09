import os


ERROR = """
FATAL ERROR: compilation returned non-zero status.
"""

class Compiler:
    
    def __init__(self, cmd):
        self.cmd = cmd
    
    def compile(self, inp, out):
        dpath = os.path.dirname(out)
        if not os.path.isdir(dpath):
            os.makedirs(dpath)
        
        cmd = self.cmd.format(inp=inp, out=out)
        print(cmd)
        if os.system(cmd):
            raise SystemExit(ERROR)
