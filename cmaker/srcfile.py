import os


H_EXT = ".h"
O_EXT = ".o"
D_EXT = ".d"


class SrcFile:
    
    @staticmethod
    def create(fcentral, dcentral, config, mfile):
        base = os.path.splitext(mfile.fpath)[0]
        h_mfile = fcentral[base + H_EXT]
        src_mfile = fcentral[base + config.c_ext]
        obj_name = base.replace("/", config.obj_dirsep).replace("\\", config.obj_dirsep)
        obj_base = os.path.join(config.obj_dir, obj_name)
        obj_mfile = fcentral[obj_base + O_EXT]
        dep_mfile = fcentral[obj_base + D_EXT]
        
        dfile = None
        if dep_mfile.exists:
            dfile = dcentral[dep_mfile]
        
        return SrcFile(
            fcentral=fcentral,
            h_mfile=mfile,
            c_mfile=src_mfile,
            o_mfile=obj_mfile,
            d_mfile=dep_mfile,
            dfile=dfile
        )
    
    def __init__(self, fcentral, h_mfile, c_mfile, o_mfile, d_mfile, dfile):
        self.fcentral = fcentral
        self.h_mfile = h_mfile
        self.c_mfile = c_mfile
        self.o_mfile = o_mfile
        self.d_mfile = d_mfile
        self.dfile = dfile
    
    def rcompile(self, compiler):
        return self._rcompile(compiler, visited=set(), obj_mfiles=[])
    
    def compile(self, compiler):
        if self.should_compile():
            compiler.compile(inp=self.c_mfile.fpath, out=self.o_mfile.fpath)
            self.o_mfile.await_update()
            self.d_mfile.await_update()
            assert not self.should_compile()
    
    def should_compile(self):
        return self.dfile is None or self.dfile.should_compile()

    # === PRIVATE ===
    
    def _rcompile(self, compiler, visited, obj_mfiles):
        
        self.compile(compiler)
        if self.o_mfile.exists:
            obj_mfiles.append(self.o_mfile)
        
        # Block cyclic future visits again
        visited.add(self.h_mfile)
        
        if self.dfile is not None:
            for h_mfile in self.dfile.h_deps:
                
                if h_mfile not in visited:
                    
                    # Block cyclic future visits again
                    visited.add(h_mfile)
                    
                    srcfile = SrcFile.create(
                        fcentral=self.fcentral,
                        dcentral=self.dcentral,
                        config=self.config,
                        mfile=h_mfile
                    )
                    srcfile._rcompile(compiler, visited, obj_mfiles)
        
        assert len(obj_mfiles) == len(set(obj_mfiles))
        return obj_mfiles
