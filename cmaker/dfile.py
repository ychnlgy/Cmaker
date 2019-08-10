class DFile:
    
    @staticmethod
    def parse(fcentral, mfile):
        fit = mfile.parse()
        
        head = next(fit)
        target, all_deps = head.split(": ")
        all_deps = _clean(all_deps)
        src = all_deps[0]
        h_deps = all_deps[1:]
        for subs in map(_clean, fit):
            h_deps.extend(subs)
        
        target = fcentral[target]
        src = fcentral[src]
        h_deps = [
            fcentral[h_dep]
            for h_dep in filter(None, h_deps)
        ]
        return DFile(mfile, target, src, h_deps)
    
    def __init__(self, d_mfile, target, src, h_deps):
        self.d_mfile = d_mfile
        self.target = target
        self.src = src
        self.h_deps = h_deps
    
    def should_compile(self):
        
        if not self.src.exists:
            return False
            
        else:
            
            if not self.target.exists:
                return True
            
            for h_mfile in self.h_deps:
                if self._check_header_age(h_mfile):
                    return True

            return self._check_src_age()
    
    # === PRIVATE ===
    
    def _check_header_age(self, h_mfile):
        return not h_mfile.exists or self._check_dep_age(h_mfile)

    def _check_dep_age(self, mfile):
        return self.target < mfile or self.d_mfile < mfile
    
    def _check_src_age(self):
        return self._check_dep_age(self.src)

# === PRIVATE ===

def _clean(line):
    return line.rstrip(" \\").rstrip().split(" ")
