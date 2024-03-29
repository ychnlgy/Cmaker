# Cmaker
Recursive make-operation for sprawling C++ projects.

### Installation

```bash
pip3 install cmaker
```

### Command line use

Consider a C++ application entry source code at `main.cpp` that includes headers from various folders. To automatically discover its dependencies and compile what is necessary, do:

```bash
makerc.py --input main.cpp --output app.exe
```

This should produce `app.exe` in the current directory.

### Script use

```python3
import cmaker

maker = cmaker.Maker("<path-to-config>")
maker.make("<main>.cpp", "<out>")
```

### Custom arguments

Copy the following contents of the configuration file into `cmaker.config` in the working directory:

```config
c_ext = .cpp
obj_dirsep = .
obj_dir = dump
compile_cmd = g++ -MMD --coverage -c {inp} -o {out}
combine_cmd = g++ -MMD --coverage {inp} -o {out}
```

Change whatever your heart desires, but you MUST include the `-MMD` option for `g++` to produce dependency files.
