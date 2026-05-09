# blockgen ![](https://img.shields.io/badge/python-3.9+-blue.svg)

**blockgen** is a Python3 module that allows reading and writing comment-delimited blocks inside files, which enables generating code next to traditionally handmade code efficiently.

**blockgen** can be seen as a _preprocessor_ for most file formats accepting comments (e.g. `.cpp`, `.html`, `.md`, `.py`, ...).

## Installation

```shell
$ pip install blockgen
```

## Reading blocks

Blocks are sections of a file delimited by the `<<[ block_name ]>>` and `<<[ end ]>>` markers :

```cpp
// main.cpp

// <<[ block1 ]>>
#include <iostream>
#include <vector>
// <<[ end ]>>

int main() {
    std::cout << /*<<[ block2 ]>>*/ "Hello world !" /*<<[ end ]>>*/ << std::endl;
    return 0;
}
```

...whose content can be easily retrieved with the `get_blocks` function :

```python
import blockgen

blocks: dict[str, str] = blockgen.file.get_blocks("/path/to/main.cpp")
assert blocks["block1"] == '#include <iostream>\n#include <vector>'
assert blocks["block2"] == '"Hello world !"'
```

## Writing blocks

The content of the blocks can also be modified with the `set_blocks` function :

```python
import blockgen

new_blocks = {
    "block1": '#include <iostream>\n#include <string>',
    "block2": '"Hello blockgen !"',
}
blockgen.file.set_blocks("/path/to/main.cpp", new_blocks)
```

...resulting in the following file :

```cpp
// main.cpp

// <<[ block1 ]>>
#include <iostream>
#include <string>
// <<[ end ]>>

int main() {
    std::cout << /*<<[ block2 ]>>*/ "Hello blockgen !" /*<<[ end ]>>*/ << std::endl;
    return 0;
}
```

## Reinjecting blocks

Blocks can be used to inject generated sections inside handwritten files, but the other way around is also possible: you can maintain handwritten sections inside generated files using the `write_and_reinject_blocks` function :

```python
import blockgen

file_content = """
void function_1() {
    // <<[ function_1_impl ]>>
    static_assert(false, "function_1 not implemented"); // TODO: implement me
    // <<[ end ]>>
}
"""

blockgen.file.write_and_reinject_blocks("/path/to/utils.cpp", file_content)
```

...which generates the following file :

```cpp
// utils.cpp

void function_1() {
    // <<[ function_1_impl ]>>
    static_assert(false, "function_1 not implemented"); // TODO: implement me
    // <<[ end ]>>
}
```

The file can then be modified by hand, and these handwritten sections will be preserved across future generations.

This means we can modify how the file is generated and execute `write_and_reinject_blocks` a second time :

```python
import blockgen

file_content = """
void function_1() {
    // <<[ function_1_impl ]>>
    static_assert(false, "function_1 not implemented"); // TODO: implement me
    // <<[ end ]>>
}
void function_2() {
    // <<[ function_2_impl ]>>
    static_assert(false, "function_2 not implemented"); // TODO: implement me
    // <<[ end ]>>
}
"""

blockgen.file.write_and_reinject_blocks("/path/to/utils.cpp", file_content)
```

...while still preserving the sections written by hand so far :

```cpp
// utils.cpp

void function_1() {
    // <<[ function_1_impl ]>>
    std::cout << "function_1" << std::endl; // Written by hand
    // <<[ end ]>>
}
void function_2() {
    // <<[ function_2_impl ]>>
    static_assert(false, "function_2 not implemented"); // TODO: implement me
    // <<[ end ]>>
}
```

This technique allows to seamlessly maintain handwritten code and generated code together in the same file, compared to traditionally having the generated code and handwritten code in separate files.

Under the hood, `write_and_reinject_blocks` is equivalent to :

```python
import blockgen

old_blocks = blockgen.file.get_blocks("/path/to/utils.cpp")
with open("/path/to/utils.cpp", "w") as f:
    f.write(file_content)
blockgen.file.set_blocks("/path/to/utils.cpp", old_blocks)
```

As a safety feature, all old blocks must be reinjected into the new file, inside each section with the same name, otherwise it will be considered as code loss and an exception will be raised. Human intervention is required to deal with such scenarios, like deleting the concerned blocks in the file before executing `write_and_reinject_blocks`.

## Integration in build pipelines

Integrating `blockgen` in your build pipeline is straightforward: simply call the concerned Python scripts from your build file (e.g. makefile, CMake file, Maven file, ...) before the compilation step.

All the write operations of `blockgen` are designed to only modify the files if the new content is different from the old one, avoiding unnecessary file modifications and thus unnecessary recompilations.

If some of your scripts require some additional dependencies, such as JSON files, you can configure your build pipeline to execute the concerned scripts only when these dependencies are modified, to save some build time.

## Integration with CI pipelines

In your CI pipeline (e.g. GitHub Actions, GitLab CI, Jenkins, ...), it is recommended for your CI job to check for source divergence after executing the scripts, and abort the job if any divergence is detected. For example with Jenkins, you can easily do that at the end of your Python scripts :

```python
import os
import subprocess

is_Jenkins_build = os.environ.get("JENKINS_URL") is not None \
                or os.environ.get("JENKINS_HOME") is not None \
                or os.environ.get("JENKINS_INSTANCE") is not None

if is_Jenkins_build:
    output = subprocess.check_output("git status --porcelain", shell=True).decode()
    if output:
        message = "Source divergence detected:\n\n"
        message += f"{output}\n"
        message += "Please build before pushing your changes."
        raise Exception(message)
```

This will ensure that all the generated code is part of the repository and that no one forgets to run the scripts before pushing their changes, which is a common source of friction when using code generation.

As for the question "Is it wise to push generated code ?", the philosophical answer is that without `blockgen` you would have to write the generated code by hand and push it anyway. If you have a lot of generated code, you can still do it the old way and try to have the handwritten code (part of the repository) and the generated code (not part of the repository) in separate files.

## Links

- [Documentation](https://github.com/ldflo/blockgen/blob/master/docs/doc_blockgen.md)
- [Examples](https://github.com/ldflo/blockgen/tree/master/examples/)
- [PyPI](https://pypi.org/project/blockgen/)
