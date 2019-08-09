class Config:
    
    @staticmethod
    def parse(fpath):
        kwargs = {}
        with open(fpath, "r") as f:
            for line in map(str.strip, f):
                if line and line[0] != "#":
                    k, v = line.split("=")
                    kwargs[k.strip()] = v.strip()
        return Config(**kwargs)
    
    def __init__(
        self,
        c_ext,
        obj_dirsep,
        obj_dir,
        compile_args,
        compile_cmd,
        combine_args,
        combine_cmd
    ):
        self.c_ext = c_ext
        self.obj_dirsep = obj_dirsep
        self.obj_dir = obj_dir
        self.compile_cmd = compile_cmd
        self.combine_cmd = combine_cmd
